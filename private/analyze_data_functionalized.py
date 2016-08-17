import csv
import ast
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
from operator import itemgetter
import math
import numpy as np
from data_helpers import *
import cvxpy

slider_order = ['Defense', 'Health',
	'Transportation', 'Income Tax', 'Deficit'];


def plot_sliders_over_time(data, title, prepend=""):
	n = range(0, len(data) + 1)

	for slider in range(0, len(slider_order)):
		vals = [d['question_data'][prepend + 'slider' +
			str(slider) + '_loc'] for d in data]
		vals.insert(0, initial_values[slider])  # prepend initial values
		plt.plot(n, vals, label=slider_order[slider])
	plt.legend(loc='upper left', fontsize=18)

	plt.tick_params(axis='both', which='major', labelsize=18)

	# Add the axis labels
	plt.title(title + " " + prepend, fontsize=18)
	plt.ylabel('$ (Billions)', fontsize=18)
	plt.xlabel('Iteration', fontsize=18)
	plt.show()


def calculate_full_elicitation_euclideanpoint(data):
	X = cvxpy.Variable(5)  # 1 point for each mechanism
	fun = 0
	for d in data:
		y = [d['question_data']['slider' +
			str(slider) + '_loc'] for slider in range(5)]
		w = [d['question_data']['slider' +
			str(slider) + '_weight'] for slider in range(5)]
		sumsq = math.sqrt(sum([math.pow(w[i], 2) for i in range(5)]))
		w = [w[i] / sumsq for i in range(5)]
		for slider in range(5):
			fun += w[slider] * cvxpy.abs(X[slider] - y[slider])
	obj = cvxpy.Minimize(fun)
	constraints = [X >= 0, X[0] + X[1] + X[2] -
		X[3] + INITIALDEFICITADDITIVE == X[4]]
	prob = cvxpy.Problem(obj, constraints)
	result = prob.solve()
	items = [X.value[i, 0] for i in range(5)]
	print 'Optimal full elicitation:', items
	deficit = items[0] + items[1] + items[2] - \
		items[3] + INITIALDEFICITADDITIVE
	items.append(deficit)
	return items


def calculate_full_elicitation_average(data):
	sliders = {0: [], 1: [], 2: [], 3: [], 4: []}
	weights = {0: [], 1: [], 2: [], 3: [], 4: []}
	rawaverages = {}
	weightedaverages_l1 = {}
	weightedaverages_l2 = {}

	for slider in sliders:
		sliders[slider] = [d['question_data'][
			'slider' + str(slider) + '_loc'] for d in data]
		weights[slider] = [d['question_data'][
			'slider' + str(slider) + '_weight'] for d in data]

	# normalize slider weights
	for i in range(len(weights[0])):
		summ = float(sum([weights[slider][i] for slider in weights]))
		for s in weights:
			weights[s][i] /= summ

	for slider in sliders:
		rawaverages[slider] = np.mean(sliders[slider])
		weightedaverages_l1[slider] = np.average(
			sliders[slider], weights=weights[slider])
		weightedaverages_l2[slider] = np.average(
			sliders[slider], weights=[math.pow(x, 2) for x in weights[slider]])

	return rawaverages, weightedaverages_l2, weightedaverages_l1, calculate_full_elicitation_euclideanpoint(
		data)


