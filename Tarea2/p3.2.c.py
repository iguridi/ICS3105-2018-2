import model

import gurobipy as gp

try:

    # Create a new model
    m = gp.Model("dual lp")

    # Create variables
    f_ = []
    for s in model.S:
        x_vars = {}
        for x in model.X(s):
            obj = m.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, name=f'f_{{{s},{x}}}')
            x_vars[x] = obj

        f_.append(x_vars)

    # set objective
    obj = 0
    for s in range(len(f_)):
        for x in f_[s]:
            obj += f_[s][x] * model.r(s, x)

    m.setObjective(obj, gp.GRB.MAXIMIZE)

    # set restrictions
    factor = 0.9
    for s1 in model.S:
        rtn = 0
        rtn += sum(f_[s1].values())
        for s in model.S:
            for x in model.X(s):
                rtn -= factor * f_[s][x] * model.p(s1, s, x)

        m.addConstr( rtn == 1, f'c{s1}' )

    m.optimize()

    # m.printAttr([s[x] for s in f_ for x in s])
    

    # print('Obj: %g' % m.objVal)
    def printSolution():
        if m.status == gp.GRB.Status.OPTIMAL:
            print('\nValue: %g' % m.objVal)
            for v in m.getVars():
                print('%s %g' % (v.varName, v.x))
        else:
            print('No solution')
    
    printSolution()



except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

# except AttributeError:
#     print('Encountered an attribute error')
