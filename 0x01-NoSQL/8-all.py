#!/usr/bin/env python3
"""lists all documents in a collection:"""

from pymongo import MongoClient


def list_all(mongo_collection):
    """lists all documents in a collection:"""
    all_document = mongo_collection.find()
    return all_document
