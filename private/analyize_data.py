import csv
import ast
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
from operator import itemgetter

import numpy as np



DEBUG_LEVEL = 0

def load_data(filename):
    with open(filename, mode='rb') as file:
        reader = csv.DictReader(file)
        return list(reader)
    print "unable to open file"
    return None

slider_order = ['Defense', 'Health', 'Transportation', 'Tax']
mechanism_names = ['Constrained Movement', 'Comparisons', 'Full Elicitation']

def load_data_experiment2(data): #ideal points and weights elicitation
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

def load_data_experiment0(data): #constrained movement
    answer = {}
    answer['slider0_loc'] = float(data['slider0'][0])
    answer['slider1_loc'] = float(data['slider1'][0])
    answer['slider2_loc'] = float(data['slider2'][0])
    answer['slider3_loc'] = float(data['slider3'][0])
    answer['explanation'] = data['text_explanation']

    return answer

def load_data_experiment1(data): #comparisons
    answer = {}
    answer['explanation'] = data['text_explanation']
    answer['selection'] = data[""]
    #TODO include radius values and so forth
    return answer

switcher_load_data = {
    0: load_data_experiment0,
    1: load_data_experiment1,
    2: load_data_experiment2,
}

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
    plot_sliders_over_time(data, 'Constrained Movement Mechanism')
    return None


def analyze_data_experiment1(data): # comparisons
	#plot_sliders_over_time(data)
    return None


def analyze_data_experiment2(data): # ideal points and elicitation
    return None

switcher_analyze_data = {
    0: analyze_data_experiment0,
    1: analyze_data_experiment1,
    2: analyze_data_experiment2,
}


def clean_data(dirty):
    clean = []
    organized_data = {}
    organized_data[0] = []
    organized_data[1] = []
    organized_data[2] = []

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

        d['time_page0'] = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.0'])['time']/1000.0 #in seconds
        d['time_page1'] = answerdict['time']/1000.0
        d['time_page2'] = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.2'])['time']/1000.0

        #print d['experiment_id'], d['question_num'], answerdict
        d['question_data'] = switcher_load_data[d['question_num']](answerdict)

        clean.append(d)
        organized_data[d['question_num']].append(d)

    for key in organized_data:
        organized_data[key] = sorted(organized_data[key], key=itemgetter('experiment_id'))
    return clean, organized_data

def analyze_data(organized_data):
    # for comparisons & constrained movement, plot the locations for each slider (with labels) and deficit over time
    # for raw elicitation, calculate the minimizer (optimal point)
    # also calculate average time for each mechanism

    for key in organized_data:
        print switcher_analyze_data[key](organized_data[key])
    calculate_time_spent(organized_data)

def calculate_time_spent(organized_data):
    #For each mechanism, calculate average time spent on each page and plot it in a chuncked bar graph
    pagenames = ['Introduction', 'Mechanism', 'Feedback']

    dpoints = []#np.empty((len(organized_data.keys())* len(pagenames), 3), dtype = )
    for key in organized_data:
    	for page in range(0, len(pagenames)):
    		dpoints.append([mechanism_names[key], pagenames[page], np.mean([d['time_page' + str(page)] for d in organized_data[key]])])
    barplot(np.array(dpoints), 'test', 'Time (Seconds)', 'Page')



def barplot(dpoints, label, ylabel, xlabel):
    '''
    copied from http://emptypipes.org/2013/11/09/matplotlib-multicategory-barchart/ on 6/27/2016
        modified to take in the matrix already rather than calculating mean values
    Create a barchart for data across different categories with
    multiple conditions for each category.
    
    @param ax: The plotting axes from matplotlib.
    @param dpoints: The data set as an (n, 3) numpy array
    '''

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Aggregate the conditions and the categories according to their
    # mean values
    conditions = [(c, np.mean(dpoints[dpoints[:,0] == c][:,2].astype(float))) 
                  for c in np.unique(dpoints[:,0])]
    categories = [(c, np.mean(dpoints[dpoints[:,1] == c][:,2].astype(float))) 
                  for c in np.unique(dpoints[:,1])]
        
    # sort the conditions, categories and data so that the bars in
    # the plot will be ordered by category and condition
    conditions = [c[0] for c in sorted(conditions, key=o.itemgetter(1))]
    categories = [c[0] for c in sorted(categories, key=o.itemgetter(1))]

    
    dpoints = np.array(sorted(dpoints, key=lambda x: categories.index(x[1])))

    # the space between each set of bars
    space = 0.3
    n = len(conditions)
    width = (1 - space) / (len(conditions))
    
    # Create a set of bars at each position
    for i,cond in enumerate(conditions):
        indeces = range(1, len(categories)+1)
        vals = dpoints[dpoints[:,0] == cond][:,2].astype(np.float)
        pos = [j - (1 - space) / 2. + i * width for j in indeces]
        ax.bar(pos, vals, width=width, label=cond, 
               color=cm.Accent(float(i) / n)
               )
    
    # Set the x-axis tick labels to be equal to the categories
    ax.set_xticks(indeces)
    ax.set_xticklabels(categories)
    ax.tick_params(axis='both', which='major', labelsize=18)

    plt.setp(plt.xticks()[1])#, rotation=90)
    
    # Add the axis labels
    ax.set_ylabel(ylabel, fontsize = 18)
    #ax.set_xlabel(xlabel, fontsize = 18)
    
    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 18)
        
    plt.savefig(label + '.png')
    plt.show()


def main():

    #data = clean_data(load_data('export-20160623074343_edited.csv'))
    # data = clean_data(load_data('export-20160625101532_edited.csv'))

    data, organized_data = clean_data(load_data('export-20160627170659_edited.csv'))
    if DEBUG_LEVEL > 0:
        print len(data)
        for key in organized_data:
            print key, [d['experiment_id'] for d in organized_data[key]]
    analyze_data(organized_data)

if __name__ == "__main__":
    main()
