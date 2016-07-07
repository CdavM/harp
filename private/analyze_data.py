import csv
import ast
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
from operator import itemgetter

import numpy as np
from data_helpers import *


DEBUG_LEVEL = 0

def plot_sliders_over_time(data, title):
    n = range(1, len(data) + 1)

    for slider in range(0, len(slider_order)):
        vals = [d['question_data']['slider' + str(slider) + '_loc'] for d in data]
        plt.plot(n, vals, label = slider_order[slider])
    plt.legend(loc='upper left', fontsize = 18)

    plt.tick_params(axis='both', which='major', labelsize=18)
    
    # Add the axis labels
    plt.title(title, fontsize = 18)
    plt.ylabel('$ (Billions)', fontsize = 18)
    plt.xlabel('Iteration', fontsize = 18)
    plt.show()

def analyze_data_experiment0(data): # constrained movement
    plot_sliders_over_time(data, 'l2 Constrained Movement Mechanism')
    creditsused = [] #histogram of credits used
    for exp in data:
    	creditsused.append(calc_credits_used(exp))
    plt.hist(creditsused, bins = 10, range =[0, 1])
    plt.show()
    return None


def analyze_data_experiment1(data): # comparisons
    plot_sliders_over_time(data, 'Comparison Mechanism')
    return None


def analyze_data_experiment2(data): # ideal points and elicitation
    return None

def analyze_data_experiment3(data): # constrained movement
    plot_sliders_over_time(data, 'l1 Constrained Movement Mechanism')
    creditsused = []
    for exp in data:
    	creditsused.append(calc_credits_used(exp))
    plt.hist(creditsused, bins = 10, range =[0, 1])
    plt.show()

switcher_analyze_data = {
    0: analyze_data_experiment0,
    1: analyze_data_experiment1,
    2: analyze_data_experiment2,
    3: analyze_data_experiment3
}

def calc_credits_used(experiment):
	return experiment['question_data']['slider0_creditsused'] + experiment['question_data']['slider1_creditsused'] + experiment['question_data']['slider2_creditsused'] + experiment['question_data']['slider3_creditsused']

def analyze_data(organized_data, LABEL):
    # for comparisons & constrained movement, plot the locations for each slider (with labels) and deficit over time
    # for raw elicitation, calculate the minimizer (optimal point)
    # also calculate average time for each mechanism

    for key in organized_data:
        print switcher_analyze_data[key](organized_data[key])
    #calculate_time_spent(organized_data, LABEL)
    analyze_movement_and_weights(organized_data, LABEL)
slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]


def analyze_movement_and_weights(organized_data, LABEL):
	averages_byitem = {0: np.zeros(4), 1:np.zeros(4), 2:np.zeros(4), 3:np.zeros(4)}
	averages_bymostmovement = {0: np.zeros(4), 1:np.zeros(4), 2:np.zeros(4), 3:np.zeros(4)}
	averages_creditpercentage = {0:np.zeros(4), 3:np.zeros(4)}
	averages_creditpercentage_bymost = {0:np.zeros(4), 3:np.zeros(4)}
	num_key_positive = np.zeros(4)
	for key in organized_data:
		for experiment in organized_data[key]:
			percentages = get_movement_percentages(experiment)
			if percentages is None:
				print "Did not move at all", experiment['experiment_id']
				continue
			num_key_positive[key] += 1
			#print key, percentages
			averages_byitem[key] += percentages
			averages_bymostmovement[key] += sorted(percentages, reverse = True)
			if key == 0 or key == 3:
				credit_percentages = get_credit_percentage(experiment)
				averages_creditpercentage[key] += credit_percentages
				averages_creditpercentage_bymost[key] += sorted(credit_percentages, reverse=True)
		averages_byitem[key] /= num_key_positive[key]
		averages_bymostmovement[key] /= num_key_positive[key]
		if key == 0 or key == 3:
			averages_creditpercentage[key] /= num_key_positive[key]
			averages_creditpercentage_bymost[key] /= num_key_positive[key]


	dpoints_byitem = []
	dpoints_bymost = []
	dpoints_credits = []
	dpoints_credits_bymost = []

	for key in averages_byitem.keys():
		for idx in xrange(4):
			dpoints_byitem.append([mechanism_names[key], slider_order[idx], averages_byitem[key][idx]])
			dpoints_bymost.append([mechanism_names[key], str(idx), averages_bymostmovement[key][idx]])
			if key == 0 or key == 3:
				dpoints_credits.append([mechanism_names[key], slider_order[idx], averages_creditpercentage[key][idx]])
				dpoints_credits_bymost.append([mechanism_names[key], str(idx), averages_creditpercentage_bymost[key][idx]])

	barplot(np.array(dpoints_byitem), LABEL, 'Percent of movement', 'Item', slider_order[0:4], mechanism_names)
	barplot(np.array(dpoints_bymost), LABEL, 'Percent of movement', 'Order by movement', [str(x) for x in xrange(4)], mechanism_names)
	barplot(np.array(dpoints_credits), LABEL, 'Percent of credits used', 'Item', slider_order[0:4], [mechanism_names[0], mechanism_names[3]])
	barplot(np.array(dpoints_credits_bymost), LABEL, 'Percent of credits used', 'Order by movement', [str(x) for x in xrange(4)], [mechanism_names[0], mechanism_names[3]])


