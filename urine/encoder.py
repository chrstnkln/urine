import struct
import zlib

from urine import __protocol_version__
from urine.extensions import UrineExtension
from urine.types import data_types

_exclude_identifier = '_urine_exclude'
_include_identifier = '_urine_include'


def include(*args):
    """Class decorator specifying the class attributes to be encoded
    """
    def include(cls):
        setattr(cls, _include_identifier, args)
        return cls
    return include


def exclude(*args):
    """Class decorator specifying the class attributes to be excluded from encoding
    """
    def exclude(cls):
        setattr(cls, _exclude_identifier, args)
        return cls
    return exclude


class UrineEncoder(object):
    _type_id_dict = {x: i for i, x in enumerate(data_types)}

    def __init__(self):
        self.buffer = bytearray()

        self._extension_hash_dict = {}
        self._type_extension_dict = {}

    def extend(self, obj_type, extension):
        """Adds an extension to the encoder.

        Args:
            obj_type (type): Object type the extension will apply to
            extension (UrineExtension): Extension that inherits and implements UrineExtension

        Raises:
            ValueError: Two different extensions generate the same CRC32 hash (very unlikely)
        """
        if issubclass(extension, UrineExtension):
            if (extension in self._extension_hash_dict) or (obj_type in self._type_extension_dict):
                return

            crc32 = zlib.crc32(extension.__name__.encode('utf-8'))

            if crc32 in self._extension_hash_dict.values():
                raise ValueError('Extension hash duplicate detected, change extension name: {}'.format(
                    extension.__name__
                ))

            self._extension_hash_dict[extension] = crc32
            self._type_extension_dict[obj_type] = extension

    def encode(self, obj):
        """Encodes a python object.

        Args:
            obj (object): Object to be encoded

        Returns:
            bytearray: Encoded object
        """
        self._write_protocol_version()
        self._encode(obj)

        temp = self.buffer
        self.buffer = bytearray()

        return temp

    def encode_extension(self, obj, extension, add_type=True):
        if add_type:
            self._write_type('extension')

        encoded = extension.encode(obj)

        self.encode_uint32(self._extension_hash_dict[extension], add_type=False)
        self.encode_uint32(len(encoded), add_type=False)
        self.buffer += encoded

    def encode_bool(self, val, add_type=True):
        if add_type:
            self._write_type('bool')

        self.buffer += struct.pack('?', val)

    def encode_int(self, val, add_type=True):
        if val >= 0:
            if val <= 0xff:
                self.encode_uint8(val, add_type=add_type)
            elif val <= 0xffff:
                self.encode_uint16(val, add_type=add_type)
            elif val <= 0xffffffff:
                self.encode_uint32(val, add_type=add_type)
            elif val <= 0xffffffffffffffff:
                self.encode_uint64(val, add_type=add_type)
            else:
                self.encode_bignum(val, add_type=add_type)
        else:
            abs_val = abs(val)

            if abs_val <= 0x80:
                self.encode_int8(val, add_type=add_type)
            elif abs_val <= 0x8000:
                self.encode_int16(val, add_type=add_type)
            elif abs_val <= 0x80000000:
                self.encode_int32(val, add_type=add_type)
            elif abs_val <= 0x8000000000000000:
                self.encode_int64(val, add_type=add_type)
            else:
                self.encode_bignum(val, add_type=add_type)

    def encode_int8(self, val, add_type=True):
        if add_type:
            self._write_type('int8')

        self.buffer += struct.pack('b', val)

    def encode_int16(self, val, add_type=True):
        if add_type:
            self._write_type('int16')

        self.buffer += struct.pack('<h', val)

    def encode_int32(self, val, add_type=True):
        if add_type:
            self._write_type('int32')

        self.buffer += struct.pack('<i', val)

    def encode_int64(self, val, add_type=True):
        if add_type:
            self._write_type('int64')

        self.buffer += struct.pack('<q', val)

    def encode_uint8(self, val, add_type=True):
        if add_type:
            self._write_type('uint8')

        self.buffer += struct.pack('B', val)

    def encode_uint16(self, val, add_type=True):
        if add_type:
            self._write_type('uint16')

        self.buffer += struct.pack('<H', val)

    def encode_uint32(self, val, add_type=True):
        if add_type:
            self._write_type('uint32')

        self.buffer += struct.pack('<I', val)

    def encode_uint64(self, val, add_type=True):
        if add_type:
            self._write_type('uint64')

        self.buffer += struct.pack('<Q', val)

    def encode_bignum(self, val, add_type=True):
        if add_type:
            self._write_type('bignum')

        self.encode_bool(val < 0, add_type=False)

        val = hex(abs(val))[2:]
        parts = [val[i:i + 16] for i in range(0, len(val), 16)]

        self.encode_uint32(len(parts), add_type=False)

        for part in parts:
            self.encode_uint64(int(part, 16), add_type=False)

    def encode_float(self, val, add_type=True):
        if add_type:
            self._write_type('float')

        self.buffer += struct.pack('<d', val)

    def encode_complex(self, val, add_type=True):
        if add_type:
            self._write_type('complex')

        self.buffer += struct.pack('<dd', val.real, val.imag)

    def encode_bytes(self, data, add_type=True):
        if add_type:
            self._write_type('bytes')

        self.encode_uint32(len(data), add_type=False)
        self.buffer += data

    def encode_bytearray(self, data, add_type=True):
        if add_type:
            self._write_type('bytearray')

        self.encode_uint32(len(data), add_type=False)
        self.buffer += data

    def encode_string(self, string, add_type=True):
        byte_str = string.encode('utf-8')
        if add_type:
            self._write_type('string')

        self.encode_uint32(len(byte_str), add_type=False)
        self.buffer += byte_str

    def encode_list(self, lst, add_type=True):
        if add_type:
            self._write_type('list')

        self.encode_uint32(len(lst), add_type=False)

        for obj in lst:
            self._encode(obj)

    def encode_tuple(self, tpl, add_type=True):
        if add_type:
            self._write_type('tuple')

        self.encode_uint32(len(tpl), add_type=False)

        for obj in tpl:
            self._encode(obj)

    def encode_set(self, st, add_type=True):
        if add_type:
            self._write_type('set')

        self.encode_uint32(len(st), add_type=False)

        for obj in st:
            self._encode(obj)

    def encode_frozenset(self, st, add_type=True):
        if add_type:
            self._write_type('frozenset')

        self.encode_uint32(len(st), add_type=False)

        for obj in st:
            self._encode(obj)

    def encode_dict(self, dct, add_type=True):
        if add_type:
            self._write_type('dict')

        self.encode_uint32(len(dct), add_type=False)

        for key, val in dct.items():
            self._encode(key)
            self._encode(val)

    def encode_range(self, rng, add_type=True):
        if add_type:
            self._write_type('range')

        self.encode_int(rng.start)
        self.encode_int(rng.stop)
        self.encode_int(rng.step)

    def encode_class(self, obj, add_type=True):
        inclusions = () if not hasattr(obj, _include_identifier) else getattr(obj, _include_identifier)
        exclusions = () if not hasattr(obj, _exclude_identifier) else getattr(obj, _exclude_identifier)

        if inclusions:
            attrs = {x: getattr(obj, x) for x in inclusions}
        else:
            attrs = {
                x: getattr(obj, x)
                for x in dir(obj)
                if all((
                    not callable(getattr(obj, x)),
                    not (x.startswith('__') and x.endswith('__')),
                    x not in exclusions,
                    x != _exclude_identifier
                ))
            }

        if add_type:
            self._write_type('class')

        self.encode_string(type(obj).__name__, add_type=False)
        self.encode_uint32(len(attrs), add_type=False)

        for attr_name, val in attrs.items():
            self.encode_string(attr_name, add_type=False)
            self._encode(val)

    def encode_none(self):
        self._write_type('none')

    def _encode(self, obj):
        obj_type = type(obj)

        if obj_type in self._type_extension_dict:
            self.encode_extension(obj, self._type_extension_dict[obj_type])

        elif obj_type is bool:
            self.encode_bool(obj)
        elif obj_type is int:
            self.encode_int(obj)
        elif obj_type is float:
            self.encode_float(obj)
        elif obj_type is complex:
            self.encode_complex(obj)
        elif obj_type is bytes:
            self.encode_bytes(obj)
        elif obj_type is bytearray:
            self.encode_bytearray(obj)
        elif obj_type is str:
            self.encode_string(obj)
        elif obj_type is list:
            self.encode_list(obj)
        elif obj_type is tuple:
            self.encode_tuple(obj)
        elif obj_type is set:
            self.encode_set(obj)
        elif obj_type is frozenset:
            self.encode_frozenset(obj)
        elif obj_type is dict:
            self.encode_dict(obj)
        elif obj_type is range:
            self.encode_range(obj)
        elif isinstance(obj, object):
            if obj is None:
                self.encode_none()
            else:
                self.encode_class(obj)

    def _write_protocol_version(self):
        major, minor = __protocol_version__.split('.')

        self.encode_uint8(int(major), add_type=False)
        self.encode_uint8(int(minor), add_type=False)

    def _write_type(self, type_str):
        type_id = self._type_id_dict[type_str]
        self.encode_uint8(type_id, add_type=False)
