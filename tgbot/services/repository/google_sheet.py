from tgbot.config import Config


async def set_categories(categories):
    # set static start cell (need fix ??)
    iter_dict: dict = {"range": "B2:2", "values": [categories]}
    return iter_dict


async def set_data(agcm, data, categories):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(Config.SPREADSHEET_ID)


    # set reader permission for any one (need fix ??) 
    await agc.insert_permission(ss.id, None, perm_type="anyone", role="reader")

    sheet = await ss.get_worksheet(0)

    batch_list = []
    batch_list.append(await set_categories(categories))

    '''
    parsed data example:
    [
        {
            date_1, None, cat_x, None, cat_y, cat_z
        },
        {
            date_2, cat_xx, None, none, None, None
        }
    ]
    '''

    iter_dict: dict = {}
    for count_1, value in enumerate(data.values(), start=3):
        iter_dict["range"] = f"{count_1}:{count_1}"
        iter_dict["values"] = [value]

        batch_list.append(iter_dict)
        iter_dict: dict = {}

    await sheet.batch_update(batch_list)

