import covid
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType, component

class Button_Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Covids")
    async def Covid(self, ctx):
        one = Button(label="🦠 확진환자", style=ButtonStyle.blue, id="Embed1")
        two = Button(label="😷 격리중", style=ButtonStyle.blue, id="Embed2")
        three = Button(label="😂 격리해제", style=ButtonStyle.blue, id="Embed3")
        four = Button(label="🩸 사망자", style=ButtonStyle.red, id="Embed4")

        Embed1 = discord.Embed(title='코로나19 국내 발생현황',description="",color=0xFF0F13).add_field(name='🦠 확진환자',value=f'{covid.totalcovid}({covid.todaytotalcovid}) 명'f'\n\n국내발생: {covid.todaydomecovid} 명'f'\n해외유입: {covid.todayforecovid} 명',inline=False).set_footer(text=covid.datecr.string)

        Embed2 = discord.Embed(title='코로나19 국내 발생현황',description="",color=0xFF0F13,).add_field(name='😷 격리중',value=f'{covid.totalcaing}({covid.todaycaing}) 명',inline=False).set_footer(text=covid.datecr.string)

        Embed3 = discord.Embed(title='코로나19 국내 발생현황',description="",color=0xFF0F13).add_field(name='😂 격리해제',value=f'{covid.totalca}({covid.todayca}) 명',inline=False).set_footer(text=covid.datecr.string)
    
        Embed4 = discord.Embed(title='코로나19 국내 발생현황',description="",color=0xFF0F13).add_field(name='🩸 사망자',value=f'{covid.totaldead}({covid.todaydead}) 명',inline=False).set_footer(text=covid.datecr.string)

        await ctx.send(
            embed = discord.Embed(title='코로나19 국내 발생현황',description="",color=0xFF0F13,url='http://ncov.mohw.go.kr/').set_footer(text="밑에 버튼을 눌러 알아보세요!"),
            components=[
                [one],
                [two],
                [three],
                [four]
            ]
        )

        buttons = {
            "Embed1": Embed1,
            "Embed2": Embed2,
            "Embed3": Embed3,
            "Embed4": Embed4
        }

        while True:
            event = await self.bot.wait_for("button_click")          
            if event.channel is not ctx.channel:                # wait for the button click, get the button id
                return
            if event.channel == ctx.channel:
                response = buttons.get(event.component.id)     
                if response is None:
                    await event.channel.send(
                        "Something went wrong. Please try it again."            # error
                    )
                if event.channel == ctx.channel:
                    await event.respond(    
                        type=InteractionType.ChannelMessageWithSource,      # send the message
                        embed=response
                    )

def setup(bot):
    bot.add_cog(Button_Covid(bot))
