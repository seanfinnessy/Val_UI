import base64
import json
import requests
import urllib3

from setup.GameSetup import GameSetup

class LocalSetup:
    '''
    Get user's region and headers for API access
    '''
    
    def __init__(self, lockfile) -> None:
        self.lockfile = lockfile
        self.local_headers = {'Authorization': 'Basic ' + base64.b64encode(('riot:' + self.lockfile['password']).encode()).decode()}
        
    def get_region(self):
        try:
            response = requests.get(
                f"https://127.0.0.1:{self.lockfile['port']}/product-session/v1/external-sessions", headers=self.local_headers, verify=False)
            res_json = response.json()
            return list(res_json.values())[0]['launchConfiguration']['arguments'][3].split("=")[1]
        except:
            return -1
    
    def get_headers(self):
        try:
            response = requests.get(
                f"https://127.0.0.1:{self.lockfile['port']}/entitlements/v1/token", headers=self.local_headers, verify=False)
            entitlements = response.json()
            puuid = entitlements['subject']
            headers = {
                'Authorization': f"Bearer {entitlements['accessToken']}",
                'X-Riot-Entitlements-JWT': entitlements['token'],
                'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
                'X-Riot-ClientVersion': GameSetup.get_current_version()
            }
            return headers, puuid
        except:
            return -1
        
    def get_presence(self, puuid):
        try:
            response = requests.get(f"https://127.0.0.1:{self.lockfile['port']}/chat/v4/presences", headers=self.local_headers, verify=False)
            presences = response.json()
            return self.sort_presences(presences, puuid)
        
        except ConnectionRefusedError:
            print("Having trouble retrieving presence.")
        except ConnectionAbortedError:
            print("Having trouble retrieving presence.")
        except ConnectionError:
            print("Having trouble retrieving presence.")
        except urllib3.exceptions.MaxRetryError:
            print("Requested too many times.")
            
    
    @staticmethod
    def sort_presences(presences, puuid):
        current_party: list = []
        my_party_id: str = ""
        
        for presence in presences['presences']:
            if presence['puuid'] == puuid:
                # Decode base64 'private' object.
                private_obj: object = json.loads(base64.b64decode(presence['private']))
                # Grab properties
                my_party_id = private_obj['partyId']
                my_name = presence['game_name']
                my_tag = presence['game_tag']
                game_state = private_obj["sessionLoopState"]
                # Append to current party list
                current_party.append({
                    "gameName": presence['game_name'],
                    "gameTag": presence['game_tag'],
                    "playerId": presence['puuid'],
                    "loggedInUser": True
                })
        
        for presence in presences['presences']:
            # Checkers for if presences are from Valorant.
            
            if "{" not in str(presence['private']) and presence['private'] is not None and presence['private'] != "":
                # Get rid of presence for league game.
                if json.loads(base64.b64decode(presence['private']))["partyId"] == my_party_id and presence['puuid'] != puuid:
                    current_party.append(
                        {
                            "gameName": presence['game_name'], 
                            "gameTag": presence['game_tag'], 
                            "playerId": presence['puuid'], 
                            "loggedInUser": False
                         })
        
        return game_state, my_name, my_tag, current_party