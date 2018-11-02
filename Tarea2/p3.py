# import matplotlib.pyplot as plt

#%%

epsilon = 0.01

S = [0, 1, 2]

def X(s):
    dic = {
        0 : ('azul', 'negro'),
        1 : ('verde', 'rojo'),
        2: ('gris',)
    }
    return dic[s]

def r(s, a):
    # {(s:a): v}
    dic = {
        (0, 'azul'): -3.5,
        (0, 'negro'): -1.7,
        (1, 'rojo'): -2.6,
        (1, 'verde'): -2.6,
        (2, 'gris'): 1
    }
    return dic[(s,a)]


def p(s1, s, a):
    dic = {
        (0, 0, 'azul'): 0.5,
        (1, 0, 'azul'): 0.5,
        (0, 0, 'negro'): 0.1,
        (2, 0, 'negro'): 0.9,
        (0, 1, 'rojo'): 0.2,
        (1, 1, 'rojo'): 0.8,
        (1, 1, 'verde'): 0.6,
        (2, 1, 'verde'): 0.4,
        (2, 2, 'gris'): 1 
    }
    return dic.get((s1, s, a), 0)


def limit():
    return epsilon * (1 - factor) / (2 * factor)


def module(v1, v2):
    return sum([(v1[i] - v2[i]) ** 2 for i in range(len(v1))]) ** (1/2)


def value_iteration(factor):
    def E(s, a):
        return sum([p(s1, s, a) * Vn[s1] for s1 in S])
    n = 0
    Vs = []
    Vn = [0, 0, 0]
    Vn1 = [0, 0, 0]
    d = [None, None, None]
    while True:
        for s in S:
            best =  max([(r(s, a) + factor * E(s, a), a) for a in X(s)])
            Vn1[s] = best[0]
            d[s] = best[1]
        # print(Vn1)
        if n % 10 == 0:
            # print(f'{Vn1} - {module(Vn, Vn1)}')
            pass
        Vs.append(Vn)
        if module(Vn, Vn1) < limit():
            print(d)
            break
        Vn = Vn1.copy()
        n += 1
    Vs.append(Vn1)
    return Vs


def policy_iteration(factor):
    def E(s, a):
        return sum([p(s1, s, a) * Vn[s1] for s1 in S])
    n = 0
    # Vs = []
    ds = []
    dn = ['azul', 'verde', 'gris']
    Vn = [r(i, dn[i]) for i in range(3)]
    Vn1 = [None, None, None]
    dn1 = [None, None, None]
    while True:
        for s in S:
            best = max([(r(s, a) + factor * E(s, a), a) for a in X(s)])
            Vn1[s] = best[0]
            dn1[s] = best[1]
        # Vs.append(Vn)
        ds.append(dn)
        print(dn)
        if dn1 == dn:
            # print(dn)
            break
        dn = dn1.copy()
        Vn = Vn1.copy()
        n += 1
    return ds




#%%
import matplotlib.pyplot as plt

factor = 0.9

Vs2 = value_iteration(factor)
s0, s1, s2 = zip(*Vs2)
fig, ax = plt.subplots()
ax.plot(s0, 'C1', label='Estado 0')
ax.plot(s1, 'C2', label='Estado 1')
ax.plot(s2, 'C3', label='Estado 2')

plt.ylabel('Value to go')
plt.xlabel('Etapas')

legend = ax.legend(loc='lower right', shadow=False, fontsize=10)
# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('w')

# plt.show()
plt.savefig(f'graph.p3.2.a.{factor}.png', dpi=150, format='png', bbox_inches='tight', )

#%%
factor = 0.9
ds = policy_iteration(factor)
print(ds)

