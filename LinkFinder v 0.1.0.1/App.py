import os
import io
from typing import Union, Callable

from PIL import Image

import tkinter
from tkinter import filedialog as fd
import customtkinter

import webbrowser

from Libs import Check_phase_func as cp
from Libs import Config_func as config
from Libs import Data_func as db


class App(customtkinter.CTk):
    # Основные параметры приложения / main parametres of app
    def __init__(self):
        super().__init__()
        self.params()
        self.find_center()

        self.title('| LinkFinder v 0.1.0.2 |')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Размещаем элементы главного окна
        self.put_main_frames()
        
        # Привязываем быстрые сочетания для главного окна
        self.keyboard_bind()
        
        # Проверка версий драйверов
        versions = cp.find_drivers(cp.try_driver_last_version())
        if versions[0] == "warning":
            Messange(self, self, 'warning', 'Warning 0.1', 
            'Не найден драйвер подходящей версии,\n'+
            'возможна работа только c базой данных.'+
            '\n\nВерсия вашего браузера:\n'+ versions[1], skip_button=True)
    #============================================================================================================
    # Технические функции 
    # Функция присвоения главных параметров / main parametres function
    def params(self):
        #(подгружаем данные из файла конфигурации)
        self.database = db.Database()
        self.config_data = config.get_config()
        #(применяем сохраненную конфигурацию)
        customtkinter.set_appearance_mode(self.config_data['USER_SETTINGS']['theme'])

        self.text_colors = ("#4682B4", "#FFFAFA")

        self.APP_WIDTH = 780
        self.APP_HEIGHT = 520

        self.MSG_WIDTH = 400
        self.MSG_HEIGHT = 200

        self.OPT_WIDTH = 500
        self.OPT_HEIGHT = 500
    
    # Функция для поиска координат центра экрана / function to find coordinates of screen center
    def find_center(self):
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        # Координаты центра экрана для уведомлений и окон
        self.X_APP = (SCREEN_WIDTH / 2) - (self.APP_WIDTH / 2)
        self.Y_APP = (SCREEN_HEIGHT / 2) - (self.APP_HEIGHT / 2)

        self.X_MSG = (SCREEN_WIDTH / 2) - (self.MSG_WIDTH / 2)
        self.Y_MSG = (SCREEN_HEIGHT / 2) - (self.MSG_HEIGHT / 2)

        self.X_OPT = (SCREEN_WIDTH / 2) - (self.OPT_WIDTH / 2)
        self.Y_OPT = (SCREEN_HEIGHT / 2) - (self.OPT_HEIGHT / 2)
   
    # Функция размещения всех фреймов / frame position function
    def put_main_frames(self):
        self.left_main_frame = Left_main(self)
        self.left_main_frame.pack(side=tkinter.LEFT, fill='y')
        
        self.search_frame = Search(self)
        self.search_frame.pack(side=tkinter.TOP, fill='x', padx=5, pady=5)
        
        self.result_and_save_frame = Result_and_save(self)
        self.result_and_save_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
    
    # Функция закрытия приложения / app closing function
    def on_closing(self, event=0):
        self.database.close_connection()
        self.destroy()
    
    # Функция привязки нажатия клавиш и их сочетаний / keyboard bind function
    def keyboard_bind(self):
        self.bind('<Control-q>', lambda event : self.quit())
        self.bind('<Control-o>', lambda event : Options(self))
    
    # Функция обновления параметров / refresh app with new config parametres
    def refresh_by_config(self):
        customtkinter.set_appearance_mode(self.config_data['USER_SETTINGS']['theme'])
        self.result_and_save_frame.destroy()
        self.result_and_save_frame = Result_and_save(self)
        self.result_and_save_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
#============================================================================================================
# Класс основной левой группы виджетов / class of left frame
class Left_main(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=220, corner_radius=0, bg_color="transparent")
        self.main_opt = Options_list(self).pack(padx=5, pady=5)
        self.serch_opt = Search_options(self, master.text_colors).pack(padx=5, pady=5)
        self.save_opt = Save_options(self, master.text_colors).pack(padx=5, pady=5, expand=True, fill='y')

