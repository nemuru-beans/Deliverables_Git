#from dotenv import load_dotenv
import re
import requests
from bs4 import BeautifulSoup
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    BroadcastRequest,
    TextMessage)
import 天気予報.config as config
#import json
#import os

channel_access_token = config.CHANNEL_ACCESS_TOKEN

def get_yahoo_weather(area_code):
    """4桁のエリアコードを取得し、そのエリアの翌日の天気をYahoo!天気から取得、文章として返す"""
    url = "https://weather.yahoo.co.jp/weather/jp/13/" + str(area_code) + ".html"
    r = requests.get(url, timeout=10.0)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    max_temp = re.split(r'[\[\]]', rs[20])
    min_temp = re.split(r'[\[\]]', rs[21])
    max_zero = False
    min_zero = False
    if max_temp[1][0] == '+':
        max_depend = '今日よりも' + str(max_temp[1][1:]) + '℃高くなる見通しです。'
    elif max_temp[1][0] == '-':
        max_depend = '今日よりも' + str(max_temp[1][1:]) + '℃低くなる見通しです。'
    else:
        max_depend = '今日とほぼ変わらない見通しです。'
        max_zero = True
    if min_temp[1][0] == '+':
        min_depend = '今日よりも' + str(min_temp[1][1:]) + '℃高くなる見通しです。'
    elif min_temp[1][0] == '-':
        min_depend = '今日よりも' + str(min_temp[1][1:]) + '℃低くなる見通しです。'
    else:
        min_depend = '今日とほぼ変わらない見通しです。'
        min_zero = True
    temp_alert = ''
    if max_zero is False and min_zero is False:
        if int(max_temp[1][1:]) >= 3 or int(max_temp[1][1:]) >= 3:
            temp_alert = '気温の変動が大きくなる見通しです。自律神経の乱れに注意しましょう。\n'
    
    rain = []
    for i in range(4):
        if rs[i+28] != '---':
            rain.append(int(rs[i+28][:-1]))
        else:
            rain.append(0)
    rain_max = max(rain)
    #print(rain_max) #テスト用
    if rain_max <= 10:
        rain_text = '雨はほとんど降らない見通しです。洗濯のチャンスです。'
    elif rain_max <= 50:
        rain_text = '雨が降る可能性があります。折り畳み傘を持って行きましょう。'
    else:
        rain_text = '雨が降る見込みです。長傘を持って行ってもいいかもしれません。'
    return  "こんばんは。お天気くんが明日、" + rs[18] + "の東京都の天気をお知らせします。\n\n\
明日の天気は" + rs[19] + "、最高気温は" + max_temp[0] + ", 最低気温は" + min_temp[0] + "です。\n"\
"明日の最低気温は" + min_depend + '\n明日の最高気温は' + max_depend + "\n"\
+ temp_alert +\
"明日の降水確率は最高で" + str(rain_max) + "%です。" + rain_text +  "\n\
\n以上、自動配信にてお届けしました。"
message=TextMessage(text=get_yahoo_weather("4410"))
#CHANNEL_ACCESS_TOKEN = 'ここにアクセストークンを置いていた'
configuration = Configuration(access_token=channel_access_token)
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
    line_bot_api.broadcast(BroadcastRequest(messages=[message]))
#print(message)