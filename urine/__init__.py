__protocol_version__ = '1.0'


from urine.decoder import UrineDecoder
from urine.encoder import UrineEncoder, exclude, include
from urine.extensions import UrineExtension

_encoder = UrineEncoder()
_decoder = UrineDecoder()


def encode(obj):
    """Encodes a python object.

    Args:
        obj (object): Object to be encoded

    Returns:
        bytearray: Encoded object
    """
    return _encoder.encode(obj)


def decode(data):
    """Decodes an object that was encoded with urine.

    Args:
        data (bytes, bytearray): Data to be decoded

    Returns:
        object: Decoded object
    """
    return _decoder.decode(data)


def extend(obj_type, extension):
    """Adds an extension to the encoder and decoder

    Args:
        obj_type (type): Object type the extension will apply to
        extension (UrineExtension): Extension that inherits and implements UrineExtension
    """
    _encoder.extend(obj_type, extension)
    _decoder.extend(extension)
