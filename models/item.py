from db import db

class ItemModel(db.Model):  #mapping of row in a toble to a python class
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)   #set to autoincrement
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    
    #gives us the associated object with that foreign key on each.
    #backpopulates on the store model so we can get the items list that are associated with each store
    store = db.relationship("StoreModel", back_populates="items")
    
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

    #NOTE: SQLite does not enforce foreign key constraint


