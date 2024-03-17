import customtkinter
import json
from queue import Queue
import calc

global que
que = Queue()

class DiscordBotEntryToken(customtkinter.CTk):
    
    def __init__(self) -> None:
        super().__init__()
        
        with open('settings.json') as f:
            self.settings = json.load(f)['windowsGlobal']
        
        with open('tokens.json') as f:
            self.tokens = json.load(f)
        
        self.title("GDKP Helper: ожидание токена")
        self.geometry(f"{900}x{180}")

        customtkinter.set_appearance_mode(self.settings["apperance_mode"])
        customtkinter.set_default_color_theme(self.settings["color_mode"])
        customtkinter.set_widget_scaling(
            int(self.settings["scaling_event"].replace("%", "")) / 100)
        
        self.grid_rowconfigure((1), weight=0)
        self.grid_rowconfigure((1, 2), weight=0)

        customtkinter.CTkLabel(self, text="Токен дискорд бота не был обнаружен или некорректен", 
                               font=customtkinter.CTkFont(size=20, weight="bold")).grid(
                                   row=0, column=0, padx=20, pady=(20, 10))

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Введите токен")
        self.entry.grid(row=1, column=0, columnspan=1, padx=(5, 5), pady=(20, 2), sticky="nsew")
        customtkinter.CTkButton(self, border_width=2, text_color=("gray10", "#DCE4EE"), text='Insert', 
                                command=lambda: self.insert(self.entry.get())).grid(
            row=1, column=1, padx=(100, 100), pady=(2, 20), sticky="nsew")
                                
    
    def insert(self, token: str) -> None:
        self.tokens['discord_token'] = token
        with open("tokens.json", "w", encoding="utf-8") as file:
            json.dump(self.tokens, file, indent=2)
        self.on_closing()
    
    def on_closing(self) -> None:
        self.destroy()
        self.quit()
    
    
    
    
class _CheckWindow(customtkinter.CTk):
    
    def __init__(self, error: str = None) -> None:
        super().__init__()
        
        with open('settings.json', encoding='UTF-8') as f:
            self.settings = json.load(f)['windowsGlobal']
        
        self.title("GDKPHelper: check")
        self.geometry(f"{800}x{300}")

        customtkinter.set_appearance_mode(self.settings["apperance_mode"])
        customtkinter.set_default_color_theme(self.settings["color_mode"])
        customtkinter.set_widget_scaling(
            int(self.settings["scaling_event"].replace("%", "")) / 100)   
    
        self.grid_rowconfigure((1), weight=0)
        self.grid_rowconfigure((1, 2), weight=0)
        
        self.textbox = customtkinter.CTkTextbox(self, width=500)
        self.textbox.grid(row=1, column=1, padx=20, pady=20,sticky="nsew")
        if error is not None:
            self.textbox.insert("0.0", error)
        else:
            self.textbox.insert("0.0", calc.pcheque())
                
        self.button_fix = customtkinter.CTkButton(self, command=self._fix, text='Исправить')
        self.button_fix.grid(row=2, column=1, padx=20, pady=10)        
        
        self.button_next = customtkinter.CTkButton(self, command=self._next, text='Сделать выгрузку')
        self.button_next.grid(row=2, column=2, padx=20, pady=10)

    
    def _next(self) -> None:
        que.put(True)
        self.quit()
        self.destroy()
        
    def _fix(self) -> None:
        self.on_closing()
        
    def on_closing(self) -> None:
        que.put(False)
        self.quit()
        self.destroy()
    
    
    
    
