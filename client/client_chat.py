import requests
import json

class ClientChat:
    """
    Methods for chat
    """
    def __init__(self, rahtiapp):
        self.rahtiapp = rahtiapp

    def register_user(self, user, password):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/users/register/"
        else:
            url = "http://127.0.0.1:8000/users/register/"

        payload = {
            "username": user,
            "password": password
        }

        response = requests.request("POST", url, json=payload, timeout=20)
        result = json.loads(response.text)

        return response, result.get('detail')

    def sanity(self):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/ping"
        else:
            url = "http://127.0.0.1:8000/ping"
        
        response = requests.get(url)

        return response.text

    def check_user(self, username, password):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/users/check-api-token/"
        else:
            url = "http://127.0.0.1:8000/users/check-api-token/"
        
        payload = {
            "username": username,
            "password": password
        }
        
        response = requests.request("POST", url, json=payload, timeout=20)
        result = json.loads(response.text)

        return response, result
    
    def post_message(self, message, room, token, username):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/post/"
        else:
            url = "http://127.0.0.1:8000/chatroom/post/"

        payload = {
            "message": message,
            "room_uuid": room,
            "api_token": token,
            "user": username
        }

        response = requests.request("POST", url, json=payload, timeout=20)

        return response

    def join_chat_room(self, name, token):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/join/"
        else:
            url = "http://127.0.0.1:8000/chatroom/join/"

        payload = {
            "room_uuid": name,
            "api_token": token
        }

        response = requests.request("POST", url, json=payload, timeout=20)
        result = json.loads(response.text)

        return response, result

    def create_chat_room(self, name, token):

        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/create/"
        else:
            url = "http://127.0.0.1:8000/chatroom/create/"

        payload = {
            "name": name,
            "api_token":token
        }

        response = requests.request("POST", url, json=payload)
        result = json.loads(response.text)

        return response, result


    def leave_chat_room(self, uuid, token):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/leave/"
        else:
            url = "http://127.0.0.1:8000/chatroom/leave/"
        
        payload = {
            "room_uuid": uuid,
            "api_token": token
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers)

        return response
    
    def get_chat_rooms(self, token):
        if self.rahtiapp:
            url = "http://server-fastapideploy-chatexperience.rahtiapp.fi/chatroom/rooms/"
        else:
            url = "http://127.0.0.1:8000/chatroom/rooms/"
        
        payload = {
            "api_token": token
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("GET", url, json=payload, headers=headers, timeout=20)

        return response
    