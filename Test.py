from discord import FFmpegPCMAudio, Activity, ActivityType
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
from random import randrange, choice
import simplejson as json
from asyncio import sleep
import subprocess
import string
import time
import random
import asyncio
import json
import requests
import discord
import os
import pytz
import sqlite3
from colorama import init
from termcolor import colored
from core.toxbot_core import *
from classes import UsTaCr
from Cybernator import Paginator as Pag

init()
print(header_logo)
print_log('wait', "Ожидание:  Инициализация")
try:
    data = core_parse_data(data)
    print_log('wait', "Импорт значений из конфига.")
    if(data["FirstBoot"] == "True"):
        print_log('warn', "Обнаружен первый запуск программы:  Переходим в режим настройки")
        first_boot_cofigure(data)
    else:
        bot = Bot(command_prefix="++", help_command=None)
        client = discord.ext.commands.Bot(command_prefix = "++")
        init_successful = True
        if(init_successful):
            print_log('info', "Инициализация прошла успешно")
            try:
                print_log("wait", "Ожидание:  Запуск базы данных")
                conn = sqlite3.connect('Poor_Warrior_of_Christ.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS economy (
                    "id"    INT,
                    "money" INT)''')
                print_log("info", "База данных загруженна.")
            except Exception as e:
                print_log('err', "Ошибка базы данных: " + e)

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="++help"))
            print_log("info", "Бот успешно cumming!")
except Exception as e:
    print_log('err', "Неудалось спарсить значения из конфига: " + str(e))

@bot.event
async def on_ready():
    print('Bot is running...')
    print(f"Name: {bot.user.name}")
    print(f"ID: {bot.user.id}")
    print('------')

@bot.event
async def on_member_join(member):
    welcome_msg = f"hi {member.name}" # You don't need to define the message.
    await member.send(welcome_msg) # You can do await member.send("message") instead of defining it.

bot.run("OTMxMjI3NDIwNzMwNzM2Njgx.YeBXHg.gZW15MNP6W-55N-rVZZYcntDV6g")