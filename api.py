# -*- coding: utf-8 -*- #

""" api methods
"""
from functools import partial, reduce
from itertools import chain
from typing import Iterator
import re

import requests
import xml.etree.ElementTree as ET

import config

YAHOO_CLIENT_ID = config.YAHOO_CLIENT_ID
YAHOO_CLIENT_SECRET = config.YAHOO_CLIENT_SECRET

unwanted_chars = ['【', '】']

def clean_product_name(product_name: str):
    space_pattern = re.compile(r"\s+", re.UNICODE)
    non_space_name = space_pattern.sub('', product_name)
    for remove_char in unwanted_chars:
        non_space_name.replace(remove_char, '')
    return non_space_name


def get_name_from_jan(jan_code):
    """
    get multiple names from yahoo shopping api
    :param jan_code:
    :return:
    """
    url = "http://shopping.yahooapis.jp/ShoppingWebService/V1/itemSearch?" \
          "appid=dj00aiZpPXFSZkd4U2lLU0NweCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjI-&jan=%s" % jan_code
    r = requests.get(url)
    root = ET.fromstring(r.text)
    name_elements = root.findall("./{urn:yahoo:jp:itemSearch}Result/{urn:yahoo:jp:itemSearch}Hit/"
                                 "{urn:yahoo:jp:itemSearch}Name")
    return [clean_product_name(str(e.text)) for e in name_elements[:5]]


def get_product_name(jan_code):
    """
    get product name from yahoo api
    :param jan_code:
    :return: name of item
    """
    product_names = get_name_from_jan(jan_code)
    try:
        lcs_instance = LCS()
        name = lcs_instance.lcs(product_names)
        if name == "":
            raise ValueError
        return lcs_instance.lcs(product_names)
    except Exception as e:
        return "unknown item %s" % jan_code


class LCS:

    def __init__(self):
        pass

    def ngram(self, seq: str, n: int) -> Iterator[str]:
        return (seq[i: i + n] for i in range(0, len(seq) - n + 1))

    def allngram(self, seq: str) -> set:
        lengths = range(len(seq))
        ngrams = map(partial(self.ngram, seq), lengths)
        return set(chain.from_iterable(ngrams))

    def lcs(self, sequences):
        seqs_ngrams = map(self.allngram, sequences)
        intersection = reduce(set.intersection, seqs_ngrams)
        longest = max(intersection, key=len)
        return longest


if __name__ == '__main__':
    pass
