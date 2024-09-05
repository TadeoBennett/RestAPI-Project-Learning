from db import db

class ItemModel(db.Model):  #mapping of row in a toble to a python class
    __tablename = "items"

    id = db.Column(db.Integer, primary_key=True)   #set to autoincrement
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")




