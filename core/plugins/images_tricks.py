from core.toxbot_core_texts				import *
from simpledemotivators 				import Demotivator
from core.toxbot_core					import *
from datetime							import datetime
from discord 							import Activity, ActivityType
from pil 								import Image, ImageDraw, ImageFont, ImageOps

import requests
import asyncio
import random
import io
import os

#-	Рандомайзер фразочек -#
water = "- ToxBot#1253 -"
def random_demo():
	strings = ['Люблю когда черные квадраты обмазываются текстом']*25 + ['В чёрный квадрат постучали... \n "Демотиватор", - подумал Штирлец']*25 + ['Текст с чёрными квадратами.']*25 + ['Почему квадраты чёрные?']*25
	return random.choice(strings)

@asyncio.coroutine
async def img_tricks(discord, bot, data, print_log, notfy):
	#######################################
	##      Демотевируем все живое       ##
	#######################################
	@bot.command()
	async def dem(ctx, URL, text1 = '', text2 = ''):
		#------------------------------------------------#
		embed = discord.Embed		(title=f"🖼️ Создаем ваш демотеватор 🖼️", description="Работаем. \n \n _Думаем, получится круто..._", colour=discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail			(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed = embed)
		await asyncio.sleep(1)
		update_emb = discord.Embed	(title=f"🖼️ Создаем ваш демотеватор 🖼️", description="Работаем.. \n \n _Думаем, получится круто..._", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		await asyncio.sleep(1)
		update_emb = discord.Embed	(title=f"🖼️ Создаем ваш демотеватор 🖼️", description="Работаем... \n \n _Думаем, получится круто..._", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		#------------------------------------------------#

		try:
			#------------------------------------------------#
			outfile = './saves/demotivators/{} - Демотиватор от {}.jpg'.format(datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)
			demot = Demotivator(text1, text2)
			demot.create(URL, watermark=water, arrange=True, use_url = True, result_filename=outfile, delete_file=True)
			#------------------------------------------------#
			update_emb = discord.Embed	(title=f"🖼️ Ваш демотеватор готов! 🖼️", description="Вот ваш результат:  \n  \n *{}*".format(random_demo()), colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			await ctx.send(file=discord.File(outfile))
			#------------------------------------------------#
			print_log('image', 'Пользователь {} создал демотеватор. \n               (Сохранен как: {})'.format(ctx.message.author.name, outfile))
			#------------------------------------------------#

		except Exception as e:
			#------------------------------------------------#
			update_emb = discord.Embed	(title=f"❌ Что то пошло не так! ❌", description=f"Нам не удалось создать демотеватор: \n {str(e)} \n \n *Мы правда сожалеем об этом w_w*", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			#------------------------------------------------#
			print_log('err', 'Ошибка создания демотеватора: ' + str(e))
			#------------------------------------------------#

	#######################################
	##       Шакалим пикчи без СМС       ##
	#######################################
	@bot.command()
	async def shakal(ctx, URL, q = 8):
		#------------------------------------------------#
		embed = discord.Embed		(title=f"🖼️ Шакалим вашу пикчу 🖼️", description="Работаем. \n \n _Мы уже кинули фото в пасть шакалам..._", colour=discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail			(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed = embed)
		await asyncio.sleep(1)
		update_emb = discord.Embed	(title=f"🖼️ Шакалим вашу пикчу 🖼️", description="Работаем.. \n \n _Мы уже кинули фото в пасть шакалам..._", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		await asyncio.sleep(1)
		update_emb = discord.Embed	(title=f"🖼️ Шакалим вашу пикчу 🖼️", description="Работаем... \n \n _Мы уже кинули фото в пасть шакалам..._", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		#------------------------------------------------#

		try:
			#------------------------------------------------#
			outfile = './saves/shakalim/{} - Шакальная хуйня от {}.jpg'.format(datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)
			raw = requests.get(URL, stream=True).raw
			image = Image.open(raw).convert('RGB')

			#------------------------------------------------#
			#(width, height) = image.size
			#idraw = ImageDraw.Draw(image)
			#idraw.line((1000 - len(water) * 5, 817, 1008 + len(water) * 5, 817), fill=0, width=4)                    Тут я хотел сделать ватермарку, но ее тоже шакалит и мне лень
			#font = ImageFont.truetype(font='times.ttf', size=20, encoding='UTF-8')
			#size = idraw.textsize(water.lower(), font=font)
			#idraw.text((((width + 729) - size[0]) / 2, ((height - 192) - size[1])),water.lower(), font=font)
            #------------------------------------------------#

			image.save(outfile, 'JPEG', quality=q)
			#------------------------------------------------#
			update_emb = discord.Embed	(title=f"🖼️ Шакалы наконец догрызли пикчу! 🖼️", description="Вот ваш результат:  \n  \n *Надеимся, степень жевания вас устраивает -_-*", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			await ctx.send(file=discord.File(outfile))
			#------------------------------------------------#
			print_log('image', 'Пользователь {} зашакалил пикчу.  \n               (Сохранена как: {})'.format(ctx.message.author.name, outfile))
			#------------------------------------------------#
		except Exception as e:
			#------------------------------------------------#
			update_emb = discord.Embed	(title=f"❌ Что то пошло не так! ❌", description=f"Наши шакалы не смогли пережевать вашу пикчу: \n {str(e)} \n \n *Видимо она крепче чем их клыки O_o*", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			#------------------------------------------------#
			print_log("err", "Ошибка при сохранении шакальной херни: {}".format(e))
			#------------------------------------------------#
