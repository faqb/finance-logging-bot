from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from cashews import cache


class LangMiddleware(LifetimeControllerMiddleware):
    """Define user language."""

    skip_patterns = ["error", "update"]

    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        # trying to get user language from cache
        user_lang_cache = await cache.get(str(obj.from_user.id))

        if not user_lang_cache:

            # getting user language from database and store to cache
            user_lang = await data["repo"].get_language(obj.from_user.id)
            await cache.set(key=str(obj.from_user.id), value=user_lang)

        data["lang"] = user_lang_cache or user_lang

    async def post_process(self, obj, data, *args):
        del data["lang"]

