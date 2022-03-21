##############################################
#            YouTube for ToxBot              #
#				v.0.4.1 rev B 	             #
#		(Powered by Ampernic and Wiskey)     #
#	   Copyright BetaNet Team © 2018-2022    #
#				   FreeWare					 #
##############################################
#	   Fucked by AxisShevc (Ampernicsa)      #
#  	 Передам привет нытикам говнокодерам     #	Ampernic, Wiskey, Ampernicsa
##############################################			  / __\ ___| |_ __ _  /\ \ \___| |_  /__   \___  __ _ _ __ ___  
#	       Дмитрий Гудков это ложь :3        #			 /__\/// _ \ __/ _` |/  \/ / _ \ __|   / /\/ _ \/ _` | '_ ` _ \ 
#			Вселенная голограмма.            #			/ \/  \  __/ || (_| / /\  /  __/ |_   / / |  __/ (_| | | | | | |
#		   Скупайте золото в Sunlight.		 #			\_____/\___|\__\__,_\_\ \/ \___|\__|  \/   \___|\__,_|_| |_| |_|
##############################################																		2018-2022
# Мені пiхуй отсосите, я живу в іншому місті #
#			 Що ви мені зробите?             #
##############################################
#           Last update: 03/21/2022          #
##############################################

from discord import FFmpegPCMAudio, Activity, ActivityType
from core.toxbot_core import *
from core.toxbot_core_texts	import *
import yt_dlp
import asyncio

global YDL_OPTIONS
global FFMPEG_OPTIONS

YDL_OPTIONS = {'format': 'worstaudio/best',
					'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio', 'quiet': 'True', "external_downloader_args": ['-loglevel', 'panic']}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

##############################################            Не спиздили у вексеры, а адаптировали
#              	    Рамки                    #											(С) Дмитрий Гудков 2018
##############################################

