from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class UserAddSchema(Schema):
    email = fields.Str(required=True)


class UserSchema(UserAddSchema):
    id = fields.UUID(required=False, attribute='id_')


class UserGetRequestSchema(Schema):
    id = fields.UUID(required=True)


class ListUsersSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListUsersResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUsersSchema)


class GetSUserSchema(Schema):
    user = fields.Nested(UserSchema)


class UserGetResponseSchema(OkResponseSchema):
    data = fields.Nested(GetSUserSchema)
