# code to determine randomization scheme
import math
import random
import numpy as np
import cvxpy
import csv
import sys
from data_helpers_multiplesets import *

def load_sample_people_from_file(filename_forloadingpeople, superdictionary_forloadingpeople, deficit_offset_forloadingpeople):
    data, organized_data = clean_data(load_data(
        filename_forloadingpeople), superdictionary_forloadingpeople, deficit_offset_forloadingpeople);
    persons = []
    for row in organized_data[2]:  # full elicitation in most filenames
        ideals = [row['question_data']['slider' +
            str(slider) + '0_loc'] for slider in range(5)]
        ideals[2] = ideals[2] + 88 #added education to new experiment
        weights = [row['question_data']['slider' +
            str(slider) + '0_weight'] for slider in range(5)]
        persons.append([ideals, weights])
    return persons

# Workers have some ideal point, weights on each


def create_ideal_points_and_weights(
    num_items=5, centers=[425, 1200, 350, 1450, 753], weight_centers=[8, 8, 6, 5, 5]):
	centers[4] = calculate_deficit(centers, deficit_offset=228)
	ideals = []
	weights = []
	for i in range(num_items):
		ideals.append(min(max(0.01, np.random.normal(
		    loc=centers[i], scale=centers[i] * .3)), centers[i] * 2))
		# ideals.append(np.random.uniform(
		    # low=centers[i] * .25, high=centers[i] * 1.75));
		    # low=centers[i] * .5, high=centers[i] * 1.5));
		weights.append(
		    min(10, max(0.01, np.random.normal(weight_centers[i], scale=2))));
	return [ideals, weights]


def calculate_deficit(values, deficit_offset=228):
	return values[0] + values[1] + values[2] - values[3] + deficit_offset;


def intialize_mechanisms(mechanism_super_dictionary):
	mechanisms = {}
	for mech in range(len(mechanism_super_dictionary)):
		for setnum in range(mechanism_super_dictionary[mech]['numsets']):
			mechanism_super_dictionary[mech]['initial_values'][setnum][4] = calculate_deficit(
			    mechanism_super_dictionary[mech]['initial_values'][setnum])

		if mechanism_super_dictionary[mech]['type'] == 'comparisons':
			mechanisms[mech] = {'question_ID': mechanism_super_dictionary[mech][
			    'type'], 'values': mechanism_super_dictionary[mech]['initial_values'], 'number_previous': 0, 'busy': False, 'averaging_status_array': [-100] * mechanism_super_dictionary[mech]['num_to_average_per_step']}
			for setnum in range(mechanism_super_dictionary[mech]['numsets']):
				for item in range(4):
					mechanisms[mech]["set" + str(setnum) + "slider" + str(item) +
					                  "1"] = mechanism_super_dictionary[mech]['initial_values'][setnum][item]
	 	else:
		 	mechanisms[mech] = {'question_ID': mechanism_super_dictionary[mech][
		 	    'type'], 'values': mechanism_super_dictionary[mech]['initial_values'], 'number_previous': 0, 'busy': False, 'num_to_average_per_step': mechanism_super_dictionary[mech]['num_to_average_per_step'], 'averaging_array': np.zeros((mechanism_super_dictionary[mech]['numsets'], mechanism_super_dictionary[mech]['num_to_average_per_step'], 5)), 'averaging_status_array': [-100] * mechanism_super_dictionary[mech]['num_to_average_per_step']}
	return mechanisms


def radius_fn(num_previous, radius_parameters):
	if radius_parameters['radius_type'] == 'constant':
		return float(radius_parameters['starting']);
	elif radius_parameters['radius_type'] == 'decreasing':
		return float(radius_parameters['starting']) / (num_previous + 1);
	elif radius_parameters['radius_type'] == 'decreasing_slow':
		return float(radius_parameters['starting']) / (math.floor(num_previous / float(radius_parameters['decrease_every'])) + 1)


def get_turker_times(num_turkers, window_length, max_turkers_per_window):
	turker_times = []
	num_windows = int(math.ceil(num_turkers / max_turkers_per_window))
	for window in range(num_windows):
		loc = []
		for i in range(max_turkers_per_window):
			loc.append(random.uniform(window_length *
			           window, window_length * (window + 1)))
		turker_times = np.append(turker_times, sorted(loc))
	return turker_times