def plot_allmechansisms_together(
	organized_data, mechanism_super_dictionary, slider_order, lines_to_do=None):
	if lines_to_do is None:
		lines_to_do = mechanism_super_dictionary.keys();

	legend_names = []
	f, axarr = plt.subplots(5, sharex=True)
	lines = []

	full_elicitation_averages = {}
	for mech in mechanism_super_dictionary:
		if mechanism_super_dictionary[mech]['type'] == 'full':
			rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs = calculate_full_elicitation_average(organized_data[mech])
			full_elicitation_averages[mech] = {'rawaverages': rawaverages, 'weightedaverages_l2': weightedaverages_l2, 'weightedaverages_l1': weightedaverages_l1, 'euclideanprefs': euclideanprefs}

	maxn = -1
	for slider in xrange(0, len(slider_order)):
		for mechanism in mechanism_super_dictionary:
			if mechanism not in lines_to_do:
				continue
			if mechanism_super_dictionary[mechanism]['type'] == 'l1' or mechanism_super_dictionary[mechanism]['type'] == 'l2':
				n = range(0, len(organized_data[mechanism]) + 1)
				maxn = max(maxn, len(n))
				vals = [d['question_data']['slider' + str(slider) + '_loc'] for d in organized_data[mechanism]]
				vals.insert(0, mechanism_super_dictionary[mechanism]['initial_values'][slider]) #prepend initial values
				l = axarr[slider].plot(n, vals, label = mechanism_super_dictionary[mechanism]['name'])
				if slider == 0:
					lines.append(l[0])
					legend_names.append(mechanism_super_dictionary[mechanism]['name'])

		# comparisons
			if mechanism_super_dictionary[mechanism]['type'] == 'comparisons':
				for set_num in range(mechanism_super_dictionary[mechanism]['numsets']):
					n = range(0, len(organized_data[mechanism]) + 1)
					maxn = max(maxn, len(n))
					vals = [d['question_data']['set' + str(set_num) + 'slider' + str(slider) + '_loc'] for d in organized_data[mechanism]]
					vals.insert(0, mechanism_super_dictionary[mechanism]['initial_values'][set_num][slider]) #prepend initial values
					l = axarr[slider].plot(n, vals, label = mechanism_super_dictionary[mechanism]['name'] + ", Set " + str(set_num))
					if slider == 0:
						lines.append(l[0])
						legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ", Set " + str(set_num))

			n = range(maxn)
			if mechanism_super_dictionary[mechanism]['type'] == 'full':
				vals = [full_elicitation_averages[mechanism]['euclideanprefs'][slider] for _ in n]
				l = axarr[slider].plot(n, vals, label = mechanism_super_dictionary[mechanism]['name'])

				if slider == 0:
					lines.append(l[0])
					legend_names.append(mechanism_super_dictionary[mechanism]['name'])

		axarr[slider].set_title(slider_order[slider], fontsize = 18)
		axarr[slider].set_ylabel('$ (Billions)', fontsize = 18)
		axarr[slider].tick_params(axis='both', which='major', labelsize=18)
	
	axarr[len(slider_order)-1].set_xlabel('Iteration', fontsize = 18)
	f.legend(lines,legend_names , loc='upper center', borderaxespad=0., ncol = 3, fontsize = 18)
		
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
	for setnum in range(2):
		plot_sliders_over_time(data, 'Comparison Mechanism', 'set' + str(setnum))
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
	3: analyze_data_experiment3,
	4: analyze_data_experiment0,
	5: analyze_data_experiment1,
	6: analyze_data_experiment2,
	7: analyze_data_experiment3,
	8: analyze_data_experiment0,
	9: analyze_data_experiment1,
	10: analyze_data_experiment2,
	11: analyze_data_experiment3

}

def calc_credits_used(experiment):
	return experiment['question_data']['slider0_creditsused'] + experiment['question_data']['slider1_creditsused'] + experiment['question_data']['slider2_creditsused'] + experiment['question_data']['slider3_creditsused']

def analyze_data(organized_data, LABEL):
	# for comparisons & constrained movement, plot the locations for each slider (with labels) and deficit over time
	# for raw elicitation, calculate the minimizer (optimal point)
	# also calculate average time for each mechanism
	calculate_time_spent(organized_data, LABEL)

	# for key in organized_data:
	#	print switcher_analyze_data[key](organized_data[key])
	analyze_movement_and_weights(organized_data, LABEL)
slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]

def movingaverage(interval, window_size):
	window = np.ones(int(window_size))/float(window_size)
	return np.convolve(interval, window, 'valid')

