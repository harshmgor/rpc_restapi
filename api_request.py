#!/usr/bin/env python
import requests
import json


def api_get(url, headers):
    data = requests.get(url, headers=headers)
    return data.json()


def api_post(url, data, headers):
    return requests.post(url, data=json.dumps(list_to_dict(data)), headers=headers)


def api_put(url, data, headers):
    return requests.put(url, data=json.dumps(list_to_dict(data)), headers=headers)


def api_delete(url):
    return requests.delete(url)


def list_to_dict(data):
    _dict = {}
    for i in range(0, len(data), 2):
        _dict[data[i]] = data[i + 1]
    return _dict
