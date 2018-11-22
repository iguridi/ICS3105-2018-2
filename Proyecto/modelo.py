# coding: utf-8
from prettytable import PrettyTable
from scipy.stats import poisson, binom, expon
from math import factorial, exp, inf
import numpy as np


def calculate_diff(old, new):
    a = old - new
    return np.sqrt(a.dot(a))


I = 2  # tipos de cirugías
E = 4  # cantidad de camas


# def k(i, x): return 3 * x + i  # costo por posponer agendamiento urgente


def h(i, x): 
    return x


s_example = (
    tuple([0 for i in range(I)]),  # queue
    tuple([0 for i in range(I)])  # occupied
)
# S['u'][2][3]['urgente']


def rec(assigns, total, i=0):
    if i >= len(assigns):
        yield tuple(assigns)
    else:
        for j in range(0, total+1):
            yield from rec(assigns[:i] + [j] + assigns[i+1:], total-j, i+1)


def state_generator():
    # returns ((u_u, u_nu, w)_i, ...) \forall i
    states = set()
    max_length_queue = E * 2
    urgs_gen = rec([0 for i in range(I)], max_length_queue)
    occupied_gen = list(rec([0 for i in range(I)], E))
    for urgs in urgs_gen:
        for w in occupied_gen:
            states.add((urgs, w))
    return list(states)


def x(s):
    # returns ((urgent, no-urgent), ...)
    accs = set()
    total = E - sum(s[1])

    nagns = I
    gen = rec([i for i in range(nagns)], total)
    for options in gen:
        # if sum(options) < total: 
            # we dont consider the ones that left beds empty
            # continue
        acc = tuple(min(options[i], s[0][i]) for i in range(I))
        accs.add(acc)
    return accs


def P_1(llegan):
    # completar acá con algo más real
    if llegan == 1:
        return 0.5
    if llegan == 2:
        return 0.5
    return 0

### hashing probabilities
### calculation is very expensive
exponential = [expon.cdf(1, scale=5*(i+1)) for i in range(I)]

dic = {}
for i in range(I):
    for a in range(E):
        for w1 in range(a+1):
            p = exponential[i]
            dic[(a - w1, i)] = binom.pmf(a - w1, a, p)

def P_2(w1, a, i):
    return dic.get((a - w1, i), 0)


    # p = exponential[i]
    # dic[(w1, a, i)] = dic.get((w1, a, i), 0) + 1
    # return binom.pmf(w1, a, p)
    

# def a(i, w, x):
#     return w[i] + sum(x[i][j] for j in range(len('urgente', 'no-urgente')))


# def P_2(s1, i, x):
#     g = s1[1][i]
#     a = sum([x[i][j] for j in range(len(('urgente', 'no-urgente')))])
#     return Pri(r, a)


def P(s1, s, x):
    def a(i):
        return s[1][i] + x[i]
    p = 1
    # probabilidad cola	
    for i in range(I):
        u, u1 = s[0], s1[0]
        p *= P_1(u[i] - x[i] - u1[i])
    # probabilidad ocupados
    w1 = s1[1]
    for i in range(I):
        p *= P_2(w1[i], a(i), i)
    # if p != 0:
    #     print(p)
    return p
    # return poisson.pmf(x, 1/2.58/20, 0)


def c(s,x):
    if sum(s[0]) - sum(x) < 0:
        print(s[0])
        print(x)
        # print(list(zip(*x))[0], 'blabla')
        raise Exception
    # cost = 0
    # cost += k(lengths[0] - sum(x_trasp[0])) 
    # cost += h(lengths[1] - sum(x_trasp[1]))
    c = 0
    for i in range(I):
        c += h(i, sum(s[0]) - sum(x))
    return c
    # return k(lengths[0] - sum(x_trasp[0])) + h(lengths[1] - sum(x_trasp[1]))


def limit(epsilon, lambd):
    return epsilon * (1 - lambd) / (2 * lambd)




def value_iteration(epsilon, lambd):
    def Esp(s, x):
        ps = np.empty(states_size)
        for i in range(states_size):
            # if S[i][1] 
            ps[i] = P(S[i], s, x)
        # ps = np.array([P(S[i], s, x) for i in range(states_size)])
        return np.dot(Vn, ps)
        # return sum(P(S[i], s, x) * Vn[i] for i in range(states_size))
    Vn = np.full((states_size, ), 100)
    Vn1 = np.empty((states_size, ))
    lim = limit(epsilon, lambd)
    while True:
        for i in range(states_size):
            # print('whaat')
            s = S[i]
            best = min((c(s, x) + lambd * Esp(s, x), x) for x in x(s))
            Vn1[i] = best[0]
        diff = calculate_diff(Vn, Vn1)
        print('Diff:', diff)
        if diff < lim:
            break
        Vn = np.empty_like(Vn1)
        np.copyto(Vn, Vn1)

    Vn = Vn1
    return [min((c(s, x) + lambd * Esp(s, x), x) for x in x(s)) for s in S]


s = [
    tuple([10 for i in range(I)]),
    tuple([0 for i in range(I)])
]

# for i in range(15):
#     print(P_2(0,7,i))
# print(*sorted(x(s)), sep='\n')
# S()
print('beds:', E)
print('patient types:', I)
print('number of actions:', len(x(s)))
# print(limit(0.3,0.9))

S = state_generator()
states_size = len(S)
print('number of states:', states_size)

epsilon = 0.99
lambd = 0.9
results = value_iteration(epsilon, lambd)

d = [i[1] for i in results]


def print_results(d, s):
    t = PrettyTable(['Type', '', 'Queue', 'Assigned', 'Previously occupied', 'Capacity'])
    for i in range(I):
        t.add_row(
            [f'{i}', '', f'{s[0][i]}', f'{d[i]}', f'{s[1][i]}', ''])
    t.add_row(
    ['', f'Total Use', '', f'{sum(d)}', f'{sum(s[1])}', E])
    print(t)
    return t

for s in range(10):
    print_results(results[s][1], S[s])


def occupied(s):
    return sum(s[1])


def queue(s):
    return sum(s[0])

def queue_type(i, s):
    return s[0][i]

def all_type_waiting(s):
    for i in range(I):
        if queue_type(i,s) == 0:
            return False
    return True

cont = 0
for i in range(states_size):
    # for i in range(I)
    s = S[i]
    if occupied(s) < E - 1 and all_type_waiting(s):
        cont += 1
        print_results(d[i], S[i])
        if cont == 10: break

    # if sum(d[i]) + sum(S[i][1]) != E and sum(S[i][0]) > :

# print(*sorted(state_generator()), sep='\n')



