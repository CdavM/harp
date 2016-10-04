import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 81)
db = client['meteor']
questions = db['questions']

for q in questions.find():
    q['busy'] = False
    ar = q['averaging_status_array']
    for ind in range(len(ar)):
        if ar[ind] == 'BUSY':
            ar[ind] = 'FREE'
    q['averaging_status_array'] = ar
    questions.update_one(
        {"question_ID": q['question_ID']},
        {
            "$set": q
        }
    );
