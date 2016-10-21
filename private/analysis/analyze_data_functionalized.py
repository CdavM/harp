import csv
import ast
import seaborn as sns
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
from operator import itemgetter
import math
import numpy as np
from data_helpers_multiplesets import *
import cvxpy
import weightedstats as ws
import operator
slider_order = ['Defense', 'Health',
	'Transportation', 'Income Tax', 'Deficit'];
import latexify

def plot_sliders_over_time(data, title, prepend=""):
	n = range(0, len(data) + 1)

	for slider in range(0, len(slider_order)):
		vals = [d['question_data'][prepend + 'slider' +
			str(slider) + '_loc'] for d in data]
		vals.insert(0, initial_values[slider])  # prepend initial values
		plt.plot(n, vals, label=slider_order[slider])
	plt.legend(loc='upper left')

	plt.tick_params(axis='both', which='major')

	# Add the axis labels
	plt.title(title + " " + prepend)
	plt.ylabel('\$ (Billions)')
	plt.xlabel('Iteration')
	plt.savefig(LABEL + '_' + title + prepend + '.pdf', format='pdf', dpi=1000)
	plt.close()


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
	median = {}
	weighted_median = {}
	# print data

	for slider in sliders:
		for d in data:
			if d.has_key(dataname) and d[dataname].has_key(sliderprepend + 'slider' + str(slider) + '0_loc'):
				sliders[slider].append(d[dataname][
					sliderprepend + 'slider' + str(slider) + '0_loc'])
				weights[slider].append(d[dataname][
					sliderprepend + 'slider' + str(slider) + '0_weight'])
	# print sliders, weights

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
		median[slider] = np.median(sliders[slider])
		weighted_median[slider] = ws.weighted_median(sliders[slider], weights = weights[slider])

	return rawaverages, weightedaverages_l2, weightedaverages_l1, calculate_full_elicitation_euclideanpoint(
		data, deficit_offset, dataname, sliderprepend), median, weighted_median

def calculate_full_elicitation_euclideanpoint_iterative(data, deficit_offset, dataname='question_data', sliderprepend=''):
	X = cvxpy.Variable(5)  # 1 point for each mechanism
	fun = 0
	fullelicit = {0:[],1:[],2:[],3:[],4:[]}
	print "started 1 full elicit"
	count = 0
	for d in data:
		print count,
		count+=1
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
		deficit = items[0] + items[1] + items[2] - \
			items[3] + deficit_offset
		items.append(deficit)

		for slider in range(5):
			fullelicit[slider].append(items[slider])

	print "done 1 fullelicit"
	return fullelicit
def calculate_full_elicitation_average_iterative(data, deficit_offset, dataname='question_data', sliderprepend=''):
	sliders = {0: [], 1: [], 2: [], 3: [], 4: []}
	weights = {0: [], 1: [], 2: [], 3: [], 4: []}
	rawaverages = {}
	weightedaverages_l1 = {}
	weightedaverages_l2 = {}
	median = {}
	weighted_median = {}
	# print data

	for slider in sliders:
		for d in data:
			if d.has_key(dataname) and d[dataname].has_key(sliderprepend + 'slider' + str(slider) + '0_loc'):
				sliders[slider].append(d[dataname][
					sliderprepend + 'slider' + str(slider) + '0_loc'])
				weights[slider].append(d[dataname][
					sliderprepend + 'slider' + str(slider) + '0_weight'])
	# print sliders, weights

	# normalize slider weights
	for i in range(len(weights[0])):
		summ = float(sum([weights[slider][i] for slider in weights]))
		for s in weights:
			weights[s][i] /= max(summ, .001)

	for slider in sliders:
		rawaverages[slider] = [np.mean(sliders[slider][0:t]) for t in range(1, len(sliders[slider]))]
		weightedaverages_l1[slider] = [np.average(
			sliders[slider][0:t], weights=weights[slider][0:t]) for t in range(1, len(sliders[slider]))]
		weightedaverages_l2[slider] = [np.average(
			sliders[slider][0:t], weights=[math.pow(x, 2) for x in weights[slider][0:t]])  for t in range(1, len(sliders[slider]))]
		median[slider] = [np.median(sliders[slider][0:t])  for t in range(1, len(sliders[slider][0:t]))]
		weighted_median[slider] = [ws.weighted_median(sliders[slider][0:t], weights = weights[slider][0:t])  for t in range(1, len(sliders[slider]))]

	return rawaverages, weightedaverages_l2, weightedaverages_l1, calculate_full_elicitation_euclideanpoint_iterative(
		data, deficit_offset, dataname, sliderprepend), median, weighted_median

sliderranges = {
0: [199, 801], 1: [699, 1301], 2: [99,701], 3:[1199,1801], 4:[100, 1300]
}

def find_normalized_movement(slidernum, setnum, d):
	initialvals = [d['question_data']['initial_slider' +
		str(slider) + str(setnum) + '_loc'] for slider in range(5)]

	movedtovals = [d['question_data']['slider' +
		str(slider) + str(setnum) + '_loc'] for slider in range(5)]

	radius = d['radius']

	mapped=map(operator.sub, movedtovals, initialvals)
	vals = [x/radius for x in mapped]

	#because a few bugs where movement is more than radius. Problem is not that bad though (only a few people, and no more than 1.5 the radius)
	if abs(vals[slidernum]) > 1.1 and slidernum !=4:
		vals[slidernum] = vals[slidernum]/abs(vals[slidernum])
		print "somehow moved more than radius ", vals, radius, initialvals, movedtovals
	# if slidernum is 4:
	# 	print movedtovals[4], initialvals[4], radius
	return vals[slidernum]

