from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import pytz
from werkzeug.security import check_password_hash
from .models import User,es_data
from . import db
from datetime import datetime,timedelta
auth = Blueprint('auth',__name__)
global user_name

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    #print(username,password)
    
    
   # user=conn.execute('Select password from user_detail where id= ? AND password= ?',(username,password)).fetchone()
    user=User.query.filter_by(id=username).first()
    if not user or user.password!=password:
        print (1)
        flash('Incorrect User ID or Password', 'error')
        return redirect(url_for('auth.login'))
        
        #return render_template('login.html')
    if (username.lower()=='admin'):
        session['user_name'] = "Admin"
        login_time = make_aware(datetime.now())
        session['login_time'] = login_time.isoformat()
        session['tokens']=0
        return redirect(url_for('main.adminprofile'))
    else:
        session['user_name'] = username
        login_time = make_aware(datetime.now())
        session['login_time'] = login_time.isoformat()
        session['tokens']=0
        return redirect(url_for('main.profile'))


    

def make_aware(dt, timezone=pytz.utc):
    if dt.tzinfo is None:
        return timezone.localize(dt)
    return dt

@auth.route('/logout')
def logout():
    if 'user_name' in session:
        login_time_str = session.pop('login_time', None)
        login_time = datetime.fromisoformat(login_time_str)
        login_time = make_aware(login_time)  # Ensure it is offset-aware
        logout_time = make_aware(datetime.now())
        session_duration = logout_time - login_time
        session_duration=int(session_duration.total_seconds())
        new_record = es_data(id=session['user_name'], session_time=session_duration,tokens=session['tokens'],file_size=0)
        db.session.add(new_record)
        db.session.commit()
        session.clear()
    
    
        return render_template('logout.html')
    else:
        return("Error occured!")