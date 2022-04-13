from typing import Any
from typing import Optional
from typing import Tuple

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from cashews import cache


class ACLMiddleware(I18nMiddleware):
    """Get user locale."""

    skip_patterns = ["error", "update"]

    def __init__(self, domain, path=None, default="en"):
        super().__init__(domain, path, default)

    async def get_user_locale(
            self,
            action: str,
            args: Tuple[Any]
    ) -> Optional[str]:

        user = types.User.get_current()
        return await cache.get(str(user.id))

