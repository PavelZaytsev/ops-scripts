#! /usr/bin/env python

import requests
import sys
import os
import glob
import json
from datetime import datetime
from requests import HTTPError

user = 'elastic'
password = 'changeme'
arguments = sys.argv
url = 'http://localhost:9200'

"""
Should be bug id

"""


def create_index(index_name):
    try:
        index_name = '{}_layouts'.format(index_name)
        uri = '/'.join([url, index_name])
        print('Checking if index exists')
        r = requests.head(uri, auth=(user, password))
        if r.status_code == 200:
            print('Already exists')
            return
        print('Creating index {}'.format(index_name))
        settings = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            },
            "mappings": {
                "properties": {
                    "segments": {
                        "type": "nested"
                    }
                }
            }
        }
        r = requests.put(uri, json=settings, auth=(user, password))
        r.raise_for_status()

    except Exception as e:
        print('Failed to create an index', e)
        raise


def index_record(index_name, record):
    try:
        index_name = '{}_layouts'.format(index_name)
        uri = '/'.join([url, index_name, '_doc'])
        r = requests.post(uri, json=record, auth=(user, password))
        r.raise_for_status()
    except Exception as e:
        print('Failed to send a record', e)
        raise


def index_layouts(layout_path, index_name):
    create_index(index_name)
    pattern = 'LAYOUTS_*.ds'
    all_layouts = glob.glob('/'.join([layout_path, pattern]))
    if not all_layouts:
        raise FileNotFoundError('Layouts are missing in the directory')
    print('Indexing layouts')
    for f in all_layouts:
        timestamp = datetime.utcfromtimestamp(os.path.getmtime(f))
        buffer = []
        with open(f, 'rb') as file:
            content = file.read(4)
            while content != b'':
                content = file.read(1)
                buffer.append(content)
            string = str(b''.join(buffer), 'utf-8')
            json_string = json.loads(string)
            json_string['timestamp'] = timestamp.isoformat()
            index_record(index_name, json_string)


if len(arguments) < 3:
    print('Path and index name are required')
else:
    layout_path = arguments[1].strip()
    index_name = arguments[2].strip()
    index_layouts(layout_path, index_name)
