#!/usr/bin/env python3
"""
provides some stats about Nginx
logs stored in MongoDB
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    provides some stats about Nginx
    logs stored in MongoDB
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    status = mongo_collection.count_documents({})
    print(f"{status} logs")
    for method in methods:
        method_len = len(list(mongo_collection.find({"method": method})))
        print(f"\tmethod {method}: {method_len}")
    count = mongo_collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{count} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017')
    log_stats(client.logs.nginx)
