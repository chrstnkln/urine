import urine


def test_list():
    values = [[], [1, 2, 3]]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, list)


def test_nested_lists():
    values = [[[[[]]]], [1, 2, [1, [2], 3, [4, 5, 6]]]]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, list)
