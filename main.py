from discord import FFmpegPCMAudio, Activity, ActivityType
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
import time
import random
import asyncio
import json
import requests
import discord
import os
import pytz
bot = Bot(command_prefix="++", help_command=None)
client = discord.ext.commands.Bot(command_prefix = "++")
Token = ("OTMxMjI3NDIwNzMwNzM2Njgx.YeBXHg.gZW15MNP6W-55N-rVZZYcntDV6g")

@bot.event
async def on_ready():
	activity = discord.Game(name="++help", type=3)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="++help"))
	print("Бот успешно cumming!")



#лист команд
@bot.command()
async def help(ctx):
	await ctx.send('''
- лист всех команд на данный момент: -

- ++rlist - Список всех радиостанций.
- ++stop - Отключение бота от войса
-
- ++time - Время по мск.
-
- ++coin - Игра в монетку.
- ++randomto - Рандом от одного до любого числа.
- ++roulette - Русская рулетка.
- (*Число от 1 до 5 с приставкой* **bul** *добавляет пули, пример: ++roulette5bul*)
- ++slots - Слоты казино
-
- ++kill @человек - Убить.
- ++twisted @человек - Свернуть шею.
-
- ++google *текст* - Ссылка на запрос гугл.
- ++yandex *текст* - Ссылка на запрос яндекс.
- ++duckduck *текст* - Ссылка на запрос duckduckgo.
- (*Для более одного слова используйте +, пример: ++google рыжие+коты.*)
-
- ++steam - Ссылка на рандомную игру из стима.
''')



#инфо
@bot.command()
async def info(ctx):
	await ctx.send('''
---------------------------------------------------------
-- Работают над ботом: Tonix#5322 , 410#0797 
------------------------------------------------------------
-- Помогал: plаyer210#9142                          
------------------------------------------------------
-- Пожертвования на разработку:                            
-- <https://yoomoney.ru/to/4100112019491157>      
------------------------------------------------------------
-- Донатеры: Porg_Studio
----------------------------------------------------------
''')

#fuck_you
@bot.command()
async def fuck_you(ctx):
	author = ctx.message.author
	await ctx.send(f"No, {author.mention}, fuck you!")


#time
@bot.command()
async def time(ctx):
	tz_Moscow = pytz.timezone('Europe/Moscow')
	datetime_Moscow = datetime.now(tz_Moscow)
	await ctx.send(datetime_Moscow.strftime("%H:%M:%S"))

#пинг
@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="ping", description=f" {round(bot.latency * 1000)} ms", colour = discord.Colour.from_rgb(230,0,0))
    await ctx.send(embed=embed)



#db.addevery
@bot.event
async def rplayer() -> None:
	voice_channel = bot.get_channel(928937414913851412)
	player = await voice_channel.connect()
	player.play(FFmpegPCMAudio("http://chanson.hostingradio.ru:8041/chanson256.mp3"))
#db.stop
@bot.command()
async def stop(ctx):
	await ctx.voice_client.disconnect()
	await ctx.send("Радио остановленно.")

@bot.command()
async def c(ctx):
	await ctx.send("Ты еблан?")




#дог фокс гей егор энд кет
@bot.command()
async def dog(ctx):
	response = requests.get("https://some-random-api.ml/img/dog")
	json_data = json.loads(response.text)

	embed = discord.Embed(color = 0x8b0000, title = "Fucking dog.")
	embed.set_image(url = json_data["link"])
	await ctx.send(embed = embed)
#fox
@bot.command()
async def fox(ctx):
	response = requests.get("https://some-random-api.ml/img/fox")
	json_data = json.loads(response.text)

	embed = discord.Embed(color = 0x8b0000, title = "Fucking fox.")
	embed.set_image(url = json_data["link"])
	await ctx.send(embed = embed)
#cat
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
#gay
@bot.command()
async def gay(ctx):
	strings = ["https://media.discordapp.net/attachments/674594514303975434/931593784259674142/b95400d0-b508-4244-9bc5-a8b098f8a80e.png", "https://media.discordapp.net/attachments/762655570221203466/931594108580008026/unknown.png", "https://media.discordapp.net/attachments/674594514303975434/931602635189002240/7f6a9091-9a0b-40be-902e-85ac93930b36.png", "https://media.discordapp.net/attachments/678564352164495387/932670407876702228/unknown.png?width=455&height=675"]
	await ctx.send(random.choice(strings))
