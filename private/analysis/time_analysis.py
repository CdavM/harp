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

def main():

    times = []
#    with open('export-20160727220017.csv', 'rb') as file:
    with open('export-20160718044154_FIRSTREALRUN_FINAL.csv', 'rb') as file:
#    with open('export-20160722200126_SECONDRUN_FINAL.csv', 'rb') as file:
        reader = csv.DictReader(file)
        times = [float(row['initial_time']) for row in reader]
    times = sorted(times)
    minn = times[0]
    times = [x - minn for x in times]

    plt.scatter(range(len(times)), times)
    plt.xlabel('Person number')
    plt.ylabel('Timestamp')
    plt.show()

if __name__ == "__main__":
    main()     