# Класс виджета поисковой строки / class of search frame
class Search(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=40, corner_radius=10, bg_color="transparent")       
        self.search_img = customtkinter.CTkImage(Image.open('./Design/icon-search-outline.png'), size=(15,15))
        self.clear_img = customtkinter.CTkImage(Image.open('./Design/icon-cross-outline.png'))
        self.entry = customtkinter.CTkEntry(self, placeholder_text=None,
                                            height=30,
                                            corner_radius=8, border_width=1)
        self.entry.pack(side=tkinter.LEFT, expand=True, fill='x', padx=5, pady=5)

        self.clear_button = customtkinter.CTkButton(self, image=self.clear_img,
                                                    height=30, width=30,
                                                    corner_radius=8, border_width=1,
                                                    border_color='#0267A7', fg_color="transparent", bg_color="transparent",
                                                    text=None,
                                                    command=self.clear)
        self.clear_button.pack(side=tkinter.LEFT, padx=(0, 5), pady=5)
        master.bind('<Control-n>', lambda event : self.clear())
        self.search_button = customtkinter.CTkButton(self, image=self.search_img,
                                                    height=30, width=40,
                                                    corner_radius=8, border_width=1,
                                                    border_color='#0267A7', fg_color="transparent", bg_color="transparent",
                                                    compound="right",
                                                    text="Найти",
                                                    text_color='#0267A7',
                                                    command=None)
        self.search_button.pack(side=tkinter.RIGHT, padx=(0, 5), pady=5)
        master.bind('<Return>', lambda event : self.clear())
    def clear(self):
        self.entry.delete("0", tkinter.END)

# Класс виджета окна результатов и сохранения в файл / class of result frame
class Result_and_save(tkinter.PanedWindow):
    def __init__(self, master):
        super().__init__ (master, orient='vertical', bg=master.cget('bg'), borderwidth=0, sashwidth=10)
        self.data = Result_data(self, parse=True, base=True, temporary=True)
        self.data.pack(side = tkinter.TOP)
        self.add(self.data)
        self.save = Save_to_file(self)
        self.save.pack(side = tkinter.TOP)
        self.add(self.save)

#============================================================================================================
# Классы виджетов и графических элементов / classes of parent window widgets
        
