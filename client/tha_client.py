import curses
import getpass
import time
import requests
import threading
import argparse
import redis
import client_chat
from curses.textpad import Textbox, rectangle
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, MenuItem

stdscr = curses.initscr()


class MyMenu:
    def __init__(self):
        self.apitoken = None
        self.username = None
        self.rooms = []
        self.row = 3

    def my_handler(self, message):
        self.row = self.row + 1
        stdscr.addstr(self.row, 2, "broker:{}".format(str(message.get("data"))))
        stdscr.refresh()

    def chat_room(self, stdscr, room):
        # stdscr.scrollok(1) # enable scrolling
        # stdscr.timeout(1)  # make 1-millisecond timeouts on `getch`
        k = 0
        stdscr.clear()
        stdscr.addstr(1, 2, "Room:{}".format(room))

        # Listen messages
        r = redis.Redis(host="0.0.0.0", decode_responses=True)
        sub = r.pubsub()
        sub.subscribe(**{room: self.my_handler})
        thread = sub.run_in_thread(sleep_time=0.001)

        while k != ord("q"):

            height, width = stdscr.getmaxyx()
            chat_box_y = int(height * 0.2)
            chat_box_start = int(height * 0.8)

            rectangle(stdscr, 0, 0, chat_box_start - 1, width - 1)
            editwin = curses.newwin(chat_box_y - 3, width - 3, chat_box_start + 1, 1)
            rectangle(stdscr, chat_box_start, 0, height - 2, width - 1)
            stdscr.refresh()

            box = Textbox(editwin)

            box.edit()
            message = box.gather()
            k = stdscr.getch()
            payload = {
                "message": message,
                "room_uuid": room,
                "api_token": self.apitoken,
            }
            if k == curses.KEY_ENTER or k in [10, 13]:
                response = requests.post(
                    url="http://127.0.0.1:8000/chatroom/post/", json=payload
                )

                stdscr.getch()
                # stdscr.scroll(1)
                self.row = self.row + 1

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
        menu.items.append(MenuItem("Your rooms:"))
        for i in resp.json():
            menu.items.append(
                FunctionItem(
                    f"{i['name']}, {i['uuid']}",
                    lambda: my_menu.chat_room(stdscr, i["uuid"]),
                )
            )

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
        room_uuid = input("Give me a room_uuid: ")
        resp = requests.post(
            "http://127.0.0.1:8000/chatroom/join/",
            json={"api_token": self.apitoken, "room_uuid": room_uuid},
            timeout=20,
        )
        print(resp.json())
        menu.items.append(
            FunctionItem(
                f"{resp.json().get('name')}, {resp.json()['uuid']}",
                lambda: my_menu.chat_room(stdscr, resp.json()["uuid"]),
            )
        )
        return

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
            if response.json().get("status_code") == 409:
                return
        except TimeoutError:
            print("Are you connected?")
            return
        print("chatroom created!")
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
        menu.items.append(
            FunctionItem(
                f"{response.json()['name'], response.json()['uuid']}",
                lambda: my_menu.chat_room(stdscr, response.json()["uuid"]),
            )
        )
        print("room created!")
        time.sleep(2)


def parse_args():
    parser = argparse.ArgumentParser(description="Run a chat client")

    parser.add_argument(
        "--localhost",
        type=bool,
        help="if you want to use localhost: python3 client.py --localhost=True",
    )

    return parser.parse_args()


args = parse_args()

menu = CursesMenu("Main Menu", "Select an option:")
my_menu = MyMenu()
# item1 = MenuItem(my_menu.rooms, menu)
menu.items.append(FunctionItem("Login", my_menu.login))
menu.items.append(FunctionItem("Register", my_menu.register))
menu.items.append(FunctionItem("Join Chatroom", my_menu.join_chatroom))
menu.items.append(FunctionItem("Create Chatroom", my_menu.create_chatroom))
# menu.items.append(item1)


menu.show()
