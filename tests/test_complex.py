import urine


def test_complex():
    values = [complex(23, 5), complex(0, 0), complex(0.3563, -33), complex(-24.4466, -22)]
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, complex)
