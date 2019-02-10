# -*- coding: utf-8 -*- #

""" Item class
"""

class Item:

    def __init__(self, item_name, item_jan):
        self.info = {
            'item_name': item_name,
            'jan_code': item_jan,
            'tasks_id': None,
        }

    def add_to_tasks(self, task_list):
        res = task_list.add_task(self.info['item_name'])
        self._add_item_id(res['id'])

    def add_to_database(self, db):
        db.add_item(self)

    def _add_item_id(self, item_id):
        self.info['tasks_id'] = item_id

    def get_keys(self):
        return ('item_name', 'jan_code', 'tasks_id')

    def get_values(self):
        info = self.info
        return ("N" + info['item_name'], info['jan_code'], info['tasks_id'])

    def get_name(self):
        return self.info['item_name']

    def get_jan(self):
        return self.info['jan_code']

    def get_task_id(self):
        return self.info['tasks_id']

    @staticmethod
    def is_same_kind_of_item(item1, item2):
        return item1.info['item_name'] == item2.info['item_name']

    @staticmethod
    def is_same_item(item1, item2):
        return item1.info['jan_code'] == item2.info['jan_code']
