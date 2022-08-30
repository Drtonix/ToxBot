import discord
from discord.ext import commands
import sqlite3
from core.toxbot_core import print_log, send_embed

def DB_Core(manager_data):
	class DB_Core:
		def __init__(self, manager_data):
			self.name = 'DB_Core'
			self.ver = '0.1.3s'
			manager_data.plugins_counter+=1
			print_log('wait', '\tОжидание: Загрузка модуля базы данных')
			print_log('bank', '\t\tВыполняется: Проверка наличия базы / Создание базы')
			self.conn = sqlite3.connect('Poor_Warrior_of_Christ.db')
			self.cursor = self.conn.cursor()
			try:
				self.cursor.execute('''CREATE TABLE IF NOT EXISTS admininfo (
					"id"	INT,
					"welcomeid"	INT)''')
				self.cursor.execute('''CREATE TABLE IF NOT EXISTS levels (
					"id"	INT,
					"level"	INT,
					"exp"	INT,
					"guild_id"	INT)''')
				self.cursor.execute('''CREATE TABLE IF NOT EXISTS switches (
					"id"	INT,
					"msgs"	INT,		
					"guild_id"	INT)''') #0 - сообщения в лс, 1 - сообщение в чат, 2 - отключенные сообщения
				print_log('info', '\tУспех: Модуль базы данных инициализирован\n')
				manager_data.loaded_plugins.update({self.name : self.ver})
			except Exception as e:
				print_log('err', '\tОшибка загрузки модуля: ' + str(e) + '\n')

	global db 
	db = DB_Core(manager_data)

class UserTableCreate:
	def member(self, ctx, member):
		db.cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (member.id, ctx.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (member.id, 100.00, ctx.guild.id))
			return
		else:
			pass
		db.conn.commit()
	def author(self, ctx):
		db.cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (ctx.author.id, ctx.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (ctx.author.id, 100.00, ctx.guild.id))
			return
		else:
			pass
		db.conn.commit()
	def message(self, message):
		db.cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (message.author.id, 100.00, message.guild.id))
			return
		else:
			pass
	def expm(self, ctx, member):
		db.cursor.execute("SELECT exp FROM levels WHERE id=? AND guild_id=?", (member.id, ctx.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO levels VALUES (?, ?, ?, ?)', (member.id, 0, 0, ctx.guild.id))
			return
		else:
			pass
		db.conn.commit()
	def expa(self, message):
		db.cursor.execute("SELECT exp FROM levels WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO levels VALUES (?, ?, ?, ?)', (message.author.id, 0, 0, message.guild.id))
			return
		else:
			pass
		db.conn.commit()
	
	def switch(self, message):
		db.cursor.execute("SELECT id FROM switches WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO switches VALUES (?, ?, ?)', (message.author.id, 0, message.guild.id))
			return
		else:
			pass
		db.conn.commit()

	def switchc(self, ctx):
		db.cursor.execute("SELECT id FROM switches WHERE id=? AND guild_id=?", (ctx.author.id, ctx.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO switches VALUES (?, ?, ?)', (ctx.author.id, 0, ctx.guild.id))
			return
		else:
			pass

	def expam(self, message):
		db.cursor.execute("SELECT exp FROM levels WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO levels VALUES (?, ?, ?, ?)', (message.author.id, 0, 0, message.guild.id))
		else:
			pass
		db.conn.commit()
		db.cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (message.author.id, 100.00, message.guild.id))
		else:
			pass
		db.conn.commit()
class ServerTableCreate:
	def create(self, ctx):
		db.cursor.execute("SELECT id FROM admininfo WHERE id=?", (ctx.guild.id,))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO admininfo VALUES (?, ?)', (ctx.guild.id, 0))
		else:
			pass
		db.conn.commit()
	def creeate(self, member):
		db.cursor.execute("SELECT id FROM admininfo WHERE id=?", (member.guild.id,))
		if db.cursor.fetchone() == None:
			db.cursor.execute('INSERT INTO admininfo VALUES (?, ?)', (member.guild.id, 0))
		else:
			pass
		db.conn.commit()
SeTaCr = ServerTableCreate()
UsTaCr = UserTableCreate()
