$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return decodeURI(results[1]) || 0;
    }
};

function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 14; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

// Router.route('/', function(){
//
//   Router.go('/radius=-1&mechanism=l2&hitId='+makeid()+'&workerId='+makeid()+'&assignmentId='+makeid());
//   //TODO remove above line when not demo
//
//   var wid = $.urlParam('workerId');
//   var asg_val = $.urlParam('assignmentId');
//   var hit_val = $.urlParam('hitId');
//   var demo = true; //demo mode
//   var radius_set = $.urlParam('radius');
//   var mechanism = $.urlParam('mechanism');
//
//   if (wid == null || wid.length < 5){
//       if (demo){
//         Router.go('/radius=-1&mechanism=l2&hitId='+makeid()+'&workerId='+makeid()+'&assignmentId='+makeid());
//       }
//       else{
//         Router.go('/hitId='+makeid()+'&workerId='+makeid()+'&assignmentId='+makeid());
//       }
//       //Router.go('/end');// Uncomment this when not debugging anymore
//   }
//
//
//   //NOTE: nothing below this will run... because of router.go above (I think)
//   var curr_experiment = Answers.findOne({worker_ID: wid});
//   initial_time_val = new Date().getTime();
//
//   Session.set('worker_ID_value', wid);
//   Session.set('initial_time_value', initial_time_val);
//   Session.set('asg_ID_value', asg_val);
//   Session.set('hit_ID_value', hit_val)
//   if (radius_set == null || demo == false){
//     radius_set = -1
//   }
//   if (demo == false){
//     mechanism = '';
//   }
//   else if (mechanism == null && demo == true){
//     mechanism = 'l2';
//   }
//
//   if ((curr_experiment && curr_experiment.experiment_finished))
//   {
//     //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
//     Router.go('/end');  //send them to end, entry participated already.
//   } else {
//     console.log('starting call with none', radius_set, mechanism)
//     Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val, radius:radius_set, mechanism:mechanism}, 'startup');
//     this.render('experiment');
//   }
// });

// Router.route('/hitId=:hit&workerId=:wid&assignmentId=:asg', function(){
//   // if (Session.get('worker_ID_value').length != 14) {
//   //   Router.go('/end')
//   // }
//   var wid = this.params.wid;
//   var asg_val = this.params.asg;
//   var hit_val = this.params.hit;
//   var curr_experiment = Answers.findOne({worker_ID: wid});
//   Session.set('worker_ID_value', wid);
//   console.log(curr_experiment);
//   console.log(wid);
//   console.log(hit_val);
//   if ((curr_experiment && curr_experiment.experiment_finished) || (wid.length <6 ))
//   {
//     //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
//     Router.go('/end');  //send them to end, entry participated already.
//   } else {
//     initial_time_val = new Date().getTime();
//     console.log('starting call with noneradmech', radius_set, mechanism)
//     Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val}, 'startup');
//     this.render('experiment');
//   }
// });
//
// Router.route('/mechanism=:mec', function(){
//   var wid = makeid();
//   var asg_val = makeid();
//   var hit_val = makeid();
//   var demo = true; //demo mode
//   var radius_set = $.urlParam('radius');
//   var mechanism = $.urlParam('mechanism');
//
//   var curr_experiment = Answers.findOne({worker_ID: wid});
//   initial_time_val = new Date().getTime();
//
//   Session.set('worker_ID_value', wid);
//   Session.set('initial_time_value', initial_time_val);
//   Session.set('asg_ID_value', asg_val);
//   Session.set('hit_ID_value', hit_val)
//   if (radius_set == null || demo == false){
//     radius_set = -1
//   }
//   if (demo == false){
//     mechanism = '';
//   }
//   else if (mechanism == null && demo == true){
//     mechanism = 'l2';
//   }
//
//   if ((curr_experiment && curr_experiment.experiment_finished))
//   {
//     //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
//     Router.go('/end');  //send them to end, entry participated already.
//   } else {
//     console.log('starting call with mech', radius_set, mechanism)
//     Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val, radius:radius_set, mechanism:mechanism}, 'startup');
//     this.render('experiment');
//   }
//
// });
//
// Router.route('/radius=:rad', function(){
//   var wid = makeid();
//   var asg_val = makeid();
//   var hit_val = makeid();
//   var demo = true; //demo mode
//   var radius_set = $.urlParam('radius');
//   var mechanism = $.urlParam('mechanism');
//
//   var curr_experiment = Answers.findOne({worker_ID: wid});
//   initial_time_val = new Date().getTime();
//
//   Session.set('worker_ID_value', wid);
//   Session.set('initial_time_value', initial_time_val);
//   Session.set('asg_ID_value', asg_val);
//   Session.set('hit_ID_value', hit_val)
//   if (radius_set == null || demo == false){
//     radius_set = -1
//   }
//   if (demo == false){
//     mechanism = '';
//   }
//   else if (mechanism == null && demo == true){
//     mechanism = 'l2';
//   }
//
//   if ((curr_experiment && curr_experiment.experiment_finished))
//   {
//     //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
//     Router.go('/end');  //send them to end, entry participated already.
//   } else {
//     console.log('starting call with rad', radius_set, mechanism)
//     Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val, radius:radius_set, mechanism:mechanism}, 'startup');
//     this.render('experiment');
//   }
//
// });

