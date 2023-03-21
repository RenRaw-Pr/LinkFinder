from Libs import Data_func as df
import pandas as pd
import glob
import os

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

database = df.Database()
database.delete_reference()

path = '/Users/Dmitrii/Desktop/LinkFinder v 0.1.0.3/Data_for_check/*.csv'
files = glob.glob(path)
for file in files:
    data = pd.read_csv('././Data_for_check/'+os.path.basename(file), sep=';')
    data = data.iloc[2:,1:6]

    replace_dict = {
        'шт\S+':'шт',
        'комп\S+':'комплект',
        'ка\S+':'картридж',
        'уп\S+':'упаковка',
    }

    data['Ед.изм.'].replace(replace_dict, regex=True, inplace=True)
    data.dropna(axis=0, inplace=True)
    symbols_for_replace = '- ;,.\/:!?+=#@$^&'
    for row in data.itertuples():
        database.add_reference((row[1].lstrip(symbols_for_replace),row[2].lstrip(symbols_for_replace),row[5],'RUB',row[3],None,None))

database.close_connection()
