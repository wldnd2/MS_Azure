import os
from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, request, redirect, url_for, render_template, Flask
from PyPDF2 import PdfReader
import openai, json

def pdf_processing(filename:str, start_page, end_page, num_of_questions):    
    """ PDF 추출 Setting """
    reader = PdfReader("./uploads/" + filename)
    pages = reader.pages 
#    txt = open("./downloads/" + filename + "_questions.txt", 'w', encoding='utf-8')
    cur = 0 # 현재 페이지
    """ ChatGPT Setting """
    OPEN_AI_API_KEY = "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" # 각자 키 입력 (https://platform.openai.com/account/api-keys 확인 ㄱ)
    openai.api_key = OPEN_AI_API_KEY
    model = "gpt-3.5-turbo"
    messages = [ # system content 손 볼 필요 있음
            {"role": "system", "content": "사용자가 전송하는 내용 중 중요한 내용을 사용하여 4지선다형 문제 1개를 내고,\
                각각의 문제의 정답과 해설을 알려주세요.\n\
                답변 형식: json 형식"}
    ]
    
    """ JSON Setting """
    json_file_path = "./downloads/questions.json"
    json_data = {}
    json_data['questions'] = []

    for page in pages: # 페이지별 문제 추출
        cur += 1 # 현재 페이지 수
        #print('end============',type(end_page))
        if cur < int(start_page) or cur > int(end_page): # start_page ~ end_page 까지만 작동
            continue
        
        query = page.extract_text() # 각 페이지에서 text 추출하여 query에 저장
        print(f"-- {cur} 페이지 문제 추출 중 --")
        messages.append({"role": "user", "content": query})
        
        # ChatGPT API 호출하기
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        answer = response['choices'][0]['message']['content']
        
        # Json 데이터에 현재 페이지에서 생성된 question 추가
        """ !!Json 형식으로 GPT 답변이 온다고 가정하고 코드 작성!! """
#        add_code = "json_data['questions'].append(" + answer + ")"
#        exec(add_code)
        print(answer)
        
        # 다음 페이지를 위해 messages에서 현재 페이지의 text로 작성된 user content 삭제
        messages.pop()
        
    # Json 파일에 쓰기
#    with open(json_file_path, 'w', encoding='utf-8') as outfile:
#        json.dump(json_data, outfile, indent='\t', ensure_ascii=False)
    # txt.close()
