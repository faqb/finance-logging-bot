from aiogram import Dispatcher

from tgbot.handlers.admin.handlers import start
from tgbot.handlers.admin.handlers import echo_message
from tgbot.handlers.admin.handlers import today_statistics
from tgbot.handlers.admin.handlers import month_statistics
from tgbot.handlers.admin.handlers import get_language
from tgbot.handlers.admin.handlers import change_language
from tgbot.handlers.admin.handlers import get_consumption
from tgbot.handlers.admin.handlers import add_consumption
from tgbot.handlers.admin.handlers import get_detailed_statistics
from tgbot.models.role import UserRole
from tgbot.states.consumption import ConsumptionState
from tgbot.states.lang import LangState


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
            start,
            commands=["start", "help"],
            state="*",
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            today_statistics,
            commands=["today"],
            state="*",
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            month_statistics,
            commands=["month"],
            state="*",
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            get_language,
            commands=["lang"],
            state="*",
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            change_language,
            state=LangState.change,
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            get_consumption,
            commands=["add"],
            state="*",
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            add_consumption,
            state=ConsumptionState.add,
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
            get_detailed_statistics,
            commands=["detailed"],
            state="*",
            role=UserRole.ADMIN
            )

    dp.register_message_handler(
        echo_message,
        state="*",
        role=UserRole.ADMIN
        )

