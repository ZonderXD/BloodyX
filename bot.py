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
from mod import *
from discord.ext import commands
from discord.utils import get
from Cybernator import Paginator

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

@bot.event
async def on_ready():
    print(f'          [Woof X]')
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game('⊱ Prefix: . ⊰'))
    print(f"[Woof X] Bot successfully launched!;")
    print(f"[Woof X] Name: [{bot.user}];")
    print(f'[Woof X] ID: [{bot.user.id}]')
    print('[------------------------------]')
    print(f'          [Other]')

@bot.event
async def is_owner(ctx):
    return ctx.author.id == 716724192065749075 or  ctx.author.id == 491928659599425537# Айди создателя бота

@bot.command()
@commands.check(is_owner)
async def opros(ctx, *, arg):
	await ctx.message.delete()
	embed = discord.Embed(title=f"Опрос:", color = 0x00ffff)
	embed.add_field(name=f'**Вопрос:**', value=f"**{arg}**\n", inline=False)  # Создает строку
	embed.add_field(name=f'**Решение:**', value="**-=-=- Да - ❤ -=-=-\n -=-=- Нет - 💔 -=-=-**\n\n", inline=False)  # Создает строку
	embed.add_field(name=f'**Инфо:**', value="**Голосование будет длиться 1 минуту!**", inline=False)  # Создает строку
	await ctx.send(embed=embed)

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
@commands.check(is_owner)
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
        text = '𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691 © | Все права защищены',
        icon_url = ctx.message.author.avatar_url))
    await message.add_reaction("🎉")
    while seconds > -1:
        time_end = time_end_form(seconds)
        text_message = discord.Embed(
            description = f"**Разыгрывается: `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
            colour = 0x75218f).set_footer(
            text = '𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691 © | Все права защищены',
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
                text = '𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691 © | Все права защищены',
                icon_url = ctx.message.author.avatar_url)
        elif str(user_win.id) == str(bot.user.id):
            winners()
        else:
            win = discord.Embed(
                description = f'**Победитель розыгрыша: {user_win.mention}!\nНапишите организатору {author.mention}, чтобы получить награду.**',
                colour = 0x75218f).set_footer(
                text = '𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691 © | Все права защищены',
                icon_url = ctx.message.author.avatar_url)

    winners()
    global win
    await message.edit(embed = win)
    await author.send(embed = discord.Embed(description = f'**Ваш розыгрыш закончился.**',
                                            colour = 0x75218f).set_footer(
        text = '𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691 © | Все права защищены',
        icon_url = ctx.message.author.avatar_url))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 714560313697239044: # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '✅': # Emoji для реакций
            role = guild.get_role(713846336595689552) # ID Ролей для выдачи

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 714560313697239044: # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '✅': # Emoji для реакций
            role = guild.get_role(713846336595689552) # ID Ролей для выдачи

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)

@bot.command( pass_context = True, aliases = [ "Предложить", "предложить", "предложка", "Предложка", "Suggest" ])
async def suggest( ctx , * , agr ):
    if ctx.author.id == 662346548025491476:
        await ctx.send(embed = discord.Embed(description = f"**Извините, но Вы не можете использовать данную команду так как создатель бота запретил Вам доступ к этой команде!**"))
    else:
        await ctx.message.add_reaction('✅')
        suggest_chanell = bot.get_channel( 703655454563237969 ) #Айди канала предложки
        embed = discord.Embed(title=f"{ctx.author.name} Предложил :", description= f" {agr} \n\n")

        embed.set_thumbnail(url=ctx.guild.icon_url)

        message = await suggest_chanell.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❎')

@bot.event
async def on_message(msg):
    await bot.process_commands( msg )
    if msg.author.bot or msg.author.id == 668325441224048641 or msg.author.id == 342317507991961602 or msg.author.id == 491928659599425537:
        pass
    else:
        mes = msg.content.lower()
        author = msg.author
        mat = open('mat.txt', 'r', encoding='utf-8')
        for line in mat:
            if mes.find(line[0:-1]) != -1:
                if msg.author.bot:
                    pass
                else:
                    await msg.delete()
                    await msg.channel.send(embed = discord.Embed(description= f"**{author.mention}, Вы написали сообщение в котором есть запрещённое слово!**", color = 0x75218f))
                    print(f"⊱ {author.name}, произнёс слово [{msg.content}] ⊰")
    
        mat.close()

