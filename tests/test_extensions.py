import datetime
import struct

import pytest

import urine


class DatetimeExtension(urine.UrineExtension):
    def encode(obj):
        return struct.pack('<HBBBBBI', *[
            obj.year,
            obj.month,
            obj.day,
            obj.hour,
            obj.minute,
            obj.second,
            obj.microsecond
        ])

    def decode(data):
        unpacked = struct.unpack('<HBBBBBI', data)
        return datetime.datetime(*unpacked)


class MissingEncodeExtension(urine.UrineExtension):
    pass


class MissingDecodeExtension(urine.UrineExtension):
    def encode(obj):
        return b"TEST DATA"


class u202104(urine.UrineExtension):
    pass


class F108909(urine.UrineExtension):
    pass


def test_extensions(blank_encoder, blank_decoder):
    blank_encoder.extend(datetime.datetime, DatetimeExtension)
    blank_decoder.extend(DatetimeExtension)

    dt = datetime.datetime.today()
    enc = blank_encoder.encode(dt)
    dec = blank_decoder.decode(enc)

    assert dec == dt
    assert isinstance(dec, datetime.datetime)


def test_global_extensions():
    urine.extend(datetime.datetime, DatetimeExtension)

    dt = datetime.datetime.today()
    enc = urine.encode(dt)
    dec = urine.decode(enc)

    assert dec == dt
    assert isinstance(dec, datetime.datetime)


def test_duplicate_extensions():
    urine.extend(datetime.datetime, DatetimeExtension)
    urine.extend(datetime.datetime, DatetimeExtension)


def test_extension_with_missing_encode_function(blank_encoder, blank_decoder):
    blank_encoder.extend(datetime.datetime, MissingEncodeExtension)
    blank_decoder.extend(MissingEncodeExtension)

    dt = datetime.datetime.today()

    pytest.raises(NotImplementedError, lambda: blank_encoder.encode(dt))


def test_extension_with_missing_decode_function(blank_encoder, blank_decoder):
    blank_encoder.extend(datetime.datetime, MissingDecodeExtension)
    blank_decoder.extend(MissingDecodeExtension)

    dt = datetime.datetime.today()
    enc = blank_encoder.encode(dt)

    pytest.raises(NotImplementedError, lambda: blank_decoder.decode(enc))


def test_extensions_with_same_crc_hash_value(blank_encoder, blank_decoder):
    blank_encoder.extend(int, u202104)
    blank_decoder.extend(u202104)

    pytest.raises(ValueError, lambda: blank_encoder.extend(float, F108909))
    pytest.raises(ValueError, lambda: blank_decoder.extend(F108909))
