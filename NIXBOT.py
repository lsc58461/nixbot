#pyinstaller --icon=NIX.ico --onefile NIXBOT.py

import os
import json
import discord
import datetime
import re
import configparser
import requests as requestss
import requests_async as requests

from ftplib import FTP
from urllib import request
from discord.ext import commands, tasks
from itertools import cycle
from bs4 import BeautifulSoup

locale = ""
config = configparser.ConfigParser()
config.read('Config.ini', encoding='UTF-8-SIG') 
config.sections()
client = commands.Bot(command_prefix = ';')
status = cycle(['Produced By JeongYun','LOL PatchNotes'])
now = datetime.datetime.now()
Data_PatchNote_File = 'Data.ini'
Data_Issues_File = 'Data_Issues.ini'
Data_Issues_Empty_File = "Data_Issues_Empty.ini"
Issues_JSON_File = 'Issues.json'
FileName_PatchNote = Data_PatchNote_File
FileName_Issues = Data_Issues_File
Data_URL = os.environ["Data_URL"]

#채널 ID
Channel_ID_PatchNote = int(os.environ["Channel_ID_PatchNote"])
Channel_ID_PatchNote2 = int(os.environ["Channel_ID_PatchNote2"])
Channel_ID_Issues = int(os.environ["Channel_ID_Issues"])
Channel_ID_Issues2 = int(os.environ["Channel_ID_Issues2"])

#토큰
Token = os.environ["Token"]

config.read(Data_PatchNote_File, encoding='UTF-8-SIG') 
config.sections()
title2 = config['Data']['title']

config.read(Data_Issues_File, encoding='UTF-8-SIG') 
config.sections()
Issues2 = config['Data']['Issues']

ftp = FTP('fxserver.dothome.co.kr')
ftp.login(os.environ["Server_ID"], os.environ["Server_PW"])
ftp.cwd('html/DATA')

a = 0 #Post_PatchNote
b = 0 #Post_Issues
c = 0 #Post_Issues_Empty
cc = ""

@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

@tasks.loop(seconds=2)
async def Post_PatchNote():
    try:
        global a
        if a == 1:
            now = datetime.datetime.now()
            print(f"{now})  전송 시작")
            channel = client.get_channel(Channel_ID_PatchNote)
            channel2 = client.get_channel(Channel_ID_PatchNote2)
            print(f"{now})  채널 이름:{channel}\n{now})  채널 ID:{Channel_ID_PatchNote}")
            print(f"{now})  채널 이름:{channel2}\n{now})  채널 ID:{Channel_ID_PatchNote2}")
            URL = await requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
            URL.encoding = 'UTF-8-SIG'
            URL = URL.text

            #패치노트 주소
            soup = BeautifulSoup(URL, 'html.parser')
            PatchNote_URL_find = soup.find('a', {'class': 'style__Wrapper-sc-1h41bzo-0'})
            PatchNote_URL = "https://kr.leagueoflegends.com" + PatchNote_URL_find.get('href')
            print(f"{now})  패치노트 주소\n{now})    -{PatchNote_URL}")

            #패치노트 이미지 주소
            PatchNote_URLs = await requests.get(PatchNote_URL)
            soup = BeautifulSoup(PatchNote_URLs.text, 'html.parser')
            PatchNote_Image_Find = soup.find('a', {'class':'skins cboxElement'})
            PatchNote_Image_URL = PatchNote_Image_Find.get('href')
            print(f"{now})  패치노트 이미지 주소:\n{now})    -{PatchNote_Image_URL}")

            #패치노트 제목
            soup = BeautifulSoup(URL, "html.parser")
            for a in soup.find('h2'):
                PatchNote_Title = a.string
                print(f"{now})  패치노트 제목:{PatchNote_Title}")

            config['Data'] = {}
            config['Data']['title'] = PatchNote_Title
            with open(Data_PatchNote_File, 'w', encoding='UTF-8-SIG') as configfile:
                config.write(configfile)

            config.read(Data_PatchNote_File, encoding='UTF-8-SIG') 
            config.sections()
            title2 = config['Data']['title']
            print(f"{now})  패치노트 저장 제목:{title2}")

            PatchNote_URL2 = await requests.get(PatchNote_URL)
            PatchNote_URL2.encoding = 'UTF-8-SIG'
            soup = BeautifulSoup(PatchNote_URL2.text, "html.parser")
            PatchNote_Text = soup.find('blockquote', {'class': 'blockquote context'})
            PatchNote_Text = re.sub('<.+?>', '', str(PatchNote_Text), 0).strip()
            print(f"패치노트 내용:{PatchNote_Text}")

            MyEmbed = discord.Embed(
                title = PatchNote_Title,
                url = PatchNote_URL,
                color = 0x38f2ff
            )
            MyEmbed.set_thumbnail(
                url = "https://cdn.discordapp.com/attachments/811123288352358441/831572153542639666/league_of_legends_sm.png"
            )
            MyEmbed.add_field(
                name = "\n\u200b",
                value =  '```css\n{} · · ·\n```'.format(PatchNote_Text[0:266]),
                inline = True
            )
            MyEmbed.set_author(
                name = "League of Legends",
                icon_url = "https://cdn.discordapp.com/attachments/872119542510391336/900320015935496202/15202c5af949bc39.png"
            )     
            MyEmbed.set_image(
                url = PatchNote_Image_URL
            )
            

            await channel.send(embed=MyEmbed)
            await channel2.send(embed=MyEmbed)
            print(f"{now})  패치노트 전송 성공")
            a = 0
            print(f"{now})  a == {a}")
    except Exception as ex:
        a = 1
        print(f"{now})  Post_PatchNote 에러 발생\n{now})    -{ex}")

