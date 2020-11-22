from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from pytz import timezone
import pandas as pd
import random

time_table_DB = pd.read_csv('time_table.csv')

ERROR_MESSAGE = "🤦🏻‍♂️학교 또는 기상청에서 제공하는 데이터 정보가 없습니다. 나중에 다시 시도해주세요."

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Safari/537.36"
}

quickReplies = [
    {
        "messageText": "처음으로 돌아갈래!",
        "action": "message",
        "label": "처음으로 돌아갈래!"
    },
    {
        "messageText": "오늘 급식 메뉴는 뭐야?",
        "action": "message",
        "label": "오늘 급식 메뉴는 뭐야?"
    },
    {
        "messageText": "내일 급식 메뉴는 뭐야?",
        "action": "message",
        "label": "내일 급식 메뉴는 뭐야?"
    },
    {
        "messageText": "시간표 알려줘!",
        "action": "message",
        "label": "시간표 알려줘!"
    },
    {
        "messageText": "내 백준 티어 알려줘!",
        "action": "message",
        "label": "내 백준 티어 알려줘!"
    },
    {
        "messageText": "현재 날씨가 궁금해!",
        "action": "message",
        "label": "현재 날씨가 궁금해!"
    }
]

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, Flask!'


@app.route('/time_table', methods=['POST'])
def time_table():
    req = request.get_json()

    tmp = 0

    set_grade = req["action"]["detailParams"]["set_grade"]["value"]
    set_class = req["action"]["detailParams"]["set_class"]["value"]
    date = json.loads(req["action"]["detailParams"]
                      ["sys_date"]["value"])["dateTag"]

    if date == "Monday":
        date, tmp = "월요일", 1
    elif date == "Tuesday":
        date, tmp = "화요일", 2
    elif date == "Wednesday":
        date, tmp = "수요일", 3
    elif date == "Thursday":
        date, tmp = "목요일", 4
    elif date == "Friday":
        date, tmp = "금요일", 5
    else:
        tmp = ERROR_MESSAGE

    with open("DB/.log", "a", encoding="UTF8") as file:
        try:
            index = 25*(int(set_grade)-1) + (int(set_class)-1)*5 + tmp - 1
            _time_table = list(time_table_DB['time'].iloc[index].split("+"))
            _res_time_table = [f"{key+1}교시 : {value}" for key,
                               value in enumerate(_time_table)]
            answer = [f"[📆{set_grade}학년 {set_class}반 {date} 시간표입니다.]",
                      ("-".join(_res_time_table)).replace("-", "\n")]
            log = {
                "use-skill": "time_table",
                "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                "type": 200
            }
        except:
            answer = ["오류!", ERROR_MESSAGE]
            log = {
                "use-skill": "time_table",
                "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                "type": 404
            }
        file.write(f"{log}\n")

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": answer[0],
                        "description": answer[1],
                        "thumbnail": {
                            "imageUrl": "https://i.ibb.co/LPgF9pp/image.png"
                        }
                    }
                }
            ],
            "quickReplies": quickReplies
        }
    }

    return jsonify(res)


