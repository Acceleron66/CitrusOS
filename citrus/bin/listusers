#!/usr/bin/env python3

import getpass
import grp
import os
import pwd
import subprocess

HEADER = """
==========================================
      CitrusOS Guillotine
         User Manager
==========================================
"""


def clear():
    os.system("clear")


def pause():
    input("\nPress Enter to continue...")


def sudo_members():
    try:
        return grp.getgrnam("sudo").gr_mem
    except KeyError:
        return []
