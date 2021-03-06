from http import HTTPStatus
import time
import json

from flask import Flask, jsonify
from flask_sock import Sock
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from setup.GameSetup import GameSetup
from setup.LobbySetup import LobbySetup
from setup.LocalSetup import LocalSetup

# Setup for app
app = Flask(__name__)
api = Api(app)
sock = Sock(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.dn'
db = SQLAlchemy(app)
ma = Marshmallow(app)
last_game_state: str = ""

lockfile: dict = {'name': '', 'PID': '', 'port': '', 'password': '', 'protocol': ''}
headers: dict = {}
puuid: str = ""
region: str = ""
seasonId: str = ""

@sock.route("/lobby", methods=["GET"])
def get_game_state(ws):
    global last_game_state
    global headers
    global puuid
    global region
    global seasonId

    # Create lockfile
    lockfile = GameSetup.get_lockfile()

    # Create headers and PUUID
    headers, puuid = LocalSetup(lockfile).get_headers()
    print(puuid)

    # Get region
    region = LocalSetup(lockfile).get_region()

    # Get current season ID
    seasonId = LobbySetup(headers).get_latest_season_id(region)

    # Get presences (party info)
    game_state, game_name, game_tag, current_party = LocalSetup(
        lockfile).get_presence(puuid)
    print("The last game state: " + last_game_state)

    # While loop for game state.
    while True:
        time.sleep(5)
        # Check presence every 5 seconds. If user logs out of game, exit loop.
        try:
            game_state, game_name, game_tag, current_party = LocalSetup(lockfile).get_presence(puuid)
        except TypeError:
            raise Exception("Game has not started yet!")
        except UnboundLocalError:
            print("Looks like you logged out of your game.")
            # Set game state to LOGGED_OUT
            last_game_state = "LOGGED_OUT"
            break

        # Check game state and if you previously logged out.
        if game_state != last_game_state:
            last_game_state = game_state

            # Get presences for menus
            if last_game_state == "MENUS":
                ws.send(json.dumps({'game_state': game_state, 'game_name': game_name, 'game_tag': game_tag}))
                continue
            
            # Get presences for ingame
            if last_game_state == "INGAME":
                ws.send(json.dumps({'game_state': game_state, 'game_name': game_name, 'game_tag': game_tag}))
                continue
            
            # Send info to client
            ws.send(json.dumps({'game_state': game_state, 'game_name': game_name, 'game_tag': game_tag}))

# Resources
class Rank(Resource):
    def get(self, player_id):
        print(region)
        player_rank, win_percent = LobbySetup(headers).get_player_mmr(region, player_id, seasonId)
        result = json.dumps({
            "rankObj": player_rank,
            "winPercent": win_percent
        })
        return result, HTTPStatus.OK
        
api.add_resource(Rank, "/mmr/<string:player_id>")

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
