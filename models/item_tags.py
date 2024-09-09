from db import db

class ItemsTags(db.Model):
    __table__name = "items_tags"
    id = db.Column(db.Integer, primary_key=True)
    #two foreign key columns
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))