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
import numpy as np
from PyPDF2 import PdfReader
from pdf import pdf_processing
from generate_txt import generate_txt_file
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
User_answer = []
global false_answer
false_answer = 0

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global false_answer
    GPT_answer.clear()
    User_answer.clear()
    false_answer = 0
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
            User_answer.append(int(value))
        return redirect(url_for('check'))
    else:
        GPT_answer.clear()
        User_answer.clear()
        filename = session.get('filename')
        result = session.get('result')
        result["filename"] = filename
        question = pdf_processing(result["filename"], result["start_page"], result["end_page"], result["num_of_questions"], result["api"])
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
            GPT_answer.append(int(value["정답"]))
        print(Qna_result)
        session["GPT_QUESTIONS"] = json.dumps(Qna_result)
        return render_template('questions.html', result=Qna_result)

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        GPT_response = json.loads(session.get('GPT_QUESTIONS', '{}'))
        print(GPT_response)
        generate_txt_file(GPT_response)
        # 다운로드할 파일 경로 설정
        filepath = os.path.join(os.getcwd(), 'GPT_questions.txt')
        # 파일 다운로드 함수 호출
        return send_file(filepath, as_attachment=True)
    else:
        print("********** CHECK ***********")
        print(GPT_answer)
        print(User_answer)
        false_answer = np.equal(GPT_answer,User_answer)
        false_ans_num = len(false_answer) - sum(false_answer)
        print(false_answer)
        print(false_ans_num)
        GPT_response = json.loads(session.get('GPT_QUESTIONS', '{}'))
        return render_template('check.html', check_result=GPT_response, false_num=false_ans_num, false_answer=false_answer)

if __name__ == '__main__':
    app.run() # 배포시 debug=True 삭제
    # app.run(host='0.0.0.0') 배포 시 사용