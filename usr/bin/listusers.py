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


def list_users():

    admins = sudo_members()

    print()

    for user in pwd.getpwall():

        if user.pw_uid >= 1000 or user.pw_name == "root":

            role = "Administrator" if (
                user.pw_name in admins or user.pw_name == "root"
            ) else "Standard User"

            print(f"{user.pw_name:<18} {role}")



def create_user():

    username = input("New username: ").strip()

    if not username:
        print("Invalid username.")
        return

    try:

        subprocess.run(
            ["sudo", "useradd", "-m", "-s", "/bin/bash", username],
            check=True
        )

        subprocess.run(
            ["sudo", "passwd", username],
            check=True
        )

        print(f"\n🍋 User '{username}' created.")

    except subprocess.CalledProcessError:
        print("Failed to create user.")


def delete_user():

    username = input("Delete user: ").strip()

    if username == getpass.getuser():

        print("\nYou cannot delete the account you are using.")
        return

    confirm = input(
        f"Delete '{username}' and home directory? (y/N): "
    ).lower()

    if confirm != "y":
        print("Cancelled.")
        return

    try:

        subprocess.run(
            ["sudo", "userdel", "-r", username],
            check=True
        )

        print("User removed.")

    except subprocess.CalledProcessError:
        print("Unable to delete user.")


def change_password():

    username = input("Username: ").strip()

    try:

        subprocess.run(
            ["sudo", "passwd", username],
            check=True
        )

    except subprocess.CalledProcessError:
        print("Unable to change password.")


def user_info():

    username = input("Username: ").strip()

    try:

        subprocess.run(["id", username])

    except Exception:
        print("User not found.")


def toggle_admin():

    username = input("Username: ").strip()

    current = getpass.getuser()

    if username == current:

        print("\nYou cannot change your own administrator privileges.")
        return

    admins = sudo_members()

    try:

        if username in admins:

            confirm = input(
                f"Remove administrator privileges from {username}? (y/N): "
            ).lower()

            if confirm != "y":
                return

            subprocess.run(
                ["sudo", "gpasswd", "-d", username, "sudo"],
                check=True
            )

            print(f"\n🍋 {username} is now a Standard User.")

        else:

            confirm = input(
                f"Grant administrator privileges to {username}? (y/N): "
            ).lower()

            if confirm != "y":
                return

            subprocess.run(
                ["sudo", "usermod", "-aG", "sudo", username],
                check=True
            )

            print(f"\n🍋 {username} is now an Administrator.")

    except subprocess.CalledProcessError:
        print("Operation failed.")


while True:

    clear()

    print(HEADER)

    print("1) List Users")
    print("2) Create User")
    print("3) Delete User")
    print("4) Change Password")
    print("5) User Information")
    print("6) Toggle Administrator")
    print("7) Exit")

    choice = input("\nChoice: ")

    if choice == "1":
        list_users()
        pause()

    elif choice == "2":
        create_user()
        pause()

    elif choice == "3":
        delete_user()
        pause()

    elif choice == "4":
        change_password()
        pause()

    elif choice == "5":
        user_info()
        pause()

    elif choice == "6":
        toggle_admin()
        pause()

    elif choice == "7":
        break

    else:
        print("Invalid choice.")
        pause()
