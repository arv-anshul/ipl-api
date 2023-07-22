from typing import Any

import numpy as np

from src.core.data import BATTER_DF
from src.core.encoder import numpy_encoder
from src.core.exception import API_ERROR_MSG, NOT_IMPLEMENTED


def get_all_batters() -> dict[str, str]:
    return NOT_IMPLEMENTED


@numpy_encoder
def get_batter_info(
    player: str,
) -> dict[str, dict[str, Any]] | dict[str, str]:
    df = BATTER_DF.query("batter==@player")

    if df.shape[0] != 0:
        TotalRun = df["batsman_run"].sum()
        Innings = df["ID"].unique().shape[0]
        AverageScore = TotalRun / Innings
        Sixes = df.query("batsman_run==6 and non_boundary==0").shape[0]
        Fours = df.query("batsman_run==4 and non_boundary==0").shape[0]
        TotalRunBySeason = df.groupby("Season")["batsman_run"].sum().to_dict()
        TimesOut = df.query("player_out==@player").shape[0]
        PlayedFor = df["BattingTeam"].unique().tolist()
        HowOut = (df.query("player_out==@player")["kind"]
                  .value_counts().to_dict())
        PlayerOfMatch = (df.groupby("ID")["Player_of_Match"].unique()
                         .isin([player]).sum())
        SeasonsPlayed = df["Season"].unique().tolist()
        BatInSuperOver = df.query('SuperOver=="Y"').shape[0]

        # Fifty & Century
        runs = np.array(df.groupby("ID")["total_run"].sum().values)
        Fifty = sum((runs >= 50) & (runs < 100))
        Century = sum(runs >= 100)

        # StrikeRate
        balls_played = df.query('not extra_type=="wides"').shape[0]
        if balls_played:
            StrikeRate = np.round((TotalRun / balls_played) * 100, 3)
        else:
            StrikeRate = 0

        Description = f"Show the stats of {player} for the IPL."

        return {
            player: {
                "TotalRun": TotalRun,
                "Innings": Innings,
                "AverageScore": AverageScore,
                "Sixes": Sixes,
                "Fours": Fours,
                "TotalRunBySeason": TotalRunBySeason,
                "TimesOut": TimesOut,
                "PlayedFor": PlayedFor,
                "HowOut": HowOut,
                "PlayerOfMatch": PlayerOfMatch,
                "Fifty": Fifty,
                "Century": Century,
                "StrikeRate": StrikeRate,
                "SeasonsPlayed": SeasonsPlayed,
                "BatInSuperOver": BatInSuperOver,
                "Description": Description,
            }
        }

    else:
        return {"error": API_ERROR_MSG.format(para="batter", job="bat")}
