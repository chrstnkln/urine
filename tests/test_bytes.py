import urine

values = [b'sdgvn4309', b'\x00', b'\xfe\x02\xc2\x24\xae']


def test_bytes():
    for val in values:
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, bytes)


def test_bytearray():
    for val in values:
        val = bytearray(val)
        enc = urine.encode(val)
        dec = urine.decode(enc)

        assert dec == val
        assert isinstance(dec, bytearray)
