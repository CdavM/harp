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

initial_values = [600, 950, 140, 1500, 506]

DEBUG_LEVEL = 0
slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]
mechanism_names = ['l2 Constrained Movement', 'Comparisons', 'Full Elicitation', 'l1 Constrained Movement']
def plot_sliders_over_time(data, title):
    n = range(0, len(data) + 1)

    for slider in range(0, len(slider_order)):
        vals = [d['question_data']['slider' + str(slider) + '_loc'] for d in data]
        vals.insert(0, initial_values[slider]) #prepend initial values
        plt.plot(n, vals, label = slider_order[slider])
    plt.legend(loc='upper left', fontsize = 18)

    plt.tick_params(axis='both', which='major', labelsize=18)
    
    # Add the axis labels
    plt.title(title, fontsize = 18)
    plt.ylabel('$ (Billions)', fontsize = 18)
    plt.xlabel('Iteration', fontsize = 18)
    plt.show()

def calculate_full_elicitation_euclideanpoint(data):
    X = cvxpy.Variable(4) #1 point for each mechanism
    fun = 0
    for d in data:
        y = [d['question_data']['slider' + str(slider) + '_loc'] for slider in range(4)]
        w = [d['question_data']['slider' + str(slider) + '_weight'] for slider in range(4)]
        sumsq = math.sqrt(sum([math.pow(w[i],2) for i in range(4)]))
        w = [w[i] / sumsq for i in range(4)]
        for slider in range(4):
            fun += w[slider]*cvxpy.abs(X[slider] - y[slider])
    obj = cvxpy.Minimize(fun)
    constraints = [X >= 0]
    prob = cvxpy.Problem(obj, constraints)
    result = prob.solve()
    items = [X.value[i,0] for i in range(4)]
    print 'Optimal full elicitation:', items
    deficit = items[0] + items[1] + items[2] - items[3] + 316
    items.append(deficit)
    return items

def calculate_full_elicitation_average(data):
    sliders = {0:[], 1:[], 2:[], 3:[], 4:[]}
    weights = {0:[], 1:[], 2:[], 3:[], 4:[]}
    rawaverages = {}
    weightedaverages_l1 = {}
    weightedaverages_l2 = {}

    for slider in sliders:
        sliders[slider] = [d['question_data']['slider' + str(slider) + '_loc'] for d in data]
        weights[slider] = [d['question_data']['slider' + str(slider) + '_weight'] for d in data]

    #normalize slider weights
    for i in range(len(weights[0])):
        summ = float(sum([weights[slider][i] for slider in weights]))
        for s in weights:
            weights[s][i]/= summ

    for slider in sliders:
        rawaverages[slider] = np.mean(sliders[slider])
        weightedaverages_l1[slider] = np.average(sliders[slider], weights = weights[slider])
        weightedaverages_l2[slider] = np.average(sliders[slider], weights = [math.pow(x,2) for x in weights[slider]])


    return rawaverages, weightedaverages_l2, weightedaverages_l1, calculate_full_elicitation_euclideanpoint(data)


def plot_allmechansisms_together(organized_data):
    f, axarr = plt.subplots(5, sharex=True)
    lines = []
    rawaverages_mech2, weightedaverages_l2_mech2, weightedaverages_l1_mech2, euclideanprefs_mech2 = calculate_full_elicitation_average(organized_data[2])
    maxn = -1
    for slider in xrange(0, len(slider_order)):
        for mechanism in [0, 1, 3]:#xrange(0, 4):
            n = range(0, len(organized_data[mechanism]) + 1)
            maxn = max(maxn, len(n))
            vals = [d['question_data']['slider' + str(slider) + '_loc'] for d in organized_data[mechanism]]
            vals.insert(0, initial_values[slider]) #prepend initial values
            l = axarr[slider].plot(n, vals, label = mechanism_names[mechanism])
            if slider == 0:
                lines.append(l[0])
            #if mechanism == 0:
           #lines.append(l[0])

        #mechanism 2, fullelicitation:
        n = range(maxn)
        vals = [rawaverages_mech2[slider] for _ in n]
        l = axarr[slider].plot(n, vals, label = mechanism_names[2])
        if slider == 0:
            lines.append(l[0])
        # vals = [weightedaverages_l2_mech2[slider] for _ in n]
        # l = axarr[slider].plot(n, vals, label ='Full Elicitation Weighted L2')
        # if slider == 0:
        #     lines.append(l[0])
        # vals = [weightedaverages_l1_mech2[slider] for _ in n]
        # l = axarr[slider].plot(n, vals, label = 'Full Elicitation Weighted')
        # if slider == 0:
        #     lines.append(l[0])

        vals = [euclideanprefs_mech2[slider] for _ in n]
        l = axarr[slider].plot(n, vals, label = 'Full Elicitation -- Euclidean')
        if slider == 0:
            lines.append(l[0])

        axarr[slider].set_title(slider_order[slider], fontsize = 18)
        axarr[slider].set_ylabel('$ (Billions)', fontsize = 18)
        axarr[slider].tick_params(axis='both', which='major', labelsize=18)

    axarr[len(slider_order)-1].set_xlabel('Iteration', fontsize = 18)
    f.legend(lines, [mechanism_names[0], mechanism_names[1], mechanism_names[3],mechanism_names[2], 'Full Elicitation -- Euclidean'], loc='Upper Center', borderaxespad=0., ncol = 3, fontsize = 18)
    print lines
    #f.legend(loc='upper left', fontsize = 18)
    #plt.legend()

    # Add the axis labels
    #.title('All mechanisms', fontsize = 18)
    
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
    calculate_time_spent(organized_data, LABEL)

    for key in organized_data:
        print switcher_analyze_data[key](organized_data[key])
    analyze_movement_and_weights(organized_data, LABEL)
slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'valid')

def plot_percent_movements_over_time(organized_data, LABEL):
    averages_byitem = {0: [[],[],[],[]], 1:[[],[],[],[]], 2:[[],[],[],[]], 3:[[],[],[],[]]}
    averages_bymostmovement = {0: [[],[],[],[]], 1:[[],[],[],[]], 2:[[],[],[],[]], 3:[[],[],[],[]]}
    averages_creditpercentage = {0:[[],[],[],[]], 3:[[],[],[],[]]}
    averages_creditpercentage_bymost = {0:[[],[],[],[]], 3:[[],[],[],[]]}
    for key in organized_data:
        for experiment in organized_data[key]:
            percentages = get_movement_percentages(experiment)
            if percentages is None:
                print "Did not move at all", experiment['experiment_id']
                continue
            for i in range(len(percentages)):
                averages_byitem[key][i].append(percentages[i])
                averages_bymostmovement[key][i].append(sorted(percentages, reverse = True)[i])
            if key == 0 or key == 3:
                credit_percentages = get_credit_percentage(experiment)
                for i in range(len(credit_percentages)):
                    averages_creditpercentage[key][i].append(credit_percentages[i])
                    averages_creditpercentage_bymost[key][i].append(sorted(credit_percentages, reverse=True)[i])

    f, axarr = plt.subplots(4, sharex=True)
    lines = []
    mechanisms_to_do = [2]
    for slider in xrange(0, 4):
        for mechanism in mechanisms_to_do:#xrange(0, 4):
            n = range(0, len(averages_byitem[mechanism][slider]))
            vals = averages_byitem[mechanism][slider]
            l = axarr[slider].plot(n, vals, label = mechanism_names[mechanism], linestyle = 'None', marker = '.')
            #plot line of best fit
            #l = axarr[slider].plot(n, np.poly1d(np.polyfit(n, vals, 1))(n), label = mechanism_names[mechanism])
            mvgs = movingaverage(vals, 10)
            #l = axarr[slider].plot(range(len(mvgs)),mvgs, label = mechanism_names[mechanism])
            
            if slider == 0:
                lines.append(l[0])
        axarr[slider].set_title(slider_order[slider], fontsize = 18)
        axarr[slider].set_ylabel('Percent movement', fontsize = 18)
        axarr[slider].set_ylim([0.1,.4])
        axarr[slider].tick_params(axis='both', which='major', labelsize=18)

    axarr[len(mechanisms_to_do)-1].set_xlabel('Iteration', fontsize = 18)
    f.legend(lines, [mechanism_names[mechanisms_to_do[i]] for i in range(len(mechanisms_to_do))], loc='Upper Left', borderaxespad=0., ncol = 4, fontsize = 18)
    print lines
    plt.show()


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
    with open ('bonusinfo_real.csv', 'wb') as file:
        writer = csv.writer(file)
        for key in organized_data:
            for d in organized_data[key]:
                writer.writerow([d['worker_ID'], d['question_num'], d['question_data']['explanation'], d['feedback_data']['feedback'],  d['time_page0'],  d['time_page1'],  d['time_page2'],  d['time_page3']])
def print_different_things(organized_data):
    for key in organized_data:
        print "MECHANISM: " + mechanism_names[key]
        for d in organized_data[key]:
			print d['question_data']['explanation'][0], "\n"
			print d['question_data']['slider0_weight'], d['question_data']['slider1_weight'], d['question_data']['slider2_weight'], d['question_data']['slider3_weight']
			print d['question_data']['slider0_loc'], d['question_data']['slider1_loc'], d['question_data']['slider2_loc'], d['question_data']['slider3_loc']
			print "\n\n"


    for key in organized_data:
        print "MECHANISM: " + mechanism_names[key]
        for d in organized_data[key]:
            print d['feedback_data']['feedback'][0], "\n"
def main():


    #data, organized_data = 445.70 clean_data(load_data('export-20160707161738_PILOTFINAL_fixed.csv'))
    data, organized_data = clean_data(load_data('export-20160713195656.csv'))

    LABEL = 'Actual'
    print len(data)
    for key in organized_data:
        print key, len(organized_data[key])#[d['experiment_id'] for d in organized_data[key]]

    for key in organized_data:
        print key, len(organized_data[key])    
    #plot_percent_movements_over_time(organized_data, 'Real Experiment')
    plot_allmechansisms_together(organized_data)

    #analyze_data(organized_data, LABEL)

    #organize_payment(organized_data)

    #print_different_things(organized_data  )

if __name__ == "__main__":
    main()


