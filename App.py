import os
import io
from typing import Union, Callable

from PIL import Image

import tkinter
from tkinter import filedialog as fd
from tkinter import ttk
import customtkinter

import webbrowser

from Libs import Config_func as config
from Libs import Data_func as db

import pandas as  pd

class App(customtkinter.CTk):
    # Основные параметры приложения / main parametres of app
    def __init__(self):
        super().__init__()
        self.params()
        self.find_center()

        self.title('| LinkFinder v 0.1.0.3 |')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")
        self.minsize(240,480)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Размещаем элементы главного окна
        self.put_main_frames()
        
        # Привязываем быстрые сочетания для главного окна
        self.keyboard_bind()
    #============================================================================================================
    # Технические функции 
    # Функция присвоения главных параметров / main parametres function
    def params(self):
        #(подгружаем данные из файла конфигурации)
        self.database = db.Database()
        self.config_data = config.get_config()
        #(применяем сохраненную конфигурацию)
        customtkinter.set_appearance_mode(self.config_data['USER_SETTINGS']['theme'])

        self.text_colors = ("#FFFAFA")

        self.APP_WIDTH = 780
        self.APP_HEIGHT = 480

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
        config.set_config(self)
        customtkinter.set_appearance_mode(self.config_data['USER_SETTINGS']['theme'])
        
        self.left_main_frame.destroy()
        self.left_main_frame = Left_main(self)
        self.left_main_frame.pack(side=tkinter.LEFT, fill='y')
        
        self.search_frame.destroy()
        self.search_frame = Search(self)
        self.search_frame.pack(side=tkinter.TOP, fill='x', padx=5, pady=5)
        
        self.result_and_save_frame.destroy()
        self.result_and_save_frame = Result_and_save(self)
        self.result_and_save_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        
#============================================================================================================
# Класс основной левой группы виджетов / class of left frame
class Left_main(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=240, corner_radius=0, bg_color="transparent")
        self.main_opt = Options_list(self).pack(padx=5, pady=5, fill='x')
        self.search_opt = Search_options(self, master.text_colors).pack(padx=5, pady=5)
        self.save_opt = Save_options(self, master.text_colors).pack(padx=5, pady=5, expand=True, fill='y')

