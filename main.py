from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from pytz import timezone
import pandas as pd

time_table_DB = pd.read_csv('time_table.csv')

ERROR_MESSAGE = "🤦🏻‍♂️학교 또는 기상청에서 제공하는 데이터 정보가 없습니다. 나중에 다시 시도해주세요."  # no data

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

    try:
        index = 25*(int(set_grade)-1) + (int(set_class)-1)*5 + tmp - 1
        _time_table = list(time_table_DB['time'].iloc[index].split("+"))
        _res_time_table = [f"{key+1}교시 : {value}" for key,
                           value in enumerate(_time_table)]
        answer = [f"[📆{set_grade}학년 {set_class}반 {date} 시간표입니다.]",
                  ("-".join(_res_time_table)).replace("-", "\n")]
    except:
        answer = ["오류!", ERROR_MESSAGE]

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

        try:
            answer = ["[🍚" + m + "월 " + d + "일 중식입니다.]", data['mealServiceDietInfo']
                      [1]['row'][0]['DDISH_NM'].replace("<br/>", "\n")]
        except KeyError:
            answer = ["오류!", ERROR_MESSAGE]
    except UnboundLocalError:
        answer = ["오류!", ERROR_MESSAGE]

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

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    try:
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
    except:
        answer = ["오류!", ERROR_MESSAGE]

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


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