def do_mechanism(turker_idealpt, mechanism_assignment,
                 mechanisms, time_of_last_turker, turker_time, mechanism_super_dictionary, deficit_offset, radius_parameters, current_avg_number):
	row = fill_out_preliminaries(
	    {}, mechanism_assignment, mechanisms, turker_time, mechanism_super_dictionary[mechanism_assignment]['numsets'], deficit_offset, radius_parameters, current_avg_number)

	time_of_last_turker[mechanism_assignment] = turker_time
	row = simulate_person(turker_idealpt, mechanism_assignment, mechanisms,
	                      row, mechanism_super_dictionary, deficit_offset, current_avg_number)

	return row;


def fill_out_preliminaries(row, mechanism_assignment, mechanisms, turker_time, numsets, deficit_offset, radius_parameters, current_avg_number):
	row['worker_ID'] = 'NA'
	row['asg_ID'] = 'NA'
	row['initial_time'] = int(turker_time)
	row['begin_time'] = int(turker_time)
	row['experiment_id'] = sum(
	    [mechanisms[m]['number_previous'] for m in mechanisms])
	row['current_question'] = mechanism_assignment
	row['experiment_finished'] = True
	row['begin_experiment'] = True
	row['num_of_previous_participants'] = mechanisms[
	    mechanism_assignment]['number_previous']
	row['current_answer'] = 0
	for setnum in range(numsets):
		row['initial_slider0' +
		    str(setnum)] = mechanisms[mechanism_assignment]['values'][setnum][0]
		row['initial_slider1' +
		    str(setnum)] = mechanisms[mechanism_assignment]['values'][setnum][1]
		row['initial_slider2' +
		    str(setnum)] = mechanisms[mechanism_assignment]['values'][setnum][2]
		row['initial_slider3' +
		    str(setnum)] = mechanisms[mechanism_assignment]['values'][setnum][3]
		row['initial_deficit' + str(setnum)] = calculate_deficit(
		    mechanisms[mechanism_assignment]['values'][setnum], deficit_offset);
	row['timer'] = 100;
	row['radius'] = radius_fn(mechanisms[mechanism_assignment][
	                          'number_previous'], radius_parameters)

	# print row
	return row


def check_busy(mechanism, time, time_of_last_turker,
               busy_time=6):
	return check_busy_times(time_of_last_turker[mechanism], time, busy_time)


def check_busy_times(time_last, current_time, busy_time=6):
	return (time_last > current_time - busy_time)


def assignment_david_option2(
    time_of_last_turker, time, mechanism_super_dictionary, TIME_IN_MECHANISM, probabilities=None):
	if probabilities is None:
		probabilities = [1.0 / len(mechanism_super_dictionary.keys())
		                           for _ in range(len(mechanism_super_dictionary.keys()))]
	all_busy = True;

	for mech in mechanism_super_dictionary.keys():
		all_busy = all_busy and check_busy(
		    mech, time, time_of_last_turker, busy_time=TIME_IN_MECHANISM)

	if all_busy:
		return 0;
	else:
		mechanism = np.random.choice(
		    range(len(mechanism_super_dictionary.keys())), p=probabilities)
		while check_busy(mechanism, time, time_of_last_turker):
			mechanism = np.random.choice(
			    range(len(mechanism_super_dictionary.keys())), p=probabilities)
		return mechanism


def assignment_pregeneratedlist(time_of_last_turker, time, lst):
	index = 0;
	while lst[index] != 2 and check_busy(lst[index], time, time_of_last_turker):
		index += 1
	mech = lst[index]
	lst = np.delete(lst, index)
	# lst.remove(mech)
	return mech, lst


def generate_random_list(LIMIT, mechs_per_list):
	lst = []
	num_windows = int(math.ceil(LIMIT * 10 / mechs_per_list))
	for window in range(num_windows):
		lst = np.append(lst, np.random.choice(
		    range(0, 4), size=mechs_per_list, replace=False))
	return lst


