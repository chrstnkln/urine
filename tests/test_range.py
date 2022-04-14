import urine


def test_range():
    values = [range(10), range(3, 5), range(20, 300, 2)]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, range)
