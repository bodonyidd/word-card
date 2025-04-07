import os

import json
import uuid
from utils.folder import MAIN_FOLDER

# Open and read the JSON file
CARDS_FILE_PATH = os.path.join(MAIN_FOLDER, "data", "cards", "cards.json")


def create_card_id():
    package_uuid = uuid.uuid4()
    return f"card_{package_uuid}"


def read_cards():
    with open(CARDS_FILE_PATH, "r") as file:
        data = json.load(file)
    return data


def add_card(input_data, package_id):
    # NOTE: Handle if cards.json does not exist, or empty
    input_data["package_id"] = package_id
    input_data["card_id"] = create_card_id()
    saved_card_data = read_cards()
    saved_card_data.append(input_data)
    with open(CARDS_FILE_PATH, "w") as json_file:
        json.dump(saved_card_data, json_file, indent=4)
    return input_data


# def get_user_packages(username:str):
#     users=read_users()
#     package_ids=[]
#     for i in users:
#         if i.get("name")==username:
#             package_ids=i.get("package_ids")

#     from handle_packages import read_packages
#     packages=read_packages()
#     user_packages=[]
#     for i in package_ids:
#         for j in packages:
#             if i==j.get("package_id"):
#                 user_packages.append(j)
#     return user_packages
