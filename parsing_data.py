import pandas as pd


class InternationalMatchesParser:
    PATH = './data/results.csv'
    df = pd.read_csv(PATH)

    # Code to add an "id" column:
    def __init__(self):
        self.df['id'] = self.df.index
        self.df.insert(0, 'id', self.df.pop('id'))

    def get_country_df(self, country):
        filtered = (self.df['home_team'].str.lower() == country.lower()) |\
                   (self.df['away_team'].str.lower() == country.lower())

        return self.df[filtered]

    def get_match_result(self, match_id):
        home_team_name, away_team_name, \
        home_team_score, away_team_score \
            = self.df.loc[match_id, 'home_team': 'away_score']

        if home_team_score > away_team_score:
            return home_team_name
        elif home_team_score < away_team_score:
            return away_team_name

        return 'Draw'

    def get_n_of_wins_for_country(self, country, official_only=True):
        # Returns number of wins in official(non-friendly) matches for a passes country
        counter = 0

        country_df = self.get_country_df(country)

        if official_only:
            official_matches = country_df['tournament'] != 'Friendly'
            country_df = country_df[official_matches]

        for i in range(country_df.shape[0]):
            match_id = country_df.iloc[i, 0]
            match_result = self.get_match_result(match_id)

            if match_result.lower() == country.lower():
                counter += 1

        return counter

    def matches_played(self, country, official_only=True):
        country_df = self.get_country_df(country)

        if official_only:
            official_matches = country_df['tournament'] != 'Friendly'
            country_df = country_df[official_matches]

        return len(country_df)

    def get_country_win_rate(self, country):

        win_rate = self.get_n_of_wins_for_country(country) /\
                   self.matches_played(country)

        win_rate = round(win_rate * 100, 1)

        return win_rate
