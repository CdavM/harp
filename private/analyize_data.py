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
	answer['slider0_loc'] = float(data['slider0_text'][0])
	answer['slider1_loc'] = float(data['slider1_text'][0])
	answer['slider2_loc'] = float(data['slider2_text'][0])
	answer['slider3_loc'] = float(data['slider3_text'][0])
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
		if len(row['experiment_id'])==0 or len(row['answer1']) == 0:
			continue
		d = {}
		copy_over = ['worker_ID', 'asg_ID', 'payments']
		for ide in copy_over:
			d[ide] = row[ide]
		d['experiment_id'] = int(row['experiment_id'])
		d['question_num'] = int(row['current_question'])
		d['begin_time'] = int(row['begin_time'])
		d['initial_time'] = int(row['initial_time'])

		answerdict = ast.literal_eval(row['answer1'])[str(d['question_num'])]
		d['timestamp'] = answerdict['0']['time']
		if '1' not in answerdict:
			continue
		d['question_data'] = switcher[d['question_num']](answerdict['1'])

		clean.append(d)
	return clean

def main():
	data = clean_data(load_data('export-20160623074343_edited.csv'))
	print data

if __name__ == "__main__":
	main()
