# -*- coding: utf-8 -*- #

""" main controller
"""

import api
import config
from item import Item
from tasks import Tasklist
from database import DataBase

TASKLIST = Tasklist('shoplist')
DB = DataBase('buy')

def process(jan_code):
    if config.mode == 'trash':
        # add to shoplist and 'buy' database
        try:
            print(jan_code)
            item_name = api.get_product_name(jan_code)
            item = Item(item_name, jan_code)
            item.add_to_tasks(TASKLIST)
            item.add_to_database(DB)
        except Exception as e:
            print(str(e))
    else:
        # remove from shoplist
        task_ids = DB.search_by_jan(jan_code)
        print(task_ids)
        for task_id in task_ids:
            TASKLIST.remove_task(task_id)
        print("done")

if __name__ == '__main__':
    pass
