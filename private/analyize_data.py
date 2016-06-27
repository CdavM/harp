import csv
import ast

def load_data(filename):
	with open(filename, mode='rb') as file:
		reader = csv.DictReader(file)
		return list(reader)
	print "unable to open file"
	return None

slider_order = ['Defense', 'Health', 'Transportation', 'Tax']

def experiment_2(data): #ideal points and weights elicitation
	answer = {}
	answer['slider0_loc'] = float(data['slider0_text'][0])
	answer['slider0_weight'] = float(data['slider0w_text'][0])

	answer['slider1_loc'] = float(data['slider1_text'][0])
	answer['slider1_weight'] = float(data['slider1w_text'][0])
	
	answer['slider2_loc'] = float(data['slider2_text'][0])
	answer['slider2_weight'] = float(data['slider2w_text'][0])

	answer['slider3_loc'] = float(data['slider3_text'][0])
	answer['slider3_weight'] = float(data['slider3w_text'][0])

	answer['explanation'] = data['text_explanation']

	return answer

def experiment_0(data): #constrained movement
	answer = {}
	answer['slider0_loc'] = float(data['slider0'][0])
	answer['slider1_loc'] = float(data['slider1'][0])
	answer['slider2_loc'] = float(data['slider2'][0])
	answer['slider3_loc'] = float(data['slider3'][0])
	answer['explanation'] = data['text_explanation']

	return answer

def experiment_1(data): #comparisons
	answer = {}
	answer['explanation'] = data['text_explanation']
	answer['selection'] = data[""]
	return answer

switcher = {
    0: experiment_0,
    1: experiment_1,
    2: experiment_2,
}

def clean_data(dirty):
	clean = []
	for row in dirty:
		if len(row['experiment_id'])==0 or (len(row['answer1.0.1']) == 0 and len(row['answer1.1.1']) == 0 and len(row['answer1.2.1']) == 0):
			continue
		d = {}
		copy_over = ['worker_ID', 'asg_ID']
		for ide in copy_over:
			d[ide] = row[ide]
		d['experiment_id'] = int(row['experiment_id'])
		d['question_num'] = int(row['current_question'])
		d['begin_time'] = int(row['begin_time'])
		d['initial_time'] = int(row['initial_time'])

		answerdict = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.1'])

		d['time_page0'] = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.0'])['time']
		d['time_page1'] = answerdict['time']
		d['time_page2'] = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.2'])['time']

		#print d['experiment_id'], d['question_num'], answerdict
		d['question_data'] = switcher[d['question_num']](answerdict)

		print d
		clean.append(d)
	return clean

def main():
	#data = clean_data(load_data('export-20160623074343_edited.csv'))
	# data = clean_data(load_data('export-20160625101532_edited.csv'))
	data = clean_data(load_data('export-20160627170659_edited.csv'))

	print len(data)

if __name__ == "__main__":
	main()
