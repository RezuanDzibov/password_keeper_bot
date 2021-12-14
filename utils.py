from aiogram.utils import markdown as md

from db import Database


pass_man = Database()


async def return_grouped_rows(list_of_rows):
    if list_of_rows:
        rows_list = []
        for row_id, site_name in enumerate(list_of_rows, start=1):
            rows_list.append(
                md.text(
                    md.text(f'Row id: {row_id}\n'),
                    md.text(f'Site name: {site_name[0]}\n'),
                    md.text('-' * 50)
                )
            )
        rows = '\n'.join(rows_list)
        return rows
    else:
        return None