import urine


def test_none():
    assert urine.decode(urine.encode(None)) is None
