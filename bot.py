import discord
import asyncio
import datetime
import random as r
import random
import io
import os
import nekos
import sqlite3
import time
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

conn = sqlite3.connect("database.db") #например: C:/Users/z3r0x/Desktop/LionBot/database.db
cursor = conn.cursor()

@bot.event
async def on_ready():
    print(f'          [Bloody X]')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('EXPLOIT BLOODY X'))
    print(f"[Bloody X] Bot successfully launched!;")
    print(f"[Bloody X] Name: [{bot.user}];")
    print(f'[Bloody X] ID: [{bot.user.id}]')
    print('[------------------------------]')
    print(f'          [Other]')

@bot.event
async def is_owner(ctx):
    return ctx.author.id == 668325441224048641 # Айди создателя бота

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

@bot.command()
@commands.check(is_owner)
async def opros(ctx, *, arg):
    await ctx.message.delete()
    embed = discord.Embed(title=f"Опрос:", color = 0x00ffff)
    embed.add_field(name=f'**Вопрос:**', value=f"**{arg}**\n", inline=False)  # Создает строку
    embed.add_field(name=f'**Решение:**', value="**-=-=- Да - ❤ -=-=-\n -=-=- Нет - 💔 -=-=-**\n\n", inline=False)  # Создает строку
    embed.add_field(name=f'**Инфо:**', value="**Выбор за Вами!**", inline=False)  # Создает строку
    await ctx.send(embed=embed)

@bot.event
async def on_member_join( member ):
    emb = discord.Embed( description = f"**Приветствую тебя {member.mention}. Ты попал на сервер `{member.guild.name}`. Удачи тебе на сервере! 😜**", color = 0xda4a )
    role = discord.utils.get( member.guild.roles, id = 696322642747064383 ) # Айди роли которая будет выдаватся когда человек зашёл на сервер

    await member.add_roles( role )
    channel = bot.get_channel( 696322644106281032 ) # Айди канала куда будет писатся сообщение
    await channel.send( embed = emb )

@bot.command(aliases=['bot'])
async def botinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Информация о боте **Bloody X#7002**.\n Бот был написан специально для проекта **`Bloody X`**,\n Подробнее о командах: **`.help`**", color = 0x00ffff)
    embed.add_field(name=f'**Меня создал:**', value="๖̶̶̶ζ͜͡𝔻𝕣𝕒𝕘𝕠𝕟 𝔽𝕖𝕤𝕙#8992(<@668325441224048641>)", inline=False)  # Создает строку
    embed.add_field(name=f'**Помощь в создании:**', value="ПчелоБан#2362 (<@342317507991961602>)", inline=False)  # Создает строку
    embed.add_field(name=f'**Лицензия:**', value="LD-v7", inline=False)  # Создает строку
    embed.add_field(name=f'**Я написан на:**', value="Discord.py", inline=False)  # Создает строку
    embed.add_field(name=f'**Версия:**', value="V.3.0.1", inline=False)  # Создает строку
    embed.add_field(name=f'**Патч:**', value="10", inline=False)  # Создает строку
    embed.set_thumbnail( url = bot.user.avatar_url)
    embed.set_footer(text=f"ζ͜͡𝔻𝕣𝕒𝕘𝕠𝕟 𝔽𝕖𝕤𝕙#8992 © | Все права защищены", icon_url='https://cdn.discordapp.com/avatars/668325441224048641/8c31407c2e8c98b98b112f315b4c82b6.webp?size=1024') # создаение футера
    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_owner)
