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

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

@bot.event
async def on_ready():
    print(f'          [Noxus]')
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game('Здарова братан, я 𝙽𝚘𝚡𝚞𝚜, напиши ".help" и получи список моих команд'))
    print(f"[Noxus] Bot successfully launched!;")
    print(f"[Noxus] Name: [{bot.user}];")
    print(f'[Noxus] ID: [{bot.user.id}]')

def owner(ctx):
    return ctx.message.author.id == 662346548025491476

@bot.command()
@commands.check(owner)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, модуль `{extension}` был успешно загружен!**", color = 0x00ffff))

@bot.command()
@commands.check(owner)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, модуль `{extension}` был успешно выгружен!**", color = 0x00ffff))

@bot.command()
@commands.check(owner)
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}, модуль `{extension}` был успешно перезагружен!**", color = 0x00ffff))

def random_meme():
    with open('memes_data.txt', 'r') as file:
        memes = file.read().split(',')
    picked_meme = random.choice(memes)
    return picked_meme

@bot.command()
async def cat(ctx):
    meow = random.randint(1, 100000)
    embed = discord.Embed(title='**Вот тебе кот:**' ,colour=0x00ffff)
    embed.set_image(url = f'https://cataas.com/cat?{meow}')
    await ctx.send(embed=embed)

@bot.command()
@commands.check(owner)
@commands.cooldown(1, 10, commands.BucketType.user)
async def giveaway( ctx, seconds: int, *, text ):
    def time_end_form( seconds ):
        h = seconds//3600
        m = (seconds - h*3600)//60
        s = seconds%60
        if h < 10:
            h = f"0{h}"
        if m < 10:
            m = f"0{m}"
        if s < 10:
            s = f"0{s}"
        time_reward = f"{h} : {m} : {s}"
        return time_reward

    author = ctx.message.author
    time_end = time_end_form(seconds)
    await ctx.message.delete()
    message = await ctx.send(embed = discord.Embed(
        description = f"**Разыгрывается : `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
        colour = 0x75218f).set_footer(
        text = 'Parazzit#1283 © | Все права защищены',
        icon_url = ctx.message.author.avatar_url))
    await message.add_reaction("🎉")
    while seconds > -1:
        time_end = time_end_form(seconds)
        text_message = discord.Embed(
            description = f"**Разыгрывается: `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
            colour = 0x75218f).set_footer(
            text = 'Parazzit#1283 © | Все права защищены',
            icon_url = ctx.message.author.avatar_url)
        await message.edit(embed = text_message)
        await asyncio.sleep(1)
        seconds -= 1
        if seconds < -1:
            break
    channel = message.channel
    message_id = message.id
    message = await channel.fetch_message(message_id)
    reaction = message.reactions[ 0 ]

    users = await reaction.users().flatten()

    def winners():
        global win

        user_win = random.choice(users)

        if reaction.count == 1:
            win = discord.Embed(
                description = f'**В этом розыгрыше нет победителя!**',
                colour = 0x75218f).set_footer(
                text = 'Parazzit#1283 © | Все права защищены',
                icon_url = ctx.message.author.avatar_url)
        elif str(user_win.id) == str(bot.user.id):
            winners()
        else:
            win = discord.Embed(
                description = f'**Победитель розыгрыша: {user_win.mention}!\nНапишите организатору {author.mention}, чтобы получить награду.**',
                colour = 0x75218f).set_footer(
                text = 'Parazzit#1283 © | Все права защищены',
                icon_url = ctx.message.author.avatar_url)

    winners()
    global win
    await message.edit(embed = win)
    await author.send(embed = discord.Embed(description = f'**Ваш розыгрыш закончился.**',
                                            colour = 0x75218f).set_footer(
        text = 'Parazzit#1283 © | Все права защищены',
        icon_url = ctx.message.author.avatar_url))

@bot.command()
async def neko(ctx):
    number = random.randint(1,3)
    if (number == 1): 
        embed = discord.Embed(description = f"{ctx.author.mention} вот тебе аниме гирл:", colour = 0xff0000)
        embed.set_image(url=nekos.img('neko'))
    if (number == 2):
        embed = discord.Embed(description = f"{ctx.author.mention} Вот тебе лисичка:", colour = 0xff0000)
        embed.set_image(url=nekos.img('fox_girl'))
    if (number == 3):
        embed = discord.Embed(description = f"{ctx.author.mention} Вот тебе класик:", colour = 0xff0000)
        embed.set_image(url=nekos.img('avatar'))
    await ctx.send(embed = embed)

