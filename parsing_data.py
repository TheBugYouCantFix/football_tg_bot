import pandas as pd


class InternationalMatchesParser:
    df = pd.read_csv('./data/results.csv')
    column_names = [i for i in df.columns]

    def get_country_df(self, country):
        filtered = (self.df['home_team'] == country) | (self.df['away_team'] == country)
        return self.df[filtered]

    def get_match_result(self, match_id):
        # Return value example: England - 4 Scotland - 2
        home_team_name, away_team_name, \
        home_team_score, away_team_score \
            = self.df.loc[match_id, 'home_team': 'away_score']

        if home_team_score > away_team_score:
            return home_team_name
        elif home_team_score < away_team_score:
            return away_team_name

        return 'Draw'


imp = InternationalMatchesParser()
print(imp.get_match_result(1000))