from flask import Blueprint, render_template,session,redirect, url_for
from . import db
from .models import User,es_data
main = Blueprint('main',__name__)


@main.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
@main.route('/')
def index():
    return render_template('index.html')
@main.route('/profile')
def profile():
    
    
    user_name = session.get('user_name')
    if user_name==None:
        return render_template('logout.html')
    return render_template('profile.html',user_name=user_name)


@main.route('/adminprofile')
def adminprofile():
   
    #data = session.get('data', 'Guest')
    return render_template('adminprofile.html')

@main.route('/admindetails')
def admin_user_details_post():
    data=es_data.query.all()
    print (data)
    
    return render_template('admindetails.html',data=data)


