import pandas as pd


class InternationalMatchesParser:
    PATH = './data/results.csv'
    df = pd.read_csv(PATH)

    # Code to add an "id" column:
    def __init__(self):
        self.df['id'] = self.df.index
        self.df.insert(0, 'id', self.df.pop('id'))

    @staticmethod
    def get_country_df(frame: pd.DataFrame, country):
        filtered = (frame['home_team'].str.lower() == country.lower()) |\
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

        return 'Draw'

    def get_n_of_wins_for_country(self, frame: pd.DataFrame, country, official_only=True):
        # Returns number of wins in official(non-friendly) matches for a passes country
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
        # Returns the df of matched held after a given year
        if year <= 1872:
            return self.df

        filtered = self.df['date'].str[:4].astype(int) >= year

        return self.df[filtered]

    def get_country_win_rate(self, country, after_year=-1):
        frame = self.after_year(after_year)

        win_rate = self.get_n_of_wins_for_country(frame, country) /\
                   self.matches_played(frame, country)

        win_rate = round(win_rate * 100, 1)

        return win_rate


    # TODO: implement graphs of win rate