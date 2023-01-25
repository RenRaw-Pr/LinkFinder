import os
from PIL import Image
import tkinter
from tkinter import filedialog as fd
import customtkinter
from Libs import Check_phase_func as cp
from Libs import Config_func as conf


class App(customtkinter.CTk):
    # Основные параметры приложения / main parametres of app
    def __init__(self):
        super().__init__()
        self.params()
        self.find_center()

        self.title('| LinkFinder v 0.1.0.1 |')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Размещаем элементы главного окна
        self.put_main_frames()
        
        # Привязываем быстрые сочетания для главного окна
        self.keyboard_bind()
        
        # Проверка версий драйверов
        versions = cp.find_drivers(cp.try_driver_last_version())
        if versions[0] == "warning":
            Messange(self, 'warning', 'Warning 0.1', 
            'Не найден драйвер подходящей версии,\n'+
            'возможна работа только c базой данных.'+
            '\n \nВерсия вашего браузера: '+ versions[1], skip_button='True')
    #============================================================================================================
    # Технические функции 
    # Функция присвоения главных параметров / main parametres function
    def params(self):
        #(подгружаем данные из файла конфигурации)
        self.config_data = conf.get_config()
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
        self.data = Result_data(self)
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
        
        self.namebox = customtkinter.CTkLabel(self, text="Настройки поиска", font=("Arial", 14),
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

        self.namebox_2 = customtkinter.CTkLabel(self, text="Создание временной \nбазы данных из файла",
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
            conf.set_config(self.master.master)    

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
    def __init__(self, master):
        super().__init__(master, height=400, corner_radius=10)
        
        if master.master.config_data['USER_SETTINGS']['theme']=='Dark':
            self.info_bg_color = "#2B2B2B"
        if master.master.config_data['USER_SETTINGS']['theme']=='Light':
            self.info_bg_color = "#DBDBDB"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.infobox = tkinter.Canvas(self, bg=self.info_bg_color,  highlightthickness=0)
        self.infobox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="vertical",
                                                    width=15, corner_radius=5, border_spacing=2,
                                                    minimum_pixel_length=30,
                                                    hover=True,
                                                    command=self.infobox.yview)
        self.scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
        self.infobox.configure(yscrollcommand=self.scrollbar.set)
        
# Класс виджета сохранения данных в файл / save to file format frame class
class Save_to_file(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)

#============================================================================================================
# Классы для создания дополнительных окон     
# Класс уведомлений [cl = 'warning', 'info', 'error'] / messange class [cl = 'warning', 'info', 'error']
class Messange(customtkinter.CTkToplevel):
    def __init__(self, master, cl, title, msg, skip_button=None):
        super().__init__(master)
        self.geometry(f"{master.MSG_WIDTH}x{master.MSG_HEIGHT}+{int(master.X_MSG)}+{int(master.Y_MSG)}")
        self.title(title)
        self.resizable(width=False, height=False)
        self.attributes('-topmost', 'true')
        self.font = customtkinter.CTkFont(family="Avenir Next", size=12, weight='normal')

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
        self.icon_warning.grid(row=0, column=0, padx=10, pady=0, sticky="W")

        self.text = customtkinter.CTkLabel(self.frame,
                                            width=master.MSG_WIDTH-130,height=master.MSG_HEIGHT-20, 
                                            text=msg, #text_font=self.font,
                                            justify=tkinter.LEFT)
        self.text.grid(row=0, column=1, padx=10, pady=0, sticky="N")

        if skip_button == 'True': 
            if cl == 'warning':
                self.color = '#FFDE3B'
            if cl == 'error':
                self.color = '#FB0406'
            if cl == 'info':
                self.color = '#03ACC7'
            self.button = customtkinter.CTkButton(self.frame,
                                                    width=50, height=20, 
                                                    border_width=2, corner_radius=8, 
                                                    text="Пропустить",
                                                    #text_font=self.font,
                                                    border_color=self.color, text_color=self.color, fg_color="transparent", bg_color="transparent", hover_color=('#B0AFB1','#515152'),
                                                    command=self.destroy)
            self.bind('<Return>', self.destroy)
            self.button.place(anchor='se', x=master.MSG_WIDTH-25, y=master.MSG_HEIGHT-25)
            
        self.mainloop()

# Класс окна настроек / optons window class
class Options(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('| Настройки | Options |')
        self.geometry(f"{master.OPT_WIDTH}x{master.OPT_HEIGHT}+{int(master.X_OPT)}+{int(master.Y_OPT)}")
        self.resizable(width=False, height=False)
        self.attributes('-topmost', 'true')

        self.frame_left = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=master.OPT_HEIGHT-20,
                                                corner_radius=10)
        self.frame_left.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.frame_right = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=master.OPT_HEIGHT-105,
                                                corner_radius=10)
        self.frame_right.grid(row=0, column=1, sticky="ne", pady=10)

        self.frame_save = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=30,
                                                corner_radius=10)
        self.frame_save.grid(row=0, column=1, sticky="se", pady=10) 

        self.frame_default = customtkinter.CTkFrame(self,
                                                    width=(master.OPT_WIDTH-30)/2,
                                                    height=30,
                                                    corner_radius=10)
        self.frame_default.grid(row=0, column=1, sticky="se", pady=55)

        self.save_button = customtkinter.CTkButton(self.frame_save, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Сохранить изменения",
                                                    command=self.save_button_func)
        self.save_button.pack(padx=5, pady=5)

        self.default_button = customtkinter.CTkButton(self.frame_default, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="Сбросить настройки",
                                                    command=self.default_button_func)
        self.default_button.pack(padx=5, pady=5)



        self.label_1r = customtkinter.CTkLabel(self.frame_right,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Цветовое оформление:")
        self.label_1r.place(x=5, y=5)

        self.optionmenu_1r = customtkinter.CTkOptionMenu(self.frame_right,
                                                        width=(master.OPT_WIDTH-30)/2-20,
                                                        height=20,
                                                        values=conf.mix_values(["Dark", "Light", "System"],
                                                                                master.config_data['USER_SETTINGS']['theme']),
                                                        command=self.theme_button)
        self.optionmenu_1r.place(x=5, y=30)
        
        self.keyboard_bind()

    def theme_button(self, value):
        self.master.config_data['USER_SETTINGS']['theme'] = value
    
    def save_button_func(self):
        conf.set_config(self.master)
        self.master.refresh_by_config()
        self.destroy()
    
    def default_button_func(self):
        conf.return_to_default(self.master)
        conf.set_config(self.master)
        self.master.refresh_by_config()
        self.destroy()

    def keyboard_bind(self):
        self.bind('<Control-s>', lambda event : self.save_button_func())
        self.bind('<Control-d>', lambda event : self.default_button_func())
        self.bind('<Control-q>', lambda event : self.destroy())

# Класс модуля в окне результатов
class Info_module(customtkinter.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master, height=60, corner_radius=10)

# Запуск приложения / Start app
if __name__ == "__main__":
    app = App()
    app.mainloop()
