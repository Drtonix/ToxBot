from discord import FFmpegPCMAudio, Activity, ActivityType
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
import time
import random
import json
import requests
import discord
import os
import pytz
bot = Bot(command_prefix="db.", help_command=None)
client = discord.ext.commands.Bot(command_prefix = "db.")
Token = ("OTMxMjI3NDIwNzMwNzM2Njgx.YeBXHg.gZW15MNP6W-55N-rVZZYcntDV6g")


#лист команд
@bot.command()
async def help(ctx):
  await ctx.send('''
лист всех команд на данный момент:

-- db.fuck_you - Бот пошлёт тебя. --
-- db.radiolist - Список всех радиостанций. --
-- db.time - Время по мск. --
-- db.stop - Отключение бота от войса-выключить шансон. --
-- db.cat - Рандомные фото кисок. --
-- db.dog - Рандомные фото собак. --
-- db.fox - Рандомные фото лисичек. --
-- db.coin - Игра в монетку. --
-- db.randomto - Рандом от одного до любого числа. --
-- db.roulette - Русская рулетка.
   (*Число от 1 до 5 с приставкой* **bul** *добавляет пули.*) --
-- db.fuck @человек - Выебать. --
-- db.kill @человек - Убить. --
-- db.twisted @человек - Свернуть шею. --
-- db.niggers - Негры. --
-- db.gay - Егорка or Вова) --
-- db.help - Догадайся сам. --
-- db.balls - Сочные шары. --''')



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



#db.addevery
@bot.event
async def on_ready() -> None:
    voice_channel = bot.get_channel(928937414913851412)
    player = await voice_channel.connect()
    player.play(FFmpegPCMAudio("http://chanson.hostingradio.ru:8041/chanson256.mp3"))
#db.stop
@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Радио остановленно.")





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
    await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")



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
  await ctx.send("Выпало число " + rndm +".")



#fuck табуретка
@bot.command()
async def fuck(ctx, text):
  author = ctx.message.author
  num2 = str(text)
  if num2.find("@here") == -1 and num2.find("@everyone") == -1:
    await ctx.send(f"{author.mention} выебал " + num2 + ".")
  else:
    await ctx.send("Иди нахуй. Я ебал.")
# нет блять kill стол
@bot.command()
async def kill(ctx, text):
  author = ctx.message.author
  num2 = str(text)
  if num2.find("@here") == -1 and num2.find("@everyone") == -1:
    await ctx.send(f"{author.mention} убил " + num2 + ".")
  else:
    await ctx.send("Иди нахуй. Я ебал твою собаку.")
#да блять twisted свернул шею двери
@bot.command()
async def twisted(ctx, text):
  author = ctx.message.author
  num2 = str(text)
  if num2.find("@here") == -1 and num2.find("@everyone") == -1:
    await ctx.send(f"{author.mention} свернул шею " + num2 + ".")
  else:
    await ctx.send("Иди нахуй. Я ебал твою маму.")





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



#очень много радиостанций

#список радиостанций:
@bot.command()
async def radiolist(ctx):
  await ctx.send(
"(\n\Список всех команд на переключение радиостанций:\n\ndb.anime - аниме радио\n\ndb.shanson - шансон\n-------------------\ndb.novradio - новое радио\n-------------------------\ndb.fmradio - фм радио\n---------------------\ndb.dorozhnoeradio - Дорожное радио (Омск)\n--------------------\ndb.radio90s - радио 90х\n-----------------------\ndb.pulsradio80s - радио 80х\n---------------------------\ndb.popradio70s - поп радио 70х\n------------------------------\ndb.counthitsradio - хиты кантри\n-------------------------------\ndb.rockhitsradio - хиты рока\n----------------------------\ndb.rockfmradio - рок фм\n-----------------------\ndb.ruyalretradio - ретро\n------------------------\ndb.psychedcradio - психоделик\n-----------------------------\ndb.classicrock - классический рок\n------------------------------\ndb.rertofm -  ретро фм\n----------------------\ndb.heavymetal - хевиметал\n-------------------------\ndb.radiorelaxua - украинское радио релакс\n-----------------------------------------\ndb.korolishyt - радио Король и Шут\n----------------------------------\ndb.letov - радио Гражданская оборона\n--------------------------------\ndb.rammstein - радио Раммштайн\n---------------------------------\ndb.radiosssr - ссср радио\n-------------------------\ndb.radiodetyam - детское радио\n-----------------------------\ndb.redhotchilradio - red hot chili peppers радио\n\nсписок будет дополняться")



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
async def shanson(ctx):
    await rplay(ctx, "http://chanson.hostingradio.ru:8041/chanson256.mp3")
    await ctx.send ("Радио включено.\nИграет: Шансон")
@bot.command()
async def novradio(ctx):
    await rplay(ctx, "http://live.novoeradio.by:8000/novoeradio-128k")
    await ctx.send ("Радио включено.\nИграет: Новое радио")
