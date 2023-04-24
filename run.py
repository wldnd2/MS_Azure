# -*- coding: utf-8 -*-
"""
    pip install flask
    pip install openai -> 오류나면 cmd 관리자권한으로 실행해서 입력
    pip install PyPDF2
    
    실행: python run.py
"""
import os
import json
import openai
import secrets
from PyPDF2 import PdfReader
from pdf import pdf_processing
from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, request, redirect, url_for, render_template, Flask, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

UPLOAD_FOLDER = os.getcwd() + '/uploads'  # 절대 파일 경로
ALLOWED_EXTENSIONS = set(['pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 16MB로 업로드 크기 제한, RequestEntityTooLarge : 크기 초과시 이 예외 발생, 처리 필요

GPT_answer = []
User_anwer = []

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
            session['filename'] = filename
            session['result'] = result
            return redirect(url_for('questions'))
    return render_template('fileupload.html') # GET 

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        for key, value in request.form.items():
            User_anwer.append(int(value))
        return redirect(url_for('check'))
    else:
        filename = session.get('filename')
        result = session.get('result')
        result["filename"] = filename
        question = pdf_processing(result["filename"], result["start_page"], result["end_page"], result["num_of_questions"])
        Qna_result = {}
        Qna_number = 1
        # print("***********{ PDF RESULT }***********")
        # print(question)
        print("\n***********{ Questions PROCESSING }*************")
        for key, value in question.items():
            try:
                if(value[0] == "[" and value[-1] == "]"):
                    print("***********{ List processing }***********")
                    value = json.loads(value)
                    for item in value:
                        Qna_result[Qna_number] = item
                        Qna_number += 1
                else:
                    print("***********{ Json processing }***********")
                    Qna_result[Qna_number] = json.loads(value)
                    Qna_number += 1
            except:
                print("***********{ PASS!!!! }*************")
                continue
        print("\n***********{ FINAL RESULT }*************")
        print(Qna_result)
        print("*******************************************")
        for key, value in Qna_result.items():
            GPT_answer.append(value["정답"])
        session["GPT_QUESTIONS"] = Qna_result
        return render_template('questions.html', result=Qna_result)

@app.route('/check', methods=['GET', 'POST'])
def check():
    print("********** CHECK ***********")
    print(GPT_answer)
    print(User_anwer)
    GPT_response = session.get('GPT_QUESTIONS')
    print(GPT_response)
    return render_template('check.html', check_result=GPT_response)

if __name__ == '__main__':
    app.run(debug=True) # 배포시 debug=True 삭제
    # app.run(host='0.0.0.0') 배포 시 사용