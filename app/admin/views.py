from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_session import new_session

from app.admin.schemes import AdminResponseSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    async def post(self):
        data = await self.request.json()
        email = data['email']
        password = data['password']
        admin = await self.request.app.store.admins.get_by_email(email)
        if not admin or not admin.is_password_correct(password):
            raise HTTPForbidden

        admin_json = AdminResponseSchema().dump(admin)
        # session = await new_session(request=self.request)
        # session["admin"] = admin_json

        return json_response(data=admin_json)


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
