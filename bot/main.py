import discord
from replit import db
import os
from discord.ext import commands
from live import alive


TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.reply("pong")



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






alive()
bot.run(TOKEN)