class RootWindow(customtkinter.CTk):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.content = {}
        
        with open('settings.json', encoding="utf-8") as f:
            self.settings = json.load(f)
            self.addon = self.settings['addon']
        
        customtkinter.set_appearance_mode(self.settings['windowsGlobal']["apperance_mode"])
        customtkinter.set_default_color_theme(self.settings['windowsGlobal']["color_mode"])
        customtkinter.set_widget_scaling(
            int(self.settings['windowsGlobal']["scaling_event"].replace("%", "")) / 100)
        
        self.title("GDKPHelper (ru)")
        self.geometry(f"{1000}x{630}")
        
        
        # Left bar
        self.sidebar_set = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_set.grid(row=0, column=0, rowspan=9, sticky="nsew")
        
        self.label_botStatus = customtkinter.CTkLabel(self.sidebar_set, text="Bot offline", 
                               font=customtkinter.CTkFont(size=20, weight="bold"), text_color='#FF0000')
        self.label_botStatus.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_set.grid_rowconfigure(1, weight=1)
        
        customtkinter.CTkLabel(self.sidebar_set, text="Color Mode:", anchor="w").grid(row=4, column=0, padx=20, pady=(10, 0))
        self.color_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_set, values=["blue", "green", "dark-blue"],
                                                                       command=self.change_color_mode_event)
        self.color_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(5, 5))
        
        customtkinter.CTkLabel(self.sidebar_set, text="Appearance Mode:", anchor="w").grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_set, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        
        customtkinter.CTkLabel(self.sidebar_set, text="UI Scaling:", anchor="w").grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_set, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))
        
        self.appearance_mode_optionemenu.set(self.settings['windowsGlobal']["apperance_mode"])
        self.scaling_optionemenu.set(self.settings['windowsGlobal']["scaling_event"])
        self.color_mode_optionemenu.set(self.settings['windowsGlobal']["color_mode"])
        
        
        
        self.grid_columnconfigure((1, 2), weight=1)
        
        
        # First row
        self.sidebar_raidLeader = customtkinter.CTkFrame(self, corner_radius=10)
        self.sidebar_raidLeader.grid(row=0, column=1, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_raidLeader, text="Рейд Лидер: ",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=0, column=0, padx=2, pady=5)
        self.entry_raidLeader_discordName = customtkinter.CTkEntry(self.sidebar_raidLeader, 
                                                                   placeholder_text=self.settings['rootWindow']['discordRL'])
        self.entry_raidLeader_discordName.grid(row=0, column=1, padx=2, pady=5, sticky="nsew")
        self.entry_raidLeader_nickName = customtkinter.CTkEntry(self.sidebar_raidLeader, 
                                                                placeholder_text=self.settings['rootWindow']['nickNameRL'])
        self.entry_raidLeader_nickName.grid(row=0, column=2, padx=2, pady=5, sticky="nsew")
        
        self.content['rlDiscord'] = self.settings['rootWindow']['discordRL']
        self.content['rlNickname'] = self.settings['rootWindow']['nickNameRL']

        
        
        self.sidebar_raid = customtkinter.CTkFrame(self, corner_radius=10)
        self.sidebar_raid.grid(row=0, column=2, sticky="nsew")
        customtkinter.CTkLabel(self.sidebar_raid, text="Рейд: ",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=0, column=0, padx=2, pady=5)
        self.optionemenu_raid_raidName = customtkinter.CTkOptionMenu(self.sidebar_raid, command=self.command_optionmenu_raid_raidName, width=50,
                                                                     values=[raid for raid in self.settings['raidStat'][self.addon]])
        self.optionemenu_raid_raidName.grid(row=0, column=1, padx=2, pady=5)
        self.optionemenu_raid_raidMode = customtkinter.CTkOptionMenu(self.sidebar_raid, command=self.command_optionmenu_raid_raidMode, width=50,
                                                                     values=['10', '25'])
        self.optionemenu_raid_raidMode.grid(row=0, column=2, padx=2, pady=5)
        self.entry_raid_countHM = customtkinter.CTkEntry(self.sidebar_raid, placeholder_text='Убитых в хм')
        self.entry_raid_countHM.grid(row=0, column=3, padx=2, pady=5, sticky="nsew")
        
        self.optionemenu_raid_raidName.set(self.settings['rootWindow']["raidName"])
        self.optionemenu_raid_raidMode.set(self.settings['rootWindow']["raidMode"])
        
        self.content['raidName'] = self.settings['raidStat'][self.addon][self.settings['rootWindow']["raidName"]]['title']
        self.content['raidMode'] = self.settings['rootWindow']["raidMode"]
        self.content['raid'] = self.settings['rootWindow']["raidName"]
        
        # Second row
        self.grid_rowconfigure(1, weight=1)
        self.string_input_button = customtkinter.CTkButton(self, text="Добавить описание", fg_color="transparent", border_width=1, 
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=1, column=1, padx=20, pady=10, columnspan=2, sticky="ew")
        self.content['description'] = self.settings['rootWindow']['description']
        
        # Third row
        customtkinter.CTkLabel(self, text="О рейде",
                               font=customtkinter.CTkFont(size=20, weight="bold")).grid(
                                   row=2, column=1, padx=20, pady=10, columnspan=2)
               
                               
        # Fourth row
        self.sidebar_aboutRaid = customtkinter.CTkFrame(self, corner_radius=10)
        self.sidebar_aboutRaid.grid(row=3, column=1, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.sidebar_aboutRaid.columnconfigure((0, 1), weight=1)
        
        self.entry_aboutRaid_raidTime = customtkinter.CTkEntry(self.sidebar_aboutRaid, placeholder_text='Время рейда')
        self.entry_aboutRaid_raidTime.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.entry_aboutRaid_collectionTime = customtkinter.CTkEntry(self.sidebar_aboutRaid, placeholder_text='Время сборов')
        self.entry_aboutRaid_collectionTime.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.entry_aboutRaid_wholeBank = customtkinter.CTkEntry(self.sidebar_aboutRaid, placeholder_text='Общий банк', border_width=5)
        self.entry_aboutRaid_wholeBank.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.entry_aboutRaid_raidersCount = customtkinter.CTkEntry(self.sidebar_aboutRaid, placeholder_text='Рейдеров с долей', border_width=5)
        self.entry_aboutRaid_raidersCount.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        
        # Fifth row
        self.sidebar_bonus = customtkinter.CTkFrame(self, corner_radius=10)
        self.sidebar_bonus.grid(row=4, column=1, sticky="nsew", padx=20, pady=10)
        self.sidebar_bonus.columnconfigure((0, 1), weight=1)
        
        customtkinter.CTkLabel(self.sidebar_bonus, text="Бонусы:",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=0, column=0, columnspan=2, padx=5, pady=5)
        
        customtkinter.CTkLabel(self.sidebar_bonus, text="0.5%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=1, column=0, padx=5, pady=5)
        self.entry_bonus_005 = customtkinter.CTkEntry(self.sidebar_bonus, placeholder_text='0')
        self.entry_bonus_005.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_bonus, text="1%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=2, column=0, padx=5, pady=5)
        self.entry_bonus_010 = customtkinter.CTkEntry(self.sidebar_bonus, placeholder_text='0')
        self.entry_bonus_010.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_bonus, text="1.5%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=3, column=0, padx=5, pady=5)
        self.entry_bonus_015 = customtkinter.CTkEntry(self.sidebar_bonus, placeholder_text='0')
        self.entry_bonus_015.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_bonus, text="10%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=4, column=0, padx=5, pady=5)
        self.entry_bonus_100 = customtkinter.CTkEntry(self.sidebar_bonus, placeholder_text='0')
        self.entry_bonus_100.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        
        self.content['content_bonus'] = False
        
        
        self.sidebar_fine = customtkinter.CTkFrame(self, corner_radius=10)
        self.sidebar_fine.grid(row=4, column=2, sticky="nsew", padx=20, pady=10)
        self.sidebar_fine.columnconfigure((0, 1), weight=1)
        
        customtkinter.CTkLabel(self.sidebar_fine, text="Штрафы:",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=0, column=0, columnspan=2, padx=5, pady=5)
        
        customtkinter.CTkLabel(self.sidebar_fine, text="10%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=1, column=0, padx=5, pady=5)
        self.entry_fine_10 = customtkinter.CTkEntry(self.sidebar_fine, placeholder_text='0')
        self.entry_fine_10.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_fine, text="25%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=2, column=0, padx=5, pady=5)
        self.entry_fine_25 = customtkinter.CTkEntry(self.sidebar_fine, placeholder_text='0')
        self.entry_fine_25.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_fine, text="50%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=3, column=0, padx=5, pady=5)
        self.entry_fine_50 = customtkinter.CTkEntry(self.sidebar_fine, placeholder_text='0')
        self.entry_fine_50.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        
        customtkinter.CTkLabel(self.sidebar_fine, text="75%",
                               font=customtkinter.CTkFont(size=15)).grid(
                                   row=4, column=0, padx=5, pady=5)
        self.entry_fine_75 = customtkinter.CTkEntry(self.sidebar_fine, placeholder_text='0')
        self.entry_fine_75.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        
        self.content['content_fine'] = False
        
        
        
        # Sixth row
        customtkinter.CTkLabel(self, text="Отображение контента",
                               font=customtkinter.CTkFont(size=20, weight="bold")).grid(
                                   row=5, column=1, padx=20, pady=10, columnspan=2)
                      
                               
        #Seventh row
        self.sidebar_content = customtkinter.CTkFrame(self, corner_radius=10)
        self.sidebar_content.grid(row=6, column=1, columnspan=2, sticky="nsew", padx=20, pady=10)
        self.sidebar_content.columnconfigure((0, 1), weight=1)
        
        self.switch_content_time = customtkinter.CTkSwitch(self.sidebar_content, text="Показывать время рейда и сборов")
        self.switch_content_time.grid(row=0, column=0, padx=5, pady=5)
        self.switch_content_course = customtkinter.CTkSwitch(self.sidebar_content, text="Показывать изменение доли")
        self.switch_content_course.grid(row=1, column=0, padx=5, pady=5)
        self.switch_content_bonus = customtkinter.CTkSwitch(self.sidebar_content, text="Показывать бонусы")
        self.switch_content_bonus.grid(row=0, column=1, padx=5, pady=5)
        self.switch_content_fine = customtkinter.CTkSwitch(self.sidebar_content, text="Показывать штрафы") 
        self.switch_content_fine.grid(row=1, column=1,padx=5, pady=5)
        
        if self.settings['rootWindow']['switch_content_time'] == 1: self.switch_content_time.select()
        if self.settings['rootWindow']['switch_content_course'] == 1: self.switch_content_course.select()
        if self.settings['rootWindow']['switch_content_bonus'] == 1: self.switch_content_bonus.select()
        if self.settings['rootWindow']['switch_content_fine'] == 1: self.switch_content_fine.select()
        
        self.content['content_time'] = False
        self.content['content_course'] = False
        self.content['content_bonus'] = False
        self.content['content_fine'] = False
        
        # Eighth row 
        self.grid_rowconfigure(7, weight=1)
        self.string_input_button = customtkinter.CTkButton(self, text="Далее", command=self.next)
        self.string_input_button.grid(row=7, column=1, padx=20, pady=10, columnspan=2, sticky="ew")
        
        self.content['content_course'] = False
        
    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.settings['windowsGlobal']["apperance_mode"] = new_appearance_mode
        
    def change_color_mode_event(self, new_color_mode: str) -> None:
        self.settings['windowsGlobal']["color_mode"] = new_color_mode

    def change_scaling_event(self, new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        self.settings['windowsGlobal']["color_mode"] = new_scaling_float
        
        
    def change_label(self, status: bool) -> None:
        if status: self.label_botStatus.configure(text_color='#FFFFFF', text='Bot online')
        else: self.label_botStatus.configure(text_color='#FF0000', text='Bot offline')
        
    def command_optionmenu_raid_raidName(self, raidName: str) -> None:
        self.content['raidName'] = self.settings['raidStat'][self.addon][raidName]['title']
        
    def command_optionmenu_raid_raidMode(self, raidMode: str) -> None: 
        self.content['raidMode'] = raidMode
    
    def open_input_dialog_event(self) -> None:
        dialog = customtkinter.CTkInputDialog(text="Введите описание:", title="GDKP Helper: Description")
        self.content['description'] = dialog.get_input()
        
    def next(self) -> None: 
        
        def to_int(value: str) -> int:
            try: 
                return abs(int(value))
            except:
                return 0
            
        
        def checkWindow(error: str = None) -> None:
            if error is None: window = _CheckWindow()
            else: window = _CheckWindow(error)
            window.protocol("WM_DELETE_WINDOW", window.on_closing)
            window.mainloop()
            
        self.content['wholeBank'] = to_int(self.entry_aboutRaid_wholeBank.get())
        self.content['raidersCount'] = to_int(self.entry_aboutRaid_raidersCount.get())
        
        if self.content['wholeBank'] == '' or self.content['raidersCount'] == '':
            checkWindow({'error': 'Не заполнены обязательные поля (общий банк и количество рейдеров)'})
            return
            
        self.settings['rootWindow']['switch_content_time'] = self.switch_content_time.get()
        self.settings['rootWindow']['switch_content_course'] = self.switch_content_course.get()
        self.settings['rootWindow']['switch_content_bonus'] = self.switch_content_bonus.get()
        self.settings['rootWindow']['switch_content_fine'] = self.switch_content_fine.get()
        
        if self.entry_raidLeader_discordName.get() != '': 
            self.content['rlDiscord'] = self.entry_raidLeader_discordName.get()
            self.settings['rootWindow']['discordRL'] = self.content['rlDiscord']
        else:
            self.content['rlDiscord'] = self.settings['rootWindow']['discordRL']
            
        if self.entry_raidLeader_nickName.get() != '': 
            self.content['rlNickname'] = self.entry_raidLeader_nickName.get()
            self.settings['rootWindow']['nickNameRL'] = self.content['rlNickname']
        else:
            self.content['rlNickname'] = self.settings['rootWindow']['nickNameRL']
        self.content['raid'] = self.optionemenu_raid_raidName.get()
                        
        self.content['bonus'] = {
            '005': to_int(self.entry_bonus_005.get()),
            '010': to_int(self.entry_bonus_010.get()),
            '015': to_int(self.entry_bonus_015.get()),
            '100': to_int(self.entry_bonus_100.get())
        }
        self.content['fine'] = {
            '10': to_int(self.entry_fine_10.get()),
            '25': to_int(self.entry_fine_25.get()),
            '50': to_int(self.entry_fine_50.get()),
            '75': to_int(self.entry_fine_75.get())
        }
        self.content['raiders_norOrdinary'] = (self.content['raidersCount'] - 
            sum(self.content['bonus'].values()) - sum(self.content['fine'].values()))
        
        if self.content['raiders_norOrdinary'] < 0:
            checkWindow({'error': 'Людей с долями и бонусами больше, чем всего рейдеров. Получивший штраф не может получить бонус'})
            return
        
        if self.settings['rootWindow']['switch_content_time'] == 1:
            self.content['content_time'] = True
            self.content['raidTime'] = self.entry_aboutRaid_raidTime.get()
            self.content['collectionTime'] = self.entry_aboutRaid_collectionTime.get()
            
        if self.settings['rootWindow']['switch_content_course'] == 1:
            self.content['content_course'] = True
        
        if self.settings['rootWindow']['switch_content_bonus'] == 1:
            self.content['content_bonus'] = True
        
        if self.settings['rootWindow']['switch_content_fine'] == 1:
            self.content['content_fine'] = True
            
        
        self.content['discor_bot'] = {
            'color': self.settings['discord_bot']['color'],
            'error_color': self.settings['discord_bot']['error_color'],
            }
        self.content['countHM'] = to_int(self.entry_raid_countHM.get())
    
        calc.calculator(self.content)
        checkWindow()

        if que.get():
            if 'error' not in calc.CHEQUE:
                calc.CHEQUE['stat_count'] = self.settings['raidStat'][self.addon][self.content['raid']]['mode'][self.content['raidMode']]['count']
                calc.CHEQUE['stat_avgX'] = self.settings['raidStat'][self.addon][self.content['raid']]['mode'][self.content['raidMode']]['avgX']
                
                self.settings['raidStat'][self.addon][self.content['raid']]['mode'][self.content['raidMode']]['count'] += 1
                self.settings['raidStat'][self.addon][self.content['raid']]['mode'][self.content['raidMode']]['avgX'] = (
                    (calc.CHEQUE['stat_avgX'] + calc.CHEQUE['x']) / (calc.CHEQUE['stat_count'] + 1)
                )
                with open("settings.json", "w", encoding="UTF-8") as file:
                    json.dump(self.settings, file, indent=2)
                
            self.on_closing()
        else: return
            
    def on_closing(self) -> None:
        self.destroy()
        self.quit()
        
    
        