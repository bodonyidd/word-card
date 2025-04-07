import os

import json
from utils.folder import MAIN_FOLDER

# Open and read the JSON file
from utils.handle_packages import read_packages

USER_FILE_PATH = os.path.join(MAIN_FOLDER, "data", "users", "users.json")


def read_users():
    with open(USER_FILE_PATH, "r") as file:
        data = json.load(file)
    return data


def write_users(data):
    with open(USER_FILE_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)


def get_registered_users():
    all_user_data = read_users()
    usernames = []
    for user in all_user_data:
        usernames.append(user.get("name"))
    return usernames


def get_user_data_by_username(username: str):
    users = read_users()
    for i in users:
        if i.get("name") == username:
            return i


def get_user_package_ids(username: str):
    user_data = get_user_data_by_username(username)
    package_ids = user_data.get("package_ids")
    return package_ids


def update_user_packages(username: str, key_to_update: str, value: str):
    users = read_users()
    for i in users:
        if i.get("name") == username:
            i[key_to_update].append(value)
    write_users(users)
    return read_users()


def get_user_packages_data(username: str):
    package_ids = get_user_package_ids(username)

    packages = read_packages()
    user_packages = []
    for i in package_ids:
        for j in packages:
            if i == j.get("package_id"):
                user_packages.append(j)
    return user_packages


def add_package_to_user(username: str, package_id: str):
    package_ids = get_user_package_ids(username)
    package_ids.append(package_id)


def add_user(username: str):
    all_user_data: list = read_users()
    all_user_data.append({"name": f"{username}", "secret": "", "package_ids": []})
    write_users(all_user_data)
    return True if username in get_registered_users() else False
