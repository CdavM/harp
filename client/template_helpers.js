Template.registerHelper('worker_id_value',function(){
    if (Session.equals("worker_ID_value", -1)){
        return "BLANK";
    } else {
        return Session.get('worker_ID_value');
    }
});

Template.registerHelper('time_remaining', function(){
    var time_message = "";
    if (Meteor.settings.public.show_timer){
        var time_left = Session.get("time_remaining");
        var mins_left = parseInt(time_left / 60);
        var secs_left = time_left % 60;
        time_message = "Time remaining on this page: " + mins_left + " minutes and " + secs_left + " seconds";
        return time_message;
    }
    return;
});
Template.registerHelper('current_payment', function(){return Session.get('current_payment');});
Template.registerHelper('experiment_finished', function(){return Session.get('experiment_finished');});

Template.registerHelper('show_payment_system', function(){
    return Meteor.settings.public.show_payment; //show the user their current payment
});
Template.registerHelper('slider_names', function(slider_name_arg, color_arg, slider_title_arg) {
    var slider_object = {};
    slider_object.id = slider_name_arg;
    slider_object.title = slider_title_arg;
    slider_object.text = slider_name_arg+"_text";
    slider_object.name = slider_name_arg;
    switch (color_arg){
        case "blue":
            slider_object.color = "rgb(51, 122, 183)";
            break;
        case "green":
            slider_object.color = "rgb(92, 184, 92)";
            break;
        case "orange":
            slider_object.color = "rgb(240, 173, 78)";
            break;
        case "red":
            slider_object.color = "rgb(217, 83, 79)";
            break;
        case "lightblue":
            slider_object.color = "rgb(91, 192, 222)";
            break;
    }
    slider_object.min = slider_name_arg+"min";
    slider_object.cur = slider_name_arg+"cur";
    slider_object.max = slider_name_arg+"max";
    slider_object.comp = slider_name_arg + "comp";
    slider_object.label = slider_name_arg+"label";
    slider_object.value = Session.get(slider_name_arg);
    switch (slider_title_arg){
        case "National Defense":
            slider_object.tooltip = "The amount spent by the Department of Defense and spending on programs related to the military, but not veteran benefits. This amount is estimated to be $541 Billion in 2016.";
            break;
        case "Medicare & Health":
            slider_object.tooltip = "The amount spent on Medicare, Medicaid, the Children’s Health Insurance Program (CHIP), and Affordable Care Act (ACA) marketplace subsidies, along with related governmental health programs. This amount was estimated to be $1,004 Billion ($1.004 Trillion) in 2016.";
            break;
        case "Education, Science, Environment, & Transportation":
            slider_object.tooltip = "The amount spent on Transportation, Education, NASA, the Environmental Protection Agency, Department of Energy, the National Science Foundation, and related government programs. This amount is estimated to be $303 Billion in 2016.";
            break;
        case "Individual Income Tax":
            slider_object.tooltip = "The amount the Federal Government collects through individual income taxes. Assume that everyone’s taxes (including yours!) change proportionally to the amount you have increased or decreased. This amount is estimated to be $1,460 Billion ($1.46 Trillion) in 2016. Estimtes of income tax receipts are inexact, but assume that tax policy will be adjusted to try to achieve the increase or decrease specified.";
            break;
        case "Deficit":
            slider_object.tooltip = "The amount by which spending exceeds revenues. A negative value indicates a budget surplus. This value assumes spending on all other items is held constant. Like the income tax, this value is a rough estimate in any given year. However, you can assume for this survey that the estimes are approximately correct.";
    }
    return slider_object;
});

Template.registerHelper('deficit_names', function(well_idx) {
    if (typeof(well_idx) == "undefined") {
        well_idx = "";
    }
    deficit_object = {};
    deficit_object.deficit_text = "deficit_text"+well_idx;
    deficit_object.deficit_value = "deficit_value"+well_idx;
    deficit_object.deficit_percentage = "deficit_percentage"+well_idx;

    return deficit_object;
});
Template.registerHelper('initialized', function(){
    if(Session.equals('initialized', true)){
        return true;
    } else {
        return false;
    }
});

Template.registerHelper('current_answer', function(){
    var current_answer_value = Answers.findOne({worker_ID: Session.get("worker_ID_value")}).current_answer;
    return Meteor.settings.public.answer_forms[current_answer_value].template;
});

Template.registerHelper('current_mechanism', function(){
    var current_question_value = Answers.findOne({worker_ID: Session.get("worker_ID_value")}).current_question;
    if (current_question_value == 0){
        return "full_elicitation_mechanism";
    } else if ([1, 2, 3].indexOf(current_question_value) > -1){
        return "L2_mechanism";
    } else if ([4, 5, 6].indexOf(current_question_value) > -1){
        return "L1_mechanism";
    } else if ([7, 8, 9].indexOf(current_question_value) > -1){
        return "Linf_mechanism";
    }
});

Template.registerHelper('current_question_text', function(){
    var current_question_value = Answers.findOne({worker_ID: Session.get("worker_ID_value")}).current_question;
    if (current_question_value == 0){
        return "full_elicitation_text";
    } else if ([1, 2, 3].indexOf(current_question_value) > -1){
        return "L2_text";
    } else if ([4, 5, 6].indexOf(current_question_value) > -1){
        return "L1_text";
    } else if ([7, 8, 9].indexOf(current_question_value) > -1){
        return "Linf_text";
    }
});

Template.registerHelper('waiting', function(){
    return Session.get('waiting');
});
