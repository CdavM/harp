import simulate_entire_experiment_functionalized
import analyze_data_functionalized
import copy
import os
def plotHistogramFromFile():
  filename = "simulations/REAL_fullelicitation_withouteducation.csv"
  mechanism_super_dictionary = {0: {'type': 'l2', 'name': 'Group 1 Full Elicitation -- Euclidean', 'numsets': 1, 'initial_values': [[450, 1200, 350, 1400, 828]]},
                                  1: {'name': 'Group 1 l2 Constrainted Movement', 'type': 'comparisons', 'numsets': 2, 'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
                                  2: {'name': 'full', 'type': 'full', 'numsets': 1, 'initial_values': [[450, 1200, 350, 1400, 828]]}
                                  }

  analyze_data_functionalized.analysis_call(filename, 'whatever', mechanism_super_dictionary, plotHistogramOfFull = True)

def main():
    deficit_offset = 228
    LIMIT = 2500

    lines_to_do = [[0, 1, 2, 3], [0, 1], [0, 4, 5, 6], [0, 4]]#, [0, 7, 8, 9], [0, 7]]
    labels = ['L2', 'L2Single', 'L1', 'L1Single', 'Comparisons', 'ComparisonsSingle']
    radius_parameters_1 = {'radius_type' : 'decreasing_slow', 'starting' : 50, 'decrease_every' : 5}
    radius_parameters_2 = {'radius_type' : 'constant', 'starting' : 50}
    radius_parameters_3 = {'radius_type' : 'decreasing', 'starting' : 50}


    # mechanism_super_dictionary = {0: {'type': 'full', 'name': 'Group 1 Full Elicitation -- Euclidean', 'numsets': 1, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828]]},
    #                               1: {'name': 'Group 1 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
    #                               2: {'name': 'Group 2 l2 Constrainted Movement', 'type': 'l2', 'numsets': 1, 'num_to_average_per_step' : 10,'initial_values': [[450, 1200, 350, 1400, 828]]},
    #                               3: {'name': 'Group 3 l2 Constrainted Movement', 'type': 'l2', 'numsets': 1, 'num_to_average_per_step' : 10,'initial_values': [[450, 1200, 350, 1400, 828]]},
    #                               4: {'name': 'Group 1 l1 Constrainted Movement', 'type': 'l1', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
    #                               5: {'name': 'Group 2 l1 Constrainted Movement', 'type': 'l1', 'numsets': 1, 'num_to_average_per_step' : 10,'initial_values': [[450, 1200, 350, 1400, 828]]},
    #                               6: {'name': 'Group 3 l1 Constrainted Movement', 'type': 'l1', 'numsets': 1, 'num_to_average_per_step' : 10,'initial_values': [[450, 1200, 350, 1400, 828]]}
    #                               # 7: {'name': 'Group 1 Comparisons', 'type': 'comparisons', 'numsets': 2, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
    #                               # 8: {'name': 'Group 2 Comparisons', 'type': 'comparisons', 'numsets': 1, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828]]},
    #                               # 9: {'name': 'Group 3 Comparisons', 'type': 'comparisons', 'numsets': 1, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828]]}
    #                              }
    mechanism_super_dictionary_exact= {0:{'type': 'full', 'name': 'Group 1 Full Elicitation -- Euclidean', 'numsets': 1, 'num_to_average_per_step' : 1,'initial_values': [[425, 1200, 350, 1450, 753]]},
                                  1: {'name': 'Group 1 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[425, 1200, 350, 1450, 753], [450, 1100, 300, 1400, 828]]},
                                  2: {'name': 'Group 2 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[425, 1200, 350, 1450, 753], [500, 1000, 250, 1350, 753]]},
                                  3: {'name': 'Group 3 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[425, 1200, 350, 1450, 753], [390, 1100, 300, 1430, 753]]},
                                  4: {'name': 'Group 1 l1 Constrainted Movement', 'type': 'l1', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[425, 1200, 350, 1450, 753], [450, 1100, 300, 1400, 828]]},
                                  5: {'name': 'Group 2 l1 Constrainted Movement', 'type': 'l1', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[425, 1200, 350, 1450, 753], [500, 1000, 250, 1350, 753]]},
                                  6: {'name': 'Group 3 l1 Constrainted Movement', 'type': 'l1', 'numsets': 2, 'num_to_average_per_step' : 10,'initial_values': [[425, 1200, 350, 1450, 753], [390, 1100, 300, 1430, 753]]}
                                  # 7: {'name': 'Group 1 Comparisons', 'type': 'comparisons', 'numsets': 2, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828], [600, 950, 300, 1300, 828]]},
                                  # 8: {'name': 'Group 2 Comparisons', 'type': 'comparisons', 'numsets': 1, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828]]},
                                  # 9: {'name': 'Group 3 Comparisons', 'type': 'comparisons', 'numsets': 1, 'num_to_average_per_step' : 1,'initial_values': [[450, 1200, 350, 1400, 828]]}
                                  }


    for starting_radius in [10, 100, 35, 50, 25, 75, 15]:
      for decrease_every in [25,20,15,10,5,3,1]:
        for ppl_in_block in [1, 3, 5, 10, 15, 20]:
          LABEL = 'Loop_Starting' + str(starting_radius) + 'DecreaseEvery' + str(decrease_every) + 'Block' + str(ppl_in_block) + "_"
          filename = "simulations/" + LABEL + ".csv";
          if os.path.isfile(filename):
            print "skipping because exists", starting_radius, decrease_every, ppl_in_block
            continue
          print starting_radius, decrease_every, ppl_in_block

          radius_parameters_loop = {'radius_type' : 'decreasing_slow', 'starting' : starting_radius, 'decrease_every' : decrease_every}

          for mech in mechanism_super_dictionary_exact:
            if mechanism_super_dictionary_exact[mech]['type'] != 'full':
              mechanism_super_dictionary_exact[mech]['num_to_average_per_step'] = ppl_in_block
          try:
            simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
                 filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_loop)
          except:
            print "exception on simulated", starting_radius, decrease_every, ppl_in_block
          
          try:
            analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels, plotAllOverTime = True)
          except:
            print "exception on analysis", starting_radius, decrease_every, ppl_in_block
            pass

    # LABEL = 'TestAveraging10_decreasing50_5_' + str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";
    # radius_parameters_1 = {'radius_type' : 'decreasing_slow', 'starting' : 25, 'decrease_every' : 5}

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_1)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels, plotAllOverTime = True)


    # LABEL = 'RD_exact_decreasingSLOWEST10_' + str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";
    # radius_parameters_1 = {'radius_type' : 'decreasing_slow', 'starting' : 10, 'decrease_every' : 50}

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_1)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels, plotAllOverTime = True)

    # LABEL = 'RD_Exact_decreasingslow50_' + str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_1)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels,plotAllOverTime = True)

    # LABEL = 'RD_exact_decreasingslow25_' + str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";

    # radius_parameters_1 = {'radius_type' : 'decreasing_slow', 'starting' : 25, 'decrease_every' : 5}

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_1)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels, plotAllOverTime = True)

    # LABEL = 'RD_exact_decreasingslow15_' + str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";

    # radius_parameters_1 = {'radius_type' : 'decreasing_slow', 'starting' : 15, 'decrease_every' : 5}

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_1)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels, plotAllOverTime = True)

    # LABEL = 'RD_exact_decreasingslower15_' + str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";

    # radius_parameters_1 = {'radius_type' : 'decreasing_slow', 'starting' : 15, 'decrease_every' : 20}

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_1)
    # analyze_data_functionalized.analysis_call(filename, LABEL, copy.deepcopy(mechanism_super_dictionary_exact), deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels, plotAllOverTime = True)


    # LABEL = 'RD_AtAndAboveEquil_decreasingfast250_'+ str(LIMIT) + "ppl" + "_"
    # filename = "simulations/" + LABEL + ".csv";
    # radius_parameters_3 = {'radius_type' : 'decreasing', 'starting' : 250}

    # simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
    #      filename, LABEL, mechanism_super_dictionary, deficit_offset = deficit_offset, LIMIT = LIMIT, radius_parameters = radius_parameters_3)
    # analyze_data_functionalized.analysis_call(filename, LABEL, mechanism_super_dictionary, deficit_offset = deficit_offset, lines_to_do = lines_to_do, labels = labels,plotAllOverTime = True)


if __name__ == "__main__":
    main()
    #plotHistogramFromFile()
    print 'done'