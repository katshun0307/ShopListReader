# -*- coding: utf-8 -*- #

""" configurations
"""

import os
import logging

APP_NAME = "ShopListReader"

# set up yahoo api tokens
YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
YAHOO_CLIENT_SECRET = os.environ.get("YAHOO_CLIENT_ID")

# google api path
GOOGLE_CLIENT_SECRET_PATH = "./credentials/client_secret.json"
GOOGLE_CREDENTIAL_PATH = "./credentials/credential.json"

# database config
DB_LOGIN = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'shoplist',
    'charset': 'utf8'
}

# logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def error(s):
    logging.error(s)

# mode change
SHOP_CODE = 1000000011
TRASH_CODE = 1000000111

mode = "trash"
