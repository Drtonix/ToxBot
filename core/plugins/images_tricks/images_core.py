import random
import discord

from datetime import datetime
import requests
from PIL import Image

from core.toxbot_core import print_log, send_embed
from core.toxbot_core_texts import default_thumbnail, num_ver, water

from core.plugins.images_tricks.simpledemotivators import Demotivator, Quote


# -	Рандомайзер фразочек -#
def random_demo():
    strings = ['Люблю когда черные квадраты обмазываются текстом'] * 25 + [
        'В чёрный квадрат постучали... \n "Демотиватор", - подумал Штирлец'] * 25 + [
                  'Текст с чёрными квадратами.'] * 25 + ['Почему квадраты чёрные?'] * 25
    return random.choice(strings)


def img_tricks(bot):
    class img_core:
        def __init__(self):
            # Выводим сообщение об успешной инициализации модуля
            print_log('warn', 'Модуль изображений инициализирован')

        @staticmethod
        async def check(ctx):
            await send_embed(ctx, 'Все работает!',
                             'На данный момент модуль изображений импортирован',
                             f'ToxBot v{num_ver}',
                             default_thumbnail)

        @staticmethod
        async def dem_create(ctx, url, text1, text2):
            outfile = './saves/demotivators/{} - Демотиватор от {}.jpg'.format(
                datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)

            ImgDem = Demotivator(text1, text2)
            try:
                ImgDem.create(url,
                              use_url=True,
                              arrange=False,
                              font_name='./core/fonts/Times.ttf',
                              watermark=water,
                              result_filename=outfile,
                              delete_file=True)
                await send_embed(ctx,
                                 'Ваш демотиватор создан', f'''
                                 _*{random_demo()}*_
                                 ''',
                                 f'ToxBot v{num_ver}',
                                 default_thumbnail)
                await ctx.send(file=discord.File(outfile))
            except Exception as e:
                await send_embed(ctx,
                                 'Не удалось создать демотиватор', f'''
                                 Произошла ошибка при создании демотиватора
                                 ({str(e)})''',
                                 f'ToxBot v{num_ver}',
                                 default_thumbnail)

        @staticmethod
        async def quote_create(ctx, nick, text):
            outfile = './saves/quotes/{} - Цитата от {}.jpg'.format(
                datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)
            ImgQuote = Quote(text, nick.display_name)
            try:
                ImgQuote.create(nick.avatar_url_as(format="jpg"),
                                use_url=True,
                                headline_text_font='./core/fonts/Verdana.ttf',
                                author_name_font='./core/fonts/Arial.ttf',
                                quote_text_font='./core/fonts/Arial.ttf',
                                result_filename=outfile)
                await ctx.send(file=discord.File(outfile))
            except Exception as e:
                await send_embed(ctx,
                                 'Не удалось добавить цитату в фонд', f'''
                                 Произошла ошибка заполнении бланка
                                 ({str(e)})''',
                                 f'ToxBot v{num_ver}',
                                 default_thumbnail)

        @staticmethod
        async def shakal_create(ctx, url, quality):
            try:
                outfile = './saves/shakalim/{} - Шакальная хуйня от {}.jpg'.format(
                    datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'), ctx.message.author.name)
                raw = requests.get(url, stream=True).raw
                image = Image.open(raw).convert('RGB')
                image.save(outfile, 'JPEG', quality=quality)
                await send_embed(ctx,
                                 'Шакалы догрызли вашу пикчу', f'''
                                 Вот ваш результат: 
                                 (Текущее качество: `{quality}`)''',
                                 f'ToxBot v{num_ver}',
                                 default_thumbnail)
                await ctx.send(file=discord.File(outfile))
            except Exception as e:
                await send_embed(ctx,
                                 'Не удалось зашакалить пикчу', f'''
                                 Произошла при получении вашей пикчи
                                 ({str(e)})''',
                                 f'ToxBot v{num_ver}',
                                 default_thumbnail)

    img_edit = img_core()

    @bot.command()
    async def img_check(ctx):
        await img_edit.check(ctx)

    @bot.command(aliases = ["demotivator", "демотиватор", "дем"])
    async def dem(ctx, url=None, text1=None, text2=None):
        if url is None or text1 is None or text2 is None:
            await send_embed(ctx,
                             'Не удалось создать демотиватор', '''
                             Неправильно введены параметры для создания
                             Напомню: `++dem ссылка "Текст 1" "Текст 2"`
                             (Кавычки у текстов обязательно!)''',
                             f'ToxBot v{num_ver}',
                             default_thumbnail)
        else:
            await img_edit.dem_create(ctx, url, text1, text2)

    # noinspection PyUnboundLocalVariable
    @bot.command(pass_context=True, aliases = ["цитата", "запомните"])
    async def quote(ctx, nick: discord.Member = None, *, text=None):
        if nick is not None and text is not None:
            await img_edit.quote_create(ctx, nick, text)
        elif ctx.message.reference and isinstance(ctx.message.reference.resolved, discord.Message):
            msg = ctx.message.reference.resolved
            await img_edit.quote_create(ctx, msg.author, msg.content)
        else:
            await send_embed(ctx,
                             'Не добавить цитату', '''
                             Неправильно введены параметры для создания
                             Напомню: `++quote пинг Текст цитаты`
                             (Или можете прислать команду в ответ на сообщение)''',
                             f'ToxBot v{num_ver}',
                             default_thumbnail)

    @bot.command(pass_context=True, aliases = ["шакал", "шакализатор"])
    async def shakal(ctx, url=None, quality=7):
        if url is None:
            await send_embed(ctx,
                             'Не удалось зашакалить пикчу', '''
                             Не введена ссылка на фото
                             Напомню: `++shakal ссылка качество`
                             Качество по умолчанию: `7`
                             (Качество можно указать от 0 до 100)''',
                             f'ToxBot v{num_ver}',
                             default_thumbnail)
        else:
            await img_edit.shakal_create(ctx, url, quality)
