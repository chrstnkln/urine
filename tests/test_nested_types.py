import urine


def test_nested_types():
    data = [
        [33.4, {4: b'eerrr', 10: set(), 20: frozenset(['ss', b'gg'])}, {44.6, 3, complex(3, 22.2)}],
        ({}, {3: True}), None,
        [0x457348976498fea73647ad37463eda24dafe3174ecad828defacd7392dace2845cc382742aec373aecd3925eadc],
        None,
        False
    ]

    enc = urine.encode(data)
    dec = urine.decode(enc)

    assert dec == data
