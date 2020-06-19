import discord
import asyncio
import datetime
import random as r
import random
import io
import os
import wikipedia
import nekos
import sqlite3
import json
import requests
import time
import sys
import traceback
import youtube_dl
from mod import *
from discord.ext import commands
from discord.utils import get
from yandex_music import Client
from Cybernator import Paginator

class flags(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 60*60*24*2, commands.BucketType.member)
    async def bunting(self,ctx):
        with open('flags.json','r',encoding='utf8') as f:
            flags = json.load(f)
            count = 1
            while count <= 5:
                otvet = random.choice(flags['Флаги'])
                e = discord.Embed(title = f"Флаг {count}")
                e.set_image(url = otvet['url'])
                await ctx.send(embed = e)
                def check(m):
                    return m.content == otvet['answer'] and ctx.channel == ctx.channel

                msg = await bot.wait_for('message', check=check)
                em = discord.Embed(title = "Правильный ответ!")
                em.add_field(name = "Ответил:", value = f"{msg.author.mention}")
                em.add_field(name = "Правильный ответ:",value = f"{otvet['answer']}")
                await ctx.channel.send(embed = em)
                count = count + 1
                await asyncio.sleep(1)
                if count == 5:
                    e = discord.Embed(title = "Конец игры!", description = f"Ивент был проведён {ctx.author.mention}, и мы всем желаем удачи! Спасибо за участие!")
                    await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(flags(bot))
