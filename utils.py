from db import Database


pass_man = Database()


async def return_formatted_rows(list_of_rows):
    if list_of_rows:
        rows_list = []
        for count, service_name in enumerate(list_of_rows, start=1):
            rows_list.append(f'{count} {service_name[0]}')
        ready_rows = '\n'.join(rows_list)
        return ready_rows
    else:
        return None