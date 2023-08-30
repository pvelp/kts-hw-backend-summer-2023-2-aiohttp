from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest, HTTPNotFound, HTTPUnauthorized
from aiohttp_session import new_session, get_session

from app.admin.schemes import AdminResponseSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
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
    async def get(self):
        # try:
        #     self.request.admin
        # except Exception:
        #     raise HTTPUnauthorized

        if self.request.admin.email == self.request.app.config.admin.email:
            return json_response(data=AdminResponseSchema().dump(self.request.admin))
        # else:
        #     raise HTTPUnauthorized
