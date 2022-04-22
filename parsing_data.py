import pandas
import pandas as pd
import pycountry as pc
import matplotlib.pyplot as plt


class InternationalMatchesParser:

    DRAW = 'draw'

    def __init__(self, path='./data/results.csv'):
        self.PATH = path
        self.df = pd.read_csv(self.PATH)

        # Code to add an "id" column:
        self.df['id'] = self.df.index
        self.df.insert(0, 'id', self.df.pop('id'))

        self.win_rate_df = pd.DataFrame(columns=['year', 'wr_df'])

    @staticmethod
    def get_country_df(frame: pd.DataFrame, country):
        filtered = (frame['home_team'].str.lower() == country.lower()) | \
                   (frame['away_team'].str.lower() == country.lower())

        return frame[filtered]

    @staticmethod
    def get_official_matches_df(frame: pd.DataFrame):
        official_matches = frame['tournament'] != 'Friendly'

        return frame[official_matches]

    def get_match_result(self, match_id):
        home_team_name, away_team_name, \
            home_team_score, away_team_score \
            = self.df.loc[match_id, 'home_team': 'away_score']

        if home_team_score > away_team_score:
            return home_team_name
        elif home_team_score < away_team_score:
            return away_team_name

        return self.DRAW

    def get_n_of_wins_for_country(self, frame: pd.DataFrame, country, official_only=True):
        """
        Returns number of wins in official(non-friendly) matches for a passes country

        :param frame:
        :param country:
        :param official_only:
        :return:
        """
        counter = 0

        country_df = self.get_country_df(frame, country)

        if official_only:
            country_df = self.get_official_matches_df(country_df)

        for i in range(country_df.shape[0]):
            match_id = country_df.iloc[i, 0]
            match_result = self.get_match_result(match_id)

            if match_result.lower() == country.lower():
                counter += 1

        return counter

    def matches_played(self, frame, country, official_only=True):
        country_df = self.get_country_df(frame, country)

        if official_only:
            country_df = self.get_official_matches_df(country_df)

        return len(country_df)

    def after_year(self, year: int):
        """
        Returns the df of matched held after a given year

        :param year:
        :return:
        """

        if year <= 1872:
            return self.df

        filtered = self.df['date'].str[:4].astype(int) >= year

        return self.df[filtered]

    def get_country_win_rate(self, country, after_year=-1):
        frame = self.after_year(after_year)

        wins = self.get_n_of_wins_for_country(frame, country)
        matches_played = self.matches_played(frame, country)

        if matches_played == 0:
            return -1

        win_rate = wins / matches_played

        win_rate = round(win_rate * 100, 1)

        return win_rate

    def fill_countries_win_rate_df(self, df: pandas.DataFrame, year):
        data = []

        for country in pc.countries:
            name = country.name
            rate = self.get_country_win_rate(name)

            if rate == -1 and hasattr(country, 'official_name'):
                name = country.official_name

            wins = self.get_n_of_wins_for_country(df, name)
            rate = self.get_country_win_rate(name)

            if rate == -1:
                continue

            data.append([name, wins, rate])

        df = pd.DataFrame(data, columns=['country', 'wins', 'win_rate'])

        max_n_of_wins = df['wins'].max()
        for i in range(df.shape[0]):
            row = df.iloc[i]
            wins = row['wins']

            weight = 0.7
            coefficient = (wins / max_n_of_wins) * weight
            final_rate = row['win_rate'] * coefficient * (2 - weight)

            df.at[i, 'win_rate'] = final_rate  # setting a new value of win rate

        sorted_df = df.sort_values(by=['win_rate'], ascending=False)

        length = self.win_rate_df.shape[1]
        self.win_rate_df.at[length, 'year'] = year
        self.win_rate_df.at[length, 'wr_df'] = sorted_df

        print(self.win_rate_df)

        # self.build_win_rate_graph(sorted_df, 10)

    @staticmethod
    def build_win_rate_graph(df: pd.DataFrame, n=5):
        print(n)
        df = df.head(n)
        print(df)
        df.plot.bar(x='country', y='win_rate')
        plt.show()


if __name__ == '__main__':
    imp = InternationalMatchesParser()
    year = 2020
    new_df = imp.after_year(year)
    imp.fill_countries_win_rate_df(new_df, year)
