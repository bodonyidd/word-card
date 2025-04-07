from typing import Union
from utils.handle_mongo import MorzsaDB
from bson.objectid import ObjectId


class Card_Management:
    def __init__(self):
        self.mongo = MorzsaDB()
        self.collection_name = "cards"

    def add_card(
        self,
        author_id: Union[ObjectId, str],
        package_id: Union[ObjectId, str],
        front: str,
        back: str,
        front_info: str = None,
        back_info: str = None,
    ):
        if isinstance(author_id, str):
            author_id = ObjectId(author_id)
        if isinstance(package_id, str):
            package_id = ObjectId(package_id)

        data = {
            "author_id": author_id,
            "package_id": package_id,
            "front": front,
            "back": back,
            "front_info": front_info,
            "back_info": back_info,
        }
        result = self.mongo.add_data_to_given_collection(
            collection_name=self.collection_name, data=data
        )
        search_result = self.mongo.get_data_by_property(
            collection_name=self.collection_name, property_value=result.inserted_id
        )
        return search_result

    def get_cards_by_package_id(self, package_id):
        if isinstance(package_id, str):
            package_id = ObjectId(package_id)
        return (
            self.mongo.get_cards_collection()
            .find({"package_id": package_id})
            .to_list()
        )
        # [] or

        # [{
        # '_id': ObjectId('671958c30c135dc10f2e51d4'),
        # 'package_name': 'my_package',
        #  'author': ObjectId('6719584a0c135dc10f2e51d3')
        # }]

    def get_package_by_name(self, package_name: str):
        return (
            self.mongo.get_packages_collection()
            .find({"package_name": package_name})
            .to_list()
        )