def plot_whether_mechanisms_converged(
	organized_data, mechanism_super_dictionary, slider_order, lines_to_do=None, deficit_offset=0, labels=[''], LABEL='', sliderranges = sliderranges, windowlen = 30):
	if lines_to_do is None:
		lines_to_do = [mechanism_super_dictionary.keys()];

	full_elicitation_averages = {}
	for mech in mechanism_super_dictionary:
		if mechanism_super_dictionary[mech]['type'] == 'full':
			pass
			# rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs, median, weightedmedian = calculate_full_elicitation_average_iterative(
			# 		organized_data[mech], deficit_offset)
			# full_elicitation_averages[mech] = {'rawaverages': rawaverages, 'weightedaverages_l2': weightedaverages_l2,
			# 	'weightedaverages_l1': weightedaverages_l1, 'euclideanprefs': euclideanprefs, 'median' : median, 'weightedmedian' : weightedmedian}
	for ltd in range(len(lines_to_do)):
		legend_names = []
		f, axarr = plt.subplots(5, sharex=True)
		lines = []

		for slider in xrange(0, len(slider_order)):
			axarr[slider].set_ylim([0, 1.001])
			for mechanism in lines_to_do[ltd]:
				if mechanism_super_dictionary[mechanism]['type'] == 'l1' or mechanism_super_dictionary[mechanism]['type'] == 'l2' or mechanism_super_dictionary[mechanism]['type'] == 'linf':
					for set_num in range(mechanism_super_dictionary[mechanism]['numsets']):
						n = range(0, len(organized_data[mechanism]))
						# find normalized movement for this slider (some redundant code in normalizaiton since do by slider)
						vals = [find_normalized_movement(slider, set_num, d) for tt,d in enumerate(organized_data[mechanism])]
						b = np.array(vals).cumsum()
						b[windowlen:] = b[windowlen:] - np.array(vals).cumsum()[:-windowlen] #running sum of windowlen
						b = [abs(b[tt])/min(tt+1, windowlen) for tt in range(len(b))]
						if slider == 4 and mechanism_super_dictionary[mechanism]['type'] == 'linf':
							axarr[slider].set_ylim([0, 2.001])
							# b = [b[tt]/4 for tt in range(len(b))]
						# raw_vals = [d['question_data']['slider' + str(slider) + str(set_num) + '_loc'] for d in organized_data[mechanism]]
						# averages_after_point = [np.average(raw_vals[t:]) for t in range(len(raw_vals))]
						# averages_after_point_differences = [(averages_after_point[tt] - averages_after_point[tt-1])*(len(averages_after_point) - tt + 1) for tt in range(1, len(averages_after_point))]

						# b = [b[tt]/min(tt+1, windowlen) for tt in range(len(b))]


						# if max(abs(np.array(b))) > 1:
						# 	print vals[0:2*windowlen]
						# 	print b[0:2*windowlen]
						l = axarr[slider].plot(n, b, label=mechanism_super_dictionary[
											   mechanism]['name'] + ", Set " + str(set_num))
						if slider == 0:
							lines.append(l[0])
							legend_names.append(mechanism_super_dictionary[mechanism][
												'name'] + ", Set " + str(set_num))

						# l = axarr[slider].plot(range(len(averages_after_point_differences)), averages_after_point_differences, label=mechanism_super_dictionary[
						# 					   mechanism]['name'] + ", Set " + str(set_num) + ", moving average")
						# if slider == 0:
						# 	lines.append(l[0])
						# 	legend_names.append(mechanism_super_dictionary[mechanism][
						# 						'name'] + ", Set " + str(set_num))

						# if slider is 4:
						# 	print vals, b

				if mechanism_super_dictionary[mechanism]['type'] == 'full':
					pass
					# vals = full_elicitation_averages[mechanism]['euclideanprefs'][slider]
					# vals = [(vals[tt] - vals[tt-1]) for tt in range(1, len(vals))]
					# b = np.array(vals).cumsum()
					# b[windowlen:] = b[windowlen:] - np.array(vals).cumsum()[:-windowlen] #running sum of windowlen
					# b = [abs(b[tt])/min(tt+1, windowlen) for tt in range(len(b))]
					# # b = [b[tt]/min(tt+1, windowlen) for tt in range(len(b))]
					#
					# n = range(len(b))
					# l = axarr[slider].plot(n, b, label=mechanism_super_dictionary[
					# 					   mechanism]['name'] + '--maximization solution', linestyle='--', marker='+')
					#
					# if slider == 0:
					# 	lines.append(l[0])
					# 	legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ' maximization solution')

					# vals = full_elicitation_averages[mechanism]['median'][slider]
					# vals = [(vals[tt] - vals[tt-1]) for tt in range(1, len(vals))]
					# b = np.array(vals).cumsum()
					# b[windowlen:] = b[windowlen:] - np.array(vals).cumsum()[:-windowlen] #running sum of windowlen
					# b = [abs(b[tt])/min(tt+1, windowlen) for tt in range(len(b))]
					# # b = [b[tt]/min(tt+1, windowlen) for tt in range(len(b))]
					#
					# # print vals
					# # print b
					# n = range(len(vals))
					# l = axarr[slider].plot(n, b, label=mechanism_super_dictionary[
					# 					   mechanism]['name'] + '--median', linestyle='--', marker='+')
					#
					# if slider == 0:
					# 	lines.append(l[0])
					# 	legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ' median')

					# vals = full_elicitation_averages[mechanism]['weightedmedian'][slider]
					# vals = [(vals[tt] - vals[tt-1]) for tt in range(1, len(vals))]
					# b = np.array(vals).cumsum()
					# b[windowlen:] = b[windowlen:] - np.array(vals).cumsum()[:-windowlen] #running sum of windowlen
					# b = [abs(b[tt])/min(tt+1, windowlen) for tt in range(len(b))]
					# # b = [b[tt]/min(tt+1, windowlen) for tt in range(len(b))]
					#
					# n = range(len(vals))
					# l = axarr[slider].plot(n, b, label=mechanism_super_dictionary[
					# 					   mechanism]['name'] + '--weighted median', linestyle='--', marker='+')

					# if slider == 0:
					# 	lines.append(l[0])
					# 	legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ' weighted median')


			# axarr[slider].set_title(slider_order[slider])
			# axarr[slider].set_ylabel('Norm of movement in window', fontsize=12)
			# axarr[slider].tick_params(axis='both', which='major')

		# axarr[len(slider_order) - 1].set_xlabel('Iteration')

		fs = 10
		if len(legend_names) <= 10:
			fs = 18
		f.legend(lines, legend_names, loc='upper center',
				 borderaxespad=.5, ncol=3)#, fontsize=fs)
		# # plt.xlabel('n')
		plt.xlim([0, 220])
		f.text(0.5, 0.25, 'Deficit', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.41, 'Income Tax', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.58, 'Transportation, Science, \& Education', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.74, 'Healthcare', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.91, 'Defense', ha='center', va='center', fontsize = 5)
		f.text(.5, 0.05, 'Iteration', ha='center', va='center', fontsize = 5)

		f.text(0.06, 0.5, '$\\big|\\big| \\frac{1}{N}\sum_{v_t}\\frac{[x_t | x_{t-1} = x] - x}{r_t}\\big|\\big|$', ha='center', va='center', rotation='vertical', fontsize = 5)

		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()

		# plt.show()
		# plt.tight_layout()
		plt.savefig("" + LABEL + 'movementcumsum_' + labels[ltd] + '.pdf',bbox_inches='tight', format='pdf', dpi=1000)
		plt.close();

