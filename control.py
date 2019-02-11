# -*- coding: utf-8 -*- #

""" main controller
"""

import api
import config
from item import Item
from tasks import Tasklist
from database import ShopListDatabase, ItemDatabase

TASKLIST = Tasklist('shoplist')
shoplist_db = ShopListDatabase('buy')
items_db = ItemDatabase('item')

def process(jan_code):
    if config.mode == 'trash':
        # add to shoplist and 'buy' database
        try:
            print(jan_code)
            # search name in database first
            item_name = items_db.search_by_jan(jan_code)
            if not item_name:
                # search name on web
                item_name = api.get_product_name(jan_code)
            item = Item(item_name, jan_code)
            item.add_to_tasks(TASKLIST)
            item.add_to_database(shoplist_db)
        except Exception as e:
            print(str(e))
    else:
        # complete in database
        task_ids = shoplist_db.search_by_jan(jan_code, is_complete=False)
        print(task_ids)
        shoplist_db.set_complete(jan_code)
        # remove from shoplist
        updated = [TASKLIST.get_task(task_id) for task_id in task_ids]
        print("updated is " % updated)
        if len(updated) is not 0:
            # if updated is not empty, update item_name on tasks to database
            new_name = updated[-1]['title']
            items_db.set_new_name(jan_code, new_name)
        for task_id in task_ids:
            TASKLIST.remove_task(task_id)

if __name__ == '__main__':
    pass
