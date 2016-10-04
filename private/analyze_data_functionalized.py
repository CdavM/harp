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
from data_helpers_multiplesets import *
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


def calculate_full_elicitation_euclideanpoint(data, deficit_offset, dataname='question_data', sliderprepend=''):
	X = cvxpy.Variable(5)  # 1 point for each mechanism
	fun = 0
	for d in data:
		if dataname not in d:
			continue
		y = [d[dataname][sliderprepend + 'slider' +
			str(slider) + '0_loc'] for slider in range(5)]
		w = [d[dataname][sliderprepend + 'slider' +
			str(slider) + '0_weight'] for slider in range(5)]
		sumsq = max(.001, math.sqrt(sum([math.pow(w[i], 2) for i in range(5)])))
		w = [w[i] / sumsq for i in range(5)]
		for slider in range(5):
			fun += w[slider] * cvxpy.abs(X[slider] - y[slider])
	obj = cvxpy.Minimize(fun)
	constraints = [X >= 0, X[0] + X[1] + X[2] -
		X[3] + deficit_offset == X[4]]
	prob = cvxpy.Problem(obj, constraints)
	result = prob.solve()
	items = [X.value[i, 0] for i in range(5)]
	print 'Optimal full elicitation:', items
	deficit = items[0] + items[1] + items[2] - \
		items[3] + deficit_offset
	items.append(deficit)
	return items


def calculate_full_elicitation_average(data, deficit_offset, dataname='question_data', sliderprepend=''):
	sliders = {0: [], 1: [], 2: [], 3: [], 4: []}
	weights = {0: [], 1: [], 2: [], 3: [], 4: []}
	rawaverages = {}
	weightedaverages_l1 = {}
	weightedaverages_l2 = {}

	print data

	for slider in sliders:
		for d in data:
			if d.has_key(dataname) and d[dataname].has_key(sliderprepend + 'slider' + str(slider) + '0_loc'):
				sliders[slider].append(d[dataname][
					sliderprepend + 'slider' + str(slider) + '0_loc'])
				weights[slider].append(d[dataname][
					sliderprepend + 'slider' + str(slider) + '0_weight'])
	print sliders, weights

	# normalize slider weights
	for i in range(len(weights[0])):
		summ = float(sum([weights[slider][i] for slider in weights]))
		for s in weights:
			weights[s][i] /= max(summ, .001)

	for slider in sliders:
		rawaverages[slider] = np.mean(sliders[slider])
		weightedaverages_l1[slider] = np.average(
			sliders[slider], weights=weights[slider])
		weightedaverages_l2[slider] = np.average(
			sliders[slider], weights=[math.pow(x, 2) for x in weights[slider]])

	return rawaverages, weightedaverages_l2, weightedaverages_l1, calculate_full_elicitation_euclideanpoint(
		data, deficit_offset, dataname, sliderprepend)


def plot_allmechansisms_together(
	organized_data, mechanism_super_dictionary, slider_order, lines_to_do=None, deficit_offset=0, labels=[''], LABEL=''):
	if lines_to_do is None:
		lines_to_do = [mechanism_super_dictionary.keys()];

	for ltd in range(len(lines_to_do)):
		legend_names = []
		f, axarr = plt.subplots(5, sharex=True)
		lines = []

		full_elicitation_averages = {}
		for mech in mechanism_super_dictionary:
			if mechanism_super_dictionary[mech]['type'] == 'full':
				rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs = calculate_full_elicitation_average(
					organized_data[mech], deficit_offset)
				full_elicitation_averages[mech] = {'rawaverages': rawaverages, 'weightedaverages_l2': weightedaverages_l2,
					'weightedaverages_l1': weightedaverages_l1, 'euclideanprefs': euclideanprefs}

		maxn = 0
		for mechanism in mechanism_super_dictionary:
			if mechanism not in lines_to_do[ltd]:
				continue
			n = range(0, len(organized_data[mechanism]))
			maxn = max(maxn, len(n))

		for slider in xrange(0, len(slider_order)):
			for mechanism in mechanism_super_dictionary:
				if mechanism not in lines_to_do[ltd]:
					continue
				if mechanism_super_dictionary[mechanism]['type'] == 'l1' or mechanism_super_dictionary[mechanism]['type'] == 'l2' or mechanism_super_dictionary[mechanism]['type'] == 'linf':
					for set_num in range(mechanism_super_dictionary[mechanism]['numsets']):
						n = range(0, len(organized_data[mechanism]))
						maxn = max(maxn, len(n))
						# initial instead of actual for averaging purposes
						vals = [d['question_data']['initial_slider' +
							str(slider) + str(set_num) + '_loc'] for d in organized_data[mechanism]]
						l = axarr[slider].plot(n, vals, label=mechanism_super_dictionary[
											   mechanism]['name'] + ", Set " + str(set_num))
						if slider == 0:
							lines.append(l[0])
							legend_names.append(mechanism_super_dictionary[mechanism][
												'name'] + ", Set " + str(set_num))

			# comparisons
				if mechanism_super_dictionary[mechanism]['type'] == 'comparisons':
					for set_num in range(mechanism_super_dictionary[mechanism]['numsets']):
						n = range(0, len(organized_data[mechanism]))
						maxn = max(maxn, len(n))
						vals = [d['question_data'][
							'set' + str(set_num) + 'slider' + str(slider) + '_loc'] for d in organized_data[mechanism]]
						l = axarr[slider].plot(n, vals, label=mechanism_super_dictionary[
											   mechanism]['name'] + ", Set " + str(set_num))
						if slider == 0:
							lines.append(l[0])
							legend_names.append(mechanism_super_dictionary[mechanism][
												'name'] + ", Set " + str(set_num))

				n = range(maxn)
				if mechanism_super_dictionary[mechanism]['type'] == 'full':
					vals = [full_elicitation_averages[mechanism]
						['euclideanprefs'][slider] for _ in n]
					l = axarr[slider].plot(n, vals, label=mechanism_super_dictionary[
										   mechanism]['name'], linestyle='--', marker='+')

					if slider == 0:
						lines.append(l[0])
						legend_names.append(mechanism_super_dictionary[mechanism]['name'])

			axarr[slider].set_title(slider_order[slider], fontsize=18)
			axarr[slider].set_ylabel('$ (Billions)', fontsize=18)
			axarr[slider].tick_params(axis='both', which='major', labelsize=18)

		axarr[len(slider_order) - 1].set_xlabel('Iteration', fontsize=18)
		f.legend(lines, legend_names, loc='upper center',
				 borderaxespad=0., ncol=3, fontsize=18)

		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()

		# plt.show()
		plt.savefig("" + LABEL + labels[ltd] + '.png')
		plt.close();


