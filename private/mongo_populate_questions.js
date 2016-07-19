/*mongo commands are:
 meteor mongo btsturk.meteor.com
 load("private/mongo_populate_questions.js")
 */

//remove old questions
db.questions.remove({});

//add questions
db.questions.insert({
    "question_ID": 0,
    "text": "mechanism0",
    "busy": false,
    "previous_participants": 0,
    "slider0": 600,
    "slider1": 950,
    "slider2": 140,
    "slider3": 1500,
    "slider_2016_0": 541,
    "slider_2016_1": 1004,
    "slider_2016_2": 149,
    "slider_2016_3": 1460
});
db.questions.insert({
    "question_ID": 1,
    "text": "mechanism1",
    "busy": false,
    "previous_participants": 0,
    "set0slider01": 600,
    "set0slider11": 950,
    "set0slider21": 140,
    "set0slider31": 1500,
    "set1slider01": 500,
    "set1slider11": 1054,
    "set1slider21": 155,
    "set1slider31": 1420
});
db.questions.insert({
    "question_ID": 2,
    "text": "mechanism2",
    "busy": false,
    "previous_participants": 0,
    "slider0": 541,
    "slider1": 1004,
    "slider2": 149,
    "slider3": 1460
});
db.questions.insert({
    "question_ID": 3,
    "text": "mechanism3",
    "busy": false,
    "previous_participants": 0,
    "slider0": 600,
    "slider1": 950,
    "slider2": 140,
    "slider3": 1500,
    "slider_2016_0": 541,
    "slider_2016_1": 1004,
    "slider_2016_2": 149,
    "slider_2016_3": 1460
});