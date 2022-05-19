import discord
import asyncio
from core.toxbot_core import print_log, send_embed
from core.toxbot_core_texts import num_ver, default_thumbnail


def calls(bot):
    class make_call:
        def __init__(self):
            print_log('warn', 'Модуль звонков инициализирован')

        async def call_recognize(self, ctx, number=None, text=None):
            if number == '911':
                await self.print_call(ctx,
                                      number,
                                      text,
                                      True,
                                      'Не волнуйтесь, полиция в пути. \n \n _Предупреждаем:_ \n *Все вызовы записываются*',
                                      'полиция (тут пинг)',
                                      False)
            elif number == '255':
                await self.print_call(ctx,
                                      number,
                                      text,
                                      True,
                                      'Вы позвонили в пиццерию. \n Ваш заказ готовится.',
                                      'пиццерия (тут пинг)',
                                      False)
            elif str(number) == '@everyone' or number == '@here':
                await self.print_call(ctx,
                                      number,
                                      text,
                                      False,
                                      None,
                                      None,
                                      True)
            else:
                try:
                    number = int(number.replace('<', '').replace('>', '').replace('@', ''))
                    e = await bot.fetch_user(number)
                    if not None:
                        await self.print_call(ctx,
                                              e.mention,
                                              text)
                except:
                    await send_embed(ctx,
                                     '❌ Не удалось дозвониться ❌',
                                     'Абонент не зарегистрирован в нашей сети',
                                     f'ToxBot v{num_ver}',
                                     default_thumbnail)

        @staticmethod
        async def print_call(ctx,
                             number=None,
                             text=None,
                             custom=False,
                             custom_message=None,
                             custom_ping=None,
                             reject=False):

            embed = discord.Embed(title=f"📞 Звонок на номер `{number.replace('<', '').replace('>', '').replace('@', '')}` 📞",
                                  description="Звонок.",
                                  colour=discord.Colour.from_rgb(230, 0, 0))
            embed.set_thumbnail(url=default_thumbnail)
            msg = await ctx.send(embed=embed)

            await asyncio.sleep(1)

            update_emb = discord.Embed(title=f"📞 Звонок на номер `{number.replace('<', '').replace('>', '').replace('@', '')}` 📞",
                                       description="Звонок..",
                                       colour=discord.Colour.from_rgb(230, 0, 0))
            update_emb.set_thumbnail(url=default_thumbnail)
            await msg.edit(embed=update_emb)

            await asyncio.sleep(1)

            update_emb = discord.Embed(title=f"📞 Звонок на номер `{number.replace('<', '').replace('>', '').replace('@', '')}` 📞",
                                       description="Звонок...",
                                       colour=discord.Colour.from_rgb(230, 0, 0))
            update_emb.set_thumbnail(url=default_thumbnail)
            await msg.edit(embed=update_emb)

            await asyncio.sleep(1)

            if not reject:
                if not custom:
                    await ctx.send(f'{number}')
                    update_emb = discord.Embed(title=f"📞 Звонок на номер `{number.replace('<', '').replace('>', '').replace('@', '')}` 📞",
                                               description=f'Ожидаем ответа пользователя. \n \n _Предупреждаем:_  \n *Ваш оператор может брать плату за вызовы.*',
                                               colour=discord.Colour.from_rgb(230, 0, 0))
                    update_emb.set_thumbnail(url=default_thumbnail)
                    await msg.edit(embed=update_emb)
                    if text is not None:
                        await ctx.send(f'{text}')
                    number = int(number.replace('<', '').replace('>', '').replace('@', ''))
                    number = await bot.fetch_user(number)
                    print_log('call', f'Аббонент {ctx.author.display_name} позвонил {number.display_name}')
                else:
                    await ctx.send(f'{custom_ping}')
                    update_emb = discord.Embed(title=f"📞 Звонок на номер `{number.replace('<', '').replace('>', '').replace('@', '')}` 📞",
                                               description=custom_message,
                                               colour=discord.Colour.from_rgb(230, 0, 0))
                    update_emb.set_thumbnail(url=default_thumbnail)
                    await msg.edit(embed=update_emb)
                    if text is not None:
                        await ctx.send(f'{text}')
                        print_log('call', f'Аббонент {ctx.author.display_name} вызвал {number} ("{text}")')
                    else:
                        print_log('call', f'Аббонент {ctx.author.display_name} вызвал {number} (Причина не уточняется)')

            else:
                update_emb = discord.Embed(title=f"❌ Звонок прерван секретной службой БДБ ❌",
                                           description=f'В наше время за такое бы... \n В прочем не важно...  \n Просто не делай так больше.',
                                           colour=discord.Colour.from_rgb(230, 0, 0))
                update_emb.set_thumbnail(
                    url="https://sun1-22.userapi.com/s/v1/ig2/oLl_jHdbHnIJTa8XG8Y_S5PUu25rsWwApBOd7Zu26sqPqWL9Kq2u_AKIqGEk6-WLV7k9oFmq7-XZ7HKH-EWuVWPv.jpg?size=200x200&quality=96&crop=149,52,420,420&ava=1")
                await msg.edit(embed=update_emb)

    call_center = make_call()

    @bot.command(pass_context=True)
    async def call(ctx, number=None, *, text=None):
        await call_center.call_recognize(ctx, number, text)
