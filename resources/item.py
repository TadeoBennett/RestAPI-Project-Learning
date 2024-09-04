import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema
from schemas import ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")



@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # Get an item ----------------------------
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message = "store not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item Not Found")


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id): # the validated json (item_data) goes infront of every other parameter
        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     abort(400, message="Bad Request. Ensure 'price', and 'name' are included in teh JSON payload.")

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    #Get all Items ----------------------------
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values() #returns a list of items and not an object of items

    # Create an item for a store ---------------------------
    # Expecting the data in a json payload
    @blp.arguments(ItemSchema)  #the json data is checked here and returns the validated dictionary
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json()   #due to to the validation with marshmallow(ItemSchema), this is not necessary

        #----checking of necessary values is done through marshmallow

        #checking for no repeated items
        for item in items.values():
            if(
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id} #similar to when we created a store
        items[item_id] = item

        return item, 201




