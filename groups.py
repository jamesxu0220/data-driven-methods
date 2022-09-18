from DataDrivenFinance import app
from DataDrivenFinance.databases import db, Group
from flask import request, redirect, render_template


@app.route('/groups/', methods=['POST', 'GET'])
def groups():
    if request.method == 'POST':
        gid = request.form['group_id']
        if Group.query.filter_by(group_id=gid).first():
            return """
                <!doctype html>
                <title>Error</title>
                <h3>Error: Group ID already exists!</h3>
                <a href=".">Try something new</a>
                """
        gname = request.form['group_name']
        m1_id = request.form['member1_id']
        m2_id = request.form['member2_id']
        m3_id = request.form['member3_id']
        m4_id = request.form['member4_id']
        m5_id = request.form['member5_id']
        new_group = Group(group_id=gid, group_name=gname, member1_id=m1_id,
                          member2_id=m2_id, member3_id=m3_id, member4_id=m4_id, member5_id=m5_id)
        try:
            db.session.add(new_group)
            db.session.commit()
            return redirect('/groups/')
        except:
            return "There was an issue adding your group!"
    else:
        groups = Group.query.order_by(Group.group_id).all()
        return render_template('groups.html', groups=groups)