def plot_allmechansisms_together(
	organized_data, mechanism_super_dictionary, slider_order, lines_to_do=None, deficit_offset=0, labels=[''], LABEL='', sliderranges = sliderranges, average_iteratively = True):
	if lines_to_do is None:
		lines_to_do = [mechanism_super_dictionary.keys()];

	full_elicitation_averages = {}
	for mech in mechanism_super_dictionary:
		if mechanism_super_dictionary[mech]['type'] == 'full':
			if average_iteratively == False:
				rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs, median, weightedmedian = calculate_full_elicitation_average(
					organized_data[mech], deficit_offset)
			else:
				rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs, median, weightedmedian = calculate_full_elicitation_average_iterative(
					organized_data[mech], deficit_offset)
			full_elicitation_averages[mech] = {'rawaverages': rawaverages, 'weightedaverages_l2': weightedaverages_l2,
				'weightedaverages_l1': weightedaverages_l1, 'euclideanprefs': euclideanprefs, 'median' : median, 'weightedmedian' : weightedmedian}
	for ltd in range(len(lines_to_do)):
		legend_names = []
		f, axarr = plt.subplots(5, sharex=True)
		lines = []

		maxn = 0
		for mechanism in lines_to_do[ltd]:
			if mechanism not in lines_to_do[ltd]:
				continue
			n = range(0, len(organized_data[mechanism]))
			maxn = max(maxn, len(n))

		for slider in xrange(0, len(slider_order)):
			axarr[slider].set_ylim(sliderranges[slider])
			for mechanism in lines_to_do[ltd]:
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
					# if average_iteratively == False:
					# 	vals = [full_elicitation_averages[mechanism]
					# 		['euclideanprefs'][slider] for _ in n]
					# else:
					# 	vals = full_elicitation_averages[mechanism]['euclideanprefs'][slider]
					# 	n = range(len(vals))
					# l = axarr[slider].plot(n, vals, label=mechanism_super_dictionary[
					# 					   mechanism]['name'] + '--maximization solution', linestyle='--', marker='+')
					#
					# if slider == 1:
					# 	print vals[-1],
					# if slider == 0:
					# 	lines.append(l[0])
					# 	legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ' maximization solution')
					if average_iteratively == False:
						vals = [full_elicitation_averages[mechanism]
							['median'][slider] for _ in n]
					else:
						vals = full_elicitation_averages[mechanism]['median'][slider]
						n = range(len(vals))
					l = axarr[slider].plot(n, vals, label=mechanism_super_dictionary[
										   mechanism]['name'] + '--median', linestyle='None', marker='.', color = 'k')
					if slider == 1:
						print vals[-1],
					if slider == 0:
						lines.append(l[0])
						legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ' median')

					# if average_iteratively == False:
					# 	vals = [full_elicitation_averages[mechanism]
					# 		['weightedmedian'][slider] for _ in n]
					# else:
					# 	vals = full_elicitation_averages[mechanism]['weightedmedian'][slider]
					# 	n = range(len(vals))
					# l = axarr[slider].plot(n, vals, label=mechanism_super_dictionary[
					# 					   mechanism]['name'] + '--weighted median', linestyle='--', marker='+')
					#
					# if slider == 1:
					# 	print vals[-1]
					# if slider == 0:
					# 	lines.append(l[0])
					# 	legend_names.append(mechanism_super_dictionary[mechanism]['name'] + ' weighted median')


			# axarr[slider].set_title(slider_order[slider])
			# axarr[slider].set_ylabel('\$ (Billions)')
			# axarr[slider].tick_params(axis='both')

		# axarr[len(slider_order) - 1].set_xlabel('Iteration')

		fs = 10
		if len(legend_names) <= 10:
			fs = 18
		# f.legend(lines, legend_names)
		f.legend(lines, legend_names, loc='upper center',
				 borderaxespad=.5, ncol=4)#, fontsize=fs)
		# # plt.xlabel('n')
		plt.xlim([0, 220])
		f.text(0.5, 0.25, 'Deficit', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.41, 'Income Tax', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.58, 'Transportation, Science, \& Education', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.74, 'Healthcare', ha='center', va='center', fontsize = 5)
		f.text(0.5, 0.91, 'Defense', ha='center', va='center', fontsize = 5)
		f.text(.5, 0.05, 'Iteration', ha='center', va='center', fontsize = 5)

		f.text(0.08, 0.5, '\$ (Billions)', ha='center', va='center', rotation='vertical', fontsize = 5)

		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()

		# plt.show()
		# plt.tight_layout()
		plt.savefig("" + LABEL + labels[ltd] + '.pdf',bbox_inches='tight', format='pdf', dpi=1000)
		plt.close();


def analyze_data_experiment_l2(data):  # constrained movement
	plot_sliders_over_time(data, 'l2 Constrained Movement Mechanism')
	creditsused = []  # histogram of credits used
	for exp in data:
		creditsused.append(calc_credits_used(exp))
	plt.hist(creditsused, bins=10, range=[0, 1])
	# plt.show()
	plt.savefig("" + LABEL + "_l2credits used" + '.pdf', format='pdf', dpi=1000)
	plt.close();

	return None


def analyze_data_experiment_comparisons(data):  # comparisons
	for setnum in range(2):
		plot_sliders_over_time(data, 'Comparison Mechanism', 'set' + str(setnum))
	return None

