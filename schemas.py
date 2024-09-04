from marshmallow import Scheme, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required=True)
    price = fields.Float(required = True)
    store_id = fields.Str(required=True)



class ItemUdpateSchema(Schema):
    name = fields.Str()
    price = fields.Str()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    names = fields.Str(dump_only=True)























