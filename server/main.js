//This code only executed on the server

Meteor.publish("answers", function(){return Answers.find()});
Meteor.publish("questions", function(){return Questions.find()});
Solutions = new Mongo.Collection("solutions");
Meteor.publish("answerforms", function(){return AnswerForms.find()});
intervals = {};
counters = {};
timers = {};

threshold = Meteor.settings.threshold_workers; //we need at least threshold users in every experiment
experiment_id_counter = 1;

existing_experiment_counter = 0;
if (Answers.findOne({begin_experiment: true})){
    existing_experiment_counter = Answers.find({begin_experiment: true}, {sort: {experiment_id:-1}, limit:1}).fetch();
    experiment_id_counter = existing_experiment_counter[0].experiment_id + 1;
}


Meteor.startup(function(){
    clear_busy_flags:{
        Questions.update({},{$set:{'busy': false}}, {multi: true});
    }
    /*
    //check and potentially update question database
    update_questions:{
        for(post in Meteor.settings.questions){
            if(!Questions.findOne(Meteor.settings.questions[post]) || Questions.find().count() != Meteor.settings.questions.length){
                console.log("Updating questionbank database");
                Questions.remove({});
                for(post in Meteor.settings.questions){
                    Questions.insert(Meteor.settings.questions[post]);
                }
                break update_questions;
            }
        }
    }
    //check and potentially update answer_forms

    update_answer_forms:{
        for(post in Meteor.settings.public.answer_forms){
            if(!AnswerForms.findOne(Meteor.settings.public.answer_forms[post]) || AnswerForms.find().count() != Meteor.settings.public.answer_forms.length){
                console.log("Updating answer form database");
                AnswerForms.remove({});
                for(post in Meteor.settings.public.answer_forms){
                    AnswerForms.insert(Meteor.settings.public.answer_forms[post]);
                }
                break update_answer_forms;
            }
        }
    }
    */
});

