import json
import sqlite3
import pytz
import random
import asyncio
import requests
from datetime import datetime
from Cybernator import Paginator as Pag
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import DiscordComponents
from classes import UsTaCr
from core.toxbot_core import *

# Переменные

data = None
init_successful = False
intents = discord.Intents.all()

# Инициализация

init()
print(header_logo)
print_log('wait', "Ожидание:  Инициализация")
try:
	data = core_parse_data(data)
	print_log('wait', "Импорт значений из конфига.")
	if data["FirstBoot"] == "True":
		print_log('warn', "Обнаружен первый запуск программы:  Переходим в режим настройки")
		first_boot_cofigure(data)
	else:
		bot = Bot(command_prefix="++", help_command=None, intents=intents)
		client = discord.ext.commands.Bot(command_prefix="++", intents=discord.Intents.all())
		init_successful = True
		if init_successful:
			print_log('info', "Инициализация прошла успешно")
			try:
				print_log("wait", "Ожидание:  Запуск базы данных")
				conn = sqlite3.connect('Poor_Warrior_of_Christ.db')
				cursor = conn.cursor()
				cursor.execute('''CREATE TABLE IF NOT EXISTS economy (
					"id"	INT,
					"money"	INT)''')
				print_log("info", "База данных загружена.")
			except Exception as e:
				print_log('err', "Ошибка базы данных: " + str(e))

		@bot.event
		async def on_ready():
			DiscordComponents(bot)
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="++help"))
			print_log("info", "Бот успешно cumming!")
except Exception as e:
	print_log('err', "Не удалось спарсить значения из конфига: " + str(e))

