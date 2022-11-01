import discord
import asyncio
import random

from datetime import datetime
from Cybernator import Paginator as Pag
from core.toxbot_core import print_log, send_embed

def mmbr_inv(bot, manager_data):
	class mmbr_inv:
		def __init__(self, manager_data):
			self.name 	= 'members_inventory'
			self.ver 	= 'v0.0.1 build 1'
			self.require= ['DB_Core', 'economy_core']
			self.loaded = False
			manager_data.plugins_counter+=1
			print_log('wait', '\tОжидание: Загрузка модуля системы предметов')
			print_log('bank', '\t\tВыполняется: Проверка наличия зависимостей модуля')
			try:
				from core.plugins.database_core import db, UsTaCr, SeTaCr
				global db, UsTaCr, SeTaCr
				if self.require[0] in manager_data.loaded_plugins:
					if self.require[1] in manager_data.loaded_plugins:
						print_log('bank', '\t\tВыполняется: Проверка наличия таблицы инвентарей')
						try:
							db.cursor.execute('''CREATE TABLE IF NOT EXISTS inventories (
								"seller_id"	INT,
								"byer_id"	INT,
								"item_name"	VARCHAR,
								"item_id"	INT,
								"cost"	DOUBLE,
								"comment"	VARCHAR,
								"date"		VARCHAR)''')
						except Exception as e:
							print(str(e))
						self.loaded = True
						manager_data.loaded_plugins.update({self.name : self.ver})
						print_log('info', '\tУспех: Модуль системы предметов инициализирован\n')
					else:
						print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[1]}. Плагин может работать некоректно.\n')
				else:
					print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[0]}. Плагин может работать некоректно.\n')
			except:
				print_log('warn', f'\tПредупреждение: Не найдена зависимость {self.require[0]}. Плагин может работать некоректно.\n')

	plugin = mmbr_inv(manager_data)

	@bot.command()
	async def inv(ctx, member:discord.Member = None):
		try:
			if member == None:
				member = ctx.author
			global p
			p= 'Купленные предметы\n```'
			for row in db.cursor.execute(f'SELECT item_id, seller_id, byer_id, item_name, comment, cost, date FROM inventories WHERE byer_id = {member.id} ORDER BY item_id DESC'):
				await ctx.send(row)
				item_id=row[0]
				seler_name=await bot.fetch_user(row[1]);seler_name=seler_name.display_name
				byer_name=await bot.fetch_user(row[2]);byer_name=byer_name.display_name
				item_name=row[3]
				item_description = row[4]
				item_cost=row[5]
				buy_date=row[6]
				p = p+f'Лот: {item_id}\n\tПредмет: {item_name}\n\tОписание: {item_description}\n\tКуплен у {seler_name} за {item_cost} TXC, {buy_date}'
			if 'Лот' not in p:
				p=p+'Отсутствует'
			p=p+'```'
			await ctx.send(p)
		except Exception as e:
			await ctx.send(str(e))