def analyze_data_experiment_l2(data):  # constrained movement
	plot_sliders_over_time(data, 'l2 Constrained Movement Mechanism')
	creditsused = []  # histogram of credits used
	for exp in data:
		creditsused.append(calc_credits_used(exp))
	plt.hist(creditsused, bins=10, range=[0, 1])
	plt.show()
	return None


def analyze_data_experiment_comparisons(data):  # comparisons
	for setnum in range(2):
		plot_sliders_over_time(data, 'Comparison Mechanism', 'set' + str(setnum))
	return None


def analyze_data_experiment_full(data):  # ideal points and elicitation
	f_weights, axarr_weights = plt.subplots(5, sharex=False)
	f_values, axarr_values = plt.subplots(5, sharex=False)

	lines_values = []
	lines_weights = []

	# plot distribution of points, weights
	for slider in range(5):
		values = [row['question_data']['slider' +
			str(slider) + '0_loc'] for row in data]
		weights = [min(10, row['question_data']['slider' +
					   str(slider) + '0_weight']) for row in data]
		axarr_values[slider].hist(values, 40)
		axarr_weights[slider].hist(weights, 40)
		if max(weights) > 10:
			print weights

	plt.show()
	return None


def analyze_data_experiment_l1(data):  # constrained movement
	plot_sliders_over_time(data, 'l1 Constrained Movement Mechanism')
	creditsused = []
	for exp in data:
		creditsused.append(calc_credits_used(exp))
	plt.hist(creditsused, bins=10, range=[0, 1])
	plt.show()


def calc_credits_used(experiment):
	return experiment['question_data']['slider0_creditsused'] + experiment['question_data']['slider1_creditsused'] + experiment['question_data']['slider2_creditsused'] + experiment['question_data']['slider3_creditsused']

switcher_analyze_data = {
	'full': analyze_data_experiment_full,
	'l1': analyze_data_experiment_l1,
	'l2': analyze_data_experiment_l2,
	'comparisons': analyze_data_experiment_comparisons
}


def analyze_data(organized_data, LABEL, lines_to_do):
	# for comparisons & constrained movement, plot the locations for each slider (with labels) and deficit over time
	# for raw elicitation, calculate the minimizer (optimal point)
	# also calculate average time for each mechanism
	# calculate_time_spent(organized_data, LABEL)

	for key in organized_data:
		if key not in lines_to_do[0]:
			continue
		print switcher_analyze_data[key](organized_data[key])
	# analyze_movement_and_weights(organized_data, LABEL)

slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]


def movingaverage(interval, window_size):
	window = np.ones(int(window_size)) / float(window_size)
	return np.convolve(interval, window, 'valid')