@bot.command()
async def fmradio(ctx):
    await rplay(ctx, "http://listen.teploe.net:8100/npkfm")
    await ctx.send ("Радио включено.\nИграет: Фм радио")
@bot.command()
async def radio90s(ctx):
    await rplay(ctx, "http://prmstrm.1.fm:8000/90s")
    await ctx.send ("Радио включено.\nИграет: Радио 80х")
@bot.command()
async def popradio70s(ctx):
    await rplay(ctx, "http://prmstrm.1.fm:8000/70s")
    await ctx.send ("Радио включено.\nИграет: Поп радио 70х")
@bot.command()
async def counthitsradio(ctx):
    await rplay("http://prmstrm.1.fm:8000/acountry")
    await ctx.send ("Радио включено.\nИграет: Хиты кантри")
@bot.command()
async def rockhitsradio(ctx):
    await rplay(ctx, "http://prmstrm.1.fm:8000/x")
    await ctx.send ("Радио включено.\nИграет: Хиты рока")
@bot.command()
async def rockfmradio(ctx):
    await rplay(ctx, "http://jfm1.hostingradio.ru:14536/rock00.mp3")
    await ctx.send ("Радио включено.\nИграет: Рок фм радио")
@bot.command()
async def royalretradio(ctx):
    await rplay(ctx, "http://185.39.195.90:8000/nostalgia")
    await ctx.send ("Радио включено.\nИграет: Ретро")
@bot.command()
async def psychedcradio(ctx):
    await rplay(ctx, "http://psyprog.rupsy.ru:8000/psyprog")
    await ctx.send ("Радио включено.\nИграет: Психоделик")
@bot.command()
async def radiodetyam(ctx):
    await rplay(ctx, "https://str.pcradio.ru/rusradio_deti-hi")
    await ctx.send ("Радио включено.\nИграет: Детское радио")
@bot.command()
async def retrofm(ctx):
    await rplay(ctx, "https://str.pcradio.ru/retrofm_ru-hi")
    await ctx.send ("Радио включено.\nИграет: Ретро фм")
@bot.command()
async def radiosssr(ctx):
    await rplay(ctx, "https://str.pcradio.ru/SSSR-hi")
    await ctx.send ("Радио включено.\nИграет: Ссср радио")
@bot.command()
async def radiorelaxua(ctx):
    await rplay(ctx, "https://str.pcradio.ru/radiorelax_ua-hi")
    await ctx.send ("Радио включено.\nИграет: Украинское радио релакс")
@bot.command()
async def korolishyt(ctx):
    await rplay(ctx, "https://str.pcradio.ru/Korol_i_Shut-hi")
    await ctx.send ("Радио включено.\nИграет: Радио Король и Шут")
@bot.command()
async def letov(ctx):
    await rplay(ctx, "https://str.pcradio.ru/Grazhdanskaja_oborona-hi")
    await ctx.send ("Радио включено.\nИграет: Радио Гражданская оборона")
@bot.command()
async def classicrock(ctx):
    await rplay(ctx, "https://str.pcradio.ru/rpr1_de_clasro-hi")
    await ctx.send ("Радио включено.\nИграет: Классический рок")
@bot.command()
async def heavymetal(ctx):
    await rplay(ctx, "https://str.pcradio.ru/rpr1_de_metal-hi")
    await ctx.send ("Радио включено.\nИграет: Хевиметал")
@bot.command()  
async def rammstein(ctx):
    await rplay(ctx, "https://str.pcradio.ru/Rammstein-hi")
    await ctx.send ("Радио включено.\nИграет: Раммштайн")
@bot.command()
async def redhotchilradio(ctx):
    await rplay(ctx, "https://str.pcradio.ru/red_hot_chili_peppers-hi")
    await ctx.send ("Радио включено.\nИграет: Red Hot Chili Peppers радио")
@bot.command()
async def pulsradio80s(ctx):
    await rplay(ctx, "https://str.pcradio.ru/pulsradio_80s-hi")
    await ctx.send ("Радио включено.\nИграет: Радио 80х")
@bot.command()
async def dorozhnoeradio(ctx):
    await rplay(ctx, "https://str.pcradio.ru/dorozhnoe_omsk-hi")
    await ctx.send ("Радио включено.\nИграет: Дорожное радио (Омск)")
@bot.command()
async def anime(ctx):
    await rplay(ctx, "https://japanimradio-osaka.com/radio/8000/stream")
    await ctx.send ("Радио включено. \nИграет: Аниме радио")

@bot.command()
async def mechanic(ctx, *, link: str):
    if link != None:
        rplay(ctx, str(link))
        await ctx.send("удачно поставлено")
    else:
        await ctx.send("вставьте ссылку")

bot.run(Token)
