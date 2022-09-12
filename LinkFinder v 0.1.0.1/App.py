from PIL import Image, ImageTk
import tkinter
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
        '''
        # Проверка версий драйверов
        versions = cp.find_drivers(cp.try_driver_last_version())
        if versions[0] == "warning":
            Messange(self, 'warning', 'Warning 0.1', 
            'Не найден драйвер подходящей версии,\n'+
            'возможна работа только c базой данных.'+
            '\n \nВерсия вашего браузера: '+ versions[1], skip_button='True')
        '''
    #============================================================================================================
    # Технические функции 
    # Функция присвоения главных параметров / main parametres function
    def params(self):
        #(подгружаем данные из файла конфигурации)
        self.config_data = conf.get_config()
        #(применяем сохраненную конфигурацию)
        customtkinter.set_appearance_mode(self.config_data['USER_SETTINGS']['theme'])

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
        super().__init__(master, width=220, corner_radius=0, bg_color=None)
        self.main_opt = Options_list(self).pack(padx=5, pady=5)
        self.serch_opt = Search_options(self).pack(padx=5, pady=5)
        self.save_opt = Save_options(self).pack(padx=5, pady=5, expand=True, fill='y')

# Класс виджета поисковой строки / class of search frame
class Search(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=40, corner_radius=10, bg_color=None)       
        search_img = ImageTk.PhotoImage(Image.open('./Design/icon-search-outline.png'))
        clear_img = ImageTk.PhotoImage(Image.open('./Design/icon-cross-outline.png'))
        self.entry = customtkinter.CTkEntry(self, placeholder_text=None,
                                            height=30,
                                            corner_radius=8, border_width=1)
        self.entry.pack(side=tkinter.LEFT, expand=True, fill='x', padx=5, pady=5)

        self.clear_button = customtkinter.CTkButton(self, image=clear_img,
                                                    height=30, width=30,
                                                    corner_radius=8, border_width=1,
                                                    border_color='#0267A7', fg_color=None, bg_color=None,
                                                    text=None,
                                                    command=self.clear)
        self.clear_button.pack(side=tkinter.LEFT, padx=(0, 5), pady=5)
        master.bind('<Control-n>', lambda event : self.clear())
        self.search_button = customtkinter.CTkButton(self, image=search_img,
                                                    height=30, width=40,
                                                    corner_radius=8, border_width=1,
                                                    border_color='#0267A7', fg_color=None, bg_color=None,
                                                    compound="right",
                                                    text="Найти",
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
        self.settings_img = ImageTk.PhotoImage(Image.open('./Design/icon-settings-outline.png'))
        def settings():
            Options(master.master)

        self.button_1 = customtkinter.CTkButton(self, 
                                                image=self.settings_img,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color=None, bg_color=None,
                                                text=None,                                                  
                                                command=settings)
        self.button_1.place(x=5, y=5)
        
        self.button_2 = customtkinter.CTkButton(self,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color=None, bg_color=None,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_2.place(x=40, y=5)

        self.button_3 = customtkinter.CTkButton(self,
                                                height=30, width=30,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color=None, bg_color=None,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_3.place(x=75, y=5)

        self.button_4 = customtkinter.CTkButton(self,
                                                height=30, width=85,
                                                corner_radius=8, border_width=1,
                                                border_color='#0267A7', fg_color=None, bg_color=None,
                                                text='',
                                                state=tkinter.DISABLED)
        self.button_4.place(x=110, y=5)

# Класс виджета настроек поиска / search settings widget class
class Search_options(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200, height=400, corner_radius=10)

# Класс виджета настроек сохранения в файл / save to file widget class
class Save_options(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=200, corner_radius=10)

# Класс виджета вывода данных / result data frame class
class Result_data(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=400, corner_radius=10)

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
        
        self.frame = customtkinter.CTkFrame(self, 
                                        width=master.MSG_WIDTH-20, 
                                        height=master.MSG_HEIGHT-20, 
                                        corner_radius=10)
        self.frame.pack(padx=10, pady=10)
        self.frame.pack_propagate(0)
        
        self.img = ImageTk.PhotoImage(Image.open('./Design/icon-' + cl + '-outline.png'))
        self.icon_warning = customtkinter.CTkLabel(self.frame,
                                                    width=70,
                                                    height=70,
                                                    image=self.img)
        self.icon_warning.grid(row=0, column=0, padx=10, pady=10)

        self.text = customtkinter.CTkLabel(self.frame, width=300,height=160, 
                                            text=msg, text_font=("Roboto Medium", -12),
                                            justify=tkinter.LEFT)
        self.text.grid(row=0, column=1, padx=0, pady=10, sticky='w')

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
                                                    text_font=("Roboto Medium", -12),
                                                    border_color=self.color, text_color=self.color, fg_color=None, bg_color=None, hover_color=None,
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


# Запуск приложения / Start app
if __name__ == "__main__":
    app = App()
    app.mainloop()
