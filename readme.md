# [서비스] GPT Question Maker: 당신의 PDF를 이용한 문제 & 풀이 제공

1. [서비스 소개](#서비스-소개)   
2. [서비스 플로우](#서비스-플로우)   
3. [서비스 링크](#서비스-링크)   
4. [데모 영상](#데모-영상)   
5. [기대 효과 & 확장 가능성](#기대-효과-&-확장-가능성)
6. [Team INFO](#team-info)

# 서비스 소개

> ### 다가온 시험기간. 강의자료만 붙들고 외우고 있는 당신. 당신의 실력이 어느 정도인지 파악하고 싶지 않으신가요?
> ### “Chatster”를 통해 당신이 가지고 있는 PDF로 문제를 만들고 당신의 실력을 테스트해보세요.

![https://cdn.aifactory.space/images/20230424222653_AwsL.png](https://cdn.aifactory.space/images/20230424222653_AwsL.png)

### 🤷서비스 배경

- 공부를 하다 보면, 개념은 알지만 **이 개념을 통해서 어떻게 문제가 나올 지 모르기에**, 본인이 정확하게 무엇을 모르는지도 모르는 경우가 많습니다. 이에 불편함을 느낀 저희는 PDF를 첨부하면 문제를 만들어주는 서비스를 개발하게 되었습니다.

### 🤷‍♀️서비스 대상

- 교수님 혹은 선생님이 주신 강의자료로부터 문제를 만들어서 본인의 실력을 테스트해보고 싶은 학생

### 🤷‍♂️서비스 목적

- 본인이 공부한 강의자료를 바탕으로 만들어진 문제를 풀어 봄으로써, 메타 인지 능력을 향상시키고자 하여 이 서비스를 고안하게 되었습니다.

*※ 메타 인지란? 자기 자신이 인지하고 있음을 아는 것, 즉 "자신이 알고 있는지 모르고 있는지를 안다"라는 뜻입니다.*

# 서비스 플로우

![https://cdn.aifactory.space/images/20230424204348_DXjt.png](https://cdn.aifactory.space/images/20230424204348_DXjt.png)

### 1. **Main Page**: PDF를 업로드하고 해당 PDF에서 문제를 출제할 페이지와 출제할 문제 수를 입력하는 페이지

![https://cdn.aifactory.space/images/20230424222647_YXAU.png](https://cdn.aifactory.space/images/20230424222647_YXAU.png)

### 2. **Loading Page**: GPT가 문제를 생성하는 동안 표시되는 페이지

![https://cdn.aifactory.space/images/20230424222706_zoDB.png](https://cdn.aifactory.space/images/20230424222706_zoDB.png)

### 3. **Questions Page**: GPT가 출제한 문제를 화면에 제시하여 웹상에서 직접 문제풀이가 가능하도록 함

![https://cdn.aifactory.space/images/20230424222725_ObXd.png](https://cdn.aifactory.space/images/20230424222725_ObXd.png)

![https://cdn.aifactory.space/images/20230424222731_yjFz.png](https://cdn.aifactory.space/images/20230424222731_yjFz.png)

### **4. Answers Page**: 오답 여부를 파악하고, 풀이를 확인할 수 있는 페이지로, 출제된 문제를 TXT 파일 형태로 다운로드받을 수 있음

![https://cdn.aifactory.space/images/20230424222740_jRzf.png](https://cdn.aifactory.space/images/20230424222740_jRzf.png)

![https://cdn.aifactory.space/images/20230424222745_YCiZ.png](https://cdn.aifactory.space/images/20230424222745_YCiZ.png)

# 서비스 링크

### 배포 링크: [https://port-0-ms-azure-17xqnr2llgujko5k.sel3.cloudtype.app/](https://port-0-ms-azure-17xqnr2llgujko5k.sel3.cloudtype.app/)

※ 배포 툴 (cloudtype) 의 무료 용량 제한으로 인해, 배포 링크를 통해 실행하게 되면 1페이지당 1문제씩만 문제 생성이 가능합니다. 더욱 자유로운 사용을 위해선 로컬을 통해 테스트해보심을 추천드립니다!🤓

# 데모 영상

# 사용된 스택

front-end: 
<img src="https://img.shields.io/badge/Html5-E34F26?style=for-the-badge&logo=Html5&logoColor=white">
<img src="https://img.shields.io/badge/Css3-1572B6?style=for-the-badge&logo=Css3&logoColor=white">

back-end: 
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">

distribute: 
<img src="https://img.shields.io/badge/Cloudtype-000000?style=for-the-badge&logo=Cloudtype&logoColor=white">
## 기대 효과 & 확장 가능성

- 학생들은 이 서비스를 이용하여 **본인이 공부하던 강의자료를 바탕으로 만들어진 문제**를 통해 자신이 정확하게 알고있는 것과 모르고 있는 것이 무엇인지를 알 수 있을 것입니다.
- 특히, 문제을 출제해 줄 뿐만 아니라 **요약 기능**을 추가한다면 시험을 대비하여 강의 자료를 단기간에 암기하는 것에도 도움을 줄 것입니다.
- 논문이나 전공 서적 등의 PDF 파일을 이용하여 문제를 추출하여 학습하는 데 사용한다면, **학습 효율을 극대화**시킬 것이라고 기대됩니다.
- **학원 선생님** 등 문제 제작에 많은 시간을 소모하는 이들에게도 이 서비스는 유용하게 사용될 수 있습니다.

# Team INFO

### 팀 Chatster(ChatGPT + Master) | 경북대학교 컴퓨터학부 소속

### 전지웅(팀장) [jun000628@naver.com](mailto:jun000628@naver.com)

### 김민주 [kimminju77786@gmail.com](mailto:kimminju77786@gmail.com)

### 김현지 [khj011030@gmail.com](mailto:khj011030@gmail.com)

### 이은지 [leeej106@knu.ac.kr](mailto:leeej106@knu.ac.kr)

### 최희정 [nuly7029@gmail.com](mailto:nuly7029@gmail.com)

