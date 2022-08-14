import asyncio
import discord
import yt_dlp

from core.toxbot_core import print_log, send_embed
from core.toxbot_core_texts import num_ver


def yt(bot, data):
    # noinspection PyBroadException
    class yt_main:

        # Инициализируем модуль
        def __init__(self, bot):

            # Параметры поиска и воспроизведения
            self.YDL_OPTIONS = {'format': 'worstaudio/best',
                                'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192',
                                'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio', 'quiet': 'True',
                                "external_downloader_args": ['-loglevel', 'panic']}
            self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                   'options': '-vn'}

            # Внутренние переменные модуля
            self.voice_channel = None  # Хранилище канала воспроизведения
            self.voice_client = None  # Хранилище клиента воспроизведения

            self.is_playing = False  # Состояние клиента воспроизведения
            self.loop = None  # Состояние "залупления" всех

            self.q = []  # Массив очереди
            self.q_now = 0  # Счетчик очереди

            # Общий метод бота
            self.bot = bot

            # Выводим сообщение об успешной инициализации модуля
            print_log('warn', 'Модуль YT инициализирован')

        async def yt_searching(self, ctx, track_name):
            with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                # Читаем информацию о треке
                try:
                    # Смотрим - является ли ввод пользователя ссылкой, может не надо искать...
                    info = ydl.extract_info(track_name, download=False)
                    track_found = True
                except:
                    try:
                        # Не является - пробуем найти в поиске
                        info = ydl.extract_info(f"ytsearch:{track_name}", download=False)['entries'][0]
                        track_found = True
                    except Exception as e:
                        # Не нашли трек
                        await send_embed(ctx, 'Трек не найден', '''
                                Убедитесь, что вы ввели название правильно
                                И что ваш трек есть в библиотеке YouTube
                                _*(Если это какая то ошибка - попробуйте указать ссылку)*_''',
                                         f'ToxBot v{num_ver} - всегда рад помочь',
                                         'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
                        track_found = False

                # Если трек найден
                if track_found:

                    # Сохраняем информацию о треке который нашли
                    url = info['formats'][4]['url']  # Ссылка на поток
                    track_name = info['title']  # Название трека
                    track_time = info['duration_string']  # Длительность трека
                    track_author = ctx.message.author.name  # Кто запросил трек
                    track_thumbnail = info['thumbnail']  # Превью трека
                    self.q.append(
                        [url, track_name, track_time, track_author, track_thumbnail])  # Запись данных в массив

                    # Пытаемся запустить воспроизведение
                    try:
                        # Если трек первый - запускаем
                        if len(self.q) - 1 == self.q_now:

                            # Выводим информацию о треке
                            await send_embed(ctx, 'Сейчас играет:', f'''
                                Трек: _*{self.q[0][1]}*_
                                Продолжительность: _*{self.q[0][2]}*_
                                ''',
                                             f'Запросил: {self.q[0][3]}',
                                             self.q[0][4])  # Тут превью видео

                            # Запускаем первый трек
                            await self.playing(url, ctx)

                        # В противном случае - просто выводим информацию о добавлении трека в очередь
                        else:
                            await send_embed(ctx, 'Трек добавлен в очередь', f'''
                                Трек: _*{track_name}*_
                                Продолжительность: _*{track_time}*_
                                ''',
                                             f'Запросил: {track_author}',
                                             track_thumbnail)  # Тут превью видео
                    except Exception as e:
                        await ctx.send(str(e))

        async def next_track(self, ctx):
            try:
                # Проверяем, остались ли еще треки в очереди
                if self.q_now < len(self.q) - 1:
                    if self.loop == 'all' or self.loop is None:
                        self.q_now += 1  # Увеличиваем счетчик очереди если нет лупа на 1 трек

                    # Выводим информацию о следующем треке
                    await send_embed(ctx, 'Сейчас играет:', f'''
                                    Трек: _*{self.q[self.q_now][1]}*_
                                    Время: _*{self.q[self.q_now][2]}*_''',
                                     f'Запросил: {self.q[self.q_now][3]}',
                                     self.q[self.q_now][4])

                    # Запускаем воспроизведение
                    await self.playing(self.q[self.q_now][0], ctx)

                # Если треки кончились и бот еще в войсе
                else:
                    if self.loop is not None:  # Если "залуплено" - стартуем с начала
                        # Обнуляем счетчик
                        self.q_now = 0

                        # Выводим информацию о следующем треке
                        await send_embed(ctx, 'Сейчас играет:', f'''
                                        Трек: _*{self.q[self.q_now][1]}*_
                                        Время: _*{self.q[self.q_now][2]}*_''',
                                         f'Запросил: {self.q[self.q_now][3]}',
                                         self.q[self.q_now][4])

                        # Запускаем воспроизведение
                        await self.playing(self.q[self.q_now][0], ctx)

                    elif self.loop is None and self.voice_client:  # Нет - кикаем
                        await self.stop_playing(ctx)
            except:
                pass    # Да, это необходимо чтобы бот не подсирал в чат хуй знает откуда взятые попытки воспроизведения

        async def stop_playing(self, ctx):
            try:
                # Проверяем играет ли вообще бот, если да - отключаем
                voice_channel = ctx.author.voice.channel
                if self.voice_client.is_connected and self.is_playing:
                    await self.voice_client.disconnect()  # Отключаем бота
                    self.is_playing = False  # Снимаем флаг
                    self.q_now = 0  # Обнуляем счетчик очереди
                    self.q = []  # Отчищаем массив очереди
                    await send_embed(ctx, 'Воспроизведение остановлено',
                                     f'Прервал: {ctx.message.author.name}',
                                     'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
                if ctx.author.voice_channel == None:
                    await send_embed(ctx, 'Вы не находитесь в голосовом канале',
                                     'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
            except Exception as e:
                print_log('err', f'Ошибка: Не удалось прервать воспроизведение. ({str(e)})')

        async def playing(self, url, ctx):
            # Проверяем не подключен ли уже бот к войсу
            if self.voice_client:
                try:
                    self.voice_client.pause()  # Ставим на паузу и лишь потом включаем
                    if data["OS"] == 1:
                        self.voice_client.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source=url,
                                                                      **self.FFMPEG_OPTIONS))
                    elif data["OS"] == 0:
                        self.voice_client.play(
                            discord.FFmpegPCMAudio(executable="ffmpeg", source=url,
                                                   **self.FFMPEG_OPTIONS))

                    self.is_playing = True

                    while self.voice_client.is_playing():
                        await asyncio.sleep(1)

                    await self.next_track(ctx)
                except Exception as e:
                    print_log('err', f'Ошибка: Не удалось запустить воспроизведение. ({str(e)})')
            else:
                try:
                    self.voice_client = await self.voice_channel.connect()
                    if data["OS"] == 1:
                        self.voice_client.play(discord.FFmpegPCMAudio(executable=r"./ffmpeg/ffmpeg.exe", source=url,
                                                                      **self.FFMPEG_OPTIONS))
                    elif data["OS"] == 0:
                        self.voice_client.play(
                            discord.FFmpegPCMAudio(executable="ffmpeg", source=url,
                                                   **self.FFMPEG_OPTIONS))
                    self.is_playing = True

                    while self.voice_client.is_playing():
                        await asyncio.sleep(1)

                    await self.next_track(ctx)
                except Exception as e:
                    print_log('err', f'Ошибка: Не удалось запустить воспроизведение. ({str(e)})')

    ytx = yt_main(bot)

    @bot.command(pass_context=True)
    async def p(ctx, *, track=None):
        if track is not None:
            try:
                ytx.voice_channel = ctx.message.author.voice.channel
                ytx.voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
                await ytx.yt_searching(ctx, track)
            except:
                print_log('err', f'Пользователь {ctx.message.author.name} не находится в войсе')
                await send_embed(ctx, 'Не удалось запустить воспроизведение', '''
                                Вы не находитесь в войсе.
                                Вы можете добавить трек в очередь только находясь в войсе.''',
                                 'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
        else:
            await send_embed(ctx, 'Не удалось добавить трек', '''
                            Вы не ввели название трека или ссылку''',
                             'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')

    @bot.command(pass_context=True)
    async def skip(ctx):
        await ytx.next_track(ctx)

    @bot.command(pass_context=True)
    async def loop(ctx, type='off'):
        if type == 'off':
            ytx.loop = None
            await send_embed(ctx, 'Повтор отключен', '''
                            Текущий режим повтора: _*Выключен*_
                            После окончания очереди бот отключится.''',
                            'Но ты всегда можешь добавить еще треков.',
                            'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
        elif (ytx.loop is None or ytx.loop == 'one') and type == 'all':
            ytx.loop = type
            await send_embed(ctx, 'Повтор включен', '''
                            Текущий режим повтора: _*Включен (Все треки)*_
                            Повторяется вся очередь.''',
                            'Вы можете добавлять еще треки в очередь.',
                            'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
        elif (ytx.loop is None or ytx.loop == 'all') and type == 'one':
            ytx.loop = type
            await send_embed(ctx, 'Повтор включен', '''
                            Текущий режим повтора: _*Включен (Один трек)*_
                            Повторяется лишь текущий трек.''',
                            'Когда он тебе надоест - можешь отключить или сменить режим.',
                            'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')

    @bot.command(pass_context=True)
    async def stop(ctx):
        if ytx.voice_client and ytx.voice_client.is_playing():
            await ytx.stop_playing(ctx)
        else:
            await send_embed(ctx, 'Невозможно прервать воспроизведение.',
                             'Бот ничего не играет.',
                             'Но ты всегда можешь что-то включить.',
                             'https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')

    @bot.command()
    async def qnow(ctx):
        await ctx.send(f'qnow: {ytx.q_now} \n len(q): {len(ytx.q)} \n loop type: {ytx.loop}')
