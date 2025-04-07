from typing import Dict, Union
from utils.handle_mongo import MorzsaDB


class User_Management:
    def __init__(self):
        self.mongo = MorzsaDB()
        self.collection_name = "users"

    def check_user_exists(self, property_value: str, property_name: str = "user_name"):
        user_data: Union[Dict, None] = self.mongo.get_data_by_property(
            collection_name=self.collection_name,
            property_name=property_name,
            property_value=property_value,
        )
        if user_data is None:
            return False  # user does not exist
        return user_data  # user exists

    def add_user(self, name: str, password: str):
        data = {"user_name": name, "password": password}
        if (
            self.check_user_exists(property_name="user_name", property_value=name)
            is not False
        ):
            raise ValueError("User is already exist")
        result = self.mongo.add_data_to_given_collection(
            collection_name=self.collection_name, data=data
        )
        search_result = self.mongo.get_data_by_property(
            collection_name=self.collection_name, property_value=result.inserted_id
        )
        return search_result