def plot_percent_movements_over_time(organized_data, LABEL):
	averages_byitem = {'0': [[],[],[],[]], '1set0':[[],[],[],[]], '1set1':[[],[],[],[]], '2':[[],[],[],[]], '3':[[],[],[],[]]}
	averages_bymostmovement = {'0': [[],[],[],[]], '1set0':[[],[],[],[]], '1set1':[[],[],[],[]], '2':[[],[],[],[]], '3':[[],[],[],[]]}
	averages_creditpercentage = {'0':[[],[],[],[]], '3':[[],[],[],[]]}
	averages_creditpercentage_bymost = {'0':[[],[],[],[]], '3':[[],[],[],[]]}
	for key in organized_data:
		for experiment in organized_data[key]:
			if key != 1:
				percentages = get_movement_percentages(experiment)
				if percentages is None:
					print "Did not move at all", experiment['experiment_id']
					continue
				for i in range(len(percentages)):
					averages_byitem[str(key)][i].append(percentages[i])
					averages_bymostmovement[str(key)][i].append(sorted(percentages, reverse = True)[i])
				if key == 0 or key == 3:
					credit_percentages = get_credit_percentage(experiment)
					for i in range(len(credit_percentages)):
						averages_creditpercentage[str(key)][i].append(credit_percentages[i])
						averages_creditpercentage_bymost[str(key)][i].append(sorted(credit_percentages, reverse=True)[i])
			else:
				for setnum in range(0, 2):
					percentages = get_movement_percentages(experiment, prepend = 'set' + str(setnum))
					if percentages is None:
						print "Did not move at all", experiment['experiment_id']
						continue
					for i in range(len(percentages)):
						averages_byitem[str(key) + 'set' + str(setnum)][i].append(percentages[i])
						averages_bymostmovement[str(key) + 'set' + str(setnum)][i].append(sorted(percentages, reverse = True)[i])	  

	f, axarr = plt.subplots(4, sharex=True)
	lines = []
	mechanisms_to_do = [0, 1, 2, 3, 4]
	for slider in xrange(0, 4):
		for mechanism in mechanisms_to_do:#xrange(0, 4):
			n = range(0, len(averages_byitem[keyorder[mechanism]][slider]))
			vals = averages_byitem[keyorder[mechanism]][slider]
			l = axarr[slider].plot(n, vals, label = mechanism_names_expanded[mechanism], linestyle = 'None', marker = '.')
			# plot line of best fit
			# l = axarr[slider].plot(n, np.poly1d(np.polyfit(n, vals, 1))(n), label = mechanism_names_expanded[mechanism])
			mvgs = movingaverage(vals, 10)
			# l = axarr[slider].plot(range(len(mvgs)),mvgs, label = mechanism_names_expanded[mechanism])
			
			if slider == 0:
				lines.append(l[0])
		axarr[slider].set_title(slider_order[slider], fontsize = 18)
		axarr[slider].set_ylabel('Percent movement', fontsize = 18)
		axarr[slider].set_ylim([0.1,.4])
		axarr[slider].tick_params(axis='both', which='major', labelsize=18)

	axarr[3].set_xlabel('Iteration', fontsize = 18)
	f.legend(lines, [mechanism_names_expanded[mechanisms_to_do[i]] for i in range(len(mechanisms_to_do))], loc='upper left', borderaxespad=0., ncol = 4, fontsize = 18)
	print lines
	plt.show()