def analyze_data_experiment_full_allcombined(all_data, LABEL, lines_to_do_fullhist, labels_fullhist, mechanism_super_dictionary):  # ideal points and elicitation

	# plot distribution of points, weights, combining the data for mechanisms in current line to do
	#also plot distribution of deficit - max(others), deficit - min(others)

	f_weights, axarr_weights = plt.subplots(5, sharex=True)
	f_values, axarr_values = plt.subplots(5, sharex=True)
	lines_values = {0:[], 1:[],2:[],3:[],4:[]}
	lines_weights = {0:[], 1:[],2:[],3:[],4:[]}

	mechnames = []
	for mech in [0, 1, 4, 7]:
		mechnames.append(mechanism_super_dictionary[mech]['name'])
		if mechanism_super_dictionary[mech]['type'] == 'full':
			dataname = 'question_data'
		else:
			dataname = 'extra_full_elicitation_data'
		for slider in range(5):
			lines_values[slider].extend([row[dataname]['slider' +
				str(slider) + '0_loc'] for row in all_data[mech] if dataname in row])
			lines_weights[slider].extend([min(10, row[dataname]['slider' +
						   str(slider) + '0_weight']) for row in all_data[mech] if dataname in row])
	for slider in range(5):
		# axarr_values[slider].set_title(slider_order[slider])
		# axarr_weights[slider].set_title(slider_order[slider])
		axarr_values[slider].hist(lines_values[slider], 50, range =[-500, 2500])
		axarr_weights[slider].hist(lines_weights[slider], 30)
		latexify.format_axes(axarr_weights[slider])
		latexify.format_axes(axarr_values[slider])


	axarr_values[0].legend(loc='upper left',
			 borderaxespad=0., ncol=4)
	axarr_weights[0].legend(loc='upper left',
			 borderaxespad=0., ncol=4)

	if max(lines_weights) > 10:
		print weights



	plt.figure(f_weights.number)
	# f_weights.text(0.5, 0.21, 'Deficit', ha='center', va='center', fontsize = 5)
	# f_weights.text(0.5, 0.39, 'Income Tax', ha='center', va='center', fontsize = 5)
	# f_weights.text(0.5, 0.575, 'Transportation, Science, \& Education', ha='center', va='center', fontsize = 5)
	# f_weights.text(0.5, 0.76, 'Healthcare', ha='center', va='center', fontsize = 5)
	# f_weights.text(0.5, 0.94, 'Defense', ha='center', va='center', fontsize = 5)
	# f_weights.text(.5, 0.045, 'Full Elicitation Weight', ha='center', va='center', fontsize = 5)
	# f_weights.text(0.025, 0.5, 'Number of Voters', ha='center', va='center', rotation='vertical', fontsize = 5)
	# plt.tight_layout()
	# plt.savefig(LABEL + '_FullElicitWeights_Alltogether_tight' '.pdf',bbox_inches='tight', format='pdf', dpi=1000)

	f_weights.text(0.5, 0.245, 'Deficit', ha='center', va='center', fontsize = 5)
	f_weights.text(0.5, 0.41, 'Income Tax', ha='center', va='center', fontsize = 5)
	f_weights.text(0.5, 0.575, 'Transportation, Science, \& Education', ha='center', va='center', fontsize = 5)
	f_weights.text(0.5, 0.74, 'Healthcare', ha='center', va='center', fontsize = 5)
	f_weights.text(0.5, 0.91, 'Defense', ha='center', va='center', fontsize = 5)
	f_weights.text(.5, 0.04, 'Full Elicitation Weight', ha='center', va='center', fontsize = 5)
	f_weights.text(0.08, 0.5, 'Number of Voters', ha='center', va='center', rotation='vertical', fontsize = 5)
	plt.savefig(LABEL + '_FullElicitWeights_Alltogether' '.pdf',bbox_inches='tight', format='pdf', dpi=1000)

	plt.figure(f_values.number)
	plt.xlim([-500, 2500])
	f_values.text(0.5, 0.245, 'Deficit', ha='center', va='center', fontsize = 5)
	f_values.text(0.5, 0.41, 'Income Tax', ha='center', va='center', fontsize = 5)
	f_values.text(0.5, 0.575, 'Transportation, Science, \& Education', ha='center', va='center', fontsize = 5)
	f_values.text(0.5, 0.74, 'Healthcare', ha='center', va='center', fontsize = 5)
	f_values.text(0.5, 0.91, 'Defense', ha='center', va='center', fontsize = 5)
	f_values.text(.5, 0.04, 'Full Elicitation Value', ha='center', va='center', fontsize = 5)
	f_values.text(0.08, 0.5, 'Number of Voters', ha='center', va='center', rotation='vertical', fontsize = 5)
	plt.savefig(LABEL + '_FullElicitValues_Alltogether' +'.pdf',bbox_inches='tight', format='pdf', dpi=1000)
	plt.close()

	return None


