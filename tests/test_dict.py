import urine


def test_dict():
    values = [{}, {1: 4, 'loong': 33.3}]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, dict)


def test_nested_dicts():
    values = [{3: 'rrtt', 33.3: {3: {}}}, {3: {}}]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, dict)