@bot.command()
async def meme(ctx):
    emb = discord.Embed(description = f"**Вот тебе мем:**", color = 0xda4a)
    emb.set_image(url= random_meme())
    await ctx.send(embed=emb)

@bot.command()
@commands.has_permissions( administrator = True)
async def clear(ctx, amount:int=None):
    if amount == None:
        return await ctx.send(embed = discord.Embed(description = f'**Укажите количество сообщений для удаления**', color=0x75218f))
    embed = discord.Embed(description=f'**Было удалено {amount} сообщений**', color=0x75218f)
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=embed, delete_after=6.0)

@bot.command(aliases=['bot'])
async def botinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Информация о боте **𝙽𝚘𝚡𝚞𝚜#6265**.\n Бот был написан специально для проекта **`𝙽𝚘𝚡𝚞𝚜`**,\n Подробнее о командах: **`.help`**", color = 0x00ffff)
    embed.add_field(name=f'**Меня создал:**', value="`Parazzit#1283`(<@662346548025491476>)", inline=False)  # Создает строку
    embed.add_field(name=f'**Помощь в создании:**', value="`*нету*`(/*нету/*)", inline=False)  # Создает строку
    embed.add_field(name=f'**Лицензия:**', value="LD-v7", inline=False)  # Создает строку
    embed.add_field(name=f'**Я написан на:**', value="Discord.py", inline=False)  # Создает строку
    embed.add_field(name=f'**Версия:**', value="V.3.2.4", inline=False)  # Создает строку
    embed.add_field(name=f'**Патч:**', value="46", inline=False)  # Создает строку
    embed.set_thumbnail( url = bot.user.avatar_url)
    embed.set_footer(text=f"Parazzit#1283 © | Все права защищены", icon_url="https://cdn.discordapp.com/avatars/662346548025491476/c23dc4b634f03c950d8202e194a635b1.png?size=512")
    await ctx.send(embed=embed)

@bot.command()
@commands.check(owner)
async def emoji(ctx,id:int,reaction:str):
		await ctx.message.delete()
		message = await ctx.message.channel.fetch_message(id)
		await message.add_reaction(reaction)

