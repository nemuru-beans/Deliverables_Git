#import os
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    BroadcastRequest,
    TextMessage)
#import json
import requests
from bs4 import BeautifulSoup
import re

def getYahooWeather(AreaCode):
    url = "https://weather.yahoo.co.jp/weather/jp/13/" + str(AreaCode) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    maxTemp = re.split(r'[\[\]]', rs[20])
    minTemp = re.split(r'[\[\]]', rs[21])
    if maxTemp[1][0] == '+':
        maxDepend = '今日よりも' + str(maxTemp[1][1:]) + '℃高くなる見通しです。'
    elif maxTemp[1][0] == '-':
        maxDepend = '今日よりも' + str(maxTemp[1][1:]) + '℃低くなる見通しです。'
    else:
        maxDepend = '今日とほぼ変わらない見通しです。'
    if minTemp[1][0] == '+':
        minDepend = '今日よりも' + maxTemp[1][1:] + '℃高くなる見通しです。'
    elif minTemp[1][0] == '-':
        minDepend = '今日よりも' + maxTemp[1][1:] + '℃低くなる見通しです。'
    else:
        minDepend = '今日とほぼ変わらない見通しです。'
    if int(maxTemp[1][1:]) >= 3 or int(maxTemp[1][1:]) >= 3:
        tempAlert = '気温の変動が大きくなる見通しです。自律神経の乱れに注意しましょう。\n'
    else:
        tempAlert = ''
    
    rain = []
    for i in range(4):
        if rs[i+28] != '---':
            rain.append(int(rs[i+28][:-1]))
        else:
            rain.append(0)
    rainMax = max(rain)
    #print(rainMax)
    if rainMax <= 10:
        rainText = '雨はほとんど降らない見通しです。洗濯のチャンスです。'
    elif rainMax <= 50:
        rainText = '雨が降る可能性があります。折り畳み傘を持って行きましょう。'
    else:
        rainText = '雨が降る見込みです。長傘を持って行ってもいいかもしれません。'
    return  "こんばんは。お天気くんが明日、" + rs[18] + "の東京都の天気をお知らせします。\n\n\
明日の天気は" + rs[19] + "、最高気温は" + maxTemp[0] + ", 最低気温は" + minTemp[0] + "です。\n"\
"明日の最低気温は" + minDepend + '\n明日の最高気温は' + maxDepend + "\n"\
+ tempAlert +\
"明日の降水確率は最高で" + str(rainMax) + "%です。" + rainText +  "\n\
\n以上、自動配信にてお届けしました。"
message=TextMessage(text=getYahooWeather("4410"))
channel_access_token = 'ここにチャンネルアクセストークンを入力'
configuration = Configuration(access_token=channel_access_token)
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
    line_bot_api.broadcast(BroadcastRequest(messages=[message]))
