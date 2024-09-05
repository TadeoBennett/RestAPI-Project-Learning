import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")



@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # Get an item ----------------------------
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented")


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id): # the validated json (item_data) goes infront of every other parameter
        item = ItemModel.query.get(item_id)
        
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
    
    

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
        item = ItemModel(**item_data) #turn the dictionary into keyword arguments
        try:
            db.session.add(item) #put in place where its not written to db file 
            db.session.commit() #write to database file
            
        except IntegrityError:
            abort(500, message="Error while atttempting to insert duplicate item")
        except SQLAlchemyError:
            abort(500, message="An error occured whille inserting the item")
            
        return item, 201