import base64
import requests
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