#nig
@bot.command()
async def niggers(ctx):
	strings = ["http://3.bp.blogspot.com/-yf3xMdLObGk/T3fON3wZurI/AAAAAAAA4tQ/QT5PT9q_tAY/s1600/Daddy838.jpg", "https://famt.ru/wp-content/uploads/2019/07/k-chemu-snitsya-negr-muzhchina.jpg", "https://otvet.imgsmail.ru/download/u_08aceead9e79f1fa2d6d289905d78e8d_800.jpg", "https://themancrushblog.com/wp-content/uploads/2013/11/daniel-louisy+5.jpg", "https://www.timeout.ru/img/%D0%9C%D0%B0%D1%80%D0%B3%D0%B0%D1%80%D0%B8%D1%82%D0%B0/%D0%9A%D0%B8%D0%BD%D0%BE/%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%202020/C4D_SHwWQAA2FZR.jpg","https://s00.yaplakal.com/pics/pics_original/1/6/3/14400361.jpg", "https://bi.im-g.pl/im/2/11093/z11093482IER.jpg","https://www.meme-arsenal.com/memes/f8fb9c33e73272021defca88c110cac8.jpg","https://i.imgur.com/Ogcuewp.jpg", "http://risovach.ru/upload/2018/12/generator/negr_194265628_orig_.jpg","http://prettymalemodels.com/wp-content/uploads/2017/03/DSC_7241-Edit.jpg","https://yt3.ggpht.com/-D6fqV6rRmRQ/AAAAAAAAAAI/AAAAAAAAAAA/UkT41uCEBZw/s900-c-k-no/photo.jpg","https://w7.pngwing.com/pngs/505/138/png-transparent-jay-rock-rapper-follow-me-home-musician-black-friday-jay-z-tshirt-arm-abdomen.png","https://mypersonalbroker.files.wordpress.com/2017/11/04.jpg"]
	await ctx.send(random.choice(strings))
#сочные шарики
@bot.command()
async def balls(ctx):
	strings = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ","https://i.ytimg.com/vi/qJPq0EaCRck/maxresdefault.jpg","https://ae01.alicdn.com/kf/HLB1y77JaOrxK1RkHFCcq6AQCVXaf.jpg", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/60c2c9c4-c5db-443a-ba53-0acc0a5875e7/d2m8je7-0a3eb7d7-5b0c-44d7-a536-bc4db8844b4a.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi82MGMyYzljNC1jNWRiLTQ0M2EtYmE1My0wYWNjMGE1ODc1ZTcvZDJtOGplNy0wYTNlYjdkNy01YjBjLTQ0ZDctYTUzNi1iYzRkYjg4NDRiNGEuanBnIn1dXX0.K08BpRRTK3Oqw_r-PQWbDQ_Ur-H80hIk86LW1grED5Q"]
	await ctx.send(random.choice(strings))



#рандом
@bot.command()
async def coin(ctx):
	monetka = ['Орел.'] * 49 + ['Решка.'] * 49 + ['Ребро!'] * 2
	await ctx.send(random.choice(monetka))
#и ещё рандом
@bot.command()
async def randomto(ctx, text):
	num2 = str(text)
	rndm = str(random.randint(1, int(num2[num2.find(" ")+1:len(num2)])))
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send("Выпало число " + rndm +".")
	else:
	  await ctx.send("Иди нахуй. Я ебал твою маму.",  delete_after=5)


#да или нет
@bot.command()
async def danet(ctx, *, text):
	num2 = str(text)
	danet = ['да.'] * 25 + ['нет.'] * 25 + ['скорее всего.'] * 25 + ['наверное.'] * 25
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"Я думаю что {random.choice(danet)}")
	else:
		await ctx.send("Иди нахуй. Я ебал твою маму.",  delete_after=5)


#fuck табуретка
@bot.command()
async def fuck(ctx, *, text):
	author = ctx.message.author
	num2 = str(text)
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"{author.mention} выебал " + num2 + ".")
	else:
		await ctx.send("Иди нахуй. Я ебал.",  delete_after=5)
# нет блять kill стол
@bot.command()
async def kill(ctx, *, text):
	author = ctx.message.author
	num2 = str(text)
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"{author.mention} убил " + num2 + ".")
	else:
		await ctx.send("Иди нахуй. Я ебал твою собаку.",  delete_after=5)
#да блять twisted свернул шею двери
@bot.command()
async def twisted(ctx, *, text):
	author = ctx.message.author
	num2 = str(text)
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"{author.mention} свернул шею " + num2 + ".")
	else:
		await ctx.send("Иди нахуй. Я ебал твою маму.",  delete_after=5)





#рулетка
@bot.command()
async def roulette(ctx):
	author = ctx.message.author
	ruletka = [f'Пусто, {author.mention} остался в живых.'] * 5 + [f'Выстрел, {author.mention} застрелился.'] * 1
	await ctx.send(random.choice(ruletka))
#рулетка на две пули
@bot.command()
async def roulette2bul(ctx):
	author = ctx.message.author
	ruletka = [f'Пусто, {author.mention} остался в живых.'] * 4 + [f'Выстрел, {author.mention} застрелился.'] * 2
	await ctx.send(random.choice(ruletka))
