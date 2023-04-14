import sqlite3 as sl
import pandas as pd
import os

# Для базы данных
class Database():
    def __init__(self):
        self.connect = sl.connect("./Data/Save_data.db")
        self.curs = self.connect.cursor()
        self.curs.executescript(
        """
        CREATE TABLE IF NOT EXISTS REFERENCES_DB
        (CODE TEXT NOT NULL,
        NAME TEXT NOT NULL,
        PRICE REAL NOT NULL,
        PRICE_UNIT TEXT NOT NULL,
        UNIT TEXT NOT NULL,
        URL_ADRESS TEXT,
        SCREENSHOT BLOB);

        CREATE TABLE IF NOT EXISTS PARSE_RESULTS
        (CODE TEXT,
        NAME TEXT NOT NULL,
        PRICE REAL NOT NULL,
        PRICE_UNIT TEXT NOT NULL,
        UNIT TEXT NOT NULL,
        URL_ADRESS TEXT NOT NULL,
        SCREENSHOT BLOB,
        DATE TEXT NOT NULL);

        CREATE TABLE IF NOT EXISTS TEMPORARY_DB
        (CODE TEXT NOT NULL,
        NAME TEXT NOT NULL,
        PRICE REAL NOT NULL,
        PRICE_UNIT TEXT NOT NULL,
        UNIT TEXT NOT NULL,
        URL_ADRESS TEXT ,
        SCREENSHOT BLOB);

        CREATE TABLE IF NOT EXISTS SEARCH_HISTORY
        (CODE TEXT,
        NAME TEXT NOT NULL,
        PRICE REAL,
        PRICE_UNIT TEXT NOT NULL,
        UNIT TEXT NOT NULL,
        URL_ADRESS TEXT,
        SCREENSHOT BLOB,
        NUM INTEGER NOT NULL);
        """)
        self.connect.commit()

    def close_connection(self):
        self.connect.close()
    
    # ДЛЯ ИСТОРИИ ------------------- структура: (code, name, price, price_unit, unit, url, screenshot, num)
    def delete_history(self):
        self.curs.execute(
        "DELETE FROM SEARCH_HISTORY;")
        
        self.connect.commit()

    def add_history(self, data, maximum):
        self.curs.executescript(
        f"""
        UPDATE SEARCH_HISTORY SET NUM = NUM+1;
        DELETE FROM SEARCH_HISTORY WHERE NUM>{maximum};
        """)
        
        self.curs.execute(
        """   
        INSERT INTO SEARCH_HISTORY VALUES
        (?,?,?,?,?,?,?,?);
        """, data)
        
        self.connect.commit()

    def add_history_series(self, data, maximum):
        self.curs.executescript(
        f"""
        UPDATE SEARCH_HISTORY SET NUM = NUM+1;
        DELETE FROM SEARCH_HISTORY WHERE NUM>{maximum};
        """)
        for elem in data:
            self.curs.execute(
            """   
            INSERT INTO SEARCH_HISTORY VALUES
            (?,?,?,?,?,?,?,?);
            """, elem)

        self.connect.commit()

    def get_history(self, num):
        self.curs.execute(
        """
        SELECT * FROM SEARCH_HISTORY
        WHERE NUM = ?
        """,(num,))
        
        res = self.curs.fetchall()
        self.connect.commit()
        return(res)

    def get_all_history(self):
        self.curs.execute(
        """
        SELECT * FROM SEARCH_HISTORY
        """)
        
        res = self.curs.fetchall()
        self.connect.commit()
        return(res)
    
    # ДЛЯ ЗАПИСЕЙ ИЗ ДОКУМЕНТОВ ----- структура: (code, name, price, price_unit, unit, url, screenshot)
    def add_reference(self, data):
        self.curs.execute(
        """   
        INSERT INTO REFERENCES_DB VALUES
        (?,?,?,?,?,?,?);
        """, data)
        
        self.connect.commit()

    def get_ref_by_name(self, name):
        self.curs.execute(
        """
        SELECT * FROM REFERENCES_DB WHERE NAME = ?
        """, (name,))
        res = self.curs.fetchall()
        self.connect.commit()
        return(res)

    def delete_reference(self):
        self.curs.execute(
        "DELETE FROM REFERENCES_DB;")
        
        self.connect.commit()

    def get_ref(self):
        self.curs.execute(
        """
        SELECT * FROM REFERENCES_DB
        """,)

        res = self.curs.fetchall()
        self.connect.commit()
        return(res)

   # ДЛЯ ВРЕМЕННОЙ БАЗЫ ИЗ ДОКУМЕНТА ----- структура: (code, name, price, price_unit, unit, url, screenshot)
    def add_temporary(self, data):
        self.curs.execute(
        """   
        INSERT INTO TEMPORARY_DB VALUES
        (?,?,?,?,?,?,?);
        """, data)
        
        self.connect.commit()

    def get_temp_by_name(self, name):
        self.curs.execute(
        """
        SELECT * FROM TEMPORARY_DB WHERE NAME = ?
        """, (name,))
        res = self.curs.fetchall()
        self.connect.commit()
        return(res)

    def delete_temporary(self):
        self.curs.execute(
        "DELETE FROM TEMPORARY_DB;")
        
        self.connect.commit()

    def get_temp(self):
        self.curs.execute(
        """
        SELECT * FROM TEMPORARY_DB
        """,)

        res = self.curs.fetchall()
        self.connect.commit()
        return(res)
    
    # ДЛЯ ЗАПИСЕЙ ПАРСЕРА ----------- структура: (code, name, price, price_unit, unit, url, screenshot, date)
    def add_parse(self, data):
        self.curs.execute(
        """   
        SELECT DATETIME('now');
        """)
        time = self.curs.fetchall()
        data = list(data)
        data.append(time[0][0])
        
        self.curs.execute(
        """   
        INSERT INTO PARSE_RESULTS VALUES
        (?,?,?,?,?,?,?,?);
        """, data)
        
        self.connect.commit()

    def get_parse_by_name(self, name, time_warning):
        self.curs.execute(
        """
        SELECT * FROM PARSE_RESULTS WHERE NAME = ?
        """, (name,))
        res = self.curs.fetchall()
        
        for elem in res:
            self.curs.execute(
            f"""
            SELECT STRFTIME('%s', 'now') - STRFTIME('%s', "{elem[-1]}");
            """)
            time = self.curs.fetchall()
            elem = list(elem)
            if int(time[0][0])/3600>time_warning:
                elem.append(False)
            else:
                elem.append(True)

        self.connect.commit()
        return(res)

    def update_parse_by_name(self, name, url, new_data):
        self.curs.execute(
        f"""
        UPDATE PARSE_RESULTS SET PRICE = {new_data[1]}, SCREENSHOT = "{new_data[2]}", DATE = DATETIME('now')
        WHERE NAME = "{name}" AND URL_ADRESS = "{url}";
        """)
        
        self.connect.commit()

    def delete_parse(self):
        self.curs.execute(
        "DELETE FROM PARSE_RESULTS;")
        
        self.connect.commit()

    def get_parse(self):
        self.curs.execute(
        """
        SELECT * FROM PARSE_RESULTS
        """,)

        res = self.curs.fetchall()
        self.connect.commit()
        return(res)
    
