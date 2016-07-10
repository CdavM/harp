#code to determine randomization scheme
import math
import random
import numpy as np
def get_turkers (num_turkers, window_length, max_turkers_per_window):
	turkers = []
	num_windows = int(math.ceil(num_turkers/max_turkers_per_window))
	for window in range(num_windows):
		loc = []
		for i in range(max_turkers_per_window):
			loc.append(random.uniform(window_length*window, window_length*(window + 1)))
		turkers = np.append(turkers, sorted(loc))
	return turkers


def assign_mechanism(mechanism, num_turkers, time_of_last_turker, time):
	num_turkers[mechanism] = num_turkers[mechanism] + 1
	time_of_last_turker[mechanism] = time

def check_busy(mechanism, time, time_of_last_turker, busy_time = 9):
	return (time_of_last_turker[mechanism] + busy_time > time)

def assignment_david_option2(time_of_last_turker, time, probabilities = [.27, .27, .19, .27]):
	all_busy = True;
	for mech in range(0, 4):
		all_busy = all_busy and check_busy(mech, time, time_of_last_turker)
	
	if all_busy:
		return 2;
	else:
		mechanism = np.random.choice(range(4), p=probabilities)
		while check_busy(mechanism, time, time_of_last_turker):
			mechanism = np.random.choice(range(4), p=probabilities)
		return mechanism

def assignment_pregeneratedlist(time_of_last_turker, time, lst):
	index = 0;
	while lst[index]!=2 and check_busy(lst[index], time, time_of_last_turker):
		index += 1
	mech = lst[index]
	lst = np.delete(lst, index)
	#lst.remove(mech)
	return mech, lst

def generate_random_list(LIMIT, mechs_per_list):
	lst = []
	num_windows = int(math.ceil(LIMIT*10/mechs_per_list))
	for window in range(num_windows):
		lst = np.append(lst, np.random.choice(range(0, 4), size=mechs_per_list, replace=False))
	return lst

LIMIT = 10000
def main():
	time_of_last_turker = {0: -100, 1: -100, 2: -100, 3:-100}
	num_turkers = {0: 0, 1: 0, 2: 0, 3:0}
	turkers = get_turkers(LIMIT, 10, 3);

	pregeneratedlist = generate_random_list(LIMIT, 3)
	for turker in turkers:
		#assign = assignment_david_option2(time_of_last_turker, turker)
		assign, pregeneratedlist = assignment_pregeneratedlist(time_of_last_turker, turker, pregeneratedlist)
		assign_mechanism(assign, num_turkers, time_of_last_turker, turker)
	for mech in range(0, 4):
		print mech, num_turkers[mech]/float(LIMIT)


#print get_turkers(10, 5, 2)
main();