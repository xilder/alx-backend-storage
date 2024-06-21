#!/usr/bin/env python3
"""returns all students sorted by average score"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    list_docs = mongo_collection.find()
    avg_score_list = []
    for doc in list_docs:
        obj = {}
        obj['_id'] = doc.get('_id')
        obj['name'] = doc.get('name')
        count = 0

        for topic in doc.get('topics'):
            count += topic.get('score')

        avg = count / len(doc.get('topics'))
        obj['averageScore'] = avg
        avg_score_list.append(obj)

    return sorted(avg_score_list, key=lambda x: x.get('averageScore'), reverse=True)