def analyze_data_experiment_full(all_data, LABEL, lines_to_do_fullhist, labels_fullhist, mechanism_super_dictionary):  # ideal points and elicitation

	# plot distribution of points, weights, combining the data for mechanisms in current line to do
	#also plot distribution of deficit - max(others), deficit - min(others)
	for en,ltd in enumerate(lines_to_do_fullhist):
		f_weights_defminusmin = plt.figure('minusmin')
		f_weights_defminusmax = plt.figure('minusmax')

		f_weights, axarr_weights = plt.subplots(5, sharex=True)
		f_values, axarr_values = plt.subplots(5, sharex=True)
		lines_values = {0:[], 1:[],2:[],3:[],4:[]}
		lines_weights = {0:[], 1:[],2:[],3:[],4:[]}
		lines_weights_minusmin = []
		lines_weights_minusmax = []
		lines_weights_minushealth = []

		mechnames = []
		for mech in ltd:
			mechnames.append(mechanism_super_dictionary[mech]['name'])
			if mechanism_super_dictionary[mech]['type'] == 'full':
				dataname = 'question_data'
			else:
				dataname = 'extra_full_elicitation_data'
			for slider in range(5):
				lines_values[slider].append([row[dataname]['slider' +
					str(slider) + '0_loc'] for row in all_data[mech] if dataname in row])
				lines_weights[slider].append([min(10, row[dataname]['slider' +
							   str(slider) + '0_weight']) for row in all_data[mech] if dataname in row])
			maxes = lines_weights[0][-1]
			mins = lines_weights[0][-1]
			healthweights = lines_weights[1][-1]

			for slider in range(1, 4):
				maxes = [max(lines_weights[slider][-1][i], maxes[i]) for i in range(len(maxes))]
				mins = [min(lines_weights[slider][-1][i], mins[i]) for i in range(len(mins))]
			lines_weights_minusmin.append(map(operator.sub, lines_weights[4][-1], mins))
			lines_weights_minusmax.append(map(operator.sub, lines_weights[4][-1], maxes))
			lines_weights_minushealth.append(map(operator.sub, lines_weights[4][-1], healthweights))

		for slider in range(5):
			axarr_values[slider].set_title(slider_order[slider])
			axarr_weights[slider].set_title(slider_order[slider])
			axarr_values[slider].hist(lines_values[slider], 30, label = mechnames)
			axarr_weights[slider].hist(lines_weights[slider], 30, label = mechnames)
			latexify.format_axes(axarr_weights[slider])
			latexify.format_axes(axarr_values[slider])


		axarr_values[0].legend(loc='upper left',
				 borderaxespad=0., ncol=4)
		axarr_weights[0].legend(loc='upper left',
				 borderaxespad=0., ncol=4)

		if max(lines_weights) > 10:
			print weights


		plt.figure('minushealth')
		plt.title('Deficit Weight - Health Weight')
		plt.hist(lines_weights_minushealth, 30, label = mechnames)
		plt.legend(loc='upper left',
				 borderaxespad=0., ncol=4)
		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()
		plt.tight_layout()
		plt.savefig(LABEL + '_FullElicitWeights_DeficitMinusHealth' + labels_fullhist[en]  + '.pdf', format='pdf', dpi=1000)

		plt.figure('minusmin')
		plt.title('Deficit Weights - Min(other Weights)')
		plt.hist(lines_weights_minusmin, 30, label = mechnames)
		plt.legend(loc='upper left',
				 borderaxespad=0., ncol=4)
		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()
		plt.tight_layout()
		plt.savefig(LABEL + '_FullElicitWeights_DeficitMinusMins' + labels_fullhist[en]  + '.pdf', format='pdf', dpi=1000)

		plt.figure('minusmax')
		plt.title('Deficit Weights - Max(other Weights)')
		plt.hist(lines_weights_minusmax, 30, label = mechnames)
		plt.legend(loc='upper left',
				 borderaxespad=0., ncol=4)
		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()
		plt.tight_layout()
		plt.savefig(LABEL + '_FullElicitWeights_DeficitMinusMaxes' + labels_fullhist[en]  + '.pdf', format='pdf', dpi=1000)

		plt.figure(f_weights.number)
		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()
		# plt.tight_layout()
		plt.savefig(LABEL + '_FullElicitWeights_' + labels_fullhist[en]  + '.pdf', format='pdf', dpi=1000)
		plt.figure(f_values.number)
		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()
		# plt.tight_layout()
		plt.savefig(LABEL + '_FullElicitValues_' + labels_fullhist[en]  + '.pdf', format='pdf', dpi=1000)
		plt.close()

	return None

def plot_histogram_of_credits_used(all_data, LABEL, lines_to_do_creditshist, labels_creditshist, mechanism_super_dictionary):  # ideal points and elicitation

	# plot distribution of credits used by mechanism type
	for en,ltd in enumerate(lines_to_do_creditshist):
		f_credits, axarr_credits = plt.subplots(4, sharex=True)
		lines_credits = {0:[], 1:[],2:[],3:[]}
		mechnames = []
		for mech in ltd:
			if mechanism_super_dictionary[mech]['type'] == 'full':
				continue
			mechnames.append(mechanism_super_dictionary[mech]['name'])
			mechvals = []
			for setnum in range(mechanism_super_dictionary[mech]['numsets']):
				mechvals.extend([get_credit_percentage(row, setnum) for row in all_data[mech]])
			for slider in range(4):
				lines_credits[slider].append([mv[slider] for mv in mechvals])

		for slider in range(4):
			axarr_credits[slider].set_title(slider_order[slider])
			axarr_credits[slider].hist(lines_credits[slider], 10, label = mechnames)
		axarr_credits[0].legend(loc='upper left',
				 borderaxespad=0., ncol=4)

		plt.figure(f_credits.number)
		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()
		plt.savefig(LABEL + '_HistogramOfCreditsUsed_' + labels_creditshist[en]  + '.pdf', format='pdf', dpi=1000)
		plt.close()

	return None

def analyze_data_experiment_l1(data):  # constrained movement
	plot_sliders_over_time(data, 'l1 Constrained Movement Mechanism')
	creditsused = []
	for exp in data:
		creditsused.append(calc_credits_used(exp))
	plt.hist(creditsused, bins=10, range=[0, 1])
	plt.savefig("" + LABEL + "_l1credits used hist" + '.pdf', format='pdf', dpi=1000)
	plt.close();

	# plt.show()

def analyze_data_experiment_linf(data):  # constrained movement
	plot_sliders_over_time(data, 'l1 Constrained Movement Mechanism')
	creditsused = []
	for exp in data:
		creditsused.append(calc_credits_used(exp))
	plt.hist(creditsused, bins=10, range=[0, 1])
	plt.savefig("" + LABEL + "_l1credits used hist" + '.pdf', format='pdf', dpi=1000)
	plt.close();

	# plt.show()

def calc_credits_used(experiment):
	return experiment['question_data']['slider0_creditsused'] + experiment['question_data']['slider1_creditsused'] + experiment['question_data']['slider2_creditsused'] + experiment['question_data']['slider3_creditsused']

