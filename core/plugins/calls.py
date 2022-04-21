from discord import Activity, ActivityType
from core.toxbot_core import *
from core.toxbot_core_texts	import *
import asyncio

@asyncio.coroutine
async def calls(discord, bot, data, print_log, notfy):
	@bot.command(pass_context=True)
	async def call(ctx, number = None, *,text = None):
		embed = discord.Embed(title=f"📞 Звонок на номер `{number}` 📞", description="Звонок.", colour=discord.Colour.from_rgb(230,0,0))
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		msg = await ctx.send(embed = embed)
		await asyncio.sleep(1)
		update_emb = discord.Embed(title=f"📞 Звонок на номер `{number}` 📞", description="Звонок..", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		await asyncio.sleep(1)
		update_emb = discord.Embed(title=f"📞 Звонок на номер `{number}` 📞", description="Звонок...", colour=discord.Colour.from_rgb(230,0,0))
		update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		await msg.edit(embed=update_emb)
		await asyncio.sleep(1)

		if number == "911":
			await ctx.send(f'''
	<@&966062221589348422>''')
			update_emb = discord.Embed(title=f"📞 Звонок на номер `{number}` 📞", description=f'''
	Не волнуйтесь, полиция в пути.''', colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			if text != None:
				await ctx.send(f'{text}')
		if number == "255":
			await ctx.send(f'''
	<@&966065342390628374>''')
			update_emb = discord.Embed(title=f"📞 Звонок на номер `{number}` 📞", description=f'Вы позвонили в пиццерию. \n Ваш звказ готовится.', colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed=update_emb)
			if text != None:
				await ctx.send(f'{text}')
		if (number !="911" and number != "255") or number == None:
			update_emb = discord.Embed(title=f"📞 Звонок на номер `{number}` 📞", description="Абонент не зарегестрирован в сети, \n или номер набран не правильно.", colour=discord.Colour.from_rgb(230,0,0))
			update_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			await msg.edit(embed = update_emb)