#-*- coding: utf-8 -*-

"""
    pip install flask
    pip install openai -> 오류나면 cmd 관리자권한으로 실행해서 입력
    pip install PyPDF2
    
    실행: python run.py
"""
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, request, redirect, url_for, render_template, Flask
from flask import session
from PyPDF2 import PdfReader
import openai, json
from pdf import pdf_processing
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = os.getcwd() + '/uploads'  # 절대 파일 경로
ALLOWED_EXTENSIONS = set(['pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 16MB로 업로드 크기 제한, RequestEntityTooLarge : 크기 초과시 이 예외 발생, 처리 필요

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        result = request.form # start_page, end_page, num_of_questions 변수 저장
        file = request.files['myfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(f'upload file: {filename}, {result}')
            session['filename'] = filename
            session['result'] = result
            return redirect(url_for('loading'))
    return render_template('fileupload.html') # GET 

@app.route('/loading', methods=['GET', 'POST'])
def loading():
    filename = session.get('filename')
    result = session.get('result')
    #print(filename, result)
    if request.method == 'POST':
        res = request.form # filename, start_page, end_page, num_of_questions 변수 저장
        # return redirect(url_for('questions', result=res))
        result["filename"] = filename
        return questions(result)
    return render_template('loading.html', filename=filename, result=result)
    
@app.route('/questions')
def questions(result):
    question = pdf_processing(result["filename"], result["start_page"], result["end_page"], result["num_of_questions"])
    return render_template('questions.html', result=question)


if __name__ == '__main__':
    app.run(debug=True) # 배포시 debug=True 삭제
    # app.run(host='0.0.0.0') 배포 시 사용
    