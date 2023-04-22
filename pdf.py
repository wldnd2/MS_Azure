import os
from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, request, redirect, url_for, render_template, Flask
from PyPDF2 import PdfReader
import openai, json

def pdf_processing(filename:str, start_page, end_page, num_of_questions):    
    """ PDF 추출 Setting """
    reader = PdfReader("./uploads/" + filename)
    pages = reader.pages 
    txt = open("./result/" + filename.split(".")[0] + "_questions.txt", 'w', encoding='utf-8') # filename.split(".")[0] => 확장자명 제거
    cur = 0 # 현재 페이지

    """ JSON Setting """
    json_data = {}
    json_data['questions'] = []

    """ ChatGPT Setting """
    OPEN_AI_API_KEY = "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" # 각자 키 입력 (https://platform.openai.com/account/api-keys 확인 ㄱ)
    openai.api_key = OPEN_AI_API_KEY
    model = "gpt-3.5-turbo"
    messages = [ # system content 손 볼 필요 있음
            {"role": "system", "content": "사용자가 전송하는 내용 중에서 문제를 제출한다. 2문제만 제출한다. 모든 문제는 4지선다형 문제로 일치시킨다. \
                답변 형식은 json형식으로 각각의 문제번호(숫자로만 key를 표시), 문제(question을 key로 표시), \
                4지선다(1,2,3,4를 key로 한다), 정답(answer를 key로 표시)과 해설(explanation를 key로 표시)을 알려주세요."}
    ]

    """ 페이지 추출 """
    for page in pages:
        cur += 1 # 현재 페이지 수
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
        # add_code = "json_data['questions'].append(" + answer + ")"
        # exec(add_code)
        
        """ json 데이터 추출 """
        print(f"answer: {answer}")
        # JSON 문자열을 파싱하여 딕셔너리로 저장
        data = json.loads(answer)
        # 문제 형식으로 출력
        for key, value in data.items():
            txt.write(f'{value["question"]}\n')
            for i in range(1, 5):
                txt.write(f'{i}. {value[str(i)]}\n')
            txt.write(f'정답: {value["answer"]}\n')
            txt.write(f'해설: {value["explanation"]}\n\n')
        
        """  Json Data 입력 """
        with open("./result/" + filename.split(".")[0] + "_questions.json", "w", encoding="utf-8") as f:
            json.dump(answer,f, ensure_ascii=False, sort_keys=True)
        # 다음 페이지를 위해 messages에서 현재 페이지의 text로 작성된 user content 삭제
        messages.pop()
    txt.close()