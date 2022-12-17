import urllib
import requests

def chat(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]

if __name__ == "__main__":
    while True:
        msg = input("Input>>")
        res = chat(msg)
        print("Output>>", res)