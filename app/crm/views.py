import uuid

from aiohttp.web_exceptions import (HTTPForbidden, HTTPNotFound,
                                    HTTPUnauthorized)
from aiohttp_apispec import (docs, querystring_schema, request_schema,
                             response_schema)

from app.crm.models import User
from app.crm.schemes import (ListUsersResponseSchema, UserAddSchema,
                             UserGetRequestSchema, UserGetResponseSchema,
                             UserSchema)
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import check_basic_auth, json_response


class AddUserView(View):
    @docs(tags=["crm"], summary="Add new user", description="Add new user to database")
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = self.request.get('data')
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response({'user': {'email': user.email, 'id': str(user.id_)}})


class ListUsersView(View):
    @docs(tags=['crm'], summary='List users', description='List users from database')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        auth = self.request.headers.get('Authorization')
        config = self.request.app.config
        if not auth:
            raise HTTPUnauthorized
        if not check_basic_auth(auth, config.username, config.password):
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [UserSchema().dump(user) for user in users]
        return json_response({'users': raw_users})


class GetUserView(View):
    @docs(tags=["crm"], summary="Get user", description="Get user from database")
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        auth = self.request.headers.get('Authorization')
        config = self.request.app.config
        if not auth:
            raise HTTPUnauthorized
        if not check_basic_auth(auth, config.username, config.password):
            raise HTTPForbidden
        user_id = self.request.query.get('id')
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if not user:
            raise HTTPNotFound
        return json_response({'user': UserSchema().dump(user)})
