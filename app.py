from tkinter.messagebox import RETRY
import os, csv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import numpy as np


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = './______submissions/'
db = SQLAlchemy(app)

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(15), nullable=False)
    member1_id = db.Column(db.String(15))
    member2_id = db.Column(db.String(15))
    member3_id = db.Column(db.String(15))
    member4_id = db.Column(db.String(15))
    member5_id = db.Column(db.String(15))

class Submission(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, primary_key=True)
    submitted = db.Column(db.Boolean)
    time = db.Column(db.DateTime)

class Decision(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), primary_key=True)
    rank1 =  db.Column(db.Float, nullable=False)
    rank2 =  db.Column(db.Float, nullable=False)
    rank3 =  db.Column(db.Float, nullable=False)
    rank4 =  db.Column(db.Float, nullable=False)
    rank5 =  db.Column(db.Float, nullable=False)
    decision =  db.Column(db.Float, nullable=False)

class Performance(db.Model):
     submission_id = db.Column(db.Integer, primary_key=True)
     group_id = db.Column(db.Integer, primary_key=True)
     rps = db.Column(db.Float)
     #ret = db.Column(db.Float)
     #sdp = db.Column(db.Float)
     #ir = db.Column(db.Float)
     #rps_rank = db.Column(db.Integer)
     #ir_rank = db.Column(db.Integer)
     #overall_ranking = db.Column(db.Integer)




## ------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')
## ------------------------------------------------------------------
@app.route('/groups/', methods=['POST', 'GET'])
def groups():
    if request.method == 'POST':
        gid = request.form['group_id']
        gname = request.form['group_name']
        m1_id = request.form['member1_id']
        m2_id = request.form['member2_id']
        m3_id = request.form['member3_id']
        m4_id = request.form['member4_id']
        m5_id = request.form['member5_id']
        new_group = Group(group_id=gid, group_name=gname, member1_id=m1_id, member2_id=m2_id, member3_id=m3_id, member4_id=m4_id, member5_id=m5_id)
        try:
            db.session.add(new_group)
            db.session.commit()
            return redirect('/groups/')
        except:
            return "There was an issue adding your group!"
    else:
        groups = Group.query.order_by(Group.group_id).all()
        return render_template('groups.html', groups=groups)
## ------------------------------------------------------------------
def allowed_file(filename): # checks to make sure submission file is a csv file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "csv"

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        #return request.form
        gid = request.form['group_id']
        sid = request.form['submission_id']
        file = request.files['portfolio_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            with open(filepath) as this_file:
                csv_file = csv.DictReader(this_file)
                total_weight = 0
                decisions = []

                for row in csv_file:
                    if round(float(row['rank1']) + float(row['rank2']) + float(row['rank3']) + float(row['rank4']) + float(row['rank5']), 3) != 1:
                        return "Error: " + str(row["id"]) + "'s ranks do not sum to unity"
                    total_weight += float(row['decision'])
                    decisions.append(Decision(group_id=gid, submission_id=sid, symbol=row['id'], rank1=row['rank1'], \
                        rank2=row['rank2'], rank3=row['rank3'], rank4=row['rank4'], rank5=row['rank5'], decision = row['decision']))

                if len(decisions) != 110:
                    return "Error: Portfolio should have 110 rows!"
                elif round(total_weight, 3) != 1:
                    return "Error: Portfolio should have weights (decisions) summing to 1!"
                else:
                    for decision in decisions:
                        try:
                            db.session.add(decision)
                            db.session.commit()
                        except:
                            return "There was an issue adding data in for stock " + str(decision['id'])
            return """
            <!doctype html>
            <title>File Submitted</title>
            <h3>Portfolio Submitted Successfully</h3>
            <a href="../">Back to Home</a>
            """
        else:
            return """
            <!doctype html>
            <title>File Error</title>
            <h3>File error - make sure file's type is .csv</h3>
            <a href=".">Try Again</a>
            """
    else:
        return render_template('submit.html')
## ------------------------------------------------------------------
@app.route('/portfolios/', methods=['POST', 'GET'])
def portfolios():
    if request.method == 'POST':    
        portfolios = Decision.query.order_by(Decision.submission_id, Decision.group_id).all()
        return render_template('portfolios.html', portfolios=portfolios)


## ------------------------------------------------------------------
def getRPS(gid: int, sid: int):
    try:
        portfolio = Decision.query.filter_by(group_id=gid).filter_by(submission_id=sid).first()
        sample = Decision.query.filter_by(group_id=-999).filter_by(submission_id=sid).first()
    except:
        return "Unexpected error in getRPS"
    f_array = np.array([[portfolio.rank1, portfolio.rank2, portfolio.rank3, portfolio.rank4, portfolio.rank5]])
    f = np.cumsum(f_array, axis=1)
    q_array = np.array([[sample.rank1, sample.rank2, sample.rank3, sample.rank4, sample.rank5]])
    q = np.cumsum(q_array, axis=1)
    return float(np.sum((q-f)**2,axis=1)/f.shape[1])

@app.route('/performance/', methods=['POST', 'GET'])
def performance():
    if request.method == 'POST':
        gid = request.form['group_id']
        sid = request.form['submission_id']
        try:
            performance = Performance.query.filter_by(group_id=gid).filter_by(submission_id=sid).first()
        except:
            new_rps = getRPS(gid, sid)
            new_perf = Performance(group_id=gid, submission_id=sid, rps=new_rps)
            try:
                db.session.add(new_perf)
                db.session.commit()
            except:
                return "error adding new perf"
            performance = Performance.query.filter_by(group_id=gid).filter_by(submission_id=sid).first()
            return render_template('performance.html', data=performance)
    else:
        return render_template('performance_inquiry.html')







if __name__ == "__main__":
    app.run(debug=True)