def plot_percent_movements_over_time(organized_data, LABEL, mechanism_super_dictionary):
	averages_byitem = {}
	averages_bymostmovement = {}
	averages_creditpercentage = {}
	averages_creditpercentage_bymost = {}
	for key in organized_data:
		numsets = mechanism_super_dictionary[key]['numsets']
		for experiment in organized_data[key]:
			for setnum in range(numsets):
				strkey = str(key) + 'set' + str(setnum)
				if strkey not in averages_byitem:
					averages_byitem[strkey] = [[], [], [], []]
					averages_bymostmovement[strkey] = [[], [], [], []]
					averages_creditpercentage[strkey] = [[], [], [], []]
					averages_creditpercentage_bymost[strkey] = [[], [], [], []]

				if mechanism_super_dictionary[key]['type'] != 'comparisons':
					percentages = get_movement_percentages(
						experiment, setnum, mechanism_super_dictionary[key])
					if percentages is None:
						print "Did not move at all", experiment['experiment_id']
						continue
					for i in range(len(percentages)):
						averages_byitem[strkey][i].append(percentages[i])
						averages_bymostmovement[strkey][i].append(
							sorted(percentages, reverse=True)[i])
					if mechanism_super_dictionary[key]['type'] == 'l2' or mechanism_super_dictionary[key]['type'] == 'l1':
						credit_percentages = get_credit_percentage(experiment, setnum)
						if credit_percentages is not None:
							for i in range(len(credit_percentages)):
								averages_creditpercentage[strkey][i].append(credit_percentages[i])
								averages_creditpercentage_bymost[strkey][i].append(
									sorted(credit_percentages, reverse=True)[i])
				else:
					for setnum in range(0, 2):
						percentages = get_movement_percentages(
							experiment, setnum, mechanism_super_dictionary[key])
						if percentages is None:
							print "Did not move at all", experiment['experiment_id']
							continue
						for i in range(len(percentages)):
							averages_byitem[strkey][i].append(percentages[i])
							averages_bymostmovement[strkey][i].append(
								sorted(percentages, reverse=True)[i])

	f, axarr = plt.subplots(4, sharex=True)
	lines = []
	labelnames = []
	for slider in xrange(0, 4):
		for key in organized_data:
			numsets = mechanism_super_dictionary[key]['numsets']
			for setnum in range(numsets):
				strkey = str(key) + 'set' + str(setnum)
				labelnames.append(mechanism_super_dictionary[key][
								  'name'] + ", Set " + str(setnum))
				n = range(0, len(averages_byitem[strkey][slider]))
				vals = averages_byitem[strkey][slider]
				l = axarr[slider].plot(n, vals, label=labelnames[-1],
									   linestyle='None', marker='.')
				# plot line of best fit
				# l = axarr[slider].plot(n, np.poly1d(np.polyfit(n, vals, 1))(n), label =
				# mechanism_names_expanded[mechanism])
				mvgs = movingaverage(vals, 10)
				# l = axarr[slider].plot(range(len(mvgs)),mvgs, label =
				# mechanism_names_expanded[mechanism])

				if slider == 0:
					lines.append(l[0])
		axarr[slider].set_title(slider_order[slider], fontsize=18)
		axarr[slider].set_ylabel('Percent movement', fontsize=18)
		axarr[slider].set_ylim([0.1, .4])
		axarr[slider].tick_params(axis='both', which='major', labelsize=18)

	axarr[3].set_xlabel('Iteration', fontsize=18)
	f.legend(lines, labelnames, loc='upper left',
			 borderaxespad=0., ncol=4, fontsize=18)
	print lines
	plt.show()


def analyze_movement_and_weights(organized_data, LABEL, mechanism_super_dictionary):
	averages_byitem = {}
	averages_bymostmovement = {}
	averages_creditpercentage = {}
	averages_creditpercentage_bymost = {}
	num_key_positive = np.zeros(len(mechanism_super_dictionary))
	for key in organized_data:
		numsets = mechanism_super_dictionary[key]['numsets']
		for experiment in organized_data[key]:
			num_key_positive[key] += 1
			for setnum in range(numsets):
				strkey = str(key) + 'set' + str(setnum)
				if strkey not in averages_byitem:
					averages_byitem[strkey] = np.zeros(4)
					averages_bymostmovement[strkey] = np.zeros(4)
					averages_creditpercentage[strkey] = np.zeros(4)
					averages_creditpercentage_bymost[strkey] = np.zeros(4)

				percentages = get_movement_percentages(
					experiment, setnum, mechanism_super_dictionary[key])
				if percentages is None:
					print "Did not move at all", experiment['experiment_id']
					continue
				# print key, percentages
				averages_byitem[strkey] += percentages
				averages_bymostmovement[
					strkey] += sorted(percentages, reverse=True)

				if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2':
					credit_percentages = get_credit_percentage(
						experiment, setnum)
					if credit_percentages is not None:
						averages_creditpercentage[strkey] += credit_percentages
						averages_creditpercentage_bymost[
							strkey] += sorted(credit_percentages, reverse=True)

		for setnum in range(numsets):
			strkey = str(key) + 'set' + str(setnum)
			averages_byitem[strkey] /= num_key_positive[key]
			averages_bymostmovement[strkey] /= num_key_positive[key]
			if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2':
				averages_creditpercentage[strkey] /= num_key_positive[key]
				averages_creditpercentage_bymost[
					strkey] /= num_key_positive[key]

	dpoints_byitem = []
	dpoints_bymost = []
	dpoints_credits = []
	dpoints_credits_bymost = []
	labelnames = []
	labelnames_credit = []
	for key in mechanism_super_dictionary:
		numsets = mechanism_super_dictionary[key]['numsets']
		for setnum in range(numsets):
			averageskey = str(key) + 'set' + str(setnum)
			labelnames.append(mechanism_super_dictionary[key][
							  'name'] + ", Set " + str(setnum))
			for idx in xrange(4):
				dpoints_byitem.append(
					[labelnames[-1], slider_order[idx], averages_byitem[averageskey][idx]])
				dpoints_bymost.append(
					[labelnames[-1], str(idx), averages_bymostmovement[averageskey][idx]])
				if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2':
					if labelnames[-1] not in labelnames_credit:
						labelnames_credit.append(labelnames[-1])
					dpoints_credits.append(
						[labelnames[-1], slider_order[idx], averages_creditpercentage[averageskey][idx]])
					dpoints_credits_bymost.append(
						[labelnames[-1], str(idx), averages_creditpercentage_bymost[averageskey][idx]])
	barplot(np.array(dpoints_byitem), LABEL, 'Percent of movement',
			'Item', slider_order[0:4], labelnames)
	barplot(np.array(dpoints_bymost), LABEL, 'Percent of movement',
			'Order by movement', [str(x) for x in xrange(4)], labelnames)
	barplot(np.array(dpoints_credits), LABEL, 'Percent of credits used',
			'Item', slider_order[0:4], labelnames_credit)
	barplot(np.array(dpoints_credits_bymost), LABEL, 'Percent of credits used',
			'Order by movement', [str(x) for x in xrange(4)], labelnames_credit)