if init_successful:
	tz = pytz.timezone('Europe/Moscow')
	date = datetime.now(tz).strftime("%d%m")
	if date != "0104":
		@bot.command()
		async def ver(ctx):
			try:
				embed = discord.Embed(title="ToxBot {}!".format(num_ver), description=text_ver, colour=discord.Colour.from_rgb(230, 0, 0))
				embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
				msg = await ctx.send(embed=embed)
			except Exception as e:
				print_log('err', f'Ошибка: {e}')

		# Команды
		@bot.event
		async def on_member_join(member):
			await member.send('Добро пожаловать на сервер БДБ!\nСписок команд: ++help\nВы так же можете поддержать разработку бота: ++info')
			for ch in bot.get_guild(member.guild.id).channels:
				if ch.name == "💬┃био-отходняк-чат":
					await bot.get_channel(ch.id).send(f'Поздоровайтесь с новым участником Сервера, {member.display_name}!')
		@bot.event
		async def on_member_remove(member):
			for ch in bot.get_guild(member.guild.id).channels:
				if ch.name == "💬┃био-отходняк-чат":
					await bot.get_channel(ch.id).send(f'К сожалению, участник {member.display_name} покинул нас.')

		@bot.event
		async def on_voice_state_update(member, before, after):
			if after.channel != None:
				if after.channel.id == 964912138923700224:
					for guild in bot.guilds:
						maincategory = discord.utils.get(guild.categories, id=864965395312017449)
						channel2 = await guild.create_voice_channel(
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


		@bot.command()
		async def stats(ctx):
			members = ctx.guild.members
			online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
			idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
			offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
			dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
			all_members = online+idle+offline+dnd
			embed = discord.Embed(title="ToxBot", description=f'''\nОнлайн: {online}.\nОффлайн: {offline}.\nНеактивны: {idle}.\nНе беспокоить: {dnd}.\nВсего участников: {all_members}.''', colour = discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msg = await ctx.send(embed=embed)

		# help, info
		@bot.command()
		async def help(ctx):
			embed = discord.Embed(title="Используйте `++` перед \nначалом команды", description='''		
📌**Основное**
Инфо — `help`, `info`, `ver`
🎧**Воспроизведение**
Медиа — `p`, `loop`, `skip`, `stop`, `rstop`
Список радиостанций — `rlist`
🖼️**Работа с изображениями**
Фильтры — `shakal`
Создание фотокарточек — `dem`, `quote`
🎲**Игры и действия**
Действия — `kill`, `twisted`, `fuck`, `eat`, `give`, `call`
Казино игры — `roulette`, `coin`, `slots`
📚**Инфо и полезные штуки**
Инфо о пользователях — `stats`, `membinfo`
Полезные команды бота — `randomto`, `cal`, `time`, `laugh`, `yesorno`, `clear`
🔎**Поиск**
Поисковики — `google`, `yandex`, `duckduck`, `yahoo`''', colour = discord.Colour.from_rgb(230,0,0))
			strings = ["Попробуйте написать ++helpОсновное, ++helpВоспроизведение или тому подобное."]* 88 + ["Шуруп, забитый молотком, держится крепче, чем гвоздь, закрученный отвёрткой."]*1 +["Обувь будет носиться значительно дольше, если не покупать новую."]*1 + ["Если сосиски отварить с кубиком говяжьего бульона - то они будут пахнуть мясом."]*1 +["Большинство электрических приборов потребляют меньше электричества в выключенном состоянии."]*1 + ["Вегетарианский суп будет питательней, если в него положить немного говядины."]*1 +["Если ваш компьютер заразил вирус - как можно скорее переформатируйте ваш жесткий диск; не давайте вирусу удовольствие самому это сделать."]*1 + ["Если вы хотите приготовить дрожжевое тесто, но у вас нет дрожжей, то ни фига у вас не получится."]*1 +["Если ваш сосед внезапно купил ружье, вам лучше завязать с музыкой."]*1 + ["Нельзя смотреться в зеркало когда ешь - счастье своё проешь. И когда пьёшь - пропьёшь. А в туалете зеркало вообще лучше не вешать.."]*1 +["Если крыть нечем - кройте матом."]*1 + ["Не стой, где попало - попадёт ещё раз"]*1 + ["Если ваша машина издает странные звуки, увеличивайте громкость радио до тех пор, пока не перестанете их слышать."]*1
			embed.set_footer(text=random.choice(strings))
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msg = await ctx.send(embed = embed)

		@bot.command()
		async def info(ctx):
			embed1 = discord.Embed(title="ToxBot Info (1)", description='''
💎**Пожертвования на разработку**

Юmoney:
<https://bit.ly/3vrvWlJ>
Qiwi:
TONIXX
Donationalerts:
<https://bit.ly/3KSJ6OW>
Patreon:
<https://bit.ly/3xud881>

Наш спонсор:
Паблик с мемами в телеге
https://t.me/uuuuuuu40
''', colour = discord.Colour.from_rgb(230,0,0))
			embed1.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			embed2 = discord.Embed(title="ToxBot Info (2)", description='''
🔧**Работают над ботом**
Tonix#5322 , 410#0797, Ampernic#9707
🏠**Официальный сервер бота**
https://discord.gg/XMYZKS3b3j

 Мы хотим сказать спасибо всем тем,
у кого мы позаимствовали код.
 Как говорил Линус Торвальдс:
«Программы — как секс: лучше,
 когда бесплатно.»''')
			embed2.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			embed3 = discord.Embed(title="ToxBot Info (2)", description='''
❤️**Донатеры**


Ampernic - 200 рублей ежегодно
CentrumEx - 50 рублей
Porg_Studio - dlc для Dead Sells, 300р
Unikum131 - 100 рублей
Weriase - 50 рублей 

Спасибо что пользуетесь ToxBot!''')
			embed3.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			embeds = [embed1, embed2, embed3]
			message = await ctx.send(embed = embed1)
			reactions = ["◀️", "▶️"]
			page = Pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, color = discord.Colour.from_rgb(230,0,0), use_exit = True, reactions = reactions, timeout = 33)
			await page.start()


		@bot.event
		async def on_command_error(ctx, error):
			if isinstance(error, commands.CommandNotFound):
				await ctx.send(embed = discord.Embed(description = f'**`{ctx.author.name}, данной команды не существует.`**'))


		@bot.command()
		async def cal(ctx, *, expression:str):
			try:
				calculation = eval(expression)
				await ctx.send('Выражение: {}.\nОтвет: {}.'.format(expression, calculation))
			except SyntaxError:
				await ctx.send("Введите выражение правильно.")
			except ValueError:
				await ctx.send("Введите выражение правильно.")
			except ZeroDivisionError:
				await ctx.send("На ноль делить нельзя.")

		@bot.command()
		async def membinfo(ctx,member:discord.Member = None, guild: discord.Guild = None):
			emb = discord.Embed(title=f"Информация о пользователе {member}:", color=discord.Colour.from_rgb(230,0,0))
			emb.add_field(name="Никнейм:", value=member.display_name,inline=False)
			t = member.status
			if t == discord.Status.online:
				d = " В сети"
			t = member.status
			if t == discord.Status.offline:
				d = " Не в сети"
			t = member.status
			if t == discord.Status.idle:
				d = " Не активен"
			t = member.status
			if t == discord.Status.dnd:
				d = " Не беспокоить"
			emb.add_field(name="Активность:", value=d,inline=False)
			emb.add_field(name="Статус:", value=member.activity,inline=False)
			emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
			emb.add_field(name="Аккаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
			emb.add_field(name="Зашёл на сервер:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
			await ctx.send(embed = emb)

		@bot.command()
		async def coin(ctx):
			monetka = ['Орел.'] * 49 + ['Решка.'] * 49 + ['Ребро!'] * 2
			await ctx.send(random.choice(monetka))


		@bot.command()
		async def randomto(ctx, text):
			num2 = str(text)
			rndm = str(random.randint(1, int(num2[num2.find(" ")+1:len(num2)])))
			await ctx.send("Выпало число " + rndm +".")


		@bot.command()
		async def yesorno(ctx, *, text):
			danet = ['Да.'] * 25 + ['Нет.'] * 25 + ['Скорее всего да.'] * 25 + ['Скорее всего нет.'] * 25 + ['Наверное да.'] * 25 + ['Наверное нет.'] * 25 + ['Не уверен.'] * 25 + ['Не могу ответить.']
			await ctx.send(f"{random.choice(danet)}")


		@bot.command()
		async def fuck(ctx, *, target):
			author = ctx.message.author
			target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
			target = target.split(' ')
			try:
				target1 = await bot.fetch_user(int(target[0]))
				target.remove(target[0])
				await ctx.send(f"{author.display_name} выебал(а) {target1.display_name} " + ' '.join(target) + ".") 
			except:
				await ctx.send(f"{author.display_name} выебал(а) {target1}.")
		@bot.command()
		async def kill(ctx, *, target):
			author = ctx.message.author
			target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
			target = target.split(' ')
			try:
				target1 = await bot.fetch_user(int(target[0]))
				target.remove(target[0])
				await ctx.send(f"{author.display_name} убил(а) {target1.display_name} " + ' '.join(target) + ".")
			except:
				await ctx.send(f"{author.display_name} убил(а) {target1}.")
		@bot.command()
		async def eat(ctx, *, target):
			author = ctx.message.author
			target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
			target = target.split(' ')
			try:
				target1 = await bot.fetch_user(int(target[0]))
				target.remove(target[0])
				await ctx.send(f"{author.display_name} съел(а) {target1.display_name} " + ' '.join(target) + ".")
			except:
				await ctx.send(f"{author.display_name} съел(а) {target1}.")
		@bot.command()
		async def twisted(ctx, *, target):
			author = ctx.message.author
			target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
			target = target.split(' ')
			try:
				target1 = await bot.fetch_user(int(target[0]))
				target.remove(target[0])
				await ctx.send(f"{author.display_name} свернул(а) шею {target1.display_name} " + ' '.join(target) + ".")
			except:
				await ctx.send(f"{author.display_name} свернул(а) шею {target1}.")
		@bot.command()
		async def give(ctx, *, target):
			author = ctx.message.author
			target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
			target = target.split(' ')
			try:
				target1 = await bot.fetch_user(int(target[0]))
				target.remove(target[0])
				await ctx.send(f"{author.display_name} дал(а) {target1.display_name} " + ' '.join(target) + ".")
			except:
				await ctx.send(f"{author.display_name} дал(а) {target1}.")

		@commands.has_permissions(administrator=True)
		@bot.command()
		async def clear(ctx, number: int):
			if number < 1:
				await ctx.send("Нельзя удалить меньше одного сообщения.")
			if number > 111:
				await ctx.send("Слишком много.")
			if ((number >= 1) and (number <= 111)):
				await ctx.channel.purge(limit=number)

		@bot.command()
		async def roulette(ctx):
			author = ctx.message.author
			ruletka = [f'Пусто, {author.mention} остался в живых.'] * 5 + [f'Выстрел, {author.mention} застрелился.'] * 1
			await ctx.send(random.choice(ruletka))
		@bot.command()
		async def roulette2bul(ctx):
			author = ctx.message.author
			ruletka = [f'Пусто, {author.mention} остался в живых.'] * 4 + [f'Выстрел, {author.mention} застрелился.'] * 2
			await ctx.send(random.choice(ruletka))
		@bot.command()
		async def roulette3bul(ctx):
			author = ctx.message.author
			ruletka = [f'Пусто, {author.mention} остался в живых.'] * 3 + [f'Выстрел, {author.mention} застрелился.'] * 3
			await ctx.send(random.choice(ruletka))
		@bot.command()
		async def roulette4bul(ctx):
			author = ctx.message.author
			ruletka = [f'Пусто, {author.mention} остался в живых.'] * 2 + [f'Выстрел, {author.mention} застрелился.'] * 4
			await ctx.send(random.choice(ruletka))
		@bot.command()
		async def roulette5bul(ctx):
			author = ctx.message.author
			ruletka = [f'Пусто, {author.mention} остался в живых.'] * 1 + [f'Выстрел, {author.mention} застрелился.'] * 5
			await ctx.send(random.choice(ruletka))
		@bot.command()
		async def roulette6bul(ctx):
			author = ctx.message.author
			await ctx.send(f'{author.mention} застрелился от своей тупости.')

		@bot.command()
		async def google(ctx, *, text):
			text = discord.utils.escape_mentions(str(text))
			textb = text.replace(' ', '+')
			link = (f"https://www.google.ru/search?q={textb}")
			await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
		@bot.command()
		async def yandex(ctx, *, text):
			text = discord.utils.escape_mentions(str(text))
			textb = text.replace(' ', '+')
			link = (f"https://yandex.ru/search/?text={textb}")
			await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
		@bot.command()
		async def duckduck(ctx, *, text):
			text = discord.utils.escape_mentions(str(text))
			textb = text.replace(' ', '+')
			link = (f"https://duckduckgo.com/?q={textb}")
			await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
		@bot.command()
		async def yahoo(ctx, *, text):
			text = discord.utils.escape_mentions(str(text))
			textb = text.replace(' ', '+')
			link = (f"https://search.yahoo.com/search?p={textb}")
			await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")


		@bot.command()
		async def steam(ctx):
			await ctx.send("Ссылка на рандомную игру из стима:\n<https://store.steampowered.com/explore/random>")


		@bot.command()
		async def slots(ctx):
			slots = ["🍓", "🍋", "🍒", "💣"]
			r1 = random.choice(slots)
			embed = discord.Embed(title="ToxCasino777", description="⚫" + "⚫" + "⚫", colour = discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/984411549236101150/unknown.png")
			msg = await ctx.send(embed=embed)
			for x in range(4):
				r1 = random.choice(slots)
				await asyncio.sleep(0.2)
				new_emb = discord.Embed(title="ToxCasino777", description=r1 + "⚫" + "⚫", colour = discord.Colour.from_rgb(230,0,0))
				new_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/984411549236101150/unknown.png")
				await msg.edit(embed=new_emb)
				r2 = random.choice(slots)
			for x in range(4):
				r2 = random.choice(slots)
				await asyncio.sleep(0.2)
				new_emb = discord.Embed(title="ToxCasino777", description=r1 + r2 + "⚫", colour = discord.Colour.from_rgb(230,0,0))
				new_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/984411549236101150/unknown.png")
				await msg.edit(embed=new_emb)
				r3 = random.choice(slots)
			for x in range(4):
				r3 = random.choice(slots)
				await asyncio.sleep(0.2)
				new_emb = discord.Embed(title="ToxCasino777", description=r1 + r2 + r3, colour = discord.Colour.from_rgb(230,0,0))
				new_emb.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/984411549236101150/unknown.png")
				await msg.edit(embed=new_emb)
			if r1 == r2 == r3 and r1 != "💣":
				await msg.add_reaction('✅')
			if r1 == r2 == r3 and r1 == "💣":
				await msg.add_reaction('💥')
			if r1 != r2 or r2 != r3 or r1 != r3:
				await msg.add_reaction('❌')

		# Помощь по командам
		@bot.command()
		async def helpОсновное(ctx):
			embed = discord.Embed(title="Помощь по командам", colour=discord.Colour.from_rgb(230,0,0), description='`help` —  Меню команд.\n`info` — Инфо о донатерах и разработчиках.\n`ver` - Версия бота на текущий момент.')
			msg = await ctx.send(embed = embed)
		@bot.command()
		async def helpВоспроизведение(ctx):
			embed = discord.Embed(title="Помощь по командам", colour=discord.Colour.from_rgb(230,0,0), description='`p` *URL* — Воспроизведение аудио с ютуба.\n`p1|p2|p3...` — Воспроизведение радио.\n`loop all|one|off` — Вкл/Выкл повтор.\n`skip` — Пропустить трек.\n`stop` — Остановить воспроизведение.\n`rstop` — Остановить радио\n`rlist` — Лист всех радиостанций.')
			msg = await ctx.send(embed = embed)
		@bot.command()
		async def helpРабота(ctx):
			embed = discord.Embed(title="Помощь по командам", colour=discord.Colour.from_rgb(230,0,0), description='`dem` *ссылка на пикчу* *Текст 1* *Текст 2* — Демотиватор.\n`shakal` *ссылка на пикчу* *качество (0-100)* — Зашакаливание.\n`quote` *@Пинг пользователя* *текст цитаты* - Создание цитаты, так же работает если написать команду в ответ на сообщение.')
			msg = await ctx.send(embed = embed)
		@bot.command()
		async def helpИгры(ctx):
			embed = discord.Embed(title="Помощь по командам", colour=discord.Colour.from_rgb(230,0,0), description='`call` *911|255|пинг* *текст* - позвонить в полицию, пиццерию или же любому пользователю, текст не обязателен.\n`kill` *текст* - Убить.\n`twisted` *текст* — Свернуть шею.\n`fuck` *текст* — Изнасиловать.\n`eat` *текст* — Съесть.\n`give` *текст* - Дать.\n`roulette2bul|3bul|4bul...` — Русская рулетка, `roulette` — одна пуля.\n`coin` - Игра в монетку\n`slots` - Слоты казино.')
			msg = await ctx.send(embed = embed)
		@bot.command()
		async def helpИнфо(ctx):
			embed = discord.Embed(title="Помощь по командам", colour=discord.Colour.from_rgb(230,0,0), description='`stats` — Список активностей людей на сервере.\n`membinfo` *@пользователь* — Информация о пользователе.\n`randomto(Число)` — Рандом до заданного числа больше одного.\n`cal` — Калькулятор.\n`time` — Время по МСК.\n`laugh` — Смех.\n`yesorno` — Да или нет.\n`clear число` —  Удаление сообщений. Только для админов.')
			msg = await ctx.send(embed = embed)
		@bot.command()
		async def helpПоиск(ctx):
			embed = discord.Embed(title="Помощь по командам", colour=discord.Colour.from_rgb(230,0,0), description='`google|yandex|duckduck|yahoo` *текст* — Поиск по этому запросу.')
			msg = await ctx.send(embed = embed)

		#Всякие элементарные вещи
		@bot.command()
		async def time(ctx):
			tz_Moscow = pytz.timezone('Europe/Moscow')
			datetime_Moscow = datetime.now(tz_Moscow)
			embed = discord.Embed(title="ToxBot", description=datetime_Moscow.strftime("%H:%M:%S"), colour = discord.Colour.from_rgb(230,0,0))
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
			msg = await ctx.send(embed=embed)

		@bot.command()
		async def nothing(ctx):
			await ctx.send("** **")

		@bot.command()
		async def laugh(ctx):
			def rnd_str(min_chars=6, max_chars=10, alphabet=("А", "Х", "П", "а", "х", "п")):
				return ''.join(random.choices(alphabet, k=random.randint(min_chars, max_chars)))
			await ctx.send(f"{(rnd_str(6, 10))}!!!")

		@bot.command()
		async def fuck_you(ctx):
			author = ctx.message.author
			await ctx.reply(f"No, {author.mention}, fuck you!")

		@bot.command()
		async def ping(ctx):
			embed = discord.Embed(title="Понг!", description=f" {round(bot.latency * 1000)} мс.", colour = discord.Colour.from_rgb(230,0,0))
			await ctx.send(embed=embed)

		@bot.command()
		async def c(ctx):
			author = ctx.message.author
			await ctx.reply(f"{author.mention} ты еблан?")

		@bot.command()
		async def dog(ctx):
			response = requests.get("https://some-random-api.ml/img/dog")
			json_data = json.loads(response.text)
			embed = discord.Embed(color = 0x8b0000, title = "Fucking dog.")
			embed.set_image(url = json_data["link"])
			await ctx.send(embed = embed)

		@bot.command()
		async def fox(ctx):
			response = requests.get("https://some-random-api.ml/img/fox")
			json_data = json.loads(response.text)
			embed = discord.Embed(color = 0x8b0000, title = "Fucking fox.")
			embed.set_image(url = json_data["link"])
			await ctx.send(embed = embed)

		@bot.command()
		async def cat(ctx):
			response = requests.get("https://some-random-api.ml/img/cat")
			json_data = json.loads(response.text)
			embed = discord.Embed(color = 0x8b0000, title = "Fucking cat.")
			embed.set_image(url = json_data["link"])
			await ctx.send(embed = embed)

		@bot.command()
		async def bird(ctx):
			response = requests.get("https://some-random-api.ml/img/bird")
			json_data = json.loads(response.text)
			embed = discord.Embed(color = 0x8b0000, title = "Fucking bird.")
			embed.set_image(url = json_data["link"])
			await ctx.send(embed = embed)


		@bot.command()
		async def cum(ctx):
			response = ("http://www.hudeem-s-profi.ru/files/images/6zqbxxxljrnpsdldhcxz.jpg")
			await ctx.send(response)

		@bot.command()
		async def xoxol(ctx):
			response = ("https://avelita.ru/wa-data/public/shop/products/94/02/10294/images/25335/25335.650.jpg")
			embed = discord.Embed(title="хохлы", description="В связи с ситуацией в украине, эта команда временно не работает.", colour = discord.Colour.from_rgb(230,0,0))
			embed.set_image(url = response)
			await ctx.send(embed = embed)

		@bot.command()
		async def gay(ctx):
			strings = ["https://media.discordapp.net/attachments/674594514303975434/931593784259674142/b95400d0-b508-4244-9bc5-a8b098f8a80e.png", "https://media.discordapp.net/attachments/762655570221203466/931594108580008026/unknown.png", "https://media.discordapp.net/attachments/674594514303975434/931602635189002240/7f6a9091-9a0b-40be-902e-85ac93930b36.png", "https://media.discordapp.net/attachments/678564352164495387/932670407876702228/unknown.png?width=455&height=675", "https://media.discordapp.net/attachments/939136925095297055/965175091619045436/IMG_20220416_145225.jpg", "https://media.discordapp.net/attachments/704372667859599453/964104094723735582/IMG-20220413-WA0002.jpeg", "https://media.discordapp.net/attachments/704372667859599453/965288887754846218/IMG-20220414-WA0010.jpeg", "https://media.discordapp.net/attachments/704372667859599453/965289162997645312/IMG_20220417_183413.jpg"]
			await ctx.send(random.choice(strings))

		@bot.command()
		async def niggers(ctx):
			strings = ["http://3.bp.blogspot.com/-yf3xMdLObGk/T3fON3wZurI/AAAAAAAA4tQ/QT5PT9q_tAY/s1600/Daddy838.jpg", "https://famt.ru/wp-content/uploads/2019/07/k-chemu-snitsya-negr-muzhchina.jpg", "https://otvet.imgsmail.ru/download/u_08aceead9e79f1fa2d6d289905d78e8d_800.jpg", "https://themancrushblog.com/wp-content/uploads/2013/11/daniel-louisy+5.jpg", "https://www.timeout.ru/img/%D0%9C%D0%B0%D1%80%D0%B3%D0%B0%D1%80%D0%B8%D1%82%D0%B0/%D0%9A%D0%B8%D0%BD%D0%BE/%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%202020/C4D_SHwWQAA2FZR.jpg","https://s00.yaplakal.com/pics/pics_original/1/6/3/14400361.jpg","https://www.meme-arsenal.com/memes/f8fb9c33e73272021defca88c110cac8.jpg","https://i.imgur.com/Ogcuewp.jpg", "http://risovach.ru/upload/2018/12/generator/negr_194265628_orig_.jpg","http://prettymalemodels.com/wp-content/uploads/2017/03/DSC_7241-Edit.jpg","https://yt3.ggpht.com/-D6fqV6rRmRQ/AAAAAAAAAAI/AAAAAAAAAAA/UkT41uCEBZw/s900-c-k-no/photo.jpg","https://w7.pngwing.com/pngs/505/138/png-transparent-jay-rock-rapper-follow-me-home-musician-black-friday-jay-z-tshirt-arm-abdomen.png","https://mypersonalbroker.files.wordpress.com/2017/11/04.jpg"]
			await ctx.send(random.choice(strings))

		@bot.command()
		async def balls(ctx):
			strings = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ","https://i.ytimg.com/vi/qJPq0EaCRck/maxresdefault.jpg","https://ae01.alicdn.com/kf/HLB1y77JaOrxK1RkHFCcq6AQCVXaf.jpg", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/60c2c9c4-c5db-443a-ba53-0acc0a5875e7/d2m8je7-0a3eb7d7-5b0c-44d7-a536-bc4db8844b4a.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi82MGMyYzljNC1jNWRiLTQ0M2EtYmE1My0wYWNjMGE1ODc1ZTcvZDJtOGplNy0wYTNlYjdkNy01YjBjLTQ0ZDctYTUzNi1iYzRkYjg4NDRiNGEuanBnIn1dXX0.K08BpRRTK3Oqw_r-PQWbDQ_Ur-H80hIk86LW1grED5Q"]
			await ctx.send(random.choice(strings))


		@bot.command()
		async def pizza(ctx):
			strings = ["https://media.discordapp.net/attachments/939136925095297055/966067143013716018/unknown.png", "https://media.discordapp.net/attachments/939136925095297055/966067143277944833/unknown.png", "https://media.discordapp.net/attachments/939136925095297055/966067143915475005/unknown.png", "https://media.discordapp.net/attachments/939136925095297055/966067144251031602/unknown.png"]
			await ctx.send(random.choice(strings))
		@bot.command()
		async def coke(ctx):
			strings = ["https://media.discordapp.net/attachments/939136925095297055/966067823459835954/unknown.png", "https://media.discordapp.net/attachments/939136925095297055/966067823707316304/unknown.png", "https://media.discordapp.net/attachments/939136925095297055/966067824009302066/unknown.png"]
			await ctx.send(random.choice(strings))


		@bot.command(aliases = ["balance", "баланс", "деньги"])
		async def ballance(ctx, member: discord.Member = None):
			if member is None:
				UsTaCr.author(ctx)
				for row in cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id}'):
					embed = discord.Embed(title = "ToxCoins", description = f"Баланс {ctx.author.display_name} - {row[0]} ТоксКоинов.", colour = discord.Colour.from_rgb(230,0,0))
					await ctx.send(embed=embed)
			else:
				UsTaCr.member(ctx, member)
				for row in cursor.execute(f'SELECT "money" FROM economy WHERE id = {member.id}'):
					embed = discord.Embed(title = "ToxCoins", description = f"Баланс {member.display_name} - {row[0]} ТоксКоинов.", colour = discord.Colour.from_rgb(230,0,0))
					await ctx.send(embed=embed)

		@bot.command(aliases = ["pay", "заплатить", "отдать"])
		async def givecoins(ctx, member: discord.Member = None, Value: int = None):
			if member is None:
				await ctx.send("Укажите цель!")
			else:
				UsTaCr.author(ctx)
				UsTaCr.member(ctx, member)
				if Value is None:
					await ctx.send("Укажите количество ТоксКоинов!")
				elif Value <= 0:
					await ctx.send("Нельзя передать 0 ТоксКоинов или меньше!")
				else:
					ebal = 0
					for row in cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id}'):
						ebal = int(row[0])
					if ebal >= Value:
						for row in cursor.execute(f'SELECT "money" FROM economy WHERE id={ctx.author.id}'):
							orow1 = int(row[0])
							row1 = int(row[0]) - Value
						curosr.execute(f'UPDATE economy SET money = {row1} WHERE id={ctx.author.id}')
						for row in cursor.execute(f'SELECT money FROM economy WHERE id={member.id}'):
							orow2 = int(row[0])
							row2 = int(row[0]) + Value
						curosr.execute(f'UPDATE economy SET money = {row2} WHERE id={member.id}')
						embed = discord.Embed(title="ToxCoins", description=f"Пользователь {ctx.author.display_name} дал {Value} ТоксКоинов {member.display_name}.\nНовый баланс {member.display_name} - {row2} ТоксКоинов.")
					else:
						await ctx.send("Недостаточно денег!")

		FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

		@bot.command()
		async def rlist(ctx):
			embed1 = discord.Embed(title = "Список радиостанций (1)", description = '''
`p1` - Шансон
`p2` - Радио Дача
`p3` - Х*й забей радио
`p4` - Новое Радио
`p5` - FM радио
`p6` - Дорожное Радио (Омск)
`p7` - POP радио 70х
`p8` - Радио 80х
`p9` - Радио 90х
`p10` - хиты кантри
`p11` - хиты рока
`p12` - рок фм
`p13` - Христианское радио
`p14` - психоделик''')
			embed2 = discord.Embed(title = "Список радиостанций (2)", description = '''
`p15` - классический рок
`p16` - Ретро FM
`p17` - Хевиметал
`p18` - Украинское Радио Релакс
`p19` - детское радио
`p20` - ссср радио
`p21` - радио аниме из Осаки
`p22` - Джаз
`p23` - lofi
`pRMS` - Радио *RAMSHTEIN*
`pRHCP` - радио *Red Hot Chili Peppers*
`pKISH` - Радио *Король и Шут*
`pL` - Радио *Гражданская оборона*
`p0` *ссылка на поток* - Своё радио''')

			embeds = [embed1, embed2]
			message = await ctx.send(embed = embed1)
			reactions = ["◀️", "▶️"]
			page = Pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, color = discord.Colour.from_rgb(230,0,0), use_exit = True, reactions = reactions, timeout = 33)
			await page.start()


		async def rplay(ctx, link: None):
			if link != None:
				voice_channel = ctx.author.voice.channel
				voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
				if voice_client:
					voice_client.pause()
					if(data["OS"]==1):
						voice_client.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source = link, **FFMPEG_OPTIONS))
					elif(data["OS"]==0):
						voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = link, **FFMPEG_OPTIONS))
				else:
					player = await voice_channel.connect()
					if(data["OS"]==1):
						player.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source = link, **FFMPEG_OPTIONS))
					elif(data["OS"]==0):
						voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = link, **FFMPEG_OPTIONS))


		@bot.command()
		async def p1(ctx):
			await rplay(ctx, "http://chanson.hostingradio.ru:8041/chanson256.mp3")
			await ctx.send("Радио включено.\nИграет: Шансон")
			print_log('info', "Радио включено: Шансон")
		@bot.command()
		async def p4(ctx):
			await rplay(ctx, "http://live.novoeradio.by:8000/novoeradio-128k")
			await ctx.send("Радио включено.\nИграет: Новое радио")
			print_log('info', "Радио включено: Новое радио")
		@bot.command()
		async def p5(ctx):
			await rplay(ctx, "http://listen.teploe.net:8100/npkfm")
			await ctx.send("Радио включено.\nИграет: FM радио")
			print_log('info', "Радио включено: FM радио")
		@bot.command()
		async def p9(ctx):
			await rplay(ctx, "http://prmstrm.1.fm:8000/90s")
			await ctx.send("Радио включено.\nИграет: Радио 90х")
			print_log('info', "Радио включено: Радио 90х")
		@bot.command()
		async def p7(ctx):
			await rplay(ctx, "http://prmstrm.1.fm:8000/70s")
			await ctx.send("Радио включено.\nИграет: Поп радио 70х")
			print_log('info', "Радио включено: Поп радио 70х")
		@bot.command()
		async def p10(ctx):
			await rplay(ctx, "http://prmstrm.1.fm:8000/acountry")
			await ctx.send("Радио включено.\nИграет: Хиты кантри")
			print_log('info', "Радио включено: Хиты кантри")
		@bot.command()
		async def p11(ctx):
			await rplay(ctx, "http://prmstrm.1.fm:8000/x")
			await ctx.send("Радио включено.\nИграет: Хиты рока")
			print_log('info', "Радио включено: Хиты рока")
		@bot.command()
		async def p12(ctx):
			await rplay(ctx, "http://jfm1.hostingradio.ru:14536/rock00.mp3")
			await ctx.send("Радио включено.\nИграет: Рок FM")
			print_log('info', "Радио включено: Рок FM")
		@bot.command()
		async def p13(ctx):
			await rplay(ctx, "https://str.pcradio.ru/radio123_by-hi")
			await ctx.send("Радио включено.\nИграет: Христианское радио")
			print_log('info', "Радио включено: Христианское радио")
		@bot.command()
		async def p14(ctx):
			await rplay(ctx, "http://psyprog.rupsy.ru:8000/psyprog")
			await ctx.send("Радио включено.\nИграет: Психоделик")
			print_log('info', "Радио включено: Психоделик")
		@bot.command()
		async def p19(ctx):
			await rplay(ctx, "https://str.pcradio.ru/rusradio_deti-hi")
			await ctx.send("Радио включено.\nИграет: Детское радио")
			print_log('info', "Радио включено: Детское радио")
		@bot.command()
		async def p16(ctx):
			await rplay(ctx, "https://str.pcradio.ru/retrofm_ru-hi")
			await ctx.send("Радио включено.\nИграет: Ретро FM")
			print_log('info', "Радио включено: Ретро FM")
		@bot.command()
		async def p20(ctx):
			await rplay(ctx, "https://str.pcradio.ru/SSSR-hi")
			await ctx.send("Радио включено.\nИграет: СССР радио")
			print_log('info', "Радио включено: СССР радио")
		@bot.command()
		async def p18(ctx):
			await rplay(ctx, "https://str.pcradio.ru/radiorelax_ua-hi")
			await ctx.send("Радио включено.\nИграет: Украинское радио релакс")
			print_log('info', "Радио включено: Украинское радио релакс")
		@bot.command()
		async def pKISH(ctx):
			await rplay(ctx, "https://str.pcradio.ru/Korol_i_Shut-hi")
			await ctx.send("Радио включено.\nИграет: Радио Король и Шут")
			print_log('info', "Радио включено: Радио Король и Шут")
		@bot.command()
		async def pL(ctx):
			await rplay(ctx, "https://str.pcradio.ru/Grazhdanskaja_oborona-hi")
			await ctx.send("Радио включено.\nИграет: Радио Гражданская оборона")
			print_log('info', "Радио включено: Радио Гражданская оборона")
		@bot.command()
		async def p15(ctx):
			await rplay(ctx, "https://str.pcradio.ru/rpr1_de_clasro-hi")
			await ctx.send("Радио включено.\nИграет: Классический рок")
			print_log('info', "Радио включено: Классический рок")
		@bot.command()
		async def p17(ctx):
			await rplay(ctx, "https://str.pcradio.ru/rpr1_de_metal-hi")
			await ctx.send("Радио включено.\nИграет: Хевиметал")
			print_log('info', "Радио включено: Хевиметал")
		@bot.command()
		async def pRMS(ctx):
			await rplay(ctx, "https://str.pcradio.ru/Rammstein-hi")
			await ctx.send("Радио включено.\nИграет: Раммштайн")
			print_log('info', "Радио включено: Раммштайн")
		@bot.command()
		async def pRHCP(ctx):
			await rplay(ctx, "https://str.pcradio.ru/red_hot_chili_peppers-hi")
			await ctx.send("Радио включено.\nИграет: Red Hot Chili Peppers радио")
			print_log('info', "Радио включено: Red Hot Chili Peppers радио")
		@bot.command()
		async def p8(ctx):
			await rplay(ctx, "https://str.pcradio.ru/pulsradio_80s-hi")
			await ctx.send("Радио включено.\nИграет: Радио 80х")
			print_log('info', "Радио включено: Радио 80х")
		@bot.command()
		async def p6(ctx):
			await rplay(ctx, "https://str.pcradio.ru/dorozhnoe_omsk-hi")
			await ctx.send("Радио включено.\nИграет: Дорожное радио (Омск)")
			print_log('info', "Радио включено: Дорожное радио (Омск)")
		@bot.command()
		async def p3(ctx):
			await rplay(ctx, "https://str.pcradio.ru/Hui_Zabey-hi")
			await ctx.send("Радио включено. \nИграет: Х*й Забей радио")
			print_log('info', "Радио включено: Х*й Забей радио")
		@bot.command()
		async def p2(ctx):
			await rplay(ctx, "http://178.217.40.125:8000/rdsat")
			await ctx.send("Радио включено. \nИграет: Радио дача")
			print_log('info', "Радио включено: Играет: Радио дача")
		@bot.command()
		async def p21(ctx):
			await rplay(ctx, "https://japanimradio-osaka.com/radio/8000/stream")
			await ctx.send("Радио включено. \nИграет: Аниме радио из Осаки.")
			print_log('info', "Радио включено: Аниме радио из Осаки.")
		@bot.command()
		async def p22(ctx):
			await rplay(ctx, "http://jfm1.hostingradio.ru:14536/jlstream.mp3")
			await ctx.send("Радио включено. \nИграет: Джаз.")
			print_log('info', "Радио включено: Джаз.")
		@bot.command()
		async def p23(ctx):
			await rplay(ctx, "https://usa9.fastcast4u.com/proxy/jamz?mp=/1")
			await ctx.send("Радио включено. \nИграет: Lofi.")
			print_log('info', "Радио включено: Lofi.")


		@bot.command()
		async def p0(ctx, *, link: str):
			txt = discord.utils.escape_mentions(link)
			if link is not None:
				await rplay(ctx, str(txt))
				await ctx.send(f"Радио включено. \nИграет: {str(txt)}")
				print_log('info', "Радио включено: Своя радиостанция (Вызвано {})".format(+ ctx.message.author.name))
			else:
				await ctx.send("Вставьте ссылку.")

		@bot.command()
		async def rstop(ctx):
			await ctx.voice_client.disconnect()
			await ctx.send("Радио остановлено.")


		plugins(bot, data)
	else:
		print_log('info', 'Сегодня я проснулся от взрывов...')
		@bot.event
		async def on_message(message):
			if '++' in message.content:
				await message.channel.send(f'В связи с ситуацией в украине, бот приостановил свою работу в России.')
	try:
		print_log('wait', "Попытка подключится используя токен: {}".format(data["Token"]))
		bot.run(data["Token"])
	except Exception as e:
		print_log('err', 'Не удалось подключиться с указанным токеном \n ({})'.format(e))
else:
	print_log('err', "Инициализация прервана.")
