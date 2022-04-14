import urine


def test_string():
    values = ['', 'Just A Fucking Test String', '異體字字典‚∂ƒ∆€€©¶[ø']
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, str)
