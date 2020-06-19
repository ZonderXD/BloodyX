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

class news(commands.Cog):

    def init(self, bot):
        self.bot = bot

    @commands.group(description = 'Создать пост от имени бота', hidden = True)
    @commands.check(owner)
    async def post(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send('`Для того чтобы отправить пост выберете категорию:\n 1. --- DM (личные сообщения)\n 2. --- Clear (Очистит личку с ботом у всех пользователей(только сообщения от бота))`')
        else:
            pass

    @post.command(description = 'Отправит пост с вашим текстом всем участникам серверов на котороых есть ваш бот.')
    async def DM(self, ctx):
        await ctx.message.delete()
        def check(m):
            return m.author.id == ctx.author.id
        await ctx.send('**Вы создали пост, пожалуйста, следуйте ниже указанным пунктам:\nВведите заголовок: \n(У вас есть 60 секунд)**')
        try:
            p = await self.bot.wait_for('message', check = check, timeout = 60.0)
            p = p.content 
        except TimeoutError:
            await ctx.send(embed = discord.Embed(title = '**Ошибка**',description ='`Вы не ввели заглавие за указанное время.`', color = discord.Color.red()))
        else:
            try:
                await ctx.send('**Введите текст поста (У вас есть 60 секунд)**')
                text = await self.bot.wait_for('message', check = check, timeout = 60.0)
                text = text.content
            except TimeoutError:
                await ctx.send(embed = discord.Embed(title = '**Ошибка**',description ='`Вы не ввели текст за указанное время.`', color = discord.Color.red()))
            else:
                Emb = discord.Embed(title = p, description = text, color = discord.Color.blurple())
                Emb.set_author(name = ctx.author.name, icon_url= ctx.author.avatar_url)
                Emb.set_footer(text = f'© Система оповещений {self.bot.user}', icon_url= self.bot.user.avatar_url)

                for guild in self.bot.guilds:
                    for member in guild.members:
                        try:
                            if member == ctx.author or member.bot:
                                pass
                            else: await member.send(embed = Emb)
                        except Exception as e:
                            print(e)
                cEmb = discord.Embed(title = 'Успешно `✔️`', description = '**Пост отправлен.**', color = discord.Color.blurple())
                cEmb.add_field(name = p, value = text, inline = False)
                cEmb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                cEmb.set_footer(text = f'© Система оповещений {self.bot.user}', icon_url= self.bot.user.avatar_url)
                await ctx.send(embed = cEmb)

    @post.command(description = 'Очистит все сообщения бота в личках')
    async def clear(self, ctx):
        await ctx.message.delete()
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.bot:
                    pass
                else:
                    channel = member.dm_channel
                    if channel is None:
                        channel = await member.create_dm()
                    else:
                        try:
                            async for message in channel.history(limit=200):
                                if message.author == self.bot.user:
                                    await message.delete()
                        except StopAsyncIteration:
                            pass
        await ctx.send('Успешно `✔️`')

def setup(bot):
    bot.add_cog(news(bot))