switcher_analyze_data = {
	'full': analyze_data_experiment_full,
	'l1': analyze_data_experiment_l1,
	'l2': analyze_data_experiment_l2,
	'full' : analyze_data_experiment_linf,
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
					if mechanism_super_dictionary[key]['type'] == 'l2' or mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'linf':
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
		axarr[slider].set_title(slider_order[slider])
		axarr[slider].set_ylabel('Percent movement')
		axarr[slider].set_ylim([0.1, .4])
		axarr[slider].tick_params(axis='both', which='major')

	axarr[3].set_xlabel('Iteration')
	f.legend(lines, labelnames, loc='upper left',
			 borderaxespad=0., ncol=4)
	# print lines
	plt.savefig("" + LABEL + "_Percent Movements over time" + '.pdf', format='pdf', dpi=1000)
	plt.close();

	# plt.show()

def plot_percent_movements_combined_by_type(organized_data, LABEL, mechanism_super_dictionary, labels, lines_to_do):
	averages_bymostmovement = {}
	averages_creditpercentage_bymost = {}
	num_key_positive = {}
	for key in mechanism_super_dictionary:
		numsets = mechanism_super_dictionary[key]['numsets']
		typekey = mechanism_super_dictionary[key]['type']#str(key) + 'set' + str(setnum)
		for experiment in organized_data[key]:
			for setnum in range(numsets):
				num_key_positive[typekey] = num_key_positive.get(typekey, 0) + 1
				if typekey not in averages_bymostmovement:
					averages_bymostmovement[typekey] = np.zeros(4)
					averages_creditpercentage_bymost[typekey] = np.zeros(4)

				percentages = get_movement_percentages(
					experiment, setnum, mechanism_super_dictionary[key])
				if percentages is None:
					print "Did not move at all", experiment['experiment_id']
					continue
				averages_bymostmovement[
					typekey] += sorted(percentages, reverse=True)

				if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2'or mechanism_super_dictionary[key]['type'] == 'linf':
					credit_percentages = get_credit_percentage(
						experiment, setnum)
					if credit_percentages is not None:
						averages_creditpercentage_bymost[
							typekey] += sorted(credit_percentages, reverse=True)

	for key in averages_bymostmovement:
		averages_bymostmovement[key] /= num_key_positive[key]
		if key == 'l1' or key == 'l2' or key == 'linf':
			averages_creditpercentage_bymost[
				key] /= num_key_positive[key]

	dpoints_bymost = []
	dpoints_credits_bymost = []
	labelnames = []
	labelnames_credit = []
	labelnamesbykey = {'linf' : '$L^\infty$', 'l2' : '$L^2$', 'l1' : '$L^1$', 'full' : 'Full Elicitation Weights'}
	xnames = ['First', 'Second', 'Third', 'Fourth']
	for key in ['full', 'l1', 'l2', 'linf']:#averages_bymostmovement:
		labelnames.append(labelnamesbykey[key])
		for idx in xrange(4):
			dpoints_bymost.append(
				[labelnames[-1], xnames[idx], averages_bymostmovement[key][idx]])
			if key == 'l1' or key == 'l2' or key == 'linf':
				if labelnames[-1] not in labelnames_credit:
					labelnames_credit.append(labelnames[-1])
				dpoints_credits_bymost.append(
					[labelnames[-1], xnames[idx], averages_creditpercentage_bymost[key][idx]])
	barplot(np.array(dpoints_bymost), LABEL+"PercentOfMovement_by_order_all", 'Movement as fraction of radius',
			'Ranking of dimensions by movement for each voter', xnames, labelnames)
	barplot(np.array(dpoints_credits_bymost), LABEL+"PercentOfCredits_by_order_all", 'Percent of credits used',
			'Order by movement', xnames, labelnames_credit)

def analyze_movement_and_weights(organized_data, LABEL, mechanism_super_dictionary, labels, lines_to_do):
	for ltd in range(len(lines_to_do)):
		averages_byitem = {}
		averages_bymostmovement = {}
		averages_creditpercentage = {}
		averages_creditpercentage_bymost = {}
		num_key_positive = np.zeros(len(mechanism_super_dictionary))
		for key in lines_to_do[ltd]:
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

					if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2'or mechanism_super_dictionary[key]['type'] == 'linf':
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
				if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2' or mechanism_super_dictionary[key]['type'] == 'linf':
					averages_creditpercentage[strkey] /= num_key_positive[key]
					averages_creditpercentage_bymost[
						strkey] /= num_key_positive[key]

		dpoints_byitem = []
		dpoints_bymost = []
		dpoints_credits = []
		dpoints_credits_bymost = []
		labelnames = []
		labelnames_credit = []
		for key in lines_to_do[ltd]:
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
					if mechanism_super_dictionary[key]['type'] == 'l1' or mechanism_super_dictionary[key]['type'] == 'l2' or mechanism_super_dictionary[key]['type'] == 'linf':
						if labelnames[-1] not in labelnames_credit:
							labelnames_credit.append(labelnames[-1])
						dpoints_credits.append(
							[labelnames[-1], slider_order[idx], averages_creditpercentage[averageskey][idx]])
						dpoints_credits_bymost.append(
							[labelnames[-1], str(idx), averages_creditpercentage_bymost[averageskey][idx]])
		barplot(np.array(dpoints_byitem), LABEL+"PercentOfMovement_by_item_"+labels[ltd], 'Percent of movement',
				'Item', slider_order[0:4], labelnames)
		barplot(np.array(dpoints_bymost), LABEL+"PercentOfMovement_by_order_"+labels[ltd], 'Percent of movement',
				'Order by movement', [str(x) for x in xrange(4)], labelnames)
		barplot(np.array(dpoints_credits), LABEL+"PercentOfCredits_by_item_"+labels[ltd], 'Percent of credits used',
				'Item', slider_order[0:4], labelnames_credit)
		barplot(np.array(dpoints_credits_bymost), LABEL+"PercentOfCredits_by_order_"+labels[ltd], 'Percent of credits used',
				'Order by movement', [str(x) for x in xrange(4)], labelnames_credit)


def get_credit_percentage(experiment, setnum):
	movement = [experiment['question_data']['slider0' + str(setnum) + '_creditsused'], experiment['question_data']['slider1' + str(setnum) + '_creditsused'], experiment[
															'question_data']['slider2' + str(setnum) + '_creditsused'], experiment['question_data']['slider3' + str(setnum) + '_creditsused']]
	# if sum(movement) < .0001:  # did not move
		# return None
	# return movement / np.sum(movement)
	return movement

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

	plt.title('Comparisons set differences over time')
	plt.ylabel('Percent difference')
	plt.xlabel('Iteration')
	plt.legend(loc='upper left', borderaxespad=0., ncol=4)
	plt.savefig("" + LABEL + "_2 set comparison diff over time" + '.pdf', format='pdf', dpi=1000)
	plt.close();

	# plt.show()

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
	# print [np.average(set0[slider]) for slider in range(4)]
	# print [np.average(set1[slider]) for slider in range(4)]

	n = len(optionsorteddifferences_over_time[0])
	for slider in xrange(0, 4):
		vals = optionsorteddifferences_over_time[slider]
		print vals
		# plt.plot(range(n), vals, label = slider_order[slider])
		# plt.plot(range(n), np.poly1d(np.polyfit(range(n), vals, 20))(range(n)),
		# label = slider_order[slider])
		movav = movingaverage(vals, len(vals) - 1)
		plt.plot(range(len(movav)), movav, label=slider_order[slider])

	plt.title('Comparisons options (ordered) differences over time')
	plt.ylabel('Option difference')
	plt.xlabel('Iteration')
	plt.legend(loc='upper left', borderaxespad=0., ncol=4)
	plt.savefig("" + LABEL + "_2set comparison analysis ordered difference over time" + '.pdf', format='pdf', dpi=1000)
	plt.close();

	# plt.show()

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


def get_movement_percentages_ofradius(single_experiment_data, setnum, mechanism_super_dictionary_specificmech, getsignsaswell=False):
	signs = None
	if mechanism_super_dictionary_specificmech['type'] == 'full':
		movement = [single_experiment_data['question_data']['slider00_weight'], single_experiment_data['question_data'][
			'slider10_weight'], single_experiment_data['question_data']['slider20_weight'], single_experiment_data['question_data']['slider30_weight']]
		radius = 10.0
	else:
		new_vals = [single_experiment_data['question_data']['slider0' + str(setnum) + '_loc'], single_experiment_data['question_data']['slider1' + str(
			setnum) + '_loc'], single_experiment_data['question_data']['slider2' + str(setnum) + '_loc'], single_experiment_data['question_data']['slider3' + str(setnum) + '_loc']]
		previous_vals = single_experiment_data['question_data'][
			'previous_slider_values' + str(setnum)][0:4]
		movement = np.abs(np.subtract(new_vals, previous_vals))
		signs = np.sign(np.subtract(new_vals, previous_vals))
		radius = float(single_experiment_data['radius'])
	if getsignsaswell:
		return [m / radius for m in movement], signs
	else:
		return [m / radius for m in movement]

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
			# print [d['time_page' + str(page)] for d in organized_data[key]]
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


	bysign_fullaswellconditioning = {'linf' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}},'l2' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}, 'l1' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}}

	bysign = {}
	differences = {}
	differences_fullaswellconditioning = {'linf' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}},'l2' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}, 'l1' : {'Ideal point above both' : {}, 'Ideal point between' : {}, 'Ideal point below both' : {}}}

	# get signs and differences separated by item and mechanism
	for key in organized_data:
		if not (mechanism_super_dictionary[key]['type'] == 'l2' or mechanism_super_dictionary[key]['type'] == 'l1'  or mechanism_super_dictionary[key]['type'] == 'linf'):
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
		# print dpoints_signs
		barplot(np.array(dpoints_signs), LABEL + ' Direction of Movement', 'Number',
				'Directions', signorder, labelnames_signs, axarr[item], item == 3, item == 0)
		axarr[item].set_title(slider_order[item])


	alll1 = {0:[], 1:[], 2:[], 3:[]}
	alll2 = {0:[], 1:[], 2:[], 3:[]}
	alllinf = {0:[], 1:[], 2:[], 3:[]}

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
			elif mechanism_super_dictionary[key]['type'] is 'linf':
				alllinf[item] = np.append(alll2[item], differences[key][item])

		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()

		plt.suptitle('Differences in percent movement per budget item, ' + mechanism_super_dictionary[key]['name'])
		plt.savefig(LABEL + 'Differences in percent movement' + mechanism_super_dictionary[key]['name'] +'.pdf', format='pdf', dpi=1000)
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
	# mng = plt.get_current_fig_manager()
	# mng.window.showMaximized()

	plt.savefig(LABEL + 'Combined Differences in percent movement'+'.pdf', format='pdf', dpi=1000)
	plt.close()


	#for the mechanisms in which also did full elicitation, plot the signs histogram
	for keylinfl2orl1 in bysign_fullaswellconditioning:
		labelnames_signs = []
		signorder = []
		f, axarr = plt.subplots(4, sharex=True)
		lines = []
		for item in range(4):
			ind = -1
			dpoints_signs = []
			for key in bysign_fullaswellconditioning[keylinfl2orl1]:
				ind+=1
				if key not in labelnames_signs:
					labelnames_signs.append(key)

				for signkey in bysign_fullaswellconditioning[keylinfl2orl1][key][item]:
					if signkey not in signorder:
						signorder.append(signkey)
					dpoints_signs.append(
						[labelnames_signs[ind], signkey, bysign_fullaswellconditioning[keylinfl2orl1][key][item][signkey]])
			# print dpoints_signs
			barplot(np.array(dpoints_signs), LABEL + ' Direction of Movement Conditioned on Full,' + keylinfl2orl1, 'Number',
					'Directions', signorder, labelnames_signs, axarr[item], item == 3, item == 0)
			axarr[item].set_title(slider_order[item])

	#for those same mechanisms, plot the differences histogram
	for keylinfl2orl1 in differences_fullaswellconditioning:
		f, axarr = plt.subplots(4, sharex=True)
		for key in differences_fullaswellconditioning[keylinfl2orl1]:
			for item in range(4):
				axarr[item].hist(differences_fullaswellconditioning[keylinfl2orl1][key][item], alpha = .5, range = (0, 2), bins = 30, label = key)
				axarr[item].set_title(slider_order[item])
				if item is 0:
					axarr[item].legend(loc='upper right')

		# mng = plt.get_current_fig_manager()
		# mng.window.showMaximized()

		plt.suptitle('Differences in percent movement per budget item, Conditioned on full, ' + str(keylinfl2orl1))
		plt.savefig(LABEL + 'Differences in percent movement, Conditioned on full, ' + str(keylinfl2orl1) + '.pdf', format='pdf', dpi=1000)
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

