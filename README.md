<div align="center">
<img src="resource/poster2.png">
<h1><b>DKSH KAKAO OPEN BUILDER CHAT BOT</b></h1>
<p>👨🏻‍💻 단국대학교부속소프트웨어고등학교 카카오톡 i 오픈빌더 챗봇 👨🏻‍💻</p>
<img src="https://img.shields.io/badge/Python-v3-blue.svg">
<img src="https://img.shields.io/github/license/DKSH-Astronaut/Dankook_ATM?style=flat">
<img src="https://img.shields.io/github/last-commit/DKSH-Astronaut/Dankook_ATM">
</div>
<br>

# 1. 소개
안녕하세요!

저는 단대소프트웨어고등학교의 생활을 좀 더 향상시킬 수 있도록 노력하는 카카오톡 봇입니다.

만나서 반가워요! 혹시 궁금하신 점이 있으신가요?


# 2. 파일 구조
```shell
.
├── resource
│   ├── DKSHLIFE.png
│   ├── error[1].png
│   ├── error[2].png
│   ├── maybeyouwant.png
│   ├── meal.png
│   ├── poster.png
│   ├── poster2.png
│   ├── song.png
│   ├── timetable.png
│   ├── wantMeal.png
│   ├── wantTimetable.png
│   ├── wantWeather.png
│   └── weather.png
├── sample
│   ├── meal_error.jpg
│   ├── meal_success.jpg
│   ├── time_table_success.jpg
│   ├── weather_error.jpg
│   └── weather_success.jpg
├── .gitignore
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── runtime.txt
└── time_table.csv
```

# 3. 메인 기능
| # | Func Name | what it does | `keyword` | using example | Entity Name |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 오늘 급식 파싱 | 나이스에서 오늘 급식정보를 파싱하여 리턴합니다. | `오늘` | `오늘 급식 알려줘`, `오늘 급식` ... | `sys_date` |
| 2 | 내일 급식 파싱 | 나이스에서 내일 급식정보를 파싱하여 리턴합니다. | `내일` | `내일 급식 알려줘`, `내일 급식` ... | `sys_date` |
| 3 | 시간표 | 전학급의 시간표 정보를 리턴합니다. | `1학년`, `2학년`, `1반`, `2반`, `월요일` ... | [look sample image](https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/time_table_success.jpg) | `sys_date`, `set_grade`, `set_class` |
| 4 | 날씨 파싱 | 원하는 지역의 날씨 정보를 리턴합니다. | `대치동`, `성동구`, `서울` ... | [look sample image](https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/weather_success.jpg) | `sys_location` |
| 5 | Solved.ac 프로필 확인 | 자신의 백준 티어를 파싱하여 리턴합니다. | `(자신의 백준 아이디)` | [look sample image](https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/solved_success.jpg) | `boj_name` |

# 4. 실제 사용 예시
<div align="center">
<img src="https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/meal_success.jpg">
<img src="https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/time_table_success.jpg">
<img src="https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/weather_success.jpg">
<img src="https://github.com/kitae0522/DKSH-KAKAO-i/blob/main/sample/solved_success.jpg">
</div>

# 5. 패치노트 (2021년도부터 작성)
2021-03-02 / 00:06 : 날씨 검색 기능 삭제 (삭제 사유 : 사용 빈도수 매우 낮음)
2021-05-03 / 20:01 : 2021학년도 1학기 시간표로 교체 및 MySQL 연동

# 6. 개발 환경
- Lang : Python 3.7.7
- Web Framework : flask
- Server : pythonanywhere

# 7. 이것을 어떻게 사용하나요?
- Development >
```shell
$ git clone https://github.com/kitae0522/DKSH-KAKAO-i.git
$ pip3 install -r requirments.txt
$ python3 main.py
```

- User >
  - 카카오톡 채널 아이디 : @dkshlife
  - 카카오톡 채널 링크 : [https://pf.kakao.com/_VvPXxb](https://pf.kakao.com/_VvPXxb)

# 8. 개발자 정보

- 개발자 : [@kitae0522](https://github.com/kitae0522)
- 피드백 : kitae040522@gmail.com or leave an issue
- Repo : [http://github.com/kitae0522/DKSH-KAKAO-i](http://github.com/kitae0522/DKSH-KAKAO-i)
