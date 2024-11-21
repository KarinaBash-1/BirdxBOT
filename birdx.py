import base64
import json
import os
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime
def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def make_request(method, url, headers, json=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, json=json)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, data=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json, data=data)
        else:
            raise ValueError("Invalid method.")
        
        if response.status_code >= 420:
            if retry_count > 5:
                print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code: {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response.json()

class Birdx():
    def __init__(self):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            # "telegramauth": f"tma {token}",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127", "Microsoft Edge WebView2";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "Referer": "https://birdx.birds.dog/home",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
    
    def get_user_info(self, query):
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        url = "https://api.birds.dog/user"
        try:
            response = make_request('get', url, headers)
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def get_info(self, query):
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        url = 'https://api.birds.dog/minigame/incubate/info'
        try:
            response = make_request('get', url, headers)
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def upgraded(self, query):
        url = 'https://api.birds.dog/minigame/incubate/upgrade'
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        try:
            response = make_request('get', url, headers)
            if response is not None:
                sec = 3600
                print_(f"Upgraded Success, Level {response.get('level',0)} | Waiting Time : {round(sec*response.get('duration',0))} seconds")
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def confirm_upgrade(self, query):
        url = 'https://api.birds.dog/minigame/incubate/confirm-upgraded'
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        try:
            response = make_request('post', url, headers)
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def join_game(self, query):
        url = 'https://api.birds.dog/minigame/egg/join'
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        try:
            response = make_request('get', url, headers)
            if response is not None:
                data_turn = self.turn_game(query)
                turn = data_turn.get('turn')
                while True:
                    if turn <= 0:
                        data_claim_game = self.claim_game(query)
                        if data_claim_game is not None:
                            print_("Total Reward Claimed")
                        break
                    else:
                        data_play = self.play_game(query)
                        if data_play is not None:
                            result = data_play.get('result')
                            data_turn = self.turn_game(query)
                            if data_turn is not None:
                                total = data_turn.get('total')
                                turn = data_turn.get('turn')
                                print_(f"Play game done, Reward : {result} | Total Reward : {total}")


        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def turn_game(self, query):
        url = 'https://api.birds.dog/minigame/egg/turn'
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        try:
            response = make_request('get', url, headers)
            return response

        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def play_game(self, query):
        url = 'https://api.birds.dog/minigame/egg/play'
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        try:
            response = make_request('get', url, headers)
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def claim_game(self, query):
        url = 'https://api.birds.dog/minigame/egg/claim'
        headers = self.headers
        headers['telegramauth'] = f"tma {query}"
        try:
            response = make_request('get', url, headers)
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def mint_status(self, query):
        url = 'https://worm.birds.dog/worms/mint-status'
        headers = self.headers
        headers['authorization'] = f"tma {query}"
        try:
            response = make_request('get', url, headers)
            if response is not None:
                data = response.get('data',{})
                nextMintTime = data.get('nextMintTime')
                status = data.get('status','')
                print_(f"Status Mint Worm : {status}")
                if status == "MINT_OPEN":
                    data_mint = self.mint_worm(query)
                    data_user = self.get_user_info(query)
                    if data_mint is not None:
                        name = data_user.get('name',{})
                        id = data_user.get('telegramId',{})
                        username = data_user.get('telegramUserName',{})
                        minted = data_mint.get('minted',{})
                        message = data_mint.get('message','')
                        if message == 'SUCCESS':
                            print_(f"Data Worm : Type {minted.get('type','')} | reward {minted.get('reward',0)}")
                            print_(f"Data User : {name} | {id} | {username} ")
                        else:
                            print_(f" Mint Worm : {message}")
                            print_(f"Data User : {name} | {id} | {username} ")

                else:
                    if nextMintTime is not None:
                        dt_object = datetime.fromisoformat(nextMintTime.replace("Z", "+00:00"))
                        unix_time = int(dt_object.timestamp())
                        remaining = unix_time - time.time()
                        print_(f'Remaining Mint Worm : {round(remaining)} Seconds')
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
    
    def mint_worm(self, query):
        url = 'https://worm.birds.dog/worms/mint'
        headers = self.headers
        headers['authorization'] = f"tma {query}"
        try:
            response = make_request('post', url, headers)
            
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch user data for token. Error: {e}")
            return None
