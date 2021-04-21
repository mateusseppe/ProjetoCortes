import pandas as pd
import pulp
import numpy as np
from collections import Counter

blocos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
length = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
demanda = np.random.randint(10, 20, 12)
print(demanda)
print(length)
l = dict(zip(blocos, length))
d = dict(zip(blocos, demanda))
n_max = sum(l[i]*d[i] for i in blocos)
n_max = n_max/6
n_max = int(n_max)
I = []
for i in range(n_max):
    I.append(i+1)

if __name__ == '__main__':
    model = pulp.LpProblem("Problema dos Cortes", pulp.LpMinimize)
    y = pulp.LpVariable.dicts("Barra", I, cat='Binary')
    x = pulp.LpVariable.dicts("Bloco por barra", ((i, j)
                                                  for i in I for j in blocos), lowBound=0, cat='Integer')
    model += pulp.lpSum(y[i] for i in I)
    for i in I:
        model += pulp.lpSum(l[j]*x[i, j]
                            for j in blocos) <= 12*y[i]
    for j in blocos:
        model += pulp.lpSum(x[i, j] for i in I) == d[j]
    #solver = pulp.getSolver('GUROBI')
    # model.solve(solver)
    model.solve()
    names = []
    values = []
    print(type(x))
    for variable in model.variables():
        names.append(variable.name)
        values.append(variable.varValue)
        # if variable.varValue != 0:
        # print("{}".format(variable.name))
        # print("{}".format(variable.varValue))

    print('Custo Total', pulp.value(model.objective))
