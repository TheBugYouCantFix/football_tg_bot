import datetime

import matplotlib.pyplot as plt

from pickle_utils.pickle_object_saver import PickleObjectSaver
from parsing_data import InternationalMatchesParser


class GraphMaker:

    def __init__(self, df):
        self.df = df[1:]  # start year is 1873 but the df starts from year 1873
        self.imp = InternationalMatchesParser()

    def n_best_by_wr(self, year, n=5) -> None:
        i = year - self.imp.START_YEAR
        wr_df = self.df.loc[i, 'wr_df'].head(n)
        wr_df.plot.bar(x='Country', y='Win_rate')

        plt.show()
        plt.title(f'Top {n} national football teams by win rate in {year}.')

    def country_wr(self, country):
        x, y = [], []

        for index, row in self.df.iterrows():

            wr_df = row['wr_df']
            year = row.iloc[0]
            filtered = wr_df['country'] == country.capitalize()
            rate = wr_df[filtered].iloc[0, 3]
            rate = round(rate, 1)

            x.append(year)
            y.append(rate)

            if year == datetime.date.today().year - 3:
                break

        plt.plot(x, y)

        plt.title(f'Win rate graph for national football team of {country.capitalize()}.')
        plt.xlabel('Year')
        plt.ylabel('Win rate')

        plt.show()


if __name__ == '__main__':
    pos = PickleObjectSaver()

    filename = 'all_time_wr_df.pickle'
    df = pos.get_object(filename)

    gm = GraphMaker(df)
    gm.country_wr('germany')
