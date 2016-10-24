import csv
import ast
import seaborn as sns
import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o
from operator import itemgetter

import numpy as np
import os


def load_data(filename):
    with open(filename, mode='rb') as file:
        reader = csv.DictReader(file)
        return list(reader)
    print "unable to open file"
    return None

slider_order = ['Defense', 'Health', 'Transportation', 'Income Tax', "Deficit"]
mechanism_names = ['l2 Constrained Movement', 'Comparisons',
    'Full Elicitation', 'l1 Constrained Movement']


# ideal points and weights elicitation
def load_data_experiment_full(answerdata, restofdata, num_sets, deficit_additive, isfullslider=False):
    prepend = ""
    if isfullslider:
        prepend = "full"
    answer = {}
    answer['slider00_loc'] = float(answerdata[prepend + 'slider0_text'][0])
    answer['slider00_weight'] = float(
        answerdata[prepend + 'slider0weight_text'][0])

    answer['slider10_loc'] = float(answerdata[prepend + 'slider1_text'][0])
    answer['slider10_weight'] = float(
        answerdata[prepend + 'slider1weight_text'][0])

    answer['slider20_loc'] = float(answerdata[prepend + 'slider2_text'][0])
    answer['slider20_weight'] = float(
        answerdata[prepend + 'slider2weight_text'][0])

    answer['slider30_loc'] = float(answerdata[prepend + 'slider3_text'][0])
    answer['slider30_weight'] = float(
        answerdata[prepend + 'slider3weight_text'][0])

    answer['slider40_loc'] = answer['slider00_loc'] + answer['slider10_loc'] + \
        answer['slider20_loc'] - answer['slider30_loc'] + deficit_additive
    answer['slider40_weight'] = float(
        answerdata[prepend + 'slider4weight_text'][0])

    answer['explanation'] = answerdata['text_explanation']

    return answer


