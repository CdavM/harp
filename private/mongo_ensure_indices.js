db.questions.ensureIndex({ question_id : 1})
db.answers.ensureIndex({experiment_id : "text"})
db.answers.ensureIndex({worker_ID : "text"})
db.scheduling.ensureIndex({experiment_id : "text"})