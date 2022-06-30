import requests

from utility.conversions import number_to_ranks

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
        
    def get_matchmaking_history(self, region, puuid) -> list:
        '''
        Returns last 10 comp matches
        '''
        try:
            response = requests.get(
                f"https://pd.{region}.a.pvp.net/match-history/v1/history/{puuid}?queue=competitive", headers=self.headers, verify=False
            )

            content = response.json()
            match_list:list = []
            for match in content["History"]:
                match_list.append(match)
            return match_list
        except:
            return -1
    
    def get_match_id(self, region, puuid) -> str:
        '''
        Get match ID of current match.
        '''
        try:
            response = requests.get(
                f"https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/players/{puuid}", headers=self.headers, verify=False)
            content = response.json()
            match_id: str = content["MatchID"]
            return match_id
        except:
            return -1
    
    def get_ongoing_match(self, region, match_id):
        '''
        Get ongoing match details
        '''
        try:
            response = requests.get(
                f"https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{match_id}", headers=self.headers, verify=False)
            content = response.json()
            players = content["Players"]
            # Get all PUUIDs in lobby
            player_dict = {"puuid": [], "agent": [], "team": [], "incognito": bool}
            for player in players:
                # Do not look up streamer mode players.
                if player["PlayerIdentity"]["Incognito"] == False:
                    player_dict["incognito"].append(False)
                    player_dict["puuid"].append(player["Subject"])
                    player_dict["agent"].append(player["CharacterID"])
                    player_dict["team"].append(player["TeamID"])
                else:
                    player_dict["incognito"].append(True)
                    player_dict["agent"].append(player["CharacterID"])
                    player_dict["team"].append(player["TeamID"])
                    
            map = str(content["MapID"]).rsplit("/", 1)[1]
            if content["ProvisioningFlow"] == "CustomGame":
                game_mode_in_ongoing_match = "Custom".upper()
            else:
                game_mode_in_ongoing_match = str(
                    content["MatchmakingData"]["QueueID"]).upper()
            return player_dict, map, game_mode_in_ongoing_match
        
        except:
            print('Error retrieving ongoing match.')
            return -1
    
    def get_player_mmr(self, region, player_id, seasonId):
        response = requests.get(
            f"https://pd.{region}.a.pvp.net/mmr/v1/players/{player_id}", headers=self.headers, verify=False)
        keys = ['CurrentRank', 'RankRating', 'Leaderboard']
        try:
            if response.ok:
                r = response.json()
                if r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId] or r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["NumberOfWinsWithPlacements"] != 0:
                    numberOfWins = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["NumberOfWinsWithPlacements"]
                    numberOfGames = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["NumberOfGames"]
                    winPercent = round(int(numberOfWins) /
                                       int(numberOfGames), 3) * 100
                else:
                    winPercent = 0
                rankTIER = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["CompetitiveTier"]
                if int(rankTIER) >= 24:
                    rank = [rankTIER,
                            r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["RankedRating"],
                            r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["LeaderboardRank"],
                            ]
                elif int(rankTIER) not in (0, 1, 2):
                    rank = [rankTIER,
                            r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonId]["RankedRating"],
                            'N/A',
                            ]
                else:
                    rank = [0, 0, 'N/A']
            else:
                print("Failed retrieving rank.")
                rank = [0, 0, 'N/A']
                winPercent = 0
        except TypeError:
            rank = [0, 0, 'N/A']
            winPercent = 0
        except KeyError:
            rank = [0, 0, 'N/A']
            winPercent = 0

        # Convert tier to rank name.
        rank[0] = number_to_ranks[rank[0]]
        return dict(zip(keys, rank)), winPercent