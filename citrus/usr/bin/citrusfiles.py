#!/usr/bin/env python3

import curses
import os
import shutil
import subprocess


class CitrusFiles:

    def __init__(self, screen):

        self.screen = screen

        # Current directory
        self.path = os.path.expanduser("~")


        # Navigation history
        self.back_history = []
        self.forward_history = []


        # File list
        self.files = []

        self.cursor = 0
        self.offset = 0


        # Which panel is active
        # 0 = sidebar
        # 1 = files
        self.focus = 1


        # Sidebar items
        self.sidebar = [
            ("🏠 Home", os.path.expanduser("~")),
            ("💻 File System", "/"),
            ("📁 Documents", os.path.expanduser("~/Documents")),
            ("📁 Projects", os.path.expanduser("~/Projects"))
        ]

        self.sidebar_cursor = 0


        # Setup terminal
        curses.curs_set(0)

        self.setup_colours()

        self.load_files()



    def setup_colours(self):

        curses.start_color()

        curses.use_default_colors()


        # Green terminal style
        curses.init_pair(
            1,
            curses.COLOR_GREEN,
            -1
        )


        # Selected item
        curses.init_pair(
            2,
            curses.COLOR_BLACK,
            curses.COLOR_GREEN
        )


        # Border
        curses.init_pair(
            3,
            curses.COLOR_GREEN,
            -1
        )


        self.normal = curses.color_pair(1)

        self.selected = curses.color_pair(2)

        self.border = curses.color_pair(3)



    def load_files(self):

        try:

            self.files = sorted(
                os.listdir(self.path),
                key=lambda item:
                    (
                        not os.path.isdir(
                            os.path.join(
                                self.path,
                                item
                            )
                        ),
                        item.lower()
                    )
            )


        except PermissionError:

            self.files = []


        # Add parent directory
        self.files.insert(
            0,
            ".."
        )


        self.cursor = 0
        self.offset = 0



    def change_directory(self, location):

        if os.path.isdir(location):

            self.back_history.append(
                self.path
            )

            self.forward_history.clear()


            self.path = location

            self.load_files()



    def draw_border(self):

        height, width = self.screen.getmaxyx()


        self.screen.attron(
            self.border
        )


        self.screen.border()


        self.screen.attroff(
            self.border
        )


        # Title

        self.screen.addstr(
            0,
            3,
            "🍋 Citrus Files",
            self.border
        )


        # Divider

        divider = 20


        for y in range(1, height-1):

            self.screen.addch(
                y,
                divider,
                curses.ACS_VLINE,
                self.border
            )



    def draw_sidebar(self):

        self.screen.addstr(
            2,
            2,
            "Places",
            self.normal
        )


        for index, item in enumerate(self.sidebar):

            name, location = item


            if index == self.sidebar_cursor and self.focus == 0:

                self.screen.addstr(
                    index + 4,
                    2,
                    name,
                    self.selected
                )

            else:

                self.screen.addstr(
                    index + 4,
                    2,
                    name,
                    self.normal
                )
    def draw_files(self):

        height, width = self.screen.getmaxyx()

        sidebar_width = 20


        # Current location

        self.screen.addstr(
            2,
            sidebar_width + 3,
            self.path[:width-sidebar_width-5],
            self.normal
        )


        view_height = height - 6


        visible = self.files[
            self.offset:
            self.offset + view_height
        ]


        for index, filename in enumerate(visible):

            real_index = index + self.offset


            full_path = os.path.join(
                self.path,
                filename
            )


            if filename == "..":

                icon = "⬆"

            elif os.path.isdir(full_path):

                icon = "📁"

            else:

                icon = "📄"


            text = f"{icon} {filename}"


            if (
                real_index == self.cursor
                and self.focus == 1
            ):

                self.screen.addstr(
                    index + 4,
                    sidebar_width + 3,
                    text[:width-sidebar_width-5],
                    self.selected
                )

            else:

                self.screen.addstr(
                    index + 4,
                    sidebar_width + 3,
                    text[:width-sidebar_width-5],
                    self.normal
                )



    def draw_footer(self):

        height, width = self.screen.getmaxyx()


        message = (
            "TAB Switch | ↑↓ Move | ←→ History | "
            "ENTER Open | C CD | M Move | N New | D Delete | Q Quit"
        )


        self.screen.addstr(
            height-2,
            2,
            message[:width-4],
            self.normal
        )



    def draw(self):

        self.screen.clear()


        self.draw_border()

        self.draw_sidebar()

        self.draw_files()

        self.draw_footer()


        self.screen.refresh()



    def move_file_cursor(self, amount):

        if not self.files:
            return


        self.cursor += amount


        if self.cursor < 0:

            self.cursor = len(self.files)-1


        if self.cursor >= len(self.files):

            self.cursor = 0



        height = self.screen.getmaxyx()[0]

        view_height = height - 6


        if self.cursor < self.offset:

            self.offset = self.cursor


        elif self.cursor >= self.offset + view_height:

            self.offset = (
                self.cursor -
                view_height +
                1
            )



    def move_sidebar_cursor(self, amount):

        self.sidebar_cursor += amount


        if self.sidebar_cursor < 0:

            self.sidebar_cursor = len(self.sidebar)-1


        if self.sidebar_cursor >= len(self.sidebar):

            self.sidebar_cursor = 0



    def open_sidebar_location(self):

        name, location = self.sidebar[
            self.sidebar_cursor
        ]


        if os.path.isdir(location):

            self.back_history.append(
                self.path
            )

            self.forward_history.clear()

            self.path = location

            self.load_files()



    def go_back(self):

        if self.back_history:

            self.forward_history.append(
                self.path
            )


            self.path = (
                self.back_history.pop()
            )


            self.load_files()



    def go_forward(self):

        if self.forward_history:

            self.back_history.append(
                self.path
            )


            self.path = (
                self.forward_history.pop()
            )


            self.load_files()



    def toggle_focus(self):

        if self.focus == 0:

            self.focus = 1

        else:

            self.focus = 0
    def open_selected(self):

        if not self.files:
            return


        selected = self.files[self.cursor]


        # Parent directory

        if selected == "..":

            parent = os.path.dirname(
                self.path
            )

            if parent:

                self.change_directory(
                    parent
                )

            return



        full_path = os.path.join(
            self.path,
            selected
        )


        # Open directory

        if os.path.isdir(full_path):

            self.change_directory(
                full_path
            )

            return



        # Open files

        extensions = [

            ".txt",
            ".py",
            ".c",
            ".cpp",
            ".js",
            ".html",
            ".css",
            ".sh",
            ".json"
        ]


        if selected.endswith(
            tuple(extensions)
        ):

            curses.endwin()

            subprocess.call(
                [
                    "nano",
                    full_path
                ]
            )

            self.screen.refresh()

            return



        # Run executable files

        if os.access(
            full_path,
            os.X_OK
        ):

            curses.endwin()

            subprocess.call(
                [
                    full_path
                ]
            )

            input(
                "\nPress ENTER to return..."
            )

            self.screen.refresh()



    def cd_command(self):

        height, width = self.screen.getmaxyx()


        curses.echo()


        self.screen.addstr(
            height-3,
            2,
            "CD path: ",
            self.normal
        )


        location = self.screen.getstr(
            height-3,
            11
        ).decode()


        curses.noecho()


        if os.path.isdir(location):

            self.change_directory(
                os.path.abspath(location)
            )



    def move_selected(self):

        if not self.files:
            return


        selected = self.files[
            self.cursor
        ]


        if selected == "..":

            return


        source = os.path.join(
            self.path,
            selected
        )


        height, width = self.screen.getmaxyx()


        curses.echo()


        self.screen.addstr(
            height-3,
            2,
            "Move to: ",
            self.normal
        )


        destination = self.screen.getstr(
            height-3,
            11
        ).decode()


        curses.noecho()



        if os.path.isdir(destination):

            shutil.move(
                source,
                destination
            )


            self.load_files()



    def new_folder(self):

        height, width = self.screen.getmaxyx()


        curses.echo()


        self.screen.addstr(
            height-3,
            2,
            "Folder name: ",
            self.normal
        )


        name = self.screen.getstr(
            height-3,
            15
        ).decode()


        curses.noecho()


        if name:

            os.mkdir(
                os.path.join(
                    self.path,
                    name
                )
            )


        self.load_files()



    def delete_selected(self):

        if not self.files:
            return


        selected = self.files[
            self.cursor
        ]


        if selected == "..":

            return


        target = os.path.join(
            self.path,
            selected
        )


        if os.path.isdir(target):

            shutil.rmtree(
                target
            )

        else:

            os.remove(
                target
            )


        self.load_files()
    def run(self):

        while True:

            self.draw()

            key = self.screen.getch()



            # TAB switches panels

            if key == 9:

                self.toggle_focus()



            # QUIT

            elif key in (
                ord("q"),
                ord("Q")
            ):

                break



            # Sidebar controls

            elif self.focus == 0:


                if key == curses.KEY_UP:

                    self.move_sidebar_cursor(
                        -1
                    )


                elif key == curses.KEY_DOWN:

                    self.move_sidebar_cursor(
                        1
                    )


                elif key in (
                    10,
                    curses.KEY_ENTER
                ):

                    self.open_sidebar_location()



            # File panel controls

            else:


                if key == curses.KEY_UP:

                    self.move_file_cursor(
                        -1
                    )


                elif key == curses.KEY_DOWN:

                    self.move_file_cursor(
                        1
                    )


                elif key == curses.KEY_LEFT:

                    self.go_back()



                elif key == curses.KEY_RIGHT:

                    self.go_forward()



                elif key in (
                    10,
                    curses.KEY_ENTER
                ):

                    self.open_selected()



                elif key == 127:

                    parent = os.path.dirname(
                        self.path
                    )

                    if parent:

                        self.change_directory(
                            parent
                        )



                elif key in (
                    ord("c"),
                    ord("C")
                ):

                    self.cd_command()



                elif key in (
                    ord("m"),
                    ord("M")
                ):

                    self.move_selected()



                elif key in (
                    ord("n"),
                    ord("N")
                ):

                    self.new_folder()



                elif key in (
                    ord("d"),
                    ord("D")
                ):

                    self.delete_selected()




def main(screen):

    app = CitrusFiles(screen)

    app.run()



if __name__ == "__main__":

    curses.wrapper(main)
