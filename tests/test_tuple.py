import urine


def test_tuple():
    values = [tuple(), (3, 6, 1, 9)]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, tuple)


def test_nested_tuples():
    values = [tuple(tuple(tuple())), (2, 4, tuple((7, 3, (8,))))]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, tuple)
