from marshmallow import Schema, fields

class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    url_img = fields.Str()
    description = fields.Str()
    price = fields.Float(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class LevelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ProductSchema(PlainProductSchema):
    user_id = fields.Int(required=True)
    user = fields.Nested(UserSchema, dump_only=True, many=True)

class ProductsUserSchema(Schema):
    products = fields.Nested(ProductSchema, dump_only=True, many=True)
    users = fields.Nested(UserSchema, dump_only=True, many=True)

class RevokedJWTSchema(Schema):
    id = fields.Int(dump_only=True)
    token = fields.Str(required=True)

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)
    level_id = fields.Int(required=True)
    level = fields.Nested(LevelSchema, dump_only=True)