def analyze_movement_and_weights(organized_data, LABEL):
	averages_byitem = {'0': np.zeros(4), '1set0':np.zeros(4), '1set1':np.zeros(4), '2':np.zeros(4), '3':np.zeros(4), '4':np.zeros(4), '5set0':np.zeros(4), '5set1':np.zeros(4), '6':np.zeros(4), '7':np.zeros(4)}
	averages_bymostmovement = {'0': np.zeros(4), '1set0':np.zeros(4), '1set1':np.zeros(4), '2':np.zeros(4), '3':np.zeros(4), '4':np.zeros(4), '5set0':np.zeros(4), '5set1':np.zeros(4), '6':np.zeros(4), '7':np.zeros(4)}
	averages_creditpercentage = {'0':np.zeros(4), '3':np.zeros(4), '4':np.zeros(4), '7':np.zeros(4)}
	averages_creditpercentage_bymost = {'0':np.zeros(4), '3':np.zeros(4), '4':np.zeros(4), '7':np.zeros(4)}
	num_key_positive = np.zeros(8)
	for key in organized_data:
		for experiment in organized_data[key]:
			num_key_positive[key] += 1
			if key!= 1 and key !=5:
				percentages = get_movement_percentages(experiment)
				if percentages is None:
					print "Did not move at all", experiment['experiment_id']
					continue
				# print key, percentages
				averages_byitem[str(key)] += percentages
				averages_bymostmovement[str(key)] += sorted(percentages, reverse = True)

				if key%4 == 0 or key%4 == 3:
					credit_percentages = get_credit_percentage(experiment)
					averages_creditpercentage[str(key)] += credit_percentages
					averages_creditpercentage_bymost[str(key)] += sorted(credit_percentages, reverse=True)
			else:
				for setnum in range(2):
					percentages = get_movement_percentages(experiment, prepend = 'set' + str(setnum))
					if percentages is None:
						print "Did not move at all", experiment['experiment_id']
						continue
					# print key, percentages
					averages_byitem[str(key) + 'set' + str(setnum)] += percentages
					averages_bymostmovement[str(key) + 'set' + str(setnum)] += sorted(percentages, reverse = True)
		if key!= 1 and key!=5:
			averages_byitem[str(key)] /= num_key_positive[key] 
			averages_bymostmovement[str(key)] /= num_key_positive[key] 
			if key == 0%4 or key%4 == 3:
				averages_creditpercentage[str(key)] /= num_key_positive[key] 
				averages_creditpercentage_bymost[str(key)] /= num_key_positive[key] 
		else:
			for setnum in range(2):
				averages_byitem[str(key) + 'set' + str(setnum)] /= num_key_positive[key] 
				averages_bymostmovement[str(key) + 'set' + str(setnum)] /= num_key_positive[key]
				
	dpoints_byitem = []
	dpoints_bymost = []
	dpoints_credits = []
	dpoints_credits_bymost = []

	for key in range(10):
		for idx in xrange(4):
			averageskey = keyorder[key]
			dpoints_byitem.append([mechanism_names_expanded[key], slider_order[idx], averages_byitem[averageskey][idx]])
			dpoints_bymost.append([mechanism_names_expanded[key], str(idx), averages_bymostmovement[averageskey][idx]])
			if averageskey == '0' or averageskey == '3' or averageskey == '4' or averageskey == '7':
				dpoints_credits.append([mechanism_names_expanded[key], slider_order[idx], averages_creditpercentage[averageskey][idx]])
				dpoints_credits_bymost.append([mechanism_names_expanded[key], str(idx), averages_creditpercentage_bymost[averageskey][idx]])

	barplot(np.array(dpoints_byitem), LABEL, 'Percent of movement', 'Item', slider_order[0:4], mechanism_names_expanded)
	barplot(np.array(dpoints_bymost), LABEL, 'Percent of movement', 'Order by movement', [str(x) for x in xrange(4)], mechanism_names_expanded)
	barplot(np.array(dpoints_credits), LABEL, 'Percent of credits used', 'Item', slider_order[0:4], [mechanism_names_expanded[0], mechanism_names_expanded[4], mechanism_names_expanded[5], mechanism_names_expanded[9]])
	barplot(np.array(dpoints_credits_bymost), LABEL, 'Percent of credits used', 'Order by movement', [str(x) for x in xrange(4)], [mechanism_names_expanded[0], mechanism_names_expanded[4], mechanism_names_expanded[5], mechanism_names_expanded[9]])


def get_credit_percentage(experiment):
	movement = [experiment['question_data']['slider0_creditsused'] , experiment['question_data']['slider1_creditsused'] , experiment['question_data']['slider2_creditsused'] , experiment['question_data']['slider3_creditsused']]
	if sum(movement) < .0001: #did not move
		return None
	return movement/np.sum(movement)