# функция для создания временной базы данных из файла
def get_csv(path):
    data = pd.read_csv(path, sep=';')
    data.dropna(axis=1, how='all', inplace=True)
    return data

# создание временной базы данных из csv
def create_temporary_database_from_csv(data, index_tuple):
    database = Database()
    database.delete_temporary()

    # Создание словарей регулярных выражений для замены повторяющихся значений
    unit_replace_dict = {
        'шт\S+':'шт',
        'комп\S+':'комплект',
        'ка\S+':'картридж',
        'уп\S+':'упаковка',
    }

    # Замена данных в соответствии с заданными словарями
    data[index_tuple["unit_index"]].replace(unit_replace_dict, regex=True, inplace=True)
    # Редактирование данных и запись
    symbols_for_replace = '- ;,.\/:!?+=#@$^&'

    if index_tuple["url_index"] != None and index_tuple["screenshot_index"] == None:
        data = data.loc[index_tuple["start_row"]:,[
            index_tuple["code_index"],
            index_tuple["name_index"],
            index_tuple["price_index"],
            index_tuple["unit_index"],
            index_tuple["url_index"]
        ]]
        data.dropna(axis=0, how='any', inplace=True)
        for row in data.itertuples():
            database.add_temporary((row[1].lstrip(symbols_for_replace),
                                    row[2].lstrip(symbols_for_replace),
                                    row[3], index_tuple["price_unit"],
                                    row[4],
                                    row[5],
                                    None))
    
    if index_tuple["url_index"] == None and index_tuple["screenshot_index"] == None:
        data = data.loc[index_tuple["start_row"]:,[
            index_tuple["code_index"],
            index_tuple["name_index"],
            index_tuple["price_index"],
            index_tuple["unit_index"]
        ]]
        data.dropna(axis=0, how='any', inplace=True)
        for row in data.itertuples():
            database.add_temporary((row[1].lstrip(symbols_for_replace),
                                    row[2].lstrip(symbols_for_replace),
                                    row[3], index_tuple["price_unit"],
                                    row[4],
                                    None,
                                    None))

    if index_tuple["url_index"] != None and index_tuple["screenshot_index"] != None:
        data = data.loc[index_tuple["start_row"]:,[
            index_tuple["code_index"],
            index_tuple["name_index"],
            index_tuple["price_index"],
            index_tuple["unit_index"],
            index_tuple["url_index"],
            index_tuple["screenshot_index"]
        ]]
        data.dropna(axis=0, how='any', inplace=True)
        for row in data.itertuples():
            database.add_temporary((row[1].lstrip(symbols_for_replace),
                                    row[2].lstrip(symbols_for_replace),
                                    row[3], index_tuple["price_unit"],
                                    row[4],
                                    row[5],
                                    row[6]))
    
    database.close_connection()

