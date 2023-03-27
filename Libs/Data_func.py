import sqlite3 as sl
import pandas as pd

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
        URL_ADRESS TEXT NOT NULL,
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

# функция для создания временной базы данных из файла
def get_csv(path):
    data = pd.read_csv(path, sep=';')
    data.dropna(axis=1, how='all', inplace=True)
    return data

'''
def create_temporary_database_from_csv(path, code_index, name_index, price_index, unit_index, price_unit='RUB', url_index=None, screenshot_index=None):
    database = Database()
    database.delete_temporary()

    data = pd.read_csv(path, sep=';')
    data.dropna(axis=1, how='all', inplace=True)
    #data = data.iloc[:,[code_index,name_index,price_index,unit_index]]
    
    # Создание словарей регулярных выражений для замены повторяющихся значений
    unit_replace_dict = {
        'шт\S+':'шт',
        'комп\S+':'комплект',
        'ка\S+':'картридж',
        'уп\S+':'упаковка',
    }

    # Замена данных в соответствии с заданными словарями
    data[data.columns[unit_index]].replace(unit_replace_dict, regex=True, inplace=True)
    # Редактирование данных и запись
    symbols_for_replace = '- ;,.\/:!?+=#@$^&'
    
    if url_index != None and screenshot_index == None:
        for row in data.itertuples():
            database.add_temporary((row[code_index].lstrip(symbols_for_replace),
                                    row[name_index].lstrip(symbols_for_replace),
                                    row[price_index], price_unit,
                                    row[unit_index],
                                    row[url_index],
                                    None))
    if url_index == None and screenshot_index == None:
        for row in data.itertuples():
            database.add_temporary((row[code_index].lstrip(symbols_for_replace),
                                    row[name_index].lstrip(symbols_for_replace),
                                    row[price_index], price_unit,
                                    row[unit_index],
                                    None,
                                    None))
    if url_index != None and screenshot_index != None:
        for row in data.itertuples():
            database.add_temporary((row[code_index].lstrip(symbols_for_replace),
                                    row[name_index].lstrip(symbols_for_replace),
                                    row[price_index], price_unit,
                                    row[unit_index],
                                    row[url_index],
                                    row[screenshot_index]))
    database.close_connection()
'''