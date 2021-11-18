#pyinstaller --icon=NIX.ico --onefile NIXBOT.py

import os
import discord
import configparser
from discord.ext import commands, tasks
from itertools import cycle
from Now_Time import Time
from Read_Config import Config_Detect, Config_Title
from FTP_TitleName_Post import FTP_Post
from Crawling_PatchNote import Crawling_URL, Crawling_Title, Crawling_Content, Crawling_Image_URL

config = configparser.ConfigParser()
client = commands.Bot(command_prefix = ';')
status = cycle(['Produced By JeongYun','LOL PatchNotes'])
Data_PatchNote_File = 'Data.ini'
Data_URL = os.environ["Data_URL"]

#채널 ID
Channel_ID_PatchNote = int(os.environ["Channel_ID_PatchNote"])
Channel_ID_PatchNote2 = int(os.environ["Channel_ID_PatchNote2"])
Channel_ID_Issues = int(os.environ["Channel_ID_Issues"])
Channel_ID_Issues2 = int(os.environ["Channel_ID_Issues2"])

#토큰
Token = os.environ["Token"]

Detect = 0

@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

@tasks.loop(seconds=2)
async def Post_PatchNote():
    try:
        global Detect
        if Detect == 1:
            channel = client.get_channel(Channel_ID_PatchNote)
            
            MyEmbed = discord.Embed(
                title = Crawling_Title(),
                url = Crawling_URL(),
                color = 0x38f2ff
            )
            MyEmbed.set_thumbnail(
                url = "https://cdn.discordapp.com/attachments/811123288352358441/831572153542639666/league_of_legends_sm.png"
            )
            MyEmbed.add_field(
                name = "\n\u200b",
                value =  '```css\n{} · · ·\n```'.format(Crawling_Content()[0:266]),
                inline = True
            )
            MyEmbed.set_author(
                name = "League of Legends",
                icon_url = "https://cdn.discordapp.com/attachments/872119542510391336/900320015935496202/15202c5af949bc39.png"
            )     
            MyEmbed.set_image(
                url = Crawling_Image_URL()
            )
            await channel.send(embed=MyEmbed)
            print(f"{Time()})  패치노트 전송 성공")
            Detect = 0
            print(f"{Time()})  Detect : {Detect}")
    except Exception as ex:
        Detect = 1
        print(f"{Time()})  Post_PatchNote 에러 발생\n{Time()})    -{ex}")

@tasks.loop(seconds=5)
async def Title_Detected():
    try:
        global Detect
        Title = Config_Title()
        print(f"{Time()})  패치노트 감지 중:{Crawling_Title()}")
        if Title != Crawling_Title():
            print(f"{Time()})  패치노트 제목 변경감지\n{Time()})  패치노트 제목:{Crawling_Title()}")
            config['Data'] = {}
            config['Data']['Title'] = Crawling_Title()
            with open(Data_PatchNote_File, 'w', encoding='UTF-8-SIG') as configfile:
                config.write(configfile)
            FTP_Post(Data_PatchNote_File)
            Detect = Config_Detect()
    except Exception as ex:
        print(f"{Time()})  Title_Detected 에러 발생\n{Time()})    -{ex}")
      
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
