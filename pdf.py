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
    questions = {}
    cnt = 1
    cur = 0 # 현재 페이지
    """ ChatGPT Setting """
    OPEN_AI_API_KEY = "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" # 각자 키 입력 (https://platform.openai.com/account/api-keys 확인 ㄱ)
    openai.api_key = OPEN_AI_API_KEY
    model = "gpt-3.5-turbo"
    messages = [ # system content 손 볼 필요 있음
            {"role": "system", "content": "사용자가 전송하는 내용을 토대로 문제를 한 개만 만들어줘. { 문제 : 질문, 1 : 첫 번째 선택지, 2 : 두 번째 선택지, 3: 세 번째 선택지, 4: 네 번째 선택지, 정답: 정답번호, 해설: 해설 } 이러한 형태로 출력해줘. json 형식으로 답해줘."}
    ]
    
    """ JSON Setting """
    json_file_path = "./downloads/questions.json"
    json_data = {}
    json_data['questions'] = []

    for page in pages: # 페이지별 문제 추출
        cur += 1 # 현재 페이지 수
        if cur < int(start_page) or cur > int(end_page): # start_page ~ end_page 까지만 작동
            continue;
        
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
        print('answer: ',answer)
        print('cnt: ',cnt)

        questions[cnt] = answer
        cnt += 1
        
        # 다음 페이지를 위해 messages에서 현재 페이지의 text로 작성된 user content 삭제
        messages.pop()
        
    # Json 파일에 쓰기
#    with open(json_file_path, 'w', encoding='utf-8') as outfile:
#        json.dump(json_data, outfile, indent='\t', ensure_ascii=False)
    # txt.close()

    return questions