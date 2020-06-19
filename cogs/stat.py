# pip install discord.py
# pip install json
# pip install asyncio

import discord
import json
import asyncio
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from random import randint

def dump( filename, filecontent ): # Фунция записи json файлов
	with open( filename, 'w', encoding = 'utf-8' ) as f:
		json.dump( filecontent, f, ensure_ascii = False )


def load( filename ): # Функция загрузки json файлов
	with open( filename, 'r', encoding = 'utf-8' ) as f:
		return json.load( f )


class Stat(object): # Создаём нужный класс

	def __init__(self, client): # Инициализатор
		self.client = client


	@commands.command(aliases = ['server-stats']) # Добавляем алиасы
	@commands.has_permissions( administrator = True ) # Только для администратора
	async def serverstats( self, ctx, arg1, *, arg2 ):
		client = self.client # Мне так удобней =))

		guild = ctx.guild # Записываем гильдию отправленого сообщения в переменную 
		message_author = ctx.author.name # Записываем автора отправленого сообщения в переменую

		stats_category = await ctx.guild.create_category(arg1) # Создаём категорию с указаным названием
		await asyncio.sleep(1) # Используем асинхроный сон на 1 секунду

		overwrite = discord.PermissionOverwrite( connect = False ) # Записываем права к будущуму голосовому каналу
		stats_channel = await ctx.guild.create_voice_channel(f' [{ctx.guild.member_count}] {arg2}', category = stats_category ) # Создаём голосовой канал
		
		await stats_channel.set_permissions( ctx.guild.default_role, overwrite = overwrite ) # К ранее созданому каналу ставим права
		await stats_category.edit( position = 0 ) # Делаем нашу категорию с каналом самыми первыми 
		
		stats_channel_id = stats_channel.id # Записываем айди созданого канала в переменную

		emb = discord.Embed( title = '**Созданна новая статистика**', description = f'**{ctx.message.author.mention} - Создатель**' , colour = discord.Color.green() ) # Делаем эмбед
		
		emb.set_author( name = client.user.name, icon_url = client.user.avatar_url ) # Добавляем автора
		emb.set_footer( text = Footer, icon_url = client.user.avatar_url ) # Добавляем футер

		await ctx.send( embed = emb ) # Отправляем ранее созданый эмбед

		info = {
			'channel_id': stats_channel_id, 
			'channel_guild': ctx.guild.name
		} # Делаем словарь с нашими даными 
		filename = f'serverstatschannel{ctx.guild.id}.json' # Получаем путь к нужному файлу

		dump( filename, info ) # Записываем наши даные в файл


	@commands.Cog.listener() # Ивент в когах
	async def on_member_join( self, member ):

		try:
			serverstats_file = f'./Data/Info/serverstatschannel{member.guild.id}.json'
			stats_channel = load( serverstats_file )

			stats_channel_id = int(stats_channel['channel_id'])
			member_count = member.guild.member_count
			channel = self.client.get_channel( stats_channel_id )

			if member_count >= 100:
				stats_channel_name = channel.name[5:]

			elif member_count >= 10:
				stats_channel_name = channel.name[4:]

			elif member_count < 10:
				stats_channel_name = channel.name[3:]

			await channel.edit( name = f' [{member_count}] {stats_channel_name}' )
		except:
			pass


	@commands.Cog.listener() # Ивент в когах
	async def on_member_remove( self, member ):

		try:
			serverstats_file = f'./Data/Info/serverstatschannel{member.guild.id}.json'
			stats_channel = load( serverstats_file )

			stats_channel_id = int(stats_channel['channel_id'])
			member_count = member.guild.member_count
			channel = self.client.get_channel( stats_channel_id )

			if member_count >= 100:
				stats_channel_name = channel.name[5:]

			elif member_count >= 10:
				stats_channel_name = channel.name[4:]

			elif member_count < 10:
				stats_channel_name = channel.name[3:]

			await channel.edit( name = f' [{member_count}] {stats_channel_name}' )
		except:
			pass
		

def setup( client ):
	client.add_cog(Stat(client))