# -*- coding: utf-8 -*- #

""" google tasks api
"""

import argparse
import oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build

import config

SCOPE_URL = "https://www.googleapis.com/auth/tasks"
flags = None


class Tasklist:

    def __init__(self, list_name):
        self.list_name = list_name
        self.credentials = self.get_credentials()
        self.service = self.build_service()
        self.list_id = self.get_list_id()

    @staticmethod
    def get_credentials():
        store = Storage(config.GOOGLE_CREDENTIAL_PATH)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = flow_from_clientsecrets(
                filename=config.GOOGLE_CLIENT_SECRET_PATH,
                scope=[SCOPE_URL])
            flow.user_agent = config.APP_NAME
            credentials = run_flow(flow, store, flags=flags)
        return credentials

    def build_service(self):
        service = build('tasks', 'v1', credentials=self.credentials)
        return service

    def get_list_id(self):
        task_lists = self.get_lists()
        for task_list in task_lists:
            if task_list['title'] == self.list_name:
                return task_list['id']
        raise KeyError("list of name %s not found." % self.list_name)

    def get_lists(self):
        results = self.service.tasklists().list().execute()
        lists = results.get('items', [])
        return lists

    def add_task(self, name):
        result = self.service.tasks().insert(tasklist=self.list_id, body={'title': name}).execute()
        return result

    def remove_task(self, task_id):
        result = self.service.tasks().delete(tasklist=self.list_id, task=task_id).execute()
        return result


if __name__ == '__main__':
    flags = argparse.ArgumentParser(
        parents=[oauth2client.tools.argparser]
    ).parse_args()
    shoplist = Tasklist("shoplist")
    print(shoplist.add_task("hogehoge"))


