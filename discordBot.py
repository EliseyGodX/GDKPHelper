import discord
import asyncio
import json
from datetime import date
from queue import Queue
from threading import Thread
import calc

start_que = Queue()
message_que = asyncio.Queue()

class LaunchingDiscordBot:
    
    async def start(self) -> bool:
        self.status = False
        
        self.thread = Thread(target=self.__connect)
        self.thread.start()
        
        if start_que.get(): self.status = True
        else: 
            await message_que.put(False)
            del self
        
    async def message(self) -> bool:
        await message_que.put(True)
        self.thread.join()
        return True

    async def close_connect(self) -> bool:
        await message_que.put(False)
        self.thread.join()
        return True
    
    def __connect(self) -> None:
        self.bot = _DiscordBot()


class _DiscordBot:
    global client, tokens, settings
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)
    with open('tokens.json', encoding='UTF-8') as f:
        tokens = json.load(f)
    
    def __init__(self) -> None:
        try: 
            client.run(tokens['discord_token'])
        except: 
            start_que.put(False)
        
    @client.event
    async def on_ready():
        start_que.put(True)
        if await message_que.get():
            guild = client.get_guild(tokens['guild_id'])
            channel = guild.get_channel(tokens['channel_id'])
            
            if 'error' in calc.CHEQUE: 
                await channel.send(embed = discord.Embed(
                        title='GDKP Helper',
                        description=calc.CHEQUE['error'],
                        color=calc.CHEQUE['discor_bot']['error_color']))
                await client.close()
        
            
            embed = discord.Embed(title=f"{calc.CHEQUE['raidName']} {calc.CHEQUE['raidMode']} ({calc.CHEQUE['countHM']} хм)", 
                                  description=calc.CHEQUE['description'], 
                                  color=calc.CHEQUE['discor_bot']['color'])

            embed.add_field(name='О рейде', value=f':euro: Общий банк: {calc.CHEQUE["wholeBank"]}\n:busts_in_silhouette: Количество рейдеров с долей: {calc.CHEQUE["raidersCount"]}', inline=True)
            if calc.CHEQUE['content_time']:
                embed.add_field(name="⠀", value=f':clock1: Время рейда: {calc.CHEQUE["raidTime"]}\n:clock130: Время сбора: {calc.CHEQUE["collectionTime"]}', inline=True)
            embed.add_field(name="⠀", value="", inline=False)
            
            if calc.CHEQUE['content_bonus']:
                value = ''
                if calc.CHEQUE['bonus']['005'] != 0: 
                    value += f"Бонус 0.5% ({int(calc.CHEQUE['wholeBank']*0.005)}г): {calc.CHEQUE['bonus']['005']} человек" + '\n'
                if calc.CHEQUE['bonus']['010'] != 0: 
                    value += f"Бонус 1% ({int(calc.CHEQUE['wholeBank']*0.010)}г): {calc.CHEQUE['bonus']['010']} человек" + '\n'
                if calc.CHEQUE['bonus']['015'] != 0: 
                    value += f"Бонус 1.5% ({int(calc.CHEQUE['wholeBank']*0.015)}г): {calc.CHEQUE['bonus']['015']} человек" + '\n'
                if calc.CHEQUE['bonus']['100'] != 0: 
                    value += f"Бонус 10% ({int(calc.CHEQUE['wholeBank']*0.100)}г): {calc.CHEQUE['bonus']['100']} человек"
                    
                embed.add_field(name="Бонусы (% от общего банка)", value=value, inline=True)
                
            
            if calc.CHEQUE['content_fine'] is True:
                value = ''
                if calc.CHEQUE['fine']['10'] != 0: 
                    value += f"Штраф 10% ({int(calc.CHEQUE['x']*0.1)}г): {calc.CHEQUE['fine']['10']} человек" + '\n'
                if calc.CHEQUE['fine']['25'] != 0: 
                    value += f"Штраф 25% ({int(calc.CHEQUE['x']*0.25)}г): {calc.CHEQUE['fine']['25']} человек" + '\n'
                if calc.CHEQUE['fine']['50'] != 0: 
                    value += f"Штраф 50% ({int(calc.CHEQUE['x']*0.5)}г): {calc.CHEQUE['fine']['50']} человек" + '\n'
                if calc.CHEQUE['fine']['75'] != 0: 
                    value += f"Штраф 75% ({int(calc.CHEQUE['x']*0.75)}г): {calc.CHEQUE['fine']['75']} человек"
                    
                embed.add_field(name="Штрафы (% от доли)", value=value, inline=True)
                
            embed.add_field(name="⠀", value="", inline=False)
            
            embed.add_field(name="ДОЛЯ", value="", inline=False) 
            value = ''
            value_ = ''
            value1 = ''
            if calc.CHEQUE['bonus']['005'] != 0: 
                value += f"С бонусом 0.5%" + '\n'
                value_ += f"{calc.CHEQUE['x'] + int(calc.CHEQUE['wholeBank']*0.005)}г" + '\n'
                value1 += f"{calc.CHEQUE['bonus']['005']} человек" + '\n'
            if calc.CHEQUE['bonus']['010'] != 0: 
                value += f"С бонусом 1%" + '\n'
                value_ += f"{calc.CHEQUE['x'] + int(calc.CHEQUE['wholeBank']*0.010)}г" + '\n'
                value1 += f"{calc.CHEQUE['bonus']['010']} человек" + '\n'
            if calc.CHEQUE['bonus']['015'] != 0: 
                value += f"С бонусом 1.5%" + '\n'
                value_ += f"{calc.CHEQUE['x'] + int(calc.CHEQUE['wholeBank']*0.015)}г" + '\n'
                value1 += f"{calc.CHEQUE['bonus']['015']} человек" + '\n'
            if calc.CHEQUE['bonus']['100'] != 0: 
                value += f"С бонусом 10%"
                value_ += f"{calc.CHEQUE['x'] + int(calc.CHEQUE['wholeBank']*0.100)}г"
                value1 += f"{calc.CHEQUE['bonus']['100']} человек"
                
            embed.add_field(name="", value=value, inline=True) 
            embed.add_field(name="", value=value_, inline=True)
            embed.add_field(name="", value=value1, inline=True)
            embed.add_field(name="⠀", value="", inline=False) 
            

            value = ''
            value_ = ''
            value1 = ''
            if calc.CHEQUE['fine']['10'] != 0: 
                value += f"Со штрафом 10%" + '\n'
                value_ += f"{int(calc.CHEQUE['x']*0.9)}г" + '\n'
                value1 += f"{calc.CHEQUE['fine']['10']} человек" + '\n'
            if calc.CHEQUE['fine']['25'] != 0: 
                value += f"Со штрафом 25%" + '\n'
                value_ += f"{int(calc.CHEQUE['x']*0.75)}г" + '\n'
                value1 += f"{calc.CHEQUE['fine']['25']} человек" + '\n'
            if calc.CHEQUE['fine']['50'] != 0: 
                value += f"Со штрафом 50%" + '\n'
                value_ += f"{int(calc.CHEQUE['x']*0.50)}г" + '\n'
                value1 += f"{calc.CHEQUE['fine']['50']} человек" + '\n'
            if calc.CHEQUE['fine']['75'] != 0: 
                value += f"Со штрафом 75%"
                value_ += f"{int(calc.CHEQUE['x']*0.25)}г"
                value1 += f"{calc.CHEQUE['fine']['75']} человек"
                
            embed.add_field(name="", value=value, inline=True) 
            embed.add_field(name="", value=value_, inline=True)
            embed.add_field(name="", value=value1, inline=True)
            embed.add_field(name="⠀", value="", inline=False) 
            embed.add_field(name=f"ОБЫЧНАЯ ДОЛЯ: {calc.CHEQUE['x']}г", value='', inline=False) 
            
            value = ''
            if calc.CHEQUE['content_course'] == 1:
                oldX = calc.CHEQUE['stat_avgX']
                calc.CHEQUE['stat_count'] += 1
                newX = calc.CHEQUE['x']
                if oldX == 0:
                    value += f":cyclone: Первый рейд этой сложности"
                elif oldX > newX:
                    procent = int(abs((newX - oldX) / oldX * 100))
                    value += f":red_circle: Доля меньше на {procent}% среднего значения (статистика ведётся по {calc.CHEQUE['stat_count']} рейдам)"
                else:
                    procent = int(abs((newX - oldX) / oldX * 100))
                    value += f":green_square: Доля больше на {procent}% среднего значения (статистика ведётся по {calc.CHEQUE['stat_count']} рейдам)"
                embed.add_field(name='⠀', value=value, inline=False) 
            
                
            embed.set_author(name=f"Рейд лидер - @{calc.CHEQUE['rlDiscord']} | {calc.CHEQUE['rlNickname']}", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            embed.set_footer(text=f"Дата публикации: {date.today()}")

            await channel.send(embed=embed)
            await client.close()
        else: await client.close()
        