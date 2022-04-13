from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    """Define user role."""

    skip_patterns = ["error", "update"]

    def __init__(self, admin_set_id: set):
        super().__init__()
        self.admin_set_id = admin_set_id

    async def pre_process(self, obj, data, *args):
        if obj.from_user.id in self.admin_set_id:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

    async def post_process(self, obj, data, *args):
        del data["role"]
