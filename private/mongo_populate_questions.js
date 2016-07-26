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
      "slider0": 541,
      "slider1": 1054,
      "slider2": 303,
      "slider3": 1298,
      "slider_2016_0": 541,
      "slider_2016_1": 1004,
      "slider_2016_2": 303,
      "slider_2016_3": 1248 
});
db.questions.insert({
    "question_ID": 1,
    "text": "mechanism1",
    "busy": false,
    "previous_participants": 0,
      "set0slider01": 541,
      "set0slider11": 1054,
      "set0slider21": 303,
      "set0slider31": 1298,
      "set1slider01": 541,
      "set1slider11": 1054,
      "set1slider21": 303,
      "set1slider31": 1298
});
db.questions.insert({
    "question_ID": 2,
    "text": "mechanism2",
    "busy": false,
    "previous_participants": 0,
      "slider0": 541,
      "slider1": 1004,
      "slider2": 303,
      "slider3": 1248
});
db.questions.insert({
    "question_ID": 3,
    "text": "mechanism3",
    "busy": false,
    "previous_participants": 0,
      "slider0": 541,
      "slider1": 1054,
      "slider2": 303,
      "slider3": 1298,
      "slider_2016_0": 541,
      "slider_2016_1": 1004,
      "slider_2016_2": 303,
      "slider_2016_3": 1248
});
db.questions.insert({
      "question_ID": 4,
      "text": "mechanism0 - version 2",
      "busy": false,
      "previous_participants": 0,
      "slider0": 500,
      "slider1": 1100,
      "slider2": 253,
      "slider3": 1350,
      "slider_2016_0": 541,
      "slider_2016_1": 1004,
      "slider_2016_2": 303,
      "slider_2016_3": 1248
});
db.questions.insert({
      "question_ID": 5,
      "text": "mechanism1 - version 2",
      "busy": false,
      "previous_participants": 0,
      "set0slider01": 500,
      "set0slider11": 1100,
      "set0slider21": 253,
      "set0slider31": 1350,
      "set1slider01": 541,
      "set1slider11": 1054,
      "set1slider21": 303,
      "set1slider31": 1298
});
db.questions.insert({
      "question_ID": 6,
      "text": "mechanism2 - version 2",
      "busy": false,
      "previous_participants": 0,
      "slider0": 541,
      "slider1": 1004,
      "slider2": 303,
      "slider3": 1248
});
db.questions.insert({
      "question_ID": 7,
      "text": "mechanism3 - version 2",
      "busy": false,
      "previous_participants": 0,
      "slider0": 500,
      "slider1": 1100,
      "slider2": 253,
      "slider3": 1350,
      "slider_2016_0": 541,
      "slider_2016_1": 1004,
      "slider_2016_2": 303,
      "slider_2016_3": 1248
});