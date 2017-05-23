from gurobipy import *
from collections import OrderedDict
from tsputil import *
from helpers import *
from itertools import chain, combinations

def solve_tsp(points, subtours=[]):
    points = list(points)
    V = range(len(points))
    E = [(i, j) for i in V for j in V if i < j]
    E = tuplelist(E)

    m = Model("TSP0")
    m.setParam(GRB.param.Presolve, 0)
    m.setParam(GRB.param.Method, 0)
    m.setParam(GRB.param.MIPGap, 1e-7)

    ######### BEGIN: Write here your model for Task 1

    edges = {}

    #Add a variable for every edge. Store in OrderedDict for simplicity.
    for edge in E:
        edges[edge[0], edge[1]] = m.addVar(name="x" + str(edge[0]) + "_" + str(edge[1]), ub=1)

    m.update()



    #Set objective to minimize cost (SUM: x_i,j * c_i,j)
    m.setObjective(quicksum(edges[e[0], e[1]] * distance(points[e[0]], points[e[1]]) for e in E), GRB.MINIMIZE)

    #Degree constraint
    for i in V:
        m.addConstr(quicksum(edges[k, l] for (k, l) in E if k == i or l == i) == 2, "dc_" + str(i))


    #Manually added constraints
    S = [(0, 3, 6, 9, 19), (10, 12, 18), (4, 7, 16), (12, 18), (0, 3, 6, 8, 9, 19), (2, 4, 5, 7, 10, 13, 14, 16), (0, 3, 6, 8, 9, 12, 18, 19)]

    for idx, s in enumerate(S):
        m.addConstr(quicksum(edges[i, j] for i in s for j in s if i < j) <= len(s) - 1, "sec_" + str(idx))

    ######### END

    m.optimize()
    m.write("tsplp.lp")

    if m.status == GRB.status.OPTIMAL:
        print('The optimal objective is %g' % m.objVal)
        m.write("tsplp.sol")  # write the solution
        return {(i, j): edges[i, j].x>=0.99 for i, j in E}
    else:
        print "Something wrong in solve_tsplp"
        exit(0)

ran_points = Cities(n=20,seed=42)



sol = solve_tsp(ran_points, [])

plot_situation(ran_points, sol)

