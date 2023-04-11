import configparser
import os

# Функция для создания файла конфигурации, на случай его отсутствия или повреждения
def create_config():
    path = './Data/settings.ini'
    config = configparser.ConfigParser()
    config.add_section('DEFAULT_SETTINGS')
    config.set('DEFAULT_SETTINGS', 'Theme', 'Dark')

    config.add_section('USER_SETTINGS')
    config.set('USER_SETTINGS', 'Theme', '')
    
    config.add_section('SEARCH_SETTINGS')
    config.set('SEARCH_SETTINGS', 'temporary_base', '')
    
    config.set('SEARCH_SETTINGS', 'history_limit', '0')
    config.set('SEARCH_SETTINGS', 'scale', '4')
    
    config.set('SEARCH_SETTINGS', 'using_parser', 'False')
    config.set('SEARCH_SETTINGS', 'using_database', 'False')
    config.set('SEARCH_SETTINGS', 'using_temporary', 'False')

    config.set('SEARCH_SETTINGS', 'caps', 'False')
    config.set('SEARCH_SETTINGS', 'symbols', 'False')
    config.set('SEARCH_SETTINGS', 'only_nums', 'False')

    config.add_section('FILE_SAVE_SETTINGS')
    # используется при создании файла
    config.set('FILE_SAVE_SETTINGS', 'file_format', 'csv') # xlsx, csv, json
    config.set('FILE_SAVE_SETTINGS', 'file_name', '') # задается пользователем
    config.set('FILE_SAVE_SETTINGS', 'save_dir', str(os.path.expanduser("~/Downloads"))) # место сохранения экспортируемого файла (по умолчанию "загрузки")
    
    # используется при сохранении в файл
    config.set('FILE_SAVE_SETTINGS', 'file_direction', '')
    config.set('FILE_SAVE_SETTINGS', 'data_source', 'form') # form, parser_history, temporary, parsed, reference

    with open(path, "w") as config_file:
        config.write(config_file)

# Функция поиска параметра в файле конфигурации
def get_config():
    path='./Data/settings.ini'
    # В случае отсутствия файла, он будет создан
    if not os.path.exists(path):
        create_config()
    # Считывание данных
    config = configparser.ConfigParser()
    config.read(path)
    out = {}
    for section in config.sections():
        out[section] = {}
        for key, value in config.items(section):
            out[section][key] = value

    # Проверка и заполнение отсутствующих данных
    for key in out['USER_SETTINGS'].keys():
        if out['USER_SETTINGS'][key] == '':
            out['USER_SETTINGS'][key] = out['DEFAULT_SETTINGS'][key]
    
    return out

# Функция для записи в файл конфигурации
def set_config(master):
    path='./Data/settings.ini'
    # В случае отсутствия файла, он будет создан
    if not os.path.exists(path):
        create_config()
    # Запись данных
    config = configparser.ConfigParser()
    config.read(path)
    for key in master.config_data['USER_SETTINGS'].keys():
        config.set('USER_SETTINGS', key, master.config_data['USER_SETTINGS'][key])
    
    for key in master.config_data['SEARCH_SETTINGS'].keys():
        config.set('SEARCH_SETTINGS', key, master.config_data['SEARCH_SETTINGS'][key])
    with open(path, "w") as config_file:
        config.write(config_file)

# Функция для сброса настроек по умолчанию
def return_to_default(master):
    for key in master.config_data['USER_SETTINGS'].keys():
        master.config_data['USER_SETTINGS'][key] = master.config_data['DEFAULT_SETTINGS'][key]

# Функция замены для перестановки текущих настроек на первое место в списке
def mix_values(list, actual_value):
    new_list=[]
    new_list.append(actual_value)
    for elem in list:
        if elem != actual_value:
            new_list.append(elem)
    return new_list