import simulate_entire_experiment_functionalized
import analyze_data_functionalized
import copy
import os

mechanism_super_dictionary_forloading_from_old_experiments = {2: {'type': 'full', 'name': 'Group 1 Full Elicitation', 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[450, 1200, 350, 1400, 828]]},
                                                              0: {'name': 'Group 1 L2', 'type': 'l2', 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
                                                              3: {'name': 'Group 1 L1', 'type': 'l1', 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
                                                              1: {'name': 'Group 1 Comparisons', 'type': 'comparisons', 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
                                                              }

mechanism_super_dictionary_real_BIGEXPERIMENT1 = {0: {'type': 'full', 'name': 'Full Elicitation', 'do_full_as_well': False, 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[425, 1200, 350, 1450, 753]]},
                                                  1: {'name': 'Group 1 L2', 'type': 'l2', 'do_full_as_well': True, 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[440, 1050, 350, 1500, 828], [541, 1004, 303, 1460, 753]]},
                                                  2: {'name': 'Group 2 L2', 'type': 'l2', 'do_full_as_well': False, 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[541, 1004, 303, 1460, 753], [500, 1100, 350, 1540, 828]]},
                                                  3: {'name': 'Group 3 L2', 'type': 'l2', 'do_full_as_well': False, 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1100, 350, 1540, 828], [440, 1050, 350, 1500, 828]]},
                                                  4: {'name': 'Group 1 L1', 'type': 'l1', 'do_full_as_well': True, 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[440, 1050, 350, 1500, 828], [541, 1004, 303, 1460, 753]]},
                                                  5: {'name': 'Group 2 L1', 'type': 'l1', 'do_full_as_well': False, 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[541, 1004, 303, 1460, 753], [500, 1100, 350, 1540, 828]]},
                                                  6: {'name': 'Group 3 L1', 'type': 'l1', 'do_full_as_well': False, 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1100, 350, 1540, 828], [440, 1050, 350, 1500, 828]]}
                                                  }

