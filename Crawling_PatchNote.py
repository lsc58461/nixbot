import re
import requests

from Now_Time import Time
from urllib import request
from bs4 import BeautifulSoup


Data_PatchNote_File = 'Data.ini'
Data_URL = "http://fxserver.dothome.co.kr/DATA/Data.ini"

def Crawling_Title(): #패치노트 제목
    try:
        URL = requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
        URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(URL.text, "html.parser")
        try:
            for a in soup.find('h2'):
                PatchNote_Title = a.string
        except:
            print(f'{Time()})  "h2" 요소를 찾지 못했어요.')
            pass
        mem = request.urlopen(Data_URL).read()
        with open(Data_PatchNote_File, mode="wb") as f:
            f.write(mem)
        
        return PatchNote_Title
    except Exception as ex:
        print(f'{Time()})  "Crawling_Title" 에러 발생\n{Time()})    -{ex}')
        return

def Crawling_URL(): #패치노트 URL
    try:
        URL = requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
        URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(URL.text, "html.parser")
        PatchNote_URL_find = soup.find('a', {'class': 'style__Wrapper-sc-1h41bzo-0'})
        PatchNote_URL = "https://kr.leagueoflegends.com" + PatchNote_URL_find.get('href')
        print(f"{Time()})  패치노트 URL\n{Time()})    -{PatchNote_URL}")
        return PatchNote_URL
    except Exception as ex:
        print(f'{Time()})  "Crawling_URL" 에러 발생\n{Time()})    -{ex}')
        return

def Crawling_Image_URL(): #패치노트 이미지 URL
    try:
        URL = requests.get(Crawling_URL())
        URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(URL.text, "html.parser")
        PatchNote_Image_Find = soup.find('a', {'class':'skins cboxElement'})
        PatchNote_Image_URL = PatchNote_Image_Find.get('href')
        print(f"{Time()})  패치노트 이미지 URL:\n{Time()})    -{PatchNote_Image_URL}")
        return PatchNote_Image_URL
    except Exception as ex:
        print(f'{Time()})  "Crawling_Image_URL" 에러 발생\n{Time()})    -{ex}')
        return
    
def Crawling_Content(): #패치노트 내용
    try:      
        PatchNote_URL = requests.get(Crawling_URL())
        PatchNote_URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(PatchNote_URL.text, "html.parser")
        PatchNote_Text = soup.find('blockquote', {'class': 'blockquote context'})
        PatchNote_Text = re.sub('<.+?>', ' ', str(PatchNote_Text), 0).strip()
        PatchNote_Text = re.sub('<.+?>', '\n', str(PatchNote_Text), 0).strip()
        PatchNote_Text = re.sub('    ', '\n', str(PatchNote_Text), 0).strip()
        print(f"{Time()})  패치노트 내용:{PatchNote_Text}")
        return PatchNote_Text
    except Exception as ex:
        print(f'{Time()})  "Crawling_Content" 에러 발생\n{Time()})    -{ex}')
        return                 
