from flask import Flask
from flask_sock import Sock
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from setup.GameSetup import GameSetup
from setup.LobbySetup import LobbySetup
from setup.LocalSetup import LocalSetup

# Setup for app
app = Flask(__name__)
sock = Sock(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.dn'
db = SQLAlchemy(app)
ma = Marshmallow(app)

@sock.route("/lobby", methods=["GET"])
def get_hello(ws):
    # Create lockfile
    lockfile = GameSetup.get_lockfile()
    
    # Create headers and PUUID
    headers, puuid = LocalSetup(lockfile).get_headers()
    
    # Get region
    region = LocalSetup(lockfile).get_region()
    
    # Get current season ID
    seasonId = LobbySetup(headers).get_latest_season_id(region)
    
    while True:
        text = ws.receive()
        ws.send(text[::-1])
def main():
    app.run(debug=True)
    
if __name__ == "__main__":
    main()