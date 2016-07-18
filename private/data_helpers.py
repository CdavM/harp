import csv
import ast
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
from operator import itemgetter

import numpy as np



def load_data(filename):
    with open(filename, mode='rb') as file:
        reader = csv.DictReader(file)
        return list(reader)
    print "unable to open file"
    return None

slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]
mechanism_names = ['l2 Constrained Movement', 'Comparisons', 'Full Elicitation', 'l1 Constrained Movement']

def load_data_experiment2(answerdata, restofdata): #ideal points and weights elicitation
    answer = {}
    answer['slider0_loc'] = float(answerdata['slider0_text'][0])
    answer['slider0_weight'] = float(answerdata['slider0weight_text'][0])

    answer['slider1_loc'] = float(answerdata['slider1_text'][0])
    answer['slider1_weight'] = float(answerdata['slider1weight_text'][0])
    
    answer['slider2_loc'] = float(answerdata['slider2_text'][0])
    answer['slider2_weight'] = float(answerdata['slider2weight_text'][0])

    answer['slider3_loc'] = float(answerdata['slider3_text'][0])
    answer['slider3_weight'] = float(answerdata['slider3weight_text'][0])

    answer['slider4_loc'] = answer['slider0_loc'] + answer['slider1_loc'] + answer['slider2_loc'] - answer['slider3_loc'] + 316
    answer['slider4_weight'] = float(answerdata['slider4weight_text'][0])

    answer['explanation'] = answerdata['text_explanation']

    return answer

def load_data_experiment0(answerdata, restofdata): #l2 constrained movement
    answer = {}
    answer['slider0_loc'] = float(answerdata['slider0'][0])
    answer['slider1_loc'] = float(answerdata['slider1'][0])
    answer['slider2_loc'] = float(answerdata['slider2'][0])
    answer['slider3_loc'] = float(answerdata['slider3'][0])
    answer['slider4_loc'] = float(answerdata['deficit'])
    answer['explanation'] = answerdata['text_explanation']
    
    answer['previous_slider_values'] = [float(restofdata['initial_slider0']), float(restofdata['initial_slider1']), float(restofdata['initial_slider2']), float(restofdata['initial_slider3']), float(restofdata['initial_deficit'])]
    
    answer['slider0_creditsused'] = float(restofdata['answer1.slider0_credits']) 
    answer['slider1_creditsused'] = float(restofdata['answer1.slider1_credits'])
    answer['slider2_creditsused'] = float(restofdata['answer1.slider2_credits'])
    answer['slider3_creditsused'] = float(restofdata['answer1.slider3_credits'])

    return answer

def load_data_experiment3(answerdata, restofdata): #l1 constrained movement
    answer = {}
    answer['slider0_loc'] = float(answerdata['slider0'][0])
    answer['slider1_loc'] = float(answerdata['slider1'][0])
    answer['slider2_loc'] = float(answerdata['slider2'][0])
    answer['slider3_loc'] = float(answerdata['slider3'][0])
    answer['slider4_loc'] = float(answerdata['deficit'])
    answer['explanation'] = answerdata['text_explanation']
    
    answer['previous_slider_values'] = [float(restofdata['initial_slider0']), float(restofdata['initial_slider1']), float(restofdata['initial_slider2']), float(restofdata['initial_slider3']), float(restofdata['initial_deficit'])]
    
    answer['slider0_creditsused'] = float(restofdata['answer1.slider0_credits'])
    answer['slider1_creditsused'] = float(restofdata['answer1.slider1_credits'])
    answer['slider2_creditsused'] = float(restofdata['answer1.slider2_credits'])
    answer['slider3_creditsused'] = float(restofdata['answer1.slider3_credits'])

    return answer

def load_data_experiment1(answerdata, restofdata): #comparisons
    answer = {}
    answer['explanation'] = answerdata['text_explanation']
    for set_num in range(2):
        answer['set' + str(set_num) + 'selection'] = int(answerdata["optionset" + str(set_num)][0])

        answer['set' + str(set_num) + 'option0'] = [float(restofdata['set' + str(set_num) + 'slider00']), float(restofdata['set' + str(set_num) + 'slider10']), float(restofdata['set' + str(set_num) + 'slider20']), float(restofdata['set' + str(set_num) + 'slider30']), float(restofdata['set' + str(set_num) + 'slider40'])]
        answer['set' + str(set_num) + 'option1'] = [float(restofdata['set' + str(set_num) + 'slider01']), float(restofdata['set' + str(set_num) + 'slider11']), float(restofdata['set' + str(set_num) + 'slider21']), float(restofdata['set' + str(set_num) + 'slider31']), float(restofdata['set' + str(set_num) + 'slider41'])]
        answer['set' + str(set_num) + 'option2'] = [float(restofdata['set' + str(set_num) + 'slider02']), float(restofdata['set' + str(set_num) + 'slider12']), float(restofdata['set' + str(set_num) + 'slider22']), float(restofdata['set' + str(set_num) + 'slider32']), float(restofdata['set' + str(set_num) + 'slider42'])]

        real_answer = {}
        real_answer[set_num] = answer['set' + str(set_num) + 'option' + str(answer['set' + str(set_num) + 'selection'])]
        for loc in xrange(5):
            answer['set' + str(set_num) + 'slider' + str(loc)+'_loc'] = real_answer[set_num][loc]
        
        answer['set' + str(set_num) + 'previous_slider_values'] = answer['set' + str(set_num) + 'option1']

    print answer
    #TODO include radius values and so forth
    return answer

