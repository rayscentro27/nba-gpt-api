def key_player_search(name: str) -> str:
    return f"player_search:{name.strip().lower()}"

def key_player_career_seasons(player_id: int) -> str:
    return f"player_career_seasons:{player_id}"

def key_player_gamelog(player_id: int, season: str, season_type: str) -> str:
    return f"player_gamelog:{player_id}:{season}:{season_type}"

def key_league_player_stats(season: str, season_type: str, per_mode: str) -> str:
    return f"league_player_stats:{season}:{season_type}:{per_mode}"

def key_league_team_stats(season: str, season_type: str, per_mode: str) -> str:
    return f"league_team_stats:{season}:{season_type}:{per_mode}"

def key_scoreboard(game_date: str) -> str:
    return f"scoreboard:{game_date}"
