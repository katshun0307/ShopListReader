# -*- coding: utf-8 -*- #

""" manage database
"""

import MySQLdb
from item import Item
import config


class DataBase:

    def __init__(self, table_name):
        self.db = MySQLdb.connect(**config.DB_LOGIN)
        self.table_name = table_name

    def reconnect(self):
        if not self.db.is_connected():
            self.db = MySQLdb.connect(**config.DB_LOGIN)

    def add_item(self, item):
        cursor = self.db.cursor()
        try:
            stmt = "insert into %s (item_name, jan_code, tasks_id) values (N'%s', %s, '%s')" % \
                   (self.table_name, item.get_name(), item.get_jan(), item.get_task_id())
            print(stmt)
            cursor.execute("SET NAMES utf8")
            cursor.execute(stmt)
            cursor.fetchall()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def search_by_task_id(self, task_id):
        cursor = self.db.cursor()
        try:
            stmt = "select item_name, jan_code from %s  where" \
                   "tasks_id = %s" % (self.table_name, task_id)
            cursor.execute(stmt)
            result = cursor.fetchall()
            return Item(result[0])
        except Exception as e:
            config.error("could not find data with task_id: %s" % task_id)

    def search_by_jan(self, jan_code):
        cursor = self.db.cursor()
        try:
            stmt = "select item_name, tasks_id from %s  where " \
                   "jan_code = %s" % (self.table_name, jan_code)
            cursor.execute(stmt)
            result = cursor.fetchall()
            return [r[1] for r in result]
        except Exception as e:
            config.error("database.search_by_jan :: could not find data with jan_code: %s (%s)"
                         % (jan_code, e))


if __name__ == '__main__':
    pass
