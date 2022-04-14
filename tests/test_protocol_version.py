import pytest

import urine


def test_invalid_protocol_version():
    data = b'\x00\xfe\xae\x3c'
    pytest.raises(ValueError, lambda: urine.decode(data))
