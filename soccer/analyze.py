import numpy as np
from extract import get_data
from statistics import mean

def get_predicted_win_percentage(goals_scored, goals_allowed, exponent):
    var_R = goals_scored/goals_allowed

    return (var_R**exponent) / (var_R**exponent + 1)

def find_best_exponent(team_data):
    best_exponent = {}
    all_exponents = {}
    for team,info in team_data.items():
        goals_scored = info["goals_scored"]
        goals_allowed = info["goals_allowed"]
        actual_win_percentage = info["actual_win_percentage"]

        #predicted = [(exp, actual_win_percentage - get_predicted_win_percentage(goals_scored, goals_allowed, exp)) for exp in range(0, 20, 1)]
        predicted = [(exp, actual_win_percentage - get_predicted_win_percentage(goals_scored, goals_allowed, exp)) for exp in np.linspace(0, 20, 101)]
        best = min(predicted, key=lambda tup:abs(tup[1]))
        if len(all_exponents) is 0:
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
 

if __name__=="__main__":
    data = get_data()
    find_best_exponent(data)