@tasks.loop(seconds=5)
async def Title_Detected():
    try:
        global a
        URL = await requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
        URL.encoding = 'UTF-8-SIG'
        now = datetime.datetime.now()
        soup = BeautifulSoup(URL.text, "html.parser")
        for a in soup.find('h2'):
            PatchNote_Title = a.string
    
        File_Save = Data_PatchNote_File
        mem = request.urlopen(Data_URL).read()

        with open(File_Save, mode="wb") as f:
            f.write(mem)

        config.read(Data_PatchNote_File, encoding='UTF-8-SIG') 
        config.sections()
        title2 = config['Data']['title']
    
        print(f"{now})  패치노트 감지 중:{PatchNote_Title}")
        if title2 != PatchNote_Title:
            print(f"{now})  패치노트 제목 변경감지\n{now})  패치노트 제목:{PatchNote_Title}")
        
            config['Data'] = {}
            config['Data']['title'] = PatchNote_Title
            with open(Data_PatchNote_File, 'w', encoding='UTF-8-SIG') as configfile:
                config.write(configfile)
        
            ftp = FTP('fxserver.dothome.co.kr')
            ftp.login(os.environ["Server_ID"], os.environ["Server_PW"])
            ftp.cwd('html/DATA')  # 업로드할 FTP 폴더로 이동
            myfile = open(FileName_PatchNote,'rb')  # 로컬 파일 열기
            print(f"{now})  FTP 로컬 파일 열기 완료")
            ftp.storbinary('STOR ' +FileName_PatchNote, myfile )  # 파일을 FTP로 업로드
            print(f"{now})  FTP 업로드 완료")
            myfile.close()  # 파일 닫기
            print(f"{now})  FTP 파일 닫기 완료")
            ftp.quit()
            print(f"{now})  FTP 모듈 종료")
            a = 1
            print(f"{now})  a = {a} 반환 완료")
    except Exception as ex:
        print(f"{now})  Title_Detected 에러 발생\n{now})    -{ex}")
      
@client.event
async def on_ready():
    print(f"{now})---------------    CONNECTED    ---------------")
    print(f"{now})  봇 이름 : {client.user.name}")
    print(f"{now})  봇 ID : {client.user.id}")
    print(f"{now})-----------------------------------------------")
    
    change_status.start()
    Post_PatchNote.start()
    Title_Detected.start()

client.run(Token)
