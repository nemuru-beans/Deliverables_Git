from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
)
from linebot.v3.messaging import (
    PushMessageRequest,
    TextMessage
)
import requests
from bs4 import BeautifulSoup
def GetYahooWeather(AreaCode):
    url = "https://weather.yahoo.co.jp/weather/jp/13/" + str(AreaCode) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    return  "明日の天気は" + rs[19] + "、気温は" + rs[20] + ", " + rs[21] + "です。"

channel_access_token = 'ここにアクセストークンを入力！'
configuration = Configuration(access_token=channel_access_token)
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
message=TextMessage(text=GetYahooWeather("4410"))

line_bot_api.push_message_with_http_info(
            PushMessageRequest(
                to='ここに送信先を入力！',
                messages=[message]
            )
        )