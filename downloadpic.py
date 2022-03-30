#多日同一資料夾
# [python執行檔位置] -m pip install csvsorter
from bs4 import BeautifulSoup
import requests
import os
from itertools import chain # the second of three
import datetime
import base64

def download_pic(date):
    A = str(date.strftime('%Y/%m/%d'))
    Z = str(date.strftime('%Y-%m-%d'))

    ##forming url
    message_bytes = A.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    selected_date = base64_message
    # print(base64_message)

    ##find link and number of picture
    response = requests.get(f"https://mybike.ntu.edu.tw/bike.announcement/towing/fdate/{selected_date}/ftype/999")#daterelated
    soup = BeautifulSoup(response.text, "lxml")

    results = soup.find_all("img", limit=20)
    image_links = [result.get("src") for result in results]  # 取得圖片來源連結
    results = soup.find_all("span", limit=62)
    span_links = [span.text for span in results]  # 取得文字檔

    del image_links[0]
    del image_links[0]
    del span_links[0]
    del span_links[0]
    span_links  = list(chain(*zip(span_links[1::3])))
    span_links = span_links[:-1]
    span_links = span_links[:-1]

    string = 'https://mybike.ntu.edu.tw/'
    image_links = [string + link for link in image_links]
    ##endding find link and number of picture

    ##download all pics
    for index, link in enumerate(image_links, start=0):

        if not os.path.exists("pic"):
            os.mkdir("pic")  # 建立資料夾 #daterelated

        img = requests.get(link)  # 下載圖片

        with open("pic\\" + Z + "-" + span_links[index] + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔#daterelated
            file.write(img.content)  # 寫入圖片的二進位碼
            
    return None

##selecting date

now = datetime.date.today()
delta = datetime.timedelta(days=-1)
# day = now

for i in range(100):
        day = (now + delta*i)
        download_pic(day)
        print(day)

        
print("finish")
