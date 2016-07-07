Template.experiment.events({
    'click #begin_experiment': function (event) {
        worker_ID_value = Session.get("worker_ID_value");
        Session.set('initialized', true);
        Session.set('waiting', true);
        Meteor.call('initialPost', {worker_ID: worker_ID_value}, 'begin', function(error, result){
            if (error){
                console.log("error "+error);
            } else {
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
    //$("#creditsleft").text("Credits left: " + round(radius,1)); disabled since we always start with 100 credits.
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
                sliders[ev.target.id].val(round(Session.get(ev.target.id), 2));
                return;
            }
            radius_sum = radius_sum + Math.pow((curr_slider_value - current_question[curr_slider]),2);
            slider_idx_counter ++;
        }
        //now subtract the radius for the current slider from radius sum
        radius_sum -= Math.pow((Session.get(ev.target.id)-current_question[ev.target.id]),2);
        //now see if new radius sum is bigger than radius
        if (radius_sum + Math.pow((val-current_question[ev.target.id]),2) > Math.pow(radius,2)){
            //decrease the val until we can do it
            var rad_difference = Math.sqrt(Math.pow(radius,2)-radius_sum);
            if (val > current_question[ev.target.id]){
                val = current_question[ev.target.id] + rad_difference;
            } else {
                val = current_question[ev.target.id] - rad_difference;
            }
            update_slider_flag = true;
            $("div").mouseup(); //release the mouse
        }
        if (isNaN(val)){
            sliders[ev.target.id].val(round(Session.get(ev.target.id), 2));
            return;
        }
        ev.target.value = round(val, 2); // updates the textbox
        Session.set(ev.target.id, Number(val));
        if (update_slider_flag){
            sliders[ev.target.id].val(round(val, 2));
        }
        //update stacked bars
        var slider_idx_counter = 0;
        var curr_slider_total_width = 0;
        var credit_percentage_spent = 0;
        var slider_laplace_smoothing = true;
        while (slider_idx_counter < 4){
            var curr_slider = "slider"+slider_idx_counter.toString();
            var curr_slider_value = Session.get(curr_slider);
            var curr_slider_bar = curr_slider + "bar";
            var slider_width_fraction = (Math.pow((curr_slider_value - current_question[curr_slider]), 2) / Math.pow(radius,2));
            credit_percentage_spent += slider_width_fraction;
            $("#" + curr_slider_bar).width(slider_width_fraction * $("#budgetbar").width()-0.3); //laplace smoothing
            $("#" + curr_slider_bar).text(round(slider_width_fraction*100, 1));
            curr_slider_total_width = curr_slider_total_width + $("#"+curr_slider_bar).width();
            slider_idx_counter ++;
        }
        var credits_left_fraction = 100*(1-credit_percentage_spent);
        if (credits_left_fraction < 0.15){
            credits_left_fraction = 0;
        }
        $("#creditsleft").text("Credits left: " + round(credits_left_fraction, 1));

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
    update_slider_mech31 = function (ev, val, update_slider_flag) {
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
                sliders[ev.target.id].val(round(Session.get(ev.target.id), 2));
                return;
            }
            radius_sum = radius_sum + Math.abs(curr_slider_value - current_question[curr_slider]);
            slider_idx_counter ++;
        }
        //now subtract the radius for the current slider from radius sum
        radius_sum -= Math.abs(Session.get(ev.target.id)-current_question[ev.target.id]);
        //now see if new radius sum is bigger than radius
        if (radius_sum + Math.abs(val-current_question[ev.target.id]) > radius) {
            //decrease the val until we can do it
            var rad_difference = Math.abs(radius-radius_sum);
            if (val > current_question[ev.target.id]){
                val = current_question[ev.target.id] + rad_difference;
            } else {
                val = current_question[ev.target.id] - rad_difference;
            }
            update_slider_flag = true;
            $("div").mouseup(); //release the mouse
        }
        if (isNaN(val)){
            sliders[ev.target.id].val(round(Session.get(ev.target.id), 2));
            return;
        }
        ev.target.value = round(val, 2); // updates the textbox
        Session.set(ev.target.id, Number(val));
        var radius_dif = Math.abs(radius - radius_sum);
        radius_dif -= Math.abs(val-current_question[ev.target.id]);
        radius_dif = radius_dif + 0.0001; //laplace smoothing
        var credits_percentage = 100*radius_dif/radius;
        if (isNaN(credits_percentage)){
            credits_percentage = 0;
        }
        $("#creditsleft").text("Credits left: " + round(credits_percentage, 1));
        if (update_slider_flag){
            sliders[ev.target.id].val(round(val, 2));
        }
        //update stacked bars
        var slider_idx_counter = 0;
        var curr_slider_total_width = 0;
        var slider_laplace_smoothing = true;
        while (slider_idx_counter < 4){
            var curr_slider = "slider"+slider_idx_counter.toString();
            var curr_slider_value = Session.get(curr_slider);
            var curr_slider_bar = curr_slider + "bar";
            var slider_width_fraction = Math.abs(curr_slider_value - current_question[curr_slider]) / Math.abs(radius);
            $("#" + curr_slider_bar).width(slider_width_fraction * $("#budgetbar").width()-0.3); //laplace smoothing
            $("#" + curr_slider_bar).text(round(slider_width_fraction*100, 1));
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

    update_slider_mech21 = function (ev, val, update_slider_flag) {
        var curr_experiment = Answers.findOne({worker_ID: worker_ID_value});
        var current_question = Questions.findOne({"question_ID": curr_experiment.current_question});
        if (!update_slider_flag)
            var update_slider_flag = false;
        if (isNaN(val)){
            sliders[ev.target.id].val(Number(Session.get(ev.target.id)).toFixed(2));
            return;
        }
        ev.target.value = Number(val).toFixed(2); // updates the textbox
        Session.set(ev.target.id, Number(val));
        if (update_slider_flag){
            sliders[ev.target.id].val(Number(val).toFixed(2));
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
            weight_sliders[ev.target.id].val(Number(Session.get(ev.target.id)).toFixed(3));
            return;
        }
        ev.target.value = round(val, 2); // updates the textbox
        Session.set(ev.target.id, val);
        if (update_slider_flag){
            weight_sliders[ev.target.id].val(round(val, 2));
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
            well_idx = "";
        }
        var total_money_spent = 0;
        for (var slider_idx_counter = 0; slider_idx_counter < 3; slider_idx_counter++){
            total_money_spent += Session.get("slider"+slider_idx_counter+well_idx);
        }
        total_money_spent -= Session.get("slider"+3+well_idx); // decreases by amt of income tax collected
        var deficit_value = total_money_spent + 316; //TODO: update with real numbers
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
            $("#deficit_percentage"+well_idx).text(deficit_value_percentage+"% increase");
        } else {
            deficit_value_percentage = -(parseInt(deficit_value_percentage*100)/100).toString();
            $("#deficit_percentage"+well_idx).css('color','green');
            $("#deficit_percentage"+well_idx).text(deficit_value_percentage+"% decrease");
        }
        $("#deficit_value"+well_idx).text("$"+deficit_value+"B");

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
    update_slider_mech3 = _.throttle(update_slider_mech31, 100);
    update_slider_mech2 = _.throttle(update_slider_mech21, 100);

    if (curr_experiment.current_question == 0) {
        sliders = {};
        for (var slider_idx = 0; slider_idx < 4; slider_idx++){
            var slider_current = 0;
            if (current_question['slider'+slider_idx]){
                slider_current = Number(current_question['slider'+slider_idx]);
                var slider_min = slider_current - (radius)*1.25;
                var slider_max = slider_current + (radius)*1.25;
                Session.set('slider'+slider_idx, slider_current);
                sliders['slider'+slider_idx] = this.$("div#slider"+slider_idx).noUiSlider({
                    start: slider_current,
                    connect: "lower",
                    range: {
                        'min': slider_min,
                        'max': slider_max
                    }
                }).noUiSlider_pips({
                    mode: 'positions',
                    values: [0,25,50,75,100],
                    density: 4
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
                $("#slider"+slider_idx+"min").text("$"+round(slider_min,2)+"B");
                $("#slider"+slider_idx+"cur").text("$"+round(slider_current,2)+"B");
                $("#slider"+slider_idx+"max").text("$"+round(slider_max,2)+"B");
            }
        }
        //update comparisons
        update_comps();
        //update the deficit text
        update_deficit();
        //initialize tooltips
        $('[data-toggle="tooltip"]').tooltip();

    } else if (curr_experiment.current_question == 3) {
        sliders = {};
        for (var slider_idx = 0; slider_idx < 4; slider_idx++){
            var slider_current = 0;
            if (current_question['slider'+slider_idx]){
                slider_current = Number(current_question['slider'+slider_idx]);
                var slider_min = slider_current - (radius)*1.25;
                var slider_max = slider_current + (radius)*1.25;
                Session.set('slider'+slider_idx, slider_current);
                sliders['slider'+slider_idx] = this.$("div#slider"+slider_idx).noUiSlider({
                    start: slider_current,
                    connect: "lower",
                    range: {
                        'min': slider_min,
                        'max': slider_max
                    }
                }).noUiSlider_pips({
                    mode: 'positions',
                    values: [0,25,50,75,100],
                    density: 4
                }).on('slide', function (ev, val) {
                    // set real values on 'slide' event
                    try {
                        update_slider_mech3(ev, val);
                    } catch (TypeError){
                    }
                }).on('change', function (ev, val) {
                    // round off values on 'change' event
                    try {
                        update_slider_mech3(ev, val);
                    } catch (TypeError){
                    }
                });
            }
        }
        //update comparisons
        update_comps();
        //update the deficit text
        update_deficit();
        //initialize tooltips
        $('[data-toggle="tooltip"]').tooltip();

    } else if (curr_experiment.current_question == 1){
        //mechanism 1 specific js
        //initialize all 15 sliders in one loop!
        var slider_idx = 0;
        var well_idx = 0;
        while(slider_idx<4){
            while(well_idx<3){
                var total_width = $(".progress").width();
                var value_difference = (current_question["slider"+slider_idx+well_idx]-current_question["slider"+slider_idx+"1"]);
                var relative_difference = value_difference/radius;
                var current_width = relative_difference * 0.3 + 0.5;
                $("#slider"+slider_idx+well_idx).width(Math.max(58, current_width*total_width));
                //display chosen value
                $("#slider"+slider_idx+well_idx).text("$"+round(current_question["slider"+slider_idx+well_idx],2)+"B");
                //display comparison to 2016 estimates
                Session.set('slider'+slider_idx+well_idx, current_question["slider"+slider_idx+well_idx]);
                var percentage_difference = compute_averages(slider_idx, current_question["slider"+slider_idx+well_idx]);
                if (percentage_difference < 0){
                    //red background
                    $("#slider"+slider_idx+well_idx+"comp").css('color','red');
                    // set value
                    $("#slider"+slider_idx+well_idx+"comp").text(round(percentage_difference, 2)+"%");
                } else {
                    //green background
                    $("#slider"+slider_idx+well_idx+"comp").css('color','green');
                    // set value
                    $("#slider"+slider_idx+well_idx+"comp").text("+"+round(percentage_difference, 2)+"%");
                }
                well_idx ++;
            }
            slider_idx++;
            well_idx = 0;
        }
        //initialize the deficit sliders
        var initial_deficit = current_question['slider41'];
        for (var well_idx = 0; well_idx < 3; well_idx++){
            var current_deficit = current_question['slider'+4+well_idx];
            var deficit_difference = current_deficit - initial_deficit;
            var deficit_scaled_difference = deficit_difference / (2*radius);
            var total_width = $(".progress").width();
            var current_width = deficit_scaled_difference * 0.5 + 0.5;
            $("#slider"+4+well_idx).width(Math.max(58, current_width*total_width));
            $("#slider"+4+well_idx).text("$"+round(current_deficit, 2) +"B");
            var deficit_percentage_change = (current_deficit - 550) / 5.5;
            if (deficit_percentage_change < 0){
                //red background
                $("#slider"+4+well_idx+"comp").css('color','green');
                // set value
                $("#slider"+4+well_idx+"comp").text(round(deficit_percentage_change, 2)+"%");
            } else {
                //green background
                $("#slider"+4+well_idx+"comp").css('color','red');
                // set value
                $("#slider"+4+well_idx+"comp").text("+"+round(deficit_percentage_change, 2)+"%");
            }
        }
        for (well_idx = 0; well_idx < 3; well_idx++){
            update_deficit(well_idx);
        }
        $('[data-toggle="tooltip"]').tooltip();

    } else if (curr_experiment.current_question == 2){
        //mechanism 2 specific js

        sliders = {};
        for (var slider_idx = 0; slider_idx < 4; slider_idx++){
            var slider_current = 0;
            if (current_question['slider'+slider_idx]){
                slider_current = Number(current_question['slider'+slider_idx]);
                var slider_min = 0;
                var slider_max = 2*slider_current;
                Session.set('slider'+slider_idx, slider_current);
                sliders['slider'+slider_idx] = this.$("div#slider"+slider_idx).noUiSlider({
                    start: slider_current,
                    connect: "lower",
                    range: {
                        'min': slider_min,
                        'max': slider_max
                    }
                }).noUiSlider_pips({
                    mode: 'positions',
                    values: [0,25,50,75,100],
                    density: 4
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
            }
        }

        //WEIGHT SLIDERS
        weight_sliders = {};
        for (var slider_idx = 0; slider_idx < 5; slider_idx++) {
            Session.set('slider'+slider_idx+"weight", 5);
            weight_sliders['slider' + slider_idx] = this.$("div#slider" + slider_idx + "weight").noUiSlider({
                start: 5,
                connect: "lower",
                range: {
                    'min': 0,
                    'max': 10
                }
            }).noUiSlider_pips({
                mode: 'positions',
                values: [0,25,50,75,100],
                density: 4
            }).on('slide', function (ev, val) {
                // set real values on 'slide' event
                try {
                    update_weight_slider(ev, val);
                } catch (TypeError) {
                }
            }).on('change', function (ev, val) {
                // round off values on 'change' event
                try {
                    update_weight_slider(ev, val);
                } catch (TypeError) {
                }
            });
        }
        //update comps
        update_comps();
        //update the deficit text
        update_deficit();
        //initialize tooltips
        $('[data-toggle="tooltip"]').tooltip();
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
Template.mechanism3.events({
    'change textarea': function(event){
        update_slider_mech3(event, event.target.value, true);
    }
});