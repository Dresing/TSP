from gurobipy import *
from collections import OrderedDict
from tsputil import *
from helpers import *
from itertools import chain, combinations

def solve_separation(points, x_star, k):
    points=list(points)
    V = range(len(points))
    Vprime = range(1,len(points))
    E = [(i,j) for i in V for j in V if i<j]
    Eprime = [(i,j) for i in Vprime for j in Vprime if i<j]
    E = tuplelist(E)
    Eprime = tuplelist(Eprime)

    m = Model("SEP")
    m.setParam(GRB.param.OutputFlag,0)
    
    ######### BEGIN: Write here your model for Task 4

    edges = {}
    z = {}

    VNoK = filter(lambda i: i != k, Vprime)


    for edge in Eprime:
        edges[edge[0], edge[1]] = m.addVar(name="y" + str(edge[0]) + "_" + str(edge[1]), vtype=GRB.BINARY)

    for vert in Vprime:
        z[vert] = m.addVar(name="z" + str(vert), vtype=GRB.BINARY)

    m.update()    

    m.setObjective(quicksum(x_star[e[0], e[1]] * edges[e[0], e[1]] for e in Eprime) - quicksum(z[v] for v in VNoK) , GRB.MAXIMIZE)


    for edge in edges:
        m.addConstr(edges[edge[0], edge[1]] >= z[edge[0]] - z[edge[1]] - 1, "ec_" + str(edge[0]) + "_" + str(edge[1]))
        m.addConstr(edges[edge[0], edge[1]]  <= z[edge[0]], "lessI_" + str(edge[0]) + "_" + str(edge[1]))
        m.addConstr(edges[edge[0], edge[1]] <= z[edge[1]], "lessJ_" + str(edge[0]) + "_" + str(edge[1]))

    m.addConstr(z[k] == 1, "K_" + str(k))

    ######### END
    m.optimize()
    #m.write("sep.lp")
    
    if m.status == GRB.status.OPTIMAL:
        #print('Separation problem solved for k=%d, solution value %g' % (k,m.objVal))
        #m.write("sep.sol") # write the solution    
        subtour = filter(lambda i: z[i].x>=1,z)
        return m.objVal, subtour
    else:
        #print "Something wrong in solve_tsplp"
        exit(0)


