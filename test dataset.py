from Libs import Data_func as df

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

database = df.Database()
#database.delete_history()
database.add_history_series((("","КОМПРЕССОРНО-КОНДЕНСАТОРНЫЙ БЛОК NSK 060 / ST", 
                                1888020.00, "RUB", "шт.", "http://flow-vent.ru/shop/product/kompressorno-kondensatornyy-blok-nsk-060", convert_to_binary_data('1.png')),
                            ("","КОМПРЕССОРНО-КОНДЕНСАТОРНЫЙ БЛОК NSK 060 / ST", 
                                None, "RUB", "шт.", "https://r507.ru/catalog/ned/kompressorno-kondensatornyy-blok-ned-nsk-060/",convert_to_binary_data('2.png')),
                            ("","КОМПРЕССОРНО-КОНДЕНСАТОРНЫЙ БЛОК NSK 060 / ST", 
                                None, "RUB", "шт.", "https://atlantcompany.ru/catalog/kkb/nsk_060_kompressorno_kondensatornyy_blok/", convert_to_binary_data('3.png'))), 
                            30, 'parse')
'''
database.delete_parse()
database.add_parse(("Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                21361.00, "RUB", "шт.", "https://ledeffect.ru/", convert_to_binary_data('1.png')))
database.add_parse(("Универсальный держатель с бетоном  Jupiter  ND1000", 
                                198.00, "RUB", "шт.", "https://rs24.ru/home.htm", convert_to_binary_data('2.png')))
database.add_parse(("Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                4166.61, "RUB", "шт.", "https://e-kc.ru/", convert_to_binary_data('3.png')))

database.delete_reference()
database.add_reference(("Светодиодный светильник 33 Вт, IP65, с закаленным стеклом   МЕТАН   LE-ССП-53-033-3773-65Д", 
                                21361.00, "RUB", "шт.", "https://ledeffect.ru/", None))
database.add_reference(("Универсальный держатель с бетоном  Jupiter  ND1000", 
                                198.00, "RUB", "шт.", "https://rs24.ru/home.htm", None))
database.add_reference(("Лоток перфорированный оцинкованный ИЭК 300х100х3000", 
                                4166.61, "RUB", "шт.", "https://e-kc.ru/", None))                
'''     
database.close_connection()