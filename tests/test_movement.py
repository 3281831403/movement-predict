import pytest

from gameplay import movement as mod

CASES = [
    ('integrate', [[0, 0, 0], [1, 0, 0], [0, 0, 0], 1], [[1.0, 0.0, 0.0], [1, 0, 0]], False),
    ('integrate', [[0, 0, 0], [0, 0, 0], [0, -9.8, 0], 1], [[0.0, -4.9, 0.0], [0, -9.8, 0]], False),
    ('dead_reckon', [[0, 0, 0], [1, 0, 0], 2], [2, 0, 0], False),
    ('reconcile', [[0, 0, 0], [10, 0, 0], 0.5], [5.0, 0.0, 0.0], True),
    ('slide', [[1, -1, 0], [0, 1, 0]], [1, 0, 0], False),
    ('jump_height', [10, 10], 5.0, True),
    ('jump_height', [10, 0], 0.0, True),
    ('integrate', [[0, 0, 0], [0, 0, 0], [0, 0, 0], 0], [[0.0, 0.0, 0.0], [0, 0, 0]], False),
    ('integrate', [[1, 2, 3], [0, 0, 0], [0, 0, 0], 0], [[1.0, 2.0, 3.0], [0, 0, 0]], False),
    ('dead_reckon', [[1, 2, 3], [0, 0, 0], 0], [1, 2, 3], False),
    ('reconcile', [[1, 2, 3], [4, 5, 6], 0], [1, 2, 3], False),
    ('reconcile', [[1, 2, 3], [4, 5, 6], 1], [4, 5, 6], False),
    ('slide', [[0, 0, 0], [0, 1, 0]], [0, 0, 0], False),
    ('jump_height', [0, 10], 0.0, True),
    ('integrate', [[0, 0, 0], [1, 1, 1], [0, 0, 0], 2], [[2.0, 2.0, 2.0], [1, 1, 1]], False),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_movement_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