def get_credit_percentage(experiment, setnum):
	movement = [experiment['question_data']['slider0' + str(setnum) + '_creditsused'], experiment['question_data']['slider1' + str(setnum) + '_creditsused'], experiment[
															'question_data']['slider2' + str(setnum) + '_creditsused'], experiment['question_data']['slider3' + str(setnum) + '_creditsused']]
	if sum(movement) < .0001:  # did not move
		return None
	return movement / np.sum(movement)


def TwoSetComparisonsAnalysis(comparisonsdata):
	differences_over_time = [[], [], [], []]

   # get direction, amount of movement per person on the different set (difference from option 1...)
   # plot abs value of difference in amount per item per person
	for experiment in comparisonsdata:
		movement_set0, movement_set1 = get_movement_values_comparisons_sets(
			experiment)
		differences = np.abs(np.subtract(movement_set0, movement_set1))
		for i in range(0, 4):
			differences_over_time[i].append(differences[i])

	n = len(differences_over_time[0])
	for slider in xrange(0, 4):
		vals = differences_over_time[slider]
		plt.plot(range(n), vals, label=slider_order[slider])
		plt.plot(range(n), np.poly1d(np.polyfit(range(n), vals, 1))
				 (range(n)), label=slider_order[slider])

	plt.title('Comparisons set differences over time', fontsize=18)
	plt.ylabel('Percent difference', fontsize=18)
	plt.xlabel('Iteration', fontsize=18)
	plt.legend(loc='upper left', borderaxespad=0., ncol=4, fontsize=18)
	plt.show()

	# for each budget item, sort the options from least to highest. See which
	# option they picked for each, how it different per person.
	optionsorteddifferences_over_time = [[], [], [], []]
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
			optionvals_set0 = [set0option0[slider],
				set0option1[slider], set0option2[slider]]
			sorted_set0 = np.argsort(optionvals_set0)
			orderset0 = np.nonzero(sorted_set0 == experiment[
								   'question_data']['set0selection'])[0][0]

			optionvals_set1 = [set1option0[slider],
				set1option1[slider], set1option2[slider]]
			sorted_set1 = np.argsort(optionvals_set1)
			orderset1 = np.nonzero(sorted_set1 == experiment[
								   'question_data']['set1selection'])[0][0]

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
		# plt.plot(range(n), np.poly1d(np.polyfit(range(n), vals, 20))(range(n)),
		# label = slider_order[slider])
		movav = movingaverage(vals, len(vals) - 1)
		plt.plot(range(len(movav)), movav, label=slider_order[slider])

	plt.title('Comparisons options (ordered) differences over time', fontsize=18)
	plt.ylabel('Option difference', fontsize=18)
	plt.xlabel('Iteration', fontsize=18)
	plt.legend(loc='upper left', borderaxespad=0., ncol=4, fontsize=18)
	plt.show()

	return 0


def get_movement_values_comparisons_sets(single_experiment_data):

	new_vals_set0 = [single_experiment_data['question_data']['set0' + 'slider0_loc'], single_experiment_data['question_data']['set0' + 'slider1_loc'],
		single_experiment_data['question_data']['set0' + 'slider2_loc'], single_experiment_data['question_data']['set0' + 'slider3_loc']]
	previous_vals_set0 = single_experiment_data[
		'question_data']['set0' + 'previous_slider_values'][0:4]
	movement_set0 = np.subtract(new_vals_set0, previous_vals_set0)
	abssum_set0 = sum(abs(movement_set0))
	if abssum_set0 > 0:
		movement_set0 = movement_set0 / abssum_set0

	new_vals_set1 = [single_experiment_data['question_data']['set1' + 'slider0_loc'], single_experiment_data['question_data']['set1' + 'slider1_loc'],
		single_experiment_data['question_data']['set1' + 'slider2_loc'], single_experiment_data['question_data']['set1' + 'slider3_loc']]
	previous_vals_set1 = single_experiment_data[
		'question_data']['set1' + 'previous_slider_values'][0:4]
	movement_set1 = np.subtract(new_vals_set1, previous_vals_set1)
	abssum_set1 = sum(abs(movement_set1))
	if abssum_set1 > 0:
		movement_set1 = movement_set1 / abssum_set1

	return movement_set0, movement_set1


