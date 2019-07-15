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


def index_layouts(bundle_path):
    index_name = bundle_path.split('/')[-1]
    create_index(index_name)
    all_layouts = aggregate_layouts(bundle_path)
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


def aggregate_layouts(bundle_path):
    try:
        dirs = next(os.walk(bundle_path))
        root_dir, child_dirs = (dirs[0], dirs[1])
        layout_paths = ['/'.join([root_dir, child_dir, 'config', 'corfu']) for child_dir in
                        child_dirs if 'nsx_manager' in child_dir]
        pattern = 'LAYOUTS_*.ds'
        all_layouts = [glob.glob('/'.join([layout_path, pattern])) for layout_path in layout_paths]
        unique_layouts = set()
        result = []
        for sublist_layout in all_layouts:
            for layout in sublist_layout:
                layout_file = layout.split('/')[-1]
                if layout_file not in unique_layouts:
                    result.append(layout)
                    unique_layouts.add(layout_file)
        return result
    except FileNotFoundError as e:
        raise ('This bundle path does not exist', e)


if len(arguments) < 2:
    print('Bundle absolute directory name is required (decompressed)')
else:
    bundle_path = arguments[1].strip()
    index_layouts(bundle_path)