def load_feedback(feedbackdata, restofdata):
    answer = {}
    answer['political_stance'] = feedbackdata.get('political_stance_report', None)
    answer['feedback'] = feedbackdata.get('feedback', '')
    return answer

switcher_load_data = {
    0: load_data_experiment0,
    1: load_data_experiment1,
    2: load_data_experiment2,
    3: load_data_experiment3
}

def clean_data(dirty):
    clean = []
    organized_data = {}
    organized_data[0] = []
    organized_data[1] = []
    organized_data[2] = []
    organized_data[3] = []

    for row in dirty:
        if len(row['experiment_id'])==0 or (len(row['answer1.0.1']) == 0 and len(row['answer1.1.1']) == 0 and len(row['answer1.2.1']) == 0 and len(row['answer1.3.1']) == 0):
            continue
        d = {}
        copy_over = ['worker_ID', 'asg_ID']
        for ide in copy_over:
            d[ide] = row[ide]
        d['experiment_id'] = int(row['experiment_id'])
        d['question_num'] = int(row['current_question'])
        d['begin_time'] = float(row['begin_time'])
        d['initial_time'] = float(row['initial_time'])
        d['radius'] = float(row['radius'])
        d['time_left_on_page'] = int(row['timer'])
        d['last_page'] = int(row['current_answer'])
        d['participant_number'] = int(row['num_of_previous_participants']) + 1
        d['finished'] = row['experiment_finished']
        #print d['question_num'], d['experiment_id']

        answerdict = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.1'])
        if len(answerdict.get('text_explanation', '')) == 0:
        	continue
        d['time_page0'] = (d['begin_time'] - d['initial_time'])/1000.0
        if len(row['answer1.' + str(d['question_num']) + '.0']) > 0:
        	d['time_page1'] = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.0'])['time']/1000.0 #in seconds
        else:
        	d['time_page1'] = 300
        d['time_page2'] = answerdict['time']/1000.0
        #print row['answer1.1.1']
        #print row['answer1.1.2']
        #print "row erroring: ", row['answer1.' + str(d['question_num']) + '.2']
        if len(row['answer1.' + str(d['question_num']) + '.2']) > 0: #otherwise they didn't submit last page
            feedbackdict = ast.literal_eval(row['answer1.' + str(d['question_num']) + '.2'])
            d['time_page3'] = feedbackdict['time']/1000.0
        else:
        	feedbackdict={}
        	d['time_page3'] = 300
        d['feedback_data'] = load_feedback(feedbackdict, row)


        #print d['experiment_id'], d['question_num'], answerdict, row
        d['question_data'] = switcher_load_data[d['question_num']](answerdict, row)

        clean.append(d)
        organized_data[d['question_num']].append(d)

    for key in organized_data:
        organized_data[key] = sorted(organized_data[key], key=itemgetter('experiment_id'))
    return clean, organized_data



def barplot(dpoints, label, ylabel, xlabel, categories_order, conditions_order):
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
    categories = categories_order
    conditions = conditions_order
    
    dpoints = np.array(sorted(dpoints, key=lambda x: categories.index(x[1])))

    # the space between each set of bars
    space = 0.3
    n = len(conditions)
    width = (1 - space) / (len(conditions))
    current_palette = sns.color_palette()

    # Create a set of bars at each position
    for i,cond in enumerate(conditions):
        indeces = range(1, len(categories)+1)
        vals = dpoints[dpoints[:,0] == cond][:,2].astype(np.float)
        pos = [j - (1 - space) / 2. + i * width for j in indeces]
        ax.bar(pos, vals, width=width, label=cond, 
               color=current_palette[i]
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
    #ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 18)
    ax.legend(handles, labels,bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=min(len(conditions), 4), mode="expand", borderaxespad=0., fontsize = 18)    
    plt.savefig(label + '.png')
    plt.show()