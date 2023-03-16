from Libs import Data_func as df

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

database = df.Database()
database.delete_history()
database.add_history_series((('Прайс лист Компания "LS-LED"',"Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                21361.00, "RUB", "шт.", "https://ledeffect.ru/", None, 1),
                            ('Прайс лист Компания "LS-LED"',"Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                27870.00, "RUB", "шт.", "https://rubilnik.ru/", None, 1),
                            ('Прайс лист Компания "LS-LED"',"Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                22850.00, "RUB", "шт.", "https://www.etm.ru/", None, 1)), 30)
database.add_history_series((('Прайс лист Интернет-магазин " ЭЛЕКТРИК "',"Универсальный держатель с бетоном  Jupiter  ND1000", 
                                198.00, "RUB", "шт.", "https://rs24.ru/home.htm", None, 1),
                            ('Прайс лист Интернет-магазин " ЭЛЕКТРИК "',"Универсальный держатель с бетоном  Jupiter  ND1000", 
                                235.52, "RUB", "шт.", "https://www.dkcmarket.ru/", None, 1),
                            ('Прайс лист Интернет-магазин " ЭЛЕКТРИК "',"Универсальный держатель с бетоном  Jupiter  ND1000", 
                                216.00, "RUB", "шт.", "https://www.etm.ru/", None, 1)), 30)
database.add_history_series((('п.339 КА; прайс лист №113',"Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                4166.61, "RUB", "шт.", "https://e-kc.ru/", None, 1),
                            ('п.339 КА; прайс лист №113',"Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                5625.00, "RUB", "шт.", "https://www.etm.ru/ipro3", None, 1),
                            ('п.339 КА; прайс лист №113',"Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                4395.00, "RUB", "шт.", "https://rs24.ru/home.htm", None, 1)), 30)

database.delete_parse()
database.add_parse(('Прайс лист Компания "LS-LED"',"Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                21361.00, "RUB", "шт.", "https://ledeffect.ru/", convert_to_binary_data('1.png')))
database.add_parse(('Прайс лист Интернет-магазин " ЭЛЕКТРИК "',"Универсальный держатель с бетоном  Jupiter  ND1000", 
                                198.00, "RUB", "шт.", "https://rs24.ru/home.htm", convert_to_binary_data('2.png')))
database.add_parse(('п.339 КА; прайс лист №113',"Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                4166.61, "RUB", "шт.", "https://e-kc.ru/", convert_to_binary_data('3.png')))

database.delete_reference()
database.add_reference(('Прайс лист Компания "LS-LED"',"Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                21361.00, "RUB", "шт.", "https://ledeffect.ru/", None))
database.add_reference(('Прайс лист Интернет-магазин " ЭЛЕКТРИК "',"Универсальный держатель с бетоном  Jupiter  ND1000", 
                                198.00, "RUB", "шт.", "https://rs24.ru/home.htm", None))
database.add_reference(('п.339 КА; прайс лист №113',"Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                4166.61, "RUB", "шт.", "https://e-kc.ru/", None))                     
database.close_connection()
