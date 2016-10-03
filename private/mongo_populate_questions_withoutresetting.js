/*mongo commands are:
 meteor mongo btsturk.meteor.com
 load("private/mongo_populate_questions.js")
 */

//add questions
db.questions.update( {"question_ID": 0},
        {$set :
        {
            "question_ID": 0,
            "text": "full elicitation mechanism",
            "busy": false,
            "do_full_as_well" : false,
            "slider0": 541,
            "slider1": 1004,
            "slider2": 303,
            "slider3": 1460

 }       });
db.questions.update( {"question_ID": 1},
        {$set :
        {
            "question_ID": 1,
            "text": "L2 mech - bunch 1",
            "busy": false,
            "do_full_as_well" : true,
            "fullslider0": 541,
            "fullslider1": 1004,
            "fullslider2": 303,
            "fullslider3": 1460,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,

 }       });
db.questions.update( {"question_ID": 2},
        {$set :
        {
            "question_ID": 2,
            "text": "L2 mech - bunch 2",
            "busy": false,
            "do_full_as_well" : false,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,

 }       });
db.questions.update( {"question_ID": 3},
        {$set :
        {
            "question_ID": 3,
            "text": "L2 mech - bunch 3",
            "busy": false,
            "do_full_as_well" : false,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
        }});
db.questions.update( {"question_ID": 4},
        {$set :
        {
            "question_ID": 4,
            "text": "L1 mech - bunch 1",
            "busy": false,
            "do_full_as_well" : true,
            "fullslider0": 541,
            "fullslider1": 1004,
            "fullslider2": 303,
            "fullslider3": 1460,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
      }
      });
db.questions.update( {"question_ID": 5},
        {$set :
        {
            "question_ID": 5,
            "text": "L1 mech - bunch 2",
            "busy": false,
            "do_full_as_well" : false,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
 }       });
db.questions.update( {"question_ID": 6},
        {$set :
        {
            "question_ID": 6,
            "text": "L1 mech - bunch 3",
            "do_full_as_well" : false,
            "busy": false,
            "slider_2016_00": 541,
            "slider_2016_10": 1004,
            "slider_2016_20": 303,
            "slider_2016_30": 1460,
            "slider_2016_01": 541,
            "slider_2016_11": 1004,
            "slider_2016_21": 303,
            "slider_2016_31": 1460,
            "number_to_average" : 10,
      }
      });

      db.questions.update( {"question_ID": 7},
              {$set :
              {
                  "question_ID": 7,
                  "text": "Linf mech - bunch 1",
                  "busy": false,
                  "do_full_as_well" : true,
                  "fullslider0": 541,
                  "fullslider1": 1004,
                  "fullslider2": 303,
                  "fullslider3": 1460,
                  "slider_2016_00": 541,
                  "slider_2016_10": 1004,
                  "slider_2016_20": 303,
                  "slider_2016_30": 1460,
                  "slider_2016_01": 541,
                  "slider_2016_11": 1004,
                  "slider_2016_21": 303,
                  "slider_2016_31": 1460,
                  "number_to_average" : 10,
            }
            });
      db.questions.update( {"question_ID": 8},
              {$set :
              {
                  "question_ID": 8,
                  "text": "Linf mech - bunch 2",
                  "busy": false,
                  "do_full_as_well" : false,
                  "slider_2016_00": 541,
                  "slider_2016_10": 1004,
                  "slider_2016_20": 303,
                  "slider_2016_30": 1460,
                  "slider_2016_01": 541,
                  "slider_2016_11": 1004,
                  "slider_2016_21": 303,
                  "slider_2016_31": 1460,
                  "number_to_average" : 10,
       }       });
      db.questions.update( {"question_ID": 9},
              {$set :
              {
                  "question_ID": 9,
                  "text": "Linf mech - bunch 3",
                  "do_full_as_well" : false,
                  "busy": false,
                  "slider_2016_00": 541,
                  "slider_2016_10": 1004,
                  "slider_2016_20": 303,
                  "slider_2016_30": 1460,
                  "slider_2016_01": 541,
                  "slider_2016_11": 1004,
                  "slider_2016_21": 303,
                  "slider_2016_31": 1460,
                  "number_to_average" : 10,
            }
          });
