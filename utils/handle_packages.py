import os

import json
import uuid

from utils.folder import MAIN_FOLDER

# Open and read the JSON file
PACKAGE_FILE_PATH=os.path.join(MAIN_FOLDER,"data","packages","packages.json")
def read_packages():
    with open(PACKAGE_FILE_PATH, 'r') as file:
        data = json.load(file)
    return data

def write_packages(data):
    with open(PACKAGE_FILE_PATH, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return read_packages()

# def get_packages_by_user(username:str):
#     all_package_data=read_packages()
#     for data in all_package_data:
#         if data.get("username")==username:
#             return data.get("packages")
#     else:
#         return []
def check_package_id_valid(package_id):
    packages=read_packages()
    for i in packages:
        if i.get("package_id")==package_id:
            return True
    else:
        return False

def get_package_by_id(package_id):
    packages=read_packages()
    for i in packages:
        if i.get("package_id")==package_id:
            return i
    else:
        return False

def create_package_name(username:str,package_name:str):
    package_uuid=uuid.uuid4()
    return f"package_{package_name}_{package_uuid}"

def add_package(username:str,package_name:str):
    all_package_data:list=read_packages()
    """
    [
    {
        "package_name": "",
        "package_id": "",
        "card_ids": []
    }
    ]   
    """
    package_id=create_package_name(username,package_name)
    package_data={
        "package_name": package_name,
        "package_id": package_id,
        "card_ids": []
    }
    all_package_data.append(package_data)
    packages=write_packages(all_package_data)
    return package_data


def add_card_to_package(package_id:str,card_id:str):
    package_data=get_package_by_id(package_id)
    all_package_data:list=read_packages()
    package_data.get("card_ids").append(card_id)
    

    all_package_data.append(package_data)
    packages=write_packages(all_package_data)
    return package_data
