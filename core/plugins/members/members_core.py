import discord
import asyncio
import random

from datetime import datetime
from Cybernator import Paginator as Pag
from core.toxbot_core import print_log, send_embed

def members_core(bot, manager_data):
	class mmbr_core:
		def __init__(self, manager_data):
			self.name 	= 'members_core'
			self.ver 	= 'v0.0.1 build 5'
			self.require= ['DB_Core', 'economy_core', 'level_core']
			self.loaded = False
			manager_data.plugins_counter+=1
			print_log('wait', '\tОжидание: Загрузка пользовательского модуля')
			print_log('bank', '\t\tВыполняется: Проверка наличия зависимостей модуля')
			try:
				from core.plugins.database_core import db, UsTaCr, SeTaCr
				global db, UsTaCr, SeTaCr
				if self.require[0] in manager_data.loaded_plugins:
					if self.require[1] in manager_data.loaded_plugins:
						if self.require[2] in manager_data.loaded_plugins:
							self.loaded = True
							manager_data.loaded_plugins.update({self.name : self.ver})
							print_log('info', '\tУспех: Пользовательский модуль инициализирован\n')
						else:
							print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[3]}. Плагин может работать некоректно.\n')
					else:
						print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[1]}. Плагин может работать некоректно.\n')
				else:
					print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[0]}. Плагин может работать некоректно.\n')
			except:
				print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[0]}. Плагин может работать некоректно.\n')

	plugin = mmbr_core(manager_data)

	if plugin.loaded:
		@bot.command(aliases = ["статистика", "серверстат", "серверстатс", "statistics", "статс", "статы", "лвл"])
		async def stats(ctx,member:discord.Member = None, guild: discord.Guild = None):
			if member is None:
				member = ctx.author
			try:

				##############################
				#	 	  Страница 1         #
				##############################
				emb1 = discord.Embed(title=f"Информация о пользователе {member}:", color=discord.Colour.from_rgb(230,0,0))
				emb1.add_field(name="Никнейм:", value=f'`{member.display_name}`',inline=False)
				t = member.status
				if t == discord.Status.online:
					d = "`В сети`"
				t = member.status
				if t == discord.Status.offline:
					d = "`Не в сети`"
				t = member.status
				if t == discord.Status.idle:
					d = "`Не активен`"
				t = member.status
				if t == discord.Status.dnd:
					d = "`Не беспокоить`"

				if member.activity is None:
					mmbr_activity = '`Отсутствует`'
				else:
					mmbr_activity = f'`{member.activity}`'

				emb1.add_field(name="Активность:", value=d,inline=False)
				emb1.add_field(name="Статус:", value=mmbr_activity,inline=False)
				

				##############################
				#	 	  Страница 2         #
				##############################

				emb2 = discord.Embed(title=f"Информация о пользователе {member}:", color=discord.Colour.from_rgb(230,0,0))
				for row in db.cursor.execute(f'SELECT row_number() over(order by exp desc), id, exp, level FROM levels WHERE guild_id = {ctx.guild.id} ORDER BY exp DESC'):
					if row[1] == member.id:
						emb2.add_field(name="Уровень на сервере: ", value=f'`{row[3]} уровень`',inline=False)
						emb2.add_field(name="Опыт: ", value=f'`{row[2]} exp`', inline=False)
						emb2.add_field(name="Место в топе: ", value=f'`{row[0]} место`', inline=False) 

				##############################
				#	 	  Страница 3         #
				##############################

				emb3 = discord.Embed(title=f"Информация о пользователе {member}:", color=discord.Colour.from_rgb(230,0,0))
				emb3.add_field(name="Роль на сервере:", value=member.top_role.mention,inline=False)
				emb3.add_field(name="Зашёл на сервер:", value=f'`{member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`',inline=False)
				emb3.add_field(name="Аккаунт был создан:", value=f'`{member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`',inline=False)

				##############################
				#	 	  Страница 4         #
				##############################

				emb4 = discord.Embed(title=f"Информация о пользователе {member}:", color=discord.Colour.from_rgb(230,0,0))
				for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id = {member.id} AND guild_id = {ctx.guild.id}'):
					emb4.add_field(name="Баланс:", value=f'`{row[0]} TXC`',inline=False)

				from core.plugins.economy.economy_core import get_history
				emb4.add_field(name="Последняя операция:", value=f'```bash\n{await get_history(ctx, ctx.author, ctx.author)}```',inline=False)


				embeds = [emb1, emb3, emb2, emb4]
				message = await ctx.send(embed = emb1)
				reactions = ["◀️", "▶️"]
				page = Pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, color = discord.Colour.from_rgb(230,0,0), use_exit = False, reactions = reactions, timeout = 99)
				await page.start()
			except Exception as e:
				await ctx.send(str(e))

		@bot.command(aliases = ['онлайн'])
		async def online(ctx):
			members = ctx.guild.members
			online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
			idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
			offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
			dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
			all_members = online+idle+offline+dnd

			embed = discord.Embed(title="ToxBot", description=f'''\nОнлайн: {online}.\n Оффлайн: {offline}.\n  Неактивны: {idle}.\n   Не беспокоить: {dnd}.\n      Всего участников: {all_members}.''', colour = discord.Colour.from_rgb(230,0,0))
			embed.set_footer(text=f'ToxBot Members')
			await ctx.send(embed=embed)
		
		@bot.command(aliases = ['топ', 'ранги', 'rank'])
		async def ranks(ctx):
			try:
				count = 1
				top_users = '';
				for row in db.cursor.execute(f"SELECT id, exp, level FROM levels WHERE guild_id = {ctx.guild.id} ORDER BY exp DESC LIMIT 5"): 
					user = await bot.fetch_user(row[0])
					username = user.display_name
					if len(username) < 7:
						while len(username) != 7:
							username = username+' '
					elif len(username) > 7:
						username = username[0:7]
					top_users = top_users+f'\n[{count}] {username}\t {row[1]} exp ({row[2]} lvl)'
					count += 1
				embed = discord.Embed(title="Топ участников", description=f'''```{top_users}```''', colour = discord.Colour.from_rgb(230,0,0))
				embed.set_footer(text=f'ToxBot Members')
				await ctx.send(embed=embed)
			except Exception as e:
				await ctx.send(str(e))


	else:
		print('Something wrong')