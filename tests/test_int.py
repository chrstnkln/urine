import urine


def assert_equal(val):
    assert urine.decode(urine.encode(val)) == val


def assert_binary_size(val, n):
    assert len(urine.encode(val)) == 3 + n


def assert_int(val):
    assert isinstance(urine.decode(urine.encode(val)), int)


def test_int8_and_uint8():
    values = [35, -66, -0x80, 220, 0xFF, 0]
    for val in values:
        assert_equal(val)
        assert_binary_size(val, 1)
        assert_int(val)


def test_int16_and_uint16():
    values = [462, -844, -0x8000, 0xFFFF]
    for val in values:
        assert_equal(val)
        assert_binary_size(val, 2)
        assert_int(val)


def test_int32_and_uint32():
    values = [830007, -66220, -0x80000000, 0xFFFFFFFF]
    for val in values:
        assert_equal(val)
        assert_binary_size(val, 4)
        assert_int(val)


def test_int64_and_uint64():
    values = [600380402146, -396395892396, -0x8000000000000000, 0xFFFFFFFFFFFFFFFF]
    for val in values:
        assert_equal(val)
        assert_binary_size(val, 8)
        assert_int(val)


def test_bignum():
    values = [
        0xABCDEF0123456789ABCDEF0123456,
        -0x4876495867459DCDE45884AECD24A3583ACE398693EEAAA93CDE24595AE
    ]

    for val in values:
        assert_equal(val)
        assert_int(val)
