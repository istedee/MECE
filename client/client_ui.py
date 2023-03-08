import sys,os
import curses
from curses.textpad import Textbox, rectangle
import threading
import time


def receive_message():
    pass

def chat_room(stdscr):
    k=0
    stdscr.clear()
    while (k != ord('q')):
        height, width = stdscr.getmaxyx()
        chat_box_y = int(height * 0.2)
        chat_box_start = int(height*0.8)

        rectangle(stdscr, 0,0, chat_box_start-1, width-1)

        editwin = curses.newwin(chat_box_y-2, width-3, chat_box_start+1, 1)
        rectangle(stdscr, chat_box_start, 0, height-2, width-1)
        stdscr.refresh()

        box = Textbox(editwin)

        box.edit()
        k = stdscr.getch()


def chat_join(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2
    y = h//2
    text = "Join a room"
    stdscr.addstr(y-2, x - (len(text)//2), text)
    editwin = curses.newwin(1,30, y,x-15)
    box = Textbox(editwin)
    rectangle(stdscr, y-1,x-16, 1+y, 1+x-16+30+1)
    stdscr.refresh()
    box.edit()
    room = box.gather()
    k = stdscr.getch()
    if k == curses.KEY_ENTER or k in [10, 13]:
        chat_room(stdscr)
        stdscr.getch()

def crete_chat_room(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2
    y = h//2
    text = "Room name"
    stdscr.addstr(y-2, x - (len(text)//2), text)
    editwin = curses.newwin(1,30, y,x-15)
    box = Textbox(editwin)
    rectangle(stdscr, y-1,x-16, 1+y, 1+x-16+30+1)
    stdscr.refresh()
    box.edit()
    room = box.gather()
    k = stdscr.getch()
    if k == curses.KEY_ENTER or k in [10, 13]:
        chat_room(stdscr)
        stdscr.getch()

menu = ['Join Chat room', 'Create Chat Room', 'Exit']

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def chatmenu(stdscr, user):
    # turn off cursor blinking
    curses.curs_set(0)
    

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # specify the current selected row
    current_row = 0

    # print the menu
    print_menu(stdscr, current_row)

    while 1:
        stdscr.addstr(0, 0, "User: {}".format(user))
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                chat_join(stdscr, "asd")
            if current_row == 1:
                crete_chat_room(stdscr)
            stdscr.getch()
            # if user selected last row, exit the program
            if current_row == len(menu)-1:
                break

        print_menu(stdscr, current_row)

def draw_login(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "Curses example"[:width-1]
        subtitle = "Written by Clay McLeod"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        stdscr.addstr(2, 10, "Username")
        editwin = curses.newwin(1,30, 4,1)
        box = Textbox(editwin)
        rectangle(stdscr, 3,0, 1+3+1, 1+30+1)

        stdscr.addstr(6, 10, "Password")
        editwin2 = curses.newwin(1,30, 8,1)
        box2 = Textbox(editwin2)
        rectangle(stdscr, 7,0,9,32)


        # Refresh the screen
        stdscr.refresh()
        
        box.edit()
        box2.edit()
        user = box.gather()
        passw = box2.gather()

        # Wait for next input
        k = stdscr.getch()
        if k == curses.KEY_ENTER or k in [10, 13]:
            chatmenu(stdscr, user)
            stdscr.getch()

def main():
    curses.wrapper(draw_login)

if __name__ == "__main__":
    main()
