import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


# Get all stores ----------------------------
@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    #change the data saved for stores into a list so it can be returned as json
    return {"stores": list(stores.values())} 


# Get a store's details --------------
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message = "store not found")


# Create a new store ---------------
@app.post("/store")
def create_store():
    store_data = request.get_json()
    #check if the name value was provided
    if(
        "name" not in store_data or store_data["name"] == ""
    ):
        abort(400, message="Bad Request. Ensure 'name' is included in the JSON payload and a value is set.")
    store_id = uuid.uuid4().hex
    # **store_data unpacks the data in store_data and uses it to create the new_store
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201



 
#Get all Items ----------------------------
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


# Get an item ----------------------------
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(201, message = "store not found")



# Create an item for a store ---------------------------
# Expecting the data in a json payload
@app.post("/item")   #adding a single item using parameters in url
def create_item():
    item_data = request.get_json()
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
        ):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included int the json payload.")
    #checking for no repeated items
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists")
    #check if the store exists 
    if item_data["store_id"] not in stores:
        abort(404, message = "store not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id} #similar to when we created a store
    items[item_id] = item

    return item, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "store deleted"}
    except KeyError:
        abort(404, message="store Not Found")




@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item Not Found")



@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad Request. Ensure 'price', and 'name' are included in teh JSON payload.")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found.")













