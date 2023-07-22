from flask import Flask, jsonify, request

from src.api.batter import get_batter_info
from src.api.bowler import get_bowler_info
from src.api.teams import get_all_teams, get_team_desc, team_vs_team
from src.core.exception import NOT_IMPLEMENTED

app = Flask(__name__)


@app.route('/')
def index():
    return 'Home Page IPL API'


@app.route('/api/teams')
def teams():
    # http://127.0.0.1:8501/api/teams
    return jsonify(get_all_teams())


@app.route('/api/teamvsteam')
def teamvteam():
    t1 = request.args.get('t1')
    t2 = request.args.get('t2')
    # http://127.0.0.1:8501/api/teamvsteam?t1=Mumbai%20Indians&t2=Chennai%20Super%20Kings
    if t1 is None or t2 is None: return NOT_IMPLEMENTED
    return jsonify(team_vs_team(t1, t2))


@app.route('/api/team_desc')
def get_team_desc_():
    s = request.args.get('s')
    # http://127.0.0.1:8501/api/team_desc?s=Mumbai%20Indians
    if s is None: return NOT_IMPLEMENTED
    return jsonify(get_team_desc(s))


@app.route('/api/batter')
def batter():
    s = request.args.get('s')
    # http://127.0.0.1:8501/api/batter?s=MS+Dhoni
    if s is None:
        return NOT_IMPLEMENTED
    return jsonify(get_batter_info(s))


@app.route('/api/batter-vs-team')
def batter_vs_team():
    return NOT_IMPLEMENTED


@app.route('/api/bowler')
def bowler():
    s = request.args.get('s')
    # http://127.0.0.1:8501/api/bowler?s=V+Kohli
    if s is None: return NOT_IMPLEMENTED
    return jsonify(get_bowler_info(s))


if __name__ == '__main__':
    app.run(port=8501, debug=True)
