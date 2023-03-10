import requests
import json

class ClientChat:
    """
    Methods for chat
    """
    def __init__(self, localhost):
        self.localhost = localhost

    def register_user(self, user, password):
        if self.localhost:
            url = "http://127.0.0.1:8000/users/register/"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/users/register/"

        payload = {
            "username": user,
            "password": password
        }

        response = requests.request("POST", url, json=payload)
        result = json.loads(response.text)

        return result.get('detail')

    def sanity(self):
        if self.localhost:
            url = "http://127.0.0.1:8000/ping"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/ping"
        
        response = requests.get(url)

        return response.text

    def check_user(self, username, password):
        if self.localhost:
            url = "http://127.0.0.1:8000/users/check-api-token/"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/users/check-api-token/"
        
        payload = {
            "username": username,
            "password": password
        }
        
        response = requests.request("POST", url, json=payload)
        result = json.loads(response.text)

        return response.status_code, result
    
    def post_message(self, message, room, token):
        if self.localhost:
            url = "http://127.0.0.1:8000/chatroom/post/"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/post/"

        payload = {
            "message": message,
            "room_uuid": room,
            "api_token": token
        }

        response = requests.request("POST", url, json=payload)

        return response

    def join_chat_room(self, name, token):
        if self.localhost:
            url = "http://127.0.0.1:8000/chatroom/join/"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/join/"

        payload = {
            "room_uuid": name,
            "api_token": token
        }

        response = requests.request("POST", url, json=payload)
        result = json.loads(response.text)

        return response, result

    def create_chat_room(self, name, token):
        if self.localhost:
            url = "http://127.0.0.1:8000/chatroom/create/"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/create/"

        payload = {
            "name": name,
            "api_token":token
        }

        response = requests.request("POST", url, json=payload)
        result = json.loads(response.text)

        return response, result


    def leave_chat_room(self, uuid, token):
        if self.localhost:
            url = "http://127.0.0.1:8000/chatroom/leave/"
        else:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/leave/"
        
        payload = {
            "room_uuid": uuid,
            "api_token": token
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers)

        return response
    