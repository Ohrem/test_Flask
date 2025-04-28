from marshmallow import Schema, fields
from marshmallow.validate import Length

class CreateToastSchema(Schema):
    text = fields.String(required=True, validate=Length(min=1, max=255))
    user_id = fields.Integer(required=False, allow_none=True)


class MarkReadToastSchema(Schema):
    id = fields.List(fields.Integer(required=True), required=True)


class GetUserToastSchema(Schema):
    user_id = fields.Integer(required=True)


class ToastResponseSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    user_id = fields.Integer(allow_none=True)
    is_read = fields.Boolean()
    created_at = fields.DateTime()