#!/usr/bin/env python3

import curses
import os


def save_file(filename, lines):
    with open(filename, "w") as f:
        f.write("\n".join(lines))


def editor(stdscr):

    os.system("stty -ixon")

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(
        1,
        curses.COLOR_BLACK,
        curses.COLOR_CYAN
    )

    curses.init_pair(
        2,
        curses.COLOR_WHITE,
        curses.COLOR_BLUE
    )

    curses.curs_set(1)

    height, width = stdscr.getmaxyx()

    lines = [""]
    filename = None

    x = 0
    y = 0


    while True:

        stdscr.clear()


        # Top menu
        stdscr.attron(
            curses.color_pair(1)
        )

        stdscr.addstr(
            0,
            0,
            " 🍋 Citrus Edit  |  File   Edit   Help "
        )

        stdscr.addstr(
            0,
            len(" 🍋 Citrus Edit  |  File   Edit   Help "),
            " " * (width-40)
        )

        stdscr.attroff(
            curses.color_pair(1)
        )


        # Text area

        for i, line in enumerate(lines):

            if i+2 < height-2:

                stdscr.addstr(
                    i+2,
                    1,
                    line
                )


        # Status bar

        stdscr.attron(
            curses.color_pair(2)
        )

        status = (
            f" Ctrl+S Save | Ctrl+Q Quit | "
            f"Line {y+1}"
        )

        stdscr.addstr(
            height-1,
            0,
            status
        )

        stdscr.attroff(
            curses.color_pair(2)
        )


        stdscr.move(
            y+2,
            x+1
        )

        stdscr.refresh()


        key = stdscr.getch()


        # Quit

        if key == 17:

            stdscr.clear()

            stdscr.addstr(
                5,
                5,
                "Save before exiting? (y/n)"
            )

            stdscr.refresh()

            answer = stdscr.getch()


            if answer in (ord("y"), ord("Y")):

                if filename is None:

                    curses.echo()

                    stdscr.addstr(
                        7,
                        5,
                        "Filename: "
                    )

                    filename = stdscr.getstr(
                        7,
                        15
                    ).decode()

                    curses.noecho()


                save_file(
                    filename,
                    lines
                )


            os.system("stty ixon")
            break


        # Save

        elif key == 19:

            curses.echo()

            stdscr.addstr(
                height-3,
                5,
                "Save as: "
            )

            filename = stdscr.getstr(
                height-3,
                15
            ).decode()

            curses.noecho()


            save_file(
                filename,
                lines
            )


        # Enter

        elif key in (10,13):

            lines.insert(
                y+1,
                ""
            )

            y += 1
            x = 0


        # Backspace

        elif key in (
            curses.KEY_BACKSPACE,
            127
        ):

            if x > 0:

                lines[y] = (
                    lines[y][:x-1]
                    +
                    lines[y][x:]
                )

                x -= 1


        # Arrow keys

        elif key == curses.KEY_UP:

            y=max(
                0,
                y-1
            )

            x=min(
                x,
                len(lines[y])
            )


        elif key == curses.KEY_DOWN:

            y=min(
                len(lines)-1,
                y+1
            )

            x=min(
                x,
                len(lines[y])
            )


        elif key == curses.KEY_LEFT:

            x=max(
                0,
                x-1
            )


        elif key == curses.KEY_RIGHT:

            x=min(
                len(lines[y]),
                x+1
            )


        # Normal typing

        elif 32 <= key <= 126:

            lines[y] = (
                lines[y][:x]
                +
                chr(key)
                +
                lines[y][x:]
            )

            x += 1



if __name__ == "__main__":

    curses.wrapper(editor)
