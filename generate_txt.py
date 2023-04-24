def generate_txt_file(GPT_questions):
    with open('GPT_questions.txt', 'w', encoding='utf-8') as f:
        for key, value in GPT_questions.items():
            f.write(f"문제 {key}: {value['문제']}\n")
            question_num = 1
            while True:
                print("ddd")
                try:
                    f.write(f"{question_num}. {value[str(question_num)]}\n")
                    question_num += 1
                except:
                    break
            f.write(f"정답: {value['정답']}\n")
            f.write(f"해설: {value['해설']}\n\n")