def TwoSetComparisonsAnalysis(comparisonsdata):
	differences_over_time = [[],[],[],[]]

   # get direction, amount of movement per person on the different set (difference from option 1...)
   # plot abs value of difference in amount per item per person
	for experiment in comparisonsdata:
		movement_set0, movement_set1 = get_movement_values_comparisons_sets(experiment)
		differences = np.abs(np.subtract(movement_set0, movement_set1))
		for i in range(0, 4):
			differences_over_time[i].append(differences[i])

	n = len(differences_over_time[0])
	for slider in xrange(0, 4):
		vals = differences_over_time[slider]
		plt.plot(range(n), vals, label = slider_order[slider])
		plt.plot(range(n), np.poly1d(np.polyfit(range(n), vals, 1))(range(n)), label = slider_order[slider])

	plt.title('Comparisons set differences over time', fontsize = 18)
	plt.ylabel('Percent difference', fontsize = 18)
	plt.xlabel('Iteration', fontsize = 18)
	plt.legend(loc='upper left', borderaxespad=0., ncol = 4, fontsize = 18)
	plt.show()

	# for each budget item, sort the options from least to highest. See which option they picked for each, how it different per person.  
	optionsorteddifferences_over_time = [[],[],[],[]]
	set0 = [[], [], [], []]
	set1 = [[], [], [], []]
	for experiment in comparisonsdata:
		set0option0 = experiment['question_data']['set' + '0' + 'option0']
		set0option1 = experiment['question_data']['set' + '0' + 'option1']
		set0option2 = experiment['question_data']['set' + '0' + 'option2']
		set1option0 = experiment['question_data']['set' + '1' + 'option0']
		set1option1 = experiment['question_data']['set' + '1' + 'option1']
		set1option2 = experiment['question_data']['set' + '1' + 'option2']


		for slider in range(0, 4):
			optionvals_set0 = [set0option0[slider], set0option1[slider], set0option2[slider]]
			sorted_set0 = np.argsort(optionvals_set0)
			orderset0 = np.nonzero(sorted_set0 == experiment['question_data']['set0selection'])[0][0]

			optionvals_set1 = [set1option0[slider], set1option1[slider], set1option2[slider]]
			sorted_set1 = np.argsort(optionvals_set1)
			orderset1 = np.nonzero(sorted_set1 == experiment['question_data']['set1selection'])[0][0]

			optionsorteddifferences_over_time[slider].append(abs(orderset0 - orderset1))
			set0[slider].append(orderset0)
			set1[slider].append(orderset1)
	print [np.average(set0[slider]) for slider in range(4)]
	print [np.average(set1[slider]) for slider in range(4)]


	n = len(optionsorteddifferences_over_time[0])
	for slider in xrange(0, 4):
		vals = optionsorteddifferences_over_time[slider]
		print vals
		# plt.plot(range(n), vals, label = slider_order[slider])
		# plt.plot(range(n), np.poly1d(np.polyfit(range(n), vals, 20))(range(n)), label = slider_order[slider])
		movav = movingaverage(vals, len(vals)-1)
		plt.plot(range(len(movav)), movav, label = slider_order[slider])

	plt.title('Comparisons options (ordered) differences over time', fontsize = 18)
	plt.ylabel('Option difference', fontsize = 18)
	plt.xlabel('Iteration', fontsize = 18)
	plt.legend(loc='upper left', borderaxespad=0., ncol = 4, fontsize = 18)
	plt.show()


	return 0

def get_movement_values_comparisons_sets(single_experiment_data):

	new_vals_set0 = [single_experiment_data['question_data']['set0' + 'slider0_loc'], single_experiment_data['question_data']['set0' + 'slider1_loc'], single_experiment_data['question_data']['set0' + 'slider2_loc'], single_experiment_data['question_data']['set0' + 'slider3_loc']]
	previous_vals_set0 = single_experiment_data['question_data']['set0' + 'previous_slider_values'][0:4]
	movement_set0 = np.subtract(new_vals_set0, previous_vals_set0)
	abssum_set0 = sum(abs(movement_set0))
	if abssum_set0 > 0:
		movement_set0 = movement_set0/abssum_set0

	new_vals_set1 = [single_experiment_data['question_data']['set1' + 'slider0_loc'], single_experiment_data['question_data']['set1' + 'slider1_loc'], single_experiment_data['question_data']['set1' + 'slider2_loc'], single_experiment_data['question_data']['set1' + 'slider3_loc']]
	previous_vals_set1 = single_experiment_data['question_data']['set1' + 'previous_slider_values'][0:4]
	movement_set1 = np.subtract(new_vals_set1, previous_vals_set1)
	abssum_set1 = sum(abs(movement_set1))
	if abssum_set1 > 0:
		movement_set1 = movement_set1/abssum_set1
	 
	return movement_set0, movement_set1

