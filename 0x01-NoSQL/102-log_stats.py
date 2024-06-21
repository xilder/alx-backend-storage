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

    print("Methods:")
    for method in methods:
        method_len = len(list(mongo_collection.find({"method": method})))
        print(f"\tmethod {method}: {method_len}")
    count = mongo_collection.count_documents({
        "method": "GET",
        "path": "/status"
        })
    print(f"{count} status check")

    print('IPs:')
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    results = mongo_collection.aggregate(pipeline)
    for result in results:
        print(f"\t{result.get('_id')}: {result.get('count')}")


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017')
    log_stats(client.logs.nginx)
