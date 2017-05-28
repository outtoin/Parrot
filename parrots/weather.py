from bs4 import BeautifulSoup as bs
import requests
def parse_weather(command):
    parsed = {}
    command = command.split(" ")
    parsed['loc'] = command[1]
    return parsed

def current_weather(command):
    KMA = "http://www.kma.go.kr/index.jsp"
    weather = parse_weather(command)
    res = requests.get(KMA)
    res = bs(res.text,'html.parser')
    result = {}
    for item in res.select("dl.region_weather_e"):
        if item.dt.a and weather['loc'] in item.dt.a.text:
            result['status'] = 'OK'
            result['message'] = str(dict(
                    loc = item.dt.a.text,
                    weather = item.dd.a.img['alt'],
                    temp = item.dd.p.text))
            return result
    result['status'] = 'ERROR'
    result['message'] = '날씨에 그 지역이 없어' + "서울,충청북도... 이런식으로 입력해봐"
    if weather['loc'].startswith('센티언스'):
        result['message'] = "그쪽은 영원히 흐릴거야"
    return result

    
if __name__ == '__main__':
    print(current_weather("날씨 서울"))
    print(current_weather("날씨 충청북도"))
    print(current_weather("날씨 제주도"))
    print(current_weather("날씨 으악"))
