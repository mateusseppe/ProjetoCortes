import pulp
import pandas as pd
import numpy as np

if __name__ == '__main__':
    I = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    l = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
    demanda = np.random.randint(10, 20, 12)
    l = dict(zip(I, l))
    d = dict(zip(I, demanda))
    n_max = sum(d[i] for i in I)
    J = []
    for i in range(n_max):
        J.append(i+1)
    L = 12

    model = pulp.LpProblem("Problema do corte das barras", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("Corte", ((i, j)
                              for i in I for j in J), lowBound=0, cat='Integer')
    y = pulp.LpVariable.dicts("Barras", J, cat='Binary')
    model += pulp.lpSum(y[j] for j in J)
    for j in J:
        model += pulp.lpSum(x[i, j]*l[i] for i in I) <= L*y[j]
    for i in I:
        model += pulp.lpSum(x[i, j] for j in J) == d[i]
    model.solve()

    # exportando os valores pro excel
    names = []
    values = []
    for variable in model.variables():
        names.append(variable.name)
        values.append(variable.varValue)
    values = np.mat(values)
    values = values.reshape(len(I)+1, len(J))
    values = np.delete(values, (0), axis=0)
    values.shape
    non_used = np.argwhere(np.all(values[..., :] == 0, axis=0))
    values = np.delete(values, non_used, axis=1)
    df = pd.DataFrame(values)
    num_rows, num_cols = values.shape
    df.to_excel("barras.xlsx", sheet_name="Cortes", startcol=1,
                header=range(1, num_cols+1), index=False)
    print("Vetor de demandas:")
    print(demanda)
    print('Número de barras utilizadas:', pulp.value(model.objective))
    soma_blocos = sum(l[i]*d[i] for i in I)
    print("A perda mínima é de:", L*pulp.value(
        model.objective) - soma_blocos, "metros")
