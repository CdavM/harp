#import analyze_data_functionalized
import simulate_entire_experiment_functionalized


def main():
    filename = "test_functionalized_overall.csv"
    LABEL = 'test'
    mechanism_super_dictionary = {0: {'type': 'full', 'name': 'Group 1 Full Elicitation -- Euclidean', 'initial_values': [[450, 1200, 370, 1300, 882]]},
                                  1: {'name': 'Group 1 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'initial_values': [[450, 1200, 370, 1300, 882], [450, 1200, 370, 1300, 882]]},
                                  2: {'name': 'Group 2 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'initial_values': [[450, 1200, 370, 1300, 882], [450, 1200, 370, 1300, 882]]},
                                  3: {'name': 'Group 3 l2 Constrainted Movement', 'type': 'l2', 'numsets': 2, 'initial_values': [[450, 1200, 370, 1300, 882], [450, 1200, 370, 1300, 882]]},
                                  4: {'name': 'Group 1 l1 Constrainted Movement', 'type': 'l1', 'numsets': 2, 'initial_values': [[450, 1200, 370, 1300, 882], [450, 1200, 370, 1300, 882]]},
                                  5: {'name': 'Group 1 Comparisons', 'type': 'comparisons', 'numsets': 2, 'initial_values': [[450, 1200, 370, 1300, 882], [450, 1200, 370, 1300, 882]]}
                                  }

    simulate_entire_experiment_functionalized.simulate_experiment_functionalized(
        filename, LABEL, mechanism_super_dictionary)
    analyze_data_functionalized.analysis_call(filename, LABEL, mechanism_super_dictionary)


if __name__ == "__main__":
    main()
