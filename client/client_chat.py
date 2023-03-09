import requests

class ClientChat:
    """
    Methods for chat
    """
    def register_user(self, user, password):
        url = "http://127.0.0.1:8000/users/register/"

        payload = {
            "username": user,
            "password": password
        }

        response = requests.request("POST", url, json=payload)
        # resp = consumer.consum()

        return response

    def sanity(self):
        url = "http://127.0.0.1:8000/ping"
        response = requests.get(url)

        return response.text
