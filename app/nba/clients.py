import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    playercareerstats,
    playergamelog,
    leaguedashplayerstats,
    leaguedashteamstats,
    scoreboardv2,
)

def search_players(name: str) -> list[dict]:
    return players.find_players_by_full_name(name)

def search_teams(name: str) -> list[dict]:
    all_teams = teams.get_teams()
    name_l = name.lower()
    return [t for t in all_teams if name_l in t["full_name"].lower()]

def get_player_career_seasons_df(player_id: int) -> pd.DataFrame:
    cs = playercareerstats.PlayerCareerStats(player_id=player_id)
    return cs.get_data_frames()[0]

def get_player_gamelog_df(player_id: int, season: str, season_type: str) -> pd.DataFrame:
    gl = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star=season_type
    )
    return gl.get_data_frames()[0]

def get_league_player_stats_df(season: str, season_type: str, per_mode: str) -> pd.DataFrame:
    dash = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star=season_type,
        per_mode_detailed=per_mode
    )
    return dash.get_data_frames()[0]

def get_league_team_stats_df(season: str, season_type: str, per_mode: str) -> pd.DataFrame:
    dash = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        season_type_all_star=season_type,
        per_mode_detailed=per_mode
    )
    return dash.get_data_frames()[0]

def get_scoreboard_dfs(game_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    sb = scoreboardv2.ScoreboardV2(game_date=game_date)
    return sb.game_header.get_data_frame(), sb.line_score.get_data_frame()
