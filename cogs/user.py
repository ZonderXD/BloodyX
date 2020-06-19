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

class user(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def cog(self,ctx):
        await ctx.send(f"{self.user.mention} коги успешно работают!")

    @commands.Cog.listener()
    async def on_ready (self):
        print("Cogs successfully launched!")

def setup(bot):
    bot.add_cog(user(bot))
