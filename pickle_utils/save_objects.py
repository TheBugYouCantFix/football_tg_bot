import os.path

from pickle_object_saver import PickleObjectSaver
from parsing_data import InternationalMatchesParser

from logging_setup import setup_logging

pos = PickleObjectSaver()
path = os.path.relpath('../data/results.csv')
imp = InternationalMatchesParser(path)

if __name__ == '__main__':
    # takes 1 hour 32 minutes to run
    setup_logging()

    df = imp.get_country_all_time_wr_df()
    NAME = 'all_time_wr_df'

    # set the update argument to True to rewrite the file
    pos.save_object(df, NAME, update=False)
