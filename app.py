from flask import Flask, render_template, request
from decouple import config
import requests
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

token = config('TELEGRAM_BOT_TOKEN')
chat_id = config('CHAT_ID')
url = "https://api.telegram.org/bot"

@app.route('/')
def hello():
    return "Hello World"

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    text = request.args.get('text')
    requests.get(f'{url}{token}/sendMessage?chat_id={chat_id}&text={text}')
    return render_template('send.html')

# 내 token을 알때만 동작
# POST 방식으로 들어올때만 동작
@app.route(f'/{token}', methods=["POST"])
def telegram():
    # 챗봇에 메시지를 보낸 사람의 ID 가져오기
    # print(request.get_json())
    data = request.get_json()
    t_chat_id = data['message']['chat']['id']
    text = data['message']['text']

    if text == "안녕":
        ret_text = "안녕하세요."
    elif text == "로또":
        numbers = range(1, 46)
        ret_text = sorted(random.sample(numbers, 6))
    elif text == "코스피":
        req = requests.get("https://finance.naver.com/sise/sise_index.nhn?code=KOSPI").text
        soup = BeautifulSoup(req, 'html.parser')
        kospi = soup.select_one('#now_value').text
        kospi_rate = soup.select_one('#change_value_and_rate').text
        ret_text = f"{kospi}    {kospi_rate}"
    elif text == "코스닥":
        req = requests.get("https://finance.naver.com/sise/sise_index.nhn?code=KOSDAQ").text
        soup = BeautifulSoup(req, 'html.parser')
        kosdoq = soup.select_one('#now_value').text
        kosdoq_rate = soup.select_one('#change_value_and_rate').text
        ret_text = f"{kosdoq}    {kosdoq_rate}"
    elif text == "멜론차트":
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://www.melon.com/chart/index.htm', headers = header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')
    
        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        songs = parse.find_all("div", {"class": "ellipsis rank02"})
        title = []
        song = []
    
        for t in titles:
            title.append(t.find('a').text)
    
        for s in songs:
            song.append(s.find('span', {"class": "checkEllipsis"}).text)
    
        for i in range(10):
            print('%3d위: %s - %s'%(i+1, title[i], song[i]))

        ret_text = f'1위 {title[0]} {song[0]}\n2위 {title[1]} {song[1]}\n3위 {title[2]} {song[2]}\n4위 {title[3]} {song[3]}\n5위 {title[4]} {song[4]}\n6위 {title[5]} {song[5]}\n7위 {title[6]} {song[6]}\n8위 {title[7]} {song[7]}\n9위 {title[8]} {song[8]}\n10위 {title[9]} {song[9]}'
    else :
        ret_text = "안녕 / 코스피 / 코스닥 / 멜론차트"
        
    requests.get(f'{url}{token}/sendMessage?chat_id={t_chat_id}&text={ret_text}')

    return "ok", 200    # 제대로 동작함, 텔레그램 특성


if __name__ == ('__main__'):
    app.run(debug=True)