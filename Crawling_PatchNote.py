import re
import requests

from Now_Time import Time
from bs4 import BeautifulSoup

Data_PatchNote_File = 'Data.ini'
Data_URL = "http://fxserver.dothome.co.kr/DATA/Data.ini"
Contour = "--------------------------------------------------------------------------"

def Crawling_Title(): #패치노트 제목
    try:
        try:
            URL = requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
        except:
            print(f"{Time()})  패치노트 URL을 불러오는데 실패했어요.\n{Contour}")
            return
        URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(URL.text, "html.parser")
        try:
            for a in soup.find('h2'):
                PatchNote_Title = a.string
                if PatchNote_Title == None:
                    print(f'{Time()})  PatchNote_Title:None(Crawling_Title)\n{Contour}')
                    return
        except Exception as ex:
            print(f"{Time()})  PatchNote_Title 에러 발생\n{Time()})    -{ex}\n{Contour}")
            return
        return PatchNote_Title
    except Exception as ex:
        print(f"{Time()})  Crawling_Title 에러 발생\n{Time()})    -{ex}\n{Contour}")
        return

def Crawling_URL(): #패치노트 URL
    try:
        URL = requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
        URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(URL.text, "html.parser")
        PatchNote_URL_find = soup.find('a', {'class': 'style__Wrapper-sc-1h41bzo-0'})
        PatchNote_URL = "https://kr.leagueoflegends.com" + PatchNote_URL_find.get('href')
        print(f"{Time()})  패치노트 URL\n{Time()})    -{PatchNote_URL}\n{Contour}")
        return PatchNote_URL
    except Exception as ex:
        print(f"{Time()})  Crawling_URL 에러 발생\n{Time()})    -{ex}\n{Contour}")
        pass

def Crawling_Image_URL(): #패치노트 이미지 URL
    try:
        URL = requests.get(Crawling_URL())
        URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(URL.text, "html.parser")
        PatchNote_Image_Find = soup.find('a', {'class':'skins cboxElement'})
        PatchNote_Image_URL = PatchNote_Image_Find.get('href')
        print(f"{Time()})  패치노트 이미지 URL:\n{Time()})    -{PatchNote_Image_URL}\n{Contour}")
        return PatchNote_Image_URL
    except Exception as ex:
        print(f"{Time()})  Crawling_Image_URL 에러 발생\n{Time()})    -{ex}\n{Contour}")
        pass
    
def Crawling_Content(): #패치노트 내용
    try:      
        PatchNote_URL = requests.get(Crawling_URL())
        PatchNote_URL.encoding = 'UTF-8-SIG'
        soup = BeautifulSoup(PatchNote_URL.text, "html.parser")
        try:
            PatchNote_Text = soup.find('blockquote', {'class': 'blockquote context'})
        except:
            print(f'{Time()})  "blockquote" 요소를 찾지 못했어요.\n{Contour}')
            return
        PatchNote_Text = re.sub('<.+?>', ' ', str(PatchNote_Text), 0).strip()
        PatchNote_Text = re.sub('<.+?>', '\n', str(PatchNote_Text), 0).strip()
        PatchNote_Text = re.sub('    ', '\n', str(PatchNote_Text), 0).strip()
        print(f"{Time()})  패치노트 내용:{PatchNote_Text}\n{Contour}")
        return PatchNote_Text
    except Exception as ex:
        print(f"{Time()})  Crawling_Content 에러 발생\n{Time()})    -{ex}\n{Contour}")
        pass
