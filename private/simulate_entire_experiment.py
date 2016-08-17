# code to determine randomization scheme
import math
import random
import numpy as np
import cvxpy
import csv

# THINGS TO ADD
# Each mechanism
#     Saving values across people
#     radius going down with # of previous people
#     How each person would act with current value and their ideal points/weights
# Try to replicate results I've seen so far to see if accurate simulation
# Try to see what different radius functions will do
# Make this so it'll create those files my analysis code can look at.

# Workers have some ideal point, weights on each


def create_ideal_points_and_weights(num_items=5, centers=[450, 1200, 370, 1300, 882]):
    ideals = []
    weights = []
    for i in range(num_items):
        ideals.append(np.random.uniform(
            low=centers[i] * .25, high=centers[i] * 1.75))
        weights.append(np.random.uniform(low=0, high=10))
    return [ideals, weights]

initial_values = [
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300],
    [450, 1200, 370, 1300]
]


def calculate_deficit(values):
    return values[0] + values[1] + values[2] - values[3] + 162


def intialize_mechanisms():
    mechanisms = {}
    types = [0, 1, 2, 3, 0, 1, 2, 3]
    for i in range(len(types)):
        if types[i] == 1:
            mechanisms[i] = {'question_ID': types[i], 'values': initial_values[
                i], 'number_previous': 0, 'busy': False}
            for item in range(4):
                mechanisms[i]["set0slider" +
                              str(item) + "1"] = initial_values[i][item]
                mechanisms[i]["set1slider" +
                              str(item) + "1"] = initial_values[i][item]
        else:
            mechanisms[i] = {'question_ID': types[i], 'values': initial_values[
                i], 'number_previous': 0, 'busy': False}
    return mechanisms


def radius_fn(num_previous, radius_type=0):
    if radius_type == 0:
        return 35
    elif radius_type == 1:
        return 200.0 / (num_previous + 1)
    elif radius_type == 2:
        return 50.0 / (math.floor(num_previous / 10.0) + 1)

LIMIT = 100
TIME_IN_MECHANISM = 6
PROBABILITIES = [.13, .13, .10, .13, .13, .13, .12, .13]
WINDOW_LEN = 12
TURKERS_PER_WINDOW = 3


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


def do_mechanism(turker_idealpt, mechanism_assignment, mechanisms, time_of_last_turker, turker_time):
    row = fill_out_preliminaries(
        {}, mechanism_assignment, mechanisms, turker_time)
    mechanisms[mechanism_assignment]['number_previous'] = mechanisms[
        mechanism_assignment]['number_previous'] + 1
    time_of_last_turker[mechanism_assignment] = turker_time
    row = simulate_person(
        turker_idealpt, mechanism_assignment, mechanisms, row)

    return row


def fill_out_preliminaries(row, mechanism_assignment, mechanisms, turker_time):
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
    row['initial_slider0'] = mechanisms[mechanism_assignment]['values'][0]
    row['initial_slider1'] = mechanisms[mechanism_assignment]['values'][1]
    row['initial_slider2'] = mechanisms[mechanism_assignment]['values'][2]
    row['initial_slider3'] = mechanisms[mechanism_assignment]['values'][3]
    row['initial_deficit'] = calculate_deficit(
        mechanisms[mechanism_assignment]['values'])
    row['timer'] = 100
    row['radius'] = radius_fn(mechanisms[mechanism_assignment][
                              'number_previous'], radius_type=0)
    return row


def check_busy(mechanism, time, time_of_last_turker, busy_time=TIME_IN_MECHANISM):
    return (time_of_last_turker[mechanism] + busy_time > time)


def assignment_david_option2(time_of_last_turker, time, probabilities=PROBABILITIES):
    all_busy = True
    for mech in range(0, 8):
        all_busy = all_busy and check_busy(mech, time, time_of_last_turker)

    if all_busy:
        return 2
    else:
        mechanism = np.random.choice(range(8), p=probabilities)
        while check_busy(mechanism, time, time_of_last_turker):
            mechanism = np.random.choice(range(8), p=probabilities)
        return mechanism


def assignment_pregeneratedlist(time_of_last_turker, time, lst):
    index = 0
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


def find_ideal_pt_for_person_in_ball(center, radius, idealpt_and_radius, constraint="l1"):
    X = cvxpy.Variable(5)  # 1 point for each item
    fun = 0
    y = idealpt_and_radius[0]
    w = idealpt_and_radius[1]
    sumsq = math.sqrt(sum([math.pow(w[i], 2) for i in range(5)]))
    w = [w[i] / sumsq for i in range(5)]

    for slider in range(5):
        fun += w[slider] * cvxpy.abs(X[slider] - y[slider])
    obj = cvxpy.Minimize(fun)
    constraints = [X >= 0, X[0] + X[1] + X[2] - X[3] + 162 == X[4]]

    if constraint == "l1":
        constraints += [cvxpy.sum_entries(
            cvxpy.abs(X[0:4] - center[0:4])) <= radius]
    else:
        constraints += [cvxpy.sum_entries(
            cvxpy.square(X[0:4] - center[0:4])) <= radius**2]

    prob = cvxpy.Problem(obj, constraints)
    result = prob.solve()
    items = [X.value[i, 0] for i in range(5)]

    if constraint == "l1":
        credits = [abs(items[i] - center[i]) / radius for i in range(4)]
    else:
        credits = [(items[i] - center[i])**2 / radius**2 for i in range(4)]

    deficit = calculate_deficit(items)
    items.append(deficit)
    return items, credits


