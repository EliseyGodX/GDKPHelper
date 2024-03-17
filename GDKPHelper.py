import asyncio
import discordBot
import windows 
import calc

if __name__ == '__main__':

    discord_bot = discordBot.LaunchingDiscordBot()
    asyncio.run(discord_bot.start())
    
    window = windows.RootWindow()
    window.change_label(discord_bot.status)
    window.protocol("WM_DELETE_WINDOW", window.on_closing)
    window.mainloop()
    flag = 1
    while not discord_bot.status and flag != 3 :
        window_entry = windows.DiscordBotEntryToken()
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window_entry.mainloop()
        del window_entry
        asyncio.run(discord_bot.start())
        flag += 1
        
    flag = False
    if 'error' not in calc.CHEQUE:
        while not flag:
            flag = asyncio.run(discord_bot.message())
    else: 
        while not flag:
            flag = asyncio.run(discord_bot.close_connect())
        
    
    
    
    