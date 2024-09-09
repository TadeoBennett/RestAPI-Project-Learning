
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
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

    @jwt_required() 
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):             #if the user is not an admin
            abort(401, message="Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item deleted"}


    @jwt_required() 
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
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all() #returns a list of items
        
    @jwt_required(fresh=True) #require that an access token be provided in the header. Note: Authorization: Bearer <access_token>
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