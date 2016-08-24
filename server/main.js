//This code only executed on the server

Meteor.publish("answers", function() {
    return Answers.find();
});
Meteor.publish("questions", function() {
    return Questions.find();
});
Solutions = new Mongo.Collection("solutions");
Meteor.publish("answerforms", function() {
    return AnswerForms.find();
});
intervals = {};
counters = {};
timers = {};

threshold = Meteor.settings.threshold_workers; //we need at least threshold users in every experiment
experiment_id_counter = 1;

existing_experiment_counter = 0;
if (Answers.findOne({
        begin_experiment: true
    })) {
    existing_experiment_counter = Answers.find({
        begin_experiment: true
    }, {
        sort: {
            experiment_id: -1
        },
        limit: 1
    }).fetch();
    experiment_id_counter = existing_experiment_counter[0].experiment_id + 1;
}


Meteor.startup(function() {
    clear_busy_flags: {
        Questions.update({}, {
            $set: {
                'busy': false
            }
        }, {
            multi: true
        });
    }

    //check and potentially update question database
    update_questions: {
        for (var post in Meteor.settings.questions) {
            if (!Questions.findOne(Meteor.settings.questions[post]) || Questions.find().count() != Meteor.settings.questions.length) {
                console.log("Updating questionbank database");
                Questions.remove({});
                for (post in Meteor.settings.questions) {
                    Questions.insert(Meteor.settings.questions[post]);
                }
                break update_questions;
            }
        }
    }

    //check and potentially update answer_forms

    update_answer_forms: {
        for (post in Meteor.settings.public.answer_forms) {
            if (!AnswerForms.findOne(Meteor.settings.public.answer_forms[post]) || AnswerForms.find().count() != Meteor.settings.public.answer_forms.length) {
                console.log("Updating answer form database");
                AnswerForms.remove({});
                for (post in Meteor.settings.public.answer_forms) {
                    AnswerForms.insert(Meteor.settings.public.answer_forms[post]);
                }
                break update_answer_forms;
            }
        }
    }

});

