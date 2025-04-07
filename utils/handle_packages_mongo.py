from utils.handle_mongo import MorzsaDB
from bson.objectid import ObjectId


class Package_Management:
    def __init__(self):
        self.mongo = MorzsaDB()
        self.collection_name = "packages"

    def get_package_by_id(self, package_id: str):
        if isinstance(package_id, str):
            package_id = ObjectId(package_id)
        result = self.mongo.get_packages_collection().find_one({"_id": package_id})
        return result

    def add_package(self, package_name: str, author_id: str):
        if isinstance(author_id, str):
            author_id = ObjectId(author_id)
        data = {"package_name": package_name, "author_id": author_id}
        result = self.mongo.add_data_to_given_collection(
            collection_name=self.collection_name, data=data
        )
        search_result = self.get_package_by_id(result.inserted_id)
        return search_result

    def get_packages_by_author(self, author_id):
        if isinstance(author_id, str):
            author_id = ObjectId(author_id)
        return (
            self.mongo.get_packages_collection()
            .find({"author_id": author_id})
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
