import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('Poor_Warrior_of_Christ.db')
cursor = conn.cursor()

class UserTableCreate:
	def member(self, ctx, member):
		cursor.execute("SELECT id FROM economy WHERE id=?", (member.id,))
		if cursor.fetchone() == None:
		 	cursor.execute('INSERT INTO economy VALUES (?, ?)', (member.id, 0))
		else:
			pass
		conn.commit()
	def author(self, ctx):
		cursor.execute("SELECT id FROM economy WHERE id=?", (ctx.author.id,))
		if cursor.fetchone() == None:
			cursor.execute('INSERT INTO economy VALUES (?, ?)', (ctx.author.id, 0))
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
