import datetime

import matplotlib.pyplot as plt

from pickle_utils.pickle_object_saver import PickleObjectSaver
from parsing_data import InternationalMatchesParser


class GraphMaker:

    def __init__(self, df):
        self.df = df[1:]  # start year is 1873 but the df starts from year 1873
        self.imp = InternationalMatchesParser()

    def n_best_by_wr(self, year: str, n: str) -> str:
        if not year.isdigit() or \
                int(year) < self.imp.START_YEAR or \
                int(year) > datetime.date.today().year:
            year = self.imp.START_YEAR

        if not n.isdigit() or \
                int(n) < 5 or int(n) > 10:
            n = 5

        year, n = int(year), int(n)

        i = year - self.imp.START_YEAR + 1
        wr_df = self.df.loc[i, 'wr_df'].head(n=n)
        wr_df.plot.bar(x='country', y='win_rate')

        plt.title(f'Top {n} national football teams by win rate since {year}.')
        plt.xlabel('Country')
        plt.ylabel('Year')

        filename = 'n_best_wr.png'
        plt.savefig(filename)

        return filename

    def country_wr(self, country: str) -> str:
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

        plt.clf()
        plt.plot(x, y)

        plt.title(f'Win rate graph for national football team of {country.capitalize()}.')
        plt.xlabel('Year')
        plt.ylabel('Win rate')

        filename = 'country_wr.png'
        plt.savefig(filename)

        return filename


if __name__ == '__main__':
    pos = PickleObjectSaver()

    file = 'all_time_wr_df.pickle'
    df = pos.get_object(file)

    gm = GraphMaker(df)
    gm.country_wr('germany')