def emd_play(discord, track, time, logo, nick, type):
    embed = discord.Embed(title=type, colour = discord.Colour.from_rgb(230,0,0))
    embed.set_thumbnail(url=logo)
    embed.add_field(name="Трек: ", value=track, inline=False)
    embed.add_field(name="Длительность: ", value=time, inline=False)
    embed.set_footer(text="Запрошено пользователем: " + nick + " | ToxBot", icon_url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
    return embed

##############################################
#              	    Поиск                    #
##############################################

@asyncio.coroutine
async def yt_searching(ctx, discord, track_name, q, notfy):
	with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
				try:
					info = ydl.extract_info(track_name, download=False)
				except:
					try:
						info = ydl.extract_info(f"ytsearch:{track_name}", download=False)['entries'][0]
					except Exception as e:
						await notfy(ctx, "Трек не найден (" + e + ").")
				URL = info['formats'][4]['url']
				tname = info['title']
				tdure = info['duration_string']
				taut = ctx.message.author.name
				ttubn = info['thumbnail']
				q.append([URL, tname, tdure, taut, ttubn])
				if(len(q) > 1):
					try:
						await ctx.send(embed=emd_play(discord, tname, tdure, ttubn, taut, "Добавленно в очередь: "))
					except Exception as e:
						await notfy(ctx, e)

##############################################
#             Включение треков               #
##############################################
@asyncio.coroutine
async def yt_play(discord, bot, data, print_log, notfy):

	#             -Общие переменные-             #

	voice_client = None
	loop_now = None
	q_now = 0
	q = []

	#     -Включить/Добавить в очередь трек-     #

	@bot.command(pass_context=True)
	async def p(ctx, *,messaget=None):
		try:
			if(messaget != None):
				try:
					nonlocal voice_client
					voice_channel = ctx.message.author.voice.channel
					voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
					await yt_searching(ctx, discord, messaget, q, notfy)
					if(len(q) == 1):
						if voice_client:
							try:
								voice_client.pause()
								if(data["OS"]==1):
									await ctx.send(embed=emd_play(discord, q[q_now][1], q[q_now][2], q[q_now][4], q[q_now][3], "Включено: "))
									print_log("info", "Включен трек: {} | (Запросил: {})".format(q[q_now][1], q[q_now][3]))
								elif(data["OS"]==0):
									voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = q[q_now][0], **FFMPEG_OPTIONS))
									await ctx.send(embed=emd_play(discord, q[q_now][1], q[q_now][2], q[q_now][4], q[q_now][3], "Включено: "))
									print_log("info", "Включен трек: {} | (Запросил: {})".format(q[q_now][1], q[q_now][3]))
								
								if(voice_client == None):														# It just works, It just works, Fucking bugs..... Everything sucks.... (Ampernicsa)
									voice_client=discord.utils.get(bot.voice_clients, guild=ctx.guild)          # Эта хуйня просто работает и не позволяет коду высыпать ошибками... Хз почему он ее не видит, хотя выше обращается к ней спокойно....

								while voice_client.is_playing():
									await asyncio.sleep(1)
								await skip(ctx)
							except Exception as e:
								await notfy(ctx, e)
						else:
							try:
								player = await voice_channel.connect()
								if(data["OS"]==1):
									player.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source = q[q_now][0], **FFMPEG_OPTIONS))
									await ctx.send(embed=emd_play(discord, q[q_now][1], q[q_now][2], q[q_now][4], q[q_now][3], "Включено: "))
									print_log("info", "Включен трек: {} | (Запросил: {})".format(q[q_now][1], q[q_now][3]))
								elif(data["OS"]==0):
									player.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = q[q_now][0], **FFMPEG_OPTIONS))
									await ctx.send(embed=emd_play(discord, q[q_now][1], q[q_now][2], q[q_now][4], q[q_now][3], "Включено: "))
									print_log("info", "Включен трек: {} | (Запросил: {})".format(q[q_now][1], q[q_now][3]))

								if(voice_client == None):													# Опять эта же хуйня...
									voice_client=discord.utils.get(bot.voice_clients, guild=ctx.guild)		# Все те же грабли)

								while voice_client.is_playing():
									await asyncio.sleep(1)
								await skip(ctx)
							except Exception as e:
								await notfy(ctx, e)
				except:
					await ctx.send(f"Невозможно подключить бота: Вы не в голосовом чате.")
					print_log("warn", "Ошибка воспроизведения: " + ctx.message.author.name + " не в голосовом чате")
			else:
				await ctx.send(f"Введите название трека!")
				print_log("warn", "Ошибка воспроизведения: " + ctx.message.author.name + " не указал трек.")
		except Exception as e:
			await notfy(ctx, e)

	#     -Переключение треков-     #

	@bot.command(pass_context=True)
	async def skip(ctx):
		nonlocal loop_now
		nonlocal q_now
		nonlocal q
		nonlocal voice_client
		if(voice_client != None):
			if(loop_now == None or loop_now == 'all'):
				if(q_now <= len(q)-1):
					q_now+=1
			elif(loop_now == 'one'):
				pass

			if(loop_now == "all" and q_now > len(q)-1):
				q_now = 0

			if(q_now <= len(q)-1):
				voice_client.pause()
				if(data["OS"]==1):
					voice_client.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source = q[q_now][0], **FFMPEG_OPTIONS))
					await ctx.send(embed=emd_play(discord, q[q_now][1], q[q_now][2], q[q_now][4], q[q_now][3], "Сейчас играет: "))
					print_log("info", "Сейчас играет: {} | (Запросил: {})".format(q[q_now][1], q[q_now][3]))
				elif(data["OS"]==0):
					voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = q[q_now][0], **FFMPEG_OPTIONS))
					await ctx.send(embed=emd_play(discord, q[q_now][1], q[q_now][2], q[q_now][4], q[q_now][3], "Сейчас играет: "))
					print_log("info", "Сейчас играет: {} | (Запросил: {})".format(q[q_now][1], q[q_now][3]))

				if(voice_client == None):													# Не буду это комментировать
					voice_client=discord.utils.get(bot.voice_clients, guild=ctx.guild)		# Просто работает
					
				while voice_client.is_playing():
					await asyncio.sleep(1)
				await skip(ctx)
			else:
				if voice_client:
					await stop(ctx)
		else:
			await ctx.send("Невозможно переключить трек. Бот ничего не играет.")
			print_log('warn', "Ошибка воспроизведения: Шизойд (" + ctx.message.author.name + ") переключил трек на выключенном воспроизведении")

	#     -Остановка треков-     #

	@bot.command()
	async def stop(ctx):
		try:
			nonlocal voice_client
			nonlocal q_now
			nonlocal q
			if(voice_client != None):
				await voice_client.disconnect()
				q = []
				q_now = 0
				await ctx.send("Воспроизведение остановленно.")
				print_log('wait', "Воспроизведение остановленно: прерванно по команде от " + ctx.message.author.name)
				voice_client = None
			else:
				await ctx.send("Невозможно остановить воспроизведение: Бот ничего не играет.")
				print_log('warn', "Ошибка воспроизведения: Шизойд (" + ctx.message.author.name + ") использовал стоп на выключенном воспроизведении")
		except Exception as e:
			await notfy(ctx, e)

	#    -Управление очередью-   #

	@bot.command()
	async def rpl(ctx, args=None):
		nonlocal loop_now
		if(args == None):
			await ctx.send('Укажите режим повтора!')
			print_log('warn', "Ошибка воспроизведения: Шизойд (" + ctx.message.author.name + ") опять забыл указать режим")
		else:
			if(args == 'all'):
				await ctx.send('Повтор включен: Все треки')
				loop_now = args
				print_log('wait', ctx.message.author.name + " включил повтор всей очереди.")
			elif(args == 'one'):
				await ctx.send('Повтор включен: Один трек')
				loop_now = args
				print_log('wait', ctx.message.author.name + " включил повтор одного трека.")
			elif(args == 'off'):
				await ctx.send('Повтор выключен.')
				loop_now = None
				print_log('wait', ctx.message.author.name + " выключил повтор.")




##############################################################     Ampernicsa (3/19/2022)
#  Всю эту хуйню надо будет переписать, но сука, пусть этим  #			-Okay (Ampernic 3/20/2022)
#             Занимается Ампер сука. Я заебалась:3           #				-Ага, выебывайся дальше) (Ampernicsa 3/20/2022)
##############################################################

#----------------------------------------------------------------------------------------------------------------------------------#
										#- BetaNet Clowns 2022. Everything sucks. -#