def analyze_extra_full_elicitation(data, mechanism_super_dictionary_value, mech_key, LABEL, slider_order, deficit_offset = 0, average_iteratively = True):
	legend_names = []
	f, axarr = plt.subplots(5, sharex=True)
	lines = []
	if average_iteratively:
		rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs, median, weightedmedian = calculate_full_elicitation_average_iterative(data, deficit_offset, dataname = 'extra_full_elicitation_data', sliderprepend = '')
	else:
		rawaverages, weightedaverages_l2, weightedaverages_l1, euclideanprefs, median, weightedmedian = calculate_full_elicitation_average(data, deficit_offset, dataname = 'extra_full_elicitation_data', sliderprepend = '')
	full_elicitation_averages = {'rawaverages': rawaverages, 'weightedaverages_l2': weightedaverages_l2, 'weightedaverages_l1': weightedaverages_l1, 'euclideanprefs': euclideanprefs, 'median' : median, 'weightedmedian' : weightedmedian}

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
		if average_iteratively == False:
			vals = [full_elicitation_averages
				['euclideanprefs'][slider] for _ in n]
		else:
			vals = full_elicitation_averages['euclideanprefs'][slider]
			n = range(len(vals))
		l = axarr[slider].plot(n, vals, label = 'Mechanism specific full maximization', linestyle = '--', marker = '+')

		if slider == 0:
			lines.append(l[0])
			legend_names.append('Mechanism specific full maximization')


		n = range(maxn)
		if average_iteratively == False:
			vals = [full_elicitation_averages
				['median'][slider] for _ in n]
		else:
			vals = full_elicitation_averages['median'][slider]
			n = range(len(vals))
		l = axarr[slider].plot(n, vals, label = 'Mechanism specific full median', linestyle = '--', marker = '+')

		if slider == 0:
			lines.append(l[0])
			legend_names.append('Mechanism specific full median')

		n = range(maxn)
		if average_iteratively == False:
			vals = [full_elicitation_averages
				['weightedmedian'][slider] for _ in n]
		else:
			vals = full_elicitation_averages['weightedmedian'][slider]
			n = range(len(vals))
		l = axarr[slider].plot(n, vals, label = 'Mechanism specific full weighted median', linestyle = '--', marker = '+')

		if slider == 0:
			lines.append(l[0])
			legend_names.append('Mechanism specific full weighted median')

		axarr[slider].set_title(slider_order[slider], fontsize = 18)
		axarr[slider].set_ylabel('\$ (Billions)', fontsize = 18)
		axarr[slider].tick_params(axis='both', which='major')

	axarr[len(slider_order)-1].set_xlabel('Iteration', fontsize = 18)
	f.legend(lines,legend_names , loc='upper center', borderaxespad=0., ncol = 3, fontsize = 18)


	# mng = plt.get_current_fig_manager()
	# mng.window.showMaximized()

	# plt.show()
	plt.savefig("" + LABEL + '_FullElicitation Extra, Group ' + str(mech_key)  + '.pdf', format='pdf', dpi=1000)
	plt.close();