async def edit(ctx, message_id: int = None, new_content: str = None):
    if message_id == None or new_content == None:
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Пожалуйста укажите `ID` сообщения или сообщение на которое хотите изменить.**'))
    else:
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
        await ctx.send('Вы не можете убить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас ударил(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def hug(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас обнял(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

no_kill_users = [ "668325441224048641", "429350473854746629" ]
@bot.command()
async def kill(ctx, member : discord.Member = None):
	if member.id in no_kill_users:
		await ctx.send(embed = discord.Embed(description = f"Извините, но Вы не можете убить данного пользователя.", color=0x6fdb9e))
	
	elif member == None:
		emb = discord.Embed(description= f'{ctx.message.author.mention} Прыгает с крыши.', color=0x6fdb9e) # Переменная ембеда и описание
		emb.set_image(url='https://cdn.discordapp.com/attachments/702533257534898248/704731742946459708/BIty.gif')
		
		await ctx.send(embed=emb)
	else:
		emb = discord.Embed(description= f'{member.mention}, Вас убил(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
		emb.set_image(url='https://cdn.discordapp.com/attachments/702533257534898248/704733276136276078/3j0F.gif') # Ищем картинку и ставим её в ембед
 	
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
	emb = discord.Embed( title = '⚙ Навигация по командам:\n ❗ Обязательные параметры: `()`\n ❓ Необязательные параметры: `[]`', color=0x6fdb9e )
	
	emb.add_field(name='💎 Базовые:', value='``.user [@user]`` - Узнать информацию о пользователе 🎭\n ``.server`` - Узнать информацию о сервере 🧿\n `.bot` - Информация о боте 🤖\n`.avatar [@user]` - Аватар пользователя 🖼\n `.suggest (text)` - Предложить идею', inline = False)
	emb.add_field(name='🎉 Весёлости:', value='``.ran_color`` - Рандомный цвет в формате HEX 🩸\n ``.coin`` - Бросить монетку 🌈\n ``.math (2*2/2+2-2)`` - Решить пример :infinity:\n `.8ball (question)` - Волшебный шар 🔮\n `.password (10 10)` - Рандомный пароль 🎩',inline = False)
	emb.add_field(name='💋 Некос:', value='\n `.hug (@user)` - Обнять 😜\n `.slap (@user)` - Ударить 😡\n `.ran_avatar` - Рандом. аватар 🤯\n `.kill (@user)` - Убить 🔪',inline = False)
	emb.add_field(name='♥ Для создателя:', value='`.owner_help` - Навигация по всем командам 👑',inline = False)
	emb.set_thumbnail(url=ctx.guild.icon_url)
	emb.set_footer(text='ζ͜͡𝔻𝕣𝕒𝕘𝕠𝕟 𝔽𝕖𝕤𝕙#8992 © | Все права защищены', icon_url='https://cdn.discordapp.com/avatars/668325441224048641/8c31407c2e8c98b98b112f315b4c82b6.webp?size=1024')
	
	await ctx.send( embed = emb )

@bot.command()
@commands.check(is_owner)
async def owner_help(ctx):
	await ctx.message.add_reaction('✅')
	emb = discord.Embed( title = '⚙ Навигация по командам:\n ❗ Обязательные параметры: `()`\n ❓ Необязательные параметры: `[]`', color=0x6fdb9e )
	
	emb.add_field(name='💎 Базовые:', value='``.user [@user]`` - Узнать информацию о пользователе 🎭\n ``.server`` - Узнать информацию о сервере 🧿\n `.bot` - Информация о боте 🤖\n`.avatar [@user]` - Аватар пользователя 🖼', inline = False)
	emb.add_field(name='🎉 Весёлости:', value='``.ran_color`` - Рандомный цвет в формате HEX 🩸\n ``.coin`` - Бросить монетку 🌈\n ``.math (2*2/2+2-2)`` - Решить пример :infinity:\n `.8ball (question)` - Волшебный шар 🔮\n `.password (10 10)` - Рандомный пароль 🎩',inline = False)
	emb.add_field(name='💋 Некос:', value='\n `.hug (@user)` - Обнять 😜\n `.slap (@user)` - Ударить 😡\n `.ran_avatar` - Рандом. аватар 🤯\n `.kill (@user)` - Убить 🔪',inline = False)
	emb.add_field(name='♥ Для создателя:', value='`.send (@user) (text)` - Отправить в лс 🎓\n `.say (text)` - Сообщение от лица бота 🎨\n `.leave (id)` - Выйти с сервера 🧥\n `.servers` - Список серверов 🎒\n `.emoji (id) (emoji)` - Добавить эмоджи 🔊',inline = False)
	emb.set_thumbnail(url=ctx.guild.icon_url)
	emb.set_footer(text='ζ͜͡𝔻𝕣𝕒𝕘𝕠𝕟 𝔽𝕖𝕤𝕙#8992 © | Все права защищены', icon_url='https://cdn.discordapp.com/avatars/668325441224048641/8c31407c2e8c98b98b112f315b4c82b6.webp?size=1024')
	
	await ctx.author.send( embed = emb )

@bot.command()
@commands.check(is_owner)
async def send(ctx, member: discord.Member = None, *, arg): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: сообщение!**'))

    else:
        
        await member.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))

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
                                                                                      f"**🌟 Аккаунт создан: {Member.created_at.strftime('%A %b %#d, %Y')}**", 
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
async def leave(ctx, server_id: int = None):
    if server_id == None:
        await ctx.send(embed = discord.Embed(description = f'Укажите `ID` сервера!', color=0x00ffff))
    else:

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



token = os.environ.get("Token")
bot.run(str(token))
