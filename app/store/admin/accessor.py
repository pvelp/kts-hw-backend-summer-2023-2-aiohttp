import typing
from typing import Optional

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await super().connect(app)
        await self.create_admin(email=self.app.config.admin.email, password=self.app.config.admin.password)
        print("Connect admin database")

    async def get_by_email(self, email: str) -> Optional[Admin]:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        if not await self.get_by_email(email):
            admin = Admin(
                id=self.app.database.next_admin_id,
                email=email,
                password=str(password)
            )
            self.app.database.admins.append(admin)
            return admin
