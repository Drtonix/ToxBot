import simplejson as json
from colorama import init
from termcolor import colored
from core.toxbot_core_texts import *
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
    elif type == 'bank':
        print(f"         {text}")


async def send_embed(ctx, title, text, footer, thumbnail = None):
    embed = discord.Embed(title=title, description=text, colour=discord.Colour.from_rgb(230, 0, 0))
    await ctx.send(embed=embed)

def is_premium(ctx):
    with open('./core/premium.txt', 'r') as file:
        premium = file.read().split('+')
    if str(ctx.author.id) in premium:
        return True
    else:
        return False


async def notify(ctx, text):
    await ctx.send(f"Ошибка:" + str(text))
    print_log("err", "Ошибка:" + str(text))


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
                os.system("sudo apt install ffmpeg")
                print("------------------------------------------------------------------------")
            except Exception as e:
                print("------------------------------------------------------------------------")
                print_log('err', "Ошибка: " + str(e))
        if input_OS == "1":
            data["OS"] = 1
            print('''Выбранная ОС: Windows. Используем ffmpeg из коробки.
------------------------------------------------------------------------
''')
    else:
        data["OS"] = 1
        print('''Выбранная ОС: Windows (По умолчанию). Используем ffmpeg из коробки.
------------------------------------------------------------------------
''')
    print_log('wait', 'Сохраняем изменения...')
    try:
        data["FirstBoot"] = "False"     # Сбрасываем значение первого запуска
        core_save_data(data)            # Сохраняем данные
        print_log('info', 'Успех: Изменения успешно сохранены.')
        print(first_boot_success)
        time.sleep(5)
        if data["OS"] == 1:
            os.system("CLS")
        elif data["OS"] == 0:
            os.system("clear")
    except Exception as e:
        print_log('err', f'Не удалось сохранить изменения! Проверьте права на запись файла. ({str(e)})')


# Загрузка модулей

class plugins_manager():
    def __init__(self, bot, data):
        print_log('warn', 'Запуск модулей...\n')

        global plugins_counter
        global loaded_plugins
        self.plugins_counter = 0
        self.loaded_plugins = {}

        try:
            import core.plugins.database_core
            core.plugins.database_core.DB_Core(self)
        except:pass

        try:
            import core.plugins.youtube
            core.plugins.youtube.yt(bot, data, self)
        except:pass

        try:
            import core.plugins.calls
            core.plugins.calls.calls(bot, self)
        except:pass

        try:
            import core.plugins.images_tricks.images_core
            core.plugins.images_tricks.images_core.img_tricks(bot, self)
        except:pass

        try:
            import core.plugins.economy.economy_core
            core.plugins.economy.economy_core.EcoCore(bot, self)
        except Exception as e:pass

        try:
            import core.plugins.leveling_core
            core.plugins.leveling_core.level_core(bot, self)
        except Exception as e:
            print(str(e))

        try:
            import core.plugins.members.members_voices
            core.plugins.members.members_voices.mv(bot, self)
        except Exception as e:pass

        try:
            import core.plugins.members.members_core
            core.plugins.members.members_core.members_core(bot, self)
        except Exception as e:
            print(str(e))

        try:
            import core.plugins.members.members_inventory
            core.plugins.members.members_inventory.mmbr_inv(bot, self)
        except Exception as e:
            print(str(e))

        if len(self.loaded_plugins) == self.plugins_counter:
            print_log('info', f'Успех: {self.plugins_counter} плагинов успешно загружено!')
        else:
            print_log('warn', f'Предупреждение: Модули загружены не полностью\n\t\t\t\t\t\tЗагружено: {len(self.loaded_plugins)} из {self.plugins_counter} плагинов')