@bot.command() # Декоратор команды
async def ran_avatar(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.', color=0x6fdb9e) # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда

@bot.command() # Декоратор команды
async def slap(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('<a:No:719995078059229336> Вы не можете ударить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас ударил(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def goose(ctx): # Название команды и аргумент
        emb = discord.Embed(description= f'**Вот твой гусь:**', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('goose')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def dog(ctx): # Название команды и аргумент
        emb = discord.Embed(description= f'**Вот твоя собака:**', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('woof')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def hug(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('<a:No:719995078059229336> Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас обнял(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command()
async def kill(ctx, member : discord.Member = None):
	if member == None:
		emb = discord.Embed(description= f'{ctx.message.author.mention} Прыгает с крыши.', color=0x6fdb9e) # Переменная ембеда и описание
		emb.set_image(url='https://pa1.narvii.com/7081/7f5f49cf4e6c0a06614d7cda9bd5954b257a2151r1-500-296_hq.gif')
		
		await ctx.send(embed=emb)
	else:
		emb = discord.Embed(description= f'{member.mention}, Вас убил(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
		emb.set_image(url='https://cdn.discordapp.com/attachments/693515715646324796/707582757144100894/tenor.gif') # Ищем картинку и ставим её в ембед
 	
		await ctx.send(embed=emb) # Отпрвака ембед

@bot.command()
async def password(ctx, lenght: int = None, number: int = None):

    if not lenght or not number:
        await ctx.send(embed = discord.Embed(description = f'<a:No:719995078059229336> Пожалуйста, укажите длину пароля и количество символов в нем.', color=0x0c0c0c)) 

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for x in range(number):
        password = ''

        for i in range( lenght ):
            password += random.choice(chars)

        await ctx.author.send(embed = discord.Embed(description = f'**Сгенерированный пароль:\n{password}**', color=0x0c0c0c)) 
        await ctx.send(embed = discord.Embed(description = f'**Пароль успешно отправлен!**', color=0x0c0c0c))
        return

@bot.command()
async def help(ctx):
    embed1 = discord.Embed(title = '⚙ Навигация по командам:\n ❗ Обязательные параметры: `()`\n ❓ Необязательные параметры: `[]`', color=0x6fdb9e )
    embed2 = discord.Embed(title ='💎 Базовые:', description='**``.user [@user]`` - Узнать информацию о пользователе 🎭\n ``.server`` - Узнать информацию о сервере 🧿\n `.bot` - Информация о боте 🤖\n`.avatar [@user]` - Аватар пользователя 🖼\n `.suggest (text)` - Предложить идею ✉\n `.wiki (text)` - Википедия 📖\n `.blacklist` - Узнать сервера в чёрном списке 🎱\n `.covid (country)` - Информация о вирусе Covid-19 🦠**', color=0x6fdb9e )
    embed3 = discord.Embed(title ='✨ Роблокс:', description='**`.music` - Коды для музыки 💨**', color = 0x6fdb9e)
    embed4 = discord.Embed(title ='🎉 Весёлости:', description='**``.ran_color`` - Рандомный цвет в формате HEX 🩸\n ``.coin`` - Бросить монетку 🌈\n ``.math (2*2/2+2-2)`` - Решить пример :infinity:\n `.8ball (question)` - Волшебный шар 🔮\n `.password (10 10)` - Рандомный пароль 🎩\n `.meme` - Рандомный мем 🤣\n `.sapper` - Типичный сапёр ♻\n `.ttt (user)` - Крестики-нолики ⭕\n `.bunting` - Угадай флаг 🏴**', color=0x6fdb9e)
    embed5 = discord.Embed(title ='💋 Некос:', description='**`.hug (@user)` - Обнять 😜\n `.slap (@user)` - Ударить 😡\n `.ran_avatar` - Рандом. аватар 🤯\n `.kill [@user]` - Убить 🔪\n `.dog` - Собака :dog:\n `.goose` - Гусь :duck:\n `.cat` - Кот 🐱\n `.neko` - Рандомная аватарка в стиле аниме ✨**', color=0x6fdb9e)
    embeds = [embed1, embed2, embed3, embed4, embed5]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds, reactions = ['<a:Left:720717981499261008>', '<a:Right:720717967343485020>'])
    await page.start()

@bot.command()
async def music(ctx):
    embed1 = discord.Embed(title ='📋 Страницы:', description='**`1.` - Страница 1 (1-6)\n `2.` - Страница 2 (7-12)\n `3.` - Страница 3 (13-19)\n `4.` - Страница 4 (20-23)**', color = 0x6fdb9e)
    embed2 = discord.Embed(title ='⚠ Патент:', description='**`❗❗❗` Кто сп#здит коды, тому п#зда!**', color = 0x6fdb9e)
    embed3 = discord.Embed(title ='📋 Страница 1', description='**`1.` РА-ТА-ТА-ТА-ТА - `4618705402`\n `2.` Копы - `2933225417`\n `3.` Последняя - `4624707819`\n `4.` Чикибамбони - `4570427470`\n `5.` 4 Украинки - `4624707819`\n `6.` Пам пам пам - `2717372934`**', color = 0x6fdb9e)
    embed4 = discord.Embed(title ='📋 Страница 2', description='**`7.` Грустный реп - `4518984639`\n `8.` Реальный Flesh - `3766039768`\n `9.` Ракета - `3666410231`\n `10.` Убьют за нас - `3134163814`\n `11.` Хубба Бубба - `4502015210`\n `12.` Надо Поле Притоптать - `1170717899`**', color = 0x6fdb9e)
    embed5 = discord.Embed(title ='📋 Страница 3', description='**`13.` Паравозик тыр, тыр, тыр - `4244590201`\n `14.` Нейтороксин - `4466370680`\n `15.` Корабль идёт ко дну - `2774380819`\n `16.` Идол - `2941601894`\n `17.` Коронаминус - `4788523402`\n `18.` Попытка номер 5 - `4722362895`\n `19.` Супер друг - `4338357412`**', color = 0x6fdb9e)
    embed6 = discord.Embed(title ='📋 Страница 4', description='**`20.` ПчелоБав Урод- `5035741007`\n `21.` Файнана - `4795882785`\n `22.` Зеленоглазые- `2714953923`\n `23.` Кто тебе сказал- `4942748329`**', color = 0x6fdb9e)
    embeds = [embed1, embed2, embed3, embed4, embed5, embed6]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message,  only=ctx.author, use_more=False, embeds=embeds, reactions = ['<a:Left:720717981499261008>', '<a:Right:720717967343485020>'])
    await page.start()

@bot.command()
async def wiki(ctx, *, text):
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(text)
    summ = wikipedia.summary(text)
    emb = discord.Embed(
        title= new_page.title,
        description= summ,
        color = 0x00ffff
    )
    emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

    await ctx.send(embed=emb)

@bot.command()
async def blacklist(ctx):
  emb = discord.Embed(title ='📋 Чёрный список:', color = 0x6fdb9e)
  emb.add_field(name=f'**🔑 Сервера:**', value="**Пусто...**", inline=False)
  emb.add_field(name=f'**✨ Участники:**', value="**`Inv4l1d#0666` - Украл аккаунт [ Печать неснимаемости ]**", inline=False)
  emb.add_field(name=f'**🎩 Как снять чс:**', value="**Напишите в лс <@719605055547768894> и ждите ответа!**", inline=False)
  emb.set_image(url='https://cdn.discordapp.com/attachments/705488180710998127/717125585918492692/D7KfkHIWkAA9m8j.jpg')

  await ctx.send(embed=emb)

@bot.command()
async def user(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"**🧬 Имя: `{Member.name}`**\n\n"
                                                                                      f"**⚔ Никнейм: `{Member.nick}`**\n\n"
                                                                                      f"**🌵 Статус: `{Member.status}`**\n\n"
                                                                                      f"**🔑 ID: `{Member.id}`**\n\n"
                                                                                      f"**🌋 Высшая роль: `{Member.top_role}`**\n\n"
                                                                                      f"**🌟 Аккаунт создан: `{Member.created_at.strftime('%A %b %#d, %Y')}`**", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f'** Аватар `{user}`**', color= 0x0c0c0c)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

@bot.command()
async def ran_color(ctx):
    clr = (random.randint(0,16777215))
    emb = discord.Embed(
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``',
        colour= clr
    )

    await ctx.send(embed=emb)

@bot.command(name = "8ball")
async def ball(ctx, *, arg):

    message = ['Нет 😑','Да 😎','Возможно 😪','Опредленно нет '] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0x0c0c0c))
    return

# Работа с ошибками шара

@ball.error 
async def ball_error(ctx, error):

    if isinstance( error, commands.MissingRequiredArgument ): 
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите вопрос.', color=0x0c0c0c)) 

@bot.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx, *, args = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Пожалуйста, укажите выражение для оценки.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Результат примера: `{args}`: \n`{result}`', color = 0x39d0d6))

@bot.command()
async def server(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"Сервер: `{ctx.guild.name}`", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f"<a:Time:719996484237656215> **Сервер создали: `{ctx.guild.created_at.strftime('%A, %b %#d %Y')}`**\n\n"
        f"<:Region:719996506857406525> **Регион: `{ctx.guild.region}`**\n\n"
        f"<:Owner:720001653163425822> **Глава сервера: `{ctx.guild.owner}`**\n\n"
        f"<:Bot:719996225453162618> **Ботов на сервере: `{len([m for m in members if m.bot])}`**\n\n"
        f"<:Online:719996334546878494> **Онлайн: `{online}`**\n\n"
        f"<:Offline:719996377865912342> **Оффлайн: `{offline}`**\n\n"
        f"<:Idle:719996278196666439> **Отошли: `{idle}`**\n\n"
        f"<:Dnd:719996257330004019> **Не трогать: `{dnd}`**\n\n"
        f"<:Shield:719996523823366195> **Уровень верификации: `{ctx.guild.verification_level}`**\n\n"
        f"<:Channels:719996243228753921> **Всего каналов: `{allchannels}`**\n\n"
        f"<:VoiceChannel:719996462305509386> **Голосовых каналов: `{allvoice}`**\n\n"
        f"<:TextChannel:719996437676425358> **Текстовых каналов: `{alltext}`**\n\n"
        f"<a:Roles:719996398044708945> **Всего ролей: `{allroles}`**\n\n"
        f"<:Members:719996296827764786> **Людей на сервере: `{ctx.guild.member_count}`**\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Информация о сервере: {ctx.guild.name}")
    await ctx.send(embed=embed)

@bot.command()
@commands.check(owner)
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0xda4a))

@bot.command()
@commands.check(owner)
async def sleave(ctx, server_id: int):
    to_leave = bot.get_guild(server_id)

    await ctx.send(embed = discord.Embed(description = f'**Я успешно прекратил обслуживание данного сервера.**', color=0x0c0c0c))
    await to_leave.leave()

@bot.command()
@commands.check(owner)
async def servers(ctx):
    description = ' '
    counter = 0
    for guild in bot.guilds:
        counter += 1
        description += f'{counter}) **`{guild.name}`** - **`{len(guild.members)}`** участников. ID: **`{guild.id}`** \n'
        await ctx.send(embed = discord.Embed(title = 'Сервера, на которых я нахожусь', description = description, color = 0x00ffff))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

token = os.environ.get("BotToken")
bot.run(str(token))
