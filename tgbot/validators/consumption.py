import re

from tgbot.exceptions.exceptions import InvalidMessageError


class ConsumptionValidator:
    """Validate user consumption."""

    async def validate_consumption(self, message: str) -> tuple:
        parsed_message = re.match(r"(.*) ([\d ]+)", message)
        if (
                not parsed_message
                or not parsed_message.group(0)
                or not parsed_message.group(1)
                or not parsed_message.group(2)
        ):
            raise InvalidMessageError("Invalid message!")

        self.category = parsed_message.group(1).strip().lower()
        self.amount = int(parsed_message.group(2).replace(" ", ""))

        return self.category, self.amount
