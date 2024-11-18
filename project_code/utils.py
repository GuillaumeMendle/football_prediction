import pandas as pd
import numpy as np

def add_team_name(df : pd.DataFrame, teams_data : pd.DataFrame) -> pd.DataFrame:
    """
    Merge the results dataset with the team dataset to add the name of the playing teams for every fixture. 
    """
    df = df.merge(teams_data, left_on="HomeTeamID", right_on = "TeamID", how="left")\
        .rename(columns = {"TeamName" : "HomeTeamName"})\
            .drop(columns="TeamID")

    return df.merge(teams_data, left_on="AwayTeamID", right_on = "TeamID", how="left")\
        .rename(columns = {"TeamName" : "AwayTeamName"})\
            .drop(columns="TeamID")


def add_points(score_team1 : int, score_team2 : int) -> int:
    """
    Returns 3 points if Team 1 scored more goals than Team 2
    1 point for a draw
    0 points if Team 2 scored more goals than Team 1
    """
    if score_team1>score_team2:
        return 3
    elif score_team1<score_team2:
        return 0
    else:
        return 1
    

def melt_results_dataset(df : pd.DataFrame) -> pd.DataFrame:
    """
    Concatenate the points scored for home and away into a single column PointsScored for easier calculations later on.
    """
    df_team_home = pd.melt(df, id_vars = ["HomeTeamID", "HomeTeamName","Gameweek"], value_vars = ["HomePoints"], value_name="PointsScored")\
    .rename(columns={"HomeTeamID":"TeamID", "HomeTeamName":"TeamName"})\
    .drop(columns="variable")

    df_team_away = pd.melt(df, id_vars = ["AwayTeamID", "AwayTeamName","Gameweek"], value_vars = ["AwayPoints"], value_name="PointsScored")\
    .rename(columns={"AwayTeamID":"TeamID", "AwayTeamName":"TeamName"})\
    .drop(columns="variable")

    return pd.concat((df_team_home, df_team_away)).sort_values(["Gameweek", "TeamID"], axis = 0)


def generate_final_ranking(df : pd.DataFrame) -> pd.DataFrame:
    """
    Generate the final ranking of season by summing the total number of points scored by every team
    throughout season 1. 
    """
    ## Aggregate per team and sum the total number of points scored by team
    df_ranking_season = df.groupby(["TeamID", "TeamName"]).agg(
        TotalPoints = ("PointsScored", "sum")
    ).sort_values(by="TotalPoints", ascending=False).reset_index()

    ## Creation of a ranking variable
    df_ranking_season["Ranking"] = np.arange(1, len(df_ranking_season)+1)

    return df_ranking_season

class GoalkeeperPreprocessing:
    def __init__(self, homonymous_player_names):
        self.homonymous_player_names = homonymous_player_names
        
    def create_player_ID(self, df : pd.DataFrame) -> pd.DataFrame:
        """
        Create a unique player ID. 
        """
        df["PlayerID"] = np.arange(1, len(df)+1)
        return df
    
    def link_players_to_teamID(self, players_data : pd.DataFrame, player_names : list)->str:
        """
        Link the team ID to the list of players in the dataset containing the starting XI of every game. 
        It uses the players' name except for the ones which are not unique.
        """
        for _name in player_names:
            if _name not in self.homonymous_player_names:
                return players_data[players_data["PlayerName"]==_name]["TeamID"].values[0]
            else: 
                continue

    def explode_startingXI_dataset(self, df : pd.DataFrame, players_data : pd.DataFrame) -> pd.DataFrame:
        """
        Return a StartingXI dataset with one unique player per row per game.
        """
        df = df.explode("StartingXI").rename(columns = {"StartingXI" : "PlayerName"})
        df = df.merge(players_data, on = ["PlayerName", "TeamID"], how = "left")
        df["MatchPlayed"] = 1 ## This variable will be useful later on for any calculations (e.g.: to count the number of games played)
        return df
    
    def run_goalkeeper_preprocessing(self, results_data : pd.DataFrame, startingXI_data : pd.DataFrame, players_data : pd.DataFrame) -> pd.DataFrame:
        """
        Run the preprocessing pipeline for the goalkeeper ratings generation. 
        """
        ## Creation of a unique player ID
        players_data = self.create_player_ID(players_data)

        ## Add team ID to the dataset using players' name
        startingXI_data_copy = startingXI_data.copy()
        startingXI_data_copy["StartingXI"] = startingXI_data_copy["StartingXI"].map(lambda x: x.split(","))
        startingXI_data_copy["TeamID"] = startingXI_data_copy["StartingXI"].map(lambda x: self.link_players_to_teamID(players_data, x))

        ## Explode the dataframe to get one player per row, per game, per team
        startingXI_data_exploded = self.explode_startingXI_dataset(startingXI_data_copy, players_data)

        ## Merge the season results with the players dataset
        df_merged = startingXI_data_exploded.merge(results_data, on = ["MatchID"], how = "right")
        results_with_players = df_merged.copy()
        return results_with_players
    
    def create_new_variables(self, df : pd.DataFrame) -> pd.DataFrame:
        """
        Creation of new variables which contain the number of goals scored by a team for a game
        with no distinction of home/away.
        """
        df["TeamScore"] = df.apply(lambda x : x.HomeScore if x.TeamID == x.HomeTeamID else x.AwayScore, axis=1)
        df["OpponentScore"] = df.apply(lambda x : x.AwayScore if x.TeamID == x.HomeTeamID else x.HomeScore, axis=1)
        df = df.drop(columns = ["HomeScore", "AwayScore"])


        df["TeamShots"] = df.apply(lambda x : x.HomeShots if x.TeamID == x.HomeTeamID else x.AwayShots, axis=1)
        df["OpponentShots"] = df.apply(lambda x : x.AwayShots if x.TeamID == x.HomeTeamID else x.HomeShots, axis=1)
        df = df.drop(columns = ["HomeShots", "AwayShots"])
        return df
