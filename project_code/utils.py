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