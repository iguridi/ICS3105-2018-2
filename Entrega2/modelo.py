# coding: utf-8
from prettytable import PrettyTable
from scipy.stats import poisson
from math import factorial, exp, inf
import numpy as np


def calculate_diff(old, new):
    a = old - new
    return np.sqrt(a.dot(a))


I = 2  # tipos de cirugías
E = 3  # cantidad de camas


def k(x): return 3 * x  # costo por posponer agendamiento urgente


def h(x): return 1 * x


# r = {'lambda' + str(i): 2 for i in range(I)}  # duración de la operación

q = {
    'urgente': {i: 2 for i in range(I)},
    'no-urgente': {i: 2 for i in range(I)}
}  # llegada de pacientes

s_example = (
    tuple([0 for i in range(I)]),  # queue urgents
    tuple([0 for i in range(I)]),  # queue not urgents
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
    max_length_urgent = E
    max_length_no_urgent = E * 2
    urgs_gen = rec([0 for i in range(I)], max_length_urgent)
    for urgs in urgs_gen:
        no_urgs_gen = rec([0 for i in range(I)], max_length_no_urgent)
        for no_urgs in no_urgs_gen:
            occupied_gen = rec([0 for i in range(I)], E)
            for w in occupied_gen:
                states.add((urgs, no_urgs, w))
    return list(states)


def x(s):
    # returns ((urgent, no-urgent), ...)
    accs = set()
    # the model can be simplified if we assume we alaways use all the capacity
    # so we would always use all the beds, or finish the queue
    # length_queue = sum(s[j][i] for i in range(I)
    #                    for j in range(len(('urgente', 'no-urgente'))))
    total = min(E - sum(s[2]), sum(s[0]) + sum(s[1]))
    # total = E - sum(s[2])

    nagns = I * 2
    gen = rec([i for i in range(nagns)], total)
    for options in gen:
        acc = []
        for i in range(I):
            urgs = min(options[i], s[0][i])
            nourgs = min(options[i+I], s[1][i])
            acc.append((urgs, nourgs))
        accs.add(tuple(acc))
    return accs


def Pri(g, a):
    lamb_i = 2.58
    comb = factorial(a) / factorial(g) / factorial(a-g)
    return comb * (1-exp(-lamb_i))**g * (exp(-lamb_i))**(a-g)


def P_1(llegan):
    # completar acá con algo más real
    if llegan == 1:
        return 0.5
    if llegan == 2:
        return 0.5
    return 0


def P_2(w1, a):
    # completar acá con algo más real
    if w1 == 1:
        return 0.5
    if w1 == 2:
        return 0.5
    return 0


def a(i, w, x):
    return w[i] + sum(x[i][j] for j in range(len('urgente', 'no-urgente')))

# def P_2(s1, i, x):
#     g = s1[1][i]
#     a = sum([x[i][j] for j in range(len(('urgente', 'no-urgente')))])
#     return Pri(r, a)


def P(s1, s, x):
    def a(i):
        w_i, x_i = s[2][i], x[i]
        return w_i + sum(x_i[j] for j in range(len(('urgente', 'no-urgente'))))
    p = 1
    # probabilidad cola
    for i in range(I):
        for j in range(len(('urgente', 'no-urgente'))):
            p *= P_1(s[j][i] - x[i][j] - s1[j][i])
    # probabilidad ocupados
    # w1 = s1[2]
    # for i in range(I):
    #     p *= P_2(w1[i], a(i))
    # if p != 0:
    #     print(p)
    return p
    # return poisson.pmf(x, 1/2.58/20, 0)


def c(lengths,x):
    if lengths[0] - sum(list(zip(*x))[0]) < 0:
        # print(s[0])
        # print(list(zip(*x))[0], 'blabla')
        raise Exception
    # cost = 0
    x_trasp = list(zip(*x))
    # cost += k(lengths[0] - sum(x_trasp[0])) 
    # cost += h(lengths[1] - sum(x_trasp[1]))
    return k(lengths[0] - sum(x_trasp[0])) + h(lengths[1] - sum(x_trasp[1]))


def limit(epsilon, lambd):
    return epsilon * (1 - lambd) / (2 * lambd)


def get_lengths(s):
    length_queue_urgents = sum(s[0])
    length_queue_not_urgents = sum(s[1])
    return length_queue_urgents, length_queue_not_urgents


def value_iteration(epsilon, lambd):
    def Esp(s, x):
        return sum(P(S[i], s, x) * Vn[i] for i in range(len(S)))
    Vn = np.full((len(S), ), 100)
    Vn1 = np.zeros((len(S), ))
    lim = limit(epsilon, lambd)
    while True:
        for i in range(len(S)):
            # print('whaat')
            s = S[i]
            lengths = get_lengths(s)
            best = min((c(lengths,x) + lambd * Esp(s, x), x) for x in x(s))
            Vn1[i] = best[0]
        diff = calculate_diff(Vn, Vn1)
        print('Diff:', diff)
        if diff < lim:
            break
        Vn = np.empty_like(Vn1)
        np.copyto(Vn, Vn1)

    Vn = Vn1
    return [min((c(get_lengths(s), x) + lambd * Esp(s, x), x) for x in x(s)) for s in S]


s = [
    tuple([10 for i in range(I)]),
    tuple([10 for i in range(I)]),
    tuple([0 for i in range(I)])
]

# print(*sorted(x(s)), sep='\n')
# S()
print('beds:', E)
print('patient types:', I)
print('number of actions:', len(x(s)))
# print(limit(0.3,0.9))

S = state_generator()
print('number of states:', len(state_generator()))

epsilon = 0.99
lambd = 0.9
results = value_iteration(epsilon, lambd)


def print_results(d, s):
    t = PrettyTable(['Type', '', 'Queue', 'Assigned', 'Previously occupied', 'Capacity'])
    # r = '                              queue             assigned\n'
    for i in range(I):
        t.add_row(
            [f'{i}', 'Urgent', f'{s[0][i]}', f'{d[i][0]}', '', ''])
        t.add_row(
            [f'{i}', 'Not urgent', f'{s[1][i]}', f'{d[i][1]}', '', ''])
    t.add_row(
    ['', f'Total Use', '', f'{sum(sum(d[j]) for j in range(I))}', f'{sum(s[2])}', E])
    print(t)
    return t

for i in range(5):
    print_results(results[i][1], S[i])

# print(*sorted(state_generator()), sep='\n')



