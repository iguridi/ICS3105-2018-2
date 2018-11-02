from pytest import fixture, mark
import p3


@fixture(name='new_game')
def _new_constants():
    pass
    # return Game('Punto', 'Rakhi')


# @mark.parametrize(
#     'one, two, expected', [
#         ([], [], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
#         ([1, 3, 5, 7, 9], [2, 4, 6, 8], []),
#         ([1, 2], [3, 4], [5, 6, 7, 8, 9]),
#         ([3, 2, 1], [9, 8, 7], [4, 5, 6]),
#     ]
# )
# def test_available(new_game, one, two, expected):
#     new_game.p1.numbers.extend(one)
#     new_game.p2.numbers.extend(two)
#     assert new_game.available == expected


# def test_winner():
#     pass


# def test_fifteen():
#     pass

@mark.parametrize(
    'v1, v2, expected', [
        ([1,1,1], [1,1,1], 0),
        ([8, -5, -2], [4, -3, 2], 6),
    ]
)
def test_module(v1, v2, expected):
    assert p3.module(v1, v2) == expected


@mark.parametrize(
    'epsilon, factor, expected', [
        (0.4, 0.8, 0.05),
    ]
)
def test_limit(epsilon, factor, expected):
    p3.epsilon = epsilon
    p3.factor = factor
    assert p3.limit() > expected - 0.0000001
    assert p3.limit() < expected + 0.0000001