# функции для создания файла из базы данных
def create_csv(path, data, data_source):
    # Обрабатываем тип заголовка для данных:
    if data_source in ["form", "temporary", "parsed", "reference"]:
        columns = ["Прайс лист", "Название", "Цена", "Валюта", "Ед. изм.", "URl-ссылка", "№ скриншота"]
    if data_source in ["parser_history"]:
        columns = ["Прайс лист", "Название", "Цена", "Валюта", "Ед. изм.", "URl-ссылка", "№ скриншота", "Номер запроса"]
    data = pd.DataFrame(data, columns=columns)
    # проверка имени файла
    counter=0
    new_path=path
    while os.path.exists(new_path):
        new_path = path[:-4]+"_"+str(counter)+path[-4:]
        counter += 1
    with open(new_path, 'w') as f: data.to_csv(f, index=False)

def create_json(path, data, data_source):
    # Обрабатываем тип заголовка для данных:
    if data_source in ["form", "temporary", "parsed", "reference"]:
        columns = ["Прайс лист", "Название", "Цена", "Валюта", "Ед. изм.", "URl-ссылка", "№ скриншота"]
    if data_source in ["parser_history"]:
        columns = ["Прайс лист", "Название", "Цена", "Валюта", "Ед. изм.", "URl-ссылка", "№ скриншота", "Номер запроса"]
    data = pd.DataFrame(data, columns=columns)
    # проверка имени файла
    counter=0
    new_path=path
    while os.path.exists(new_path):
        new_path = path[:-5]+"_"+str(counter)+path[-5:]
        counter += 1
    data.to_json(new_path, orient='records')

# функции для добавления данных в уже существующий файл
def add_to_csv(path, data, data_source):
    # Обрабатываем тип заголовка для данных:
    if data_source in ["form", "temporary", "parsed", "reference"]:
        columns = ["Прайс лист", "Название", "Цена", "Валюта", "Ед. изм.", "URl-ссылка", "№ скриншота"]
    if data_source in ["parser_history"]:
        columns = ["Прайс лист", "Название", "Цена", "Валюта", "Ед. изм.", "URl-ссылка", "№ скриншота", "Номер запроса"]
    # Запись в файл
    data = pd.DataFrame(data, columns=columns)
    with open(path, 'a') as f: data.to_csv(f, index=False)