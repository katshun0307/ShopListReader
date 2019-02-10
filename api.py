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

# メルティーキッス 焦がしバターキャラメル
sample_jan = 4902777060873
# octomore
sample_jan_2 = 5055807406154


def clean_product_name(product_name: str):
    space_pattern = re.compile(r"\s+", re.UNICODE)
    return space_pattern.sub('', product_name)
    # for remove_char in unwanted_chars:
    #     product_name.replace(remove_char, '')
    # return product_name


def get_name_from_jan(jan_code):
    url = "http://shopping.yahooapis.jp/ShoppingWebService/V1/itemSearch?" \
          "appid=dj00aiZpPXFSZkd4U2lLU0NweCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjI-&jan=%s" % jan_code
    r = requests.get(url)
    root = ET.fromstring(r.text)
    name_elements = root.findall("./{urn:yahoo:jp:itemSearch}Result/{urn:yahoo:jp:itemSearch}Hit/"
                                 "{urn:yahoo:jp:itemSearch}Name")
    return [clean_product_name(str(e.text)) for e in name_elements[:5]]


def get_product_name(jan_code):
    product_names = get_name_from_jan(jan_code)
    lcs_instance = LCS()
    return lcs_instance.lcs(product_names)


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
    print(get_name_from_jan(sample_jan_2))
