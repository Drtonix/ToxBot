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
from classes import UsTaCr, SeTaCr, conn, cursor
from core.toxbot_core import *
from PIL import Image, ImageDraw, ImageFont

# Переменные

data = None
init_successful = False
intents = discord.Intents.all()

# Инициализация

init()
print(header_logo)
print_log('wait', "Ожидание:\tИнициализация базовой конфигурации")
try:
	data = core_parse_data(data)
	print_log('bank', "\tВыполняется: Импорт конфигурации из хранилища.")
	if data["FirstBoot"] == "True":
		print_log('warn', "Обнаружен первый запуск программы:  Переходим в режим настройки")
		first_boot_cofigure(data)
	else:
		print_log('info', "Успех: Значения конфигурации получены.\n")
		bot = Bot(command_prefix="++", help_command=None, intents=intents, case_insensitive=True)
		client = discord.ext.commands.Bot(command_prefix="++", intents=discord.Intents.all())
		init_successful = True
		@bot.event
		async def on_ready():
			DiscordComponents(bot)
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="++help"))
			print_log("info", "Бот успешно запущен.")
except Exception as e:
	print_log('err', "Не удалось спарсить значения из конфига: " + str(e))

if init_successful:
	plugins_manager1 = plugins_manager(bot, data)
	@bot.command(aliases = ["версия", "вер", "version"])
	async def ver(ctx):
		try:
			embed = discord.Embed(title="ToxBot {}!".format(num_ver), description=text_ver, colour=discord.Colour.from_rgb(230, 0, 0))
			msg = await ctx.send(embed=embed)
		except Exception as e:
			print_log('err', f'Ошибка: {e}')

	# Команды
	@bot.event
	async def on_member_join(member):
		SeTaCr.creeate(member)
		await member.send(f'Добро пожаловать на сервер {member.guild.name}!\nСписок команд: ++help\nВы можете поддержать разработку бота: ++info\nОфициальный сервер бота: <https://discord.gg/AgWXKAr3gG>')
		try:
			for row in cursor.execute(f"SELECT welcomeid FROM admininfo WHERE id ={member.guild.id}"):
				if row[0] != 0:
					for ch in bot.get_guild(member.guild.id).channels:
						if ch.id == row[0]:
							await bot.get_channel(ch.id).send(f'Поздоровайтесь с новым участником Сервера, {member.display_name}!')
		except:
			print("Произошла ошибка при попытке найти канал.")
		
	@commands.has_permissions(administrator=True)
	@bot.command(aliases = ["каналприветствия"])
	async def welcomechannel(ctx, id: int = None):
		SeTaCr.create(ctx)
		if id != None:
			for row in cursor.execute(f"SELECT * FROM admininfo WHERE id = {ctx.guild.id}"):
				rowd = id
				await ctx.send("Успешно установлено. Убедитесь что вы все указали правильно иначе приветствие не будет работать.")
				cursor.execute(f"UPDATE admininfo SET welcomeid = {rowd} WHERE id = {ctx.guild.id}")
				conn.commit()
		else:
			await ctx.send("Пожалуйста, укажите ID канала через функцию для разработчиков.")
	@bot.event
	async def on_member_remove(member):
		for ch in bot.get_guild(member.guild.id).channels:
			if ch.name == "💬┃био-отходняк-чат":
				await bot.get_channel(ch.id).send(f'К сожалению, участник {member.display_name} покинул нас.')

	# help, info
	@bot.command(aliases = ["помощь", "?","хелп"])
	async def help(ctx):
		embed = discord.Embed(title="Используйте `++` перед \nначалом команды", description='''		
📌**Основное**
`help`, `info`, `ver`
🎧**Воспроизведение**
`p`, `loop`, `skip`, `stop`, `stopradio`
`rlist`
🖼️**Изображения**
`shakal`
`dem`, `quote`
🎲**Действия**
`kill`, `twisted`, `rape`, `eat`, `give`, `drink`, `call`
`roulette`, `coin`, `slots`
📚**Полезности**
`stats`, `membinfo`, `lvl`
`randomto`, `cal`, `time`, `laugh`, `yesorno`, `clear`, `welcomechannel`
`google`, `yandex`, `duckduck`, `yahoo`
💵**Экономика**
`pay`, `add`, `wd`, `bal`
🪙**ToxBot Premium**
Подробнее — `premium`''', colour = discord.Colour.from_rgb(230,0,0))
		strings = ["Напишите ++helpfull для полных команд"]* 88 + ["Шуруп, забитый молотком, держится крепче, чем гвоздь, закрученный отвёрткой."]*1 +["Обувь будет носиться значительно дольше, если не покупать новую."]*1 + ["Если сосиски отварить с кубиком говяжьего бульона - то они будут пахнуть мясом."]*1 +["Большинство электрических приборов потребляют меньше электричества в выключенном состоянии."]*1 + ["Вегетарианский суп будет питательней, если в него положить немного говядины."]*1 +["Если ваш компьютер заразил вирус - как можно скорее переформатируйте ваш жесткий диск; не давайте вирусу удовольствие самому это сделать."]*1 + ["Если вы хотите приготовить дрожжевое тесто, но у вас нет дрожжей, то ни фига у вас не получится."]*1 +["Если ваш сосед внезапно купил ружье, вам лучше завязать с музыкой."]*1 + ["Нельзя смотреться в зеркало когда ешь - счастье своё проешь. И когда пьёшь - пропьёшь. А в туалете зеркало вообще лучше не вешать.."]*1 +["Если крыть нечем - кройте матом."]*1 + ["Не стой, где попало - попадёт ещё раз"]*1 + ["Если ваша машина издает странные звуки, увеличивайте громкость радио до тех пор, пока не перестанете их слышать."]*1
		embed.set_footer(text=random.choice(strings))
		msg = await ctx.send(embed = embed)

	@bot.command(aliases = ["информация", "допинфо", "инфо", "ёбаныйобэмэ"])
	async def info(ctx):
		embed1 = discord.Embed(title="ToxBot Info (1)", description='''
💎**Пожертвования на разработку**

Donationalerts:
<https://clck.ru/32Y4WD>

Boosty:
<https://boosty.to/toxbot>
''', colour = discord.Colour.from_rgb(230,0,0))
		embed1.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		embed2 = discord.Embed(title="ToxBot Info (2)", description='''
❤️**Донатеры**

Porg_Studio - 433 рубля

Unikum131 - 150 рублей
CentrumEx - 50 рублей
Weriase - 50 рублей
''')
		embed2.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		embed3 = discord.Embed(title="ToxBot Info (3)", description='''
🔧**Работают над ботом**
Tonix#5322 , Ampernic#9707

🏠**Официальный сервер бота**
https://discord.gg/XMYZKS3b3j

Спасибо что пользуетесь ToxBot!
''')
		embed3.set_thumbnail(url="https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png")
		embeds = [embed1, embed2, embed3]
		message = await ctx.send(embed = embed1)
		reactions = ["◀️", "▶️"]
		page = Pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, color = discord.Colour.from_rgb(230,0,0), use_exit = False, reactions = reactions, timeout = 99)
		await page.start()

	@bot.command(aliases = ["премиум", "prem", "прем"])
	async def premium(ctx):
		embed = discord.Embed(title="ToxBot Premium", description='''

Вы можете оформить ToxBot Premium
за 50 рублей в месяц -
Для этого оформите подписку
на нашем бусти: boosty.to/toxbot

Команды премиума будут бесплатно дополняться
и со временем вы сможете пользоваться большим
количеством команд.

Оформив премиум, вы очень поможете
разработке ToxBot.
Команды премиума — `++premhelp`.''', colour = discord.Colour.from_rgb(230,0,0))
		await ctx.send(embed = embed)



	@bot.event
	async def on_command_error(ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send(embed = discord.Embed(description = f'**`{ctx.author.name}, данной команды не существует.`**'))

	@bot.command(aliases = ["калькулятор", "кал"])
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

	@bot.command(aliases = ["мембинфо", "пользовательинфо", "userinfo"])
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

	@bot.command(aliases = ["монетка"])
	async def coin(ctx):
		monetka = ['Орел.'] * 49 + ['Решка.'] * 49 + ['Ребро!'] * 2
		await ctx.send(random.choice(monetka))

	@bot.command()
	async def test2(ctx):
		reactions = ['😀', 
					'😡']
		winning_reaction = random.choice(reactions)
		message = await ctx.channel.send('Выбери эмодзи')
		for reaction in reactions:
			await message.add_reaction(reaction)
		def check(reaction, user):
			return user == ctx.author and str(reaction) == winning_reaction
		try:
			reaction, user = await bot.wait_for('reaction_add', check=check, timeout=60.0)
			await ctx.send('Угадал')
		except asyncio.TimeoutError:
			await ctx.send('Время вышло')
		else:
			await ctx.send('Не угадал')

	@bot.command(aliases = ["рандомдо", "рандом"])
	async def randomto(ctx, text):
		num2 = str(text)
		rndm = str(random.randint(1, int(num2[num2.find(" ")+1:len(num2)])))
		await ctx.send("Выпало число " + rndm +".")

	@bot.command(aliases = ["данет", "даилинет"])
	async def yesorno(ctx, *, text):
		danet = ['Да.'] * 25 + ['Нет.'] * 25 + ['Скорее всего да.'] * 25 + ['Скорее всего нет.'] * 25 + ['Наверное да.'] * 25 + ['Наверное нет.'] * 25 + ['Не уверен.'] * 25 + ['Не могу ответить.']
		await ctx.send(f"{random.choice(danet)}")


	@bot.command(aliases = ["fuck","изнасиловать","трахать","трахнуть","выебать","игратьвгеншинвместес"])
	async def rape(ctx, *, target):
		author = ctx.message.author
		target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
		target = target.split(' ')
		for x in range(len(target)):
			try:
				target1 = await ctx.guild.fetch_member(int(target[x]))
			except:
				target1 = " ".join(target)
			else:
				target.remove(target[x])
				break
		try:
			if len(target) > 0:
				await ctx.send(f"{author.display_name} изнасиловал(а) {target1.display_name} " + ' '.join(target) + ".")
			else:
				 await ctx.send(f"{author.display_name} изнасиловал(а) {target1.display_name}.")
		except:
				await ctx.send(f"{author.display_name} изнасиловал(а) " + ' '.join(target) + '.')
	@bot.command(aliases = ["убить", "килл", "кильнуть", "резня"])
	async def kill(ctx, *, target):
		author = ctx.message.author
		target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
		target = target.split(' ')
		for x in range(len(target)):
			try:
				target1 = await ctx.guild.fetch_member(int(target[x]))
			except:
				target1 = " ".join(target)
			else:
				target.remove(target[x])
				break
		try:
			if len(target) > 0:
				await ctx.send(f"{author.display_name} убил(а) {target1.display_name} " + ' '.join(target) + ".")
			else:
				await ctx.send(f"{author.display_name} убил(а) {target1.display_name}.")
		except:
			await ctx.send(f"{author.display_name} убил(а) {target1}.")

	@bot.command(aliases = ["съесть", "захавать","схавать"])
	async def eat(ctx, *, target):
		author = ctx.message.author
		target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
		target = target.split(' ')
		for x in range(len(target)):
			try:
				target1 = await ctx.guild.fetch_member(int(target[x]))
			except:
				target1 = " ".join(target)
			else:
				target.remove(target[x])
				break
		try:
			if len(target) > 0:
				await ctx.send(f"{author.display_name} съел(а) {target1.display_name} " + ' '.join(target) + ".")
			else:
				await ctx.send(f"{author.display_name} съел(а) {target1.display_name}.")
		except:
			await ctx.send(f"{author.display_name} съел(а) {target1}.")
		
	@bot.command(aliases = ["выпить", "бухать","выбухать"])
	async def drink(ctx, *, target):
		author = ctx.message.author
		target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
		target = target.split(' ')
		for x in range(len(target)):
			try:
				target1 = await ctx.guild.fetch_member(int(target[x]))
			except:
				target1 = " ".join(target)
			else:
				target.remove(target[x])
				break
		try:
			if len(target) > 0:
				await ctx.send(f"{author.display_name} выпил(а) {target1.display_name} " + ' '.join(target) + ".")
			else:
				await ctx.send(f"{author.display_name} выпил(а) {target1.display_name}.")
		except:
			await ctx.send(f"{author.display_name} выпил(а) {target1}.")
	
	@bot.command(aliases = ["свернутьшею","свернуть"])
	async def twisted(ctx, *, target):
		author = ctx.message.author
		target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
		target = target.split(' ')
		for x in range(len(target)):
			try:
				target1 = await ctx.guild.fetch_member(int(target[x]))
			except:
				target1 = " ".join(target)
			else:
				target.remove(target[x])
				break
		try:
			if len(target) > 0:
				await ctx.send(f"{author.display_name} свернул(а) шею {target1.display_name} " + ' '.join(target) + ".")
			else:
				await ctx.send(f"{author.display_name} свернул(а) шею {target1.display_name}.")
		except:
			await ctx.send(f"{author.display_name} свернул(а) шею {target1}.")
		
	@bot.command(aliases = ["дать", "отдать"])
	async def give(ctx, *, target):
		author = ctx.message.author
		target = target.replace('<', '').replace('>', '').replace('@', '').replace('&', '')
		target = target.split(' ')
		for x in range(len(target)):
			try:
				target1 = await ctx.guild.fetch_member(int(target[x]))
			except:
				target1 = " ".join(target)
			else:
				target.remove(target[x])
				break
		try:
			if len(target) > 0:
				await ctx.send(f"{author.display_name} дал(а) {target1.display_name} " + ' '.join(target) + ".")
			else:
				await ctx.send(f"{author.display_name} дал(а) {target1.display_name}.")
		except:
			await ctx.send(f"{author.display_name} дал(а) {target1}.")

	@commands.has_permissions(administrator=True)
	@bot.command(aliases = ["очистить"])
	async def clear(ctx, number: int):
		if number < 1:
			await ctx.send("Нельзя удалить меньше одного сообщения.")
		if number > 25:
			await ctx.send("Слишком много.")
		if ((number >= 1) and (number <= 25)):
			await ctx.channel.purge(limit=number)

	@bot.command(aliases = ["рулетка", "русскаярулетка"])
	async def roulette(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 5 + [f'Выстрел, {author.mention} застрелился.'] * 1
		await ctx.send(random.choice(ruletka))
	
	@bot.command(aliases = ["рулетка2пули", "русскаярулетка2пули"])
	async def roulette2bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 4 + [f'Выстрел, {author.mention} застрелился.'] * 2
		await ctx.send(random.choice(ruletka))
	
	@bot.command(aliases = ["рулетка3пули", "русскаярулетка3пули"])
	async def roulette3bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 3 + [f'Выстрел, {author.mention} застрелился.'] * 3
		await ctx.send(random.choice(ruletka))
	
	@bot.command(aliases = ["рулетка4пули", "русскаярулетка4пули"])
	async def roulette4bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 2 + [f'Выстрел, {author.mention} застрелился.'] * 4
		await ctx.send(random.choice(ruletka))
	
	@bot.command(aliases = ["рулетка5пуль", "русскаярулетка5пуль"])
	async def roulette5bul(ctx):
		author = ctx.message.author
		ruletka = [f'Пусто, {author.mention} остался в живых.'] * 1 + [f'Выстрел, {author.mention} застрелился.'] * 5
		await ctx.send(random.choice(ruletka))
	
	@bot.command(aliases = ["рулетка6пуль", "русскаярулетка6пуль", "яебланяеблан"])
	async def roulette6bul(ctx):
		author = ctx.message.author
		eee = [f"{author.mention} застрелился от своей тупости."] * 999 + [f"{author.mention} каким то чудом смог выжить после попадания пули в лоб" * 1]
		await ctx.send(random.choice(eee))

	@bot.command(aliases = ["гугл", "поисковик"])
	async def google(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://www.google.ru/search?q={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	
	@bot.command(aliases = ["яндекс"])
	async def yandex(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://yandex.ru/search/?text={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	
	@bot.command(aliases = ["дакдак", "дакдакго", "duckduckgo"])
	async def duckduck(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://duckduckgo.com/?q={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")
	
	@bot.command(aliases = ["яхуу","яху","яхуеюблятьчтозаназвание"])
	async def yahoo(ctx, *, text):
		text = discord.utils.escape_mentions(str(text))
		textb = text.replace(' ', '+')
		link = (f"https://search.yahoo.com/search?p={textb}")
		await ctx.send(f"Ссылка на поиск по запросу {text}:  \n{link}.")


	@bot.command(aliases = ["стим","рандомстим","рандомигра"])
	async def steam(ctx):
		await ctx.send("Ссылка на рандомную игру из стима:\n<https://store.steampowered.com/explore/random>")


	@bot.command(aliases = ["слоты", "казинослоты"])
	async def slots(ctx):
		slots = ["🍓", "🍋", "🍒", "💣"]
		r1 = random.choice(slots)
		embed = discord.Embed(title="ToxCasino777", description="⚫" + "⚫" + "⚫", colour = discord.Colour.from_rgb(230,0,0))
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

	@bot.command(aliases = ["fullhelp", "полнаяпомощь", "помощьполная", "helpf", "помощьп", "хелпф", "хелпфулл"])
	async def helpfull(ctx):
		embed1 = discord.Embed(title="ToxBot help (1)", description='''
`help` —  Меню команд.
`info` — Инфо о донатерах и разработчиках.
`ver` — Версия бота на текущий момент.
''', colour = discord.Colour.from_rgb(230,0,0))
		embed2 = discord.Embed(title="ToxBot help (2)", description='''
`p` *URL* — Воспроизведение аудио с ютуба.
`p1|p2|p3...` — Воспроизведение радио.
`loop all|one|off` — Вкл/Выкл повтор.
`skip` — Пропустить трек.
`stop` — Остановить воспроизведение.
`stopradio` — Остановить радио
`rlist` — Лист всех радиостанций.''', colour = discord.Colour.from_rgb(230,0,0))
		embed3 = discord.Embed(title="ToxBot help (3)", description='''
`dem` *ссылка на пикчу* *Текст 1* *Текст 2* — Демотиватор.
`shakal` *ссылка на пикчу* *качество (0-100)* — Зашакаливание.
`quote` *ответ на сообщение|@пинг* *текст цитаты* — Создание цитаты.''', colour = discord.Colour.from_rgb(230,0,0))
		embed4 = discord.Embed(title="ToxBot help (4)", description='''
`call` *id|@пинг* *текст* — позвонить любому пользователю, текст не обязателен.
`kill` *текст|@пинг* — Убить.
`twisted` *текст|@пинг* — Свернуть шею.
`rape` *текст|@пинг* — Изнасиловать.
`eat` *текст|@пинг* — Съесть.
`drink` *текст|@пинг* — Выпить.
`give` *текст|@пинг* - Дать.
`roulette2bul|3bul|4bul...` — Русская рулетка, `roulette` — одна пуля.
`coin` - Игра в монетку
`slots` — Слоты казино.''', colour = discord.Colour.from_rgb(230,0,0))
		embed5 = discord.Embed(title="ToxBot help (5)", description='''
`randomto *число*` — Рандом до заданного числа больше одного.
`cal` — Калькулятор.
`time` — Время по МСК.
`laugh` — Смех.
`yesorno` — Да или нет.
`clear число` —  Удаление сообщений. Только для админов.
`welcomechannel` *ID канала* — Канал где будут сообщения о пришедших и ушедших участниках.
`google|yandex|duckduck|yahoo` *текст* — Поиск по этому запросу.''', colour = discord.Colour.from_rgb(230,0,0))
		embed6 = discord.Embed(title="ToxBot help (6)", description='''
`stats` *@пинг(опционально)*— Информация о пользователе (Баланс, уровень и тд).
`pay` *@пинг* *сумма* — Отдать кому либо деньги из своего кошелька.
`add` *@пинг* *сумма* — Выдать кому либо деньги (для админов).
`wd` *@пинг* *сумма* — Забрать у кого либо деньги (для админов).
`premium` — ToxBot Premium.''', colour = discord.Colour.from_rgb(230,0,0))
		embeds = [embed1, embed2, embed3, embed4, embed5, embed6]
		message = await ctx.send(embed = embed1)
		reactions = ["◀️", "▶️"]
		page = Pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, color = discord.Colour.from_rgb(230,0,0), use_exit = False, reactions = reactions, timeout = 99)
		await page.start()

	#Всякие элементарные вещи
	@bot.command(aliases = ["время"])
	async def time(ctx):
		tz_Moscow = pytz.timezone('Europe/Moscow')
		datetime_Moscow = datetime.now(tz_Moscow)
		embed = discord.Embed(title="ToxBot", description=datetime_Moscow.strftime("%H:%M:%S"), colour = discord.Colour.from_rgb(230,0,0))
		msg = await ctx.send(embed=embed)

	@bot.command(aliases = ["ничего", "** **"])
	async def nothing(ctx):
		await ctx.send("** **")

	@bot.command(aliases = ["смех"])
	async def laugh(ctx):
		def rnd_str(min_chars=6, max_chars=10, alphabet=("А", "Х", "П", "а", "х", "п", "а", "А")):
			return ''.join(random.choices(alphabet, k=random.randint(min_chars, max_chars)))
		await ctx.send(f"{(rnd_str(6, 10))}!!!")

	@bot.command()
	async def fuck_you(ctx):
		author = ctx.message.author
		await ctx.reply(f"No, {author.mention}, fuck you!")

	@bot.command(aliases = ["пинг"])
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
	async def x0x0l(ctx):
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



	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		
	@bot.command(aliases = ["радиолист", "рлист", "radiolist"])
	async def rlist(ctx):
		embed1 = discord.Embed(title = "Список радиостанций (1)", description = '''
`p1` - Шансон
`p2` - Радио Дача
`p3` - Новое Радио
`p4` - FM радио
`p5` - Дорожное Радио (Омск)
`p6` - Джаз
`p7` - Радио 70х
`p8` - Радио 80х
`p9` - Радио 90х
`p10` - хиты кантри''')
		embed2 = discord.Embed(title = "Список радиостанций (2)", description = '''
`p14` - ссср радио
`p15` - классический рок
`p16` - Ретро FM
`p17` - Хевиметал
`p18` - Украинское Радио Релакс
`p19` - детское радио
`p11` - хиты рока
`p12` - рок фм
`p13` - психоделик
Некоторые радиостанции могут временно неработать.
''')
		embeds = [embed1, embed2]
		message = await ctx.send(embed = embed1)
		reactions = ["◀️", "▶️"]
		page = Pag(bot, message, only=ctx.author, use_more=False, embeds=embeds, color = discord.Colour.from_rgb(230,0,0), use_exit = True, reactions = reactions, timeout = 99)
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


	@bot.command(aliases = ["п1", "шансон"])
	async def p1(ctx):
		await rplay(ctx, "http://chanson.hostingradio.ru:8041/chanson256.mp3")
		await ctx.send("Радио включено.\nИграет: Шансон")
	@bot.command(aliases = ["п2", "дача"])
	async def p2(ctx):
		await rplay(ctx, "http://178.217.40.125:8000/rdsat")
		await ctx.send("Радио включено. \nИграет: Радио дача")
	@bot.command(aliases = ["п3","новое"])
	async def p3(ctx):
		await rplay(ctx, "http://live.novoeradio.by:8000/novoeradio-128k")
		await ctx.send("Радио включено.\nИграет: Новое радио")
	@bot.command(aliases = ["п4", "фм"])
	async def p4(ctx):
		await rplay(ctx, "http://listen.teploe.net:8100/npkfm")
		await ctx.send("Радио включено.\nИграет: FM радио")
	@bot.command(aliases = ["п5", "дорожное"])
	async def p5(ctx):
		await rplay(ctx, "https://str.pcradio.ru/dorozhnoe_omsk-hi")
		await ctx.send("Радио включено.\nИграет: Дорожное радио (Омск)")
	@bot.command(aliases = ["п6", "джаз"])
	async def p6(ctx):
		await rplay(ctx, "http://jfm1.hostingradio.ru:14536/jlstream.mp3")
		await ctx.send("Радио включено. \nИграет: Джаз.")
	@bot.command(aliases = ["п7", "70"])
	async def p7(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/70s")
		await ctx.send("Радио включено.\nИграет: Поп радио 70х")
	@bot.command(aliases = ["п8","80"])
	async def p8(ctx):
		await rplay(ctx, "https://str.pcradio.ru/pulsradio_80s-hi")
		await ctx.send("Радио включено.\nИграет: Радио 80х")
	@bot.command(aliases = ["п9","90"])
	async def p9(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/90s")
		await ctx.send("Радио включено.\nИграет: Радио 90х")
	@bot.command(aliases = ["п10","кантри"])
	async def p10(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/acountry")
		await ctx.send("Радио включено.\nИграет: Хиты кантри")
	@bot.command(aliases = ["п11","рок"])
	async def p11(ctx):
		await rplay(ctx, "http://prmstrm.1.fm:8000/x")
		await ctx.send("Радио включено.\nИграет: Хиты рока")
	@bot.command(aliases = ["п12","рокфм"])
	async def p12(ctx):
		await rplay(ctx, "http://jfm1.hostingradio.ru:14536/rock00.mp3")
		await ctx.send("Радио включено.\nИграет: Рок FM")
	@bot.command(aliases = ["п13","психоделик"])
	async def p13(ctx):
		await rplay(ctx, "http://psyprog.rupsy.ru:8000/psyprog")
		await ctx.send("Радио включено.\nИграет: Психоделик")
	@bot.command(aliases = ["п14","ссср"])
	async def p14(ctx):
		await rplay(ctx, "https://str.pcradio.ru/SSSR-hi")
		await ctx.send("Радио включено.\nИграет: СССР радио")
	@bot.command(aliases = ["п15","классическийрок"])
	async def p15(ctx):
		await rplay(ctx, "https://str.pcradio.ru/rpr1_de_clasro-hi")
		await ctx.send("Радио включено.\nИграет: Классический рок")
	@bot.command(aliases = ["п16","ретро"])
	async def p16(ctx):
		await rplay(ctx, "https://str.pcradio.ru/retrofm_ru-hi")
		await ctx.send("Радио включено.\nИграет: Ретро FM")
	@bot.command(aliases = ["п17","хевиметалл"])
	async def p17(ctx):
		await rplay(ctx, "https://str.pcradio.ru/rpr1_de_metal-hi")
		await ctx.send("Радио включено.\nИграет: Хевиметалл")
	@bot.command(aliases = ["п18","украинское"])
	async def p18(ctx):
		await rplay(ctx, "https://str.pcradio.ru/radiorelax_ua-hi")
		await ctx.send("Радио включено.\nИграет: Украинское радио релакс")
	@bot.command(aliases = ["п19","детское"])
	async def p19(ctx):
		await rplay(ctx, "https://str.pcradio.ru/rusradio_deti-hi")
		await ctx.send("Радио включено.\nИграет: Детское радио")
		
	@bot.command(aliases = ["выключитьрадио","выклр","стопрадио", "stopr", "rstop", "рстоп"])
	async def stopradio(ctx):
		await ctx.voice_client.disconnect()
		await ctx.send("Радио остановлено.")
		
	@bot.command(aliases = ["премхелп","спермхелп","премиумхелп","премиум?","prem?","premium?","прем?"])
	async def premhelp(ctx):
		embed = discord.Embed(title = "Премиум команды", description = '''
`say` - Сообщение в консоль ToxBot.
`phz` - Х*й забей радио
`pchrst` - Христианское радио
`panime` - радио аниме из Осаки
`plofi` - lofi
`prmsh` - Радио *RAMSHTEIN*
`prhcp` - радио *Red Hot Chili Peppers*
`pkish` - Радио *Король и Шут*
`pl` - Радио *Гражданская оборона*
`p0` *ссылка на поток* - Своё радио
''', colour = discord.Colour.from_rgb(230,0,0))
		msg = await ctx.send(embed=embed)


	wtf = []
	for x in range(498):
		wtf2 = "+" * x
		wtf.append(wtf2)
	@bot.command(aliases = wtf)
	async def whatthefuckisthisshit(ctx):
		pass

	@bot.command(aliases = ["tonix", "newpremsub"])
	async def nps(ctx, *, text):
		if ctx.message.author.id == 577054248932605952 and ctx.message.author.id != 782209104210427914:
			text = int(text)
			f = open('core/premium.txt', 'a')
			f.write(f"+{text}")
			f.close()
			await ctx.send("Поздравляю с ToxBot Premium!")
		if ctx.message.author.id == 782209104210427914:
			await ctx.send("Ampernic, попросите Tonix'а пожалуйста.")
		else:
			await ctx.send("Вы не мой создатель.")


	@bot.command(aliases = ["сказать", "консольтекст"])
	async def say(ctx, *, text):
		embed = discord.Embed(title = "ToxBot Premium", description = '''Ваше сообщение доставлено.''', colour = discord.Colour.from_rgb(230,0,0))
		embed1 = discord.Embed(title = "ToxBot premium", description = prmmtext)
		text = text
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			print(text)
			await ctx.send(embed = embed)
		else:
			await ctx.send(embed = embed1)		

	@bot.command(aliases = ["христианское","chrst","пхрист"])
	async def pchrst(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext)
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://str.pcradio.ru/radio123_by-hi")
			await ctx.send("Радио включено.\nИграет: Христианское радио")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["корольишут","киш","kish","пкиш"])
	async def pkish(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://str.pcradio.ru/Korol_i_Shut-hi")
			await ctx.send("Радио включено.\nИграет: Радио Король и Шут")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["гражданскаяоборона","оборона","летов","letov","пл"])
	async def pl(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://str.pcradio.ru/Grazhdanskaja_oborona-hi")
			await ctx.send("Радио включено.\nИграет: Радио Гражданская оборона")
		else:
			await ctx.send(embed = embed)				
		
	@bot.command(aliases = ["раммштайн","рмш","rmsh","прмш"])
	async def prmsh(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://str.pcradio.ru/Rammstein-hi")
			await ctx.send("Радио включено.\nИграет: Раммштайн")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["рхчп","rhcp","прхчп"])
	async def prhcp(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://str.pcradio.ru/red_hot_chili_peppers-hi")
			await ctx.send("Радио включено.\nИграет: Red Hot Chili Peppers радио")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["хуйзабей","хз","hz","пхз"])
	async def phz(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://str.pcradio.ru/Hui_Zabey-hi")
			await ctx.send("Радио включено. \nИграет: Х*й Забей радио")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["паниме"])
	async def panime(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://japanimradio-osaka.com/radio/8000/stream")
			await ctx.send("Радио включено. \nИграет: Аниме радио из Осаки.")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["плофи","лофи","плоуфай","лоуфай","lofi"])
	async def plofi(ctx):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
		if str(ctx.author.id) in premium:
			await rplay(ctx, "https://usa9.fastcast4u.com/proxy/jamz?mp=/1")
			await ctx.send("Радио включено. \nИграет: Lofi.")
		else:
			await ctx.send(embed = embed)				
	@bot.command(aliases = ["п0","своёрадио"])
	async def p0(ctx, *, link: str):
		embed = discord.Embed(title = "ToxBot premium", description = prmmtext, color = discord.Colour.from_rgb(230,0,0))
		with open('core/premium.txt', 'r') as file:
			premium = file.read().split('+')
			txt = discord.utils.escape_mentions(link)
		if str(ctx.author.id) in premium:
			if link is not None:
				await rplay(ctx, str(txt))
				await ctx.send(f"Радио включено. \nИграет: {str(txt)}")
			else:
				await ctx.send("Вставьте ссылку.")
		else:
			await ctx.send(embed = embed)		
	try:
		print_log('wait', "Попытка подключится используя токен: {}".format(data["Token"]))
		bot.run(data["Token"])
	except Exception as e:
		print_log('err', 'Не удалось подключиться с указанным токеном \n ({})'.format(e))
else:
	print_log('err', "Инициализация прервана.")
