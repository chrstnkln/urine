import pytest

import urine


class TestClassDependency(object):
    data = [1, 3, 'test', 'check out porcupine tree (awesome band)']


class TestClass(object):
    string = 'blob'
    dictionary = {3: '3', 22: b'somebyteshereandthere', 1: {}}
    byte = b'\x00\xef'
    num1 = 33
    num2 = 314.235
    dependency = TestClassDependency()


@pytest.fixture(scope='module')
def test_class_instance():
    return TestClass()


@pytest.fixture(scope='module')
def test_class_dependency():
    return TestClassDependency


@pytest.fixture
def blank_encoder():
    return urine.UrineEncoder()


@pytest.fixture(scope='module')
def blank_decoder():
    return urine.UrineDecoder()
