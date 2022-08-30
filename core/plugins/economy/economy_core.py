import discord
import asyncio
import random
from datetime import datetime
from core.toxbot_core import print_log, send_embed


def EcoCore(bot, manager_data):
	class EcoCore:
		def __init__(self, manager_data):
			self.name = 'economy_core'
			self.ver = '0.1.3d'
			self.require = 'DB_Core'
			self.loaded = False
			manager_data.plugins_counter+=1
			print_log('wait', '\tОжидание: Загрузка ядра модуля экономики')
			print_log('bank', '\t\tВыполняется: Проверка наличия зависимостей модуля')
			try:
				from core.plugins.database_core import db, UsTaCr, SeTaCr
				global db, UsTaCr, SeTaCr
				if self.require in manager_data.loaded_plugins:
					print_log('bank', '\t\tВыполняется: Проверка наличия таблицы экономики')
					try:
						db.cursor.execute('''CREATE TABLE IF NOT EXISTS eco_history (
							"user_id"	INT,
							"end_id"	INT,
							"guild_id"	INT,
							"type"		VARCHAR,
							"bal_start"	DOUBLE,
							"bal_end"	DOUBLE,
							"comment"	VARCHAR,
							"date"		VARCHAR)''')
						db.cursor.execute('''CREATE TABLE IF NOT EXISTS economy (
								"id"	INT,
								"money"	DOUBLE,
								"guild_id"	INT)''')
						print_log('info', '\tУспех: Модуль ядра экономики инициализирован\n')
						self.loaded = True
						manager_data.loaded_plugins.update({self.name : self.ver})
					except Exception as e:
						print_log('err', '\tОшибка загрузки модуля: ' + str(e) + '\n')
				else:
					print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require}. Плагин может работать некоректно.\n')
			except:
				print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require}. Плагин может работать некоректно.\n')

		async def get_history(self, ctx, member, author):
			try:
				for row in db.cursor.execute(f'''SELECT * FROM eco_history WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}'''):
					client = discord.Client()
					payer = await ctx.guild.fetch_member(row[1])
					if row[6] != 'None':
						comm = '\n\tКомментарий: '+ row[6]
					else:
						comm = ''
					if row[3] == 'in_pay':
						return '[+] Перевод от: {}\n\tСумма: {} TXC\n\tДата: {}{}'.format(payer.display_name,round(row[5]-row[4],2),row[7], comm)
					elif row[3] == 'out_pay':
						return '[-] Перевод для: {}\n\tСумма: {} TXC\n\tДата: {}{}'.format(payer.display_name,round(row[5]-row[4],2),row[7], comm)
					elif row[3] == 'deposit':
						return '[+] Пополнение от: {}\n\tСумма: {} TXC\n\tДата: {}{}'.format(payer.display_name,round(row[5]-row[4],2),row[7], comm)
					elif row[3] == 'withdraw':
						return '[-] Конфисковано: {}\n\tСумма: {} TXC\n\tДата: {}{}'.format(payer.display_name,round(row[5]-row[4],2),row[7], comm)
				if db.cursor.fetchone() == None:
					return 'С этого счета еще небыло операций'
			except Exception as e:
					return 'Не удалось получить информацию' + str(e)

		async def save_history(self, ctx, send_to, sender, type, send_bal_start, send_bal_end,sender_bal_start, sender_bal_end, comment, date):
			try:
				# Обрабока истории переводов
				if type == 'send':
					# Сначала сохраним историю получателя
					db.cursor.execute(f'''SELECT * FROM eco_history WHERE user_id = {send_to} AND guild_id = {ctx.guild.id}''')
					if db.cursor.fetchone() == None:
						db.cursor.execute('INSERT INTO eco_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (send_to, sender, ctx.guild.id, 'in_pay', send_bal_start, send_bal_end, comment, date))
					else:
						db.cursor.execute(f'''UPDATE eco_history SET 
							end_id = {sender},
							type 		= "in_pay",
							bal_start 	= {send_bal_start},
							bal_end 	= {send_bal_end},
							comment 	= "{comment}",
							date 		= "{date}"
							WHERE user_id={send_to} AND guild_id={ctx.guild.id}''')
					# Сохраним историю отправителя
					db.cursor.execute(f'''SELECT * FROM eco_history WHERE user_id = {sender} AND guild_id = {ctx.guild.id}''')
					if db.cursor.fetchone() == None:
						db.cursor.execute('INSERT INTO eco_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (sender, send_to, ctx.guild.id, 'out_pay', sender_bal_start, sender_bal_end, comment, date))
					else:
						db.cursor.execute(f'''UPDATE eco_history SET 
							end_id = {send_to},
							type 		= "out_pay",
							bal_start 	= {sender_bal_start},
							bal_end 	= {sender_bal_end},
							comment 	= "{comment}",
							date 		= "{date}"
							WHERE user_id={sender} AND guild_id={ctx.guild.id}''')
				if type == 'deposit':
					db.cursor.execute(f'''SELECT * FROM eco_history WHERE user_id = {send_to} AND guild_id = {ctx.guild.id}''')
					if db.cursor.fetchone() == None:
						db.cursor.execute('INSERT INTO eco_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (send_to, sender, ctx.guild.id, 'deposit', send_bal_start, send_bal_end, comment, date))
					else:
						db.cursor.execute(f'''UPDATE eco_history SET 
							end_id = {sender},
							type 		= "deposit",
							bal_start 	= {send_bal_start},
							bal_end 	= {send_bal_end},
							comment 	= "{comment}",
							date 		= "{date}"
							WHERE user_id={send_to} AND guild_id={ctx.guild.id}''')
				if type == 'withdraw':
					db.cursor.execute(f'''SELECT * FROM eco_history WHERE user_id = {send_to} AND guild_id = {ctx.guild.id}''')
					if db.cursor.fetchone() == None:
						db.cursor.execute('INSERT INTO eco_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (send_to, sender, ctx.guild.id, 'withdraw', send_bal_start, send_bal_end, comment, date))
					else:
						db.cursor.execute(f'''UPDATE eco_history SET 
							end_id = {sender},
							type 		= "withdraw",
							bal_start 	= {send_bal_start},
							bal_end 	= {send_bal_end},
							comment 	= "{comment}",
							date 		= "{date}"
							WHERE user_id={send_to} AND guild_id={ctx.guild.id}''')
			except Exception as e:
				print(e)
				await ctx.send(str(e))


	plugin = EcoCore(manager_data)

	if plugin.loaded:
		@bot.command(aliases = ["баланс", "деньги", "bal"])
		async def balance(ctx, member: discord.Member = None):
			try:
				if member is None:
					UsTaCr.author(ctx)
					for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}'):
						await send_embed(ctx, '💵 Выписка по счету 💵', f"Пользователь: `{ctx.author.display_name}`\nБаланс: `{row[0]} TXC`\n\n```bash\n{await plugin.get_history(ctx, ctx.author, ctx.author)}```", f"Банк ToxBot\nВыписка от {datetime.now().strftime('%x %H:%M:%S')}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
				else:
					if not member.bot:
						UsTaCr.member(ctx, member)
						for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id = {member.id} AND guild_id = {ctx.guild.id}'):
							await send_embed(ctx, '💵 Выписка по счету 💵', f"Пользователь: `{member.display_name}`\nБаланс: `{row[0]} TXC`\n\n```bash\n{await plugin.get_history(ctx, member, ctx.author)}```", f"Банк ToxBot\nВыписка от {datetime.now().strftime('%x %H:%M:%S')}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
					else:
						await ctx.send('Боты не имеют счета.')
			except Exception as e:
				print_log('err', str(e))
				await ctx.send(str(e))

		@bot.command(aliases = ["wd", "забрать", "конфисковать", "списать"])
		async def withdraw(ctx, member: discord.Member = None, Value: float = None, *, message = None):
			try:
				if ctx.author.guild_permissions.administrator:
					if member is None:
						await ctx.send("Укажите цель!")
					elif member.bot:
						await ctx.send("Нельзя списать валюту у бота!")
					elif Value is not None and Value <= 0:
						await ctx.send("Нельзя списать 0 ТоксКоинов или меньше!")
					else:
						UsTaCr.author(ctx)
						UsTaCr.member(ctx, member)
						ebal = 0
						date = datetime.now().strftime('%x %H:%M:%S')
						for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id={member.id} AND guild_id={ctx.guild.id}'):
							ebal = row[0]

						if Value is None or ebal <= Value:
							Value = ebal

						db.cursor.execute(f'UPDATE economy SET money = {ebal-Value} WHERE id={member.id} AND guild_id={ctx.guild.id}')
						print_log('eco', f"{ctx.author.display_name} конфисковал у {member.display_name} {Value} TXC (Сервер: {ctx.guild.name})")
						if message is not None:
							message = message[:30]
							await plugin.save_history(ctx, member.id, ctx.author.id, 'withdraw', ebal, ebal-Value, 0, 0, message, date)
							await send_embed(ctx, "💵 Выполнено списание 💵", f"Администратор:\t`{ctx.author.display_name}`\nПользователь:\t`{member.display_name}`\nСписано со счета:\t`{Value} TXC`\nБаланс до списания:\t`{ebal} TXC`\nБаланс после списания:\t`{ebal - Value} TXC`\nКомментарий к операции:\t`{message}`", f"Банк ToxBot\nТранзакция от {date}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
						else:
							await plugin.save_history(ctx, member.id, ctx.author.id, 'withdraw', ebal, ebal-Value, 0, 0, message, date)
							await send_embed(ctx, "💵 Выполнено списание 💵", f"Администратор:\t`{ctx.author.display_name}`\nПользователь:\t`{member.display_name}`\nСписано со счета:\t`{Value} TXC`\nБаланс до списания:\t`{ebal} TXC`\nБаланс после списания:\t`{ebal - Value} TXC`", f"Банк ToxBot\nТранзакция от {date}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
						db.conn.commit()
				else:
					await ctx.send("Команда списания доступна только администраторам!")
			except Exception as e:
				await ctx.send(str(e))
			
		@bot.command(aliases = ["givec", "pay", "заплатить", "передать"])
		async def givecoins(ctx, member: discord.Member = None, Value: float = None, *, message = None):
			if member is None:
				await ctx.send("Укажите цель!")
			elif member.bot:
				await ctx.send("Невозможно выполнить перевод боту.")
			elif member.id == ctx.author.id:
				await ctx.send("Вы не можете отправить деньги самому себе")
			else:
				UsTaCr.author(ctx)
				UsTaCr.member(ctx, member)
				if Value is None:
					await ctx.send("Укажите количество ТоксКоинов!")
				elif Value <= 0:
					await ctx.send("Нельзя передать 0 ТоксКоинов или меньше!")
				elif member.bot:
					await ctx.send("Нельзя передать валюту боту!")
				else:
					ebal = 0
					for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}'):
						ebal = row[0]
					if ebal >= Value:
						for row in db.cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}'):
							orow1 = int(row[0])
							row1 = int(row[0]) - Value
						db.cursor.execute(f'UPDATE economy SET money = {row1} WHERE id={ctx.author.id} AND guild_id={ctx.guild.id}')
						for row4 in db.cursor.execute(f'SELECT money FROM economy WHERE id={member.id} AND guild_id={ctx.guild.id}'):
							orow2 = int(row4[0])
							row2 = int(row4[0]) + Value
						date = datetime.now().strftime('%x %H:%M:%S')
						db.cursor.execute(f'UPDATE economy SET money = {row2} WHERE id={member.id} AND guild_id={ctx.guild.id}')
						if message is not None:
							message = message[:30]
							try:
								await plugin.save_history(ctx, member.id, ctx.author.id, 'send', orow2, row2, orow1, row1, message, date)
							except Exception as e:
								await ctx.send(str(e))
							await send_embed(ctx, "💵 Перевод выполнен 💵", f"Отправитель:\t`{ctx.author.display_name}`\nПолучатель:\t`{member.display_name}`\nБаланс отправителя:\t`{row1} TXC`\nБаланс получателя:\t`{row2} TXC`\nКомментарий к переводу: `{message}`", f"Банк ToxBot\nТранзакция от {date}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
						else:
							try:
								await plugin.save_history(ctx, member.id, ctx.author.id, 'send', orow2, row2, orow1, row1, message, date)
							except Exception as e:
								await ctx.send(str(e))
							await send_embed(ctx, "💵 Перевод выполнен 💵", f"Отправитель:\t`{ctx.author.display_name}`\nПолучатель:\t`{member.display_name}`\nБаланс отправителя:\t`{row1} TXC`\nБаланс получателя:\t`{row2} TXC`", f"Банк ToxBot\nТранзакция от {date}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
						print_log('eco', f"{ctx.author.display_name} перевел пользователю {member.display_name} {Value} TXC (Сервер: {ctx.guild.name})")
						db.conn.commit()
					else:
						await ctx.send("Недостаточно денег!")

		@bot.command(aliases = ["bcontrol", "выдать", "балансконтроль", 'add', "addc"])
		async def addcoins(ctx, member: discord.Member = None, Value: float = None, *,message = None):
			try:
				if ctx.author.guild_permissions.administrator:
					if member is None:
						await ctx.send("Укажите цель!")
					elif member.bot:
						await ctx.send("Нельзя пополнить счет бота.")
					else:
						UsTaCr.author(ctx)
						UsTaCr.member(ctx, member)
						if Value is None:
							await ctx.send("Укажите количество ТоксКоинов!")
						elif Value <= 0:
							await ctx.send("Нельзя выдать 0 ТоксКоинов или меньше!")
						else:
							date = datetime.now().strftime('%x %H:%M:%S')
							ebal = 0
							for row in db.cursor.execute(f'SELECT money FROM economy WHERE id={member.id} AND guild_id={ctx.guild.id}'):
									orow2 = row[0]
									row2 = row[0] + Value
							if Value > 4294967295 or orow2 >= 4294967295:
								await ctx.send("В выдаче отказано! Значение слишком велико или вы достигли максимального баланса.")
							else:
								db.cursor.execute(f'UPDATE economy SET money = {row2} WHERE id={member.id} AND guild_id={ctx.guild.id}')
								if message is not None:
									message = message[:30]
									await plugin.save_history(ctx, member.id, ctx.author.id, 'deposit', orow2, row2, 0, 0, message, date)
									await send_embed(ctx, "💵 Выполнено пополнение 💵", f"Администратор:\t`{ctx.author.display_name}`\nПользователь:\t`{member.display_name}`\nПополнено на:\t`{Value} TXC`\nБаланс:\t`{row2} TXC`\nКомментарий к операции:\t`{message}`", f"Банк ToxBot\nТранзакция от {date}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
								else:
									await plugin.save_history(ctx, member.id, ctx.author.id, 'deposit', orow2, row2, 0, 0, message, date)
									await send_embed(ctx, "💵 Выполнено Пополнение 💵", f"Администратор:\t`{ctx.author.display_name}`\nПользователь:\t`{member.display_name}`\nПополнено на:\t`{Value} TXC`\nБаланс:\t`{row2} TXC`", f"Банк ToxBot\nТранзакция от {date}", 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')	
								print_log('eco', f"{ctx.author.display_name} пополнил баланс {member.display_name} на {Value} TXC (Сервер: {ctx.guild.name})")
								db.conn.commit()
				else:
					await ctx.send("Команда пополнения доступна только администраторам!")
			except Exception as e:
				print_log('err', str(e))
				await ctx.send(str(e))

		@bot.command()
		async def test(ctx, member: discord.Member = None):
			try:
				plugin.create(ctx, member.id, ctx.author.id)
			except Exception as e:
				await ctx.send(str(e))