Template.experiment.events({
    'click #begin_experiment': function (event) {
        worker_ID_value = Session.get("worker_ID_value");
        Session.set('initialized', true);
        Session.set('waiting', true);
        Meteor.call('initialPost', {worker_ID: worker_ID_value, initial_time: initial_time_val}, 'begin', function(error, result){
            if (error){
                console.log("error "+error);
            } else {
                initial_time_val = new Date().getTime();
            }
        });

    },

    'click #more_instructions': function (event) {
        window.open('/more_instructions');
    },

    'click #answer_submission': function(event) {
        var answer_value = {};
        var form = $("form").children();
        //for checkboxes, radio buttons
        form.filter("label").children().filter(":checked").each(function(index, element){
            //append the values to the answer array
            if (!answer_value[$(element)[0].form.name]){
                answer_value[$(element)[0].form.name]= [$(element).val()];
            } else {
                answer_value[$(element)[0].form.name].push($(element).val());
            }
        });
        //for the button
        if (event.target.parentNode.name){
            answer_value[event.target.parentNode.name] = event.target.value;
        }
        //for textares
        form.filter("textarea").each(function(index, element){
            if ($(element).val() != " "){
                if (!answer_value[$(element).parent().attr('name')]){
                    answer_value[$(element).parent().attr('name')]= [$(element).val()];
                } else {
                    answer_value[$(element).parent().attr('name')].push($(element).val());
                }
            }
        });
        if (Object.keys(answer_value).length != $("form").length){
            alert("Please make sure to answer every question.");
            return;
        }
        worker_ID_value = Session.get('worker_ID_value');
        answer_value['time'] = new Date().getTime() - initial_time_val;
        Session.set("answered", true);
        Session.set("waiting", true);
        Meteor.call('newPost', {answer: answer_value, worker_ID: worker_ID_value}, function(error, result){
            if (error) {
                console.log("Error " + error + " occured. Please contact the administrators with the issue.");
            } else if (Answers.findOne({worker_ID: worker_ID_value}).experiment_finished){
                Session.set('experiment_finished', true);
                Router.go('/end');

            } else{
                Session.set('waiting', false);
            }
        });
    }

});
Template.experiment.helpers({
    questions: function() {
        worker_ID_value = Session.get('worker_ID_value');
        var curr_experiment = Answers.findOne({worker_ID: worker_ID_value});
        if (curr_experiment){
            //update average payment
            current_payment = curr_experiment.avg_payment;
            Session.set('current_payment', current_payment);
        }
        if (curr_experiment && (!Session.equals('current_question', curr_experiment.current_question))) {
            Session.set("current_question", curr_experiment.current_question);
            Session.set("waiting", false);
        } else {
            return Questions.find({question_ID: Session.get("current_question")});
        }
    }
});
Template.answer1.onRendered(function () {
    //initialize variables
    var curr_experiment = Answers.findOne({worker_ID: worker_ID_value});
    var radius = curr_experiment.radius;
    var current_question = Questions.findOne({"question_ID": curr_experiment.current_question});
    if (curr_experiment.current_question == 0) {
        var slider0_current = 0;
        if (current_question.slider0) {
            slider0_current = current_question.slider0;
        }
        var slider0_min = slider0_current - radius;
        var slider0_max = slider0_current + radius;
        Session.set('slider0', slider0_current);

        //noUiSlider.create(slider0, /* { options }
        slider0 = this.$("div#slider0").noUiSlider({
            start: slider0_current,
            connect: "lower",
            range: {
                'min': slider0_min,
                'max': slider0_max
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            Session.set('slider0', val);
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            Session.set('slider0', val);
        });
        var slider1_current = 0;
        if (current_question.slider1) {
            slider1_current = current_question.slider1;
        }
        var slider1_min = slider1_current - radius;
        var slider1_max = slider1_current + radius;
        Session.set('slider1', slider1_current);
        slider1 = this.$("div#slider1").noUiSlider({
            start: slider1_current,
            connect: "lower",
            range: {
                'min': slider1_min,
                'max': slider1_max
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            Session.set('slider1', val);
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            Session.set('slider1', val);
        });
        var slider2_current = 0;
        if (current_question.slider2) {
            slider2_current = current_question.slider2;
        }
        var slider2_min = slider2_current - radius;
        var slider2_max = slider2_current + radius;
        Session.set('slider2', slider2_current);
        slider2 = this.$("div#slider2").noUiSlider({
            start: slider2_current,
            connect: "lower",
            range: {
                'min': slider2_min,
                'max': slider2_max
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            Session.set('slider2', val);
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            Session.set('slider2', val);
        });
        var slider3_current = 0;
        if (current_question.slider3) {
            slider3_current = current_question.slider3;
        }
        var slider3_min = slider3_current - radius;
        var slider3_max = slider3_current + radius;
        Session.set('slider3', slider3_current);
        slider3 = this.$("div#slider3").noUiSlider({
            start: slider3_current,
            connect: "lower",
            range: {
                'min': slider3_min,
                'max': slider3_max
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            Session.set('slider3', val);
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            Session.set('slider3', val);
        });
        var slider4_current = 0;
        if (current_question.slider4) {
            slider4_current = current_question.slider4;
        }
        var slider4_min = slider4_current - radius;
        var slider4_max = slider4_current + radius;
        Session.set('slider4', slider4_current);
        slider4 = this.$("div#slider4").noUiSlider({
            start: slider4_current,
            connect: "lower",
            range: {
                'min': slider4_min,
                'max': slider4_max
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            Session.set('slider4', val);
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            Session.set('slider4', val);
        });
    }

});
Template.answer1.events({
   'change textarea': function(event){
       Session.set(event.target.id, (Number(event.target.value).toFixed(2)));
       eval(event.target.id).val(Number(event.target.value).toFixed(2));
    }
});

Template.question.helpers({
    istable: function(text){
        if (text.substring(0,6) == "In gen"){
            return true;
        } else {
            return false;
        }
    },
    isgradea: function(grade){
        if (grade == "an A"){
            return true;
        } else {
            return false;
        }
    },
    ismechrf: function(text){
        if (text.substring(10,11) == "5")
            return true;
        return false;
    }
});