# Класс виджета настроек / settings widget class
class Options_list(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200, height=40, corner_radius=10)
        self.settings_img = customtkinter.CTkImage(Image.open('./Design/icon-settings-outline.png'), size=(15,15))
        self.hover_color = ('#B0AFB1','#515152')

        def settings():
            self.opt = Options(master.master)
            self.opt.grab_set()

        self.button_1 = customtkinter.CTkButton(self, 
                                                image=self.settings_img,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                text=None,                              
                                                command=settings,
                                                )
        self.button_1.pack(padx=5, pady=5, side="left")
        
        self.button_2 = customtkinter.CTkButton(self,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_2.pack(padx=0, pady=5, side="left")

        self.button_3 = customtkinter.CTkButton(self,
                                                height=30, width=120,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_3.pack(padx=5, pady=5, side="left", expand=True)

# Класс виджета настроек поиска / search settings widget class
class Search_options(customtkinter.CTkFrame):
    def __init__(self, master, text_colors):
        super().__init__(master, width=200, height=500, corner_radius=10)
        
        self.namebox = customtkinter.CTkLabel(self, text="Настройки поиска", font=("Arial", 12),
                                                width=190, height=30,
                                                text_color=text_colors)
        self.namebox.grid(column=0, row=0, padx=5, pady=0, sticky="n")

        self.parse_switch = customtkinter.CTkSwitch(self, text="Парсинг",
                                                    command=lambda: self.parse_switch_func())
        self.parse_switch.grid(column=0, row=1, padx=5, pady=5, sticky="w")

        self.database_switch = customtkinter.CTkSwitch(self, text="Поиск по базе",
                                                    command=lambda: self.database_switch_func())
        self.database_switch.grid(column=0, row=2, padx=5, pady=5, sticky="w")

        self.temporary_base_switch = customtkinter.CTkSwitch(self, text="Временная база",
                                                    command=lambda: self.temporary_base_func())
        self.temporary_base_switch.grid(column=0, row=3, padx=5, pady=5, sticky="w")

        self.namebox_2 = customtkinter.CTkLabel(self, text="Создание временной \nбазы данных из файла", font=("Arial", 12),
                                                width=190, height=30,
                                                text_color=text_colors)
        self.namebox_2.grid(column=0, row=4, padx=5, pady=5, sticky="n")
        
        self.check_last_database()
        self.file_choose_button = customtkinter.CTkButton(self, text=self.button_text,
                                                            width=190, height=20,
                                                            text_color=text_colors,
                                                            command=lambda: self.create_temporary_database())
        self.file_choose_button.grid(column=0, row=5, padx=5, pady=5, sticky="w")

    def check_last_database(self):
        self.file_name = self.master.master.config_data['SEARCH_SETTINGS']['temporary_base']
        if self.file_name == "":
            self.button_text = "Выбрать файл"
        else:
            self.button_text = "Выбрано: " + self.file_name

    def parse_switch_func(self):
        if self.parse_switch.get():
            print("parser toggle")
    
    def database_switch_func(self):
        if self.database_switch.get():
            print("basa toggle")
    
    def temporary_base_func(self):
        if self.temporary_base_switch.get():
            print("time toggle")

    def create_temporary_database(self):
        self.file_path = fd.askopenfilename()
        self.file_name = os.path.basename(self.file_path)
        if len(self.file_name)>12:
            self.file_name = self.file_name[:13]+"..."
        if self.file_name != "":
            self.file_choose_button.configure(text="Выбрано: " + self.file_name)
            self.master.master.config_data['SEARCH_SETTINGS']['temporary_base'] = self.file_name
            config.set_config(self.master.master)    

# Класс виджета настроек сохранения в файл / save to file widget class
class Save_options(customtkinter.CTkFrame):
    def __init__(self, master, text_colors):
        super().__init__(master, width=200, corner_radius=10)
        self.namebox = customtkinter.CTkLabel(self, text="Настройки сохранения",
                                                width=190, height=30,
                                                text_color=text_colors)
        self.namebox.grid(column=0, row=0, padx=5, pady=0, sticky="n")

        self.file_choose_button = customtkinter.CTkButton(self, text="Выбрать файл",
                                                            width=190, height=20,
                                                            text_color=text_colors)
        self.file_choose_button.grid(column=0, row=1, padx=5, pady=5, sticky="w")

# Класс виджета вывода данных / result data frame class
class Result_data(customtkinter.CTkFrame):
    def __init__(self, master, parse=False, base=False, temporary=False):
        super().__init__(master, height=400, corner_radius=10)
        
        if master.master.config_data['USER_SETTINGS']['theme']=='Dark':
            self.info_bg_color = "#2B2B2B"
        if master.master.config_data['USER_SETTINGS']['theme']=='Light':
            self.info_bg_color = "#DBDBDB"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Размещение скроллбара и фрейма с информацией

        self.infobox = tkinter.Canvas(self, bg=self.info_bg_color,  highlightthickness=0)
        self.infobox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="vertical",
                                                    width=15, corner_radius=5, border_spacing=2,
                                                    minimum_pixel_length=30,
                                                    hover=True,
                                                    command=self.infobox.yview)
        self.scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
        self.infobox.configure(yscrollcommand=self.scrollbar.set)
        
        self.labels_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        #размещение инфобоксов и заголовков
        if parse==True:
            self.parse_label = customtkinter.CTkLabel(self.infobox, height=20,
                                                        text="Результаты парсинга:",
                                                        font=self.labels_font,
                                                        anchor='w')
            self.parse_label.pack(padx=5, pady=0,fill='x')
            self.parse_boxes = []
            self.parse_data = master.master.database.get_parse_by_name("Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 1)
            for key in range(len(self.parse_data)):
                self.parse_boxes.append(Info_module(self.infobox, master.master.config_data["SEARCH_SETTINGS"]["scale"], self.parse_data[key], data_type="parse").pack(padx=5, pady=5, fill='x'))

        if base==True:
            self.base_label = customtkinter.CTkLabel(self.infobox, height=20,
                                                        text="Результаты поиска по базе:",
                                                        font=self.labels_font,
                                                        anchor='w')
            self.base_label.pack(padx=5, pady=0, fill='x')
            self.base_boxes = []
            self.base_data = master.master.database.get_ref_by_name("Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д")
            for key in range(len(self.base_data)):
                self.base_boxes.append(Info_module(self.infobox, master.master.config_data["SEARCH_SETTINGS"]["scale"], self.parse_data[key], data_type="ref").pack(padx=5, pady=5, fill='x'))

        if temporary==True:
            self.parse_label = customtkinter.CTkLabel(self.infobox, height=20,
                                                        text="Результаты поиска по временной базе:",
                                                        font=self.labels_font,
                                                        anchor='w')
            self.parse_label.pack(padx=5, pady=0,fill='x')
            self.temporary_boxes = []
            self.temporary_data = master.master.database.get_temp_by_name("Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕsТАН   LE-ССП-53-033-3773-65Д")
            for key in range(len(self.temporary_data)):
                self.base_boxes.append(Info_module(self.infobox, master.master.config_data["SEARCH_SETTINGS"]["scale"], self.parse_data[key], data_type="temp").pack(padx=5, pady=5, fill='x'))

# Класс виджета сохранения данных в файл / save to file format frame class
class Save_to_file(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)

#============================================================================================================
# Классы для создания дополнительных окон     
# Класс уведомлений [cl = 'warning', 'info', 'error'] / messange class [cl = 'warning', 'info', 'error']
class Messange(customtkinter.CTkToplevel):
    def __init__(self, parent, master, cl, title, msg, skip_button=None, confirm_button=None, decline_button=None):
        super().__init__(parent)
        self.geometry(f"{master.MSG_WIDTH}x{master.MSG_HEIGHT}+{int(master.X_MSG)}+{int(master.Y_MSG)}")
        self.title(title)
        self.resizable(width=False, height=False)
        self.attributes('-topmost', 'true')

        self.flag = None
        self.font = customtkinter.CTkFont("Avenir Next", 12, 'normal')

        self.frame = customtkinter.CTkFrame(self, 
                                        width=master.MSG_WIDTH-20, 
                                        height=master.MSG_HEIGHT-20, 
                                        corner_radius=10)
        self.frame.pack(padx=10, pady=10)
        self.frame.pack_propagate(0)
        
        self.img = customtkinter.CTkImage(Image.open('./Design/icon-' + cl + '-outline.png'), size=(70,66))
        self.icon_warning = customtkinter.CTkLabel(self.frame,
                                                    width=70,
                                                    height=70,
                                                    text="",
                                                    image=self.img)
        self.icon_warning.grid(row=0, column=0, padx=20, pady=50, sticky="N")

        self.text = customtkinter.CTkLabel(self.frame,
                                            width=master.MSG_WIDTH-130,height=master.MSG_HEIGHT-20, 
                                            text=msg, font=self.font,
                                            justify=tkinter.LEFT)
        self.text.grid(row=0, column=1, padx=0, pady=0, sticky="N")
        
        if cl == 'warning':
            self.color = '#FFDE3B'
        if cl == 'error':
            self.color = '#FB0406'
        if cl == 'info':
            self.color = '#03ACC7'

        if skip_button == True: 
            self.s_button = customtkinter.CTkButton(self.frame,
                                                    width=50, height=20, 
                                                    border_width=2, corner_radius=8, 
                                                    text="Пропустить",
                                                    font=self.font,
                                                    border_color=self.color, text_color=self.color, fg_color="transparent", bg_color="transparent", hover_color=('#B0AFB1','#515152'),
                                                    command = lambda: self.destroy)
            self.s_button.pack(side='bottom', anchor='se', padx=10, pady=10)
            self.bind('<Return>', lambda e: self.destroy())
        
        if confirm_button == True: 
            self.c_button = customtkinter.CTkButton(self.frame,
                                                    width=50, height=20, 
                                                    border_width=2, corner_radius=8, 
                                                    text="Принять",
                                                    font=self.font,
                                                    border_color=self.color, text_color=self.color, fg_color="transparent", bg_color="transparent", hover_color=('#B0AFB1','#515152'),
                                                    command = lambda: self.confirm_func())
            self.c_button.pack(side='right', anchor='se', padx=10, pady=10)
            self.bind('<Return>', lambda e: self.confirm_func())
        
        if decline_button == True: 
            self.d_button = customtkinter.CTkButton(self.frame,
                                                    width=50, height=20, 
                                                    border_width=2, corner_radius=8, 
                                                    text="Отклонить",
                                                    font=self.font,
                                                    border_color=self.color, text_color=self.color, fg_color="transparent", bg_color="transparent", hover_color=('#B0AFB1','#515152'),
                                                    command = lambda: self.decline_func())
            self.d_button.pack(side='right', anchor='se', padx=0, pady=10)
        
        self.mainloop()

    def confirm_func(self):
        self.flag=True
        self.withdraw()
        
    def decline_func(self):
        self.flag=False
        self.withdraw()

# Класс окна настроек / optons window class
class Options(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('| Настройки | Options |')
        self.geometry(f"{master.OPT_WIDTH}x{master.OPT_HEIGHT}+{int(master.X_OPT)}+{int(master.Y_OPT)}")
        self.resizable(width=False, height=False)
        self.attributes('-topmost', 'true')
        
        self.buttons_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.labels_font = customtkinter.CTkFont("Avenir Next", 14, 'normal')

        self.frame_left = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=master.OPT_HEIGHT-20,
                                                corner_radius=10)
        self.frame_left.pack(padx=[10,5], pady=10, side='left', fill='both')
        
        self.frame_right = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=master.OPT_HEIGHT-100,
                                                corner_radius=10)
        self.frame_right.pack(padx=[5,10], pady=[10,0], side='top', fill='both', expand=True)

        self.frame_save = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=30,
                                                corner_radius=10)
        self.frame_save.pack(padx=[5,10], pady=[0,10], side='bottom', fill='both')

        self.frame_default = customtkinter.CTkFrame(self,
                                                    width=(master.OPT_WIDTH-30)/2,
                                                    height=30,
                                                    corner_radius=10)
        self.frame_default.pack(padx=[5,10], pady=[5,10], side='bottom', fill='both')


        self.save_button = customtkinter.CTkButton(self.frame_save, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Сохранить изменения",
                                                    font=self.buttons_font,
                                                    command=self.save_button_func)
        self.save_button.pack(padx=5, pady=5)

        self.default_button = customtkinter.CTkButton(self.frame_default, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Сбросить настройки",
                                                    font=self.buttons_font,
                                                    command=self.default_button_func)
        self.default_button.pack(padx=5, pady=5)
        
        self.label_1r = customtkinter.CTkLabel(self.frame_right,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Цветовое оформление:",
                                                font=self.labels_font)
        self.label_1r.grid(row=0, column=0, padx=5, pady=5)

        self.optionmenu_1r = customtkinter.CTkOptionMenu(self.frame_right,
                                                        width=(master.OPT_WIDTH-30)/2-20,
                                                        height=25,
                                                        values=config.mix_values(["Dark", "Light"],
                                                                                master.config_data['USER_SETTINGS']['theme']),
                                                        font=self.buttons_font,
                                                        command=self.theme_button)
        self.optionmenu_1r.grid(row=1, column=0, padx=5, pady=0)
        
        self.label_1l = customtkinter.CTkLabel(self.frame_left,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Настройки сохранённых данных",
                                                font=self.labels_font)
        self.label_1l.grid(row=0, column=0, padx=5, pady=5)
        
        self.button_1l = customtkinter.CTkButton(self.frame_left, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Очистить историю поиска",
                                                    font=self.buttons_font,
                                                    command=lambda: self.delete_history_button_func(master))
        self.button_1l.grid(row=1, column=0, padx=10, pady=[0,5])

        self.button_2l = customtkinter.CTkButton(self.frame_left, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Очистить временную  базу",
                                                    font=self.buttons_font,
                                                    command=lambda: self.delete_temporary_button_func(master))
        self.button_2l.grid(row=2, column=0, padx=10, pady=[0,5])

        self.button_3l = customtkinter.CTkButton(self.frame_left, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Очистить историю парсинга",
                                                    font=self.buttons_font,
                                                    command=lambda: self.delete_parser_history_button_func(master))
        self.button_3l.grid(row=3, column=0, padx=10, pady=[0,5])

        self.label_2l = customtkinter.CTkLabel(self.frame_left,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Лимит истории поиска",
                                                font=self.labels_font)
        self.label_2l.grid(row=4, column=0, padx=5, pady=[0,5])
        
        self.counter_1l = FloatSpinbox(self.frame_left, start=master.config_data['SEARCH_SETTINGS']['history_limit'],
                                        width=(master.OPT_WIDTH-30)/2-20,
                                        step_size=1, count_system='int',
                                        minimum=1, maximum=30)
        self.counter_1l.grid(row=5, column=0, padx=5, pady=[0,5])
        
        self.label_3l = customtkinter.CTkLabel(self.frame_left,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Маштаб просмотра",
                                                font=self.labels_font)
        self.label_3l.grid(row=6, column=0, padx=5, pady=[0,5])

        self.counter_2l = FloatSpinbox(self.frame_left, start=master.config_data['SEARCH_SETTINGS']['scale'],
                                        width=(master.OPT_WIDTH-30)/2-20,
                                        step_size=1, count_system='int',
                                        minimum=2, maximum=6)
        self.counter_2l.grid(row=7, column=0, padx=5, pady=[0,5])
        
        self.keyboard_bind()

    def theme_button(self, value):
        self.master.config_data['USER_SETTINGS']['theme'] = value
    
    def save_button_func(self):
        self.master.config_data['SEARCH_SETTINGS']['history_limit'] = str(self.counter_1l.get())
        self.master.config_data['SEARCH_SETTINGS']['scale'] = str(self.counter_2l.get())
        config.set_config(self.master)
        self.master.refresh_by_config()
        self.destroy()
    
    def delete_history_button_func(self, master):
        self.messange = Messange(parent=self, master=master, cl='info',
                                    title='| Очистка истории |',
                                    msg = "История поиска будет\nбезвозвратно удалена",
                                    skip_button=False,
                                    confirm_button=True, decline_button=True,)

    def delete_temporary_button_func(self, master):
        self.messange = Messange(parent=self, master=master, cl='info',
                                    title='| Очистка истории |',
                                    msg = "Временная база данных будет\nбезвозвратно удалена",
                                    skip_button=False,
                                    confirm_button=True, decline_button=True,)
    
    def delete_parser_history_button_func(self, master):
        self.messange = Messange(parent=self, master=master, cl='info',
                                    title='| Очистка истории |',
                                    msg = "История парсера будет\nбезвозвратно удалена",
                                    skip_button=False,
                                    confirm_button=True, decline_button=True,)
    
    def default_button_func(self):
        config.return_to_default(self.master)
        config.set_config(self.master)
        self.master.refresh_by_config()
        self.destroy()

    def keyboard_bind(self):
        self.bind('<Control-s>', lambda event : self.save_button_func())
        self.bind('<Control-d>', lambda event : self.default_button_func())
        self.bind('<Control-q>', lambda event : self.destroy())

