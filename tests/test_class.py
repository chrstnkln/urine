import urine


@urine.exclude('attr1', 'attr3')
class ExcludeTestClass(object):
    attr1 = 420
    attr2 = 1337
    attr3 = 'hi'
    attr4 = []


@urine.include('attr2', 'attr4')
class IncludeTestClass(object):
    attr1 = 420
    attr2 = 1337
    attr3 = 'hi'
    attr4 = []


def test_class(test_class_instance, test_class_dependency):
    enc = urine.encode(test_class_instance)
    dec = urine.decode(enc)

    assert type(dec).__name__ == type(test_class_instance).__name__

    for attr in dir(test_class_instance):
        if not callable(attr) and not (attr.startswith('__') and attr.endswith('__')):
            dec_attr = getattr(dec, attr)
            if attr == 'dependency':
                assert dec_attr.data == test_class_instance.dependency.data
            else:
                assert dec_attr == getattr(test_class_instance, attr)


def test_class_with_excluded_attributes():
    instance = ExcludeTestClass()
    enc = urine.encode(instance)
    dec = urine.decode(enc)

    assert not hasattr(dec, 'attr1') and not hasattr(dec, 'attr3')
    assert hasattr(dec, 'attr2') and hasattr(dec, 'attr4')


def test_class_with_included_attributes():
    instance = IncludeTestClass()
    enc = urine.encode(instance)
    dec = urine.decode(enc)

    assert not hasattr(dec, 'attr1') and not hasattr(dec, 'attr3')
    assert hasattr(dec, 'attr2') and hasattr(dec, 'attr4')
