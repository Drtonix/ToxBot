import discord
from discord.ext import commands
import sqlite3
from core.toxbot_core import print_log, send_embed
conn = sqlite3.connect('Poor_Warrior_of_Christ.db')
cursor = conn.cursor()

class UserTableCreate:
	def member(self, ctx, member):
		cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (member.id, ctx.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (member.id, 100, ctx.guild.id))
			return
		else:
			pass
		conn.commit()
	def author(self, ctx):
		cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (ctx.author.id, ctx.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (ctx.author.id, 100, ctx.guild.id))
			return
		else:
			pass
		conn.commit()
	def message(self, message):
		cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (message.author.id, 100, message.guild.id))
			return
		else:
			pass
	def expm(self, ctx, member):
		cursor.execute("SELECT exp FROM levels WHERE id=? AND guild_id=?", (member.id, ctx.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO levels VALUES (?, ?, ?, ?)', (member.id, 0, 0, ctx.guild.id))
			return
		else:
			pass
		conn.commit()
	def expa(self, message):
		cursor.execute("SELECT exp FROM levels WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO levels VALUES (?, ?, ?, ?)', (message.author.id, 0, 0, message.guild.id))
			return
		else:
			pass
		conn.commit()
	
	def switch(self, message):
		cursor.execute("SELECT id FROM switches WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO switches VALUES (?, ?, ?)', (message.author.id, 0, message.guild.id))
			return
		else:
			pass
		conn.commit()

	def switchc(self, ctx):
		cursor.execute("SELECT id FROM switches WHERE id=? AND guild_id=?", (ctx.author.id, ctx.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO switches VALUES (?, ?, ?)', (ctx.author.id, 0, ctx.guild.id))
			return
		else:
			pass

	def expam(self, message):
		cursor.execute("SELECT exp FROM levels WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO levels VALUES (?, ?, ?, ?)', (message.author.id, 0, 0, message.guild.id))
		else:
			pass
		conn.commit()
		cursor.execute("SELECT id FROM economy WHERE id=? AND guild_id=?", (message.author.id, message.guild.id))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO economy VALUES (?, ?, ?)', (message.author.id, 100, message.guild.id))
		else:
			pass
		conn.commit()
class ServerTableCreate:
	def create(self, ctx):
		cursor.execute("SELECT id FROM admininfo WHERE id=?", (ctx.guild.id,))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO admininfo VALUES (?, ?)', (ctx.guild.id, 0))
		else:
			pass
		conn.commit()
	def creeate(self, member):
		cursor.execute("SELECT id FROM admininfo WHERE id=?", (member.guild.id,))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO admininfo VALUES (?, ?)', (member.guild.id, 0))
		else:
			pass
		conn.commit()
SeTaCr = ServerTableCreate()
UsTaCr = UserTableCreate()
