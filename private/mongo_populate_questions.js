/*mongo commands are:
 meteor mongo btsturk.meteor.com
 load("private/mongo_populate_questions.js")
 */

//remove old questions
db.questions.remove({});

//add questions
db.questions.insert(
    [
        {
            "question_ID": 0,
            "text": "full elicitation mechanism",
            "busy": false,
            "previous_participants": 0,
            "slider0": 541,
            "slider1": 1004,
            "slider2": 303,
            "slider3": 1460
        },
        {
            "question_ID": 1,
            "text": "L2 mech - bunch 1",
            "busy": false,
            "previous_participants": 0,
            "slider00": 440,
            "slider10": 1050,
            "slider20": 350,
            "slider30": 1500,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider01": 541,
            "slider11": 1004,
            "slider21": 303,
            "slider31": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
            "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
            "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
        },
        {
            "question_ID": 2,
            "text": "L2 mech - bunch 2",
            "busy": false,
            "previous_participants": 0,
            "slider00": 541,
            "slider10": 1004,
            "slider20": 303,
            "slider30": 1460,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider01": 500,
            "slider11": 1100,
            "slider21": 350,
            "slider31": 1540,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
            "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
            "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
        },
        {
            "question_ID": 3,
            "text": "L2 mech - bunch 3",
            "busy": false,
            "previous_participants": 0,
            "slider00": 500,
            "slider10": 1100,
            "slider20": 350,
            "slider30": 1540,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider01": 440,
            "slider11": 1050,
            "slider21": 350,
            "slider31": 1500,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
            "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
            "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
        },
        {
            "question_ID": 4,
            "text": "L1 mech - bunch 1",
            "busy": false,
            "previous_participants": 0,
            "slider00": 440,
            "slider10": 1050,
            "slider20": 350,
            "slider30": 1500,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider01": 541,
            "slider11": 1004,
            "slider21": 303,
            "slider31": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
            "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
            "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
        },
        {
            "question_ID": 5,
            "text": "L1 mech - bunch 2",
            "busy": false,
            "previous_participants": 0,
            "slider00": 541,
            "slider10": 1004,
            "slider20": 303,
            "slider30": 1460,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider01": 500,
            "slider11": 1100,
            "slider21": 350,
            "slider31": 1540,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
            "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
            "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
        },
        {
            "question_ID": 6,
            "text": "L1 mech - bunch 3",
            "busy": false,
            "previous_participants": 0,
            "slider00": 500,
            "slider10": 1100,
            "slider20": 350,
            "slider30": 1540,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider01": 440,
            "slider11": 1050,
            "slider21": 350,
            "slider31": 1500,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
            "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
            "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
        }
    ]
);
