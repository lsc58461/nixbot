#pyinstaller --icon=NIX.ico --onefile NIXBOT.py

import os
import discord
import datetime
import re
import configparser
import requests_async as requests

from ftplib import FTP
from urllib import request
from discord.ext import commands, tasks
from itertools import cycle
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('Config.ini', encoding='UTF-8-SIG') 
config.sections()
client = commands.Bot(command_prefix = '!')
status = cycle(['Produced By JeongYun','NIX 4.0'])
now = datetime.datetime.now()
Data_File = 'Data.ini'
FileName = Data_File
Data_URL = os.environ["Data_URL"]
Channel_ID = int(os.environ["Channel_ID"])
Token = os.environ["Token"]
config.read(Data_File, encoding='UTF-8-SIG') 
config.sections()
title2 = config['Data']['title']

ftp = FTP('fxserver.dothome.co.kr')
ftp.login(os.environ["Server_ID"], os.environ["Server_PW"])
ftp.cwd('html/DATA')

a = 1

@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

@tasks.loop(seconds=2)
async def mains():
    global a
    now = datetime.datetime.now()
    if a == 0:
        print(f"{now})  전송 시작")
        channel = client.get_channel(Channel_ID)
        print(f"{now})  채널 이름:{channel}\n{now})  채널 ID:{Channel_ID}")
        URL = await requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
        URL = URL.text

        #패치노트 주소
        soup = BeautifulSoup(URL, 'html.parser')
        PatchNote_URL_find = soup.find('a', {'class': 'style__Wrapper-i44rc3-0 style__ResponsiveWrapper-i44rc3-13 gkCnQM isVisible'})
        PatchNote_URL = "https://kr.leagueoflegends.com" + PatchNote_URL_find.get('href')
        print(f"{now})  패치노트 URL:\n{now})  {PatchNote_URL}")

        #패치노트 이미지 주소
        PatchNote_URLs = await requests.get(PatchNote_URL)
        soup = BeautifulSoup(PatchNote_URLs.text, 'html.parser')
        PatchNote_Image_Find = soup.find('a', {'class':'skins cboxElement'})
        PatchNote_Image_URL = PatchNote_Image_Find.get('href')
        print(f"{now})  패치노트 이미지 URL:\n{now})  {PatchNote_Image_URL}")

        #패치노트 제목
        soup = BeautifulSoup(URL, "html.parser")
        for a in soup.find('h2'):
            PatchNote_Title = a.string
            print(f"{now})  패치노트 TITLE:{PatchNote_Title}")

        config['Data'] = {}
        config['Data']['title'] = PatchNote_Title
        with open(Data_File, 'w', encoding='UTF-8-SIG') as configfile:
            config.write(configfile)

        config.read(Data_File, encoding='UTF-8-SIG') 
        config.sections()
        title2 = config['Data']['title']
        print(f"{now})  패치노트 세이브 TITLE:{title2}")

        PatchNote_URL2 = await requests.get(PatchNote_URL)
        soup = BeautifulSoup(PatchNote_URL2.text, "html.parser")
        PatchNote_Text = soup.find('blockquote', {'class': 'blockquote context'})
        PatchNote_Text = re.sub('<.+?>', '', str(PatchNote_Text), 0).strip()
        print(f"PATCHNOTE TEXT:{PatchNote_Text}")

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
            value =  "`" + PatchNote_Text[0:266] + "· · ·" + "`",
            inline = True
        )
        MyEmbed.set_author(
            name = "League of Legends",
            icon_url = "https://cdn.discordapp.com/attachments/811123288352358441/811695474952110110/NIX.png"
        )     
        MyEmbed.set_image(
            url = PatchNote_Image_URL
        )
        '''
        MyEmbed.set_footer(
            text = f"NIX - Automation Technology\nRequsetID : {message.author.id}"
        )
        '''     
        await channel.send(embed=MyEmbed)
        print(f"{now})  패치노트 전송 성공")
        print(f"{now})  a == {a}")
        a = 1

@tasks.loop(seconds=10)
async def Title_Detected():
    URL = await requests.get("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes")
    now = datetime.datetime.now()
    global a
    soup = BeautifulSoup(URL.text, "html.parser")
    for a in soup.find('h2'):
        PatchNote_Title = a.string
    
    File_Save = Data_File
    mem = request.urlopen(Data_URL).read()

    with open(File_Save, mode="wb") as f:
        f.write(mem)
        print((f"{now})  FTP Data.ini 다운로드 완료"))

    config.read(Data_File, encoding='UTF-8-SIG') 
    config.sections()
    title2 = config['Data']['title']
    
    print(f"{now})  패치노트 감지 중:{PatchNote_Title}")
    if title2 != PatchNote_Title:
        print(f"{now})  패치노트 제목 변경감지\n{now})  패치노트 제목:{PatchNote_Title}")
        
        config['Data'] = {}
        config['Data']['title'] = PatchNote_Title
        with open(Data_File, 'w', encoding='UTF-8-SIG') as configfile:
            config.write(configfile)
        
        ftp = FTP('fxserver.dothome.co.kr')
        ftp.login('fxserver', 'dlswb4fkd!')
        ftp.cwd('html/DATA')  # 업로드할 FTP 폴더로 이동
        myfile = open(FileName,'rb')  # 로컬 파일 열기
        print(f"{now})  FTP 로컬 파일 열기 완료")
        ftp.storbinary('STOR ' +FileName, myfile )  # 파일을 FTP로 업로드
        print(f"{now})  FTP 업로드 완료")
        myfile.close()  # 파일 닫기
        print(f"{now})  FTP 파일 닫기 완료")
        ftp.quit()
        print(f"{now})  FTP 모듈 종료")
        a = 0
        print(f"{now})  a = 0 반환 완료")
        
@client.event
async def on_ready():
    print(f"{now})---------------    CONNECTED    ---------------")
    print(f"{now})  봇 이름 : {client.user.name}")
    print(f"{now})  봇 ID : {client.user.id}")
    print(f"{now})-----------------------------------------------")
    
    change_status.start()
    mains.start()
    Title_Detected.start()
    
client.run(Token)