Meteor.methods({
    initialPost: function(post, status) {
        //check if already present
        if (status == 'startup') {
            if (Answers.findOne({
                    worker_ID: post.worker_ID
                })) {
                return;
            }
            var initial_time_val = new Date().getTime();
            Answers.insert({
                worker_ID: post.worker_ID,
                asg_ID: post.asg_ID,
                hit_ID: post.hit_ID,
                initial_time: initial_time_val,
                latest_time: initial_time_val
            });
            return;
        } else {
            var experiment_id_value = experiment_id_counter;
            var begin_time_val = new Date().getTime();
            Answers.update({
                worker_ID: post.worker_ID
            }, {
                $set: {
                    begin_time: begin_time_val,
                    experiment_id: experiment_id_value,
                    avg_payment: 0,
                    experiment_finished: false,
                    latest_time: begin_time_val
                }
            });
        }

        if (counters[experiment_id_value]) {
            counters[experiment_id_value]['initial_counter']++;
        } else {
            counters[experiment_id_value] = {};
            counters[experiment_id_value]['initial_counter'] = 1;
            counters[experiment_id_value]['initial_timer'] = true;
            //set timeout, also cancel a flag
            //TODO: implement automatic start
        }
        if (!counters[experiment_id_value]['random_counter']) {
            counters[experiment_id_value]['random_counter'] = [];
        }


        if (counters[experiment_id_value]['initial_timer'] && counters[experiment_id_value]['initial_counter'] >= threshold) { //call this when we get two entries
            experiment_id_counter++;
            Answers.update({
                experiment_id: experiment_id_value
            }, {
                $set: {
                    begin_experiment: true
                }
            }, {
                upsert: true,
                multi: true
            });
            Meteor.call('beginQuestionScheduler', experiment_id_value);
            counters[experiment_id_value]['initial_timer'] = false;
        }
    },

    newPost: function(post) {
        //format time to UTC human readable format
        post.initial_time = new Date(post.initial_time).toLocaleString();
        var existing_entry = Answers.findOne({
            worker_ID: post.worker_ID
        });
        var answers_value = {};
        var experiment_id_value = existing_entry.experiment_id;
        if (existing_entry.answer1) {
            //worker has submitted some answers, retrieve them
            answers_value = existing_entry.answer1;
        }
        var current_question = existing_entry.current_question;
        var current_answer = existing_entry.current_answer;
        var current_avg_number = existing_entry.current_avg_number;

        //check if the user has answered the question already
        if (!answers_value[current_question]) {
            answers_value[current_question] = {};
        }
        post.answer['time'] = new Date().getTime() - existing_entry.latest_time;
        answers_value[current_question][current_answer] = post.answer;

        var fields_to_be_updated = {};
        var new_slider_values = {};
        var total_money_spent = 0;
        var total_money_spent_set0 = 0;
        var total_money_spent_set1 = 0;
        for (var well_idx = 0; well_idx < 2; well_idx++) {
            var total_percentage_of_credits_spent = 0;
            for (var slider_idx = 0; slider_idx < 4; slider_idx++) {
                if (post.answer['slider' + slider_idx + well_idx]) {
                    if (isNaN(Number(post.answer['slider' + slider_idx + well_idx][0]))) {
                        console.log("Value cannot be converted into a number.");
                        console.log(post.answer['slider' + slider_idx + well_idx][0]);
                        console.log("Rejecting the entry for experiment " + experiment_id_value);
                        return;
                    }
                    new_slider_values['slider' + slider_idx + well_idx] = Math.max(0.01, Number(post.answer['slider' + slider_idx + well_idx][0]));
                    if (slider_idx == 3) {
                        total_money_spent -= Number(post.answer['slider' + slider_idx + well_idx][0]);
                    } else {
                        total_money_spent += Number(post.answer['slider' + slider_idx + well_idx][0]);
                    }
                    var slider_difference = Number(post.answer['slider' + slider_idx + well_idx][0]) - existing_entry['initial_slider' + slider_idx + well_idx];
                    var slider_relative_diff = slider_difference / existing_entry['radius'];
                    if ([1, 2, 3].indexOf(current_question) > -1) {
                        // L1
                        answers_value['slider' + slider_idx + well_idx + "_credits"] = Math.abs(slider_relative_diff);
                    } else if ([4, 5, 6].indexOf(current_question) > -1) {
                        // L2
                        answers_value['slider' + slider_idx + well_idx + "_credits"] = Math.pow(slider_relative_diff, 2);
                    }
                    total_percentage_of_credits_spent += answers_value['slider' + slider_idx + well_idx + "_credits"];
                }

            }
          if (total_percentage_of_credits_spent > 1.1) {
                /*
                Too many credits used.
                */
                console.log("Too many credits used by experiment " + experiment_id_value);
                console.log("Terminating experiment " + experiment_id_value);
                return;
            }
        }
        if (Object.keys(new_slider_values).length && typeof(current_question) == "number" && current_question != 0) {
          //set it to proper array location for averaging purposes
          current_question_dict = Questions.findOne({"question_ID": current_question});
          current_question_dict.averaging_array[current_avg_number] = new_slider_values;

            Questions.update({
                "question_ID": current_question
            }, {
                $set: current_question_dict
            });
        }
        // add the deficit term
        if (current_question != 0 && current_answer == 1) {
            answers_value[current_question][current_answer]['deficit'] = total_money_spent + 162;
        }
        //Add entry to Answers
        Answers.update({
            worker_ID: post.worker_ID
        }, {
            $set: {
                answer1: answers_value
            }
        }, {
            upsert: true
        });
        //update question when we get ALL the answers
        if (!counters[experiment_id_value]) {
            counters[experiment_id_value] = {};
        }
        if (counters[experiment_id_value][current_question]) {
            counters[experiment_id_value][current_question]++;
        } else {
            counters[experiment_id_value][current_question] = 1;
        }
        var num_of_workers = Meteor.settings.threshold_workers;
        if (counters[experiment_id_value][current_question] >= num_of_workers) {
            Meteor.call('beginQuestionScheduler', experiment_id_value);
        }

    },
    submitFeedback: function(worker_ID_value, feedback_value) {
        if (typeof worker_ID_value === 'undefined' || !worker_ID_value || typeof feedback_value === 'undefined' || !feedback_value) {
            return;
        }
        Answers.update({
            worker_ID: worker_ID_value
        }, {
            $set: {
                feedback: feedback_value
            }
        }, {
            upsert: true
        });
        console.log("Feedback inserted for worker " + worker_ID_value);
    },

    beginQuestionScheduler: function(experiment_id_value, wasTimedOut) {
      wasTimedOut = (typeof wasTimedOut === 'undefined') ? 'false' : wasTimedOut;
        //update questions every duration seconds
        var curr_experiment = Answers.findOne({
            experiment_id: experiment_id_value
        });
        var num_of_questions = Questions.find().count();
        update_question = function(experiment_id_value) {
            var curr_experiment = Answers.findOne({
                experiment_id: experiment_id_value
            });
            if (!curr_experiment) {
                console.log("experiment_id " + experiment_id_value + " not found in the database");
                return;
            }
            var num_of_questions = Questions.find().count();
            var selection_size = num_of_questions;
            if (Meteor.settings.questions_subset_size) {
                selection_size = Math.min(num_of_questions, Meteor.settings.questions_subset_size);
            }
            var next_question = -1;
            if (Meteor.settings.randomize_questions) {
                //generate random question
                var question_sampler = function() {
                    var question_selected = -1;
                    // if all mechanisms are busy
                    if (Questions.find({
                            "busy": true
                        }).count() == 8) {
                        var rnd_sample = Math.random();
                        question_selected = 0;
                    } else {
                        do {
                            var rnd_sample = Math.random();
                            if (rnd_sample < 0.1666666666667)
                                question_selected = 0;
                            else if (rnd_sample < (0.1666666666667 * 7)) //TODO change from 7 to 2 after testing averaging
                                question_selected = 1;
                            else if (rnd_sample < (0.1666666666667 * 3))
                                question_selected = 3;
                            else if (rnd_sample < (0.1666666666667 * 4))
                                question_selected = 4;
                            else if (rnd_sample < (0.1666666666667 * 5))
                                question_selected = 5;
                            else
                                question_selected = 6;
                        } while ((counters[experiment_id_value]['random_counter'].indexOf(question_selected) != -1 &&
                                counters[experiment_id_value]['random_counter'].length < selection_size) ||
                            Questions.findOne({
                                "question_ID": question_selected
                            }).busy == true);
                    }
                    return question_selected;
                };
                next_question = question_sampler();
                console.log("selected question " + next_question);
            } else {
                next_question = curr_experiment.current_question;
                do {
                    next_question++;
                } while (Questions.findOne({
                        "question_ID": next_question
                    }).busy == true);
            }
            if (counters[experiment_id_value]['random_counter'].length == selection_size) {
                Meteor.clearInterval(intervals[experiment_id_value]);
                intervals[experiment_id_value] = 0;
                Answers.update({
                    experiment_id: experiment_id_value
                }, {
                    $set: {
                        experiment_finished: true,
                        question_order: counters[experiment_id_value]['random_counter']
                    }
                }, {
                    upsert: true,
                    multi: true
                });
                Meteor.setTimeout(function() {
                    console.log("all questions passed for experiment " + experiment_id_value);
                }, 30);
            } else {
                //store result
                counters[experiment_id_value]['random_counter'][counters[experiment_id_value]['random_counter'].length] = next_question;

                // look at the number of participants who were assigned here previously.
                // this number does NOT include the participant just being assigned.
                var answer_field_query = {};
                answer_field_query["answer1." + next_question + ".1"] = {
                    "$exists": true
                };

                //var number_of_previous_participants = Answers.find(answer_field_query).count();
                //new way to calculate previous participants to handle the multiple averaging case
                previous_question_dict = Questions.findOne({
                    "question_ID": next_question
                });
                var number_of_previous_participants =  previous_question_dict.previous_participants;
                Questions.update({
                    "question_ID": next_question
                }, {
                    $set: {
                        "busy": false,
                    }
                });
                Answers.update({
                    "experiment_id": experiment_id_value
                }, {
                    $set: {
                        "num_of_previous_participants": number_of_previous_participants
                    }
                }, {
                    upsert: true,
                    multi: true
                });

                // Set the busy flag
                console.log("setting busy flag to " + next_question);
                if (next_question != 0) {
                    Questions.update({
                        "question_ID": next_question
                    }, {
                        $set: {
                            "busy": true
                        }
                    });
                    console.log('finding an averaging thing that is available');
                    question_dictionary = Questions.findOne({
                        "question_ID": next_question
                    });
                    current_avg_number = -1;
                    for (i = 0; i < question_dictionary['averaging_status_array'].length; i++) {
                        if (question_dictionary['averaging_status_array'][i] == "FREE") {
                            current_avg_number = i;
                            break;
                        }
                    }
                    question_dictionary['averaging_status_array'][current_avg_number] = "BUSY";
                    question_dictionary['busy'] = true;
                    for (i = 0; i < question_dictionary['averaging_status_array'].length; i++) {
                        if (question_dictionary['averaging_status_array'][i] == "FREE") {
                            question_dictionary['busy'] = false;
                            break;
                        }
                    }
                    Questions.update({
                        "question_ID": next_question
                    }, {
                        $set: question_dictionary
                    });
                    Answers.update({
                        "experiment_id": experiment_id_value
                    }, {
                        $set: {
                            "current_avg_number": current_avg_number
                        }
                    }, {
                        upsert: true,
                        multi: true
                    });
                }

                //Questions.update({"question_ID": next_question}, {$set: {"busy": true}});

                var radius_fn = function(previous_participants) {
                    //return 50.0/(Math.floor(previous_participants/10.0)+1);
                    return 35.0 / Math.max(1, Math.ceil((previous_participants) / 10.0) + 1.0);
                };
                var radius_val = radius_fn(Questions.findOne({
                    "question_ID": next_question
                }).previous_participants);
                if ([1, 2, 3, 4, 5, 6].indexOf(next_question) > -1) {
                    var current_question = Questions.findOne({
                        "question_ID": next_question
                    });
                    var db_storage = {};
                    for (var well_idx = 0; well_idx < 2; well_idx++) {
                        var total_money_spent = 0;
                        for (var slider_idx = 0; slider_idx < 4; slider_idx++) {
                            db_storage['initial_slider' + slider_idx + well_idx] = current_question['slider' + slider_idx + well_idx];
                            if (slider_idx != 3) {
                                // add everything but taxes
                                total_money_spent += current_question['slider' + slider_idx + well_idx];
                            } else {
                                // subtract the taxes
                                total_money_spent -= current_question['slider' + slider_idx + well_idx];
                            }
                        }
                        //compute the deficit
                        db_storage['initial_deficit' + well_idx] = total_money_spent + 162;
                    }
                    //store everything
                    Answers.update({
                        experiment_id: experiment_id_value
                    }, {
                        $set: db_storage
                    }, {
                        upsert: true,
                        multi: true
                    });

                }
                Answers.update({
                    experiment_id: experiment_id_value
                }, {
                    $set: {
                        current_question: next_question,
                        current_answer: 0,
                        "radius": radius_val,
                        latest_time: new Date().getTime()
                    }
                }, {
                    upsert: true,
                    multi: true
                });
                console.log("question for experiment " + experiment_id_value + " changed to " + next_question);
            }

        };

        decrease_time = function(experiment_id_value) {
            var curr_experiment = Answers.findOne({
                experiment_id: experiment_id_value
            });
            var curr_time = curr_experiment.timer;
            if (curr_time <= 0) {
                Meteor.clearInterval(timers[experiment_id_value]);
                timers[experiment_id_value] = 0;
            } else {
                Answers.update({
                    experiment_id: experiment_id_value
                }, {
                    $set: {
                        timer: curr_time - 1
                    }
                }, {
                    upsert: true,
                    multi: true
                });
            }
        };
        //always clear existing timers
        if (timers[experiment_id_value]) {
            Meteor.clearInterval(timers[experiment_id_value]);
            timers[experiment_id_value] = 0;
        }
        if (intervals[experiment_id_value]) {
            Meteor.clearTimeout(intervals[experiment_id_value]);
            intervals[experiment_id_value] = 0;
        }
        //always update timer
        var curr_answer_form = curr_experiment.current_answer;
        if (curr_answer_form < Meteor.settings.public.answer_forms.length - 1) {
          //Nikhil's understanding: question not done yet
            var next_answer_form = curr_answer_form + 1;
            Answers.update({
                experiment_id: experiment_id_value
            }, {
                $set: {
                    current_answer: next_answer_form,
                    latest_time: new Date().getTime()
                }
            }, {
                upsert: true,
                multi: true
            });
            counters[experiment_id_value][curr_experiment.current_question] = 0;
            //potentially removes the busy flag
            if (curr_answer_form == 1) {
              //Nikhil's comment: Potentially this is where I update the averaging status, do teh averaging, etc. TODO
                //remove the busy flag.
                console.log("removing busy flag from " + curr_experiment.current_question);
                current_question_dictionary = Questions.findOne({"question_ID": curr_experiment.current_question});
                if (wasTimedOut == 'false'){
                  current_question_dictionary.averaging_status_array[curr_experiment.current_avg_number] = 'DONE';
                  var alldone = true;
                  for (var i = 0; i < current_question_dictionary.averaging_status_array.length; i++){
                    if (current_question_dictionary.averaging_status_array[i] != 'DONE'){
                      alldone = false;
                    }
                  }
                  // c. If entire array has been filled (all are DONE)
                  //       i. Do the averaging
                  //       ii. set it to initial_value
                  //       iii. reset the array
                  //       iv. reset overall busy
                  //       v. increase "number_previous"

                  if (alldone){
                    for (var well_idx = 0; well_idx < 2; well_idx ++){
                      for (var slider_idx = 0; slider_idx < 4; slider_idx ++){
                        var sumval = 0.0;
                        for (var avgi = 0; avgi < current_question_dictionary.num_to_average; avgi++)
                        {
                          sumval = sumval + current_question_dictionary[averaging_array][avgi]['slider' + slider_idx + well_idx];
                        }
                        sumval = sumval / current_question_dictionary.num_to_average;
                        current_question_dictionary['slider' + slider_idx + well_idx] = sumval;
                      }
                    }
                    for (var avgi = 0; avgi < current_question_dictionary.num_to_average; avgi++){
                      current_question_dictionary.averaging_status_array[avgi] = 'FREE';
                    }
                    current_question_dictionary.busy = false;
                    current_question_dictionary.previous_participants = current_question_dictionary.previous_participants+1;
                  }
                }
                else{ //timed out rather than completed
                  //		a. Set averaging_status_array[current_avg_number] to FREE
		              //     b. reset overall busy
                  current_question_dictionary.averaging_status_array[curr_experiment.current_avg_number] = 'FREE';
                  current_question_dictionary.busy = false;
                }
                Questions.update({
                    "question_ID": curr_experiment.current_question
                }, {
                    $set: current_question_dictionary
                });
            }
        } else {
          //Nikhil's understanding: person has finished answering the question, including feedback
            //updates the question

            //award the payment to a group

            var current_question = curr_experiment.current_question;
            // if realtime computation
            var entries = Answers.find({
                experiment_id: experiment_id_value
            }).fetch();
            // else sort answers by descending experiment id, with a limit of threshold, use that as entries.
            var answer_array = [];

            entries.forEach(function(post) {
                answer_array[answer_array.length] = post.answer1;
            });
            if (current_question !== undefined) {
                Meteor.call(Meteor.settings.payment_function, answer_array, current_question, function(error, result) {
                    if (error) {
                        console.log("Error " + error + " while processing the payment function");
                    } else {
                        entries.forEach(function(post, index) {
                            //break up the array, assign payments individually
                            var payments_value = Answers.findOne({
                                worker_ID: post.worker_ID
                            }).payments;
                            //var existing_payments = existing_entry.payments;
                            if (!payments_value) {
                                //create new payments array
                                var payments_value = [];
                                for (i = 0; i < num_of_questions; i++) {
                                    payments_value[payments_value.length] = 0;
                                }
                            }
                            payments_value[current_question] = result[index];
                            var avg_payment_value = post.avg_payment + payments_value[current_question];
                            avg_payment_value = Math.round(avg_payment_value * 1000) / 1000;
                            Answers.update({
                                worker_ID: post.worker_ID
                            }, {
                                $set: {
                                    payments: payments_value,
                                    avg_payment: avg_payment_value
                                }
                            }, {
                                upsert: true
                            });
                        });
                    }
                });
            }

            update_question(experiment_id_value);
        }
        curr_experiment = Answers.findOne({
            experiment_id: experiment_id_value
        });
        var time_value = Meteor.settings.public.answer_forms[curr_experiment.current_answer].timer;
        if (time_value > 0 && !curr_experiment.experiment_finished) {
            //initiate a countdown
            Answers.update({
                experiment_id: experiment_id_value
            }, {
                $set: {
                    timer: time_value
                }
            }, {
                upsert: true,
                multi: true
            });
            timers[experiment_id_value] = Meteor.setInterval(function() {
                decrease_time(experiment_id_value);
            }, 1000);
            intervals[experiment_id_value] = Meteor.setTimeout(function() {
                Meteor.call('beginQuestionScheduler', experiment_id_value, 'true');
            }, time_value * 1000);
        }
    }

});
Meteor.methods({
    payment: function(existing_entry) {
        return;
    },
    payment123: function(answer_array, question_ID) {
        var payment_temp = [];
        for (var i = 0; i < answer_array.length; i++) {
            payment_temp[i] = 0.04 + i;
        }
        return payment_temp;
    }
});
