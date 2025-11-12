import pandas as pd

def max_p(matrix_):
    max_=0
    for row in matrix_:
        for i in matrix_[row]:
            if i>max_:
                max_=i

    return max_

def probability_matrix(res_, team1_, team2_):
    team1_goals=res_[0][f'{team1_}']['goals']
    team1_ps=res_[0][f'{team1_}']['p']

    team2_goals=res_[0][f'{team2_}']['goals']
    team2_ps=res_[0][f'{team2_}']['p']

    matrix=pd.DataFrame(index=team2_goals, columns=team1_goals)

    for i in range(len(team1_goals)):
        for j in range(len(team2_goals)):
            matrix.iloc[j, i]=team1_ps[i]*team2_ps[j]

    return matrix