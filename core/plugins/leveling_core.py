import discord
import asyncio
import random
from datetime import datetime
from core.toxbot_core import print_log, send_embed

def level_core(bot, manager_data):
	class lvl_core:
		def __init__(self, manager_data):
			self.name 	= 'level_core'
			self.ver 	= 'v0.6.9a build 69'
			self.require= ['DB_Core', 'economy_core']
			self.loaded = False
			manager_data.plugins_counter+=1
			print_log('wait', '\tОжидание: Загрузка модуля левлелинга')
			print_log('bank', '\t\tВыполняется: Проверка наличия зависимостей модуля')
			try:
				from core.plugins.database_core import db, UsTaCr, SeTaCr
				global db, UsTaCr, SeTaCr
				if self.require[0] in manager_data.loaded_plugins:
					if self.require[1] in manager_data.loaded_plugins:
						print_log('bank', '\t\tВыполняется: Проверка наличия таблицы уровней')
						try:
							db.cursor.execute('''CREATE TABLE IF NOT EXISTS levels (
							"id"	INT,
							"level"	INT,
							"exp"	INT,
							"guild_id"	INT)''')
							self.loaded = True
							manager_data.loaded_plugins.update({self.name : self.ver})
							print_log('info', '\tУспех: Модуль левлелинга инициализирован\n')
						except Exception as e:
							print_log('err', '\tОшибка загрузки модуля: ' + str(e) + '\n')
					else:
						print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[1]}. Плагин может работать некоректно.\n')
				else:
					print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[0]}. Плагин может работать некоректно.\n')
			except:
				print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[0]}. Плагин может работать некоректно.\n')

	plugin = lvl_core(manager_data)
	if plugin.loaded:
		@bot.event
		async def on_message(message):
			if message.author.bot:
				return
			if message.content.startswith("$") or message.content.startswith("!") or message.content.startswith(".") or message.content.startswith("++"):
				await bot.process_commands(message)
				return
			else:
				try:
					UsTaCr.expa(message)
					mlength = len(message.content)
					if mlength > 4:
						row1 = 0
						for row in db.cursor.execute(f'SELECT "exp" FROM levels WHERE id={message.author.id} AND guild_id={message.guild.id}'):
							if mlength > 64:
								orow1 = int(row[0])
								row1 = int(row[0]) + random.randint(1, 64)
							else:
								orow1 = int(row[0])
								row1 = int(row[0]) + random.randint(1, mlength)
						db.cursor.execute(f'UPDATE levels SET exp = {row1} WHERE id={message.author.id} AND guild_id={message.guild.id}')
					limit = 8
					multiply = 3
					for row in db.cursor.execute(f'SELECT "level" FROM levels WHERE id={message.author.id} AND guild_id={message.guild.id}'):
						for level in range(row[0]):
							multiply += 3
						for level in range(row[0]):
							limit = limit * multiply
					for row in db.cursor.execute(f'SELECT "exp" FROM levels WHERE id={message.author.id} AND guild_id={message.guild.id}'):
						if row[0] >= limit:
							row2 = 0
							for row in db.cursor.execute(f'SELECT "level" FROM levels WHERE id={message.author.id} AND guild_id={message.guild.id}'):
								orow2 = int(row[0])
								row2 = int(row[0]) + 1
							db.cursor.execute(f'UPDATE levels SET level = {row2} WHERE id={message.author.id} AND guild_id={message.guild.id}')
							db.conn.commit()
							UsTaCr.message(message)
							row3 = 0
							for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id={message.author.id} AND guild_id={message.guild.id}'):
								orow3 = int(row[0])
								row3 = int(row[0]) + 20
							db.cursor.execute(f'UPDATE economy SET money = {row3} WHERE id={message.author.id} AND guild_id={message.guild.id}')
							db.conn.commit()
							UsTaCr.switch(message)
							for row in db.cursor.execute(f'SELECT "msgs" FROM switches WHERE id={message.author.id} AND guild_id={message.guild.id}'):
								row4 = int(row[0])
							if row4 == 1:
								await send_embed(message.author,
									f"Вы повысили уровень на сервере {message.guild.name}!",
									f"Вы получили новый уровень! Ваш уровень теперь {row2}!",
									f"ToxBot Level System {plugin.ver}",
									message.guild.icon_url)
							elif row4 == 0:
								await send_embed(message.channel,
									f"Пользователь {message.author.display_name} повысил уровень!", 
									f"Теперь у него {row2} уровень!", 
									f"ToxBot Level System {plugin.ver}")
							else:
								pass
				except Exception as e:
					print_log('warn', str(e))
			await bot.process_commands(message)
	
		@bot.command(aliases = ["уровень", "level"])
		async def lvl(ctx, member: discord.Member = None):
			if member is None:
				for row in db.cursor.execute(f'SELECT row_number() over(order by exp desc), id, exp, level FROM levels WHERE guild_id = {ctx.guild.id} ORDER BY exp DESC'):
					if row[1] == ctx.author.id:
							await send_embed(ctx,
								f"Уровень {ctx.author.display_name}", 
								f"Ваш Уровень - `{row[3]}`\nВаш опыт - `{row[2]} exp`\nВаше место в топе - `{row[0]}`", 
								f"ToxBot Level System {plugin.ver}")
			else:
				for row in db.cursor.execute(f'SELECT row_number() over(order by exp desc), id, exp, level FROM levels WHERE guild_id = {ctx.guild.id} ORDER BY exp DESC'):
					if row[1] == member.id:
						await send_embed(ctx,
								f"Уровень {member.display_name}", 
								f"Пользователь находится на `{row[3]}` уровне\nЕго опыт - `{row[2]} exp`\nМесто в топе - `{row[0]}`", 
								f"ToxBot Level System {plugin.ver}")

		@bot.command(aliases = ["Уведомления"])
		async def messages(ctx, choice: int = None):
			if choice is None:
				await send_embed(ctx, "Пожалуйста, выберите что-то.", "0 - Уведомления в чат\n1 - Уведомления в лс\n2 - Без уведомлений", f"ToxBot Level System {plugin.ver}", None)
			else:
				UsTaCr.switchc(ctx)
				if choice == 1:
					db.cursor.execute(f'UPDATE switches SET msgs = {choice} WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}')
					await send_embed(ctx, "Успешно!", "Включены уведомления в личные сообщения.", f"ToxBot Level System {plugin.ver}", None)
				elif choice == 2:
					db.cursor.execute(f'UPDATE switches SET msgs = {choice} WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}')
					await send_embed(ctx, "Успешно!", "Уведомления выключены.", f"ToxBot Level System {plugin.ver}", None)
				elif choice == 0:
					db.cursor.execute(f'UPDATE switches SET msgs = {choice} WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}')
					await send_embed(ctx, "Успешно!", "Включены уведомления в чат.", f"ToxBot Level System {plugin.ver}", None)
				else:
					await ctx.send("возможно вы ввели не то что требуется.")
				db.conn.commit()