def get_movement_percentages(single_experiment_data, prepend = ""):
	if single_experiment_data['question_num']%4 == 2:
		movement = [single_experiment_data['question_data']['slider0_weight'], single_experiment_data['question_data']['slider1_weight'], single_experiment_data['question_data']['slider2_weight'], single_experiment_data['question_data']['slider3_weight']]
	else:
		new_vals = [single_experiment_data['question_data'][prepend + 'slider0_loc'], single_experiment_data['question_data'][prepend + 'slider1_loc'], single_experiment_data['question_data'][prepend + 'slider2_loc'], single_experiment_data['question_data'][prepend + 'slider3_loc']]
		previous_vals = single_experiment_data['question_data'][prepend + 'previous_slider_values'][0:4]
		movement = np.abs(np.subtract(new_vals, previous_vals))
	if sum(movement) < .0001: #did not move
		return None
	return movement/np.sum(movement)

def calculate_time_spent(organized_data, LABEL):
	# For each mechanism, calculate average time spent on each page and plot it in a chuncked bar graph
	pagenames = ['Welcome Page', 'Instructions', 'Mechanism', 'Feedback']

	dpoints = []#np.empty((len(organized_data.keys())* len(pagenames), 3), dtype = )
	for key in organized_data:
		for page in range(0, len(pagenames)):
			# print organized_data[key]
			print [d['time_page' + str(page)] for d in organized_data[key]]
			dpoints.append([mechanism_names_fixed[key], pagenames[page], np.mean([d['time_page' + str(page)] for d in organized_data[key]])])
	barplot(np.array(dpoints), LABEL, 'Time (Seconds)', 'Page', pagenames, mechanism_names_fixed)

def organize_payment(organized_data):
	with open ('bonusinfo_real_run2_finalppl.csv', 'wb') as file:
		writer = csv.writer(file)
		for key in organized_data:
			for d in organized_data[key]:
				writer.writerow([d['worker_ID'], d['question_num'], d['question_data']['explanation'], d['feedback_data']['feedback'],  d['time_page0'],  d['time_page1'],  d['time_page2'],  d['time_page3']])
def print_different_things(organized_data):
	for key in organized_data:
		print "MECHANISM: " + mechanism_names_expanded[key]
		for d in organized_data[key]:
			print d['question_data']['explanation'][0], "\n"
			print d['question_data']['slider0_weight'], d['question_data']['slider1_weight'], d['question_data']['slider2_weight'], d['question_data']['slider3_weight']
			print d['question_data']['slider0_loc'], d['question_data']['slider1_loc'], d['question_data']['slider2_loc'], d['question_data']['slider3_loc']
			print "\n\n"


	for key in organized_data:
		print "MECHANISM: " + mechanism_names_expanded[key]
		for d in organized_data[key]:
			print d['feedback_data']['feedback'][0], "\n"

def payments_new_people(organized_data):
	newids = []
	with open ('newpeople_endof_2ndrun.csv', 'rb') as file:
		reader = csv.reader(file)
		newids = [q[0] for q in list(reader)]
	print newids

	with open ('bonusinfo_real_run2_finalppl222.csv', 'wb') as file:
		writer = csv.writer(file)
		for key in organized_data:
			for d in organized_data[key]:
				if d['worker_ID'] in newids:
					writer.writerow([d['worker_ID'], d['question_num'], d['question_data']['explanation'], d['feedback_data']['feedback'],  d['time_page0'],  d['time_page1'],  d['time_page2'],  d['time_page3']])

def analysis_call(filename, LABEL, mechanism_super_dictionary, do2SetComparisonsAnalysis = False, plotPercentMovementOverTime = False, organizePayment = False, slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', 'Deficit']):
	data, organized_data = clean_data(load_data(filename));

	if do2SetComparisonsAnalysis:
		TwoSetComparisonsAnalysis(organized_data[1])	

	if plotPercentMovementOverTime:
		plot_percent_movements_over_time(organized_data, LABEL)
	
	plot_allmechansisms_together(organized_data, mechanism_super_dictionary, slider_order = slider_order)

	# analyze_data(organized_data, LABEL)

	if organizePayment:
		organize_payment(organized_data)

	# payments_new_people(organized_data)

	# print_different_things(organized_data  )

