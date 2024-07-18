
from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()



def create_app():
    
    app = Flask(__name__)
    app.secret_key = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
    db.init_app(app)  
    app.config['UPLOAD_FOLDER']= 'C:/Users/gupta/OneDrive/Desktop/EY/app/input_files'  # Specify where to store uploaded files
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}  # Define allowed file extensions
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .email_summary import email_summary as email_blueprint
    app.register_blueprint(email_blueprint)
    return app

# def get_connection():
#     conn = sqlite3.connect('ey_db.db')
#     conn.row_factory = sqlite3.Row
#     return conn