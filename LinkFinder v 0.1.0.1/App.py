from PIL import Image, ImageTk
import tkinter
import customtkinter
from Libs import Check_phase_func as ch

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    # Основные параметры приложения / main parametres of app

    def __init__(self):
        super().__init__()
        # Основные параметры приложения / main parametres of app
        self.APP_WIDTH = 780
        self.APP_HEIGHT = 520

        self.TOP_WIDTH = 400
        self.TOP_HEIGHT = 200

        self.OPTIONS_WIDTH = 500
        self.OPTIONS_HEIGHT = 500

        self.find_center()

        self.title('LinkFinder v0.1.0.1')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")

        # Проверка версий драйверов
        versions = ch.find_drivers(ch.try_driver_last_version())
        if versions[0] == "warning":
            self.Messange(self, 'warning', 'Warning 0.1', 
            'Не найден драйвер подходящей версии,\n'+
            'подробное описание решения\n'+
            'данной проблемы можно найти в ReadmeRU.txt\n \n'+
            'Версия вашего браузера: '+ versions[1], skip_button='True')
        # Размещаем элементы главного окна
        #self.put_frames()
        self.options_open()
















    #============================================================================================================
    # Функция для поиска координат центра экрана / function to find coordinates of screen center
    def find_center(self):
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        # Координаты центра экрана для уведомлений и окон
        self.X_APP = (SCREEN_WIDTH / 2) - (self.APP_WIDTH / 2)
        self.Y_APP = (SCREEN_HEIGHT / 2) - (self.APP_HEIGHT / 2)

        self.X_TOP = (SCREEN_WIDTH / 2) - (self.TOP_WIDTH / 2)
        self.Y_TOP = (SCREEN_HEIGHT / 2) - (self.TOP_HEIGHT / 2)

        self.X_OPT = (SCREEN_WIDTH / 2) - (self.OPTIONS_WIDTH / 2)
        self.Y_OPT = (SCREEN_HEIGHT / 2) - (self.OPTIONS_HEIGHT / 2)
    # Класс уведомлений [cl = 'warning', 'info', 'error'] / messange class [cl = 'warning', 'info', 'error']
    class Messange(customtkinter.CTkToplevel):
        def __init__(self, app, cl, title, msg, skip_button=None):
            super().__init__()
            self.geometry(f"{app.TOP_WIDTH}x{app.TOP_HEIGHT}+{int(app.X_TOP)}+{int(app.Y_TOP)}")
            self.title(title)
            self.resizable(width=False, height=False)
            self.attributes('-topmost', 'true')
            
            frame = customtkinter.CTkFrame(self, width=380, height=180, corner_radius=10)
            frame.pack(padx=10, pady=10)
            frame.pack_propagate(0)
            
            img = ImageTk.PhotoImage(Image.open('/Users/Dima/Desktop/LinkFinder v 0.1.0.1/Design/'+ cl + '-outline.png'))
            icon_warning = customtkinter.CTkLabel(frame, width=50,height=180, image=img)
            icon_warning.pack(padx=10, side=tkinter.LEFT)

            text = customtkinter.CTkLabel(frame, width=300,height=160, 
                                            text=msg, text_font=("Roboto Medium", -12),
                                            justify=tkinter.LEFT)
            text.pack(side=tkinter.RIGHT)

            if skip_button == 'True': 
                if cl == 'warning':
                    color = '#E2E401'
                if cl == 'error':
                    color = '#FB0406'
                if cl == 'info':
                    color = '#03ACC7'
            
                button = customtkinter.CTkButton(frame,
                                                width=50, height=20, 
                                                border_width=1, corner_radius=8, 
                                                text="Пропустить",
                                                text_font=("Roboto Medium", -12),
                                                border_color=color, text_color=color, fg_color=None, bg_color=None, #hover_color=None,
                                                command=self.destroy)
                button.place(relx=0.7, rely=0.8)
            self.mainloop()

    def options_open(self):
        options = customtkinter.CTkToplevel(self)
        options.geometry(f"{self.OPTIONS_WIDTH}x{self.OPTIONS_HEIGHT}+{int(self.X_OPT)}+{int(self.Y_OPT)}")
        options.resizable(width=False, height=False)
        options.attributes('-topmost', 'true')







# Запуск приложения / Start app
if __name__ == "__main__":
    app = App()
    app.mainloop()