def get_movement_percentages(single_experiment_data, setnum, mechanism_super_dictionary_specificmech, getsignsaswell=False):
	signs = None
	if mechanism_super_dictionary_specificmech['type'] == 'full':
		movement = [single_experiment_data['question_data']['slider00_weight'], single_experiment_data['question_data'][
			'slider10_weight'], single_experiment_data['question_data']['slider20_weight'], single_experiment_data['question_data']['slider30_weight']]
	else:
		new_vals = [single_experiment_data['question_data']['slider0' + str(setnum) + '_loc'], single_experiment_data['question_data']['slider1' + str(
			setnum) + '_loc'], single_experiment_data['question_data']['slider2' + str(setnum) + '_loc'], single_experiment_data['question_data']['slider3' + str(setnum) + '_loc']]
		previous_vals = single_experiment_data['question_data'][
			'previous_slider_values' + str(setnum)][0:4]
		movement = np.abs(np.subtract(new_vals, previous_vals))
		signs = np.sign(np.subtract(new_vals, previous_vals))
	if sum(movement) < .0001:  # did not move
		if getsignsaswell:
			return None, None
		else:
			return None

	if getsignsaswell:
		return movement / np.sum(movement), signs
	else:
		return movement / np.sum(movement)


def calculate_time_spent(organized_data, LABEL):
	# For each mechanism, calculate average time spent on each page and plot
	# it in a chuncked bar graph
	pagenames = ['Welcome Page', 'Instructions', 'Mechanism', 'Feedback']

	# np.empty((len(organized_data.keys())* len(pagenames), 3), dtype = )
	dpoints = []
	for key in organized_data:
		for page in range(0, len(pagenames)):
			# print organized_data[key]
			print [d['time_page' + str(page)] for d in organized_data[key]]
			dpoints.append([mechanism_names_fixed[key], pagenames[page], np.mean(
				[d['time_page' + str(page)] for d in organized_data[key]])])
	barplot(np.array(dpoints), LABEL, 'Time (Seconds)',
			'Page', pagenames, mechanism_names_fixed)


def analyze_utility_functions(organized_data, LABEL, mechanism_super_dictionary):

# 			i. % of people that decreased/increased/constant both, or different things for each
# 					a) Split by mechanism
# 					b) Split by budget item as well
# 				1) For people that increased & decreased an item, how far apart were the points, and how much did they move -- just print out a list...
# 					a) For people that did the same thing, how far apart & how much did they move in each
# ii. Normalize weights learned from l2/l1 to percentage (sum to 1), with
# positive for increase, negative for decrease. Then do histogram of
# differences for each budget mechanism

