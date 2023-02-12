from PIL import Image
import tkinter
from tkinter import filedialog as fd
import customtkinter
from Libs import Data_func as db

import App

main = customtkinter.CTk()
main.title('test infomodule')
main.geometry('700x500')
customtkinter.set_appearance_mode('light')
database = db.Database()
data = database.get_parse_by_name("Универсальный держатель с бетоном  Jupiter  ND1000", 1)

infobox = App.Info_module(main, data[0], data_type='parse')
infobox.pack(padx=10, pady=10, fill='x')

main.mainloop()