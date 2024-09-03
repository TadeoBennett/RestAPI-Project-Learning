from flask import Flask, request


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
    return {"stores": stores}


# Inserting a new store
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


# Inserting an item to a store
@app.post("/store/<string:name>/item")   #adding a single item using parameters in url
def create_item(name):
    request_data = request.get_json()
    for store in stores:             #loop the list of saved stores
        if store["name"] == name:    #match name of store with the saved list
            #create the item if the store exists 
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201  #client receives the new item as json
    return {"message": "Store not found"}, 404


# Getting the details of a store
@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:             #loop the list of saved stores
        if store["name"] == name:   
            return store, 201
    return {"message": "Store not found"}, 404


#Getting the items for a store
@app.get("/store/<string:name>/items")
def get_store_items(name):
    for store in stores:             #loop the list of saved stores
        if store["name"] == name:   
            return {"items": store["items"]},201
    return {"message": "Store not found"}, 404




















