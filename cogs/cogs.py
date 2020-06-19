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

class cogs(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def cog(self,ctx):
        await ctx.send(f"Коги успешно работают!")

    @commands.command(aliases=['коронавирус', 'ковид'])
    async def covid(self, ctx, country):
        for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
            if item['country'] == country: 
                embed = discord.Embed(title=f'Статистика Коронавируса | {country}')
                embed.add_field(name='Выздоровело:',          value=f'{item["recovered"]} человек')
                embed.add_field(name='Заболеваний:',          value=f'{item["cases"]} человек')
                embed.add_field(name='Погибло:',              value=f'{item["deaths"]} человек')
                embed.add_field(name='Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
                embed.add_field(name='Погибло за сутки:',     value=f'+{item["todayDeaths"]} человек')
                embed.add_field(name='Проведено тестов:',     value=f'{item["tests"]} человек')
                embed.add_field(name='Активные зараженные:',  value=f'{item["active"]} человек')
                embed.add_field(name='В тяжелом состоянии:',  value=f'{item["critical"]} человек')
                embed.set_thumbnail(url=item["countryInfo"]['flag'])
                embed.set_footer(text="© Copyright 2020 don#4170 | Все права загрызаны")

                return await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready (self):
        print('[Noxus] Cogs successfully uploaded!')
        print('[------------------------------]')
        print(f'          [Other]')

def setup(bot):
    bot.add_cog(cogs(bot))
