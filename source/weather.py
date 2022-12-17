from platform import system
import requests
from datetime import datetime

API_KEY = "ea7fe311f8414e77beb0e2dde3063d3e"
LONGITUDE = 114.03
LATITUDE = 22.61

_lastUpdate = ["00:00",None]

def get_weather():
    global _lastUpdate
    if abs(int(_lastUpdate[0].split(":")[1]) - int(datetime.now().strftime("%H:%M:%S").split(":")[1])) >= 5  or  abs(int(_lastUpdate[0].split(":")[0]) != int(datetime.now().strftime("%H:%M:%S").split(":")[0])):
        data = requests.get("https://devapi.qweather.com/v7/weather/now?key="+str(API_KEY)+"&location="+str(LONGITUDE)+","+str(LATITUDE)).json()#fetch json data
        data = data["now"]
        text = data["text"] + "  温度："+ data["temp"]+"  感知温度：" + data["feelsLike"] + "  降雨量" + data["precip"]
        _lastUpdate = [datetime.now().strftime("%H:%M:%S"),text]
        return text
    else:
        return _lastUpdate[1]

if __name__ == "__main__":
    print(get_weather())