#pyinstaller --icon=NIX.ico --onefile NIXBOT.py

import os
import discord
import configparser

from urllib import request
from itertools import cycle
from discord.ext import commands, tasks
from Now_Time import Time
from Read_Config import Config_Title
from FTP_TitleName_Post import FTP_Post
from Crawling_PatchNote import Crawling_URL, Crawling_Title, Crawling_Content, Crawling_Image_URL

config = configparser.ConfigParser()
client = commands.Bot(command_prefix = ';')
status = cycle(['Produced By JeongYun','LOL PatchNotes'])

Data_PatchNote_File = 'Data.ini'
Data_URL = "http://fxserver.dothome.co.kr/DATA/Data.ini"

#채널 ID
Channel_ID_PatchNote = int("811169207327653908")

#토큰
Token = os.environ["Token"]

Contour = "--------------------------------------------------------------------------"

@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

@tasks.loop(count=1)
async def Post_PatchNote():
    try:
        channel = client.get_channel(Channel_ID_PatchNote)
        
        MyEmbed = discord.Embed(
            title = Crawling_Title(),
            url = Crawling_URL(),
            color = 0x38f2ff
        ).set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/811123288352358441/831572153542639666/league_of_legends_sm.png"
        ).add_field(
            name = "\n\u200b",
            value = '```css\n{} · · ·\n```'.format(Crawling_Content()[0:266]),
            inline = True
        ).set_author(
            name = "League of Legends",
            icon_url = "https://cdn.discordapp.com/attachments/872119542510391336/900320015935496202/15202c5af949bc39.png"
        ).set_image(
            url = Crawling_Image_URL()
        )
        await channel.send(embed=MyEmbed)
        print(f"{Time()})  패치노트 전송 성공\n{Contour}")
        return
    except Exception as ex:
        print(f"{Time()})  Post_PatchNote 에러 발생\n{Time()})    -{ex}\n{Contour}")
        return
    
@tasks.loop(seconds=30)
async def Title_Detected():
    try:
        Get_Server_Save_Title = request.urlopen(Data_URL).read()
        with open(Data_PatchNote_File, mode="wb") as f:
            f.write(Get_Server_Save_Title)
        config.read('Data.ini', encoding='UTF-8-SIG')
        Get_Server_Save_Title = config['Data']['Title']
        Title = Crawling_Title()
        print(f"{Time()})  패치노트 감지 중:{Title}\n{Time()})  Get_Server_Save_Title:{Get_Server_Save_Title}\n{Contour}")
        if Get_Server_Save_Title != Title:
            if Title == None:
                print(f"{Time()})  Crawling_Title:None")
                return
            else:
                print(f"{Time()})  패치노트 제목 변경감지\n{Time()})  패치노트 제목:{Title}")
                config['Data'] = {}
                config['Data']['Title'] = Title
                with open(Data_PatchNote_File, 'w', encoding='UTF-8-SIG') as configfile:
                    config.write(configfile)
                FTP_Post(Data_PatchNote_File)
                Post_PatchNote.start()
                return
    except Exception as ex:
        print(f"{Time()})  Title_Detected 에러 발생\n{Time()})    -{ex}")
        return
      
@client.event
async def on_ready():
    print(f"{Time()})---------------    CONNECTED    ---------------")
    print(f"{Time()})  봇 이름 : {client.user.name}")
    print(f"{Time()})  봇 ID : {client.user.id}")
    print(f"{Time()})-----------------------------------------------")
    
    change_status.start()
    Title_Detected.start()

client.run(Token)
