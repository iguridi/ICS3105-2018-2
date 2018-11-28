from scipy.stats import poisson


def Q(s):
    # heuristica: agendar las operaciones más largas primero
    # en el segundo lugar factible
    for i in range(I, -1, -1):
        pass





def calculate_diff(old, new):
    suma = 0
    for i in range(len(old)):
        suma += (new[i]-old[i])**2
    print(suma)
    return suma**0.5


I = 2  # tipos de cirugías
E = 6  # cantidad de pabellones


def k(x): return 3 * x  # costo por posponer agendamiento urgente
def h(x): return 1 * x

r = {'lambda' + str(i): 2 for i in range(I)}  # duración de la operación

q = {
    'urgente': {i: 2 for i in range(I)},
    'no-urgente': {i: 2 for i in range(I)}
}  # llegada de pacientes

S = {
    'u': [[0, 0] for i in range(I)],
    'w': [0 for i in range(I)]
}
# S['u'][2][3]['urgente']


def R1(s, des): pass
# S['u'][i][v][]

# desicion = (i,v,j,x,y)


def rec(assigns, total, i=0):
    if i >= len(assigns):
        yield assigns
        return
    for j in range(0, total+1):
        yield from rec(assigns[:i] + [j] + assigns[i+1:], total-j, i+1)

def x(s):
    # returns ((urgent, no-urgent), ...)
    accs = set()
    # the model can be simplified if we assume we alaways use all the capacity
    # so we would always use all the beds, or finish the queue
    length_queue = sum(s['u'][i][j] for i in range(I) for j in range(len(('urgente', 'no-urgente'))))
    total = min(E - sum(s['w']), length_queue)

    nagns = I * 2
    # flat_state = [s['u'][i][j] for i in range(I) for j in ('urgente', 'no-urgente')]
    gen = rec([i for i in range(nagns)], total)
    for options in gen:
        # if sum(options) == total: # we assume we assign all available
        acc = []
        for i in range(I):
            urgs = min(options[i], s['u'][i][0])
            nourgs = min(options[i+I], s['u'][i][1])
            acc.append((urgs,nourgs))
        accs.add(tuple(acc))
        
    return accs
    
def Pri(x):
    # Completar con la probabilidad real
    return poisson.pmf(x, 1/2.58, 0)


def P_1(u):
    # completar acá con algo más real
    if u == 1: return 0.5
    if u == 2: return 0.5
    return 0


def P_2(s1,i): 
    if sum([s1['w'][i] for i in range(I)]) < E:
        return Pri(s1['w'][i])
    return 0
        # Wait tengo uan duda, wsp
        # for i in range(0, I):

def P(s1, s, x):
    p = 1
    # probabilidad cola
    for i in range(0,I):
        for j in range(len(('urgente', 'no-urgente'))):
            # voy a trabajar acá yo
            p *= P_1(s1['u'][i][j] + x[i][j] - s1['u'][i][j])
    # probabilidad ocupados
    for i in range(0,I):
        p *= P_2(s1, i)
    
    return p
    # return poisson.pmf(x, 1/2.58/20, 0)


def value_iteration(epsilon, lambd):
    number_states = I * 2 * I
    V = [0] * number_states
    new_V = [0] * number_states
    iterations = 0

    V_array = []
    while iterations == 0 or calculate_diff(V, new_V) >= (epsilon*(1-lambd) / (2*lambd)):
        d = [0 for i in range()]
        V = new_V
        new_V = [0] * len(S)

        V_array.append(V)
        for s in S:
            vtgs = [r[s] + lambd * sum([P(x, i, j) * V[j]
                                        for j in S]) for x in x(s)]

            max_vtg = max(vtgs)
            argmax_vtg = vtgs.index(max_vtg)
            d[s] = X[s][argmax_vtg]

            new_V[s] = max_vtg

        iterations += 1

    return [max([r[s] + sum([P(x, i, j) * new_V[j] for j in S]) for x in X[s]]) for s in S], d, iterations, V_array


s = {
    'u': [{'urgente': 3, 'no-urgente': 8} for i in range(I)],
    'w': [1 for i in range(I)]
}

print(*sorted(x(s)), sep='\n')