#рулетка на три пули
@bot.command()
async def roulette3bul(ctx):
	author = ctx.message.author
	ruletka = [f'Пусто, {author.mention} остался в живых.'] * 3 + [f'Выстрел, {author.mention} застрелился.'] * 3
	await ctx.send(random.choice(ruletka))
#рулетка на четыре пули
@bot.command()
async def roulette4bul(ctx):
	author = ctx.message.author
	ruletka = [f'Пусто, {author.mention} остался в живых.'] * 2 + [f'Выстрел, {author.mention} застрелился.'] * 4
	await ctx.send(random.choice(ruletka))
#рулетка на пять пуль
@bot.command()
async def roulette5bul(ctx):
	author = ctx.message.author
	ruletka = [f'Пусто, {author.mention} остался в живых.'] * 1 + [f'Выстрел, {author.mention} застрелился.'] * 5
	await ctx.send(random.choice(ruletka))
#рулетка на шесть пуль?
@bot.command()
async def roulette6bul(ctx):
	author = ctx.message.author
	await ctx.send(f'{author.mention} застрелился от своей тупости.')





#поиск в гугле, яндексе и дакдак
@bot.command()
async def google(ctx, *, text):
	text = str(text)
	num2 = str(text)
	link = (f"https://www.google.ru/search?q={text}")
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"Ссылка :dbToxCoin: на поиск по запросу {text}:  \n{link}.")
	else:
		await ctx.send("Иди нахуй. Я ебал твою маму.",  delete_after=5)


@bot.command()
async def yandex(ctx, *, text):
	text = str(text)
	num2 = str(text)
	link = (f"https://yandex.ru/search/?text={text}")
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	else:
		await ctx.send("Иди нахуй. Я ебал твою маму.",  delete_after=5)

@bot.command()
async def duckduck(ctx, *, text):
	text = str(text)
	num2 = str(text)
	link = (f"https://duckduckgo.com/?q={text}")
	if num2.find("@here") == -1 and num2.find("@everyone") == -1:
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	else:
		await ctx.send("Иди нахуй. Я ебал твою маму.",  delete_after=5)

#ссылка на рандомную стим игру
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

	await ctx.send("конец игры")


#очень много радиостанций

#список радиостанций:
@bot.command()
async def rlist(ctx):
	await ctx.send('''
- Список всех команд на переключение радиостанций: -

-----------------------------------
 ++p1 - шансон
---------------------------------
 ++p2 - радио дача
------------------------------------
 ++p3 - х_й забей радио
--------------------------------
 ++p4 - новое радио
------------------------------------
 ++p5 - фм радио
------------------------------------------------
 ++p6 - Дорожное радио (Омск)
--------------------------------------------
 ++p7 - поп радио 70х
--------------------------------------
 ++p8 - радио 80х
-------------------------------------------
 ++p9 - радио 90х
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
 ++p16 -  ретро фм
---------------------------------
 ++p17 - хевиметал
----------------------------------------------------
 ++p18 - украинское радио релакс
-----------------------------------------------
 ++p19 - детское радио
-------------------------------------
 ++p20 - ссср радио
---------------------------------------
 ++p21 - радио аниме из Осаки.
 ----------------------------------------------
 ++pRMS - радио Раммштайн
----------------------------------------------------
 ++pRHCP - red hot chili peppers радио
-------------------------------------------------------
 ++pKISH - радио Король и Шут
------------------------------------------------
 ++pL - радио Гражданская оборона
----------------------------------------------------
 ++p0 "*ссылка на поток*" - своё радио
----------------------------------------------

- список будет дополняться -
''')


#радио
async def rplay(ctx, link: None):
	if link != None:
		voice_channel = bot.get_channel(928937414913851412)
		voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
		if voice_client:
			voice_client.pause()
			voice_client.play(FFmpegPCMAudio(link))
		else:
			player = await voice_channel.connect()
			player.play(FFmpegPCMAudio(link))

@bot.command()
async def p1(ctx):
	await rplay(ctx, "http://chanson.hostingradio.ru:8041/chanson256.mp3")
	await ctx.send ("Радио включено.\nИграет: Шансон")
@bot.command()
async def p4(ctx):
	await rplay(ctx, "http://live.novoeradio.by:8000/novoeradio-128k")
	await ctx.send ("Радио включено.\nИграет: Новое радио")
@bot.command()
async def p5(ctx):
	await rplay(ctx, "http://listen.teploe.net:8100/npkfm")
	await ctx.send ("Радио включено.\nИграет: Фм радио")
@bot.command()
async def p9(ctx):
	await rplay(ctx, "http://prmstrm.1.fm:8000/90s")
	await ctx.send ("Радио включено.\nИграет: Радио 90х")