def analysis_call(filename, LABEL, mechanism_super_dictionary, alreadyPaidFiles = None, lines_to_do = None, labels = [''], \
 analyzeUtilityFunctions = False, analyzeExtraFull = False, plotHistogramOfFull = False, \
 lines_to_do_fullhist = None, labels_fullhist = None, plotAllOverTime = False, \
 do2SetComparisonsAnalysis = False, plotPercentMovementOverTime = False, organizePayment = False, \
 slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', 'Deficit'], \
 deficit_offset = 0, average_iteratively = True, plotConvergenceAnalysis = False, \
 lines_to_do_creditshist = None, labels_creditshist = None):

	data, organized_data = clean_data(load_data(filename), mechanism_super_dictionary, deficit_offset);

	latexify.latexify()

	if do2SetComparisonsAnalysis:
		TwoSetComparisonsAnalysis(organized_data[1])

	if plotPercentMovementOverTime:
		plot_percent_movements_over_time(organized_data, LABEL, mechanism_super_dictionary)

	if plotHistogramOfFull:
		analyze_data_experiment_full_allcombined(organized_data, LABEL, lines_to_do_fullhist, labels_fullhist, mechanism_super_dictionary)
		# analyze_data_experiment_full(organized_data, LABEL, lines_to_do_fullhist, labels_fullhist, mechanism_super_dictionary)

	if analyzeUtilityFunctions:
		# plot_percent_movements_over_time(organized_data, LABEL, mechanism_super_dictionary)
		# plot_histogram_of_credits_used(organized_data, LABEL, lines_to_do_creditshist, labels_creditshist, mechanism_super_dictionary)
		plot_percent_movements_combined_by_type(organized_data, LABEL, mechanism_super_dictionary, labels, lines_to_do)
		# analyze_movement_and_weights (organized_data, LABEL, mechanism_super_dictionary, labels, lines_to_do)
		# analyze_utility_functions(organized_data, LABEL, mechanism_super_dictionary);

	if plotAllOverTime:
		plot_allmechansisms_together(organized_data, mechanism_super_dictionary, slider_order = slider_order, deficit_offset = deficit_offset, labels = labels, lines_to_do = lines_to_do, LABEL = LABEL, average_iteratively = average_iteratively)

	if plotConvergenceAnalysis:
		plot_whether_mechanisms_converged(organized_data, mechanism_super_dictionary, slider_order = slider_order, deficit_offset = deficit_offset, labels = labels, lines_to_do = lines_to_do, LABEL = LABEL)

	if analyzeExtraFull:
		for key in mechanism_super_dictionary:
			if mechanism_super_dictionary[key]['do_full_as_well']:
				analyze_extra_full_elicitation(organized_data[key], mechanism_super_dictionary[key], key, LABEL, slider_order = slider_order, deficit_offset = deficit_offset, average_iteratively = average_iteratively)



	# analyze_data(organized_data, LABEL)

	if organizePayment:
		organize_payment(organized_data, LABEL, mechanism_super_dictionary, alreadyPaidFiles)

	# payments_new_people(organized_data)

	# print_different_things(organized_data  )
