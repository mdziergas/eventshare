from flask import Blueprint, render_template, session, url_for, redirect, request
from eventshare.models import add_group, db, add_member_to_group
from bson.objectid import ObjectId

dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates',static_folder='static', url_prefix='/')


@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    groups = ['none',]
    if session['authenticated'] == True:
        username = session['username']
        user = db.users.find_one({'username':username})
        groups = user.get('groups')
        
        if groups:
            pass
        else:
            groups = ['no groups',]
    if request.method == 'POST':
        if session['authenticated'] == True:
            group_name = request.form['group_name']
            group_description = request.form['group_description']
            username = session['username']
            group_id = ObjectId()
            add_group(group_id, username, group_name, group_description)
            add_member_to_group(username, group_id, group_name)
    return render_template('dashboard.html', groups = groups)


