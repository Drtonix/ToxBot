from discord import FFmpegPCMAudio, Activity, ActivityType
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
from random import randrange, choice
import simplejson as json
from asyncio import sleep
import subprocess
import string
import time
import random
import asyncio
import json
import requests
import discord
import os
import sqlite3
import pytz
from colorama import init
from termcolor import colored
from core.toxbot_core import *
##############################################
#				 Переменные                  #
##############################################
global data
data = None
init_successful = False
##############################################
#               Инициализация                #
##############################################
init()
print(header_logo)
print_log('wait', "Ожидание:  Инициализация")
try:
	data = core_parse_data(data)
	print_log('wait', "Импорт значений из конфига.")
	if(data["FirstBoot"] == "True"):
		print_log('warn', "Обнаружен первый запуск программы:  Переходим в режим настройки")
		first_boot_cofigure(data)
	else:
		bot = Bot(command_prefix="++", help_command=None)
		client = discord.ext.commands.Bot(command_prefix = "++")
		init_successful = True
		if(init_successful):
			print_log('info', "Инициализация прошла успешно")
			try:
				print_log("wait", "Ожидание:  Запуск базы данных")
				conn = sqlite3.connect('Poor_Warrior_of_Christ.db')
				cursor = conn.cursor()
				cursor.execute('''CREATE TABLE IF NOT EXISTS economy (
					"id"	INT,
					"money"	INT)''')
				print_log("info", "База данных загруженна.")
			except Exception as e:
				print_log('err', "Ошибка базы данных: " + e)


		@bot.event
		async def on_ready():
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="++help"))
			print_log("info", "Бот успешно cumming!")
except Exception as e:
	print_log('err', "Неудалось спарсить значения из конфига: " + str(e))

