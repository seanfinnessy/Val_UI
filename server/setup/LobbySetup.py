import requests

class LobbySetup:
    '''
    Retrieve lobby details. Must be in game.
    '''

    def __init__(self, headers):
        self.headers = headers

    def get_latest_season_id(self, region):
        try:
            response = requests.get(
                f"https://shared.{region}.a.pvp.net/content-service/v3/content", headers=self.headers, verify=False)
            content = response.json()
            for season in content["Seasons"]:
                if season["IsActive"]:
                    return season["ID"]
        except:
            return -1