@bot.command()
async def p7(ctx):
	await rplay(ctx, "http://prmstrm.1.fm:8000/70s")
	await ctx.send ("Радио включено.\nИграет: Поп радио 70х")
@bot.command()
async def p10(ctx):
	await rplay(ctx, "http://prmstrm.1.fm:8000/acountry")
	await ctx.send ("Радио включено.\nИграет: Хиты кантри")
@bot.command()
async def p11(ctx):
	await rplay(ctx, "http://prmstrm.1.fm:8000/x")
	await ctx.send ("Радио включено.\nИграет: Хиты рока")
@bot.command()
async def p12(ctx):
	await rplay(ctx, "http://jfm1.hostingradio.ru:14536/rock00.mp3")
	await ctx.send ("Радио включено.\nИграет: Рок фм радио")
@bot.command()
async def p13(ctx):
	await rplay(ctx, "https://str.pcradio.ru/radio123_by-hi")
	await ctx.send ("Радио включено.\nИграет: Христианское радио")
@bot.command()
async def p14(ctx):
	await rplay(ctx, "http://psyprog.rupsy.ru:8000/psyprog")
	await ctx.send ("Радио включено.\nИграет: Психоделик")
@bot.command()
async def p19(ctx):
	await rplay(ctx, "https://str.pcradio.ru/rusradio_deti-hi")
	await ctx.send ("Радио включено.\nИграет: Детское радио")
@bot.command()
async def p16(ctx):
	await rplay(ctx, "https://str.pcradio.ru/retrofm_ru-hi")
	await ctx.send ("Радио включено.\nИграет: Ретро фм")
@bot.command()
async def p20(ctx):
	await rplay(ctx, "https://str.pcradio.ru/SSSR-hi")
	await ctx.send ("Радио включено.\nИграет: Ссср радио")
@bot.command()
async def p18(ctx):
	await rplay(ctx, "https://str.pcradio.ru/radiorelax_ua-hi")
	await ctx.send ("Радио включено.\nИграет: Украинское радио релакс")
@bot.command()
async def pKISH(ctx):
	await rplay(ctx, "https://str.pcradio.ru/Korol_i_Shut-hi")
	await ctx.send ("Радио включено.\nИграет: Радио Король и Шут")
@bot.command()
async def pL(ctx):
	await rplay(ctx, "https://str.pcradio.ru/Grazhdanskaja_oborona-hi")
	await ctx.send ("Радио включено.\nИграет: Радио Гражданская оборона")
@bot.command()
async def p15(ctx):
	await rplay(ctx, "https://str.pcradio.ru/rpr1_de_clasro-hi")
	await ctx.send ("Радио включено.\nИграет: Классический рок")
@bot.command()
async def p17(ctx):
	await rplay(ctx, "https://str.pcradio.ru/rpr1_de_metal-hi")
	await ctx.send ("Радио включено.\nИграет: Хевиметал")
@bot.command()  
async def pRMS(ctx):
	await rplay(ctx, "https://str.pcradio.ru/Rammstein-hi")
	await ctx.send ("Радио включено.\nИграет: Раммштайн")
@bot.command()
async def pRHCP(ctx):
	await rplay(ctx, "https://str.pcradio.ru/red_hot_chili_peppers-hi")
	await ctx.send ("Радио включено.\nИграет: Red Hot Chili Peppers радио")
@bot.command()
async def p8(ctx):
	await rplay(ctx, "https://str.pcradio.ru/pulsradio_80s-hi")
	await ctx.send ("Радио включено.\nИграет: Радио 80х")
@bot.command()
async def p6(ctx):
	await rplay(ctx, "https://str.pcradio.ru/dorozhnoe_omsk-hi")
	await ctx.send ("Радио включено.\nИграет: Дорожное радио (Омск)")
@bot.command()
async def p3(ctx):
	await rplay(ctx, "https://str.pcradio.ru/Hui_Zabey-hi")
	await ctx.send ("Радио включено. \nИграет: Х_й Забей радио")
@bot.command()
async def p2(ctx):
	await rplay(ctx, "http://178.217.40.125:8000/rdsat")
	await ctx.send ("Радио включено. \nИграет: Радио дача")
@bot.command()
async def p21(ctx):
	await rplay(ctx, "https://japanimradio-osaka.com/radio/8000/stream")
	await ctx.send ("Радио включено. \nИграет: Аниме радио из Осаки.")

@bot.command()
async def p0(ctx, *, link: str):
	if link != None:
		await rplay(ctx, str(link))
		await ctx.send(f"Радио включено. \nИграет: {str(link)}")
	else:
		await ctx.send("Вставьте ссылку.")

bot.run(Token)
