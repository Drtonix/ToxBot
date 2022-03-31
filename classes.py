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
UsTaCr = UserTableCreate()
