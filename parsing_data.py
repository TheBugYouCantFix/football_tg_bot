import pandas as pd
import pycountry as pc

from datetime import date

import logging


parsing_logger = logging.getLogger('parsing_logger')


class InternationalMatchesParser:

    DRAW = 'draw'
    START_YEAR = 1873

    def __init__(self, path='./data/results.csv'):
        self.PATH = path
        self.df = pd.read_csv(self.PATH)

        # Code to add an "id" column:
        self.df['id'] = self.df.index
        self.df.insert(0, 'id', self.df.pop('id'))

        self.win_rate_df = pd.DataFrame(columns=['year', 'matches_played', 'wins', 'wr_df'])

    @staticmethod
    def get_country_df(frame: pd.DataFrame, country: str) -> pd.DataFrame:
        filtered = (frame['home_team'].str.lower() == country.lower()) | \
                   (frame['away_team'].str.lower() == country.lower())

        return frame[filtered]

    @staticmethod
    def get_official_matches_df(frame: pd.DataFrame) -> pd.DataFrame:
        official_matches = frame['tournament'] != 'Friendly'

        return frame[official_matches]

    def get_match_result(self, match_id: int) -> str:
        home_team_name, away_team_name, \
            home_team_score, away_team_score \
            = self.df.loc[match_id, 'home_team': 'away_score']

        if home_team_score > away_team_score:
            return home_team_name
        elif home_team_score < away_team_score:
            return away_team_name

        return self.DRAW

    def get_n_of_wins_for_country(self, frame: pd.DataFrame, country: str, official_only=True):
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

    def matches_played(self, frame: pd.DataFrame, country: str, official_only=True) -> int:
        country_df = self.get_country_df(frame, country)

        if official_only:
            country_df = self.get_official_matches_df(country_df)

        return len(country_df)

    def year_is_valid(self, year: int) -> bool:
        if year <= self.START_YEAR or year > date.today().year:
            return False

        return True

    def after_year(self, year: int) -> pd.DataFrame:
        """
        Returns the df of matched held after a given year

        :param year:
        :return:
        """

        if not self.year_is_valid(year):
            return self.df

        filtered = self.df['date'].str[:4].astype(int) >= year

        return self.df[filtered]

    def in_year(self, year: int) -> pd.DataFrame:
        """
        Returns the df of matched held in a given year

        :param year:
        :return:
        """

        if not self.year_is_valid(year):
            return self.df

        filtered = self.df['date'].str[:4].astype(int) == year

        return self.df[filtered]

    def get_country_win_rate(self, df: pd.DataFrame, country: str) -> float:
        wins = self.get_n_of_wins_for_country(df, country)
        matches_played = self.matches_played(df, country)

        if matches_played == 0:
            return -1

        win_rate = wins / matches_played

        win_rate = round(win_rate * 100, 1)

        return win_rate

    def fill_countries_win_rate_df(self, df: pd.DataFrame, base_df: pd.DataFrame) -> pd.DataFrame:
        data = []

        for country in pc.countries:

            name = country.name

            p = self.matches_played(df, name)  # matches played in the year
            w = self.get_n_of_wins_for_country(df, name)  # wins in the year

            matches_after_prev_year = self.matches_played(base_df, name)  # matches played after the previous year
            matches = matches_after_prev_year - p  # matches played after the year

            if (matches == 0 or not isinstance(matches, int))\
                    and hasattr(country, 'official_name'):
                name = country.official_name
                matches = self.matches_played(base_df, name)

            wins = self.get_n_of_wins_for_country(base_df, name) - w  # wins played after the year

            if matches == 0:
                rate = 0
            else:
                rate = (wins / matches) * 100
                rate = round(rate, 1)

            data.append([name, matches, wins, rate])

        df = pd.DataFrame(data,
                          columns=['country', 'matches_played', 'wins', 'win_rate']
                          )

        max_n_of_wins = df['wins'].max()
        for i in range(df.shape[0]):
            if max_n_of_wins == 0:
                df.at[i, 'win_rate'] = 0
                continue

            row = df.iloc[i]
            wins = row['wins']

            weight = 0.7
            coefficient = (wins / max_n_of_wins) * weight
            final_rate = row['win_rate'] * coefficient * (2 - weight)

            df.at[i, 'win_rate'] = final_rate  # setting a new value of win rate

        sorted_df = df.sort_values(by=['win_rate'], ascending=False)

        return sorted_df

    def get_country_all_time_wr_df(self) -> pd.DataFrame:
        parsing_logger.info('data frame filling started...')

        # Pivot data
        base_df = self.df
        self.win_rate_df.at[0, 'year'] = self.START_YEAR - 1
        self.win_rate_df.at[0, 'wr_df'] = base_df

        for year in range(self.START_YEAR, date.today().year):
            df = self.in_year(year)
            wr_df = self.fill_countries_win_rate_df(df, base_df)

            i = year - self.START_YEAR  # calculating index

            # Setting values
            self.win_rate_df.at[i, 'year'] = year
            self.win_rate_df.at[i, 'wr_df'] = wr_df

            base_df = self.after_year(year)

            parsing_logger.info(f'year {year} stored')

        return self.win_rate_df
