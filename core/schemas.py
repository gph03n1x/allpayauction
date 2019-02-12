from marshmallow import Schema, fields, post_load
import uuid


class BidderSchema(Schema):
    budget = fields.Float()
    name = fields.String(missing=lambda: str(uuid.uuid4()))
    raise_step = fields.Float(load_from='raises', missing=1.0)
    item_values = fields.List(fields.Float(), required=False)

    @post_load
    def load_item_values(self, data):
        return data


class BiddersSchema(Schema):
    bidders = fields.Nested(BidderSchema, many=True)


class AuctionSchema(Schema):
    name = fields.String(missing=lambda: str(uuid.uuid4()))
    global_item_values = fields.List(
        fields.Float(), required=False, missing=[], load_from='values'
    )