@bot.event
async def on_voice_state_update(member,before,after):
    if after.channel != None and after.channel.id == 712629884119416944:
        for guild in bot.guilds:
            if guild.id == 696322642747064380:
                mainCategory = discord.utils.get(guild.categories, id=712629625049579561)
                channel2 = await guild.create_voice_channel(name=f"🌄╎{member.display_name}",category=mainCategory, user_limit=1)
                await member.move_to(channel2)
                def check(a,b,c):
                    return len(channel2.members) == 0
                await bot.wait_for('voice_state_update', check=check)
                await channel2.delete()

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

@bot.event
async def on_member_join( member ):
    emb = discord.Embed( description = f"**Приветствую тебя {member.mention}. Ты попал на сервер `{member.guild.name}`. Удачи тебе на сервере! 😜**", color = 0xda4a )
    role = discord.utils.get( member.guild.roles, id = 696322642747064383 ) # Айди роли которая будет выдаватся когда человек зашёл на сервер

    await member.add_roles( role )
    channel = bot.get_channel( 696322644106281032 ) # Айди канала куда будет писатся сообщение
    await channel.send( embed = emb )

@bot.command(aliases=['bot'])
async def botinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Информация о боте **𝐖𝐨𝐨𝐟 𝐗#7002**.\n Бот был написан специально для проекта **`Woof X`**,\n Подробнее о командах: **`.help`**", color = 0x00ffff)
    embed.add_field(name=f'**Меня создал:**', value="`𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691`(<@716724192065749075>)", inline=False)  # Создает строку
    embed.add_field(name=f'**Помощь в создании:**', value="`Satana★#2362`(<@342317507991961602>)", inline=False)  # Создает строку
    embed.add_field(name=f'**Лицензия:**', value="LD-v7", inline=False)  # Создает строку
    embed.add_field(name=f'**Я написан на:**', value="Discord.py", inline=False)  # Создает строку
    embed.add_field(name=f'**Версия:**', value="V.3.0.1", inline=False)  # Создает строку
    embed.add_field(name=f'**Патч:**', value="10", inline=False)  # Создает строку
    embed.set_thumbnail( url = bot.user.avatar_url)
    embed.set_footer(text=f"𝘾𝙮𝙗𝙚𝙧𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮ツ#9691 © | Все права защищены", icon_url='https://cdn.discordapp.com/avatars/716724192065749075/b498ce487d437b64029fa2cfedea24e3.webp?size=1024') # создаение футера
    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_owner)
async def edit(ctx, message_id: int = None, new_content: str = None):
        message = await ctx.message.channel.fetch_message(message_id)
        
        await message.edit(content = new_content)
        await ctx.message.add_reaction('✅')

@bot.command()
@commands.check(is_owner)
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
        await ctx.send('Вы не можете ударить сами себя.')
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
        await ctx.send('Вы не можете обнять сами себя.')
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
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите длину пароля и количество символов в нем.', color=0x0c0c0c)) 

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
    embed2 = discord.Embed(title ='💎 Базовые:', description='**``.user [@user]`` - Узнать информацию о пользователе 🎭\n ``.server`` - Узнать информацию о сервере 🧿\n `.bot` - Информация о боте 🤖\n`.avatar [@user]` - Аватар пользователя 🖼\n `.suggest (text)` - Предложить идею ✉\n `.wiki (text)` - Википедия 📖**', color=0x6fdb9e )
    embed3 = discord.Embed(title ='✨ Роблокс:', description='**`.music` - Коды для музыки 💨\n `.scripts` - Скрипты для читерства 🧨\n `.script (number)` - Получить сам скрипт 💡**', color = 0x6fdb9e)
    embed4 = discord.Embed(title ='🎉 Весёлости:', description='**``.ran_color`` - Рандомный цвет в формате HEX 🩸\n ``.coin`` - Бросить монетку 🌈\n ``.math (2*2/2+2-2)`` - Решить пример :infinity:\n `.8ball (question)` - Волшебный шар 🔮\n `.password (10 10)` - Рандомный пароль 🎩\n `.meme` - Рандомный мем 🤣**', color=0x6fdb9e)
    embed5 = discord.Embed(title ='💋 Некос:', description='**`.hug (@user)` - Обнять 😜\n `.slap (@user)` - Ударить 😡\n `.ran_avatar` - Рандом. аватар 🤯\n `.kill [@user]` - Убить 🔪\n `.dog` - Собака :dog:\n `.goose` - Гусь :duck:\n `.cat` - Кот 🐱\n `.neko` - Рандомная аватарка в стиле аниме ✨**', color=0x6fdb9e)
    embeds = [embed1, embed2, embed3, embed4, embed5]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds, reactions=['<a:woof_x_left:713825760099565698>', '<a:woof_x_right:713825800440512694>'])
    await page.start()