def sample_in_ball(radius, num_dimensions=4):
    dimension_counter = 0
    vector = []
    length_of_vector = 2
    while length_of_vector > 1:
        vector = [2 * np.random.random() - 1 for _ in range(num_dimensions)]
        length_of_vector = sum([math.pow(vector[i], 2)
                                for i in range(num_dimensions)])

    length_of_vector = np.sqrt(length_of_vector)
    # scale the vector to unit norm
    vector = [vector[i] / length_of_vector for i in range(num_dimensions)]
    return vector


def calculate_disutility_of_vector(pts, vector):
    idealpts = pts[0]
    weights = pts[1]

    return sum([weights[i] * abs(idealpts[i] - vector[i]) for i in range(5)])


def simulate_person(idealpts, mechanism_assignment, mechanisms, row):
    prepend = "answer1." + str(mechanism_assignment) + "."
    row[prepend + "0"] = '{"time" : 1}'
    answer = {}
    answer["text_explanation"] = ['simulated']
    answer["time"] = 1

    if mechanisms[mechanism_assignment]['question_ID'] == 1:
        sampled_vector_00 = sample_in_ball(4)
        sampled_vector_02 = sample_in_ball(4)
        sampled_vector_03 = sample_in_ball(4)

        sampled_vector_10 = sample_in_ball(4)
        sampled_vector_12 = sample_in_ball(4)
        sampled_vector_13 = sample_in_ball(4)

        for slider_idx in range(4):
            row["set0slider" + str(slider_idx) + "1"] = mechanisms[mechanism_assignment][
                "set0slider" + str(slider_idx) + "1"]
            row["set0slider" + str(slider_idx) + "0"] = max(0, row["set0slider" + str(
                slider_idx) + "1"] + sampled_vector_00[slider_idx] * (row['radius']))
            row["set0slider" + str(slider_idx) + "2"] = max(0, row["set0slider" + str(
                slider_idx) + "1"] + sampled_vector_02[slider_idx] * (row['radius']))
            row["set0slider" + str(slider_idx) + "3"] = max(0, row["set0slider" + str(
                slider_idx) + "1"] + sampled_vector_03[slider_idx] * (row['radius']))

            row["set1slider" + str(slider_idx) + "1"] = mechanisms[mechanism_assignment][
                "set1slider" + str(slider_idx) + "1"]
            row["set1slider" + str(slider_idx) + "0"] = max(0, row["set1slider" + str(
                slider_idx) + "1"] + sampled_vector_10[slider_idx] * (row['radius']))
            row["set1slider" + str(slider_idx) + "2"] = max(0, row["set1slider" + str(
                slider_idx) + "1"] + sampled_vector_12[slider_idx] * (row['radius']))
            row["set1slider" + str(slider_idx) + "3"] = max(0, row["set1slider" + str(
                slider_idx) + "1"] + sampled_vector_13[slider_idx] * (row['radius']))

        # set deficit terms
        for well_idx in range(4):
            row['set0slider4' + str(well_idx)] = calculate_deficit(
                [row['set0slider' + str(i) + str(well_idx)] for i in range(4)])
            row['set1slider4' + str(well_idx)] = calculate_deficit(
                [row['set1slider' + str(i) + str(well_idx)] for i in range(4)])

        # for each set, find person's favorite vector, select that as option
        set0utilities = [calculate_disutility_of_vector(idealpts, [row[
                                                        'set0slider' + str(item) + str(well_idx)] for item in range(5)]) for well_idx in range(4)]
        set1utilities = [calculate_disutility_of_vector(idealpts, [row[
                                                        'set1slider' + str(item) + str(well_idx)] for item in range(5)]) for well_idx in range(4)]
        answer['optionset0'] = [str(np.argmin(set0utilities))]
        answer['optionset1'] = [str(np.argmin(set1utilities))]
        answer['deficitset0'] = row[
            'set0slider4' + str(answer['optionset0'][0])]
        answer['deficitset1'] = row[
            'set1slider4' + str(answer['optionset1'][0])]

        for slider_idx in range(5):
            mechanisms[mechanism_assignment]["set0slider" + str(slider_idx) + "1"] = row[
                "set0slider" + str(slider_idx) + answer['optionset0'][0]]
            mechanisms[mechanism_assignment]["set1slider" + str(slider_idx) + "1"] = row[
                "set1slider" + str(slider_idx) + answer['optionset1'][0]]

    elif mechanisms[mechanism_assignment]['question_ID'] == 0:
        values, credits = find_ideal_pt_for_person_in_ball(mechanisms[mechanism_assignment][
                                                           'values'], row['radius'], idealpts, constraint="l2")
        for i in range(0, 4):
            answer["slider" + str(i)] = [str(values[i])]
            answer['deficit'] = values[4]
            row['answer1.slider' + str(i) + "_credits"] = credits[i]
            mechanisms[mechanism_assignment]['values'][i] = values[i]
    elif mechanisms[mechanism_assignment]['question_ID'] == 2:  # full elicitation
        for i in range(0, 5):
            answer["slider" + str(i) + "_text"] = [str(idealpts[0][i])]
            answer["slider" + str(i) + "weight_text"] = [str(idealpts[1][i])]
    elif mechanisms[mechanism_assignment]['question_ID'] == 3:
        values, credits = find_ideal_pt_for_person_in_ball(mechanisms[mechanism_assignment][
                                                           'values'], row['radius'], idealpts, constraint="l1")
        for i in range(0, 4):
            answer["slider" + str(i)] = [str(values[i])]
            answer['deficit'] = values[4]
            row['answer1.slider' + str(i) + "_credits"] = credits[i]
            mechanisms[mechanism_assignment]['values'][i] = values[i]

    row[prepend + "1"] = answer
    row[prepend + "2"] = {"political_stance_report": ["somewhat"],
                          "feedback": ["simulated"], "time": 100}

    return row

