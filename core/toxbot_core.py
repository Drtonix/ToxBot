from core.plugins.calls import *
import simplejson as json
from colorama import init
from termcolor import colored
import discord
import time
import os

# Вывод в консоль

global print_log
global notify


def print_log(type, text):
    if type == 'err':
        print(colored("[ ", "white"), colored(" ERROR ", "red"), colored(" ] {}", "white").format(text))
    elif type == 'warn':
        print(colored("[ ", "white"), colored(" WARN  ", "yellow"), colored(" ] {}", "white").format(text))
    elif type == 'info':
        print(colored("[ ", "white"), colored(" INFO  ", "green"), colored(" ] {}", "white").format(text))
    elif type == 'wait':
        print(colored("[ ", "white"), colored(" . . . ", "cyan"), colored(" ] {}", "white").format(text))
    elif type == 'call':
        print(colored("[ ", "white"), colored(" CALL  ", "magenta"), colored(" ] {}", "white").format(text))
    elif type == 'image':
        print(colored("[ ", "white"), colored(" IMAGE ", "magenta"), colored(" ] {}", "white").format(text))


async def send_embed(ctx, title, text, footer, thumbnail):
    embed = discord.Embed(title=title, description=text, colour=discord.Colour.from_rgb(230, 0, 0))
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=footer,
                     icon_url='https://media.discordapp.net/attachments/939136925095297055/943240401031135303/ToxDsBot.png')
    await ctx.send(embed=embed)


async def notify(ctx, text):
    await ctx.send(f"Ошибка: " + str(text))
    print_log("err", "Ошибка: " + str(text))


# Работа с конфигом

def core_parse_data(data):
    with open("./core/toxbot.json") as toxbot:
        data = json.load(toxbot)
        return data


def core_save_data(data):
    with open('./core/toxbot.json', 'w') as toxbot:
        json.dump(data, toxbot, indent=4)


# Мастер настройки

def first_boot_cofigure(data):
    print(first_boot_header)
    print(first_boot_enterToken)
    input_token = input("Введите токен бота (Или оставьте пустым для дефолта): ")
    if input_token != "":
        print(first_boot_newToken.format(input_token))
        Token = input_token
        data["Token"] = Token
    else:
        print("Принято решение использовать дефолтный токен. Успешно.")

    print(first_boot_enterOS)
    input_OS = input("Введите ID ОС (Для Windows - 1, для Linux - 0, по умолчанию 1): ")
    if input_OS != "":
        if input_OS == "0":
            data["OS"] = 0
            print('''Выбранная ОС: Linux. Пробуем установить ffmpeg для работы ++play
            ''')
            try:
                os.system("apt install ffmpeg")
                print("-------------------------------------------------------------------")
            except Exception as e:
                print("-------------------------------------------------------------------")
                print_log('err', "Ошибка: " + str(e))
        if input_OS == "1":
            data["OS"] = 1
            print('''Выбранная ОС: Windows. Используем ffmpeg из коробки.
-------------------------------------------------------------------
''')
    else:
        data["OS"] = 1
        print('''Выбранная ОС: Windows (По умолчанию). Используем ffmpeg из коробки.
-------------------------------------------------------------------
''')
    print_log('wait', 'Сохраняем изменения...')
    try:
        data["FirstBoot"] = "False"  # Сбрасываем значение первого запуска
        core_save_data(data)  # Сохраняем данные
        print_log('info', 'Изменения успешно сохранены.')
        print(first_boot_success)
        time.sleep(5)
        if data["OS"] == 1:
            os.system("CLS")
        elif data["OS"] == 0:
            os.system("clear")
    except Exception as e:
        print_log('err', f'Неудалось сохранить изменения! Проверьте права на запись файла. ({str(e)})')


# Загрузка модулей

def plugins(discord, bot, data):
    print_log('wait', 'Запуск модулей...')

    import core.plugins.youtube
    core.plugins.youtube.yt(bot, data)

    asyncio.run(calls(discord, bot, data, print_log, notify))

    import core.plugins.images_tricks.images_core
    core.plugins.images_tricks.images_core.img_tricks(bot)

    print_log('info', 'Успех: Модули инициализированы.')