@bot.command()
async def music(ctx):
    embed1 = discord.Embed(title ='📋 Страницы:', description='**`1.` - Страница 1 (1-6)\n `2.` - Страница 2 (7-12)\n `3.` - Страница 3 (13-19)**', color = 0x6fdb9e)
    embed2 = discord.Embed(title ='⚠ Патент:', description='**`❗❗❗` Кто сп#здит коды, тому п#зда! <@342317507991961602> не касается! `❗❗❗`**', color = 0x6fdb9e)
    embed3 = discord.Embed(title ='📋 Страница 1', description='**`1.` РА-ТА-ТА-ТА-ТА - `4618705402`\n `2.` Копы - `2933225417`\n `3.` Последняя - `4624707819`\n `4.` Чикибамбони - `4570427470`\n `5.` 4 Украинки - `4624707819`\n `6.` Пам пам пам - `2717372934`**', color = 0x6fdb9e)
    embed4 = discord.Embed(title ='📋 Страница 2', description='**`7.` Грустный реп - `4518984639`\n `8.` Реальный Flesh - `3766039768`\n `9.` Ракета - `3666410231`\n `10.` Убьют за нас - `3134163814`\n `11.` Хубба Бубба - `4502015210`\n `12.` Надо Поле Притоптать - `1170717899`**', color = 0x6fdb9e)
    embed5 = discord.Embed(title ='📋 Страница 3', description='**`13.` Паравозик тыр, тыр, тыр - `4244590201`\n `14.` Нейтороксин - `4466370680`\n `15.` Корабль идёт ко дну - `2774380819`\n `16.` Идол - `2941601894`\n `17.` Коронаминус - `4788523402`\n `18.` Попытка номер 5 - `4722362895`\n `19.` Супер друг - `4338357412`**', color = 0x6fdb9e)
    embeds = [embed1, embed2, embed3, embed4, embed5]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message,  only=ctx.author, use_more=False, embeds=embeds, reactions=['<a:woof_x_left:713825760099565698>', '<a:woof_x_right:713825800440512694>'])
    await page.start()

