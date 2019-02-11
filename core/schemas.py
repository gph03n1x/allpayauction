from marshmallow import Schema, fields
import uuid


class BidderSchema(Schema):
    budget = fields.Float()
    name = fields.String(missing=lambda: str(uuid.uuid4()))
    raise_step = fields.Float(load_from='raises', missing=1.0)


class ExperimentSchema(Schema):
    bidders = fields.Nested(BidderSchema, many=True)
    name = fields.String(missing=lambda: str(uuid.uuid4()))
    values = fields.List(fields.Float())
