from core.toxbot_core_texts				import *
from simpledemotivators 				import Demotivator, Quote
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
			demot.create(URL, watermark=water, arrange=True, use_url = True, result_filename=outfile, delete_file=True, font_name="./core/Arial.ttf")
			#------------------------------------------------#
			update_emb = discord.Embed	(title=f"🖼️ Ваш демотиватор готов! 🖼️", description="Вот ваш результат:  \n  \n *{}*".format(random_demo()), colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			await ctx.send(file=discord.File(outfile))
			#------------------------------------------------#
			print_log('image', 'Пользователь {} создал демотиватор. \n               (Сохранен как: {})'.format(ctx.message.author.name, outfile))
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
	##         Фонд Золотых Цитат        ##
	#######################################
	@bot.command()
	async def quote(ctx, nick:discord.Member = None, text = None):
		if nick != None and text != None:
			#------------------------------------------------#
			embed = discord.Embed		(title=f"🖼️ Вносим вашу цитату в фонд. 🖼️", description="Работаем. \n \n _Эти слова запомнят на веки..._", colour=discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail			(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msgs = await ctx.send(embed = embed)
			await asyncio.sleep(1)
			update_emb = discord.Embed	(title=f"🖼️ Вносим вашу цитату в фонд. 🖼️", description="Работаем.. \n \n _Эти слова запомнят на веки..._", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msgs.edit(embed=update_emb)
			await asyncio.sleep(1)
			update_emb = discord.Embed	(title=f"🖼️ Вносим вашу цитату в фонд. 🖼️", description="Работаем... \n \n _Эти слова запомнят на веки..._", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msgs.edit(embed=update_emb)
			#------------------------------------------------#
			try:
				#------------------------------------------------#
				outfile = './saves/quotes/{} - Цитата от {}.png'.format(datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)
				quote1 = Quote(text, nick.display_name)
				quote1.create(nick.avatar_url_as(format="png"), use_url = True, result_filename=outfile, headline_text_font="./core/Arial.ttf", author_name_font="./core/Arial.ttf", quote_text_font="./core/Arial.ttf")
				#------------------------------------------------#
				update_emb = discord.Embed	(title=f"🖼️ Ваш цитата внесена в Фонд! 🖼️", description="Вот что увидят ваши предки:  \n  \n *{}*".format(random_demo()), colour=discord.Colour.from_rgb(230,0,0))
				update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
				await msgs.edit(embed=update_emb)
				await ctx.send(file=discord.File(outfile))
				#------------------------------------------------#
				print_log('image', 'Пользователь {} внес свой вклад в Фонд Золотых Цитат. \n               (Сохранен как: {})'.format(ctx.message.author.name, outfile))
				#------------------------------------------------#
			except Exception as e:
				#------------------------------------------------#
				update_emb = discord.Embed	(title=f"❌ Что то пошло не так! ❌", description=f"Нам не удалось внести вашу цитату: \n {str(e)} \n \n *Возможно ваша цитата не достаточно крута w_w*", colour=discord.Colour.from_rgb(230,0,0))
				update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
				await msgs.edit(embed=update_emb)
				#------------------------------------------------#
				print_log('err', 'Ошибка создания цитаты: ' + str(e))
				#------------------------------------------------#
		elif ctx.message.reference and (msg := ctx.message.reference.resolved) and isinstance(msg, discord.Message):
			#------------------------------------------------#
			embed = discord.Embed		(title=f"🖼️ Вносим вашу цитату в фонд. 🖼️", description="Работаем. \n \n _Эти слова запомнят на веки..._", colour=discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail			(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msgs = await ctx.send(embed = embed)
			await asyncio.sleep(1)
			update_emb = discord.Embed	(title=f"🖼️ Вносим вашу цитату в фонд. 🖼️", description="Работаем.. \n \n _Эти слова запомнят на веки..._", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msgs.edit(embed=update_emb)
			await asyncio.sleep(1)
			update_emb = discord.Embed	(title=f"🖼️ Вносим вашу цитату в фонд. 🖼️", description="Работаем... \n \n _Эти слова запомнят на веки..._", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msgs.edit(embed=update_emb)
			#------------------------------------------------#
			try:
				#------------------------------------------------#
				outfile = './saves/quotes/{} - Цитата от {}.png'.format(datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)
				quote1 = Quote(msg.content, msg.author.display_name)
				quote1.create(msg.author.avatar_url_as(format="png"), use_url = True, result_filename=outfile)
				#------------------------------------------------#
				update_emb = discord.Embed	(title=f"🖼️ Ваш цитата внесена в Фонд! 🖼️", description="Вот что увидят ваши предки:  \n  \n *{}*".format('Тут должно было что-то быть, \n Фантазии ампера не хватило...'), colour=discord.Colour.from_rgb(230,0,0))
				update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
				await msgs.edit(embed=update_emb)
				await ctx.send(file=discord.File(outfile))
				#------------------------------------------------#
				print_log('image', 'Пользователь {} внес свой вклад в Фонд Золотых Цитат. \n               (Сохранен как: {})'.format(ctx.message.author.name, outfile))
				#------------------------------------------------#
			except Exception as e:
				#------------------------------------------------#
				update_emb = discord.Embed	(title=f"❌ Что то пошло не так! ❌", description=f"Нам не удалось внести вашу цитату: \n {str(e)} \n \n *Возможно ваша цитата не достаточно крута w_w*", colour=discord.Colour.from_rgb(230,0,0))
				update_emb.set_thumbnail	(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
				await msgs.edit(embed=update_emb)
				#------------------------------------------------#
				print_log('err', 'Ошибка создания цитаты: ' + str(e))
				#------------------------------------------------#
		else:
			embed = discord.Embed		(title=f"❌ Комманда введена неверно ❌", description="Вам нужно: \n \n *Или указать ответ на сообщение \n Или ввести комманду в таком формате: \n __++quote `Пинг` `'текст цитаты'`__*", colour=discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail			(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msgs = await ctx.send(embed = embed)
			print_log('err', f'Ошибка: не указан пользователь или текст.')

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