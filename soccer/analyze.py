"""
Identifies the exponent that produces the most accurate win % prediction for MLS
"""

import numpy as np
from extract import get_data
from statistics import mean
import pandas as pd

def get_predicted_win_percentage(goals_scored, goals_allowed, exponent):
    var_R = goals_scored/goals_allowed
    return (var_R**exponent) / (var_R**exponent + 1)

#find the best exponent for the predicted win % calculation
def find_best_exponent(team_data):
    best_exponent = {}
    all_exponents = {}
    #calculate predicted percentage win for each team over a range of exponents
    for team,info in team_data.items():
        goals_scored = info["goals_scored"]
        goals_allowed = info["goals_allowed"]
        actual_win_percentage = info["actual_win_percentage"]

        #predicted = [(exp, actual_win_percentage - get_predicted_win_percentage(goals_scored, goals_allowed, exp)) for exp in range(0, 20, 1)]
        predicted = [(exp, actual_win_percentage - get_predicted_win_percentage(goals_scored, goals_allowed, exp)) for exp in np.linspace(0, 20, 101)]
        best = min(predicted, key=lambda tup:abs(tup[1]))
        
        #add result for all potential exponents to a dictionary
        if len(all_exponents) == 0:
            for exp in predicted:
                all_exponents[exp[0]] = [exp[1]]
        else:
            for exp in predicted:
                all_exponents[exp[0]].append(exp[1])

        best_exponent[team] = best
    print(best_exponent)
    all_exponents_means = [(exp, mean(map(abs, values))) for exp,values in all_exponents.items()]
    print(all_exponents_means)
    print(min(all_exponents_means, key=lambda tup:tup[1]))

#attempt 2 - worked better
def find_exponent_method_2():
    #read data into dataframe
    soccer_data = pd.read_csv("mls_2013-16.csv")
    soccer_data['actual-win']=soccer_data['W']/(soccer_data['L']+soccer_data['W'])
    soccer_data['ratio'] = soccer_data['G']/soccer_data['GA']

    #calculates mean error for each exponent and puts that into a dataframe
    exp_results = pd.DataFrame(columns=["exponent", "mean_error"])
    exp_results.loc[len(exp_results.index)] = [1,2]
    for exp in np.linspace(0, 20, 101):
        exp_results.loc[len(exp_results.index)] = [exp,
            np.mean(abs(soccer_data['actual-win']-(soccer_data['ratio']**exp/(1+(soccer_data['ratio']**exp)))))]

    print(exp_results)
    print(exp_results[exp_results.mean_error == exp_results.mean_error.min()])

 

if __name__=="__main__":
    #data = get_data()
    #find_best_exponent(data)

    find_exponent_method_2()