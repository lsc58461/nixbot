#pyinstaller --icon=NIX.ico --onefile NIXBOT.py

import os
import discord
import datetime
import re
import configparser

from discord.ext import commands, tasks
from itertools import cycle
from urllib.request import urlopen
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('Config.ini', encoding='UTF-8-SIG') 
config.sections()
client = commands.Bot(command_prefix = '!')
status = cycle(['Produced By JeongYun','NIX 3.6'])
now = datetime.datetime.now()

URL = urlopen("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes").read()
Channel_ID = int(os.environ["Channel_ID"])
Token = os.environ["Token"]
config.read('Data.ini', encoding='UTF-8-SIG') 
config.sections()
title2 = config['Data']['title']

a = 0

@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

@tasks.loop(seconds=3)
async def mains():
    global a
    now = datetime.datetime.now()
    if a == 0:
        print(f"{now})  전송 시작")
        channel = client.get_channel(Channel_ID)
        print(f"{now})  채널 ID : {channel}\n{Channel_ID}")
        URL = urlopen("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes").read()

        #패치노트 주소
        soup = BeautifulSoup(URL, 'html.parser')
        PatchNote_URL_find = soup.find('a', {'class': 'style__Wrapper-i44rc3-0 style__ResponsiveWrapper-i44rc3-13 gkCnQM isVisible'})
        PatchNote_URL = "https://kr.leagueoflegends.com" + PatchNote_URL_find.get('href')
        print(f"{now})  패치노트 URL:\n{PatchNote_URL}")

        #패치노트 이미지 주소
        soup = BeautifulSoup(URL, 'html.parser')
        for a in soup.find('a'):
            if a.img:
                PatchNote_Image_URL = a.img['src']
                print(f"{now})  이미지 URL:\n{PatchNote_Image_URL}")

        #패치노트 제목
        soup = BeautifulSoup(URL, "html.parser")
        for a in soup.find('h2'):
            PatchNote_Title = a.string
            print(f"{now})  패치노트 TITLE:{PatchNote_Title}")

        config['Data'] = {}
        config['Data']['title'] = PatchNote_Title
        with open('Data.ini', 'w', encoding='UTF-8-SIG') as configfile:
            config.write(configfile)

        config.read('Data.ini', encoding='UTF-8-SIG') 
        config.sections()
        title2 = config['Data']['title']
        print(f"{now})  패치노트 세이브 TITLE:{title2}")

        PatchNote_URL2 = urlopen(PatchNote_URL).read()
        soup = BeautifulSoup(PatchNote_URL2, "html.parser")
        PatchNote_Text = soup.find('blockquote', {'class': 'blockquote context'})
        PatchNote_Text = re.sub('<.+?>', '', str(PatchNote_Text), 0).strip()
        #print(f"PATCHNOTE TEXT:{PatchNote_Text}")

        MyEmbed = discord.Embed(
            title = PatchNote_Title,
            url = PatchNote_URL,
            color = 0x38f2ff
        )
        MyEmbed.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/811123288352358441/811695474952110110/NIX.png"
        )
        MyEmbed.add_field(
            name = "────────────────────────",
            value = PatchNote_Text[0:266] + "     · · · · ·\n────────────────────────",
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
    URL = urlopen("https://kr.leagueoflegends.com/ko-kr/news/tags/patch-notes").read()
    now = datetime.datetime.now()
    global a
    soup = BeautifulSoup(URL, "html.parser")
    for a in soup.find('h2'):
        PatchNote_Title = a.string
    #print(f"{now})")

    config.read('Data.ini', encoding='UTF-8-SIG') 
    config.sections()
    title2 = config['Data']['title']
    print(f"{now})  패치노트 감지 중 : {PatchNote_Title}")
    if title2 != PatchNote_Title:
        a = 0
        print(f"{now})  패치노트 제목 변경감지\n패치노트 제목:{PatchNote_Title}")

@client.event
async def on_ready():
    print(f"{now})---------------    CONNECTED    ---------------")
    print(f"{now})  봇 이름 : {client.user.name}")
    print(f"{now})  봇 ID : {client.user.id}")
    print(f"{now})-----------------------------------------------")
    
    Title_Detected.start()
    change_status.start()
    mains.start()
    
client.run(Token)