# 'answer1.0.1','answer1.0.2','answer1.1.0','answer1.1.1','answer1.1.2','answer1.2.0','answer1.2.1','answer1.2.2','answer1.3.0','answer1.3.1','answer1.3.2','answer1.4.0','answer1.4.1','answer1.4.2','answer1.5.0','answer1.5.1','answer1.5.2','answer1.6.0','answer1.6.1','answer1.6.2','answer1.7.0','answer1.7.1','answer1.7.2','set0slider00','set0slider10', 'set0slider20','set0slider30','set0slider40','set0slider01','set0slider11','set0slider21','set0slider31','set0slider41','set0slider02','set0slider12','set0slider22','set0slider32','set0slider42','set0slider03','set0slider13','set0slider23','set0slider33','set0slider43','set1slider00','set1slider10','set1slider20','set1slider30','set1slider40','set1slider01','set1slider11','set1slider21','set1slider31','set1slider41','set1slider02','set1slider12','set1slider22','set1slider32','set1slider42','set1slider03','set1slider13','set1slider23','set1slider33','set1slider43',


def main():
    time_of_last_turker = {0: -100, 1: -100, 2: -100,
                           3: -100, 4: -100, 5: -100, 6: -100, 7: -100}
    turker_times = get_turker_times(LIMIT, WINDOW_LEN, TURKERS_PER_WINDOW)
    mechanisms = intialize_mechanisms()

    with open('simulated_experiment_constantradius_tiny.csv', 'wb') as f:
        fieldnames = ['worker_ID', 'asg_ID', 'initial_time', 'begin_time', 'experiment_id', 'current_question', 'experiment_finished', 'begin_experiment', 'num_of_previous_participants', 'current_answer', 'initial_slider0', 'initial_slider1', 'initial_slider2', 'initial_slider3', 'initial_deficit', 'timer', 'radius', 'answer1.0.0', 'answer1.0.1', 'answer1.0.2', 'answer1.1.0', 'answer1.1.1', 'answer1.1.2', 'answer1.2.0', 'answer1.2.1', 'answer1.2.2', 'answer1.3.0', 'answer1.3.1', 'answer1.3.2', 'answer1.4.0', 'answer1.4.1', 'answer1.4.2', 'answer1.5.0', 'answer1.5.1', 'answer1.5.2', 'answer1.6.0', 'answer1.6.1', 'answer1.6.2', 'answer1.7.0', 'answer1.7.1', 'answer1.7.2', 'set0slider00', 'set0slider10',
                      'set0slider20', 'set0slider30', 'set0slider40', 'set0slider01', 'set0slider11', 'set0slider21', 'set0slider31', 'set0slider41', 'set0slider02', 'set0slider12', 'set0slider22', 'set0slider32', 'set0slider42', 'set0slider03', 'set0slider13', 'set0slider23', 'set0slider33', 'set0slider43', 'set1slider00', 'set1slider10', 'set1slider20', 'set1slider30', 'set1slider40', 'set1slider01', 'set1slider11', 'set1slider21', 'set1slider31', 'set1slider41', 'set1slider02', 'set1slider12', 'set1slider22', 'set1slider32', 'set1slider42', 'set1slider03', 'set1slider13', 'set1slider23', 'set1slider33', 'set1slider43', 'answer1.slider0_credits', 'answer1.slider1_credits', 'answer1.slider2_credits', 'answer1.slider3_credits']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for turker_time in turker_times:
            mechanism_assignment = assignment_david_option2(
                time_of_last_turker, turker_time)
            # if mechanism_assignment == 1 or mechanism_assignment == 5 :
            #     continue
            turker_idealpt = create_ideal_points_and_weights()
            row = do_mechanism(turker_idealpt, mechanism_assignment,
                               mechanisms, time_of_last_turker, turker_time)
            writer.writerow(row)

        print mechanisms

# print get_turkers(10, 5, 2)
main()
