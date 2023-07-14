from __future__ import print_function
import pandas as pd
import numpy as np
import cfbd
import flatdict

pd.set_option('display.max_columns', None) # do not truncate columns

# Configure API key authorization: ApiKeyAuth
API_KEY ="C9GWPN0vXTck+dVEdIfWENsrmGokVf4gup4f1fPKJalpnslr26cmInmeqRNNcjax"
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = API_KEY
configuration.api_key_prefix['Authorization'] = 'Bearer'

def generate_df(games ):
    games_df_data = dict()
    for game in games:
        game_dict = game.to_dict()
        flattened_game_dict = flatdict.FlatDict(game_dict, delimiter='.')
        for k, v in flattened_game_dict.items():
            if k not in games_df_data:
                games_df_data[k] = []
            games_df_data[k].append(v)  
    return pd.DataFrame(games_df_data)
 

def get_venues():
    api_instance = cfbd.VenuesApi(cfbd.ApiClient(configuration))
    api_response = api_instance.get_venues()
    df = pd.DataFrame(columns = ["id", "name", "city", "state", "country_code", "capacity", "year_opened", "year_constructed", "grass"])
    for i in range(len(api_response)):
        df.loc[i] = [api_response[i].id, api_response[i].name, api_response[i].city, api_response[i].state, api_response[i].country_code, api_response[i].capacity,api_response[i].year_constructed, api_response[i].grass]

    return df

def get_team_season_stats_by_year(year):  
    api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))
    api_response = api_instance.get_team_season_stats(year=year)
    df = generate_df(api_response)
    return df

def get_team_season_stats(fyear,lyear):
    stat_categories=pd.read_csv("CSV/stat_categories.csv")
    Teams=pd.read_csv("CSV/Teams.csv")
    TEAM_SEASON_STATS = pd.DataFrame(columns=["season","team","stat_name","stat_value"])
    for year in range(fyear, lyear+1):
        df=get_team_season_stats_by_year(year)
        if not df.empty:
            df=df[["season","team","stat_name","stat_value"]]
            df=df[df["team"].isin(Teams["team"])& (df["stat_name"].isin(stat_categories["stat_categories"]))]
            TEAM_SEASON_STATS = pd.concat([TEAM_SEASON_STATS,df])
   
    return TEAM_SEASON_STATS.dropna()

def get_draft_picks_by_year(year):
    api_instance = cfbd.DraftApi(cfbd.ApiClient(configuration))
    api_response = api_instance.get_draft_picks(year=year)
    df = generate_df(api_response)
    return df

def get_draft_picks(fyear, lyear):
    Teams=pd.read_csv("CSV/Teams.csv")
    DRAFT_PICKS = pd.DataFrame(columns = ["nfl_team","college_team", "year", "round", "pick", "name", "position", "height", "weight","hometown_info.city","hometown_info.state"])
    for year in range(fyear, lyear+1):
         df=get_draft_picks_by_year(year)
         if not df.empty:
            df=df[["nfl_team","college_team", "year", "round", "pick", "name", "position", "height", "weight","hometown_info.city","hometown_info.state"]]
            df=df[df["nfl_team"].isin(Teams["team"])|df["college_team"].isin(Teams["team"])]
            
            DRAFT_PICKS = pd.concat([DRAFT_PICKS, df])
    return DRAFT_PICKS.dropna()


def get_player_season_stats_by_year_team(year,team):
    api_instance = cfbd.PlayersApi(cfbd.ApiClient(configuration))
    api_response = api_instance.get_player_season_stats(year=year,team=team)
    df = generate_df(api_response)
    return df