# loop through each l2/l1 mechanism:
	# separately for each mechanism, for each budget item, keep track of how many increased/decreased/kept constant (have a threshold for constant)
	# also keep track of histogram of percent differences for each budget item in each mechanism
		# abs(difference of percent)
		# plot histogram in single large plot -- stacked by budget item, 1 for each mechanism?
			# depedning on how similar across l2/l1, 1 for l1, and 1 for l2, maybe combine into the same plot
	# depending on above results:
		# see who increased & decreased, and what we can learn about them.


	bysign_fullaswellconditioning = {'l2' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}, 'l1' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}}

	bysign = {}
	differences = {}
	differences_fullaswellconditioning = {'l2' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}, 'l1' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}}

	# get signs and differences separated by item and mechanism
	for key in organized_data:
		if not (mechanism_super_dictionary[key]['type'] == 'l2' or mechanism_super_dictionary[key]['type'] == 'l1'):
			continue
		if key not in bysign:
			bysign[key] = {}
			differences[key] = {}
		for experiment in organized_data[key]:
			per0, signs0 = get_movement_percentages(
				experiment, 0, mechanism_super_dictionary[key], getsignsaswell=True)
			per1, signs1 = get_movement_percentages(
				experiment, 1, mechanism_super_dictionary[key], getsignsaswell=True)
			if per0 is None or per1 is None:
				continue
			do_full_as_well = mechanism_super_dictionary[key]['do_full_as_well']
			for item in range(4):
				if do_full_as_well and 'extra_full_elicitation_data' in experiment:
					directionset0 = np.sign(experiment['extra_full_elicitation_data']['slider' + str(item) + str(0) + '_loc'] - experiment['question_data']['initial_slider' + str(item) + str(0) + '_loc'])
					directionset1 = np.sign(experiment['extra_full_elicitation_data']['slider' + str(item) + str(0) + '_loc'] - experiment['question_data']['initial_slider' + str(item) + str(1) + '_loc'])
					keyfullaswell = ''
					if directionset0 > 0 and directionset1 > 0:
						keyfullaswell = 'Ideal point above both'
					elif (directionset0 > 0 and directionset1) < 0 or (directionset0 < 0 and directionset1 > 0):
						keyfullaswell = 'Ideal point between'
					elif directionset0 < 0 and directionset1 < 0:
						keyfullaswell = 'Ideal point below both'
					else:
						print 'somehow equal to ideal point', experiment

					if keyfullaswell not in bysign_fullaswellconditioning[mechanism_super_dictionary[key]['type']]:
						bysign_fullaswellconditioning[mechanism_super_dictionary[key]['type']][keyfullaswell] = {}
						differences_fullaswellconditioning[mechanism_super_dictionary[key]['type']][keyfullaswell] = {}

					signskeyitem_fullconditioning = bysign_fullaswellconditioning[mechanism_super_dictionary[key]['type']][keyfullaswell].get(
							item, {'00': 0, '01': 0, '11': 0, '-1-1': 0, '0-1': 0, '1-1': 0})
					difkeyitem_fullaswell = differences_fullaswellconditioning[mechanism_super_dictionary[key]['type']][keyfullaswell].get(item, [])

				difkeyitem = differences[key].get(item, [])
				signskeyitem = bysign[key].get(
					item, {'00': 0, '01': 0, '11': 0, '-1-1': 0, '0-1': 0, '1-1': 0})

				difkeyitem.append(abs(signs1[item]*per1[item] - signs0[item]*per0[item]))

				if do_full_as_well and 'extra_full_elicitation_data' in experiment:
					difkeyitem_fullaswell.append(abs(signs1[item]*per1[item] - signs0[item]*per0[item]))

				if signs1[item] == 0 and signs0[item] == 0:
					signskeyitem['00'] += 1
					if do_full_as_well and 'extra_full_elicitation_data' in experiment:
						signskeyitem_fullconditioning['00'] += 1;
				elif signs1[item] == -1 and signs0[item] == -1:
					signskeyitem['-1-1'] += 1
					if do_full_as_well and 'extra_full_elicitation_data' in experiment:
						signskeyitem_fullconditioning['-1-1'] += 1;
				elif signs1[item] == 1 and signs0[item] == 1:
					signskeyitem['11'] += 1
					if do_full_as_well and 'extra_full_elicitation_data' in experiment:
						signskeyitem_fullconditioning['11'] += 1;
				elif (signs1[item] == -1 and signs0[item] == 1) or (signs1[item] == 1 and signs0[item] == -1):
					signskeyitem['1-1'] += 1
					if do_full_as_well and 'extra_full_elicitation_data' in experiment:
						signskeyitem_fullconditioning['1-1'] += 1;
				elif (signs1[item] == 0 and signs0[item] == 1) or (signs1[item] == 1 and signs0[item] == 0):
					signskeyitem['01'] += 1
					if do_full_as_well and 'extra_full_elicitation_data' in experiment:
						signskeyitem_fullconditioning['01'] += 1;
				elif (signs1[item] == -1 and signs0[item] == 0) or (signs1[item] == 0 and signs0[item] == -1):
					signskeyitem['0-1'] += 1
					if do_full_as_well and 'extra_full_elicitation_data' in experiment:
						signskeyitem_fullconditioning['0-1'] += 1;

				differences[key][item] = difkeyitem
				bysign[key][item] = signskeyitem
				if do_full_as_well and 'extra_full_elicitation_data' in experiment:
					bysign_fullaswellconditioning[mechanism_super_dictionary[key]['type']][keyfullaswell][item] = signskeyitem_fullconditioning
					differences_fullaswellconditioning[mechanism_super_dictionary[key]['type']][keyfullaswell][item] = difkeyitem_fullaswell

	# plot things -- barplot of signs by budget item, mechanism (1 plot);
	# histogram of differences by budget item, mechanism (1 separate per
	# mechanism, then combine by l2/l1)
	labelnames_signs = []
	signorder = []
	f, axarr = plt.subplots(4, sharex=True)
	lines = []
	for item in range(4):
		ind = -1
		dpoints_signs = []
		for key in mechanism_super_dictionary:
			if key not in bysign:
				continue
			ind+=1
			if mechanism_super_dictionary[key]['name'] not in labelnames_signs:
				labelnames_signs.append(mechanism_super_dictionary[key][
							  'name'])

			for signkey in bysign[key][item]:
				if signkey not in signorder:
					signorder.append(signkey)
				dpoints_signs.append(
					[labelnames_signs[ind], signkey, bysign[key][item][signkey]])
		print dpoints_signs
		barplot(np.array(dpoints_signs), LABEL + ' Direction of Movement', 'Number',
				'Directions', signorder, labelnames_signs, axarr[item], item == 3, item == 0)
		axarr[item].set_title(slider_order[item])


	alll1 = {0:[], 1:[], 2:[], 3:[]}
	alll2 = {0:[], 1:[], 2:[], 3:[]}
	for key in mechanism_super_dictionary:
		if key not in differences:
			continue
		f, axarr = plt.subplots(4, sharex=True)

		for item in range(4):
			axarr[item].hist(differences[key][item], range = (0, 2), bins = 30)
			axarr[item].set_title(slider_order[item])
			if mechanism_super_dictionary[key]['type'] is 'l1':
				alll1[item] = np.append(alll1[item], differences[key][item])
			elif mechanism_super_dictionary[key]['type'] is 'l2':
				alll2[item] = np.append(alll2[item], differences[key][item])
		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()

		plt.suptitle('Differences in percent movement per budget item, ' + mechanism_super_dictionary[key]['name'])
		plt.savefig(LABEL + 'Differences in percent movement' + mechanism_super_dictionary[key]['name'] +'.png')
		#plt.show()
		plt.close()

	f, axarr = plt.subplots(4, sharex=True)
	for item in range(4):
		axarr[item].set_title(slider_order[item])
		axarr[item].hist(alll1[item],alpha = .5, range = (0, 2), bins = 30, label = 'l1')
		axarr[item].hist(alll2[item],alpha = .5, range = (0, 2), bins = 30, label = 'l2')
		if item is 0:
			axarr[item].legend(loc='upper right')
	plt.suptitle('Differences in percent movement per budget item')
	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()

	plt.savefig(LABEL + 'Combined Differences in percent movement'+'.png')
	plt.show()


	#for the mechanisms in which also did full elicitation, plot the signs histogram
	for keyl2orl1 in bysign_fullaswellconditioning:
		labelnames_signs = []
		signorder = []
		f, axarr = plt.subplots(4, sharex=True)
		lines = []
		for item in range(4):
			ind = -1
			dpoints_signs = []
			for key in bysign_fullaswellconditioning[keyl2orl1]:
				ind+=1
				if key not in labelnames_signs:
					labelnames_signs.append(key)

				for signkey in bysign_fullaswellconditioning[keyl2orl1][key][item]:
					if signkey not in signorder:
						signorder.append(signkey)
					dpoints_signs.append(
						[labelnames_signs[ind], signkey, bysign_fullaswellconditioning[keyl2orl1][key][item][signkey]])
			print dpoints_signs
			barplot(np.array(dpoints_signs), LABEL + ' Direction of Movement Conditioned on Full,' + keyl2orl1, 'Number',
					'Directions', signorder, labelnames_signs, axarr[item], item == 3, item == 0)
			axarr[item].set_title(slider_order[item])

	#for those same mechanisms, plot the differences histogram
	for keyl2orl1 in differences_fullaswellconditioning:
		f, axarr = plt.subplots(4, sharex=True)
		for key in differences_fullaswellconditioning[keyl2orl1]:
			for item in range(4):
				axarr[item].hist(differences_fullaswellconditioning[keyl2orl1][key][item], alpha = .5, range = (0, 2), bins = 30, label = key)
				axarr[item].set_title(slider_order[item])
				if item is 0:
					axarr[item].legend(loc='upper right')

		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()

		plt.suptitle('Differences in percent movement per budget item, Conditioned on full, ' + str(keyl2orl1))
		plt.savefig(LABEL + 'Differences in percent movement, Conditioned on full, ' + str(keyl2orl1) + '.png')
		#plt.show()
		plt.close()

