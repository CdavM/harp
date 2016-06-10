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
            console.log(answer_value);
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
    $("#creditsleft").text("Credits left: " + parseInt(Number(radius)*1000)/1000);
    update_slider1 = function (ev, val, update_slider_flag) {
        // the vars below are global and declared once the page is rendered!
        var curr_experiment = Answers.findOne({worker_ID: worker_ID_value});
        var radius = curr_experiment.radius;
        var current_question = Questions.findOne({"question_ID": curr_experiment.current_question});
        if (!update_slider_flag)
            update_slider_flag = false;
        var radius_sum = 0;
        var slider_idx_counter = 0;
        while (slider_idx_counter < 4){
            var curr_slider = "slider"+slider_idx_counter.toString();
            var curr_slider_value = Session.get(curr_slider);
            if (isNaN(curr_slider_value)){
                eval(ev.target.id).val((parseInt(Number(Session.get(ev.target.id))*100)/100).toFixed(2));
                return;
            }
            radius_sum = radius_sum + Math.pow((curr_slider_value - current_question[curr_slider]),2);
            slider_idx_counter ++;
        }
        //now subtract the radius for the current slider from radius sum
        radius_sum -= Math.pow((Session.get(ev.target.id)-current_question[ev.target.id]),2);
        //now see if new radius sum is bigger than radius
        if (radius_sum + Math.pow((val-current_question[ev.target.id]),2) > radius){
            //decrease the val until we can do it
            var rad_difference = Math.sqrt(radius-radius_sum);
            if (val > current_question[ev.target.id]){
                val = current_question[ev.target.id] + rad_difference;
            } else {
                val = current_question[ev.target.id] - rad_difference;
            }
            update_slider_flag = true;
            $("div").mouseup(); //release the mouse
        }
        if (isNaN(val)){
            eval(ev.target.id).val((parseInt(Number(Session.get(ev.target.id))*100)/100).toFixed(2));
            return;
        }
        ev.target.value = (parseInt(Number(val)*100)/100).toFixed(2); // updates the textbox
        Session.set(ev.target.id, Number(val));
        var radius_dif = radius - radius_sum;
        radius_dif -= Math.pow((val-current_question[ev.target.id]),2);
        radius_dif = radius_dif + 0.0001; //laplace smoothing
        radius_dif = (parseInt(Number(radius_dif)*1000)/1000).toFixed(3);
        $("#creditsleft").text("Credits left: " + radius_dif);
        if (update_slider_flag){
            eval(ev.target.id).val((parseInt(Number(val)*100)/100).toFixed(2));
        }
        //update stacked bars
        var slider_idx_counter = 0;
        var curr_slider_total_width = 0;
        var slider_laplace_smoothing = true;
        while (slider_idx_counter < 4){
            var curr_slider = "slider"+slider_idx_counter.toString();
            var curr_slider_value = Session.get(curr_slider);
            var curr_slider_bar = curr_slider + "bar";
            $("#" + curr_slider_bar).width((Math.pow((curr_slider_value - current_question[curr_slider]), 2) / radius) * $("#budgetbar").width()-0.1); //laplace smoothing
            curr_slider_total_width = curr_slider_total_width + $("#"+curr_slider_bar).width();
            slider_idx_counter ++;
        }
        var percent_difference = compute_averages(Number(ev.target.id.substr(ev.target.id.length-1)), val);
        if (percent_difference < 0){
            //red background
            $("#"+ev.target.id+"comp").css('color','red');
            // set value
            $("#"+ev.target.id+"comp").text(round(percent_difference, 2)+"%");
        } else {
            //green background
            $("#"+ev.target.id+"comp").css('color','green');
            // set value
            $("#"+ev.target.id+"comp").text("+"+round(percent_difference, 2)+"%");
        }
        var total_money_spent = 0;
        slider_idx_counter = 0;
        while (slider_idx_counter < 4){
            total_money_spent += Session.get("slider"+slider_idx_counter);
            slider_idx_counter++;
        }
        update_deficit();
    };
    update_slider_mech11 = function(ev, val){
        eval(ev.target.id).val(Number(Session.get(ev.target.id)).toFixed(2));
        $("div").mouseup(); //release the mouse
    };


    update_slider_mech21 = function (ev, val, update_slider_flag) {
        var curr_experiment = Answers.findOne({worker_ID: worker_ID_value});
        var current_question = Questions.findOne({"question_ID": curr_experiment.current_question});
        if (!update_slider_flag)
            var update_slider_flag = false;
        if (isNaN(val)){
            eval(ev.target.id).val(Number(Session.get(ev.target.id)).toFixed(2));
            return;
        }
        ev.target.value = Number(val).toFixed(2); // updates the textbox
        Session.set(ev.target.id, Number(val));
        if (update_slider_flag){
            eval(ev.target.id).val(Number(val).toFixed(2));
            $("div").mouseup(); //release the mouse
        }
        var percent_difference = compute_averages(Number(ev.target.id.substr(ev.target.id.length-1)), val);
        if (percent_difference < 0){
            //red background
            $("#"+ev.target.id+"comp").css('color','red');
            // set value
            $("#"+ev.target.id+"comp").text(round(percent_difference, 2)+"%");
        } else {
            //green background
            $("#"+ev.target.id+"comp").css('color','green');
            // set value
            $("#"+ev.target.id+"comp").text("+"+round(percent_difference, 2)+"%");
        }
        var total_money_spent = 0;
        slider_idx_counter = 0;
        while (slider_idx_counter < 4){
            total_money_spent += Session.get("slider"+slider_idx_counter);
            slider_idx_counter++;
        }
        update_deficit();
    };
    var update_weight_slider1 = function(ev, val, update_slider_flag){
        var curr_experiment = Answers.findOne({worker_ID: worker_ID_value});
        var current_question = Questions.findOne({"question_ID": curr_experiment.current_question});
        if (!update_slider_flag)
            var update_slider_flag = false;
        if (isNaN(val)){
            eval(ev.target.id).val(Number(Session.get(ev.target.id)).toFixed(2));
            return;
        }
        ev.target.value = Number(val).toFixed(2); // updates the textbox
        Session.set(ev.target.id, Number(val));
        if (update_slider_flag){
            eval(ev.target.id).val(Number(val).toFixed(2));
            $("div").mouseup(); //release the mouse
        }
    };
    var compute_averages = function(slider_ID, value){
        var ratio = 0;
        if (slider_ID == 0){
            ratio = value / 541; //TODO update with real values
        } else if (slider_ID == 1){
            ratio = value / 1004;
        } else if (slider_ID == 2){
            ratio = value / 149;
        } else if (slider_ID == 3){
            ratio = value / 1460;
        }
        percentage_difference = 100 * (ratio - 1);
        return percentage_difference;
    };
    var update_deficit = function(well_idx){
        if (typeof(well_idx) == "undefined"){
            var well_idx = "";
        }
        var total_money_spent = 0;
        slider_idx_counter = 0;
        while (slider_idx_counter < 4){
            total_money_spent += Session.get("slider"+slider_idx_counter+well_idx);
            slider_idx_counter++;
        }
        var deficit_value = total_money_spent - 2604; //TODO: update with real numbers
        var deficit_value_percentage = 100 * ((deficit_value / 550) - 1); //TODO: update with real numbers
        deficit_value = parseInt(deficit_value * 100)/100;
        if (deficit_value >= 0){
            $("#deficit_text"+well_idx).text("deficit");
            $("#deficit_value"+well_idx).css('color','red');
        } else {
            deficit_value = deficit_value.toString().substr(1);
            $("#deficit_text"+well_idx).text("surplus");
            $("#deficit_value"+well_idx).css('color','green');
        }
        if (deficit_value_percentage >= 0){
            deficit_value_percentage = (parseInt(deficit_value_percentage*100)/100).toString();
            $("#deficit_percentage"+well_idx).css('color','red');
        } else {
            deficit_value_percentage = (parseInt(deficit_value_percentage*100)/100).toString();
            $("#deficit_percentage"+well_idx).css('color','green');
        }
        $("#deficit_value"+well_idx).text("$"+deficit_value+"B");
        $("#deficit_percentage"+well_idx).text(deficit_value_percentage);

    };
    var update_comps = function(){
        var percentage_difference = 0;
        for (var slider_idx = 0; slider_idx < 4; slider_idx++){
            percentage_difference = compute_averages(slider_idx, Session.get("slider"+slider_idx));
            if (percentage_difference < 0){
                //red background
                $("#"+"slider"+slider_idx+"comp").css('color','red');
                // set value
                $("#"+"slider"+slider_idx+"comp").text(Number(percentage_difference).toFixed(2)+"%");
            } else {
                //green background
                $("#"+"slider"+slider_idx+"comp").css('color','green');
                // set value
                $("#"+"slider"+slider_idx+"comp").text("+"+Number(percentage_difference).toFixed(2)+"%");
            }
        }
    };
    update_slider = _.throttle(update_slider1, 100);
    update_weight_slider = _.throttle(update_weight_slider1, 100);
    update_slider_mech2 = _.throttle(update_slider_mech21, 100);
    update_slider_mech1 = _.throttle(update_slider_mech11, 100);

    if (curr_experiment.current_question == 0) {
        var slider0_current = 0;
        if (current_question.slider0) {
            slider0_current = current_question.slider0;
        }
        var slider0_min = slider0_current - Math.sqrt(radius)*1.25;
        var slider0_max = slider0_current + Math.sqrt(radius)*1.25;
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
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        });
        var slider1_current = 0;
        if (current_question.slider1) {
            slider1_current = current_question.slider1;
        }
        var slider1_min = slider1_current - Math.sqrt(radius)*1.25;
        var slider1_max = slider1_current + Math.sqrt(radius)*1.25;
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
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        });
        var slider2_current = 0;
        if (current_question.slider2) {
            slider2_current = current_question.slider2;
        }
        var slider2_min = slider2_current - Math.sqrt(radius)*1.25;
        var slider2_max = slider2_current + Math.sqrt(radius)*1.25;
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
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        });
        var slider3_current = 0;
        if (current_question.slider3) {
            slider3_current = current_question.slider3;
        }
        var slider3_min = slider3_current - Math.sqrt(radius)*1.25;
        var slider3_max = slider3_current + Math.sqrt(radius)*1.25;
        Session.set('slider3', slider3_current);
        for (var slider_idx = 0; slider_idx < 4; slider_idx++) {
            $("#slider"+slider_idx+"min").text("$"+eval("slider"+slider_idx+"_min").toFixed(2)+"B");
            $("#slider"+slider_idx+"cur").text("$"+eval("slider"+slider_idx+"_current").toFixed(2)+"B");
            $("#slider"+slider_idx+"max").text("$"+eval("slider"+slider_idx+"_max").toFixed(2)+"B");
        }
        slider3 = this.$("div#slider3").noUiSlider({
            start: slider3_current,
            connect: "lower",
            range: {
                'min': slider3_min,
                'max': slider3_max
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider(ev, val);
            } catch (TypeError){
            }
        });
        //update comps
        update_comps();
        //update the deficit text
        update_deficit();


    } else if (curr_experiment.current_question == 1){
        //mechanism 1 specific js
        //initialize all 15 sliders in one loop!
        var slider_idx = 0;
        var well_idx = 0;
        while(slider_idx<4){
            while(well_idx<3){
                window["slider"+slider_idx+well_idx] = this.$("div#slider"+slider_idx+well_idx).noUiSlider({
                    start: current_question["slider"+slider_idx+"1"],
                    connect: "lower",
                    range: {
                        'min': current_question["slider"+slider_idx+"1"] - Math.sqrt(radius)*1.25,
                        'max': current_question["slider"+slider_idx+"1"] + Math.sqrt(radius)*1.25
                    }
                }).on('slide', function (ev, val) {
                    // set real values on 'slide' event
                    try {
                        update_slider_mech1(ev, val);
                    } catch (TypeError){
                    }
                }).on('change', function (ev, val) {
                    // round off values on 'change' event
                    try {
                        update_slider_mech1(ev, val);
                    } catch (TypeError){
                    }
                });
                $("#slider"+slider_idx+well_idx).val(current_question["slider"+slider_idx+well_idx]);
                Session.set('slider'+slider_idx+well_idx, current_question["slider"+slider_idx+well_idx]);
                //display set value
                $("#slider"+slider_idx+well_idx+"_text").text("$"+current_question["slider"+slider_idx+well_idx].toFixed(3)+"B");
                //display comparison to 2016 estimates
                var percentage_difference = compute_averages(slider_idx, Session.get("slider"+slider_idx+well_idx));
                if (percentage_difference < 0){
                    //red background
                    $("#slider"+slider_idx+well_idx+"comp").css('color','red');
                    // set value
                    $("#slider"+slider_idx+well_idx+"comp").text(Number(percentage_difference).toFixed(2)+"%");
                } else {
                    //green background
                    $("#slider"+slider_idx+well_idx+"comp").css('color','green');
                    // set value
                    $("#slider"+slider_idx+well_idx+"comp").text("+"+Number(percentage_difference).toFixed(2)+"%");
                }
                //display min, cur and max values
                $("#slider"+slider_idx+well_idx+"min").text("$"+(current_question["slider"+slider_idx+"1"]- Math.sqrt(radius)*1.25).toFixed(2)+"B");
                $("#slider"+slider_idx+well_idx+"cur").text("$"+(current_question["slider"+slider_idx+"1"]).toFixed(2)+"B");
                $("#slider"+slider_idx+well_idx+"max").text("$"+(current_question["slider"+slider_idx+"1"]+ Math.sqrt(radius)*1.25).toFixed(2)+"B");
                well_idx ++;
            }
            slider_idx++;
            well_idx = 0;
        }
        for (well_idx = 0; well_idx < 3; well_idx++){
            update_deficit(well_idx);
        }
    } else if (curr_experiment.current_question == 2){
        //mechanism 2 specific js
        var slider0_current = 0;
        if (current_question.slider0) {
            slider0_current = current_question.slider0;
        }
        var slider1_current = 0;
        if (current_question.slider1) {
            slider1_current = current_question.slider1;
        }
        var slider2_current = 0;
        if (current_question.slider2) {
            slider2_current = current_question.slider2;
        }
        var slider3_current = 0;
        if (current_question.slider3) {
            slider3_current = current_question.slider3;
        }
        var slider_vals = {};
        for (var slider_idx = 0; slider_idx < 4; slider_idx++) {
            slider_vals["slider" + slider_idx + "_min"] = 0;
            slider_vals["slider" + slider_idx + "_max"] = 4 * eval("slider" + slider_idx + "_current");
        }
        Session.set('slider0', slider0_current);
        //noUiSlider.create(slider0, /* { options }
        slider0 = this.$("div#slider0").noUiSlider({
            start: slider0_current,
            connect: "lower",
            range: {
                'min': slider_vals["slider0_min"],
                'max': slider_vals["slider0_max"]
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        });
        Session.set('slider1', slider1_current);
        slider1 = this.$("div#slider1").noUiSlider({
            start: slider1_current,
            connect: "lower",
            range: {
                'min': slider_vals["slider1_min"],
                'max': slider_vals["slider1_max"]
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        });
        Session.set('slider2', slider2_current);
        slider2 = this.$("div#slider2").noUiSlider({
            start: slider2_current,
            connect: "lower",
            range: {
                'min': slider_vals["slider2_min"],
                'max': slider_vals["slider2_max"]
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        });
        Session.set('slider3', slider3_current);
        for (var slider_idx = 0; slider_idx < 4; slider_idx++) {
            $("#slider"+slider_idx+"min").text("$"+slider_vals["slider"+slider_idx+"_min"].toFixed(2)+"B");
            $("#slider"+slider_idx+"cur").text("$"+eval("slider"+slider_idx+"_current").toFixed(2)+"B");
            $("#slider"+slider_idx+"max").text("$"+slider_vals["slider"+slider_idx+"_max"].toFixed(2)+"B");
        }
        slider3 = this.$("div#slider3").noUiSlider({
            start: slider3_current,
            connect: "lower",
            range: {
                'min': slider_vals["slider3_min"],
                'max': slider_vals["slider3_max"]
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_slider_mech2(ev, val);
            } catch (TypeError){
            }
        });
        //WEIGHT SLIDERS
        Session.set('slider0weight', 5);
        Session.set('slider1weight', 5);
        Session.set('slider2weight', 5);
        Session.set('slider3weight', 5);
        $("p#sliderwmin").text(0);
        $("p#sliderwcur").text(5);
        $("p#sliderwmax").text(10);

        slider0w = this.$("div#slider0weight").noUiSlider({
            start: 5,
            connect: "lower",
            range: {
                'min': 0,
                'max': 10
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        });
        slider1w = this.$("div#slider1weight").noUiSlider({
            start: 5,
            connect: "lower",
            range: {
                'min': 0,
                'max': 10
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        });
        slider2w = this.$("div#slider2weight").noUiSlider({
            start: 5,
            connect: "lower",
            range: {
                'min': 0,
                'max': 10
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        });
        slider3w = this.$("div#slider3weight").noUiSlider({
            start: 5,
            connect: "lower",
            range: {
                'min': 0,
                'max': 10
            }
        }).on('slide', function (ev, val) {
            // set real values on 'slide' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        }).on('change', function (ev, val) {
            // round off values on 'change' event
            try {
                update_weight_slider(ev, val);
            } catch (TypeError){
            }
        });
        //update comps
        update_comps();
        //update the deficit text
        update_deficit();
    }

});
Template.mechanism0.events({
    'change textarea': function(event){
        update_slider(event, event.target.value, true);
    }
});
Template.mechanism2.events({
    'change textarea': function(event){
        update_slider_mech2(event, event.target.value, true);
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