@ app.route('/meal', methods=['POST'])
def meal():
    req = request.get_json()

    date = json.loads(req["action"]["detailParams"]
                      ["sys_date"]["value"])["dateTag"]

    with open("DB/.log", "a", encoding="UTF8") as file:
        try:
            if date == "today":
                YMD = datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d')
                m = datetime.now(timezone('Asia/Seoul')).strftime('%m')
                d = datetime.now(timezone('Asia/Seoul')).strftime('%d')
            elif date == "tomorrow":
                YMD = str(
                    int(datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d'))+1)
                m = datetime.now(timezone('Asia/Seoul')).strftime('%m')
                d = str(int(datetime.now(timezone('Asia/Seoul')).strftime('%d'))+1)
            url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?type=json&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7010137&MLSV_YMD={YMD}"
            res = requests.get(url)
            data = json.loads(res.text)
            log = {
                "use-skill": "meal",
                "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                "type": 200
            }

            try:
                answer = ["[🍚" + m + "월 " + d + "일 중식입니다.]", data['mealServiceDietInfo']
                          [1]['row'][0]['DDISH_NM'].replace("<br/>", "\n")]
            except KeyError:
                answer = ["오류!", ERROR_MESSAGE]
                log = {
                    "use-skill": "meal",
                    "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                    "type": 404
                }
        except UnboundLocalError:
            answer = ["오류!", ERROR_MESSAGE]
            log = {
                "use-skill": "meal",
                "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                "type": 404
            }
        file.write(f"{log}\n")

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": answer[0],
                        "description": answer[1],
                        "thumbnail": {
                            "imageUrl": "https://i.ibb.co/phvykYv/image.png"
                        }
                    }
                }
            ],
            "quickReplies": quickReplies
        }
    }

    return jsonify(res)


@ app.route('/weather', methods=['POST'])
def weather():
    req = request.get_json()

    location = req["action"]["detailParams"]["sys_location"]["value"]
    url = f'https://search.naver.com/search.naver?query={location}+날씨'

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')

    with open("DB/.log", "a", encoding="UTF8") as file:
        # 현재 온도
        NowTemp = soup.find('p', class_='info_temperature').find(
            'span', class_='todaytemp').text

        # 현재 상태
        WeatherCast = soup.find('ul', class_='info_list').find(
            'p', class_='cast_txt').text

        # 최저/최고 온도
        MinTemp = soup.find('span', class_='min').find(
            'span', class_='num').text
        MaxTemp = soup.find('span', class_='max').find(
            'span', class_='num').text

        # 미세먼지/초미세먼지
        DustData = soup.find('div', class_='detail_box')
        DustData = DustData.findAll('dd')
        FineDust = DustData[0].find('span', class_='num').text
        UltraFineDust = DustData[1].find('span', class_='num').text

        # 내일 오전, 오후 온도 및 상태 체크
        tomorrowArea = soup.find('div', class_='tomorrow_area')
        tomorrowCheck = tomorrowArea.find_all(
            'div', class_='main_info morning_box')

        # 내일 오전 온도
        tomorrowMoring = tomorrowCheck[0].find(
            'span', {'class': 'todaytemp'}).text

        # 내일 예상 오전 상태
        tomorrowMState1 = tomorrowCheck[0].find('div', {'class': 'info_data'})
        tomorrowMState2 = tomorrowMState1.find('ul', {'class': 'info_list'})
        tomorrowMState3 = tomorrowMState2.find('p', {'class': 'cast_txt'}).text

        # 내일 오후 온도
        tomorrowAfter1 = tomorrowCheck[1].find(
            'p', {'class': 'info_temperature'})
        tomorrowAfter = tomorrowAfter1.find(
            'span', {'class': 'todaytemp'}).text

        # 내일 예상 오후 상태
        tomorrowAState1 = tomorrowCheck[1].find('div', {'class': 'info_data'})
        tomorrowAState2 = tomorrowAState1.find('ul', {'class': 'info_list'})
        tomorrowAState3 = tomorrowAState2.find('p', {'class': 'cast_txt'}).text

        answer = [f"[🌈{location} 날씨 정보입니다!]", "=======오늘 날씨=======" +
                  "\n🌡현재 온도 : " + NowTemp + "°C" +
                  "\n🌡최저/최고 온도 : " + MinTemp + "°C/" + MaxTemp + "°C" +
                  "\n❤현재 상태 : " + WeatherCast +
                  "\n⚠현재 미세먼지 농도: " + FineDust +
                  "\n⚠현재 초미세먼지 농도: " + UltraFineDust + "\n\n" +
                  "=======내일 날씨=======" +
                  "\n🌡내일 예상 오전 온도 : " + tomorrowMoring + "°C" +
                  "\n❤내일 예상 오전 상태 : " + tomorrowMState3 +
                  "\n🌡내일 예상 오후 온도 : " + tomorrowAfter + "°C" +
                  "\n❤내일 예상 오후 상태 : " + tomorrowAState3]
        log = {
            "use-skill": "weather",
            "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
            "type": 200
        }
        file.write(f"{log}\n")

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": answer[0],
                        "description": answer[1],
                        "thumbnail": {
                            "imageUrl": "https://i.ibb.co/MN9pfMQ/image.png"
                        }
                    }
                }
            ],
            "quickReplies": quickReplies
        }
    }

    return jsonify(res)


