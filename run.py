"""
    pip install flask
    pip install openai -> 오류나면 cmd 관리자권한으로 실행해서 입력
    pip install PyPDF2
"""

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, request, redirect, url_for, render_template, Flask
from PyPDF2 import PdfReader
import openai

app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() + '/uploads'  # 절대 파일 경로
ALLOWED_EXTENSIONS = set(['pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 16MB로 업로드 크기 제한, RequestEntityTooLarge : 크기 초과시 이 예외 발생, 처리 필요


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        result = request.form # first_page, last_page, num_of_question 변수 저장
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_processing('uploads/'+ filename)
            return render_template('loading.html', filename=filename, result=result) 
    return render_template('fileupload.html') # GET 방식의 요청일 때


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def pdf_processing(filename:str):    
    """ PDF 추출 Setting """
    reader = PdfReader(filename)
    pages = reader.pages
    txt = open(filename + "_questions.txt", 'w+', encoding='utf-8')
    cur = 0 # 현재 페이지
    exception_pages = [] # 제외할 페이지 입력받기

    """ ChatGPT Setting """
    OPEN_AI_API_KEY = "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" # 각자 키 입력 (https://platform.openai.com/account/api-keys 확인 ㄱ)
    openai.api_key = OPEN_AI_API_KEY
    model = "gpt-3.5-turbo"
    messages = [ # system content 손 볼 필요 있음
            {"role": "system", "content": "사용자가 전송하는 내용 중 중요한 내용을 사용하여 단답식 문제 1개와 4지선다형 문제 1개를 내고,\
                각각의 문제의 정답과 해설을 알려주세요.\n\
                답변 형식: json 형식"}
    ]

    for page in pages:
        cur += 1 # 현재 페이지 수
        if cur == 6: break # test용 5페이지까지만 진행
        query = page.extract_text() # 각 페이지에서 text 추출하여 저장
        print(f"-- {cur} 페이지 문제 추출 중 --")
        print(f"[ page {cur} ]", file=txt)
        print(query, file=txt)
        messages.append({"role": "user", "content": query})
        
        # ChatGPT API 호출하기
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        answer = response['choices'][0]['message']['content']
        print(f"[ question for page {cur} ]", file=txt)
        print(answer, file=txt)
        
        messages.pop()
    txt.close()

@app.route('/questions')
def questions():
    return render_template('questions.html')

if __name__ == '__main__':
    app.run(debug=True) # 배포시 debug=True 삭제
    # app.run(host='0.0.0.0') 배포 시 사용
    