import urine


def test_set():
    values = [set(), {3, 6, 'uiiii'}]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, set)


def test_set_with_nested_frozensets():
    values = [{frozenset((frozenset(),))}, {3, 'fuck', frozenset((3, 5))}]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, set)


def test_frozenset():
    values = [frozenset(), frozenset((1, '4', 6.44))]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, frozenset)


def test_nested_frozensets():
    values = [frozenset((frozenset(),)), frozenset((frozenset(), 3, 5, frozenset((3, 5.33))))]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, frozenset)
