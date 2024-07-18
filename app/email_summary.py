from flask import Blueprint, flash, redirect, render_template, request, session, url_for,Flask,current_app
from werkzeug.security import check_password_hash
from .models import User,es_data
from . import db
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas





email_summary = Blueprint('email_summary',__name__)





from pypdf import PdfReader
import re
import google.generativeai as genai
import os

extract=""
os.environ["API_KEY"]="AIzaSyCtg5sAsSIdQmX8W_tVsZMy01xu7o5ju5Y"
list_data=[]

def pdf_text_extract(file):
    global extract
    global list_data
    clened=""
    readobj=PdfReader(file)
    for i in range(len(readobj.pages)):
    
        page=readobj.pages[i]
        text=page.extract_text()
        extract+=text
    pattern_a=r'<.*>'
    patterncom=r"https?://\S+"
    pattern_punctuation=r"[.?/,]"
    extract=re.sub(pattern_a,"",extract,flags=re.IGNORECASE)
    extract=re.sub(patterncom,"",extract,flags=re.IGNORECASE)
    extract=re.sub(pattern_punctuation,"",extract,flags=re.IGNORECASE)
    #extract.replace("/n","")
    
    #Removing stop words
    
    
    
    extract= re.sub(r"^(Re:)","",extract,flags=re.DOTALL)
    list_data=re.split(r"F\s*r\s*o\s*m\s*:\s.*?S\s*u\s*b\s*j\s*e\s*c\s*t\s*:",extract,flags=re.DOTALL|re.IGNORECASE)
    for i in  list_data:
        i.strip()
        stopwords=["thankyou", "date", "the", "a", "an", "is", "for", "your", "time", "in", "on", "to", "of","thanking","you","regards","outlook",".",",","?"]
        words=i.lower().split()
        filtered_words = [word for word in words if word not in stopwords]
        f=" ".join(filtered_words)
        clened=f+clened
        
    return clened
    
    
    
    


def connecting_to_model(extract):
    global API_KEY
    
    genai.configure(api_key=os.environ["API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash')
    conv="Create a 200 word summary explaining to a third person what is going on int email conversation thread"+ extract
    response = model.generate_content(conv)
    
    return(response.text)
    



@email_summary.route('/email_summariser')
def email_summariser():
    
    return render_template('email_summariser.html')



@email_summary.route('/process', methods=['POST','GET'])
def process_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for(email_summary))
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for(email_summary))
    
    if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)  # Save the uploaded file to a designated folder

        # Perform processing on the file here (e.g., summarization)
        output = process_file_content(file_path)  #actual processing logic
        out_name=text_to_file(output,file.filename)
    
        return render_template('email_summariser_processed.html',output_text=output,output=True)
        #return render_template('email_summariser.html',output=True, filename=out_name, download_file=out_name)
    else:
        flash('Invalid file type', 'error')
        return redirect(request.url)
    
    
@email_summary.route('/email_summariser_processed')    
#def email_summariser_processed(output):
       


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def process_file_content(file_path):
    # Replace this with your actual file processing logic
    with open(file_path, 'r') as f:
        cleaned_data=pdf_text_extract(file_path) # Read file content
        content=connecting_to_model(cleaned_data)
        print (content)
        # Perform summarization or other operations here
        # For demonstration, simply return the content as output
    print(1234)   
    return content


def text_to_file(text,filename):
    path='C:/Users/gupta/OneDrive/Desktop/EY/app/output_file/'
    output_filename=path+"output-"+".txt"
    c = canvas.Canvas(output_filename, pagesize=letter)
    f=open("output_filename","w+")
    f.write(text)
    
    f.close()
    return output_filename