# l2 constrained movement
def load_data_experiment_l2(answerdata, restofdata, numsets, deficit_additive=0):
    answer = {}

    for setnum in range(numsets):
        setstr = str(setnum);
        answer['slider0' + setstr +
            '_loc'] = float(answerdata['slider0' + setstr][0])
        answer['slider1' + setstr +
            '_loc'] = float(answerdata['slider1' + setstr][0])
        answer['slider2' + setstr +
            '_loc'] = float(answerdata['slider2' + setstr][0])
        answer['slider3' + setstr +
            '_loc'] = float(answerdata['slider3' + setstr][0])
        # answer['slider4' + setstr +
        #     '_loc'] = float(answerdata['deficit' + setstr])
        answer['explanation'] = answerdata['text_explanation']
        answer['slider4' + setstr + '_loc'] = answer['slider0' + setstr + '_loc'] + answer['slider1' + setstr + '_loc'] + answer[
                        'slider2' + setstr + '_loc'] - answer['slider3' + setstr + '_loc'] + deficit_additive  # float(restofdata['initial_deficit' + setstr])

        answer['initial_slider0' + setstr +
            '_loc'] = float(restofdata['initial_slider0' + setstr])
        answer['initial_slider1' + setstr +
            '_loc'] = float(restofdata['initial_slider1' + setstr])
        answer['initial_slider2' + setstr +
            '_loc'] = float(restofdata['initial_slider2' + setstr])
        answer['initial_slider3' + setstr +
            '_loc'] = float(restofdata['initial_slider3' + setstr])
        answer['initial_slider4' + setstr + '_loc'] = answer['initial_slider0' + setstr + '_loc'] + answer['initial_slider1' + setstr + '_loc'] + answer[
            'initial_slider2' + setstr + '_loc'] - answer['initial_slider3' + setstr + '_loc'] + deficit_additive  # float(restofdata['initial_deficit' + setstr])

        answer['explanation'] = answerdata['text_explanation']

        answer['previous_slider_values' + setstr] = [float(restofdata['initial_slider0' + setstr]), float(restofdata['initial_slider1' + setstr]), float(
            restofdata['initial_slider2' + setstr]), float(restofdata['initial_slider3' + setstr]), float(restofdata['initial_deficit' + setstr])]

        answer['slider0' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider0' + setstr + '_credits'])
        answer['slider1' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider1' + setstr + '_credits'])
        answer['slider2' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider2' + setstr + '_credits'])
        answer['slider3' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider3' + setstr + '_credits'])

    return answer

# linf constrained movement


def load_data_experiment_linf(answerdata, restofdata, numsets, deficit_additive=0):
    answer = {}

    for setnum in range(numsets):
        setstr = str(setnum);
        answer['slider0' + setstr +
            '_loc'] = float(answerdata['slider0' + setstr][0])
        answer['slider1' + setstr +
            '_loc'] = float(answerdata['slider1' + setstr][0])
        answer['slider2' + setstr +
            '_loc'] = float(answerdata['slider2' + setstr][0])
        answer['slider3' + setstr +
            '_loc'] = float(answerdata['slider3' + setstr][0])
        # answer['slider4' + setstr +
        #     '_loc'] = float(answerdata['deficit' + setstr])
        answer['explanation'] = answerdata['text_explanation']
        answer['slider4' + setstr + '_loc'] = answer['slider0' + setstr + '_loc'] + answer['slider1' + setstr + '_loc'] + answer[
                        'slider2' + setstr + '_loc'] - answer['slider3' + setstr + '_loc'] + deficit_additive  # float(restofdata['initial_deficit' + setstr])

        answer['initial_slider0' + setstr +
            '_loc'] = float(restofdata['initial_slider0' + setstr])
        answer['initial_slider1' + setstr +
            '_loc'] = float(restofdata['initial_slider1' + setstr])
        answer['initial_slider2' + setstr +
            '_loc'] = float(restofdata['initial_slider2' + setstr])
        answer['initial_slider3' + setstr +
            '_loc'] = float(restofdata['initial_slider3' + setstr])
        answer['initial_slider4' + setstr + '_loc'] = answer['initial_slider0' + setstr + '_loc'] + answer['initial_slider1' + setstr + '_loc'] + answer[
            'initial_slider2' + setstr + '_loc'] - answer['initial_slider3' + setstr + '_loc'] + deficit_additive  # float(restofdata['initial_deficit' + setstr])

        answer['previous_slider_values' + setstr] = [float(restofdata['initial_slider0' + setstr]), float(restofdata['initial_slider1' + setstr]), float(
            restofdata['initial_slider2' + setstr]), float(restofdata['initial_slider3' + setstr]), float(restofdata['initial_deficit' + setstr])]

        answer['slider0' + setstr + '_creditsused'] = abs(answer['previous_slider_values' + setstr][
                                                          0] - answer['slider0' + setstr + '_loc']) / float(restofdata['radius'])
        answer['slider1' + setstr + '_creditsused'] = abs(answer['previous_slider_values' + setstr][
                                                          1] - answer['slider1' + setstr + '_loc']) / float(restofdata['radius'])
        answer['slider2' + setstr + '_creditsused'] = abs(answer['previous_slider_values' + setstr][
                                                          2] - answer['slider2' + setstr + '_loc']) / float(restofdata['radius'])
        answer['slider3' + setstr + '_creditsused'] = abs(answer['previous_slider_values' + setstr][
                                                          3] - answer['slider3' + setstr + '_loc']) / float(restofdata['radius'])

    return answer

# l1 constrained movement


def load_data_experiment_l1(answerdata, restofdata, numsets, deficit_additive=0):
    answer = {}

    for setnum in range(numsets):
        setstr = str(setnum);
        answer['slider0' + setstr +
            '_loc'] = float(answerdata['slider0' + setstr][0])
        answer['slider1' + setstr +
            '_loc'] = float(answerdata['slider1' + setstr][0])
        answer['slider2' + setstr +
            '_loc'] = float(answerdata['slider2' + setstr][0])
        answer['slider3' + setstr +
            '_loc'] = float(answerdata['slider3' + setstr][0])
        # answer['slider4' + setstr +
        #     '_loc'] = float(answerdata['deficit' + setstr])
        answer['explanation'] = answerdata['text_explanation']
        answer['slider4' + setstr + '_loc'] = answer['slider0' + setstr + '_loc'] + answer['slider1' + setstr + '_loc'] + answer[
                        'slider2' + setstr + '_loc'] - answer['slider3' + setstr + '_loc'] + deficit_additive  # float(restofdata['initial_deficit' + setstr])

        answer['initial_slider0' + setstr +
            '_loc'] = float(restofdata['initial_slider0' + setstr])
        answer['initial_slider1' + setstr +
            '_loc'] = float(restofdata['initial_slider1' + setstr])
        answer['initial_slider2' + setstr +
            '_loc'] = float(restofdata['initial_slider2' + setstr])
        answer['initial_slider3' + setstr +
            '_loc'] = float(restofdata['initial_slider3' + setstr])
        answer['initial_slider4' + setstr + '_loc'] = answer['initial_slider0' + setstr + '_loc'] + answer['initial_slider1' + setstr + '_loc'] + answer[
            'initial_slider2' + setstr + '_loc'] - answer['initial_slider3' + setstr + '_loc'] + deficit_additive  # float(restofdata['initial_deficit' + setstr])

        answer['previous_slider_values' + setstr] = [float(restofdata['initial_slider0' + setstr]), float(restofdata['initial_slider1' + setstr]), float(
            restofdata['initial_slider2' + setstr]), float(restofdata['initial_slider3' + setstr]), float(restofdata['initial_deficit' + setstr])]

        answer['slider0' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider0' + setstr + '_credits'])
        answer['slider1' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider1' + setstr + '_credits'])
        answer['slider2' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider2' + setstr + '_credits'])
        answer['slider3' + setstr + '_creditsused'] = float(
            restofdata['answer1.slider3' + setstr + '_credits'])

    return answer


# comparisons
def load_data_experiment_comparisons(answerdata, restofdata, numsets, deficit_additive=0):
    answer = {}
    answer['explanation'] = answerdata['text_explanation']
    for set_num in range(numsets):
        answer[
            'set' + str(set_num) + 'selection'] = int(answerdata["optionset" + str(set_num)][0])

        answer['set' + str(set_num) + 'option0'] = [float(restofdata['set' + str(set_num) + 'slider00']), float(restofdata['set' + str(set_num) + 'slider10']), float(
            restofdata['set' + str(set_num) + 'slider20']), float(restofdata['set' + str(set_num) + 'slider30']), float(restofdata['set' + str(set_num) + 'slider40'])]
        answer['set' + str(set_num) + 'option1'] = [float(restofdata['set' + str(set_num) + 'slider01']), float(restofdata['set' + str(set_num) + 'slider11']), float(
            restofdata['set' + str(set_num) + 'slider21']), float(restofdata['set' + str(set_num) + 'slider31']), float(restofdata['set' + str(set_num) + 'slider41'])]
        answer['set' + str(set_num) + 'option2'] = [float(restofdata['set' + str(set_num) + 'slider02']), float(restofdata['set' + str(set_num) + 'slider12']), float(
            restofdata['set' + str(set_num) + 'slider22']), float(restofdata['set' + str(set_num) + 'slider32']), float(restofdata['set' + str(set_num) + 'slider42'])]
        answer['set' + str(set_num) + 'option3'] = [float(restofdata['set' + str(set_num) + 'slider03']), float(restofdata['set' + str(set_num) + 'slider13']), float(
            restofdata['set' + str(set_num) + 'slider23']), float(restofdata['set' + str(set_num) + 'slider33']), float(restofdata['set' + str(set_num) + 'slider43'])]

        real_answer = {}
        real_answer[set_num] = answer[
            'set' + str(set_num) + 'option' + str(answer['set' + str(set_num) + 'selection'])]
        for loc in xrange(5):
            answer['set' + str(set_num) + 'slider' + str(loc) +
                               '_loc'] = real_answer[set_num][loc]

        answer['set' + str(set_num) + 'previous_slider_values'] = answer[
                           'set' + str(set_num) + 'option1']

    # print answer
    # TODO include radius values and so forth
    return answer


def load_feedback(feedbackdata, restofdata):
    answer = {}
    answer['political_stance'] = feedbackdata.get(
        'political_stance_report', None)
    answer['feedback'] = feedbackdata.get('feedback', '')
    return answer

switcher_load_data = {
    'full': load_data_experiment_full,
    'l2': load_data_experiment_l2,
    'l1': load_data_experiment_l1,
    'linf': load_data_experiment_linf,
    'comparisons': load_data_experiment_comparisons,
}


def clean_data(dirty, mechanism_super_dictionary, deficit_offset):
    clean = []
    organized_data = {}
    for key in mechanism_super_dictionary:
        organized_data[key] = []

    for row in dirty:
        existsanswer = False;
        for key in mechanism_super_dictionary:
            existsanswer = existsanswer or (
                len(row['answer1.' + str(key) + '.1']) != 0);

        if len(row['experiment_id']) == 0 or not existsanswer:
            continue
        d = {}
        copy_over = ['worker_ID', 'asg_ID']
        for ide in copy_over:
            d[ide] = row[ide]
        d['experiment_id'] = row['experiment_id']
        d['question_num'] = int(row['current_question'])
        d['begin_time'] = float(row['begin_time'])
        d['initial_time'] = float(row['initial_time'])
        d['radius'] = float(row['radius'])
        d['time_left_on_page'] = int(row['timer'])
        d['last_page'] = int(row['current_answer'])
        d['participant_number'] = int(row['num_of_previous_participants']) + 1
        d['finished'] = row['experiment_finished']
        # print d['question_num'], d['experiment_id']
        if len(row['answer1.' + str(d['question_num']) + '.1']) == 0:
            continue
        answerdict = ast.literal_eval(
            row['answer1.' + str(d['question_num']) + '.1'])
        if len(answerdict.get('text_explanation', '')) == 0:
        	continue
        d['time_page0'] = (d['begin_time'] - d['initial_time']) / 1000.0
        if len(row['answer1.' + str(d['question_num']) + '.0']) > 0:
        	d['time_page1'] = ast.literal_eval(
        	    row['answer1.' + str(d['question_num']) + '.0'])['time'] / 1000.0  # in seconds
        else:
        	d['time_page1'] = -1
        d['time_page2'] = answerdict['time'] / 1000.0

        # either last page or extra full elicitation
        if len(row['answer1.' + str(d['question_num']) + '.2']) > 0:
            # column is a feedback dict
            if 'political_stance_report' in row['answer1.' + str(d['question_num']) + '.2']:
                feedbackdict = ast.literal_eval(
                    row['answer1.' + str(d['question_num']) + '.2'])
                d['time_page3'] = 0;
                d['time_page4'] = feedbackdict['time'] / 1000.0
            else:
                if 'full' not in row['answer1.' + str(d['question_num']) + '.2']:
                    continue
                extrafull_dict = ast.literal_eval(
                    row['answer1.' + str(d['question_num']) + '.2'])
                d['extra_full_elicitation_data'] = load_data_experiment_full(
                    extrafull_dict, row, 1, deficit_offset, isfullslider=True)
                d['time_page3'] = extrafull_dict['time'] / 1000.0
                d['time_page4'] = -1
        else:
            feedbackdict = {'feedback': ['']}
            d['time_page3'] = 0;
            d['time_page4'] = -1

        if len(row['answer1.' + str(d['question_num']) + '.3']) > 0:  # last page
            feedbackdict = ast.literal_eval(
                row['answer1.' + str(d['question_num']) + '.3'])
            d['time_page4'] = feedbackdict['time'] / 1000.0

        d['feedback_data'] = load_feedback(feedbackdict, row)

        # print d['experiment_id'], d['question_num'], answerdict, row
        d['question_data'] = switcher_load_data[mechanism_super_dictionary[d['question_num']]['type']](
            answerdict, row, mechanism_super_dictionary[d['question_num']]['numsets'], deficit_offset)

        clean.append(d)
        organized_data[d['question_num']].append(d)
    for key in organized_data:
        organized_data[key] = sorted(
            organized_data[key], key=itemgetter('begin_time'))
    return clean, organized_data


def barplot(dpoints, label, ylabel, xlabel, categories_order, conditions_order, fig = None, ax=None, showplot=True, createlegend=True, doboxplot = True):
    '''
    copied from http://emptypipes.org/2013/11/09/matplotlib-multicategory-barchart/ on 6/27/2016
        modified to take in the matrix already rather than calculating mean values
    Create a barchart for data across different categories with
    multiple conditions for each category.

    @param ax: The plotting axes from matplotlib.
    @param dpoints: The data set as an (n, 3) numpy array
    '''
    with suppress_stdout_stderr():
        wasNone = False
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            wasNone = True

        # Aggregate the conditions and the categories according to their
        # mean values
        conditions = [(c, np.mean(dpoints[dpoints[:, 0] == c][:, 2].astype(float)))
                      for c in np.unique(dpoints[:, 0])]
        categories = [(c, np.mean(dpoints[dpoints[:, 1] == c][:, 2].astype(float)))
                      for c in np.unique(dpoints[:, 1])]

        # sort the conditions, categories and data so that the bars in
        # the plot will be ordered by category and condition
        conditions = [c[0] for c in sorted(conditions, key=o.itemgetter(1))]
        categories = [c[0] for c in sorted(categories, key=o.itemgetter(1))]
        categories = categories_order
        conditions = conditions_order

        dpoints = np.array(
            sorted(dpoints, key=lambda x: categories.index(x[1])))

        # the space between each set of bars
        space = 0.3
        n = len(conditions)
        width = (1 - space) / (len(conditions))
        current_palette = sns.color_palette()

        # Create a set of bars at each position
        for i, cond in enumerate(conditions):
            indeces = range(1, len(categories) + 1)
            vals = dpoints[dpoints[:, 0] == cond][:, 2].astype(np.float)
            stds = None
            if len(dpoints[0,:]) == 4: #includes standard deviations
                stds = dpoints[dpoints[:, 0] == cond][:, 3].astype(np.float)
            pos = [j - (1 - space) / 2. + i * width for j in indeces]
            ax.bar(pos, vals, width=width, label=cond, yerr = stds,
                   color=current_palette[i % len(current_palette)]
                   )

        # Set the x-axis tick labels to be equal to the categories
        ax.set_xticks(indeces)
        ax.set_xticklabels(categories)
        # ax.tick_params(axis='both', which='major', labelsize=18)

        plt.setp(plt.xticks()[1])  # , rotation=90)

        # Add the axis labels
        # ax.set_ylabel(ylabel)  # , fontsize = 18)
        # ax.set_xlabel(xlabel, fontsize = 18)

        # Add a legend
        handles, labels = ax.get_legend_handles_labels()
        # ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize =
        # 18)

        if createlegend:
            ax.legend(handles, labels, loc='upper center',
            				 borderaxespad=.0, ncol=4, fontsize = 5)
            # ax.legend(handles, labels,bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            # ncol=min(len(conditions), 4), mode="expand", borderaxespad=0.,
            # fontsize = 18)
        if showplot:
    		fig.text(.5, 0.03, xlabel, ha='center', va='center', fontsize=7)
    		fig.text(0.02, 0.5, ylabel, ha='center', va='center',
    		       rotation='vertical', fontsize=7)
            # mng = plt.get_current_fig_manager()
            # mng.window.showMaximized()
    		plt.tight_layout()
    		plt.savefig(label + '.pdf', format='pdf', dpi=1000)
    		plt.close()
            # plt.show()

# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])
