import discord
import asyncio
import random
from datetime import datetime
from core.toxbot_core import print_log, send_embed

def mv(bot, manager_data):
	class mv_pl:
		def __init__(self, manager_data):
			self.name 	= 'member_voices'
			self.ver 	= '0.0.1'
			self.require= []
			self.loaded = False
			manager_data.plugins_counter+=1
			print_log('wait', '\tОжидание: Загрузка модуля пользовательских войсов')
			print_log('info', '\tУспех: Модуль пользовательских войсов загружен\n')
			self.loaded = True
			manager_data.loaded_plugins.update({self.name : self.ver})


	plugin = mv_pl(manager_data)

	if plugin.loaded:
		@bot.event
		async def on_voice_state_update(member, before, after):
			if after.channel != None:
				if 'Создать' in after.channel.name:
					maincategory = after.channel.category
					channel2 = await member.guild.create_voice_channel(
						f'🔉┃{member.display_name}',
						position=3,
						category=maincategory,
						bitrate=96000,
						reason=f"Создался войс для {member}"
					)
					await channel2.set_permissions(member, connect=True, mute_members=True, move_members=True, manage_channels=True)
					await member.move_to(channel2)
					def check(x, y, z):
						return len(channel2.members) == 0
					await bot.wait_for('voice_state_update', check=check)
					await channel2.delete()
