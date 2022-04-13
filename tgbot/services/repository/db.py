from tgbot.exceptions.exceptions import InvalidCategoryError
from tgbot.services.parser import Parser
from typing import Optional
from typing import Union


class LangRepository:
    def __init__(self, conn) -> None:
        self.conn = conn

    async def get_language(self, user_id: int) -> str:
        """
        Select user language to load it into cache.

        Args:
            user_id (int): telegram user id.

        Returns:
            str: current user language.

        """

        return await self.conn.fetchval(
                "SELECT (lang) FROM users WHERE users.id=$1", user_id
                )

    async def update_language(self, user_id: int, lang: str) -> None:
        """
        Update user language.

        Args:
            user_id (int): telegram user id.
            lang (str): selected user language.

        """

        await self.conn.execute(
                "UPDATE users SET lang=$1 WHERE users.id=$2", lang, user_id
                )


class ConsumptionRepository:
    def __init__(self, conn) -> None:
        self.conn = conn

    async def _check_consumption(self, category_id: int) -> Optional[int]:
        """
        Checks for the presence of at least one consumption in current day.

        Args:
            category_id (int):

        Returns:
            int: 1 if successful.
            None: if not successful.

        """

        return await self.conn.fetchval(
                        "SELECT 1 FROM consumption "
                        "WHERE category_id=$1 AND created=CURRENT_DATE",
                        category_id
                        )

    async def _category_id(self, category: str) -> int:
        """
        Select category id if category is in any alias.

        Args:
            category (str): category name.

        Returns:
            int: category id.

        """

        return await self.conn.fetchval(
                "SELECT (id) FROM aliases "
                "WHERE $1 = ANY (en_aliases || uk_aliases || ru_aliases)",
                category
                )

    async def add_consumption(self, category: str, amount: int) -> None:
        """
        Add user consumption. If consumption already exists updates it,
        otherwise created.

        Args:
            category (str): category
            amount (int): category item amount

        """

        category_id = await self._category_id(category)
        if not category_id:
            raise InvalidCategoryError("Invalid category!")

        if await self._check_consumption(category_id):
            await self.conn.execute(
                    "UPDATE consumption SET amount=amount+$1 "
                    "WHERE category_id=$2 AND created=CURRENT_DATE",
                    amount, category_id
                    )
        else:
            await self.conn.execute(
                    "INSERT INTO consumption(category_id, amount, created) "
                    "VALUES($1, $2, CURRENT_DATE)", category_id, amount
                    )

    async def day_statistics(self, lang: str) -> Union[object, str]:
        """
        Get current day statistics. May be used to fetch statistics for
        any day (NOT IMPLEMENTED).

        Args:
            lang (str): fetch data language.

        Returns:
            object: Parser object that parses fetched data.
            str: if Parser object returns None, it means that doesn't exist
                any notes in current day -> return "Nothing" message.

        """

        data = await self.conn.fetch(
                f"SELECT categories.picture, categories.{lang}_category, consumption.amount "
                "FROM consumption "
                "INNER JOIN categories ON categories.id=consumption.category_id "
                "WHERE consumption.created=CURRENT_DATE ORDER BY amount DESC"
        )
        return await Parser.parse_info(data) or "Nothing"

    async def month_statistics(self, lang: str) -> Union[object, str]:
        """
        Get current month statistics. May be used to fetch statistics for
        any month (NOT IMPLEMENTED).
        Args:
            lang (str): fetch data language.

        Returns:
            object: Parser object that parses fetched data.
            str: if Parser object returns None, it means that doesn't exist
                any notes in current month-> return "Nothing" message.

        """

        data = await self.conn.fetch(
                f"SELECT categories.picture, categories.{lang}_category, SUM(amount) "
                "FROM consumption "
                "INNER JOIN categories ON categories.id=consumption.category_id "
                "WHERE consumption.created >= date_trunc('month', CURRENT_DATE) "
                f"GROUP BY categories.{lang}_category, categories.picture"
                )
        return await Parser.parse_info(data) or "Nothing"


class GoogleSheetsRepository:
    def __init__(self, conn) -> None:
        self.conn = conn

    async def _category_count(self) -> int:
        """
        Count the number of categories.

        Returns:
            int: number of categories.

        """

        return await self.conn.fetchval(
                "SELECT COUNT(categories.id) "
                "FROM categories"
                )

    async def categories(self, lang: str) -> object:
        """
        Select all categories picture + category name.

        Args:
            lang (str): fetch data language.

        Returns:
            object: Parser object

        """

        categories = await self.conn.fetch(
                f"SELECT categories.picture, categories.{lang}_category "
                "FROM categories"
                )
        return await Parser.parse_categories(categories)

    async def google_sheet_month_statistics(self) -> object:
        """
        Select month statistics to use in Google Sheets.

        Returns:
            object: Parser object

        """

        data = await self.conn.fetch(
                "SELECT TO_CHAR(consumption.created, 'DD.MM.YYYY'), consumption.category_id, SUM(consumption.amount) "
                "FROM consumption WHERE consumption.created >= date_trunc('month', CURRENT_date) "
                f"GROUP BY consumption.created, consumption.category_id ORDER BY consumption.created, consumption.category_id"
                )
        return await Parser.parse_month_statistics(data, await self._category_count())


class Repo(LangRepository, ConsumptionRepository, GoogleSheetsRepository):
    """Db abstraction layer"""

    def __init__(self, conn) -> None:
        super().__init__(conn)

    async def upload_admins(self, admins: set) -> None:
        """
        Insert admins from config to database.
        Using to get current user language.

        Args:
            admins (set): set with admins telegram id.

        """
        for admin in admins:
            await self.conn.execute(
                    "INSERT INTO users (id) "
                    "VALUES ($1) ON CONFLICT (id) DO NOTHING", admin
                    )