# Класс модуля в окне результатов
class Info_module(customtkinter.CTkFrame):
    def __init__(self, master, scale, data, data_type=None):
        super().__init__(master, height=60, corner_radius=10)

        self.labels_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.url_font = customtkinter.CTkFont("Avenir Next", 12, 'normal', 'italic', underline=True)
        if data[5]==None:
            self.screenshot_image = customtkinter.CTkImage(light_image = Image.open("./Design/Light_image_default.png"),
                                                           dark_image = Image.open("./Design/Dark_image_default.png"), size=(192,108))

            self.screenshot_label = customtkinter.CTkLabel(self, width=202, height=118, fg_color=('#C2C2C2','#5A5A5A'), corner_radius=5,
                                                        text='', image=self.screenshot_image,
                                                        cursor='sizing')
            self.screenshot_label.grid(padx=5, pady=5, row=0, column=0, rowspan=4)
        else:
            self.screenshot_image = customtkinter.CTkImage(Image.open(io.BytesIO(data[5])), size=(192,108))

            self.screenshot_label = customtkinter.CTkLabel(self, width=202, height=118, fg_color=('#C2C2C2','#5A5A5A'), corner_radius=5,
                                                        text='', image=self.screenshot_image,
                                                        cursor='sizing')
            self.screenshot_label.grid(padx=5, pady=5, row=0, column=0, rowspan=4)
            self.screenshot_label.bind("<Button-1>", lambda e: self.open_view(int(scale), data, image=data[5]))

        self.name_label = customtkinter.CTkLabel(self, height=20, text=data[0],
                                                 anchor='w',
                                                 font=self.labels_font)
        self.name_label.grid(padx=5, pady=10, row=0, column=1, columnspan=2, sticky="NW")

        self.price_label = customtkinter.CTkLabel(self, height=20, text="Стоимость: "+ str(data[1]) +" "+data[2],
                                                 anchor='w',
                                                 font=self.labels_font)
        self.price_label.grid(padx=5, pady=5, row=1, column=1, sticky="NW")

        self.unit_label = customtkinter.CTkLabel(self, height=20, text="Единица измерения: "+data[3],
                                                 anchor='w',
                                                 font=self.labels_font)
        self.unit_label.grid(padx=5, pady=5, row=1, column=2, sticky="NW")

        self.url_label = customtkinter.CTkLabel(self, height=20, text="Ссылка на ресурс: "+data[4],
                                                 anchor='w',
                                                 font=self.url_font)
        self.url_label.grid(padx=5, pady=5, row=2, column=1, columnspan=2, sticky="NW")
        self.url_label.bind("<Button-1>", lambda e: self.clicked_url(data[4]))

        if data_type=='parse':
            self.date_label = customtkinter.CTkLabel(self, height=20, text="Информация актуальна на: "+data[6],
                                                 anchor='w',
                                                 font=self.labels_font)
            self.date_label.grid(padx=5, row=3, column=1, columnspan=2, sticky="NW")
        
    def clicked_url(self, url):
        webbrowser.open_new(url)
        
    def open_view(self, scale, data, image=None):
        if image!= None:
            self.image_view = customtkinter.CTkToplevel(self)
            self.image_view.title('| Просмотр |')
            self.image_view.geometry(f"{int(192*scale+10)}x{int(108*scale+10)}")
            self.image_view.resizable(width=False, height=False)
            self.image_view.attributes('-topmost', 'true')

            self.image_view.image = customtkinter.CTkImage(Image.open(io.BytesIO(data[5])), size=(192*scale,108*scale))
            self.image_view.image_label = customtkinter.CTkLabel(self.image_view, width=192*scale+2, height=108*scale+2,
                                                                    text='', image=self.image_view.image,
                                                                    cursor = 'sizing')
            self.image_view.image_label.pack(padx=5, pady=5)
            self.image_view.image_label.bind("<Button-1>", lambda e: self.image_view.destroy())