def find_ideal_pt_for_person_in_ball(center, radius, idealpt_and_radius, constraint="l1", deficit_offset=228):
	X = cvxpy.Variable(5)  # 1 point for each item
	fun = 0
	y = idealpt_and_radius[0];
	w = idealpt_and_radius[1];
	sumsq = math.sqrt(sum([math.pow(w[i], 2) for i in range(5)]))
	w = [w[i] / sumsq for i in range(5)]

	for slider in range(5):
		fun += w[slider] * cvxpy.abs(X[slider] - y[slider])
	obj = cvxpy.Minimize(fun)
	constraints = [X >= 0, X[0] + X[1] + X[2] - X[3] + deficit_offset == X[4]]

	if constraint == "l1":
		constraints += [cvxpy.sum_entries(cvxpy.abs(X[0:4] - center[0:4])) <= radius]
	else:
		constraints += [cvxpy.sum_entries(cvxpy.square(X[0:4] -
		                                  center[0:4])) <= radius**2]

	prob = cvxpy.Problem(obj, constraints)
	result = prob.solve(solver = 'SCS')
	items = [X.value[i, 0] for i in range(5)]

	if constraint == "l1":
		credits = [abs(items[i] - center[i]) / radius for i in range(4)]
	else:
		credits = [(items[i] - center[i])**2 / radius**2 for i in range(4)]

	return items, credits


def sample_in_ball(radius, num_dimensions=4):
	dimension_counter = 0;
	vector = [];
	length_of_vector = 2;
	while length_of_vector > 1:
		vector = [2 * np.random.random() - 1 for _ in range(num_dimensions)];
		length_of_vector = sum([math.pow(vector[i], 2)
		                       for i in range(num_dimensions)]);

	length_of_vector = np.sqrt(length_of_vector);
	# scale the vector to unit norm
	vector = [vector[i] / length_of_vector for i in range(num_dimensions)];
	return vector;


def calculate_disutility_of_vector(pts, vector):
	idealpts = pts[0]
	weights = pts[1]

	return sum([weights[i] * abs(idealpts[i] - vector[i]) for i in range(5)]);


