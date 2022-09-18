from DataDrivenFinance import app
from DataDrivenFinance.databases import db, Group, Decision
from flask import request, render_template
from werkzeug.utils import secure_filename
import os
import csv


def allowed_file(filename):  # checks to make sure submission file is a csv file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "csv"


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        gid = request.form['group_id']
        if Group.query.filter_by(group_id=gid).first() is None:
            return """
                <!doctype html>
                <title>Error</title>
                <h3>Error: Group ID not found</h3>
                <a href=".">Try Again</a>
                """
        sid = request.form['submission_id']
        if Decision.query.filter_by(group_id=gid, submission_id=sid).all():
            all_prev = Decision.query.filter_by(
                group_id=gid, submission_id=sid).all()
            for record in all_prev:
                db.session.delete(record)
            db.session.commit()
            erased = True
        else:
            erased = False
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
                    total_weight += abs(float(row['decision']))
                    decisions.append(Decision(group_id=gid, submission_id=sid, symbol=row['id'], rank1=row['rank1'],
                                              rank2=row['rank2'], rank3=row['rank3'], rank4=row['rank4'], rank5=row['rank5'], decision=row['decision']))
                if len(decisions) != 110:
                    return """
                        <!doctype html>
                        <title>Error</title>
                        <h3>Error: Portfolio must have 110 rows!</h3>
                        <a href=".">Try Again</a>
                        """
                elif round(total_weight, 3) != 1:
                    return """
                        <!doctype html>
                        <title>Error</title>
                        <h3>Error: Portfolio should have weights (decisions) summing to 1!</h3>
                        <a href=".">Try Again</a>
                        """
                else:
                    for decision in decisions:
                        try:
                            db.session.add(decision)
                            db.session.commit()
                        except:
                            return "Error: There was an issue adding data for stock " + str(decision.symbol)
            this_file.close()
            os.remove(this_file.name)
            return render_template('submit/submit_success.html', update=erased)
        else:
            return """
                <!doctype html>
                <title>File Error</title>
                <h3>File error - make sure file's type is .csv</h3>
                <a href=".">Try Again</a>
                """
    else:
        return render_template('submit/submit.html')
