import curses
import getpass
import time
import requests
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, MenuItem


class MyMenu:
    def __init__(self):
        self.apitoken = None
        self.username = None
        self.rooms = []

    def login(self):
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        msg = {"username": username, "password": password}
        try:
            response = requests.post(
                "http://127.0.0.1:8000/users/check-api-token/", json=msg, timeout=20
            )
            if response.status_code != 200:
                print("login failed")
                time.sleep(1)
                return
        except TimeoutError:
            print("Are you connected?")
            return
        # Code for adding new user to the system goes here
        print(f"Welcome, {username}!")
        time.sleep(1)
        self.username = username
        self.apitoken = response.json()["api_token"]
        resp = requests.get(
            "http://127.0.0.1:8000/chatroom/rooms/",
            json={"api_token": self.apitoken},
            timeout=20,
        )
        rooms = [[i["name"], i["uuid"]] for i in resp.json()]
        self.rooms.clear()
        self.rooms.extend(rooms)

    def register(self):
        username = input("Enter your desired username: ")
        password = getpass.getpass("Enter your desired password: ")
        msg = {"username": username, "password": password}
        try:
            response = requests.post(
                "http://127.0.0.1:8000/users/register/", json=msg, timeout=20
            )
            if response.status_code != 200:
                return
        except Exception:
            print("Error!")
            time.sleep(1)
            return
        # Code for adding new user to the system goes here
        print(f"User {username} registered successfully!")
        time.sleep(1)

    def join_chatroom(self):
        # Code for joining an existing chatroom goes here
        if self.username is None:
            print("login first!")
            time.sleep(1)
            return
        print("Joining chatroom...")

    def create_chatroom(self):
        # Code for creating a new chatroom goes here
        if self.username is None:
            print("login first!")
            time.sleep(1)
            return
        name = input("Enter server name: ")
        msg = {"name": name, "api_token": self.apitoken}
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chatroom/create/", json=msg, timeout=20
            )
            if response.status_code != 200:
                return
            elif response.json().get("status_code") == 409:
                return
        except TimeoutError:
            print("Are you connected?")
            return
        print("chatroom created!")
        print(response.json())
        room_uuid = response.json()["uuid"]
        requests.post(
            "http://127.0.0.1:8000/chatroom/join/",
            json={"api_token": self.apitoken, "room_uuid": room_uuid},
            timeout=20,
        )
        resp = requests.get(
            "http://127.0.0.1:8000/chatroom/rooms/",
            json={"api_token": self.apitoken},
            timeout=20,
        )
        rooms = [[i["name"], i["uuid"]] for i in resp.json()]
        self.rooms.clear()
        self.rooms.extend(rooms)
        print("room created!")
        time.sleep(2)


menu = CursesMenu("Main Menu", "Select an option:")
my_menu = MyMenu()
item1 = MenuItem(my_menu.rooms, menu)
menu.items.append(FunctionItem("Login", my_menu.login))
menu.items.append(FunctionItem("Register", my_menu.register))
menu.items.append(FunctionItem("Join Chatroom", my_menu.join_chatroom))
menu.items.append(FunctionItem("Create Chatroom", my_menu.create_chatroom))
menu.items.append(item1)

menu.show()