def organize_payment(organized_data, LABEL, mechanism_super_dictionary, alreadyPaidFiles = None):
	alreadyPaid = []
	if alreadyPaidFiles is not None:
		for alreadyPaidFile in alreadyPaidFiles:
			with open (alreadyPaidFile, 'rb') as file:
				reader = csv.reader(file)
				for row in reader:
					alreadyPaid.append(row[0]);

	print alreadyPaid

	with open (LABEL + '_bonusinfo.csv', 'wb') as file:
		writer = csv.writer(file)

		for key in organized_data:
			lengthlist = []
			arraylist = []
			length_list_for_mechanism =[]
			for d in organized_data[key]:
				if d['worker_ID'] in alreadyPaid:
					continue
				if len(d['feedback_data']['feedback']) == 0:
					d['feedback_data']['feedback'] = ['']
				if mechanism_super_dictionary[key]['do_full_as_well'] and 'extra_full_elicitation_data' in d:
					length_list_for_mechanism.append(len(d['question_data']['explanation'][0]) + len(d['extra_full_elicitation_data']['explanation'][0]) + len(d['feedback_data']['feedback'][0]))
				else:
					length_list_for_mechanism.append(len(d['question_data']['explanation'][0]) + len(d['feedback_data']['feedback'][0]))
			sortedlength = sorted(length_list_for_mechanism)[int(.2*len(length_list_for_mechanism))] #find 80th percentile

			for d in organized_data[key]:
				if d['worker_ID'] in alreadyPaid:
					continue
				if len(d['feedback_data']['feedback']) == 0:
					d['feedback_data']['feedback'] = ['']
				if mechanism_super_dictionary[key]['do_full_as_well'] and 'extra_full_elicitation_data' in d:
					bonuspayment = .4; #incrased base due to extra do_full_as_well
					lengthextra = len(d['question_data']['explanation'][0]) + len(d['extra_full_elicitation_data']['explanation'][0]) + len(d['feedback_data']['feedback'][0])
					if lengthextra >= sortedlength:
						bonuspayment+= .5 #bonus on top of increased base
					lengthlist.append(lengthextra)
					arraylist.append([d['worker_ID'], bonuspayment, d['question_num'], d['question_data']['explanation'][0], d['extra_full_elicitation_data']['explanation'][0], d['feedback_data']['feedback'][0],  d['time_page0'],  d['time_page1'],  d['time_page2'],  d['time_page3'], d['time_page4']])
				else:
					bonuspayment = 0;
					lengthextra = len(d['question_data']['explanation'][0]) + len(d['feedback_data']['feedback'][0])
					if lengthextra >= sortedlength:
						bonuspayment+= .4 #bonus on top of increased base
					lengthlist.append(lengthextra)
					arraylist.append([d['worker_ID'], bonuspayment, d['question_num'], d['question_data']['explanation'][0], '', d['feedback_data']['feedback'][0],  d['time_page0'],  d['time_page1'],  d['time_page2'],  d['time_page4']])
			order = np.argsort(lengthlist)[::-1]

			arraylist = [arraylist[i] for i in order]
			writer.writerows(arraylist)
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

