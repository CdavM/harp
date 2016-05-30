Template.registerHelper('worker_id_value',function(){
    if (Session.equals("worker_ID_value", -1)){
        return "BLANK";
    } else {
        return Session.get('worker_ID_value');
    }
});

Template.registerHelper('time_remaining', function(){return Session.get("time_remaining");});
Template.registerHelper('current_payment', function(){return Session.get('current_payment');});
Template.registerHelper('experiment_finished', function(){return Session.get('experiment_finished');});

Template.registerHelper('show_payment_system', function(){
    return Meteor.settings.public.show_payment; //show the user their current payment
});
Template.registerHelper('show_timer', function(){
    return Meteor.settings.public.show_timer; //show the user the time remaining
});
Template.registerHelper('slider', function () {
    return Session.get("slider");
});
Template.registerHelper('slider0_value', function () {
    return Session.get('slider0');
});
Template.registerHelper('slider1_value', function () {
    return Session.get('slider1');
});
Template.registerHelper('slider2_value', function () {
    return Session.get('slider2');
});
Template.registerHelper('slider3_value', function () {
    return Session.get('slider3');
});
Template.registerHelper('slider4_value', function () {
    return Session.get('slider4');
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
    var current_mechanism_value = Answers.findOne({worker_ID: Session.get("worker_ID_value")}).current_question;
    return "mechanism"+current_mechanism_value;
});

Template.registerHelper('current_question_text', function(){
    var current_question_value = Answers.findOne({worker_ID: Session.get("worker_ID_value")}).current_question;
    return "question"+current_question_value+"text";
});

Template.registerHelper('waiting', function(){
    return Session.get('waiting');
});