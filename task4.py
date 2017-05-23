from gurobipy import *
from collections import OrderedDict
from tsputil import *
from helpers import *
from itertools import chain, combinations
from sep import *

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


    for idx, s in enumerate(subtours):
        m.addConstr(quicksum(edges[i, j] for i in s for j in s if i < j) <= len(s) - 1, "sec_" + str(idx))    


    ######### END

    m.optimize()
    m.write("tsplp.lp")

    if m.status == GRB.status.OPTIMAL:
        #print('The optimal objective is %g' % m.objVal)
        #m.write("tsplp.sol")  # write the solution
        return {(i, j): edges[i, j].x for i, j in E}
    else:
        #print "Something wrong in solve_tsplp"
        exit(0)
n = 10
ran_points = Cities(n=n,seed=41)

subtours = []

plot_situation(ran_points)

while True:
    values = {}
    sol = solve_tsp(ran_points, subtours)
    for k in range(1, n):
        sub = solve_separation(ran_points, sol, k)
        values[k, sub[0]] = sub[1]

    best = max(values,key=lambda item:item[1])
    
    if best[1] == 0:
        break;

    subtours.append(values[best[0], best[1]])

plot_situation(ran_points, sol)

print range(1,5)
    





