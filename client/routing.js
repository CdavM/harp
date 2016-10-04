$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return decodeURI(results[1]) || 0;
    }
};

Router.route('/', function(){

  var wid = $.urlParam('workerId');
  var asg_val = $.urlParam('assignmentId');
  var hit_val = $.urlParam('hitId');

  if (wid == null || wid.length < 5){
      // Router.go('/hitId='+makeid()+'&workerId='+makeid()+'&assignmentId='+makeid());
      Router.go('/end');// Uncomment this when not debugging anymore
  }

  var curr_experiment = Answers.findOne({worker_ID: wid});
  initial_time_val = new Date().getTime();

  Session.set('worker_ID_value', wid);
  Session.set('initial_time_value', initial_time_val);
  Session.set('asg_ID_value', asg_ID);
  Session.set('hit_ID_value', hit_val)
  if ((curr_experiment && curr_experiment.experiment_finished))
  {
    //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
    Router.go('/end');  //send them to end, entry participated already.
  } else {
    Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val}, 'startup');
    this.render('experiment');
  }
});

function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 14; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

Router.route('/hitId=:hit&workerId=:wid&assignmentId=:asg', function(){
  // if (Session.get('worker_ID_value').length != 14) {
  //   Router.go('/end')
  // }
  var wid = this.params.wid;
  var asg_val = this.params.asg;
  var hit_val = this.params.hit;
  var curr_experiment = Answers.findOne({worker_ID: wid});
  Session.set('worker_ID_value', wid);
  console.log(curr_experiment);
  console.log(wid);
  console.log(hit_val);
  if ((curr_experiment && curr_experiment.experiment_finished) || (wid.length <6 ))
  {
    //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
    Router.go('/end');  //send them to end, entry participated already.
  } else {
    initial_time_val = new Date().getTime();
    Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val}, 'startup');
    this.render('experiment');
  }
});

Router.route('/end', function(){
  this.render('end');
});
