import sqlite3
import urllib.request as req
from bs4 import BeautifulSoup

#取得資料
def GetData(url):
    #設置Request Headers的資訊
    request = req.Request(url,headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8") #解碼

    
    Data = BeautifulSoup(data,"html.parser") #解析原始碼
    titles = Data.find_all("div", class_="title") #尋找所有class="title"的div標籤

    for title in titles:        
        #如果標題存在，就顯示資訊
        if title.a != None:
            title_url = 'https://www.ptt.cc'+title.a['href'] #標題網址
            print(title.a.string)
            print('網址:'+title_url+'\n')

            #執行SQL指令
            cur.execute("insert into Ptt_Movie_DB values('{}','{}')" .format(title.a.string,title_url)) 
            conn.commit() #寫入資料庫


if __name__ == "__main__":
    url = "https://www.ptt.cc/bbs/movie/index.html" #Ptt電影版網址
    db_Path = r'.\Crawler_PTT_Movie_DB.db'
    conn = sqlite3.connect(db_Path)
    cur = conn.cursor()
    GetData(url)
    print('已寫入資料庫!')
    cur.close() #關閉資源
    conn.close() #關閉連接