@ app.route('/boj', methods=['POST'])
def boj():
    req = request.get_json()

    boj_name = req["action"]["detailParams"]["boj_name"]["value"]
    url = [f'https://solved.ac/profile/{boj_name}',
           f'https://www.acmicpc.net/user/{boj_name}']

    data_set = {}
    baekjoon, cnt = True, 0
    word = [["복잡성을 통제하는 것이 컴퓨터 프로그래밍의 기초다.", "- Brian Kernighan, 유닉스 창시자"],
            ["컴퓨터는 쓸모가 없다. 그것은 그냥 대답만 할 수 있다.", "- Pablo Picasso, 화가"],
            ["컴퓨터 언어를 설계하는 것은 공원을 산책하는 것과 같다. '쥬라기 공원!!!'",
                "- Larry Wall, Perl 언어 창시자"],
            ["만일 디버깅이 벌레를 잡는 과정이라면 프로그래밍은 그걸 집어넣는 과정이다.",
             "- E.W Dijkstra, 컴퓨터 과학자(다익스트라 알고리즘 고안)"],
            ["제발 안 쉬운 걸 쉽다고 이야기하지 마세요.", "- Alan Cooper, 비주얼 베이직의 아버지"],
            ["640KB면 모든 사람들에게 충분하다.", "- Bill Gates, 마이크로소프트 창립자"]
            ]
    cnt = 0
    for i in range(len(url)):
        html = requests.get(url[i], headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        if i == 0:
            arr = ["bronze", "silver", "gold",
                   "platinum", "diamond", "ruby"]
            div = soup.find("div", {"class": "solvedac-centering"})
            for i in range(len(arr)):
                try:
                    data_set["grade"] = div.find(
                        "span", {"class": arr[i]}).find("b").text
                except AttributeError:
                    continue
        elif i == 1:
            try:
                li = soup.find(
                    "div", {"class": "panel-body"}).findAll("span")
                cnt = len(li) // 2
                data_set["solve_count"] = cnt
            except AttributeError:
                baekjoon = False
    ran_word = random.choice(word)
    with open("DB/.log", "a", encoding="UTF8") as file:
        if div is not None and baekjoon:
            answer = [f"[{boj_name} 유저의 백준 정보입니다!]",
                      f'티어 : {data_set["grade"]}\n푼 문제 갯수 : {data_set["solve_count"]}\n\n{ran_word[0]}\n{ran_word[1]}']
            log = {
                "use-skill": "boj",
                "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                "type": 200
            }
        else:
            answer = [f"[{boj_name} 유저는 존재하지 않습니다!]",
                      f'백준 사이트 회원인데 이 메세지가 뜬 다면, https://www.acmicpc.net/setting/solved.ac 에서 설정해주세요!']
            log = {
                "use-skill": "boj",
                "time": datetime.now(timezone('Asia/Seoul')).strftime('%y%m%d : %Hh %Mmin %Ssec'),
                "type": 404
            }
        file.write(f"{log}\n")

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": answer[0],
                        "description": answer[1],
                        "thumbnail": {
                            "imageUrl": "https://i.ibb.co/Zd1ycf7/bojTier.png"
                        }
                    }
                }
            ],
            "quickReplies": quickReplies
        }
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