def simulate_person(idealpts, mechanism_assignment, mechanisms, row, mechanism_super_dictionary, deficit_offset=228, current_avg_number=0):
	prepend = "answer1." + str(mechanism_assignment) + ".";
	row[prepend + "0"] = '{"time" : 1}';
	answer = {}
	answer["text_explanation"] = ['simulated'];
	answer["time"] = 1

	if mechanisms[mechanism_assignment]['question_ID'] == 'comparisons':
		for setnum in range(mechanism_super_dictionary[mechanism_assignment]['numsets']):
			sampled_vector_00 = sample_in_ball(4);
			sampled_vector_02 = sample_in_ball(4);
			sampled_vector_03 = sample_in_ball(4);
			setstr = "set" + str(setnum);

			for slider_idx in range(4):
				row[setstr + "slider" + str(slider_idx) + "1"] = mechanisms[mechanism_assignment][
				                            setstr + "slider" + str(slider_idx) + "1"];
				row[setstr + "slider" + str(slider_idx) + "0"] = max(0, row[setstr + "slider" + str(
				    slider_idx) + "1"] + sampled_vector_00[slider_idx] * (row['radius']));
				row[setstr + "slider" + str(slider_idx) + "2"] = max(0, row[setstr + "slider" + str(
				    slider_idx) + "1"] + sampled_vector_02[slider_idx] * (row['radius']));
				row[setstr + "slider" + str(slider_idx) + "3"] = max(0, row[setstr + "slider" + str(
				    slider_idx) + "1"] + sampled_vector_03[slider_idx] * (row['radius']));

			# set deficit terms
			for well_idx in range(4):
				row[setstr + 'slider4' + str(well_idx)] = calculate_deficit(
				    [row[setstr + 'slider' + str(i) + str(well_idx)] for i in range(4)]);

			# for each set, find person's favorite vector, select that as option
			utilities = [calculate_disutility_of_vector(idealpts, [row[
			                                            setstr + 'slider' + str(item) + str(well_idx)] for item in range(5)]) for well_idx in range(4)]
			answer['option' + setstr] = [str(np.argmin(utilities))]
			answer['deficit' + setstr] = row[setstr +
			    'slider4' + str(answer['option' + setstr][0])]

			for slider_idx in range(5):
			 	mechanisms[mechanism_assignment][setstr + "slider" + str(slider_idx) + "1"] = row[
			 	                                                         setstr + "slider" + str(slider_idx) + answer['option' + setstr][0]]

		mechanisms[mechanism_assignment]['number_previous'] = mechanisms[
		    mechanism_assignment]['number_previous'] + 1

	elif mechanisms[mechanism_assignment]['question_ID'] == 'l2':
		for setnum in range(mechanism_super_dictionary[mechanism_assignment]['numsets']):
			values, credits = find_ideal_pt_for_person_in_ball(mechanisms[mechanism_assignment]['values'][
			                                                   setnum], row['radius'], idealpts, constraint="l2", deficit_offset=deficit_offset)
			setstr = str(setnum)
			for i in range(0, 4):
				answer["slider" + str(i) + setstr] = [str(values[i])];
				answer['deficit' + setstr] = values[4]
				row['answer1.slider' + str(i) + setstr + "_credits"] = credits[i];
			#	mechanisms[mechanism_assignment]['values'][setnum][i] = values[i]

			mechanisms[mechanism_assignment]['averaging_array'][
			    setnum, current_avg_number, :] = values
		mechanisms[mechanism_assignment]['averaging_status_array'][
		    current_avg_number] = sys.maxsize
		if current_avg_number == mechanisms[mechanism_assignment]['num_to_average_per_step'] - 1:
			# Do the averaging, set it to initial_value, reset the array, reset
			# overall busy, increase "number_previous"

			mechanisms[mechanism_assignment]['number_previous'] = mechanisms[
			    mechanism_assignment]['number_previous'] + 1
			for setnum in range(mechanism_super_dictionary[mechanism_assignment]['numsets']):
				avg_values = np.average(mechanisms[mechanism_assignment][
				                        'averaging_array'][setnum, :, :], axis=0)
				for i in range(0, 4):
					mechanisms[mechanism_assignment]['values'][setnum][i] = avg_values[i]

			for i in range(len(mechanisms[mechanism_assignment]['averaging_status_array'])):
				mechanisms[mechanism_assignment]['averaging_status_array'][i] = -100;

	elif mechanisms[mechanism_assignment]['question_ID'] == 'full':  # full elicitation
		for setnum in range(mechanism_super_dictionary[mechanism_assignment]['numsets']):
			setstr = str(setnum)
			for i in range(0, 5):
				answer["slider" + str(i) + setstr + "_text"] = [str(idealpts[0][i])];
				answer["slider" + str(i) + setstr + "weight_text"] = [str(idealpts[1][i])]
	elif mechanisms[mechanism_assignment]['question_ID'] == 'l1':
		for setnum in range(mechanism_super_dictionary[mechanism_assignment]['numsets']):
			setstr = str(setnum)
			values, credits = find_ideal_pt_for_person_in_ball(mechanisms[mechanism_assignment]['values'][
			                                                   setnum], row['radius'], idealpts, constraint="l1", deficit_offset=deficit_offset)
			for i in range(0, 4):
				answer["slider" + str(i) + setstr] = [str(values[i])];
				row['answer1.slider' + str(i) + setstr + "_credits"] = credits[i];

				# mechanisms[mechanism_assignment]['values'][setnum][i] = values[i]
			answer['deficit' + setstr] = values[4]
			mechanisms[mechanism_assignment]['averaging_array'][
			    setnum, current_avg_number, :] = values
		mechanisms[mechanism_assignment]['averaging_status_array'][
		    current_avg_number] = sys.maxsize
		if current_avg_number == mechanisms[mechanism_assignment]['num_to_average_per_step'] - 1:
			# Do the averaging, set it to initial_value, reset the array, reset
			# overall busy, increase "number_previous"

			mechanisms[mechanism_assignment]['number_previous'] = mechanisms[
			    mechanism_assignment]['number_previous'] + 1
			for setnum in range(mechanism_super_dictionary[mechanism_assignment]['numsets']):
				avg_values = np.average(mechanisms[mechanism_assignment][
				                        'averaging_array'][setnum, :, :], axis=0)
				for i in range(0, 4):
					mechanisms[mechanism_assignment]['values'][setnum][i] = avg_values[i]

			for i in range(len(mechanisms[mechanism_assignment]['averaging_status_array'])):
				mechanisms[mechanism_assignment]['averaging_status_array'][i] = -100;

	row[prepend + "1"] = answer;
	row[prepend + "2"] = {"political_stance_report": ["somewhat"],
	    "feedback": ["simulated"], "time": 100};

	# if row['current_question'] == 4 or row['current_question'] == 1:
	# 	print row
	return row;


