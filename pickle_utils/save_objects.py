import os.path

from pickle_object_saver import PickleObjectSaver
from parsing_data import InternationalMatchesParser

pos = PickleObjectSaver()
path = os.path.relpath('../data/results.csv')
imp = InternationalMatchesParser(path)


to_save = [imp.fill_countries_win_rate_df(imp.df, 2022)]

for item in to_save:
    pos.save_object(item, '1')
