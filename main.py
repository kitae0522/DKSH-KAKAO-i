from flask import Flask, request, jsonify
from datetime import datetime
from pytz import timezone
import requests
import json
import pymysql
import random
import os

ERROR_MESSAGE : str = "🤦🏻‍♂️학교 또는 기상청에서 제공하는 데이터 정보가 없습니다. 나중에 다시 시도해주세요."

headers : dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

quickReplies : list = [
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
    }
]

def dbconn() -> None:
	with open(f"{os.getcwd()}/pw.txt") as file:
		return pymysql.connect(
			host="kitae0522.mysql.pythonanywhere-services.com",
			user="kitae0522",
			password=f"{file.readline()}",
			db="kitae0522$ddlife",
			charset="utf8"
		)

def select_time_table(id : int) -> list:
	ret = []
	try:
		db = dbconn()
		c = db.cursor()
		c.execute(f"select * from time_table where id={id}")
		ret = c.fetchall()
	except Exception as e:
		print(f"db error : {e}")
	finally:
		return ret

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, Flask!"


@app.route('/time_table', methods=['POST'])
def time_table():
    req : dict = request.get_json()

    set_grade : str = req["action"]["detailParams"]["set_grade"]["value"]
    set_class : str = req["action"]["detailParams"]["set_class"]["value"]
    date : str = json.loads(req["action"]["detailParams"]["sys_date"]["value"])["dateTag"]

    date_dict :dict = {
    	"Monday" : ["월요일", 1],
    	"Tuesday" : ["화요일", 2],
    	"Wednesday" : ["수요일", 3],
    	"Thursday" : ["목요일", 4],
    	"Friday" : ["금요일", 5]
    }

    try:
        index : int = 25*(int(set_grade)-1) + (int(set_class)-1)*5 + date_dict[date][1] - 1
        time_table_db : list = list(select_time_table(index)[0])
        period : int = 1
        res_time_table : list = []
        for key, value in enumerate(time_table_db):
        	if key >= 4 and value != None:
        		res_time_table.append(f"{period}교시 : {value}")
        		period += 1
        answer : list = [f"[📆{set_grade}학년 {set_class}반 {date_dict[date][0]} 시간표입니다.]", "-".join(res_time_table).replace("-", "\n")]

    except:
        answer : list = ["오류!", ERROR_MESSAGE]

    res : dict = {
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


@app.route('/meal', methods=['POST'])
def meal():
    req : dict = request.get_json()

    date : str = json.loads(req["action"]["detailParams"]["sys_date"]["value"])["dateTag"]

    try:
        if date == "today":
            YMD : str = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
            m : str = datetime.now(timezone('Asia/Seoul')).strftime('%m')
            d : str = datetime.now(timezone('Asia/Seoul')).strftime('%d')
        elif date == "tomorrow":
            YMD : str = str(int(datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d'))+1)
            m : str = datetime.now(timezone('Asia/Seoul')).strftime('%m')
            d : str = str(int(datetime.now(timezone('Asia/Seoul')).strftime('%d'))+1)
        url : str = "https://open.neis.go.kr/hub/mealServiceDietInfo?type=json&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7010137&MLSV_YMD=" + YMD
        res = requests.get(url, headers=headers)
        data :dict = json.loads(res.text)

        try:
            answer : list = ["[🍚" + m + "월 " + d + "일 중식입니다.]", data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].replace("<br/>", "\n")]
        except KeyError:
            answer : list = ["오류!", ERROR_MESSAGE]

    except UnboundLocalError:
        answer : list = ["오류!", ERROR_MESSAGE]

    res : dict = {
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


@ app.route('/boj', methods=['POST'])
def boj():
    req : dict = request.get_json()

    boj_name : str= req["action"]["detailParams"]["boj_name"]["value"]

    url : str = "https://api.solved.ac/v2/search/recommendations.json?query=" + boj_name

    word : list = [["복잡성을 통제하는 것이 컴퓨터 프로그래밍의 기초다.", "- Brian Kernighan, 유닉스 창시자"],
            ["컴퓨터는 쓸모가 없다. 그것은 그냥 대답만 할 수 있다.", "- Pablo Picasso, 화가"],
            ["컴퓨터 언어를 설계하는 것은 공원을 산책하는 것과 같다. '쥬라기 공원!!!'",
                "- Larry Wall, Perl 언어 창시자"],
            ["만일 디버깅이 벌레를 잡는 과정이라면 프로그래밍은 그걸 집어넣는 과정이다.",
             "- E.W Dijkstra, 컴퓨터 과학자(다익스트라 알고리즘 고안)"],
            ["제발 안 쉬운 걸 쉽다고 이야기하지 마세요.", "- Alan Cooper, 비주얼 베이직의 아버지"],
            ["640KB면 모든 사람들에게 충분하다.", "- Bill Gates, 마이크로소프트 창립자"]
            ]

    ran_word : str = random.choice(word)

    crawl_data = requests.get(url, headers=headers)
    data : dict = json.loads(crawl_data.text)

    user_count : int = data["result"]["user_count"]
    if user_count == 1:
        solved : int = data["result"]["users"][0]["solved"]
        level : int = data["result"]["users"][0]["level"]
        tier : str = "Bronze" if level < 6 else "Silver" if level >= 6 and level < 11 else "Gold" if level >= 11 and level < 16 else "Platinum" if level >= 16 and level < 21 else "Diamond" if level >= 21 and level < 26 else "Ruby" if level >= 26 else None
        level : int = 6 - (level % 5 if level % 5 else 1)

        answer : list = [f"[{boj_name} 유저의 백준 정보입니다!]",
                  f"티어 : {tier} {level}\n푼 문제 갯수 : {solved}\n\n{ran_word[0]}\n{ran_word[1]}"]
    else:
        answer : list = [f"[{boj_name} 유저는 존재하지 않습니다!]",
                  f"백준 사이트 회원인데 이 메세지가 뜬 다면, https://www.acmicpc.net/setting/solved.ac 에서 설정해주세요!"]

    res : dict = {
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
    app.run(host='0.0.0.0', port=88088, threaded=True)
