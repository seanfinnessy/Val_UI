import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class GameSetup:
    '''
    Basic utility needed for Valorant Local API
    '''
    @staticmethod
    def get_lockfile():
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')) as lockfile:
                data = lockfile.read().split(':')
                keys = ['name', 'PID', 'port', 'password', 'protocol']
                # dict constructor and zip function used to create dict with lockfile data.
                return (dict(zip(keys, data)))
        except:
            return -1
    
    @staticmethod
    def get_current_version():
        try:
            response = requests.get(
                "https://valorant-api.com/v1/version", verify=False)
            res_json = response.json()
            client_version = res_json['data']['riotClientVersion']
            return client_version
        except:
            return -1
        