mechanism_super_dictionary_real_BIGEXPERIMENT2 = {0: {'type': 'full', 'name': 'Ideal Pts.', 'do_full_as_well': False, 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[800, 1250, 400, 1500, 828]]},
                                       1: {'name': '$\mathcal{L}^2$ Group 1', 'do_full_as_well': True, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 200, 1300, 828], [200, 800, 300, 1400, 828]]},
                                       2: {'name': '$\mathcal{L}^2$ Group 2', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       3: {'name': '$\mathcal{L}^2$ Group 3', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                       4: {'name': '$\mathcal{L}^1$ Group 1', 'do_full_as_well': True, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                       5: {'name': '$\mathcal{L}^1$ Group 2', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       6: {'name': '$\mathcal{L}^1$ Group 3 ', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                       7: {'name': '$\mathcal{L}^\infty$ Group 1', 'do_full_as_well': True, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                       8: {'name': '$\mathcal{L}^\infty$ Group 2', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       9: {'name': '$\mathcal{L}^\infty$ Group 3', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]}
                                       }

mechanism_super_dictionary_BIGsCOMBINED = {0: {'type': 'full', 'name': 'Exp2 Group0 Full', 'do_full_as_well': False, 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[800, 1250, 400, 1500, 828]]},
                                       1: {'name': 'Exp2 Group1 l2', 'do_full_as_well': True, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 200, 1300, 828], [200, 800, 300, 1400, 828]]},
                                       2: {'name': 'Exp2 Group2 l2', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       3: {'name': 'Exp2 Group3 l2', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                       4: {'name': 'Exp2 Group4 l1', 'do_full_as_well': True, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                       5: {'name': 'Exp2 Group5 l1', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       6: {'name': 'Exp2 Group6 l1', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                       7: {'name': 'Exp2 Group7 linf', 'do_full_as_well': True, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                       8: {'name': 'Exp2 Group8 linf', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       9: {'name': 'Exp2 Group9 linf', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                       10: {'type': 'full', 'name': 'Exp1 Group0 Full', 'do_full_as_well': False, 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[800, 1250, 400, 1500, 828]]},
                                      11: {'name': 'Exp1 Group1 l2', 'do_full_as_well': True, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 200, 1300, 828], [200, 800, 300, 1400, 828]]},
                                      12: {'name': 'Exp1 Group2 l2', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                      13: {'name': 'Exp1 Group3 l2', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                      14: {'name': 'Exp1 Group4 l1', 'do_full_as_well': True, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                      15: {'name': 'Exp1 Group5 l1', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                      16: {'name': 'Exp1 Group6 l1', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                      }


def plotHistogramFromFile():
    filename = "simulations/REAL_fullelicitation_withouteducation.csv"
    mechanism_super_dictionary = {0: {'type': 'l2', 'name': 'Group 1 Full Elicitation', 'numsets': 1, 'initial_values': [[450, 1200, 350, 1400, 828]]},
                                  1: {'name': 'Group 1 L2', 'type': 'comparisons', 'numsets': 2, 'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
                                  2: {'name': 'full', 'type': 'full', 'numsets': 1, 'initial_values': [[450, 1200, 350, 1400, 828]]}
                                  }

    analyze_data_functionalized.analysis_call(
        filename, 'whatever', mechanism_super_dictionary, plotHistogramOfFull=True)


def actual_experiment_analysis():
    alreadyPaidFiles = ['Experiment2Day10_bonusinfo_uploaded.csv','BIGEXPERIMENT2_bonus_to_upload_ALLCOMBINED_DONE.csv', 'new_bonus_upload_that_missed.csv', 'BIGEXPERIMENT2_bonus_to_upload.csv', 'Experiment2Day8_bonusinfo_uploaded.csv']
    deficit_offset = 228
    labels = ['L2', 'L1', 'Linf', 'Full', 'L2Single', 'L1Single',
              'Comparisons', 'ComparisonsSingle']

    filename = 'export-20161016202931_BIGEXPERIMENT2FINAL.csv'
    LABEL = 'Exp2FINALclean_'
    lines_to_do = [[1, 2, 3, 0], [4, 5, 6, 0], [7, 8, 9, 0]]
    mechdict_to_use = mechanism_super_dictionary_real_BIGEXPERIMENT2
    lines_to_do_fullhist = [[0,1,4,7]]#[0], [1], [4], [7], [0,1,4,7]]
    labels_fullhist = ['All']#'Full Only', 'With L2', 'With L1', 'With Linf', 'All']
    lines_to_do_creditshist = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    labels_creditshist = ['L2', 'L1', 'Linf']
    # filename = 'experiments_BOTHLARGECOMBINED.csv'
    # LABEL = "BIGEXPERIMENTSCOMBINED"
    # lines_to_do = [[0, 10, 1, 2, 3, 11, 12, 13], [0, 10, 4, 5, 6, 14, 15, 16], [0, 10, 7, 8, 9], [0, 10]]
    # mechdict_to_use = mechanism_super_dictionary_BIGsCOMBINED



    # analyze_data_functionalized.analysis_call(
    #         filename, LABEL, copy.deepcopy(mechdict_to_use), plotHistogramOfFull=False, plotConvergenceAnalysis = True, lines_to_do=lines_to_do, labels=labels, \
    #         deficit_offset=deficit_offset, lines_to_do_fullhist = lines_to_do_fullhist, labels_fullhist = labels_fullhist)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechdict_to_use), alreadyPaidFiles=alreadyPaidFiles, deficit_offset=deficit_offset, \
    #  lines_to_do=lines_to_do, labels=labels, analyzeUtilityFunctions=True, lines_to_do_fullhist = lines_to_do_fullhist, labels_fullhist = labels_fullhist, \
    #  plotAllOverTime=True, organizePayment=False, analyzeExtraFull=True, average_iteratively = True,plotConvergenceAnalysis = True,\
    #  lines_to_do_creditshist = lines_to_do_creditshist, labels_creditshist = labels_creditshist, plotHistogramOfFull=True)

    analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechdict_to_use), alreadyPaidFiles=alreadyPaidFiles, deficit_offset=deficit_offset, \
     lines_to_do=lines_to_do, labels=labels, analyzeUtilityFunctions=False, lines_to_do_fullhist = lines_to_do_fullhist, labels_fullhist = labels_fullhist, \
     plotAllOverTime=False, organizePayment=False, analyzeExtraFull=False, average_iteratively =False,plotConvergenceAnalysis =True,\
     lines_to_do_creditshist = lines_to_do_creditshist, labels_creditshist = labels_creditshist, plotHistogramOfFull=False)

mechanism_super_dictionary_linfonly= {0: {'type': 'full', 'name': 'Group 1 Full', 'do_full_as_well': False, 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[800, 1250, 400, 1500, 828]]},
                                       1: {'name': 'Group 1 $l_\infty$', 'do_full_as_well': True, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                       2: {'name': 'Group 2 $l_\infty$', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                       3: {'name': 'Group 3 $l_\infty$', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]}
                                       }

def simulateLinfWithSpecialUtility():
    deficit_offset = 228

    LIMIT = 1200
    mechdict_to_use = mechanism_super_dictionary_linfonly
    lines_to_do = [[0, 1, 2, 3]]
    labels = ['Linf']
    lines_to_do_fullhist = [[0,1]]#[0], [1], [4], [7], [0,1,4,7]]
    labels_fullhist = ['Linf']#'Full Only', 'With L2', 'With L1', 'With Linf', 'All']
    lines_to_do_creditshist = [[1, 2, 3]]
    labels_creditshist = ['Linf']

    # LIMIT = 2500
    # lines_to_do = [[0, 1, 2, 3], [0, 4, 5, 6], [0, 7, 8, 9]]
    # mechdict_to_use = mechanism_super_dictionary_real_BIGEXPERIMENT2
    # lines_to_do_fullhist = [[0,1,4,7]]#[0], [1], [4], [7], [0,1,4,7]]
    # labels_fullhist = ['All']#'Full Only', 'With L2', 'With L1', 'With Linf', 'All']
    # lines_to_do_creditshist = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # labels_creditshist = ['L2', 'L1', 'Linf']
    # labels = ['L2', 'L1', 'Linf', 'Full', 'L2Single', 'L1Single',
    #           'Comparisons', 'ComparisonsSingle']


    radius_parameters = {
        'radius_type': 'decreasing_slow_increasing', 'starting': 100, 'decrease_every': 7}

    load_people_from_file = True
    filename_forloadingpeople = "C:\\Users\\Nikhil\\Dropbox\\src\\harp\\private\\analysis\\export-20161016202931_BIGEXPERIMENT2FINAL.csv"

    superdictionary_forloadingpeople = mechanism_super_dictionary_real_BIGEXPERIMENT2
    deficit_offset_forloadingpeople = 228

    LABEL = 'Simulate_fixed' + "_"
    filename = "simulations/" + LABEL + ".csv"



    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #     filename, LABEL, copy.deepcopy(mechanism_super_dictionary_linfonly), deficit_offset=deficit_offset, \
    #      LIMIT=LIMIT, radius_parameters=radius_parameters, load_people_from_file=load_people_from_file, \
    #       filename_forloadingpeople=filename_forloadingpeople, superdictionary_forloadingpeople=superdictionary_forloadingpeople, \
    #        deficit_offset_forloadingpeople=deficit_offset_forloadingpeople,make_deficit_ideal_neg_infin = False, addeducationoffset = False, onesided = False, quadratic = True)
    #
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(
    #     mechanism_super_dictionary_linfonly), deficit_offset=deficit_offset, lines_to_do=lines_to_do, labels=labels, plotAllOverTime=True, \
    #     analyzeUtilityFunctions=True, lines_to_do_fullhist = lines_to_do_fullhist, labels_fullhist = labels_fullhist, \
    #     organizePayment=False, analyzeExtraFull=True, average_iteratively = True, plotConvergenceAnalysis = True,\
    #     lines_to_do_creditshist = lines_to_do_creditshist, labels_creditshist = labels_creditshist, plotHistogramOfFull=True)

    simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
        filename, LABEL, copy.deepcopy(mechdict_to_use), deficit_offset=deficit_offset, \
         LIMIT=LIMIT, radius_parameters=radius_parameters, load_people_from_file=load_people_from_file, \
          filename_forloadingpeople=filename_forloadingpeople, superdictionary_forloadingpeople=superdictionary_forloadingpeople, \
           deficit_offset_forloadingpeople=deficit_offset_forloadingpeople,make_deficit_ideal_neg_infin = False, addeducationoffset = False, onesided = True, quadratic = False)

    analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(
        mechdict_to_use), deficit_offset=deficit_offset, lines_to_do=lines_to_do, labels=labels, plotAllOverTime=True, \
        analyzeUtilityFunctions=True, lines_to_do_fullhist = lines_to_do_fullhist, labels_fullhist = labels_fullhist, \
        organizePayment=False, analyzeExtraFull=True, average_iteratively = False, plotConvergenceAnalysis = True,\
        lines_to_do_creditshist = lines_to_do_creditshist, labels_creditshist = labels_creditshist, plotHistogramOfFull=True)

def main():
    deficit_offset = 228
    LIMIT = 3000

    # , [0, 7, 8, 9], [0, 7]]
    lines_to_do = [[0, 1, 2, 3], [0, 4, 5, 6], [0, 7, 8, 9]]
    labels = ['L2', 'L1', 'Linf', 'L2Single', 'L1Single',
              'Comparisons', 'ComparisonsSingle']
    radius_parameters_1 = {
        'radius_type': 'decreasing_slow', 'starting': 50, 'decrease_every': 5}
    radius_parameters_2 = {'radius_type': 'constant', 'starting': 50}
    radius_parameters_3 = {'radius_type': 'decreasing', 'starting': 50}

    mechanism_super_dictionary_BIG2_farapart = {0: {'type': 'full', 'name': 'Group 1 Full Elicitation -- Euclidean', 'do_full_as_well': False, 'numsets': 1, 'num_to_average_per_step': 1, 'initial_values': [[800, 1250, 400, 1500, 828]]},
                                                1: {'name': 'Group 1 l2 Constrainted Movement', 'do_full_as_well': True, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 200, 1300, 828], [200, 800, 300, 1400, 828]]},
                                                2: {'name': 'Group 2 l2 Constrainted Movement', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                                3: {'name': 'Group 3 l2 Constrainted Movement', 'do_full_as_well': False, 'type': 'l2', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                                4: {'name': 'Group 1 l1 Constrainted Movement', 'do_full_as_well': True, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                                5: {'name': 'Group 2 l1 Constrainted Movement', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                                6: {'name': 'Group 3 l1 Constrainted Movement', 'do_full_as_well': False, 'type': 'l1', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]},
                                                7: {'name': 'Group 1 linf Constrained Movement', 'do_full_as_well': True, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [200, 800, 200, 1400, 828]]},
                                                8: {'name': 'Group 2 linf Constrained Movement', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[500, 1000, 300, 1300, 828], [800, 1250, 400, 1500, 828]]},
                                                9: {'name': 'Group 3 linf Constrained Movement', 'do_full_as_well': False, 'type': 'linf', 'numsets': 2, 'num_to_average_per_step': 10, 'initial_values': [[800, 1250, 400, 1500, 828], [200, 800, 200, 1400, 828]]}
                                                }

    load_people_from_file = True
    filename_forloadingpeople = "C:\\Users\\Nikhil\\Dropbox\\src\\harp\\private\\resultssofar\\FinalDatas\\export-20160722200126_SECONDRUN_FINAL_sampleforsimulation.csv"
    filename_forloadingpeople = "C:\\Users\\Nikhil\\Dropbox\\src\\harp\\private\\resultssofar\\FinalDatas\\export-20160718044154_FIRSTREALRUN_FINAL_sampleforsimulation.csv"
    filename_forloadingpeople = "C:\\Users\\Nikhil\\Dropbox\\src\\harp\\private\\resultssofar\\FinalDatas\\export-20160906041734_BIGEXPERIMENT_FINAL.csv"

    superdictionary_forloadingpeople = mechanism_super_dictionary_real_BIGEXPERIMENT1
    deficit_offset_forloadingpeople = 228

    # [50, 75, 100]:#[15, 75, 25, 50, 35, 100, 10]:
    for starting_radius in [150]:
        for decrease_every in [7]:  # [7, 10, 12]:#[1, 3, 5, 10, 15, 20, 25]:
            for ppl_in_block in [10]:  # [10, 15]:#[1, 3, 5, 10, 15, 20]:
                LABEL = 'BE2far_fromfile_sameradiusdecrate' + str(starting_radius) + 'DecreaseEvery' + str(
                    decrease_every) + 'Block' + str(ppl_in_block) + "ppl" + str(LIMIT) + "_"
                filename = "simulations/" + LABEL + ".csv"
                if os.path.isfile(filename):
                    print "skipping because exists", starting_radius, decrease_every, ppl_in_block
                    continue
                print starting_radius, decrease_every, ppl_in_block

                radius_parameters_loop = {'radius_type': 'decreasing_slow',
                                          'starting': starting_radius, 'decrease_every': decrease_every}

                for mech in mechanism_super_dictionary_BIG2_farapart:
                    if mechanism_super_dictionary_BIG2_farapart[mech]['type'] != 'full':
                        mechanism_super_dictionary_BIG2_farapart[mech][
                            'num_to_average_per_step'] = ppl_in_block
                simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
                    filename, LABEL, copy.deepcopy(mechanism_super_dictionary_BIG2_farapart), deficit_offset=deficit_offset, LIMIT=LIMIT, radius_parameters=radius_parameters_loop, load_people_from_file=load_people_from_file, filename_forloadingpeople=filename_forloadingpeople, superdictionary_forloadingpeople=superdictionary_forloadingpeople, deficit_offset_forloadingpeople=deficit_offset_forloadingpeople)
                analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(
                    mechanism_super_dictionary_BIG2_farapart), deficit_offset=deficit_offset, lines_to_do=lines_to_do, labels=labels, plotAllOverTime=True)

if __name__ == "__main__":
    #simulateLinfWithSpecialUtility()
    actual_experiment_analysis()
    # main()
    # plotHistogramFromFile()
    print 'done'
