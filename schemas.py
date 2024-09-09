from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)
    price = fields.Float(required = True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    # name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    

class ItemSchema(PlainItemSchema):    # extends the PlainItemSchema
    store_id = fields.Int(required=True, load_only=True)   #able to pass in the store id for an item, from a client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)   #used when returning data to the client
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    # store_id = fields.Int()


class StoreSchema(PlainStoreSchema):    # extends the PlainItemSchema
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)



class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

















