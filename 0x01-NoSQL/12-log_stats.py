#!/usr/bin/env python3
"""
provides some stats about Nginx
logs stored in MongoDB
"""

from pymongo import MongoClient


def log_stats():
    """
    provides some stats about Nginx
    logs stored in MongoDB
    """
    client = MongoClient('mongodb://localhost:27017')
    methods = {
        'GET': 0,
        'POST': 0,
        'PUT': 0,
        'PATCH': 0,
        'DELETE': 0,
    }
    status = 0
    nginx = client.logs.nginx
    all_objs = nginx.find()
    count = 0

    for obj in all_objs:
        count += 1
        if obj['method'] in methods.keys():
            methods[obj['method']] += 1

        if obj['method'] == 'GET' and obj['path'] == "/status":
            status += 1

    print(f"{count} logs")
    print("Methods:")
    for k in methods.keys():
        print(f"\tmethod {k}: {methods[k]}")
    print(f"{status} status check")


if __name__ == "__main__":
    log_stats()
