from typing import List


class Parser:
    @staticmethod
    async def parse_info(data: List) -> str:
        parse_result = ""
        for row in data:
            for values in row.values():
                parse_result += f"{str(values).capitalize()} "
            parse_result += "\n"
        return parse_result

    @staticmethod
    async def parse_categories(categories):
        """Parse categories to insert into google sheets."""

        parse_result = []
        for row in categories:
            parse_result.append(f"{row[0]} {row[1].capitalize()}")
        return parse_result

    @staticmethod
    async def parse_month_statistics(data, category_count):
        d = {}
        parse_result = []
        for row in data:
            parse_result.append(row)
            if row[0] not in d.keys():
                d[row[0]] = [row[0]]
                d[row[0]].extend([None for _ in range(category_count)])
            d[row[0]].insert(row[1], row[2])

        return d
