import numpy as np
import pandas as pd

from .constant import BALL_BY_BALL_DATA_PATH, MATCHES_PATH

IPL_DF = pd.read_csv(MATCHES_PATH)
BALL_BY_BALL_DF = pd.read_csv(BALL_BY_BALL_DATA_PATH)

# Merged dataset
BALL_WITH_MATCH_DF = BALL_BY_BALL_DF.merge(IPL_DF, on='ID')

BALL_WITH_MATCH_DF['BowlingTeam'] = (
    BALL_WITH_MATCH_DF['Team1'] + BALL_WITH_MATCH_DF['Team2']
)

BALL_WITH_MATCH_DF['BowlingTeam'] = (
    BALL_WITH_MATCH_DF[['BowlingTeam', 'BattingTeam']]
    .apply(lambda x: x.values[0].replace(x.values[1], ''), axis=1)
)

# Batter data DataFrame
BATTER_DF = BALL_WITH_MATCH_DF[
    np.append(
        BALL_BY_BALL_DF.columns,
        ['BowlingTeam', 'Player_of_Match', 'Season', 'SuperOver']
    )
]
