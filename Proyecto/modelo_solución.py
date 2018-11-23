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


def h(i, x): 
    return x


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


ARRIVAL_RATE_PER_DAY = [5, 1]
DEPARTURE_RATE_PER_DAY = [3, 1]

def x(s):
    # returns ((urgent, no-urgent), ...)
    accs = set()
    total = E - sum(s[1])

    nagns = I
    gen = rec([i for i in range(nagns)], total)
    for options in gen:
        acc = tuple(min(options[i], s[0][i]) for i in range(I))
        accs.add(acc)
    return accs


def P_1(llegan, i):
    return dic2.get((llegan, i), 0)

### hashing probabilities
### calculation is very expensive
exponential = [expon.cdf(1, scale=1/(DEPARTURE_RATE_PER_DAY[i])) for i in range(I)]


dic2 = {}
for i in range(I):
    for j in range(E * 2):
        dic2[(j, i)] = poisson.pmf(j, ARRIVAL_RATE_PER_DAY[i])

dic = {}
for i in range(I):
    for a in range(E):
        for w1 in range(a+1):
            p = exponential[i]
            dic[(a - w1, i)] = binom.pmf(a - w1, a, p)


def P_2(w1, a, i):
    return dic.get((a - w1, i), 0)



def P(s1, s, x):
    def a(i):
        return s[1][i] + x[i]
    p = 1
    # probabilidad cola	
    for i in range(I):
        u, u1 = s[0], s1[0]
        p *= P_1(u[i] - x[i] - u1[i], i)
    # probabilidad ocupados
    w1 = s1[1]
    for i in range(I):
        p *= P_2(w1[i], a(i), i)
    return p


def c(s,x):
    c = 0
    for i in range(I):
        c += h(i, s[0][i] - x[i])
    return c


def limit(epsilon, lambd):
    return epsilon * (1 - lambd) / (2 * lambd)


def value_iteration(epsilon, lambd):
    def Esp(s, x):
        ps = np.empty(states_size)
        for i in range(states_size):
            ps[i] = P(S[i], s, x)
        return np.dot(Vn, ps)
    Vn = np.full((states_size, ), 100)
    Vn1 = np.empty((states_size, ))
    lim = limit(epsilon, lambd)
    iteraciones = 0
    while True:
        for i in range(states_size):
            s = S[i]
            best = min((c(s, x) + lambd * Esp(s, x), x) for x in x(s))
            Vn1[i] = best[0]
        iteraciones += 1
        diff = calculate_diff(Vn, Vn1)
        print('Diff:', diff)
        if diff < lim:
            break
        Vn = np.empty_like(Vn1)
        np.copyto(Vn, Vn1)

    Vn = Vn1
    print('iteraciones', iteraciones)
    return [min((c(s, x) + lambd * Esp(s, x), x) for x in x(s)) for s in S]


s = [
    tuple([10 for i in range(I)]),
    tuple([0 for i in range(I)])
]

print('beds:', E)
print('patient types:', I)
print('number of actions:', len(x(s)))

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
    s = S[i]
    if occupied(s) < E - 1 and all_type_waiting(s):
        cont += 1
        print_results(d[i], S[i])
        if cont == 10: break



