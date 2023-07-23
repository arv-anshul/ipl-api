from fastapi import APIRouter, FastAPI, HTTPException, Query

from src.api.batter import get_batter_info
from src.api.bowler import get_bowler_info
from src.api.teams import Team, get_all_teams, get_team_desc, team_vs_team

app = FastAPI()
api_v1_router = APIRouter(prefix='/api/v1')


@app.get('/')
async def root():
    return {'name': 'IPL API', 'api_route': '/api/v1'}


@api_v1_router.get('/')
async def root_v1_router():
    return {'route': '/api/v1', 'version': '1.20.2', 'running': True}


@api_v1_router.get('/teams')
async def teams():
    teams = get_all_teams()
    return teams


@api_v1_router.get('/team-vs-team')
async def team_vs_team_route(
    t1: str = Query(None, description='Name of a IPL team.'),
    t2: str = Query(None, description='Name of a IPL team.'),
):
    if t1 is None or t2 is None:
        raise HTTPException(
            status_code=400, detail='Please provide both team names',
        )

    try:
        team1, team2 = Team.decode(t1), Team.decode(t2)
    except AttributeError:
        raise HTTPException(400, "Entered team doesn't exists.")

    return team_vs_team(team1, team2)


@api_v1_router.get('/team_desc')
async def get_team_desc(
    t: str = Query(None, description='Name of a IPL team.'),
):
    if t is None:
        raise HTTPException(
            status_code=400, detail='Please provide a team name',
        )

    try:
        t = Team.decode(t)
    except AttributeError:
        raise HTTPException(400, "Entered team doesn't exists.")

    return get_team_desc(t)


@api_v1_router.get('/batter')
async def batter(
    s: str = Query(None, description='Player name who played IPL.'),
):
    if s is None:
        raise HTTPException(
            status_code=400, detail='Please provide a batter name',
        )
    return get_batter_info(s)


@api_v1_router.get('/batter-vs-team')
async def batter_vs_team():
    raise HTTPException(status_code=404, detail='Not implemented yet')


@api_v1_router.get('/bowler')
async def bowler(
    s: str = Query(None, description='Bowler name who played IPL'),
):
    if s is None:
        raise HTTPException(
            status_code=400, detail='Please provide a bowler name',
        )
    return get_bowler_info(s)


app.include_router(api_v1_router)
