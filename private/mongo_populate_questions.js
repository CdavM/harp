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
      "do_full_as_well" : true,
      "fullslider0": 541,
      "fullslider1": 1004,
      "fullslider2": 303,
      "fullslider3": 1460,
      "previous_participants": 0,
      "radius_start" : 300,
      "slider00": 500,
      "slider10": 1000,
      "slider20": 200,
      "slider30": 1300,
      "slider_2016_00": 541,
      "slider_2016_10": 1004,
      "slider_2016_20": 303,
      "slider_2016_30": 1460,
      "slider01": 200,
      "slider11": 800,
      "slider21": 300,
      "slider31": 1400,
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
      "do_full_as_well" : false,
      "previous_participants": 0,
      "radius_start" : 300,
      "slider00": 500,
      "slider10": 1000,
      "slider20": 200,
      "slider30": 1300,
      "slider_2016_00": 541,
      "slider_2016_10": 1004,
      "slider_2016_20": 303,
      "slider_2016_30": 1460,
      "slider01": 800,
      "slider11": 1250,
      "slider21": 400,
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
      "question_ID": 3,
      "text": "L2 mech - bunch 3",
      "busy": false,
      "do_full_as_well" : false,
      "previous_participants": 0,
      "radius_start" : 300,
      "slider00": 800,
      "slider10": 1250,
      "slider20": 400,
      "slider30": 1500,
      "slider_2016_00": 541,
      "slider_2016_10": 1004,
      "slider_2016_20": 303,
      "slider_2016_30": 1460,
      "slider01": 200,
      "slider11": 800,
      "slider21": 300,
      "slider31": 1400,
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
      "do_full_as_well" : true,
      "fullslider0": 541,
      "fullslider1": 1004,
      "fullslider2": 303,
      "fullslider3": 1460,
      "previous_participants": 0,
      "radius_start" : 300,
      "slider00": 500,
      "slider10": 1000,
      "slider20": 200,
      "slider30": 1300,
      "slider_2016_00": 541,
      "slider_2016_10": 1004,
      "slider_2016_20": 303,
      "slider_2016_30": 1460,
      "slider01": 200,
      "slider11": 800,
      "slider21": 300,
      "slider31": 1400,
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
      "do_full_as_well" : false,
      "previous_participants": 0,
      "radius_start" : 300,
      "slider00": 500,
      "slider10": 1000,
      "slider20": 200,
      "slider30": 1300,
      "slider_2016_00": 541,
      "slider_2016_10": 1004,
      "slider_2016_20": 303,
      "slider_2016_30": 1460,
      "slider01": 800,
      "slider11": 1250,
      "slider21": 400,
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
      "question_ID": 6,
      "text": "L1 mech - bunch 3",
      "busy": false,
      "do_full_as_well" : false,
      "previous_participants": 0,
      "radius_start" : 300,
      "slider00": 800,
      "slider10": 1250,
      "slider20": 400,
      "slider30": 1500,
      "slider_2016_00": 541,
      "slider_2016_10": 1004,
      "slider_2016_20": 303,
      "slider_2016_30": 1460,
      "slider01": 200,
      "slider11": 800,
      "slider21": 300,
      "slider31": 1400,
      "slider_2016_01": 541,
      "slider_2016_11": 1004,
      "slider_2016_21": 303,
      "slider_2016_31": 1460,
      "number_to_average" : 10,
      "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
      "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
    },
    {
        "question_ID": 7,
        "text": "Linf mech - bunch 1",
        "busy": false,
        "do_full_as_well" : true,
        "fullslider0": 541,
        "fullslider1": 1004,
        "fullslider2": 303,
        "fullslider3": 1460,
        "previous_participants": 0,
        "radius_start" : 100,
        "slider00": 500,
        "slider10": 1000,
        "slider20": 200,
        "slider30": 1300,
        "slider_2016_00": 541,
        "slider_2016_10": 1004,
        "slider_2016_20": 303,
        "slider_2016_30": 1460,
        "slider01": 200,
        "slider11": 800,
        "slider21": 300,
        "slider31": 1400,
        "slider_2016_01": 541,
        "slider_2016_11": 1004,
        "slider_2016_21": 303,
        "slider_2016_31": 1460,
        "number_to_average" : 10,
        "averaging_status_array" : ["FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE", "FREE"],
        "averaging_array" : [[],[],[],[],[],[],[],[],[],[]]
    },
    {
        "question_ID": 8,
        "text": "Linf mech - bunch 2",
        "busy": false,
        "do_full_as_well" : false,
        "previous_participants": 0,
        "radius_start" : 100,
        "slider00": 500,
        "slider10": 1000,
        "slider20": 200,
        "slider30": 1300,
        "slider_2016_00": 541,
        "slider_2016_10": 1004,
        "slider_2016_20": 303,
        "slider_2016_30": 1460,
        "slider01": 800,
        "slider11": 1250,
        "slider21": 400,
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
        "question_ID": 9,
        "text": "Linf mech - bunch 3",
        "do_full_as_well" : false,
        "busy": false,
        "previous_participants": 0,
        "radius_start" : 100,
        "slider00": 800,
        "slider10": 1250,
        "slider20": 400,
        "slider30": 1500,
        "slider_2016_00": 541,
        "slider_2016_10": 1004,
        "slider_2016_20": 303,
        "slider_2016_30": 1460,
        "slider01": 200,
        "slider11": 800,
        "slider21": 300,
        "slider31": 1400,
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