##############################################
#                 Комманды					 #
##############################################
if(init_successful):
	@bot.command()
	async def ver(ctx):
		embed = discord.Embed(title="ToxBot {}!".format(num_ver), description=text_ver.format(num_ver), colour = discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed=embed)

	@bot.command()
	async def help(ctx):
			embed = discord.Embed(title="ToxBot", description='''
	- лист всех команд на данный момент: -
	-
	- ++time - Время по мск.
	-
	- ++coin - Игра в м*о*нетку.
	- ++randomto - Рандом от одного до любого числа.
	- ++roulette - Русская рулетка.
	- (*Число от 1 до 5 с приставкой* **bul** *добавляет пули, пример: ++roulette5bul*)
	- ++slots - Слоты казино
	-
	- ++kill @челов*е*к - Убить.
	- ++twisted @человек - Свернуть шею.
	- ++laugh - Бот посмеёт*с*я.
	- ++ver - Текущая версия бота.
	- ++cal *+,-,/,** *числа* - Кальк*у*лятор.
	-
	- ++google *текст* - Ссылка на запрос google.
	- ++yandex *текст* - Ссылка на запрос yandex.
	- ++duckduck *текст* - Ссылка на запрос duckduckgo.
	- ++yahoo *текст* - Ссылка на запрос yahoo.
	-
	- ++steam - Ссылка на рандомную игру из стима.
	- 
	- ++p *название или ссылка на трек* - Включить трек из ютуба.
	- ++rpl *all|one|off* - Включить/выключить повтор.
	- ++skip - Пропустить т*р*ек. 
	- ++stop - Остановить воспроизведение.
	- ++rlist - Список всех радиостанций.
	- Тайных команд: 15.
	''', colour = discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msg = await ctx.send(embed=embed)

	@bot.command()
	async def info(ctx):
			embed = discord.Embed(title="ToxBot", description='''
	---------------------------------------------------
	-- Работают над ботом:
	-- Tonix#5322 , 410#0797, Ampernic#9707, *?*
	-- Работа над серверной частью: Ampernic#9707
	-------------------------------------------------
	-- Пожертвования на разработку:
	-- Юmoney:
	-- <https://yoomoney.ru/to/4100112019491157>
	-- Qiwi:
	-- TONIXX
	----------------------------------------------------
	-- Донатеры:
	-- Porg_Studio - dlc для Dead Sells
	-- Ampernic - 50 рублей ежемесячно
	--------------------------------------------------
	-- Официальный сервер бота:
	-- https://discord.gg/XMYZKS3b3j
	-------------------------------------------
	-- Спасибо что пользуетесь ToxBot!
	----------------------------------------------
	''', colour = discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msg = await ctx.send(embed=embed)

	@bot.command()
	async def tb(ctx):
		embed = discord.Embed(title="ToxBot", description="На месте✅", colour = discord.Colour.from_rgb(0,230,0))
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed=embed)


	@bot.command()
	async def cal(ctx, operation, *nums):
		if operation not in ['+', '-', '*', '/']:
			await ctx.reply('Пожалуйста введите команду правильно.')
		var = f' {operation} '.join(nums)
		await ctx.reply(f'{var} = {eval(var)}')


	@bot.command()
	async def nothing(ctx):
		await ctx.send("** **")


	@bot.command()
	async def laugh(ctx):
		def rnd_str(min_chars=6, max_chars=10, alphabet=("А", "Х", "П", "а", "х", "п")):
			return ''.join(random.choices(alphabet, k=random.randint(min_chars, max_chars)))
		await ctx.send(f"{(rnd_str(6, 10))}!!!")


	@bot.command()
	async def fuck_you(ctx):
		author = ctx.message.author
		await ctx.reply(f"No, {author.mention}, fuck you!")


	@bot.command()
	async def time(ctx):
		tz_Moscow = pytz.timezone('Europe/Moscow')
		datetime_Moscow = datetime.now(tz_Moscow)
		embed = discord.Embed(title="ToxBot", description=datetime_Moscow.strftime("%H:%M:%S"), colour = discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed=embed)


	@bot.command()
	async def ping(ctx):
		embed = discord.Embed(title="Понг!", description=f" {round(bot.latency * 1000)} мс.", colour = discord.Colour.from_rgb(230,0,0))
		await ctx.send(embed=embed)


	@bot.command()
	async def c(ctx):
		author = ctx.message.author
		await ctx.reply(f"{author.mention} ты еблан?")


	@bot.command()
	async def dog(ctx):
		response = requests.get("https://some-random-api.ml/img/dog")
		json_data = json.loads(response.text)
		embed = discord.Embed(color = 0x8b0000, title = "Fucking dog.")
		embed.set_image(url = json_data["link"])
		await ctx.send(embed = embed)


	@bot.command()
	async def fox(ctx):
		response = requests.get("https://some-random-api.ml/img/fox")
		json_data = json.loads(response.text)
		embed = discord.Embed(color = 0x8b0000, title = "Fucking fox.")
		embed.set_image(url = json_data["link"])
		await ctx.send(embed = embed)


	@bot.command()
	async def cat(ctx):
		response = requests.get("https://some-random-api.ml/img/cat")
		json_data = json.loads(response.text)
		embed = discord.Embed(color = 0x8b0000, title = "Fucking cat.")
		embed.set_image(url = json_data["link"])
		await ctx.send(embed = embed)


	@bot.command()
	async def cum(ctx):
		response = ("http://www.hudeem-s-profi.ru/files/images/6zqbxxxljrnpsdldhcxz.jpg")
		await ctx.send(response)


	@bot.command()
	async def xoxol(ctx):
		response = ("https://avelita.ru/wa-data/public/shop/products/94/02/10294/images/25335/25335.650.jpg")
		embed = discord.Embed(title="хохлы", description="В связи с ситуацией в украине, эта команда временно не работает.", colour = discord.Colour.from_rgb(230,0,0))
		embed.set_image(url = response)
		await ctx.send(embed = embed)


	@bot.command()
	async def gay(ctx):
		strings = ["https://media.discordapp.net/attachments/674594514303975434/931593784259674142/b95400d0-b508-4244-9bc5-a8b098f8a80e.png", "https://media.discordapp.net/attachments/762655570221203466/931594108580008026/unknown.png", "https://media.discordapp.net/attachments/674594514303975434/931602635189002240/7f6a9091-9a0b-40be-902e-85ac93930b36.png", "https://media.discordapp.net/attachments/678564352164495387/932670407876702228/unknown.png?width=455&height=675"]
		await ctx.send(random.choice(strings))


	@bot.command()
	async def niggers(ctx):
		strings = ["http://3.bp.blogspot.com/-yf3xMdLObGk/T3fON3wZurI/AAAAAAAA4tQ/QT5PT9q_tAY/s1600/Daddy838.jpg", "https://famt.ru/wp-content/uploads/2019/07/k-chemu-snitsya-negr-muzhchina.jpg", "https://otvet.imgsmail.ru/download/u_08aceead9e79f1fa2d6d289905d78e8d_800.jpg", "https://themancrushblog.com/wp-content/uploads/2013/11/daniel-louisy+5.jpg", "https://www.timeout.ru/img/%D0%9C%D0%B0%D1%80%D0%B3%D0%B0%D1%80%D0%B8%D1%82%D0%B0/%D0%9A%D0%B8%D0%BD%D0%BE/%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%202020/C4D_SHwWQAA2FZR.jpg","https://s00.yaplakal.com/pics/pics_original/1/6/3/14400361.jpg", "https://bi.im-g.pl/im/2/11093/z11093482IER.jpg","https://www.meme-arsenal.com/memes/f8fb9c33e73272021defca88c110cac8.jpg","https://i.imgur.com/Ogcuewp.jpg", "http://risovach.ru/upload/2018/12/generator/negr_194265628_orig_.jpg","http://prettymalemodels.com/wp-content/uploads/2017/03/DSC_7241-Edit.jpg","https://yt3.ggpht.com/-D6fqV6rRmRQ/AAAAAAAAAAI/AAAAAAAAAAA/UkT41uCEBZw/s900-c-k-no/photo.jpg","https://w7.pngwing.com/pngs/505/138/png-transparent-jay-rock-rapper-follow-me-home-musician-black-friday-jay-z-tshirt-arm-abdomen.png","https://mypersonalbroker.files.wordpress.com/2017/11/04.jpg"]
		await ctx.send(random.choice(strings))


	@bot.command()
	async def balls(ctx):
		strings = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ","https://i.ytimg.com/vi/qJPq0EaCRck/maxresdefault.jpg","https://ae01.alicdn.com/kf/HLB1y77JaOrxK1RkHFCcq6AQCVXaf.jpg", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/60c2c9c4-c5db-443a-ba53-0acc0a5875e7/d2m8je7-0a3eb7d7-5b0c-44d7-a536-bc4db8844b4a.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi82MGMyYzljNC1jNWRiLTQ0M2EtYmE1My0wYWNjMGE1ODc1ZTcvZDJtOGplNy0wYTNlYjdkNy01YjBjLTQ0ZDctYTUzNi1iYzRkYjg4NDRiNGEuanBnIn1dXX0.K08BpRRTK3Oqw_r-PQWbDQ_Ur-H80hIk86LW1grED5Q"]
		await ctx.send(random.choice(strings))


	@bot.command()
	async def coin(ctx):
		monetka = ['Орел.'] * 49 + ['Решка.'] * 49 + ['Ребро!'] * 2
		await ctx.send(random.choice(monetka))


	@bot.command()
	async def randomto(ctx, text):
		num2 = str(text)
		rndm = str(random.randint(1, int(num2[num2.find(" ")+1:len(num2)])))
		await ctx.send("Выпало число " + rndm +".")


	@bot.command()
	async def danet(ctx, *, text):
		num2 = str(text)
		danet = ['да.'] * 25 + ['нет.'] * 25 + ['скорее всего.'] * 25 + ['наверное.'] * 25
		await ctx.send(f"Я думаю что {random.choice(danet)}")


	@bot.command()
	async def fuck(ctx, *, text):
		author = ctx.message.author
		txt = discord.utils.escape_mentions(text)
		await ctx.send(f"{author.mention} выебал {txt}.")


	@bot.command()
	async def kill(ctx, *, text):
		author = ctx.message.author
		txt = discord.utils.escape_mentions(text)
		await ctx.send(f"{author.mention} убил {txt}.")


	@bot.command()
	async def twisted(ctx, *, text):
		author = ctx.message.author
		txt = discord.utils.escape_mentions(text)
		await ctx.send(f"{author.mention} свернул шею {txt}.")


	@bot.command()
	async def roulette(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 5 + [f'Выстрел, {author.mention} застрелился.'] * 1
		await ctx.send(random.choice(ruletka))
	@bot.command()
	async def roulette2bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 4 + [f'Выстрел, {author.mention} застрелился.'] * 2
		await ctx.send(random.choice(ruletka))
	@bot.command()
	async def roulette3bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 3 + [f'Выстрел, {author.mention} застрелился.'] * 3
		await ctx.send(random.choice(ruletka))
	@bot.command()
	async def roulette4bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 2 + [f'Выстрел, {author.mention} застрелился.'] * 4
		await ctx.send(random.choice(ruletka))
	@bot.command()
	async def roulette5bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 1 + [f'Выстрел, {author.mention} застрелился.'] * 5
		await ctx.send(random.choice(ruletka))
	@bot.command()
	async def roulette6bul(ctx):
		author = ctx.message.author
		await ctx.send(f'{author.mention} застрелился от своей тупости.')


	@bot.command()
	async def google(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://www.google.ru/search?q={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	@bot.command()
	async def yandex(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://yandex.ru/search/?text={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	@bot.command()
	async def duckduck(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://duckduckgo.com/?q={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	@bot.command()
	async def yahoo(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://search.yahoo.com/search?p={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")


	@bot.command()
	async def steam(ctx):
		await ctx.send("Ссылка на рандомную игру из стима:\n<https://store.steampowered.com/explore/random>")


	@bot.command()
	async def slots(ctx):
		slots = ["🍓", "🍉","🍋", "🍒"]
		r1 = random.choice(slots)
		embed = discord.Embed(title="ToxCasino777", description=r1 + ":grey_question:" + ":grey_question:" + ":exclamation:", colour = discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail(url="https://0225.ru/uploads/posts/2019-12/1576091203_fruktovye-sloty.jpg")
		msg = await ctx.send(embed=embed)
		for x in range(4):
			r1 = random.choice(slots)
			await asyncio.sleep(0.2)
			new_emb = discord.Embed(title="ToxCasino777", description=r1 + ":grey_question:" + ":grey_question:" + ":exclamation:", colour = discord.Colour.from_rgb(230,0,0))
			new_emb.set_thumbnail(url="https://0225.ru/uploads/posts/2019-12/1576091203_fruktovye-sloty.jpg")
			await msg.edit(embed=new_emb)
			r2 = random.choice(slots)
		for x in range(4):
			r2 = random.choice(slots)
			await asyncio.sleep(0.2)
			new_emb = discord.Embed(title="ToxCasino777", description=r1 + r2  + ":grey_question:" + ":exclamation:", colour = discord.Colour.from_rgb(230,0,0))
			new_emb.set_thumbnail(url="https://0225.ru/uploads/posts/2019-12/1576091203_fruktovye-sloty.jpg")
			await msg.edit(embed=new_emb)
			r3 = random.choice(slots)
		for x in range(4):
			r3 = random.choice(slots)
			await asyncio.sleep(0.2)
			new_emb = discord.Embed(title="ToxCasino777", description=r1 + r2  + r3  + ":exclamation:", colour = discord.Colour.from_rgb(230,0,0))
			new_emb.set_thumbnail(url="https://0225.ru/uploads/posts/2019-12/1576091203_fruktovye-sloty.jpg")
			await msg.edit(embed=new_emb)
		await ctx.reply("Конец игры.")

	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


	@bot.command(aliases = ["balance", "баланс", "деньги"])
	async def bal(ctx, member: discord.Member = None):
		if member is None:
			UsTaCr.author(ctx)
			for row in cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id}'):
				embed = discord.Embed(title = "TOXCOINS!", description = f"баланс {ctx.message.author.display_name} токскоинов - {row[0]}", colour = discord.Colour.from_rgb(51,255,51))
				await ctx.send(embed=embed)
		else:
			UsTaCr.member(ctx, member)
			for row in cursor.execute(f'SELECT "money" FROM economy WHERE id = {member.id}'):
				embed = discord.Embed(title = "TOXCOINS!", description = f"баланс {member.display_name} токскоинов - {row[0]}", colour = discord.Colour.from_rgb(51,255,51))
				await ctx.send(embed=embed)
	
	@bot.command(aliases = ["pay", "заплатить", "отдать"])
	async def give(ctx, member: discord.Member = None, Value: int = None):
		if member is None:
			await ctx.send("Укажите цель!")
		else:
			UsTaCr.author(ctx)
			UsTaCr.member(ctx, member)
			if Value is None:
				await ctx.send("Укажите количество коинов!")
			elif Value <= 0:
				await ctx.send("Нельзя передать 0 коинов или меньше!")
			else:
				ebal = 0
				for row in cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id}'):
					ebal = int(row[0])
				if ebal >= Value:
					for row in cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id}'):
					    orow1 = int(row[0])
					    row1 = int(row[0]) - Value
					curosr.execute(f'UPDATE economy SET money = {row1} WHERE id={ctx.author.id}')
					for row in cursor.execute(f'SELECT money FROM economy WHERE id={member.id}'):
					    orow2 = int(row[0])
					    row2 = int(row[0]) + Value
					curosr.execute(f'UPDATE economy SET money = {row2} WHERE id={member.id}')
					embed = discord.Embed(title="Toxcoins", description=f"пользователь {ctx.author.display_name} дал {Value} коинов {member.display_name}. \nновый баланс {member.display_name} - {row2}")
				else:
					await ctx.send("Недостаточно денег!")

	@bot.command()
	async def rlist(ctx):
		await ctx.send('''
	- Список всех команд на переключение радиостанций: -
	-----------------------------------
	 ++p1 - Шансон
	---------------------------------
	 ++p2 - Радио Дача
	------------------------------------
	 ++p3 - Х*й забей радио
	--------------------------------
	 ++p4 - Новое Радио
	------------------------------------
	 ++p5 - FM радио
	------------------------------------------------
	 ++p6 - Дорожное Радио (Омск)
	--------------------------------------------
	 ++p7 - POP радио 70х
	--------------------------------------
	 ++p8 - Радио 80х
	-------------------------------------------
	 ++p9 - Радио 90х
	----------------------------------------
	 ++p10 - хиты кантри
	-------------------------------------------
	 ++p11 - хиты рока
	------------------------------------
	 ++p12 - рок фм
	-----------------------------------------
	 ++p13 - Христианское радио
	-------------------------------------
	 ++p14 - психоделик
	----------------------------------------
	 ++p15 - классический рок
	------------------------------------------
	 ++p16 - Ретро FM
	---------------------------------
	 ++p17 - Хевиметал
	----------------------------------------------------
	 ++p18 - Украинское Радио Релакс
	-----------------------------------------------
	 ++p19 - детское радио
	-------------------------------------
	 ++p20 - ссср радио
	---------------------------------------
	 ++p21 - радио аниме из Осаки.
	----------------------------------------------
	 ++p22 - Джаз.
	-------------------------------------------- 
	 ++p23 - lofi.
	------------------------------------------- ''')
		await ctx.send('''
	** **++pRMS - Радио "RAMSHTEIN"
	----------------------------------------------------
	 ++pRHCP - "Red Hot Chili Peppers" радио
	-------------------------------------------------------
	 ++pKISH - Радио "Король и Шут""
	------------------------------------------------
	 ++pL - Радио "Гражданская оборона"
	----------------------------------------------------
	 ++p0 "*ссылка на поток*" - Своё радио
	----------------------------------------------
	- список будет дополняться -
	''')
	async def rplay(ctx, link: None):
		if link != None:
			voice_channel = ctx.author.voice.channel
			voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
			if voice_client:
				voice_client.pause()
				if(data["OS"]==1):
					player.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source = link, **FFMPEG_OPTIONS))
				elif(data["OS"]==0):
					voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = link, **FFMPEG_OPTIONS))
			else:
				player = await voice_channel.connect()
				if(data["OS"]==1):
					player.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source = link, **FFMPEG_OPTIONS))
				elif(data["OS"]==0):
					voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = link, **FFMPEG_OPTIONS))


	@bot.command()
	async def p1(ctx):
		await rplay(ctx, "http://chanson.hostingradio.ru:8041/chanson256.mp3", )
		await ctx.send("Радио включено.\nИграет: Шансон")
		print_log('info', "Радио включено: Шансон")
	@bot.command()
	async def p4(ctx):
		await rplay(ctx, "http://live.novoeradio.by:8000/novoeradio-128k")
		await ctx.send("Радио включено.\nИграет: Новое радио")
		print_log('info', "Радио включено: Новое радио")
	@bot.command()
	async def p5(ctx):
		await rplay(ctx, "http://listen.teploe.net:8100/npkfm")
		await ctx.send("Радио включено.\nИграет: FM радио")
		print_log('info', "Радио включено: FM радио")
	@bot.command()
	async def p9(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/90s")
		await ctx.send("Радио включено.\nИграет: Радио 90х")
		print_log('info', "Радио включено: Радио 90х")
	@bot.command()
	async def p7(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/70s")
		await ctx.send("Радио включено.\nИграет: Поп радио 70х")
		print_log('info', "Радио включено: Поп радио 70х")
	@bot.command()
	async def p10(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/acountry")
		await ctx.send("Радио включено.\nИграет: Хиты кантри")
		print_log('info', "Радио включено: Хиты кантри")
	@bot.command()
	async def p11(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/x")
		await ctx.send("Радио включено.\nИграет: Хиты рока")
		print_log('info', "Радио включено: Хиты рока")
	@bot.command()
	async def p12(ctx):
		await rplay(ctx, "http://jfm1.hostingradio.ru:14536/rock00.mp3")
		await ctx.send("Радио включено.\nИграет: Рок FM")
		print_log('info', "Радио включено: Рок FM")
	@bot.command()
	async def p13(ctx):
		await rplay(ctx, "https://str.pcradio.ru/radio123_by-hi")
		await ctx.send("Радио включено.\nИграет: Христианское радио")
		print_log('info', "Радио включено: Христианское радио")
	@bot.command()
	async def p14(ctx):
		await rplay(ctx, "http://psyprog.rupsy.ru:8000/psyprog")
		await ctx.send("Радио включено.\nИграет: Психоделик")
		print_log('info', "Радио включено: Психоделик")
	@bot.command()
	async def p19(ctx):
		await rplay(ctx, "https://str.pcradio.ru/rusradio_deti-hi")
		await ctx.send("Радио включено.\nИграет: Детское радио")
		print_log('info', "Радио включено: Детское радио")
	@bot.command()
	async def p16(ctx):
		await rplay(ctx, "https://str.pcradio.ru/retrofm_ru-hi")
		await ctx.send("Радио включено.\nИграет: Ретро FM")
		print_log('info', "Радио включено: Ретро FM")
	@bot.command()
	async def p20(ctx):
		await rplay(ctx, "https://str.pcradio.ru/SSSR-hi")
		await ctx.send("Радио включено.\nИграет: СССР радио")
		print_log('info', "Радио включено: СССР радио")
	@bot.command()
	async def p18(ctx):
		await rplay(ctx, "https://str.pcradio.ru/radiorelax_ua-hi")
		await ctx.send("Радио включено.\nИграет: Украинское радио релакс")
		print_log('info', "Радио включено: Украинское радио релакс")
	@bot.command()
	async def pKISH(ctx):
		await rplay(ctx, "https://str.pcradio.ru/Korol_i_Shut-hi")
		await ctx.send("Радио включено.\nИграет: Радио Король и Шут")
		print_log('info', "Радио включено: Радио Король и Шут")
	@bot.command()
	async def pL(ctx):
		await rplay(ctx, "https://str.pcradio.ru/Grazhdanskaja_oborona-hi")
		await ctx.send("Радио включено.\nИграет: Радио Гражданская оборона")
		print_log('info', "Радио включено: Радио Гражданская оборона")
	@bot.command()
	async def p15(ctx):
		await rplay(ctx, "https://str.pcradio.ru/rpr1_de_clasro-hi")
		await ctx.send("Радио включено.\nИграет: Классический рок")
		print_log('info', "Радио включено: Классический рок")
	@bot.command()
	async def p17(ctx):
		await rplay(ctx, "https://str.pcradio.ru/rpr1_de_metal-hi")
		await ctx.send("Радио включено.\nИграет: Хевиметал")
		print_log('info', "Радио включено: Хевиметал")
	@bot.command()  
	async def pRMS(ctx):
		await rplay(ctx, "https://str.pcradio.ru/Rammstein-hi")
		await ctx.send("Радио включено.\nИграет: Раммштайн")
		print_log('info', "Радио включено: Раммштайн")
	@bot.command()
	async def pRHCP(ctx):
		await rplay(ctx, "https://str.pcradio.ru/red_hot_chili_peppers-hi")
		await ctx.send("Радио включено.\nИграет: Red Hot Chili Peppers радио")
		print_log('info', "Радио включено: Red Hot Chili Peppers радио")
	@bot.command()
	async def p8(ctx):
		await rplay(ctx, "https://str.pcradio.ru/pulsradio_80s-hi")
		await ctx.send("Радио включено.\nИграет: Радио 80х")
		print_log('info', "Радио включено: Радио 80х")
	@bot.command()
	async def p6(ctx):
		await rplay(ctx, "https://str.pcradio.ru/dorozhnoe_omsk-hi")
		await ctx.send("Радио включено.\nИграет: Дорожное радио (Омск)")
		print_log('info', "Радио включено: Дорожное радио (Омск)")
	@bot.command()
	async def p3(ctx):
		await rplay(ctx, "https://str.pcradio.ru/Hui_Zabey-hi")
		await ctx.send("Радио включено. \nИграет: Х*й Забей радио")
		print_log('info', "Радио включено: Х*й Забей радио")
	@bot.command()
	async def p2(ctx):
		await rplay(ctx, "http://178.217.40.125:8000/rdsat")
		await ctx.send("Радио включено. \nИграет: Радио дача")
		print_log('info', "Радио включено: Играет: Радио дача")
	@bot.command()
	async def p21(ctx):
		await rplay(ctx, "https://japanimradio-osaka.com/radio/8000/stream")
		await ctx.send("Радио включено. \nИграет: Аниме радио из Осаки.")
		print_log('info', "Радио включено: Аниме радио из Осаки.")
	@bot.command()
	async def p22(ctx):
		await rplay(ctx, "http://jfm1.hostingradio.ru:14536/jlstream.mp3")
		await ctx.send("Радио включено. \nИграет: Джаз.")
		print_log('info', "Радио включено: Джаз.")
	@bot.command()
	async def p23(ctx):
		await rplay(ctx, "https://usa9.fastcast4u.com/proxy/jamz?mp=/1")
		await ctx.send("Радио включено. \nИграет: Lofi.")
		print_log('info', "Радио включено: Lofi.")


	@bot.command()
	async def p0(ctx, *, link: str):
		txt = discord.utils.escape_mentions(link)
		if link != None:
			await rplay(ctx, str(txt))
			await ctx.send(f"Радио включено. \nИграет: {str(txt)}")
			print_log('info', "Радио включено: Своя радиостанция (Вызвано {})".format(+ ctx.message.author.name))
		else:
			await ctx.send("Вставьте ссылку.")
	

	## Ивент на 21.03.22 (или позже) ##


	@bot.command()
	async def Error(ctx):
		await ctx.send('''
	Говорит ToxBot, если вы ввели эту команду, то вы любите загадки.
	Если сможете отгАдать все спрятанные коMанды то в конце вас ждёт
	спойлер к новому обнОвлению и послание от неизвестного разрабоTчика.
	Все команды пишYтся на латинице.
	Первая команда уже спрятана в этом сообщении, удачи.''')
	@bot.command()
	async def AMOTY(ctx):
		await ctx.send('''
	Вы смогли разгадать первую команду, поздравляю.
	Для второй мы подготовили загадку:
	Как зовут основателя ToxBot?''')
	@bot.command()
	async def Tonix(ctx):
		await ctx.send('''
		Как многие называют ToxBot?
		*Писать на английском языке*''')
	@bot.command()
	async def Toxa(ctx):
		await ctx.send('''
	Всему свое время, и время всякой вещи под небом:
	время рождаТься и время умирать… время разрушать, и время строIть…
	время разбрасывать каМни, и время собирать камни; время обнимать,
	и время уклоняться от объятий… врЕмя любить, и время ненавидеть;
	время войне, и время миру. ''')
	@bot.command()
	async def TIME(ctx):
		await ctx.send('''
	Мы не стоLько любим людей за то добро, которое они нам сделали, сколько за то добро, которое мы Iм сдEлали.''')
	@bot.command()
	async def LIE(ctx):
		await ctx.send('''
	2+2/2=?''')
	@bot.command()
	async def three(ctx):
		await ctx.send('''
	Легко?
	А теперь найдите следующую команду в списке команд.''')
	@bot.command()
	async def oecyp(ctx):
		await ctx.send('''
	https://www.youtube.com/watch?v=dQw4w9WgXcQ''')
	@bot.command()
	async def Q49WXQ(ctx):
		await ctx.send('''
	Ну а теперь финальная команда.
	Как сначала назывался бот?
	S####o#B##''')
	@bot.command()
	async def ShansonBot(ctx):
			embed = discord.Embed(title=ToxBot, description='''
	Поздравляю, вы отгадали все кOMанды.
	В следующем обновлении будет очEнь много фиксов,
	команды для донатеров и так же ноBая команда в
	которой будет информация о ближайшем обновлении.
	Надеюсь вам было хотя бы немHого интересно.''', colour = discord.Colour.from_rgb(230,0,0))
	@bot.command()
	async def OMEBH(ctx):
		response = ("https://media.discordapp.net/attachments/944694959255191603/955195169274228736/unknown.png")
		await ctx.send(response)

	plgins(discord, bot, data)
	bot.run(data["Token"])
else:
	print_log('err', "Инициализация прерванна.")