@bot.command()
async def scripts(ctx):
    embed1 = discord.Embed(title ='📋 Страницы:', description='**`1.` - Страница 1 (1-12)\n `2.` - Страница 2 (13-24)\n `3.` - Страница 3 (25-37)\n\n F.A.Q.\n ```Если вам выдадут бан в роблоксе, мы не будем причастны к этому так как мы просто даём скрипты!```**', color = 0x6fdb9e)
    embed2 = discord.Embed(title ='⚠ Патент:', description='**`❗❗❗` Кто сп#здит скрипты, тому п#зда! <@342317507991961602> не касается! `❗❗❗`**', color = 0x6fdb9e)
    embed3 = discord.Embed(title ='📋 Страница 1', description='**`1` - Break In\n `2` - Pet Ranch 2 Simulator\n `3` - Arsenal\n `4` - Build a Boat\n `5` - Fishing Simulator\n `6` - Flood Escape 2\n `7` - Bee Swarm Simulator\n `8` - Pizza Factory Tycoon\n `9` - Work At A Pizza Place\n `10` - Texting Simulator\n `11` - CB:RO\n `12` - Mad City**', color = 0x6fdb9e)
    embed4 = discord.Embed(title ='📋 Страница 2', description='**`13` - Ghost Simulator\n `14` - Speed Run 4\n `15` - Ro-Ghoul\n `16` - RoCitizens\n `17` - Muscle Legends\n `18` - Bubble Gum Simulator\n `19` - BIG Paintball\n `20` - MeepCity\n `21` - Mineverse\n `22` - Soda Simulator\n `23` - Destruction Simulator\n `24` - Horrific Housing**', color = 0x6fdb9e)
    embed5 = discord.Embed(title ='📋 Страница 3', description='**`25` - Shark Bite\n `26` - Piggy\n `27` - Lucky blocks\n `28` - A Wolf Or Other\n `29` - Jailbreak\n `30` - Robot Inc\n `31` - Pizza Factory Tycoon\n `32` - Work at a Pizza Place\n `33` - Tower of Hell\n `34` - A Bizarre Day\n `35` - Bakon\n `36` - Zombie Attack\n `37` -  Knife Ability Test (KAT)**', color = 0x6fdb9e)
    embeds = [embed1, embed2, embed3, embed4, embed5]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds, reactions=['<a:woof_x_left:713825760099565698>', '<a:woof_x_right:713825800440512694>'])
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
async def script(ctx, *, arg: int = None):
  if arg == None:
    await ctx.send(embed = discord.Embed(description = f'**Укажите номер скрипта.**', color=0x6fdb9e))
  elif arg == 1:
    await ctx.send(file=discord.File(fp = 'Scripts/Break_in_GUI.txt'))
  elif arg == 2:
    await ctx.send(file=discord.File(fp = 'Scripts/Pet_Racnh_2_script.txt'))
  elif arg == 3:
    await ctx.send(file=discord.File(fp = 'Scripts/Arsenal_Op_GUI.txt'))
  elif arg == 4:
    await ctx.send(file=discord.File(fp = 'Scripts/build_a_bot_for_treasure_gui.txt'))
  elif arg == 5:
    await ctx.send(file=discord.File(fp = 'Scripts/Fishing.txt'))
  elif arg == 6:
    await ctx.send(file=discord.File(fp = 'Scripts/Flood Escape 2.txt'))
  elif arg == 7:
    await ctx.send(file=discord.File(fp = 'Scripts/Bee Swarm Simulator.txt'))
  elif arg == 8:
    await ctx.send(file=discord.File(fp = 'Scripts/Pizza_Factory_Tycoon.txt'))
  elif arg == 9:
    await ctx.send(file=discord.File(fp = 'Scripts/Work_At_A_Pizza_Place.txt'))
  elif arg == 10:
    await ctx.send(file=discord.File(fp = 'Scripts/Texting_Simulator.txt'))
  elif arg == 11:
    await ctx.send(file=discord.File(fp = 'Scripts/CB:RO.txt'))
  elif arg == 12:
    await ctx.send(file=discord.File(fp = 'Scripts/MAD_LADS.txt'))
    await ctx.send(file=discord.File(fp = 'Scripts/Auto_Rob.txt'))
  elif arg == 13:
    await ctx.send(file=discord.File(fp = 'Scripts/Ghost Simulator.txt'))
  elif arg == 14:
    await ctx.send(file=discord.File(fp = 'Scripts/Speed_Run_4.txt'))
  elif arg == 15:
    await ctx.send(file=discord.File(fp = 'Scripts/Ro-Ghoul.txt'))
  elif arg == 16:
    await ctx.send(file=discord.File(fp = 'Scripts/RoCitizens.txt'))
  elif arg == 17:
    await ctx.send(file=discord.File(fp = 'Scripts/Muscle_Legends.txt'))
  elif arg == 18:
    await ctx.send(file=discord.File(fp = 'Scripts/Bubble Gum Simulator.txt'))
  elif arg == 19:
    await ctx.send(file=discord.File(fp = 'Scripts/BIG Paintball.txt'))
  elif arg == 20:
    await ctx.send(file=discord.File(fp = 'Scripts/MeepCity.txt'))
  elif arg == 21:
    await ctx.send(file=discord.File(fp = 'Scripts/Mineverse.txt'))
  elif arg == 22:
    await ctx.send(file=discord.File(fp = 'Scripts/Soda_Simulator.txt'))
  elif arg == 23:
    await ctx.send(file=discord.File(fp = 'Scripts/Destruction_Simulator.txt'))
  elif arg == 24:
    await ctx.send(file=discord.File(fp = 'Scripts/Horrific Housing.txt'))
    await ctx.send(file=discord.File(fp = 'Scripts/Horrific Housing 2.txt'))
  elif arg == 25:
    await ctx.send(file=discord.File(fp = 'Scripts/Shark Bite.txt'))
  elif arg == 26:
    await ctx.send(file=discord.File(fp = 'Scripts/Piggy Give Item.txt'))
  elif arg == 27:
    await ctx.send(file=discord.File(fp = 'Scripts/Lucky Block.txt'))
  elif arg == 28:
    await ctx.send(file=discord.File(fp = 'Scripts/A Wolf Of Others.txt'))
  elif arg == 29:
    await ctx.send(file=discord.File(fp = 'Scripts/AutoRobJail.txt'))
  elif arg == 30:
    await ctx.send(file=discord.File(fp = 'Scripts/Robot Inc.txt'))
  elif arg == 31:
    await ctx.send(file=discord.File(fp = 'Scripts/Pizza_Factory_Tycoon.txt'))
  elif arg == 32:
    await ctx.send(file=discord.File(fp = 'Scripts/Work_At_A_Pizza_Place.txt'))
  elif arg == 33:
    await ctx.send(file=discord.File(fp = 'Scripts/Tower_of_Hell.txt'))
  elif arg == 34:
    await ctx.send(file=discord.File(fp = 'Scripts/A Bizarre Day MODDED MINI GUI.txt'))
  elif arg == 35:
    await ctx.send(file=discord.File(fp = 'Scripts/Bakon GUI.txt'))
  elif arg == 36:
    await ctx.send(file=discord.File(fp = 'Scripts/Zombie Attack.txt'))
  elif arg == 37:
    await ctx.send(file=discord.File(fp = 'Scripts/KAT_Press_2.txt'))

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
        f":timer: **Сервер создали: `{ctx.guild.created_at.strftime('%A, %b %#d %Y')}`**\n\n"
        f":flag_white: **Регион: `{ctx.guild.region}`**\n\n"
        f":cowboy:  **Глава сервера: `{ctx.guild.owner}`**\n\n"
        f":tools: **Ботов на сервере: `{len([m for m in members if m.bot])}`**\n\n"
        f":green_circle: **Онлайн: `{online}`**\n\n"
        f":black_circle: **Оффлайн: `{offline}`**\n\n"
        f":yellow_circle: **Отошли: `{idle}`**\n\n"
        f":red_circle: **Не трогать: `{dnd}`**\n\n"
        f":shield: **Уровень верификации: `{ctx.guild.verification_level}`**\n\n"
        f":musical_keyboard: **Всего каналов: `{allchannels}`**\n\n"
        f":loud_sound: **Голосовых каналов: `{allvoice}`**\n\n"
        f":keyboard: **Текстовых каналов: `{alltext}`**\n\n"
        f":briefcase: **Всего ролей: `{allroles}`**\n\n"
        f":slight_smile: **Людей на сервере: `{ctx.guild.member_count}`**\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Информация о сервере: {ctx.guild.name}")
    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_owner)
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0xda4a))

@bot.command()
@commands.check(is_owner)
async def leave(ctx, server_id: int):
    to_leave = bot.get_guild(server_id)

    await ctx.send(embed = discord.Embed(description = f'**Я успешно прекратил обслуживание данного сервера.**', color=0x0c0c0c))
    await to_leave.leave()

@bot.command()
@commands.check(is_owner)
async def servers(ctx):
    description = ' '
    counter = 0
    for guild in bot.guilds:
        counter += 1
        description += f'{counter}) **`{guild.name}`** - **`{len(guild.members)}`** участников. ID: **`{guild.id}`** \n'
        await ctx.send(embed = discord.Embed(title = 'Сервера, на которых я нахожусь', description = description, color = 0x00ffff))

token = os.environ.get("BotToken")
bot.run(str(token))
