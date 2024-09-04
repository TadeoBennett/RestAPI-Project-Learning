import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

# Getting all stores
@app.get("/store") #http://127.0.0.1:5000/store
def getStores():
    #change the data saved for stores into a list so it can be returned as json
    return {"stores": list(stores.values())} 


# Inserting a new store
@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex()
    # **store_data unpacks the data in store_data and uses it to create the new_store
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


# Inserting an item to a store
# Expecting the data in a json payload
@app.post("/item")   #adding a single item using parameters in url
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404
    
    item_id = uuid.uuid4.hex()
    item = {**item_data, "id": item_id} #similar to when we created a store
    items[item_id] = item

    return item, 201



# Getting the details of a store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


#Getting the items for a store
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404


