def get_player_season_stats(fyear, lyear):
    Players = pd.read_csv("CSV/Players.csv")
    PLAYER_SEASON_STATS = pd.DataFrame(columns =   ['season', 'player', 'team', 'category', 'stat_type', 'stat'])
    Teams = pd.read_csv("CSV/Teams.csv")
    for team in Teams["team"]:
        for year in range(fyear, lyear+1):
            df = get_player_season_stats_by_year_team(year,team)
            if not df.empty:
                df = df[['season', 'player', 'team', 'category', 'stat_type', 'stat']]
                df = df[(df["player"].isin(Players["name"]))&df["category"].isin(["passing","rushing","receiving","kicking","punting"])]
                df["season"] = year
                PLAYER_SEASON_STATS = pd.concat([PLAYER_SEASON_STATS, df])
                
    return PLAYER_SEASON_STATS.dropna()
      
def get_games_by_year(year):
    api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
    api_response = api_instance.get_games(year)
    df = generate_df(api_response)
    return df

def get_games(fyear,lyear):
    Teams = pd.read_csv("CSV/Teams.csv")
    GAMES = pd.DataFrame(columns =  ['id', 'season', 'week','home_team','home_points', 'away_team', 'away_points','home_win','away_win'])
    for year in range(fyear,lyear):
        df = get_games_by_year(year)
        if not df.empty:
            df = df[['id', 'season', 'week', 'home_team','home_points','away_team', 'away_points']]
            df = df[df["home_team"].isin(Teams["team"])&df["away_team"].isin(Teams["team"])]
            df["home_win"] = df["home_points"]>df["away_points"]
            df["away_win"] = df["home_points"]<df["away_points"]
            GAMES = pd.concat([GAMES, df])
    return GAMES.dropna()

def get_game_media_by_year(year):
    api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
    api_response = api_instance.get_game_media(year=year)
    df = generate_df(api_response)
    return df

def get_game_media(fyear,lyear):
    games = pd.read_csv("CSV/Games.csv")
    GAME_MEDIA = pd.DataFrame(columns = ['id', 'media_type', 'outlet'])  
    for year in range(fyear,lyear+1):
        df = get_game_media_by_year(year)
        if not df.empty:
            df = df[['id', 'media_type', 'outlet']]
            df = df[df["id"].isin(games["id"])]
            GAME_MEDIA = pd.concat([GAME_MEDIA, df])
    return GAME_MEDIA.dropna()

def generate_csv():
    # stat_categories= ['penalties','completionAttempts','extraPoints','fieldGoals','turnovers','kickingPoints','tackles','interceptions','rushingYards','totalPenaltiesYards','yardsPerPass']
    # stat_categories=pd.DataFrame(columns=["stat_categories"], data=stat_categories)
    # stat_categories.to_csv("stat_categories.csv",index=False)
    # Coach = pd.read_csv("CSV/Coach.csv")
    # Teams = pd.read_csv("CSV/Teams.csv")
    # Coach_Teams = pd.read_csv("CSV/Coach_Team.csv")
    # Coach_Teams= Coach_Teams[Coach_Teams["team"].isin(Teams["team"])]
    # Coach = Coach[Coach["ID"].isin(Coach_Teams["coach_ID"])]
    # Coach.to_csv("CSV/Coach2.csv",index=False)
    # Coach_Teams.to_csv("CSV/Coach_Team2.csv",index=False)
    # get_team_records(2010,2022).to_csv("CSV/Teams_Records.csv",index=False)
    # get_team_season_stats(2010,2022).to_csv("CSV/Teams_Season_Stats.csv",index=False)
    # get_games(2010,2022).to_csv("CSV/Games.csv",index=False)
    # get_game_media(2010,2022).to_csv("CSV/Games_Media.csv",index=False)
    # get_draft_picks(2010,2022).to_csv("CSV/Players.csv",index=False)
    # get_player_season_stats(2010,2022).to_csv("CSV/player_season_stats_2010_2022.csv",index=False)
   
    p=0 

if __name__ == "__main__":
    teams = pd.read_csv("CSV/Teams.csv")
    stadiums = pd.read_csv("CSV/Stadiums.csv")
    teams["stadium_id"] = int(teams["stadium_id"])
    #teams = teams.drop(columns= ["stadium_name","staduim_capacity","year_constructed"])
    teams.to_csv("CSV/Teams.csv",index=False)

    p=0