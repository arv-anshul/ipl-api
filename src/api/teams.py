from typing import Any

import numpy as np

from src.core.data import IPL_DF
from src.core.encoder import numpy_encoder
from src.core.exception import API_ERROR_MSG


def get_all_teams() -> dict[str, str]:
    temp = list(IPL_DF['Team1'].unique())
    all_teams = {
        'TotalTeams': len(temp),
        'AllTeams': sorted(temp),
        'Description': 'List of all teams played in IPL till now.',
    }
    return all_teams


@numpy_encoder
def team_vs_team(
    team1: str, team2: str,
) -> dict[str, str] | dict[Any, int]:
    temp = IPL_DF.query(
        'Team1==@team1 & Team2==@team2 | Team1==@team2 & Team2==@team1')

    if temp.shape[0] == 0:
        return {'error': API_ERROR_MSG.format(para='teams', job='exists')}

    dict_ = temp['WinningTeam'].value_counts().to_dict()
    dict_['TotalMatches'] = temp.shape[0]
    dict_['Draws'] = temp.shape[0] - temp['WinningTeam'].value_counts().sum()
    return dict_


@numpy_encoder
def get_team_desc(
    team: str,
) -> dict[str, dict[str, Any]] | dict[str, str]:
    team_df = IPL_DF.query('Team1==@team | Team2==@team')

    if team_df.shape[0] == 0:
        return {'Error': API_ERROR_MSG.format(para='team', job='exists')}

    matches_played = team_df.shape[0]
    matches_won = team_df.query('WinningTeam==@team').shape[0]
    matches_loss = matches_played - matches_won
    matches_draw = matches_played - (matches_won + matches_loss)
    toss_won = team_df.query('TossWinner==@team').shape[0]
    avg_margin = np.round(team_df['Margin'].mean(), 2)
    toss_decision = (team_df.query('TossWinner==@team')['TossDecision']
                     .value_counts().to_dict())
    matches_per_season = team_df['Season'].value_counts().to_dict()
    title_won = (team_df.query('MatchNumber=="Final" and WinningTeam==@team')
                 .shape[0])

    types_of_main_matches = [
        'Final', 'Qualifier 2', 'Eliminator', 'Qualifier 1',
        'Qualifier', 'Elimination Final', 'Semi Final',
        '3rd Place Play-Off',
    ]
    important_matches_played = team_df[
        team_df['MatchNumber'].isin(types_of_main_matches)
    ]['MatchNumber'].value_counts().to_dict()

    return {
        team: {
            'MatchesPlayed': matches_played,
            'MatchesWon': matches_won,
            'MatchesLoss': matches_loss,
            'MatchesDraw': matches_draw,
            'TossWon': toss_won,
            'TossDecision': toss_decision,
            'AvgMargin': avg_margin,
            'SeasonsPlayed': matches_per_season,
            'TitleWon': title_won,
            'ImportantMatchesPlayed': important_matches_played,
            'Description': f'Stats for the IPL team {team}.',
        }
    }
