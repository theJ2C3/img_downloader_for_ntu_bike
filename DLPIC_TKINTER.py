#多日同一資料夾
# [python執行檔位置] -m pip install csvsorter
from tkinter.constants import END, NONE
from bs4 import BeautifulSoup
import requests
import os
from itertools import chain # the second of three
import datetime
import base64
import tkinter as tk
import tkinter.font as tkfont

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


class downloader(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createwidgets()

    def createwidgets(self):
        
        f1 = tkfont.Font(size =12,family = "Courier New")
        f2 = tkfont.Font(size=10,family="Courier New")
        
        text1 = "請輸入開始搜尋日期，中間用逗號分開:(ex: 2020,11,20)"
        self.lbldate1 = tk.Label(self, text = text1, height = 1, width=50, font = f1)
        self.inputdate1 = tk.Text(self, height = 1, width=30, font = f1)
        text2 = "請輸入結束搜尋日期，中間用逗號分開:(ex: 2021,1,22)"
        self.lbldate2 = tk.Label(self, text = text2, height = 1, width=50, font = f1)
        self.inputdate2 = tk.Text(self, height = 1, width=30, font = f1)
        textsearch = "開始搜尋"
        self.btnpush = tk.Button(self, text=textsearch,  height = 1, command=self.clickbtn, width=80, font=f2)
        outputtext = ""
        self.outputarea = tk.Label(self,text = outputtext, height = 20, width=80, font = f2)

        # grid
        self.lbldate1.grid(row=0, column=0,sticky= tk.NE+ tk.SW)
        self.inputdate1.grid(row=0, column=1,sticky= tk.NE+ tk.SW)
        self.lbldate2.grid(row=1, column=0,sticky= tk.NE+ tk.SW)
        self.inputdate2.grid(row=1, column=1,sticky= tk.NE+ tk.SW)
        self.btnpush.grid(row=2, column=0, columnspan=2, sticky= tk.NE+ tk.SW)
        self.outputarea.grid(row=3, column = 0, columnspan=2,sticky= tk.NE+ tk.SW)

    def clickbtn(self):
        date1 = self.inputdate1.get("1.0",END)
        y1, m1, d1 = date1.split(",")
        date1 = datetime.date(int(y1), int(m1), int(d1))
        date2 = self.inputdate2.get("1.0",END)
        y2, m2, d2 = date2.split(",")
        date2 = datetime.date(int(y2), int(m2), int(d2))

        delta = datetime.timedelta(days=-1)
        # print(date2)
        if (date2 < date1):
            temp = date1
            date1 = date2
            date2 = temp

        while (date1+delta != date2):
            print(date2)
            download_pic(date2)
            self.outputarea.configure(text = str(self.outputarea.cget("text")) + "\n" +str(date2))
            # self.createwidgets()
            # newtext = str(self.outputarea.cget("text")) + "\n" +str(date2)
            # self.outputarea["text"] = (newtext)
            # print(self.outputarea.cget("text"))
            date2 += delta
        print("finish")
        self.outputarea.configure(text =  str(self.outputarea.cget("text")) + "\n" +"finish!")

        return NONE


##selecting date

# now = datetime.date.today()
# delta = datetime.timedelta(days=-1)
# # day = now

# for i in range(100):
#     day = (now + delta*i)
#     download_pic(day)
#     print(day)

        
# print("finish")

dlr = downloader()
dlr.master.title("bike img downloader")
dlr.mainloop()
