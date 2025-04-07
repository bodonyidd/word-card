from pymongo.mongo_client import MongoClient
import urllib
from pymongo.database import Database
from pymongo.collection import Collection

from bson.objectid import ObjectId

db_username = "morzsadb"
db_password = "Cicaboy111@"

uri = rf"mongodb+srv://{db_username}:{urllib.parse.quote_plus(db_password)}@cluster0.vaq5p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


class MorzsaDB:
    def __init__(self):
        self.client = MongoClient(uri)

    def get_db(self) -> Database:
        return self.client["morzsa_word_cards"]

    # Send a ping to confirm a successful connection
    def test_connection(self) -> None:
        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    @property
    def collection(self) -> dict:
        return {
            "users": lambda: self.get_users_collection(),
            "cards": lambda: self.get_cards_collection(),
            "packages": lambda: self.get_packages_collection(),
        }

    def get_client(self) -> MongoClient:
        return self.client

    def get_collection_by_name(self, collection_name: str) -> Collection:
        collection_name = collection_name.lower()
        return self.collection.get(collection_name)()

    def get_users_collection(self):
        return self.get_db()["users"]

    def get_packages_collection(self):
        return self.get_db()["packages"]

    def get_cards_collection(self):
        return self.get_db()["cards"]

    def get_data_by_property(
        self, collection_name: str, property_value: str, property_name: str = "_id"
    ):
        collection = self.get_collection_by_name(collection_name)
        if property_name=="_id" and isinstance(property_value,str):
            property_value = ObjectId(property_value)
        try:
            result: list = collection.find_one(
                {f"{property_name}": property_value}
            ).to_list()
        except AttributeError:
            result: list = collection.find_one({f"{property_name}": property_value})

        return result

    def add_data_to_given_collection(self, collection_name: str, data: dict):
        collection = self.get_collection_by_name(collection_name)
        result: list = collection.insert_one(data)
        # InsertOneResult(ObjectId('672f9aaba3496641e190d813'), acknowledged=True)
        return result


if __name__ == "__main__":
    print(MorzsaDB().get_users_collection())
