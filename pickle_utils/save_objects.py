import os.path

from pickle_object_saver import PickleObjectSaver
from parsing_data import InternationalMatchesParser

pos = PickleObjectSaver()
path = os.path.relpath('../data/results.csv')
imp = InternationalMatchesParser(path)

df = imp.get_country_all_time_wr_df()
NAME = 'all_time_wr_df'

pos.save_object(df, NAME)
