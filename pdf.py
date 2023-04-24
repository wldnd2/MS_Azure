import os
from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, request, redirect, url_for, render_template, Flask
from PyPDF2 import PdfReader
import openai, json

def pdf_processing(filename:str, start_page, end_page, num_of_questions_per_page):    
    """ PDF 추출 Setting """
    reader = PdfReader("./uploads/" + filename)
    pages = reader.pages 
    # txt = open("./downloads/" + filename + "_questions.txt", 'w', encoding='utf-8')
    questions = {}
    questions_number = 1
    cur_page = 0 # 현재 페이지
    """ ChatGPT Setting """
    OPEN_AI_API_KEY = "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" # 각자 키 입력 (https://platform.openai.com/account/api-keys 확인 ㄱ)
    openai.api_key = OPEN_AI_API_KEY
    model = "gpt-3.5-turbo"
    messages = [ # system content 손 볼 필요 있음
            {"role": "system", "content": "사용자가 전송하는 내용을 토대로 문제를 정확히 1개만 출제해. { 문제 : 질문, 1 : 첫 번째 선택지, 2 : 두 번째 선택지, 3: 세 번째 선택지, 4: 네 번째 선택지, 정답: 정답번호, 해설: 해설 } 이러한 json형태로 출력해."}
    ]
    
    """ JSON Setting """
    json_file_path = "./downloads/questions.json"
    json_data = {}
    json_data['questions'] = []

    for page in pages: # 페이지별 문제 추출
        cur_page += 1 # 현재 페이지 수
        if cur_page < int(start_page) or cur_page > int(end_page): # start_page ~ end_page 까지만 작동
            continue
        
        query = page.extract_text() # 각 페이지에서 text 추출하여 query에 저장 
        print(f"-- {cur_page} 페이지 문제 추출 중 --")
        messages.append({"role": "user", "content": query})
        
        for i in range(int(num_of_questions_per_page)):
            # ChatGPT API 호출하기
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )
            answer = response['choices'][0]['message']['content']
            print('answer: ',answer)
            questions[questions_number] = answer
            questions_number += 1

        # 다음 페이지를 위해 messages에서 현재 페이지의 text로 작성된 user content 삭제
        messages.pop()
    # txt.close()
    return questions