from tgbot.config import Config
from tgbot.exceptions.exceptions import InvalidLanguageError


class LanguageValidator:
    """Check if user language exists."""

    async def validate_lang(self, message):
        if message not in Config.LANGUAGES:
            raise InvalidLanguageError("Invalid language!")

