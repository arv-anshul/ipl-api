from typing import Any

import numpy as np

from src.core.data import BALL_WITH_MATCH_DF
from src.core.encoder import numpy_encoder
from src.core.exception import API_ERROR_MSG, NOT_IMPLEMENTED


def get_all_bowlers() -> dict[str, str]:
    return NOT_IMPLEMENTED


@numpy_encoder
def get_bowler_info(
    bowler: str,
) -> dict[str, dict[str, Any]] | dict[str, str]:
    df = BALL_WITH_MATCH_DF.query("bowler==@bowler")

    if df.shape[0] == 0:
        return {"Error": API_ERROR_MSG.format(para="bowler", job="ball")}

    Wickets = df["isWicketDelivery"].sum()
    PlayedWith = df["BowlingTeam"].unique().tolist()
    Innings = df["ID"].unique().shape[0]
    BallInSuperOver = df.query("SuperOver=='Y'").shape[0]
    SeasonsPlayed = df["Season"].unique().tolist()
    PlayerOfMatch = df.query("Player_of_Match==@bowler").shape[0]

    runs = df["batsman_run"].sum()
    overs = df.groupby("ID")["overs"].value_counts().sum()
    BowlerEconomyRate = runs / (overs / 6)
    BowlingAverage = runs / Wickets
    BowlingStrikeRate = df.shape[0] / Wickets

    Description = "Shows the Stats for bowler performance in IPL."

    return {
        bowler: {
            "Wickets": Wickets,
            "PlayedWith": PlayedWith,
            "Innings": Innings,
            "BallInSuperOver": BallInSuperOver,
            "SeasonsPlayed": SeasonsPlayed,
            "PlayerOfMatch": PlayerOfMatch,
            "BowlerEconomyRate": np.round(BowlerEconomyRate, 3),
            "BowlingAverage": np.round(BowlingAverage, 3),
            "BowlingStrikeRate": np.round(BowlingStrikeRate, 3),
            "Description": Description,
        }
    }
