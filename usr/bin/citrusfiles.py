#!/usr/bin/env python3

import curses
import os


def draw_box(stdscr, y, x, height, width):

    for i in range(width):
        stdscr.addch(
            y,
            x+i,
            "-"
        )

        stdscr.addch(
            y+height-1,
            x+i,
            "-"
        )

    for i in range(height):
        stdscr.addch(
            y+i,
            x,
            "|"
        )

        stdscr.addch(
            y+i,
            x+width-1,
            "|"
        )


def main(stdscr):

    os.system("stty -ixon")

    curses.curs_set(0)

    current = os.getcwd()

    selected = 0


    while True:

        stdscr.clear()

        height, width = stdscr.getmaxyx()


        files = [
            ".."
        ]


        try:

            files += sorted(
                os.listdir(current)
            )

        except:

            files += [
                "Permission denied"
            ]


        # Header

        draw_box(
            stdscr,
            0,
            0,
            height-1,
            width-1
        )


        stdscr.addstr(
            1,
            3,
            "🍋 Citrus Files"
        )


        stdscr.addstr(
            2,
            3,
            current[:width-6]
        )


        # File list

        for i, file in enumerate(files):

            if i+4 >= height-3:
                break


            if i == selected:

                stdscr.attron(
                    curses.A_REVERSE
                )


            path = os.path.join(
                current,
                file
            )


            if os.path.isdir(path):

                display = "[DIR] " + file

            else:

                display = "      " + file


            stdscr.addstr(
                i+4,
                3,
                display[:width-6]
            )


            if i == selected:

                stdscr.attroff(
                    curses.A_REVERSE
                )


        # Footer

        stdscr.addstr(
            height-2,
            3,
            "↑↓ Move  ENTER Open  BACKSPACE Back  Q Quit"
        )


        stdscr.refresh()


        key = stdscr.getch()


        if key in (
            ord("q"),
            ord("Q")
        ):

            break


        elif key == curses.KEY_UP:

            selected = max(
                0,
                selected-1
            )


        elif key == curses.KEY_DOWN:

            selected = min(
                len(files)-1,
                selected+1
            )


        elif key in (
            10,
            13
        ):

            chosen = files[selected]

            path = os.path.join(
                current,
                chosen
            )


            if os.path.isdir(path):

                current = os.path.abspath(path)

                selected = 0


        elif key in (
            curses.KEY_BACKSPACE,
            127
        ):

            current = os.path.dirname(
                current
            )

            selected = 0



    os.system("stty ixon")



if __name__ == "__main__":

    curses.wrapper(main)
