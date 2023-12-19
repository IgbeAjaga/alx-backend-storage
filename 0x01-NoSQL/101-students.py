#!/usr/bin/env python3
"""
all students sorted by average score
"""


from pymongo import MongoClient

def top_students(mongo_collection):
    """function that returns all students sorted by average score
    """
    students = mongo_collection.find()

    for student in students:
        scores = [topic['score'] for topic in student['topics']]
        average_score = sum(scores) / len(scores) if scores else 0
        student['averageScore'] = round(average_score, 2)

    return sorted(students, key=lambda x: x['averageScore'], reverse=True)

# Test the function with the provided script
if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # ... (Your insertion of data code here)

    students = list_all(students_collection)
    for student in students:
        print("[{}] {} - {}".format(student.get('_id'), student.get('name'), student.get('topics')))

    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))

