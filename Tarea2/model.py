epsilon = 0.01

S = [0, 1, 2]


def X(s):
    dic = {
        0: ('azul', 'negro'),
        1: ('verde', 'rojo'),
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
    return dic[(s, a)]


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
