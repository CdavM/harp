Answers = new Mongo.Collection("answers");
Questions = new Mongo.Collection("questions");
AnswerForms = new Mongo.Collection("answerforms");
duration = 15000; //ms

round = function (number, num_decimals) {
    return (parseInt(Number(number)*Math.pow(10,num_decimals))/Math.pow(10,num_decimals)).toFixed(num_decimals);
};