def get_credit_percentage(experiment):
	movement = [experiment['question_data']['slider0_creditsused'] , experiment['question_data']['slider1_creditsused'] , experiment['question_data']['slider2_creditsused'] , experiment['question_data']['slider3_creditsused']]
	if sum(movement) < .0001: #did not move
		return None
	return movement/np.sum(movement)


def get_movement_percentages(single_experiment_data):
	if single_experiment_data['question_num'] == 2:
		movement = [single_experiment_data['question_data']['slider0_weight'], single_experiment_data['question_data']['slider1_weight'], single_experiment_data['question_data']['slider2_weight'], single_experiment_data['question_data']['slider3_weight']]
	else:
		new_vals = [single_experiment_data['question_data']['slider0_loc'], single_experiment_data['question_data']['slider1_loc'], single_experiment_data['question_data']['slider2_loc'], single_experiment_data['question_data']['slider3_loc']]
		previous_vals = single_experiment_data['question_data']['previous_slider_values'][0:4]
		movement = np.abs(np.subtract(new_vals, previous_vals))
	if sum(movement) < .0001: #did not move
		return None
	return movement/np.sum(movement)

def calculate_time_spent(organized_data, LABEL):
    #For each mechanism, calculate average time spent on each page and plot it in a chuncked bar graph
    pagenames = ['Welcome Page', 'Instructions', 'Mechanism', 'Feedback']

    dpoints = []#np.empty((len(organized_data.keys())* len(pagenames), 3), dtype = )
    for key in organized_data:
        for page in range(0, len(pagenames)):
            #print organized_data[key]
            print [d['time_page' + str(page)] for d in organized_data[key]]
            dpoints.append([mechanism_names[key], pagenames[page], np.mean([d['time_page' + str(page)] for d in organized_data[key]])])
    barplot(np.array(dpoints), LABEL, 'Time (Seconds)', 'Page', pagenames, mechanism_names)

def organize_payment(organized_data):
    for key in organized_data:
        print "MECHANISM: " + mechanism_names[key]
        for d in organized_data[key]:
            print d['worker_ID'], d['time_page0'], d['time_page1'], d['time_page2'], d['time_page3'], d['question_data']['explanation'], "\n"

def print_different_things(organized_data):
    for key in organized_data:
        print "MECHANISM: " + mechanism_names[key]
        for d in organized_data[key]:
            print d['question_data']['explanation'][0], "\n"

    for key in organized_data:
        print "MECHANISM: " + mechanism_names[key]
        for d in organized_data[key]:
            print d['feedback_data']['feedback'][0], "\n"
def main():

    #data = clean_data(load_data('export-20160623074343_edited.csv'))
    # data = clean_data(load_data('export-20160625101532_edited.csv'))

    #data, organized_data = clean_data(load_data('export-20160627170659_edited.csv'))
    data, organized_data = clean_data(load_data('export-20160707161738_PILOTFINAL_fixed.csv'))
    LABEL = 'Pilot'
    if DEBUG_LEVEL > 0:
        print len(data)
        for key in organized_data:
            print key, [d['experiment_id'] for d in organized_data[key]]
    analyze_data(organized_data, LABEL)

    #organize_payment(organized_data)

    #print_different_things(organized_data  )

if __name__ == "__main__":
    main()