Router.route('/', function(){
// Router.route('/radius=:rad&mechanism=:mec', function(){
  var wid = makeid();
  var asg_val = makeid();
  var hit_val = makeid();
  var demo = true; //demo mode
  var radius_set = '-1';//this.params._rad;
  var mechanism = 'l2';//this.params._mec;

  Router.go('/radius/' + radius_set+'/mechanism/'+ mechanism+'/hitId/'+makeid()+'/workerId/'+makeid()+'/assignmentId/'+makeid());
});

Router.route('/radius/:_rad/', function(){
// Router.route('/radius=:rad&mechanism=:mec', function(){
  var wid = makeid();
  var asg_val = makeid();
  var hit_val = makeid();
  var demo = true; //demo mode
  var radius_set = this.params._rad;
  var mechanism = 'l2';//this.params._mec;

  Router.go('/radius/' + radius_set+'/mechanism/'+ mechanism+'/hitId/'+makeid()+'/workerId/'+makeid()+'/assignmentId/'+makeid());
});

Router.route('/mechanism/:_mec/', function(){
// Router.route('/radius=:rad&mechanism=:mec', function(){
  var wid = makeid();
  var asg_val = makeid();
  var hit_val = makeid();
  var demo = true; //demo mode
  var radius_set = '-1';//this.params._rad;
  var mechanism = this.params._mec;

  Router.go('/radius/' + radius_set+'/mechanism/'+ mechanism+'/hitId/'+makeid()+'/workerId/'+makeid()+'/assignmentId/'+makeid());
});

Router.route('/radius/:_rad/mechanism/:_mec/', function(){
// Router.route('/radius=:rad&mechanism=:mec', function(){
  var wid = makeid();
  var asg_val = makeid();
  var hit_val = makeid();
  var demo = true; //demo mode
  var radius_set = this.params._rad;
  var mechanism = this.params._mec;

  Router.go('/radius/' + radius_set+'/mechanism/'+ mechanism+'/hitId/'+makeid()+'/workerId/'+makeid()+'/assignmentId/'+makeid());


  // var demo = true; //demo mode
  // var radius_set = $.urlParam('radius');
  // var mechanism = $.urlParam('mechanism');

  var curr_experiment = Answers.findOne({worker_ID: wid});
  initial_time_val = new Date().getTime();

  Session.set('worker_ID_value', wid);
  Session.set('initial_time_value', initial_time_val);
  Session.set('asg_ID_value', asg_val);
  Session.set('hit_ID_value', hit_val)
  if (radius_set == null || demo == false){
    radius_set = -1
  }
  if (demo == false){
    mechanism = '';
  }
  else if (mechanism == null && demo == true){
    mechanism = 'l2';
  }

  if ((curr_experiment && curr_experiment.experiment_finished))
  {
    //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
    Router.go('/end');  //send them to end, entry participated already.
  } else {
    console.log('starting call with radmech', radius_set, mechanism)
    Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val, radius:radius_set, mechanism:mechanism}, 'startup');
    this.render('experiment');
  }

});

Router.route('/radius/:_rad/mechanism/:_mec/hitId/:_hit/workerId/:_wid/assignmentId/:_asg', function(){
// Router.route('/radius=:rad&mechanism=:mec&hitId=:hit&workerId=:wid&assignmentId=:asg', function(){
  var wid = this.params._wid;
  var asg_val = this.params._asg;
  var hit_val = this.params._hit;
  var demo = true; //demo mode
  var radius_set = this.params._rad;
  var mechanism = this.params._mec;

  // var wid = $.urlParam('workerId');
  // var asg_val = $.urlParam('assignmentId');
  // var hit_val = $.urlParam('hitId');
  // var demo = true; //demo mode
  // var radius_set = $.urlParam('radius');
  // var mechanism = $.urlParam('mechanism');

  // if (wid == null || wid.length < 5){
  //     Router.go('/radius=-1&mechanism=l2&hitId='+makeid()+'&workerId='+makeid()+'&assignmentId='+makeid());
  //     //Router.go('/end');// Uncomment this when not debugging anymore
  // }

  var curr_experiment = Answers.findOne({worker_ID: wid});
  initial_time_val = new Date().getTime();

  Session.set('worker_ID_value', wid);
  Session.set('initial_time_value', initial_time_val);
  Session.set('asg_ID_value', asg_val);
  Session.set('hit_ID_value', hit_val)
  Session.set('radius_ID_value', radius_set) //for demo
  Session.set('mechanism_ID_value', mechanism)
  if (radius_set == null || demo == false){
    radius_set = -1
  }
  if (demo == false){
    mechanism = '';
  }
  else if (mechanism == null && demo == true){
    mechanism = 'l2';
  }

  if ((curr_experiment && curr_experiment.experiment_finished))
  {
    //Meteor.setTimeout(function(){Session.set('experiment_finished', false);}, 150);
    Router.go('/end');  //send them to end, entry participated already.
  } else {
    console.log('starting call with radmechall', radius_set, mechanism)
    Meteor.call('initialPost', {worker_ID: wid, initial_time: initial_time_val, asg_ID: asg_val, hit_ID: hit_val, radius:radius_set, mechanism:mechanism}, 'startup');
    this.render('experiment');
  }

});

Router.route('/end', function(){
  this.render('end');
});
