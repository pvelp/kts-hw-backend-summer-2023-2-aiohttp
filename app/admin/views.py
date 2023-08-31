from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminResponseSchema, AdminRequestSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(tags=["admin"], summary='Login for admin')
    @request_schema(AdminRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            raise HTTPBadRequest
        admin = await self.request.app.store.admins.get_by_email(email)
        if not admin or not admin.is_password_correct(password):
            raise HTTPForbidden
        raw_admin = AdminResponseSchema().dump(admin)
        session = await new_session(self.request)
        session["token"] = self.request.app.config.session.key
        session["admin"] = raw_admin
        return json_response(data=raw_admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(tags=["admin"], summary='Check current user')
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        return json_response(data=AdminResponseSchema().dump(self.request.admin))
