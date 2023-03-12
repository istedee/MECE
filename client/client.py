import curses
import getpass
import json
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
        self.chat = None
        self.rooms = []
        self.row = 3
        self.remote = None

    def my_handler(self, message):
        window_height = curses.LINES
        window_width = curses.COLS
        division_line =  int(window_height * 0.8)
        window = stdscr.subpad(division_line-2, window_width -2 , 1, 1)
        window_lines, window_cols = window.getmaxyx()
        bottom_line = window_lines - 2
        window.scrollok(1)
        splits = str(message.get("data")).split(":", 1)
        window.addstr(bottom_line, 2, "{} : {}".format(splits[0], splits[1]))
        window.scroll(1)
        window.refresh()

    def chat_room(self, stdscr, room):
        k=0
        cursor_x = 0
        cursor_y = 0
        stdscr.clear()
        stdscr.addstr(1, 2, "Room:{}".format(room))

        # Listen messages
        if self.remote:
            r = redis.Redis(host='redis-chatexperience.rahtiapp.fi', decode_responses=True, password="123")
        else:
            r = redis.Redis(decode_responses=True)
        sub = r.pubsub()
        sub.subscribe(**{room: self.my_handler})
        thread = sub.run_in_thread(sleep_time=0.001)

        height, width = stdscr.getmaxyx()
        chat_box_y = int(height * 0.2)
        chat_box_start = int(height*0.8)

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)
        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)
        statusbarstr = "Press 'ctrl' + 'g' and type 'q' to exit chatroom | Room:{} |".format(room)
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        
        rectangle(stdscr, 0,0, chat_box_start-1, width-1)

        while (k != ord('q')):

            self.row = height -1
            editwin = curses.newwin(chat_box_y-3, width-3, chat_box_start+1, 1)
            rectangle(stdscr, chat_box_start, 0, height-2, width-1)
            stdscr.refresh()

            box = Textbox(editwin)

            box.edit()
            message = box.gather()
            k = stdscr.getch()
            payload = {
                "message": message,
                "room_uuid": room,
                "api_token": self.apitoken,
                "user": self.username,
            }
            if k == curses.KEY_ENTER or k in [10, 13]:
                response = self.chat.post_message(message, room, self.apitoken, self.username)
                stdscr.getch()

    def login(self):
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        msg = {"username": username, "password": password}
        try:
            response, result = self.chat.check_user(username, password)
            if response.status_code != 200:
                print(result)
                time.sleep(1)
                return
        except TimeoutError:
            print("Are you connected?")
            return
        print(f"Welcome, {username}!")
        time.sleep(1)
        self.username = username
        self.apitoken = response.json()["api_token"]
        resp = self.chat.get_chat_rooms(self.apitoken)
        rooms = [[i["name"], i["uuid"]] for i in resp.json()]
        self.rooms.clear()
        self.rooms.extend(rooms)
        menu.items.append(MenuItem("Your rooms:"))
        for room in rooms:
            menu.items.append(
                FunctionItem(
                    f"{room[0], room[1]}",
                    my_menu.chat_room,
                    args=(stdscr, room[1])
                )
            )

    def register(self):
        username = input("Enter your desired username: ")
        password = getpass.getpass("Enter your desired password: ")
        msg = {"username": username, "password": password}
        try:
            response, detail = self.chat.register_user(username, password)
            if response.status_code != 200:
                return
        except Exception:
            print("Error!")
            time.sleep(1)
            return
        print(f"User {username} registered successfully!")
        time.sleep(1)

    def join_chatroom(self):
        if self.username is None:
            print("login first!")
            time.sleep(1)
            return
        print("Joining chatroom...")
        room_uuid = input("Give me a room_uuid: ")
        resp, detail = self.chat.join_chat_room(room_uuid, self.apitoken)
        print(resp.json())
        if resp.status_code == 200:
            menu.items.append(
                FunctionItem(
                    f"{resp.json().get('name')}, {resp.json().get('uuid')}",
                    my_menu.chat_room,
                    args=(stdscr, resp.json()["uuid"]),
                )
            )
        return
    
    def leave_chatroom(self):
        if self.username is None:
            print("login first!")
            time.sleep(1)
            return
        print("Leaving chatroom...")
        room_uuid = input("Give me a room_uuid: ")
        resp = self.chat.leave_chat_room(room_uuid, self.apitoken)
        menu.items.clear()
        stdscr.refresh()
        create_main_menu()
        resp = self.chat.get_chat_rooms(self.apitoken)
        rooms = [[i["name"], i["uuid"]] for i in resp.json()]
        self.rooms.clear()
        self.rooms.extend(rooms)
        for room in rooms:
            menu.items.append(
                FunctionItem(
                    f"{room[0], room[1]}",
                    my_menu.chat_room,
                    args=(stdscr, room[1])
                )
            )
        menu.show()
        return

    def create_chatroom(self):
        if self.username is None:
            print("login first!")
            time.sleep(1)
            return
        name = input("Enter server name: ")
        try:
            response, result = self.chat.create_chat_room(name, self.apitoken)
            if response.status_code != 200:
                return
            if response.json().get("status_code") == 409:
                return
        except TimeoutError:
            print("Are you connected?")
            return
        print("chatroom created!")
        room_uuid = response.json()["uuid"]

        self.chat.join_chat_room(room_uuid, self.apitoken)
        menu.items.clear()
        stdscr.refresh()
        create_main_menu()

        resp = self.chat.get_chat_rooms(self.apitoken)
        rooms = [[i["name"], i["uuid"]] for i in resp.json()]
        self.rooms.clear()
        self.rooms.extend(rooms)
        for room in rooms:
            menu.items.append(
                FunctionItem(
                    f"{room[0], room[1]}",
                    my_menu.chat_room,
                    args=(stdscr, room[1])
                )
            )
        menu.show()
        return


def parse_args():
    parser = argparse.ArgumentParser(description="Run a chat client")

    parser.add_argument(
        "--rahtiapp",
        type=bool,
        help="if you want to use rahtiapp: python3 client.py --rahtiapp=True",
    )

    return parser.parse_args()

menu = CursesMenu("Main Menu", "Select an option:")
my_menu = MyMenu()

def create_main_menu():
    menu.items.append(FunctionItem("Login", my_menu.login))
    menu.items.append(FunctionItem("Register", my_menu.register))
    menu.items.append(FunctionItem("Join Chatroom", my_menu.join_chatroom))
    menu.items.append(FunctionItem("Create Chatroom", my_menu.create_chatroom))
    menu.items.append(FunctionItem("Leave Chatroom", my_menu.leave_chatroom))

args = parse_args()

if args.rahtiapp is not None:
    my_menu.remote = True

create_main_menu()
try:
    my_menu.chat = client_chat.ClientChat(args.rahtiapp)
    menu.show()
except KeyboardInterrupt as e:
    pass
except:
    raise