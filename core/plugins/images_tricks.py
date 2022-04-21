from discord import Activity, ActivityType
from core.toxbot_core import *
from core.toxbot_core_texts	import *
import asyncio

from simpledemotivators import Demotivator
import urllib.request
import io


@asyncio.coroutine
async def img_tricks(discord, bot, data, print_log, notfy):
	@bot.command()
	async def dem(ctx, URL, text1 = '', text2 = ''):
		try:
			with urllib.request.urlopen(URL) as url:
		 	   f = io.BytesIO(url.read())
			demot = Demotivator(text1, text2) #2 строчки, если вы хотите только одну, то оставьте вторые кавчки пустыми
			demot.create(f) #Название изображения, которое будет взято за основу демотиватора
			await ctx.send(file=discord.File('./demresult.jpg'))
		except Exception as e:
			print_log('err', 'Ошибка: ' + str(e))