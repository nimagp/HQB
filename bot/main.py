import discord
import os
from discord.ext import commands
from live import alive
import asyncio
import requests
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="hqb.")
bot.remove_command("help")
help_embed = discord.Embed(title="راهنمای سوالات جهنمی:",description="""
***تمامی دستورات با ***`.hqb`*** آغاز می شوند***

:fire::question:`help` : نمایش راهنما \n========
:fire::question:`question` : پیشنهاد سوال \n========
:fire::question:`bug` : گزارش باگ \n========
:fire::question:`ping` : دریافت میزان تاخیر ربات \n========
:fire::question:`start` : آغاز گیم \n========
:fire::question:`pack` : پیشنهاد پک سوال  \n========
""", color=0xffffff)
#template: :fire::question:`command` : توضیحات \n========


#insert your admins here
admins=["SMM#9107","Nima Ghasemi#9847"]



@bot.command()
async def bot_is_online(ctx):
  if str(ctx.message.author) in admins:
    channel = bot.get_channel(870624299877277716)
    embed=discord.Embed(title=f"ربات روشن شد!", description="هم اکنون میتوانید از ربات استفاده کنید", color=0x00ff00)
    await channel.send(embed=embed)
    embed=discord.Embed(title="انجام شد", description="همگان دانند وضعیت مرا :)", color=0x00ff00)
    await ctx.reply(embed=embed)
  else:
    embed=discord.Embed(title="خطا", description="شما ادمین نیستید :)", color=0xFF0000)
    await ctx.reply(embed=embed)
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="hqb.help"))
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

@bot.command(help="پیشنهاد سوال")
async def question(ctx, *, question):
    channel = bot.get_channel(870559120476999690)
    embed = discord.Embed(title=f"سوال جدید از {ctx.message.author.name}", description=question, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("سوال پیشنهادی شما برای بررسی ارسال شد")

@bot.command(name="pack",help='پیشنهاد پک سوال')
async def pack(ctx):
    def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author
        

    packmsg = await ctx.send("سوالات:")
    for i in range(1,6):
      try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        await packmsg.edit(content=packmsg.content+f"\n{msg.content}")
        await msg.delete()
      except asyncio.TimeoutError:
          embed=discord.Embed(title="خطا", description="داااااداش جواب بده تو می خواستی پک پیشنهاد بدی :(", color=0xFF0000)
          await ctx.send(embed=embed)
          return 0
    channel = bot.get_channel(870559120476999690)
    embed = discord.Embed(title=f"پک سوال جدید از {ctx.message.author.name}", description=packmsg.content, color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.reply("پک سوال پیشنهادی شما ارسال شد")
@bot.command()
async def start(ctx):
  def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author
  def check_answer(msg):
    return msg.channel == ctx.channel and msg.author.mention == now_peaple
  question_pack=requests.post(url="https://nimgp.pythonanywhere.com/api/v1/get_pack_by_server/",data={"server":ctx.guild.id})
  if question_pack.status_code == 404:
    requests.post(url="https://nimgp.pythonanywhere.com/api/v1/register_server/",data={"server":ctx.guild.id,"server_name":ctx.guild.name})
    question_pack=requests.post(url="https://nimgp.pythonanywhere.com/api/v1/get_pack_by_server/",data={"server":ctx.guild.id})
  elif question_pack.status_code == 456:
    embed=discord.Embed(title="خطا", description="عزیزان آروممممم آروم :sweat_smile:\nفعلا پکی واسه شما نداریم وایسید پک جدید بیاد :relaxed:", color=0xFF0000)
    await ctx.send(embed=embed)
    return 0
  await ctx.send("بگو ببینم کیا بازی می کنن؟ :thinking: (هرکدوم رو تو یه پیام جدا منشن کن وقتی هم تموم شدن یه پیام بفرست بنویس کافیه)")
  global now_peaple
  peaples=[ctx.message.author.mention]
  pmsg = await ctx.send(f"افرادی که بازی می کنن:\n{peaples[0]}")
  for i in range(1,6):
    try:
      msg = await bot.wait_for("message", check=check, timeout=30)
      if msg.content == "کافیه":
        break
      await pmsg.edit(content=pmsg.content+f"\n{msg.content}")
      peaples.append(msg.content)
      await msg.delete()
    except asyncio.TimeoutError:
        embed=discord.Embed(title="خطا", description="من منتظر جواب توئم :zipper_mouth_face:\nولش کنسل می کنم(برو گمشو بی معرفت :confused: )", color=0xFF0000)
        await ctx.send(embed=embed)
        return 0


  questions=[]
  i=1
  for z in range(1,6):
    questions.append(question_pack.json()['ok'][f"{i}"])
    i+=1
  embed=discord.Embed(title="نام پک:", description=question_pack.json()['ok']["title"], color=0x00ff00)
  await ctx.send(embed=embed)
  i=1
  for q in questions:
    for z in range(1,6):
      embed=discord.Embed(title=f"سوال {i}:", description=question_pack.json()['ok'][f"{i}"], color=0x00ff00)
      await ctx.send(embed=embed)
      if not i == 5:
        i+=1
      for p in peaples:
        now_peaple=p
        await ctx.send(f"{p} پاسخگو باش :hugging:")
        try:
          msg = await bot.wait_for("message", check=check_answer, timeout=30)
          embed = discord.Embed(title="پاسخ آمد!", description=f"جواب {p} اینه :relaxed::\n{msg.content}", color=0x00ff00)
          await ctx.send(embed=embed)
          await msg.delete()
        except asyncio.TimeoutError:
            embed=discord.Embed(title="معرفت گوهر گرانی است به هرکس ندهند...", description="یک عدد بیشعور جواب نداد بریم بعدی :neutral_face:", color=0xFF0000)
            await ctx.send(embed=embed)
    await ctx.send("عه دیگه سوال نیست:sweat_smile:\nبه پایان رسید این دفتر ولی ضایع شدن ها همچنان باقیست... :upside_down_face:")



alive()
bot.run(TOKEN)