Meteor.methods({
    initialPost: function(post, status){
        //check if already present
        if (status == 'startup'){
            if (Answers.findOne({worker_ID: post.worker_ID})){
                return;
            }
            var initial_time_val = new Date().getTime();
            Answers.insert({worker_ID: post.worker_ID, asg_ID: post.asg_ID, hit_ID: post.hit_ID, initial_time: initial_time_val, latest_time: initial_time_val});
            return;
        } else {
            var experiment_id_value = experiment_id_counter;
            var begin_time_val = new Date().getTime();
            Answers.update({worker_ID: post.worker_ID}, {$set: {begin_time: begin_time_val, experiment_id: experiment_id_value,
                avg_payment:0, experiment_finished:false, latest_time: begin_time_val}});
        }

        if (counters[experiment_id_value]){
            counters[experiment_id_value]['initial_counter']++;
        } else {
            counters[experiment_id_value]={};
            counters[experiment_id_value]['initial_counter']=1;
            counters[experiment_id_value]['initial_timer']=true;
            //set timeout, also cancel a flag
            //TODO: implement automatic start
        }
        if (!counters[experiment_id_value]['random_counter']){
            counters[experiment_id_value]['random_counter'] = [];
        }


        if (counters[experiment_id_value]['initial_timer'] && counters[experiment_id_value]['initial_counter'] >= threshold){ //call this when we get two entries
            experiment_id_counter++;
            Answers.update({experiment_id: experiment_id_value}, {$set:{begin_experiment: true}}, {upsert: true, multi: true});
            Meteor.call('beginQuestionScheduler', experiment_id_value);
            counters[experiment_id_value]['initial_timer']=false;
        }
    },

    newPost: function(post) {
        //format time to UTC human readable format
        post.initial_time = new Date(post.initial_time).toLocaleString();
        var existing_entry = Answers.findOne({worker_ID: post.worker_ID});
        var answers_value = {};
        var experiment_id_value = existing_entry.experiment_id;
        if (existing_entry.answer1){
            //worker has submitted some answers, retrieve them
            answers_value = existing_entry.answer1;
        }
        var current_question = existing_entry.current_question;
        var current_answer = existing_entry.current_answer;
        //check if the user has answered the question already
        if (!answers_value[current_question]){
            answers_value[current_question] = {};
        }
        post.answer['time'] = new Date().getTime() - existing_entry.latest_time;
        answers_value[current_question][current_answer] = post.answer;

        var fields_to_be_updated = {};
        var total_money_spent = 0;
        for (var slider_idx = 0; slider_idx < 4; slider_idx++){
            if (post.answer['slider' + slider_idx]){
                fields_to_be_updated['slider'+slider_idx] = Number(post.answer['slider' + slider_idx][0]);
                if (slider_idx == 3) {
                    total_money_spent -= Number(post.answer['slider' + slider_idx][0]);
                } else {
                    total_money_spent += Number(post.answer['slider' + slider_idx][0]);
                }
                var slider_difference = Number(post.answer['slider' + slider_idx][0]) - existing_entry['initial_slider'+slider_idx];
                var slider_relative_diff = slider_difference / existing_entry['radius'];
                if (current_question == 0) {
                    answers_value['slider' + slider_idx + "_credits"] = Math.pow(slider_relative_diff, 2);
                } else if (current_question == 3) {
                    answers_value['slider' + slider_idx + "_credits"] = Math.abs(slider_relative_diff);
                }
            }
            if (post.answer['option']){
                // only for the comparison mechanism.
                var option_selected = post.answer['option'][0];
                var question_entry = Questions.findOne({"question_ID": current_question});
                fields_to_be_updated['slider'+slider_idx+'1'] = question_entry['slider'+slider_idx+option_selected];
                if (slider_idx == 3) {
                    // subtract taxes
                    total_money_spent -= question_entry['slider'+slider_idx+option_selected];
                } else {
                    // add everything else.
                    total_money_spent += question_entry['slider'+slider_idx+option_selected];
                }
            }
        }
        if (Object.keys(fields_to_be_updated).length && typeof(current_question) == "number" && current_question != 2) {
            Questions.update({"question_ID": current_question}, {$set: fields_to_be_updated}, {multi: true});
        }
        // add the deficit term
        if (current_question != 2 && current_answer == 1) {
            answers_value[current_question][current_answer]['deficit'] = total_money_spent + 316;
        }
        //Add entry to Answers
        Answers.update({worker_ID: post.worker_ID}, {$set: {answer1: answers_value}}, {upsert: true});
        //update question when we get ALL the answers
        if (counters[experiment_id_value][current_question]){
            counters[experiment_id_value][current_question]++;
        } else {
            counters[experiment_id_value][current_question]=1;
        }
        var num_of_workers = Meteor.settings.threshold_workers;
        if (counters[experiment_id_value][current_question] >= num_of_workers){
            Meteor.call('beginQuestionScheduler', experiment_id_value);
        }

    },
    submitFeedback: function(worker_ID_value, feedback_value){
        if (typeof worker_ID_value === 'undefined' || !worker_ID_value || typeof feedback_value === 'undefined' || !feedback_value){
            return;
        }
        Answers.update({worker_ID: worker_ID_value}, {$set:{feedback: feedback_value}}, {upsert:true});
        console.log("Feedback inserted for worker "+ worker_ID_value);
    },

    beginQuestionScheduler: function(experiment_id_value){
        //update questions every duration seconds
        var curr_experiment = Answers.findOne({experiment_id: experiment_id_value});
        var num_of_questions = Questions.find().count();
        update_question = function(experiment_id_value){
            var curr_experiment = Answers.findOne({experiment_id: experiment_id_value});
            if (!curr_experiment){
                console.log("experiment_id " + experiment_id_value + " not found in the database");
                return;
            }
            var num_of_questions = Questions.find().count();
            var selection_size = num_of_questions;
            if (Meteor.settings.questions_subset_size){
                selection_size = Math.min(num_of_questions,Meteor.settings.questions_subset_size);
            }
            var next_question = -1;
            if(Meteor.settings.randomize_questions){
                //generate random question
                do{
                    next_question = Math.floor(Math.random() * (num_of_questions));
                } while ((counters[experiment_id_value]['random_counter'].indexOf(next_question) != -1
                && counters[experiment_id_value]['random_counter'].length < selection_size)
                    || Questions.findOne({"question_ID": next_question}).busy == true);
                console.log("selected question " + next_question);
            } else {
                next_question = curr_experiment.current_question;
                do {
                    next_question ++;
                } while (Questions.findOne({"question_ID": next_question}).busy == true);
            }
            if (curr_experiment.current_question != null){

                //find number of previous participants
            }
            // look at the number of participants who were assigned here previously.
            // this number does NOT include the participant just being assigned.
            var answer_field_query = {};
            answer_field_query["answer1." + next_question+".1"] = {"$exists": true};
            var number_of_previous_participants = Answers.find(answer_field_query).count();
            Questions.update({"question_ID": next_question}, {$set:{"busy":false, "previous_participants": number_of_previous_participants}});
            Answers.update({"experiment_id": experiment_id_value}, {$set:{"num_of_previous_participants": number_of_previous_participants}}, {upsert: true, multi: true});
            if (counters[experiment_id_value]['random_counter'].length == selection_size){
                Meteor.clearInterval(intervals[experiment_id_value]);
                intervals[experiment_id_value]=0;
                Answers.update({experiment_id: experiment_id_value}, {$set:{experiment_finished: true, question_order: counters[experiment_id_value]['random_counter']}}, {upsert: true, multi: true});
                Meteor.setTimeout(function(){console.log("all questions passed for experiment " + experiment_id_value);},30);
            } else {
                //store result
                counters[experiment_id_value]['random_counter'][counters[experiment_id_value]['random_counter'].length]= next_question;
                // only questions 0, 1 and 3 can be busy!
                if (next_question != 2){
                    //set the busy flag.
                    console.log("setting busy flag to " + next_question);
                    Questions.update({"question_ID": next_question}, {$set: {"busy": true}});
                }
                var radius_fn = function (previous_participants) {
                    return 100/(previous_participants+1); //TODO update radius function
                };
                var radius_val = radius_fn(Questions.findOne({"question_ID": next_question}).previous_participants);
                if (next_question == 0 || next_question == 3){
                    var current_question = Questions.findOne({"question_ID": next_question});
                    var db_storage = {};
                    var total_money_spent = 0;
                    for (var slider_idx = 0; slider_idx < 4; slider_idx++){
                        db_storage['initial_slider'+slider_idx] = current_question['slider'+slider_idx];
                        if (slider_idx != 3) {
                            // add everything but taxes
                            total_money_spent += current_question['slider'+slider_idx];
                        } else {
                            // subtract the taxes
                            total_money_spent -= current_question['slider'+slider_idx];
                        }
                    }
                    //compute the deficit
                    db_storage['initial_deficit'] = total_money_spent + 316;
                    //store everything
                    Answers.update({experiment_id: experiment_id_value}, {$set: db_storage}, {upsert: true, multi: true});

                } else if (next_question == 1){
                    //vector generating function
                    var generate_point_on_surface_ball = function(num_of_dimensions){
                        //ball always has unit radius!
                        if (!num_of_dimensions) {
                            num_of_dimensions = 4; // default choice is 4
                        }
                        do {
                            var dimension_counter = 0;
                            var length_of_vector = 0;
                            var vector = [];
                            while (dimension_counter < num_of_dimensions){
                                //generate point by point
                                vector[dimension_counter] = 2*Math.random() - 1;
                                length_of_vector += Math.pow(vector[dimension_counter],2);
                                dimension_counter++;
                            }
                        } while (length_of_vector > 1);
                        length_of_vector = Math.sqrt(length_of_vector);
                        //scale the vector to unit norm
                        dimension_counter = 0;
                        while (dimension_counter < num_of_dimensions){
                            vector[dimension_counter] = round(vector[dimension_counter]/length_of_vector,3);
                            dimension_counter++;
                        }
                        return vector;
                    };
                    //generate two vectors on unit ball
                    var sampled_vector_0 = generate_point_on_surface_ball(4);
                    var sampled_vector_2 = generate_point_on_surface_ball(4);

                    var current_question = Questions.findOne({"question_ID": next_question});

                    var vector_object = {};
                    for (var slider_idx =0; slider_idx < 4; slider_idx++){
                        vector_object["slider"+slider_idx+"1"] = current_question["slider"+slider_idx+"1"];
                    }
                    for (slider_idx=0; slider_idx < 4; slider_idx++){
                        vector_object["slider"+slider_idx+"0"] = vector_object["slider"+slider_idx+"1"] +
                            sampled_vector_0[slider_idx]*(radius_val);
                        vector_object["slider"+slider_idx+"2"] = vector_object["slider"+slider_idx+"1"] +
                            sampled_vector_2[slider_idx]*(radius_val);
                    }
                    var compute_deficit = function (well_idx) {
                        if (typeof(well_idx) == "undefined"){
                            well_idx = "";
                        }
                        var total_money_spent = 0;
                        for (var slider_idx_counter = 0; slider_idx_counter < 3; slider_idx_counter++){
                            total_money_spent += vector_object["slider"+slider_idx_counter+well_idx];
                        }
                        total_money_spent -= vector_object["slider"+slider_idx_counter+well_idx]; // decreases by amt of income tax collected
                        var deficit_value = total_money_spent + 316; 
                        return deficit_value;
                    };

                    for (well_idx=0; well_idx < 3; well_idx++) {
                        vector_object['slider'+4+well_idx] = compute_deficit(well_idx);
                    }
                    //assign
                    Questions.update({"question_ID": next_question}, {$set:vector_object}, {upsert:true});
                    Answers.update({experiment_id: experiment_id_value}, {$set: vector_object}, {upsert: true, multi: true});
                }
                Answers.update({experiment_id: experiment_id_value}, {$set: {current_question: next_question, current_answer: 0, "radius":radius_val, latest_time: new Date().getTime()}}, {upsert: true, multi: true});
                console.log("question for experiment " + experiment_id_value + " changed to " + next_question);
            }

        };

        decrease_time = function(experiment_id_value) {
            var curr_experiment = Answers.findOne({experiment_id: experiment_id_value});
            var curr_time = curr_experiment.timer;
            if (curr_time <= 0){
                Meteor.clearInterval(timers[experiment_id_value]);
                timers[experiment_id_value] = 0;
            } else {
                Answers.update({experiment_id: experiment_id_value}, {$set: {timer: curr_time-1}}, {upsert: true, multi: true});
            }
        };
        //always clear existing timers
        if (timers[experiment_id_value]){
            Meteor.clearInterval(timers[experiment_id_value]);
            timers[experiment_id_value] = 0;
        }
        if (intervals[experiment_id_value]){
            Meteor.clearTimeout(intervals[experiment_id_value]);
            intervals[experiment_id_value] = 0;
        }
        //always update timer
        var curr_answer_form = curr_experiment.current_answer;
        if (curr_answer_form < Meteor.settings.public.answer_forms.length - 1){
            var next_answer_form = curr_answer_form + 1;
            Answers.update({experiment_id: experiment_id_value}, {$set: {current_answer: next_answer_form, latest_time: new Date().getTime()}}, {upsert:true, multi: true});
            counters[experiment_id_value][curr_experiment.current_question] = 0;
            //potentially removes the busy flag
            if (curr_answer_form == 1){
                //remove the busy flag.
                console.log("removing busy flag from " + curr_experiment.current_question);
                Questions.update({"question_ID": curr_experiment.current_question}, {$set:{"busy":false}});
            }
        } else {
            //updates the question

            //award the payment to a group

            var current_question = curr_experiment.current_question;
            // if realtime computation
            var entries = Answers.find({experiment_id: experiment_id_value}).fetch();
            // else sort answers by descending experiment id, with a limit of threshold, use that as entries.
            var answer_array = [];

            entries.forEach(function(post){
                answer_array[answer_array.length] = post.answer1;
            });
            if (current_question !== undefined){
                Meteor.call(Meteor.settings.payment_function, answer_array, current_question, function(error, result){
                    if (error){
                        console.log("Error " + error + " while processing the payment function");
                    } else {
                        entries.forEach(function(post, index){
                            //break up the array, assign payments individually
                            var payments_value = Answers.findOne({worker_ID: post.worker_ID}).payments;
                            //var existing_payments = existing_entry.payments;
                            if (!payments_value){
                                //create new payments array
                                var payments_value = [];
                                for (i = 0; i < num_of_questions; i++) {
                                    payments_value[payments_value.length] = 0;
                                }
                            }
                            payments_value[current_question] = result[index];
                            var avg_payment_value = post.avg_payment + payments_value[current_question];
                            avg_payment_value = Math.round(avg_payment_value*1000)/1000;
                            Answers.update({worker_ID: post.worker_ID}, {$set: {payments: payments_value,
                                avg_payment: avg_payment_value}}, {upsert: true});
                        })
                    }
                });
            }

            update_question(experiment_id_value);
        }
        curr_experiment = Answers.findOne({experiment_id: experiment_id_value});
        var time_value = Meteor.settings.public.answer_forms[curr_experiment.current_answer].timer;
        if (time_value > 0 && !curr_experiment.experiment_finished){
            //initiate a countdown
            Answers.update({experiment_id: experiment_id_value}, {$set: {timer: time_value}}, {upsert:true, multi: true});
            timers[experiment_id_value] = Meteor.setInterval(function(){decrease_time(experiment_id_value);}, 1000);
            intervals[experiment_id_value] = Meteor.setTimeout(function(){Meteor.call('beginQuestionScheduler', experiment_id_value);}, time_value*1000);
        }
    }

});
Meteor.methods({
    payment: function(existing_entry){
        return;
    },
    payment123: function(answer_array, question_ID){
        var payment_temp = [];
        for (var i = 0; i < answer_array.length; i++) {
            payment_temp[i] = 0.04+i;
        }
        return payment_temp;
    }
});