# Класс счетчика
class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 minimum: int = 0,
                 maximum: int = 100,
                 count_system: str = 'int',
                 start: Union[int, float] = 0,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.count_system = count_system
        self.step_size = step_size
        self.command = command
        self.minimum = minimum
        self.maximum = maximum

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.check = (self.register(self.is_valid), "%P")
        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, validate="key", validatecommand=self.check)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        if self.count_system=="int":
            self.entry.insert(0, str(int(start)))
        if self.count_system=="float":
            self.entry.insert(0, str(float(start)))

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        if self.count_system=='int':
            try:
                if int(self.entry.get()) + self.step_size <= self.maximum:
                    value = int(self.entry.get()) + self.step_size
                    self.entry.delete(0, "end")
                    self.entry.insert(0, value)
            except ValueError:
                return

        if self.count_system=='float':
            try:
                if float(self.entry.get()) + self.step_size <= self.maximum:
                    value = float(self.entry.get()) + self.step_size
                    self.entry.delete(0, "end")
                    self.entry.insert(0, value)
            except ValueError:
                return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        
        if self.count_system=='int':
            try:
                if int(self.entry.get()) - self.step_size >= self.minimum:
                    value = int(self.entry.get()) - self.step_size
                    self.entry.delete(0, "end")
                    self.entry.insert(0, value)
            except ValueError:
                return
                
        if self.count_system=='float':
            try:
                if float(self.entry.get()) - self.step_size >= self.minimum:
                    value = float(self.entry.get()) - self.step_size
                    self.entry.delete(0, "end")
                    self.entry.insert(0, value)
            except ValueError:
                return

    def get(self) -> Union[float, None]:
        try:
            if float(self.entry.get())>=self.maximum:
                value=self.maximum
            else:
                value = self.entry.get()
            if float(self.entry.get())<=self.minimum:
                value=self.minimum
            else:
                value = self.entry.get()
            if self.count_system=='int':
                return int(value)
            if self.count_system=='float':
                return float(value)
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        if self.count_system=='int':
            self.entry.insert(0, str(int(value)))
        if self.count_system=='float':
            self.entry.insert(0, str(float(value)))

    def is_valid(self, newval):
        if (float(newval)<=self.maximum) and (float(newval)>=self.minimum):
            if self.count_system=='int':
                self.entry.insert(0, str(int(newval)))
            if self.count_system=='float':
                self.entry.insert(0, str(float(newval)))
            return True
        else:
            if float(newval)>=self.maximum:
                value=self.maximum
            if float(newval)<=self.minimum:
                value=self.minimum
            if self.count_system=='int':
                self.entry.insert(0, str(int(value)))
            if self.count_system=='float':
                self.entry.insert(0, str(float(value)))

if __name__ == "__main__":
    app = App()
    app.mainloop()