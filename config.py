# -*- coding: utf-8 -*- #

""" configurations
"""

import os

APP_NAME = "ShopListReader"

# set up yahoo api tokens
YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
YAHOO_CLIENT_SECRET = os.environ.get("YAHOO_CLIENT_ID")

# google api path
GOOGLE_CLIENT_SECRET_PATH = "./credentials/client_secret.json"
GOOGLE_CREDENTIAL_PATH = "./credentials/credential.json"
