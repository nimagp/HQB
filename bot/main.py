import discord
from replit import db
import os
from discord.ext import commands
from live import alive
import asyncio

javab    = ''
porsande = ''
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="hqb.")
bot.remove_command("help")
help_embed = discord.Embed(title="راهنمای سوالات جهنمی:",description="""
***تمامی دستورات با ***`.hqb`*** آغاز می شوند***

:fire::question:`help` : نمایش راهنما \n========
:fire::question:`add` : پیشنهاد سوال \n========
:fire::question:`bug` : گزارش باگ \n========
:fire::question:`ping` : دریافت میزان تاخیر ربات \n========
:fire::question:`start` : آغاز گیم \n========
:fire::question:`question` : پرسش سوال تکی \n========
""", color=0xffffff)
#template: :fire::question:`command` : توضیحات \n========

@bot.event
async def on_ready():
    channel = bot.get_channel(870624299877277716)
    embed=discord.Embed(title=f"ربات روشن شد!", description="هم اکنون میتوانید از ربات استفاده کنید", color=0x00ff00)
    await channel.send(embed=embed)
    print(f"Logged in as {bot.user.name}({bot.user.id}")



@bot.command(name="help",help="نمایش راهنما",aliases=["h","راهنما"])
async def help(ctx):
    await ctx.reply(embed=help_embed)


@bot.command(help='پینگ ربات')
async def ping(ctx):
    await ctx.reply(f"پونگ! `{str(round(bot.latency * 1000))}` میلی ثانیه")



@bot.command(name="bug", help="گزارش باگ به ادمین ها")
async def bug(ctx, *, message):
    channel = bot.get_channel(870551794273644565)
    embed=discord.Embed(title=f"ّباگ جدید از {ctx.message.author.name}", description=message, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("باگ گزارش شد")

    
@bot.command(help="افزودن سوال")
async def add(ctx, *, question):
    channel = bot.get_channel(870559120476999690)
    embed = discord.Embed(title=f"سوال جدید از {ctx.message.author.name}", description=question, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("سوال پیشنهادی شما برای بررسی ارسال شد")

@bot.command(name="question",help='ارسال یک پرسش')
async def question(ctx):
    def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author

    qmsg = await ctx.send("لورم  ایپسوم")
    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
        await qmsg.edit(content=f'{qmsg.content}\nجواب {msg.author.mention}:\n{msg.content}')
    except asyncio.TimeoutError:
        await ctx.send("جواب نمیدی پلشت؟ با دمپایی ابری هلیکوپتری بیام دهنت؟")

@bot.command()
async def start(ctx):
    await ctx.send("گیم را استارت میکنیم الا برکت الله")
    for i in range(1,6):
        await ctx.send(f"پرسش {i}:")
        await question(ctx)
    await ctx.send("گیم تموم شد! خوش باشید!")




alive()
bot.run(TOKEN)