def analyze_extra_full_elicitation(data, mechanism_super_dictionary_value, mech_key, LABEL, slider_order, deficit_offset = 0):
	legend_names = []
	f, axarr = plt.subplots(5, sharex=True)
	lines = []
	rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs = calculate_full_elicitation_average(data, deficit_offset, dataname = 'extra_full_elicitation_data', sliderprepend = '')
	full_elicitation_averages = {'rawaverages': rawaverages, 'weightedaverages_l2': weightedaverages_l2, 'weightedaverages_l1': weightedaverages_l1, 'euclideanprefs': euclideanprefs}

	maxn = 25
	for slider in xrange(0, len(slider_order)):
		for set_num in range(mechanism_super_dictionary_value['numsets']):
			n = range(0, len(data))
			maxn = max(maxn, len(n))
			vals = [d['question_data']['initial_slider' + str(slider) + str(set_num) + '_loc'] for d in data] #initial instead of actual for averaging purposes
			l = axarr[slider].plot(n, vals, label = mechanism_super_dictionary_value['name'] + ", Set " + str(set_num))
			if slider == 0:
				lines.append(l[0])
				legend_names.append(mechanism_super_dictionary_value['name'] + ", Set " + str(set_num))

		n = range(maxn)
		vals = [full_elicitation_averages['euclideanprefs'][slider] for _ in n]
		l = axarr[slider].plot(n, vals, label = 'Mechanism specific full elicitation', linestyle = '--', marker = '+')

		if slider == 0:
			lines.append(l[0])
			legend_names.append('Mechanism specific full elicitation')

		axarr[slider].set_title(slider_order[slider], fontsize = 18)
		axarr[slider].set_ylabel('$ (Billions)', fontsize = 18)
		axarr[slider].tick_params(axis='both', which='major', labelsize=18)

	axarr[len(slider_order)-1].set_xlabel('Iteration', fontsize = 18)
	f.legend(lines,legend_names , loc='upper center', borderaxespad=0., ncol = 3, fontsize = 18)


	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()

	# plt.show()
	plt.savefig("" + LABEL + '_FullElicitation Extra, Group ' + str(mech_key)  + '.png')
	plt.close();

def analysis_call(filename, LABEL, mechanism_super_dictionary, alreadyPaidFiles = None, lines_to_do = None, labels = [''], analyzeUtilityFunctions = False, analyzeExtraFull = False, plotHistogramOfFull = False, plotAllOverTime = False, do2SetComparisonsAnalysis = False, plotPercentMovementOverTime = False, organizePayment = False, slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', 'Deficit'], deficit_offset = 0):
	data, organized_data = clean_data(load_data(filename), mechanism_super_dictionary, deficit_offset);

	if do2SetComparisonsAnalysis:
		TwoSetComparisonsAnalysis(organized_data[1])

	if plotPercentMovementOverTime:
		plot_percent_movements_over_time(organized_data, LABEL, mechanism_super_dictionary)

	if plotHistogramOfFull:
		for key in mechanism_super_dictionary:
			if mechanism_super_dictionary[key]['type'] == "full":
				analyze_data_experiment_full(organized_data[key])

	if plotAllOverTime:
		plot_allmechansisms_together(organized_data, mechanism_super_dictionary, slider_order = slider_order, deficit_offset = deficit_offset, labels = labels, lines_to_do = lines_to_do, LABEL = LABEL)

	if analyzeExtraFull:
		for key in mechanism_super_dictionary:
			if mechanism_super_dictionary[key]['do_full_as_well']:
				analyze_extra_full_elicitation(organized_data[key], mechanism_super_dictionary[key], key, LABEL, slider_order = slider_order, deficit_offset = deficit_offset)


	if analyzeUtilityFunctions:
		# plot_percent_movements_over_time(organized_data, LABEL, mechanism_super_dictionary)
		# analyze_movement_and_weights (organized_data, LABEL, mechanism_super_dictionary)
		analyze_utility_functions(organized_data, LABEL, mechanism_super_dictionary);

	# analyze_data(organized_data, LABEL)

	if organizePayment:
		organize_payment(organized_data, LABEL, mechanism_super_dictionary, alreadyPaidFiles)

	# payments_new_people(organized_data)

	# print_different_things(organized_data  )