# instead of "BUSY" as would happen on real thing, will just have the
# turker's time there
def assignemnt_with_averaging(mechanisms, turker_time, mechanism_super_dictionary, TIME_IN_MECHANISM, probabilities=None):
	if probabilities is None:
		probabilities = [1.0 / len(mechanism_super_dictionary.keys())
		                           for _ in range(len(mechanism_super_dictionary.keys()))]
	all_busy = True;

	for mech in mechanism_super_dictionary.keys():
		all_busy = all_busy and check_busy_times(mechanisms[mech][
		                                         'averaging_status_array'][-1], turker_time, busy_time=TIME_IN_MECHANISM)

	if all_busy:
		return 0, 0;
	else:
		mechanism = np.random.choice(
		    range(len(mechanism_super_dictionary.keys())), p=probabilities)
		while check_busy_times(mechanisms[mechanism]['averaging_status_array'][-1], turker_time, busy_time=TIME_IN_MECHANISM):
			mechanism = np.random.choice(
			    range(len(mechanism_super_dictionary.keys())), p=probabilities)
		current_avg_number = -1;
		for i in range(0, mechanisms[mechanism]['num_to_average_per_step']):
			if not check_busy_times(mechanisms[mechanism]['averaging_status_array'][i], turker_time, busy_time=TIME_IN_MECHANISM):
				current_avg_number = i;
				mechanisms[mechanism]['averaging_status_array'][i] = turker_time
				break;

		return mechanism, current_avg_number


def simulate_experiment_functionalized(filename, LABEL, mechanism_super_dictionary, radius_parameters, LIMIT=100, TIME_IN_MECHANISM=6, WINDOW_LEN=12, TURKERS_PER_WINDOW=3, deficit_offset=0, load_people_from_file=False, filename_forloadingpeople=None, superdictionary_forloadingpeople=None, deficit_offset_forloadingpeople=None):
	time_of_last_turker = {};
	for mech in mechanism_super_dictionary:
		time_of_last_turker[mech] = -100;
	turker_times = get_turker_times(LIMIT, WINDOW_LEN, TURKERS_PER_WINDOW);

	mechanisms = intialize_mechanisms(mechanism_super_dictionary);

	if load_people_from_file:
		persons = load_sample_people_from_file(filename_forloadingpeople, superdictionary_forloadingpeople, deficit_offset_forloadingpeople);

	with open(filename, 'wb') as f:
		fieldnames = ['worker_ID','asg_ID','initial_time','begin_time','experiment_id','current_question','experiment_finished','begin_experiment','num_of_previous_participants','current_answer','initial_slider00','initial_slider10','initial_slider20','initial_slider30','initial_deficit0','initial_slider01','initial_slider11','initial_slider21','initial_slider31', 'initial_deficit1', 'timer','radius','answer1.0.0','answer1.0.1','answer1.0.2','answer1.1.0','answer1.1.1','answer1.1.2','answer1.2.0','answer1.2.1','answer1.2.2','answer1.3.0','answer1.3.1','answer1.3.2','answer1.4.0','answer1.4.1','answer1.4.2','answer1.5.0','answer1.5.1','answer1.5.2','answer1.6.0','answer1.6.1','answer1.6.2','answer1.7.0','answer1.7.1','answer1.7.2','answer1.8.0','answer1.8.1','answer1.8.2','answer1.9.0','answer1.9.1','answer1.9.2','set0slider00','set0slider10','set0slider20','set0slider30','set0slider40','set0slider01','set0slider11','set0slider21','set0slider31','set0slider41','set0slider02','set0slider12','set0slider22','set0slider32','set0slider42','set0slider03','set0slider13','set0slider23','set0slider33','set0slider43','set1slider00','set1slider10','set1slider20','set1slider30','set1slider40','set1slider01','set1slider11','set1slider21','set1slider31','set1slider41','set1slider02','set1slider12','set1slider22','set1slider32','set1slider42','set1slider03','set1slider13','set1slider23','set1slider33','set1slider43','answer1.slider00_credits','answer1.slider10_credits','answer1.slider20_credits','answer1.slider30_credits', 'answer1.slider01_credits','answer1.slider11_credits','answer1.slider21_credits','answer1.slider31_credits']
		writer = csv.DictWriter(f, fieldnames = fieldnames);
		writer.writeheader();

		for turker_time in turker_times:
			# mechanism_assignment = assignment_david_option2(time_of_last_turker, turker_time, mechanism_super_dictionary, TIME_IN_MECHANISM)
			mechanism_assignment, current_avg_number = assignemnt_with_averaging(mechanisms, turker_time, mechanism_super_dictionary, TIME_IN_MECHANISM)

			if not load_people_from_file:
				turker_idealpt = create_ideal_points_and_weights();
			else:
			    turker_idealpt = random.choice(persons);
			row = do_mechanism(turker_idealpt, mechanism_assignment, mechanisms, time_of_last_turker, turker_time, mechanism_super_dictionary, deficit_offset, radius_parameters, current_avg_number)
			writer.writerow(row);
