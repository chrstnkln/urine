import urine


def test_float():
    values = [0.4564, 0.0, -33.1164, -0.0001, 345346.3344874457457547]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, float)
