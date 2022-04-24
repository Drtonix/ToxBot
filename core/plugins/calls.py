from discord import Activity, ActivityType
from core.toxbot_core import *
from core.toxbot_core_texts	import *
import asyncio

@asyncio.coroutine
async def calls(discord, bot, data, print_log, notfy):
	@bot.command(pass_context=True)
	async def call(ctx, number = None, *,text = None):
		disp_number = number.replace('@', '').replace('<', '').replace('>', '').replace('&', '')
		embed = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description="Звонок.", colour=discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed = embed)
		await asyncio.sleep(1)
		update_emb = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description="Звонок..", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		await asyncio.sleep(1)
		update_emb = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description="Звонок...", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		await asyncio.sleep(1)

		if number == "911":
			await ctx.send(f'''
	<@&966062221589348422>''')
			update_emb = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description=f'Не волнуйтесь, полиция в пути. \n \n _Предупреждаем:_ \n *Все вызовы записываются*', colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			if text != None:
				await ctx.send(f'{text}')
			else:
				text = "Причина не известна"
			print_log('call', "Абонент {} вызвал полицию. ({})".format(ctx.message.author.name, text))
		elif number == "255":
			await ctx.send(f'''
	<@&966065342390628374>''')
			update_emb = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description=f'Вы позвонили в пиццерию. \n Ваш заказ готовится.', colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			if text != None:
				await ctx.send(f'{text}')
		elif (number !="911" and number != "255") and number != None:
			if disp_number != 'everyone' and disp_number != 'here':
				await ctx.send(f'{number}')
				update_emb = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description=f'Ожидаем ответа пользователя. \n \n _Предупреждаем:_  \n *Ваш оператор может брать плату за вызовы.*', colour=discord.Colour.from_rgb(230,0,0))
				update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
				await msg.edit(embed=update_emb)
				if text != None:
					await ctx.send(f'{text}')
			else:
				update_emb = discord.Embed(title=f"❌ Звонок прерван секретной службой БДБ ❌", description=f'В наше время за такое бы... \n В прочем не важно...  \n Просто не делай так больше.', colour=discord.Colour.from_rgb(230,0,0))
				update_emb.set_thumbnail(url="https://sun1-22.userapi.com/s/v1/ig2/oLl_jHdbHnIJTa8XG8Y_S5PUu25rsWwApBOd7Zu26sqPqWL9Kq2u_AKIqGEk6-WLV7k9oFmq7-XZ7HKH-EWuVWPv.jpg?size=200x200&quality=96&crop=149,52,420,420&ava=1")
				await msg.edit(embed=update_emb)
		elif number == None:
			update_emb = discord.Embed(title=f"📞 Звонок на номер `{disp_number}` 📞", description="Абонент не зарегестрирован в сети, \n или номер набран не правильно.", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed = update_emb)