# Класс виджета поисковой строки / class of search frame
class Search(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=40, corner_radius=10, bg_color="transparent")       
        self.symbols_font = customtkinter.CTkFont("Avenir Next", 16, 'normal')
        self.hover_color = ('#B0AFB1','#515152')

        self.entry = customtkinter.CTkEntry(self, placeholder_text=None,
                                            height=30,
                                            corner_radius=8, border_width=1)
        self.entry.pack(side=tkinter.LEFT, expand=True, fill='x', padx=5, pady=5)

        self.clear_button = customtkinter.CTkButton(self, 
                                                    height=30, width=30,
                                                    corner_radius=8, border_width=1,
                                                    border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                    text="\u2715", text_color='#0267A7',
                                                    command=self.clear)
        self.clear_button.pack(side=tkinter.LEFT, padx=(0, 5), pady=5)
        
        master.bind('<Control-n>', lambda event : self.clear())
        
        self.search_button = customtkinter.CTkButton(self, 
                                                    height=30, width=40,
                                                    corner_radius=8, border_width=1,
                                                    border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                    compound="right",
                                                    text="Найти",
                                                    text_color='#0267A7',
                                                    command=None)
        self.search_button.pack(side=tkinter.RIGHT, padx=(0, 5), pady=5)
        
        master.bind('<Return>', lambda event : self.clear())
    
    def clear(self):
        self.entry.delete("0", tkinter.END)

    def serch_process(self):
        pass

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
        super().__init__(master, height=40, corner_radius=10)
        #self.settings_img = customtkinter.CTkImage(Image.open('./Design/icon-settings-outline.png'), size=(15,15))
        self.width = 230
        self.hover_color = ('#B0AFB1','#515152')
        self.symbols_font = customtkinter.CTkFont("Avenir Next", 16, 'normal')

        def settings():
            self.opt = Options(master.master)
            self.opt.grab_set()

        self.button_1 = customtkinter.CTkButton(self, 
                                                #image=self.settings_img,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                text="\u2699", font=self.symbols_font, text_color="#0267A7",                            
                                                command=settings,
                                                )
        self.button_1.pack(padx=[5,0], pady=5, side="left")
        
        self.button_2 = customtkinter.CTkButton(self,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_2.pack(padx=[5,0], pady=5, side="left")

        self.button_3 = customtkinter.CTkButton(self,
                                                height=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color="transparent", bg_color="transparent", hover_color=self.hover_color,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_3.pack(padx=[5,0], pady=5, side="left", expand=True)

# Класс виджета настроек поиска / search settings widget class
class Search_options(customtkinter.CTkFrame):
    def __init__(self, master, text_colors):
        super().__init__(master, height=500, corner_radius=10)
        
        self.width = 230
        self.buttons_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.labels_font = customtkinter.CTkFont("Avenir Next", 14, 'normal')

        self.namebox_1 = customtkinter.CTkLabel(self, text="Настройки поиска", font=self.labels_font,
                                                width=self.width-10, height=25)
        self.namebox_1.grid(column=0, row=0, padx=5, pady=[5,0], sticky="n")

        self.parse_switch = customtkinter.CTkSwitch(self, text="Парсинг", font=self.buttons_font,
                                                    onvalue="True", offvalue="False", variable=customtkinter.StringVar(value=master.master.config_data['SEARCH_SETTINGS']['using_parser']),
                                                    command=lambda: self.parse_switch_func(master))
        self.parse_switch.grid(column=0, row=1, padx=5, pady=[5,0], sticky="w")

        self.database_switch = customtkinter.CTkSwitch(self, text="Поиск по базе", font=self.buttons_font, 
                                                    onvalue="True", offvalue="False", variable=customtkinter.StringVar(value=master.master.config_data['SEARCH_SETTINGS']['using_database']),
                                                    command=lambda: self.database_switch_func(master))
        self.database_switch.grid(column=0, row=2, padx=5, pady=[5,0], sticky="w")

        self.temporary_base_switch = customtkinter.CTkSwitch(self, text="Временная база", font=self.buttons_font,
                                                    onvalue="True", offvalue="False", variable=customtkinter.StringVar(value=master.master.config_data['SEARCH_SETTINGS']['using_temporary']),
                                                    command=lambda: self.temporary_base_func(master))
        self.temporary_base_switch.grid(column=0, row=3, padx=5, pady=[5,0], sticky="w")

        self.namebox_2 = customtkinter.CTkLabel(self, text="Импорт данных из файла", font=self.labels_font,
                                                width=self.width-10, height=25)
        self.namebox_2.grid(column=0, row=4, padx=5, pady=[5,0], sticky="n")
        
        self.check_last_database()
        self.file_choose_button = customtkinter.CTkButton(self, text=self.button_text, font=self.buttons_font,
                                                            width=self.width-10, height=20,
                                                            text_color=text_colors,
                                                            command=lambda: self.create_temporary_database())
        self.file_choose_button.grid(column=0, row=5, padx=5, pady=[5,0], sticky="w")

        self.namebox_3 = customtkinter.CTkLabel(self, text="Настройки предобработки", font=self.labels_font,
                                                width=self.width-10, height=25)
        self.namebox_3.grid(column=0, row=6, padx=5, pady=[5,0], sticky="n")

        self.caps_switch = customtkinter.CTkSwitch(self, text="В нижний регистр", font=self.buttons_font,
                                                    onvalue="True", offvalue="False", variable=customtkinter.StringVar(value=master.master.config_data['SEARCH_SETTINGS']['caps']),
                                                    command=lambda: self.caps_switch_func(master))
        self.caps_switch.grid(column=0, row=7, padx=5, pady=[5,0], sticky="w")

        self.symbols_switch = customtkinter.CTkSwitch(self, text="Убрать знаки", font=self.buttons_font,
                                                    onvalue="True", offvalue="False", variable=customtkinter.StringVar(value=master.master.config_data['SEARCH_SETTINGS']['symbols']),
                                                    command=lambda: self.symbols_switch_func(master))
        self.symbols_switch.grid(column=0, row=8, padx=5, pady=[5,0], sticky="w")

        self.nums_switch = customtkinter.CTkSwitch(self, text="Только параметры", font=self.buttons_font,
                                                    onvalue="True", offvalue="False", variable=customtkinter.StringVar(value=master.master.config_data['SEARCH_SETTINGS']['only_nums']),
                                                    command=lambda: self.nums_switch_func(master))
        self.nums_switch.grid(column=0, row=9, padx=5, pady=[5,0], sticky="w")
    
    def check_last_database(self):
        self.file_path = self.master.master.config_data['SEARCH_SETTINGS']['temporary_base']
        self.file_name = os.path.basename(self.file_path)
        if len(self.file_name)>10: self.file_name = self.file_name[:10]+"..."
        if self.file_name == "":
            self.button_text = "Выбрать файл"
        else:
            self.button_text = "Выбрано: " + self.file_name

    def parse_switch_func(self, master):
        master.master.config_data['SEARCH_SETTINGS']['using_parser']=self.parse_switch.get()
        config.set_config(master.master)

    def database_switch_func(self, master):
        master.master.config_data['SEARCH_SETTINGS']['using_database']=self.database_switch.get()
        config.set_config(master.master)
    
    def temporary_base_func(self, master):
        master.master.config_data['SEARCH_SETTINGS']['using_temporary']=self.temporary_base_switch.get()
        config.set_config(master.master)

    def caps_switch_func(self, master):
        master.master.config_data['SEARCH_SETTINGS']['caps']=self.caps_switch.get()
        config.set_config(master.master)
    
    def symbols_switch_func(self, master):
        master.master.config_data['SEARCH_SETTINGS']['symbols']=self.symbols_switch.get()
        config.set_config(master.master)
    
    def nums_switch_func(self, master):
        master.master.config_data['SEARCH_SETTINGS']['only_nums']=self.nums_switch.get()
        config.set_config(master.master)

    def create_temporary_database(self):
        self.file_path = fd.askopenfilename(filetypes=[ 
            ("data tables", "*.csv")])
        
        if self.file_path != "": self.open_csv_options = View_CSV(self, self.file_path)

# Класс виджета настроек сохранения в файл / save to file widget class
class Save_options(customtkinter.CTkFrame):
    def __init__(self, master, text_colors):
        super().__init__(master, corner_radius=10)
        
        self.width = 230
        self.buttons_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.labels_font = customtkinter.CTkFont("Avenir Next", 14, 'normal')
        self.instructions_font = customtkinter.CTkFont("Avenir Next", 9, 'normal')
        
        self.namebox = customtkinter.CTkLabel(self, text="Настройки сохранения", font=self.labels_font,
                                                width=self.width-10, height=30)
        self.namebox.grid(column=0, row=0, padx=5, pady=[5,0], sticky="n")

        self.choose_label = customtkinter.CTkLabel(self, text="Выбор файла, в который\nнужно сохранить информацию", font=self.instructions_font,
                                                    width=90, height=30, justify='left')
        self.choose_label.grid(column=0, row=1, padx=[5,0], pady=[5,0], sticky="w")

        self.file_choose_button = customtkinter.CTkButton(self, text="Выбрать", font=self.buttons_font,
                                                            width=90, height=20,
                                                            text_color=text_colors, command = lambda:self.choose())
        self.file_choose_button.grid(column=0, row=1, padx=5, pady=[5,0], sticky="e")

        self.file_create_button = customtkinter.CTkButton(self, text="Создать", font=self.buttons_font,
                                                            width=90, height=20,
                                                            text_color=text_colors, command=lambda:self.create())
        self.file_create_button.grid(column=0, row=2, padx=5, pady=[5,0], sticky="e")

        self.choose_label = customtkinter.CTkLabel(self, text="Создание файла, в который\nнужно сохранить информацию", font=self.instructions_font,
                                                    width=90, height=30, justify='left')
        self.choose_label.grid(column=0, row=2, padx=[5,0], pady=[5,0], sticky="w")
    
    def choose(self):
        self.choose_file = Choose_Save_File(self)

    def create(self):
        self.choose_dir = Choose_Dir(self)

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
        '''
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
        '''

# Класс виджета сохранения данных в файл / save to file format frame class
class Save_to_file(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)

#============================================================================================================
# Классы для создания дополнительных окон     
# Класс уведомлений [cl = 'warning', 'info', 'error'] / messange class [cl = 'warning', 'info', 'error']
class Messange(customtkinter.CTkToplevel):
    def __init__(self, parent, master, cl, title, msg, skip_button=None, confirm_button=None, decline_button=None, confirm_button_function=None):
        super().__init__(parent)
        self.geometry(f"{master.MSG_WIDTH}x{master.MSG_HEIGHT}+{int(master.X_MSG)}+{int(master.Y_MSG)}")
        self.title(title)
        self.resizable(width=False, height=False)
        self.attributes('-topmost', 'true')

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
                                                    command = lambda: self.confirm_func(confirm_button_function))
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

    def confirm_func(self, func):
        if func != None: func()
        self.withdraw()
        
        
    def decline_func(self):
        self.withdraw()

# Класс окна настроек / optons window class
class Options(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('| Настройки | Options |')
        self.geometry(f"{master.OPT_WIDTH}x{master.OPT_HEIGHT}+{int(master.X_OPT)}+{int(master.Y_OPT)}")
        self.resizable(width=False, height=False)
        
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
                                    confirm_button=True, decline_button=True, confirm_button_function= lambda: db.Database().delete_history())

    def delete_temporary_button_func(self, master):
        def deleting(master):
            db.Database().delete_temporary()
            master.config_data['SEARCH_SETTINGS']['temporary_base'] = ''
            master.refresh_by_config()
        self.messange = Messange(parent=self, master=master, cl='info',
                                    title='| Очистка временной базы |',
                                    msg = "Временная база данных будет\nбезвозвратно удалена",
                                    skip_button=False,
                                    confirm_button=True, decline_button=True, confirm_button_function=lambda: deleting(master))
    
    def delete_parser_history_button_func(self, master):
        self.messange = Messange(parent=self, master=master, cl='info',
                                    title='| Очистка истории парсера |',
                                    msg = "История парсера будет\nбезвозвратно удалена",
                                    skip_button=False,
                                    confirm_button=True, decline_button=True, confirm_button_function=lambda: db.Database().delete_parse())
    
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

# Окно просмотра csv файла
class View_CSV(customtkinter.CTkToplevel):
    def __init__(self, master, path):
        super().__init__(master)
        self.title("| Просмотр CSV |")
        self.resizable(width=False, height=False)
        self.attributes('-topmost', 'true')

        self.data_column_max_width = 200
        self.data_column_min_width = 60
        self.CSV_VIEW_WIDTH = 0
        
        self.data = db.get_csv(path)

        self.buttons_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.labels_font = customtkinter.CTkFont("Avenir Next", 14, 'normal')
        self.table_style = ttk.Style().configure("C.TButton", font=('Aveni Next', 11))
        # инструкция
        self.instrucrions_frame = customtkinter.CTkFrame(self, height=60, width=310, corner_radius=0)
        self.instrucrions_frame.pack(padx=5, pady=0, anchor='w', fill='x')

        self.instruction = customtkinter.CTkTextbox(self.instrucrions_frame, height=45, width=300,
                                                    corner_radius=5, font=self.buttons_font, activate_scrollbars=False,
                                                    state='normal')
        self.instruction.insert('0.0','В соответсвие с данными, представленными в файле, выберите их тип ( типы не должны повторяться )\nВ данной таблице представлена только часть данных')
        self.instruction.configure(state='disabled')
        self.instruction.pack(padx=5, pady=5, fill='x', expand=False)

        self.index_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.index_frame.pack(padx=5, pady=0, fill='x', expand=False, anchor='w')

        self.choose_index_boxes = []

        # таблица
        self.table = ttk.Treeview(self, columns=self.data.columns, show='headings', style="C.TButton")

        # создание столбцов и соответсвующих им кнопок
        index = 0
        anchor= 'center'
        for col in self.data.columns:
            
            current_length = (self.data.astype(str).head(10)[col].map(len).max()+1)*10
            if current_length>=self.data_column_max_width: 
                current_length = self.data_column_max_width
                anchor='w'
            if current_length<=self.data_column_min_width: 
                current_length = self.data_column_min_width
                anchor='center'
            self.CSV_VIEW_WIDTH += current_length
            self.table.heading(index, text=col, anchor='center')
            self.table.column(index, width=current_length, anchor=anchor)
            
            new_index_box = customtkinter.CTkOptionMenu(self.index_frame,
                                                        width=current_length, height=25, corner_radius=5,
                                                        values=[' -- ', 'Прайс-лист', 'Название', 'Цена', 'Ед. изм.', 'Гиперссылка'],
                                                        font=self.buttons_font,
                                                        command=None)
            new_index_box.pack(padx=0, pady=5, side='left')
            self.choose_index_boxes.append(new_index_box)
            
            index+=1
        # создание строк
        for i, row in self.data.astype(str).head(10).iterrows():
            for k in range(len(row)):
                if len(row[k])>20: row[k] = row[k][:20]+"..."
                if row[k]=='nan': row[k] = ''
            self.table.insert('', 'end', values=list(row))
        
        self.table.configure(takefocus=False)
        self.table.pack(padx=5, pady=5, fill='x', anchor='w')

        self.geometry(f"{self.CSV_VIEW_WIDTH+10}x385")
        
        # Кнопка подтверждения сохраниения данных
        self.commit_button = customtkinter.CTkButton(self,
                                                    width=60, height=20, 
                                                    corner_radius=8, 
                                                    text="Сохранить",
                                                    font=self.buttons_font,
                                                    command = lambda: self.commit(master, path))
        self.commit_button.pack(side='right', anchor='ne', padx=10, pady=5)

        self.decline_button = customtkinter.CTkButton(self,
                                                    width=60, height=20, 
                                                    corner_radius=8, 
                                                    text="Отменить",
                                                    font=self.buttons_font,
                                                    command = lambda: self.decline())
        self.decline_button.pack(side='right', anchor='ne', padx=10, pady=5)

        self.start_row_label = customtkinter.CTkLabel(self,
                                                width=150,
                                                height=32,
                                                text="Начало считывания со строки № :",
                                                font=self.labels_font)
        self.start_row_label.pack(side='left', anchor='nw', padx=10, pady=5)

        self.start_row_counter =  FloatSpinbox(self, start=1, width=130,
                                                step_size=1, count_system='int',
                                                minimum=1, maximum=10000)
        self.start_row_counter.pack(side='left', anchor='nw', padx=0, pady=5)
    
        self.table.bind('<Button-1>', self.handle_click)
    
    def commit(self, master, path):
        self.indexes = {
                        "code_index": None,
                        "name_index": None,
                        "price_index": None,
                        "unit_index": None,
                        "price_unit": "RUB",
                        "url_index": None,
                        "screenshot_index": None,
                        "start_row": 0
        }
        for num, button in enumerate(self.choose_index_boxes):
            if button.get()=='Прайс-лист': self.indexes["code_index"]=self.data.columns[num]
            if button.get()=='Название': self.indexes["name_index"]=self.data.columns[num]
            if button.get()=='Цена': self.indexes["price_index"]=self.data.columns[num]
            if button.get()=='Ед. изм.': self.indexes["unit_index"]=self.data.columns[num]
            if button.get()=='Гиперссылка': self.indexes["url_index"]=self.data.columns[num]
        self.indexes["start_row"]=self.start_row_counter.get()-1
        try: db.create_temporary_database_from_csv(self.data, self.indexes)
        except KeyError: pass
        else: 
            master.file_name = os.path.basename(path)
            if len(master.file_name)>10: master.file_name = master.file_name[:10]+"..."
            master.file_choose_button.configure(text="Выбрано: " + master.file_name)
            master.master.master.config_data['SEARCH_SETTINGS']['temporary_base'] = master.file_path
            config.set_config(master.master.master)
            self.destroy()

    def decline(self):
        self.destroy()
    
    def handle_click(self, event):
        if self.table.identify_region(event.x, event.y) == "separator":
            return "break"

# Окно для выбора места создания файла
class Choose_Dir(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("| Выбор папки |")
        self.geometry(f"480x155+{int((self.winfo_screenwidth()-480)/2)}+{int((self.winfo_screenheight()-155)/2)}")
        self.resizable(width=False, height=False)

        self.buttons_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.labels_font = customtkinter.CTkFont("Avenir Next", 14, 'normal')
        self.instructions_font = customtkinter.CTkFont("Avenir Next", 8, 'normal')

        self.namebox_1 = customtkinter.CTkLabel(self, text="Папка для сохранения", font=self.labels_font,
                                                width=210, height=25)
        self.namebox_1.grid(column=0, row=0, padx=5)

        self.check_directory()
        self.directory_choose_button = customtkinter.CTkButton(self, text=self.button_text, font=self.buttons_font,
                                                            width=210, height=20,
                                                            command = lambda: self.choose_new_dir(master))
        self.directory_choose_button.grid(column=0, row=1, padx=5)

        self.namebox_2 = customtkinter.CTkLabel(self, text="Название и формат файла", font=self.labels_font,
                                                width=210, height=25)
        self.namebox_2.grid(column=0, row=2, padx=5)

        self.file_name_entry = customtkinter.CTkEntry(self, textvariable=customtkinter.StringVar(value="Unnamed"),
                                            width=140, height=25,
                                            corner_radius=8, border_width=1)
        self.file_name_entry.grid(column=0, row=3, padx=5, sticky='nw')

        self.file_format_button = customtkinter.CTkOptionMenu(self,
                                                        width=65, height=25, corner_radius=5,
                                                        values=['.csv', '.xlsx', '.json'],
                                                        font=self.buttons_font,
                                                        command=None)
        self.file_format_button.grid(column=0, row=3, padx=5, sticky='ne')

        self.namebox_3 = customtkinter.CTkLabel(self, text="Источник данных", font=self.labels_font,
                                                width=210, height=25)
        self.namebox_3.grid(column=0, row=4, padx=5)

        self.data_source_button = customtkinter.CTkOptionMenu(self,
                                                        width=210, height=25, corner_radius=5,
                                                        values=['Заполненная форма', 'История парсинга', 'Записи парсера', 'Временная база', 'Локальная база'],
                                                        font=self.buttons_font,
                                                        command=None)
        self.data_source_button.grid(column=0, row=5, padx=5)

        self.instruction = customtkinter.CTkTextbox(self, width=250, height=115,
                                                    corner_radius=5, font=self.buttons_font, activate_scrollbars=False,
                                                    state='normal')
        self.instruction.insert('0.0','\nФайл с сохраненными в нем данными\nбудет находиться в выбранной папке,\nтакже к файлу, при наличии,\nбудет приложена\nпапка со скриншотами.')
        self.instruction.configure(state='disabled')
        self.instruction.grid(column=1, row=0, padx=5, rowspan=5)

        self.commit_button = customtkinter.CTkButton(self, text="Создать", font=self.buttons_font,
                                                            width=100, height=20,
                                                            command = lambda: self.create_file())
        self.commit_button.grid(column=1, row=5, padx=5, sticky='ne')

        self.decline_button = customtkinter.CTkButton(self, text="Отменить", font=self.buttons_font,
                                                            width=100, height=20,
                                                            command=lambda:self.destroy())
        self.decline_button.grid(column=1, row=5, padx=5, sticky='nw')

    def check_directory(self):
        self.dir_path = self.master.master.master.config_data['FILE_SAVE_SETTINGS']['save_dir']
        self.dir_name = os.path.basename(self.dir_path)
        if len(self.dir_name)>20: self.dir_name = self.dir_name[:10]+"..."
        if self.dir_name == "":
            self.button_text = "Выбрать"
        else:
            self.button_text = ".../"+self.dir_name
    
    def choose_new_dir(self, master):
        self.dir_path = fd.askdirectory()
        if self.dir_path != '': 
            self.dir_name = os.path.basename(self.dir_path)
            if len(self.dir_name)>20: self.dir_name = self.dir_name[:10]+"..."
            self.directory_choose_button.configure(text = ".../"+self.dir_name)
            master.master.master.config_data['FILE_SAVE_SETTINGS']['save_dir'] = self.dir_path
            config.set_config(master.master.master)

    def create_file(self):
        self.full_path = self.dir_path+"/"+self.file_name_entry.get()+self.file_format_button.get() # полный путь для создания
        if self.data_source_button.get()=="Заполненная форма": 
            self.data = None 
            self.data_source='form'
        if self.data_source_button.get()=="История парсинга": 
            self.data=db.Database().get_all_history() 
            self.data_source='parser_history'
        if self.data_source_button.get()=="Записи парсера": 
            self.data=db.Database().get_parse()
            self.data_source='parsed'
        if self.data_source_button.get()=="Временная база": 
            self.data=db.Database().get_temp()
            self.data_source='temporary'
        if self.data_source_button.get()=="Локальная база": 
            self.data=db.Database().get_ref()
            self.data_source='reference'
        if self.file_format_button.get()=='.csv': db.create_csv(self.full_path, self.data, self.data_source)
        #if self.file_format_button.get()=='.xlsx': db.create_csv(self.full_path, self.data, self.data_source)
        if self.file_format_button.get()=='.json': db.create_json(self.full_path, self.data, self.data_source)
        self.destroy()

# Окно для выбора файла сохранения
class Choose_Save_File(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("| Выбор файла |")
        self.geometry(f"460x110+{int((self.winfo_screenwidth()-460)/2)}+{int((self.winfo_screenheight()-110)/2)}")
        self.resizable(width=False, height=False)

        self.buttons_font = customtkinter.CTkFont("Avenir Next", 12, 'normal')
        self.labels_font = customtkinter.CTkFont("Avenir Next", 14, 'normal')
        self.instructions_font = customtkinter.CTkFont("Avenir Next", 8, 'normal')

        self.namebox_1 = customtkinter.CTkLabel(self, text="Файл для сохранения", font=self.labels_font,
                                                width=190, height=25)
        self.namebox_1.grid(column=0, row=0, padx=5)

        self.check_file()
        self.file_choose_button = customtkinter.CTkButton(self, text=self.button_text, font=self.buttons_font,
                                                            width=190, height=20,
                                                            command=lambda: self.choose_new_file(master))
        self.file_choose_button.grid(column=0, row=1, padx=5)

        self.namebox_3 = customtkinter.CTkLabel(self, text="Источник данных", font=self.labels_font,
                                                width=190, height=25)
        self.namebox_3.grid(column=0, row=2, padx=5)

        self.data_source_button = customtkinter.CTkOptionMenu(self,
                                                        width=190, height=25, corner_radius=5,
                                                        values=['Заполненная форма', 'История парсинга', 'Записи парсера', 'Временная база', 'Локальная база'],
                                                        font=self.buttons_font,
                                                        command=None)
        self.data_source_button.grid(column=0, row=3, padx=5)

        self.instruction = customtkinter.CTkTextbox(self, width=250, height=75,
                                                    corner_radius=5, font=self.buttons_font, activate_scrollbars=False,
                                                    state='normal')
        self.instruction.insert('0.0','Данные будут добавлены в\nвыбранный файл, в отдельную папку,\nпри наличии, будут\nсохранены скриншоты.')
        self.instruction.configure(state='disabled')
        self.instruction.grid(column=1, row=0, padx=5, pady=[0,5], rowspan=3)

        self.commit_button = customtkinter.CTkButton(self, text="Создать", font=self.buttons_font,
                                                            width=100, height=20,
                                                            command=lambda: self.save_to_file())
        self.commit_button.grid(column=1, row=0, padx=5, sticky='se', rowspan=4)

        self.decline_button = customtkinter.CTkButton(self, text="Отменить", font=self.buttons_font,
                                                            width=100, height=20,
                                                            command=lambda:self.destroy())
        self.decline_button.grid(column=1, row=0, padx=5, sticky='sw', rowspan=4)

    def check_file(self):
        self.file_path = self.master.master.master.config_data['FILE_SAVE_SETTINGS']['file_direction']
        self.file_ext = os.path.splitext(self.file_path)[1]
        self.file_name = os.path.basename(self.file_path)
        if len(self.file_name)>20: self.file_name = self.file_name[:10]+"..."
        if self.file_name == "":
            self.button_text = "Выбрать"
        else:
            self.button_text = "Выбрано: "+self.file_name

    def choose_new_file(self, master):
        self.file_path = fd.askopenfilename(filetypes=[ 
            ("data tables", "*.csv"),
            ("excel tables", "*.xlsx")])
        if self.file_path != '':
            self.file_ext = os.path.splitext(self.file_path)[1]
            self.file_name = os.path.basename(self.file_path)
            if len(self.file_name)>20: self.file_name = self.file_name[:10]+"..."
            self.file_choose_button.configure(text = "Выбрано: "+self.file_name)
            master.master.master.config_data['FILE_SAVE_SETTINGS']['file_direction'] = self.file_path
            config.set_config(master.master.master)

    def save_to_file(self):
        if self.data_source_button.get()=="Заполненная форма": 
            self.data = None 
            self.data_source='form'
        if self.data_source_button.get()=="История парсинга": 
            self.data=db.Database().get_all_history() 
            self.data_source='parser_history'
        if self.data_source_button.get()=="Записи парсера": 
            self.data=db.Database().get_parse()
            self.data_source='parsed'
        if self.data_source_button.get()=="Временная база": 
            self.data=db.Database().get_temp()
            self.data_source='temporary'
        if self.data_source_button.get()=="Локальная база": 
            self.data=db.Database().get_ref()
            self.data_source='reference'
        if self.file_ext=='.csv': db.add_to_csv(self.file_path, self.data, self.data_source)
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()