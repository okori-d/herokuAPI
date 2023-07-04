#!/home/okori/pythonproject/unicart_env/bin/python

import requests
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# Connect to the MongoDB cluster
client = MongoClient("mongodb+srv://okoride0:lindahst1@database1.a17zh8w.mongodb.net/?retryWrites=true&w=majority")

# Access the first MongoDB database
db1 = client["database1"]

# Access the second MongoDB database
db2 = client["scraped_data"]

# Collection names
collection1_name = "jijiProducts"  # Collection for jiji products
collection2_name = "products"  # Collection for jumia products


# Routes

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the API!"})

@app.route("/external", methods=["GET"])
def access_external():
    try:
        response = requests.get("https://instagram.com")
        # Process the response as needed
        return response.text  # Return the response content
    except requests.exceptions.RequestException as e:
        # Handle request exception
        return str(e)


@app.route("/all", methods=["GET"])
def get_all_items():
    try:
        # Get all items from both collections
        collection1 = db1[collection1_name]
        collection2 = db2[collection2_name]

        # Projection documents to show what is included and what isn't
        collection1_data = [document for document in collection1.find({}, {"_id": 0, "Image": 1, "Item Name": 1, "Price": 1})]
        collection2_data = [document for document in collection2.find({}, {"_id": 0, "images": 1, "name": 1, "price": 1, "rating": 1})]

        result = {
            "collection1": collection1_data,
            "collection2": collection2_data
        }

        return jsonify(result)
    except PyMongoError:
        # Handle the session error or any other PyMongoError
        return jsonify({"error": "An error occurred with the database session."})
    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": str(e)})




@app.route("/item/<collection>/<item_id>", methods=["GET"])
def get_item(collection, item_id):
    # Retrieve item details from the specified collection and item_id
    if collection == "collection1":
        collection_name = collection1_name
        database = db1
    elif collection == "collection2":
        collection_name = collection2_name
        database = db2
    else:
        return jsonify({"error": "Invalid collection"})

    selected_collection = database[collection_name]
    item = selected_collection.find_one({"_id": item_id})

    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"})


if __name__ == "__main__":
    app.run(debug=True)
