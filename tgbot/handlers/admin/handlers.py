from datetime import date

import gspread_asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message
from cashews import cache
from google.oauth2.service_account import Credentials

from tgbot.config import Config
from tgbot.exceptions.exceptions import InvalidCategoryError
from tgbot.exceptions.exceptions import InvalidLanguageError
from tgbot.exceptions.exceptions import InvalidMessageError
from tgbot.middlewares.locale import ACLMiddleware
from tgbot.services.repository.db import Repo
from tgbot.services.repository.google_sheet import set_data
from tgbot.states.consumption import ConsumptionState
from tgbot.states.lang import LangState
from tgbot.validators.consumption import ConsumptionValidator
from tgbot.validators.lang import LanguageValidator


# create middleware object to translate message
_ = ACLMiddleware(Config.I18N_DOMAIN, Config.LOCALES_DIR).gettext


def get_creds():
    """Setup Google Sheet credentials to use API."""
    creds = Credentials.from_service_account_file(Config.CREDENTIALS_FILE)
    scoped = creds.with_scopes(
            [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
                ]
            )
    return scoped


# create async gspread object
agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


async def start(message: Message):
    await message.answer(
        _(
            "Add record: /add\n\n"
            "Check today statistics: /today\n"
            "Check month statistics: /month\n"
            "Get detailed month statistics: /detailed\n"
            "Select language: /lang\n"
        )
    )


async def today_statistics(message: Message, repo: Repo):
    """Get user language and show current day statistics."""

    data = ctx_data.get()
    info = await repo.day_statistics(data.get("lang"))
    await message.answer(info)


async def month_statistics(message: Message, repo: Repo):
    """Get user language and show current month statistics."""

    data = ctx_data.get()
    info = await repo.month_statistics(data.get("lang"))
    await message.answer(info)


async def get_language(message: Message):
    """Get new user language for changing."""

    # set language state
    await LangState.change.set()

    await message.answer(
        _("Select your language:\n\nEnglish: /en\nUkrainian: /uk\nRussian: /ru")
    )


async def change_language(message: Message, state: FSMContext, repo: Repo):
    try:
        # validate language
        await LanguageValidator().validate_lang(message.text.replace("/", ""))

        # clear user cache
        await cache.delete(str(message.from_user.id))

        # update language in database
        await repo.update_language(
            message.from_user.id,
            message.text.replace("/", "")
        )

        await message.answer(
            _("Your language is: ") + message.text.replace('/', '')
        )

    except InvalidLanguageError as e:
        await message.answer(str(e))

    # drop language state
    await state.finish()


async def get_consumption(message: Message):
    """Get user consumption to insert into database."""

    # set consumption state
    await ConsumptionState.add.set()

    await message.answer(
        _("Input [category price]")
    )


async def add_consumption(message: Message, state: FSMContext, repo: Repo):
    try:
        category, amount = await ConsumptionValidator().validate_consumption(
            message.text
        )
        await repo.add_consumption(category, int(amount))
        await message.answer(_("Your consumption was added!"))
    except (InvalidMessageError, InvalidCategoryError) as e:
        await message.answer(str(e))

    await state.finish()


async def get_detailed_statistics(message: Message, repo: Repo):
    """Generate Google Sheet document with detailed month statistics."""

    data = ctx_data.get()
    categories = await repo.categories(data.get("lang"))
    data = await repo.google_sheet_month_statistics()

    await message.answer(
            _(
                "Creating statistics with Google Sheets.\n"
                "It can takes some time..."
                )
            )

    # insert data to Google Sheet document
    await set_data(agcm, data, categories)

    # create document link for telegram user
    google_sheet_link = (
            "https://docs.google.com/spreadsheets/d/"
            f"{Config.SPREADSHEET_ID}"
            )

    await message.answer(google_sheet_link)


async def echo_message(message: Message):
    pass
