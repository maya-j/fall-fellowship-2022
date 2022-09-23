import pandas as pd
import numpy as np


def get_R_score(goals_scored, goals_allowed):
    return goals_scored/goals_allowed

def predicted_win_percentage(R_score, exp):
    return (R_score ** exp) / ((R_score ** exp) + 1)

def actual_win_percentage(total_wins, games_played):
    return total_wins/games_played

def find_exponent(data):
    num_of_teams = len(data) - 1 # minus the header row
    predicted = []

    for i in range(1, num_of_teams + 1):
        total_wins = data.W[i]
        games_played = data.GP[i]
        total_goals = data.G[i]
        goals_against = data.GA[i]
        actual_win_percent = actual_win_percentage(float(total_wins), float(games_played))
        R_score = get_R_score(float(total_goals), float(goals_against))
        possible_exp = np.linspace(0, 20, 201)

        for exponent in possible_exp:
            predicted_win_percent = predicted_win_percentage(R_score, exponent)
            error = actual_win_percent - predicted_win_percent
            predicted.append((exponent, error))

    best_exp = min(predicted, key=lambda x: abs(x[1]))
    return best_exp[0]

if __name__=="__main__":
    data = pd.read_csv("mls_2016.csv")
    find_exponent(data)