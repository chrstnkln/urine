import struct
import zlib

from urine import __protocol_version__
from urine.extensions import UrineExtension
from urine.types import data_types


class UrineDecoder(object):
    _id_type_dict = {i: x for i, x in enumerate(data_types)}

    def __init__(self):
        self.data = None
        self.off = 0

        self._type_function_dict = {x: getattr(self, 'decode_' + x) for x in data_types}
        self._hash_extension_dict = {}

    def extend(self, extension):
        """Adds an extension to the decoder.

        Args:
            extension (UrineExtension): Extension inheriting and implementing UrineExtension

        Raises:
            ValueError: Two different extensions generate the same CRC32 hash (very unlikely)
        """
        if issubclass(extension, UrineExtension):
            if extension in self._hash_extension_dict.values():
                return

            crc32 = zlib.crc32(extension.__name__.encode('utf-8'))

            if crc32 in self._hash_extension_dict:
                raise ValueError(
                    'Extension hash duplicate detected, change extension name {}'.format(crc32)
                )

            self._hash_extension_dict[crc32] = extension

    def decode(self, data):
        """Decodes an object that was encoded with urine.

        Args:
            data (bytes, bytearray): Data to be decoded

        Raises:
            NotImplementedError: Unimplemented protocol version

        Returns:
            object: Decoded object
        """
        self.data = data
        self.off = 0

        protocol_version = self._read_protocol_version()
        if protocol_version != __protocol_version__:
            raise ValueError('Invalid protocol version: {} (not supported)'.format(protocol_version))

        return self._decode()

    def decode_extension(self):
        crc32 = self.decode_uint32()
        data_size = self.decode_uint32()

        data = self.data[self.off:self.off + data_size]
        self.off += data_size

        extension = self._hash_extension_dict[crc32]

        return extension.decode(data)

    def decode_bool(self):
        val = struct.unpack_from('?', self.data, self.off)[0]
        self.off += 1
        return val

    def decode_int8(self):
        val = struct.unpack_from('b', self.data, self.off)[0]
        self.off += 1
        return val

    def decode_int16(self):
        val = struct.unpack_from('<h', self.data, self.off)[0]
        self.off += 2
        return val

    def decode_int32(self):
        val = struct.unpack_from('<i', self.data, self.off)[0]
        self.off += 4
        return val

    def decode_int64(self):
        val = struct.unpack_from('<q', self.data, self.off)[0]
        self.off += 8
        return val

    def decode_uint8(self):
        val = struct.unpack_from('B', self.data, self.off)[0]
        self.off += 1
        return val

    def decode_uint16(self):
        val = struct.unpack_from('<H', self.data, self.off)[0]
        self.off += 2
        return val

    def decode_uint32(self):
        val = struct.unpack_from('<I', self.data, self.off)[0]
        self.off += 4
        return val

    def decode_uint64(self):
        val = struct.unpack_from('<Q', self.data, self.off)[0]
        self.off += 8
        return val

    def decode_bignum(self):
        signed = self.decode_bool()
        parts_len = self.decode_uint32()
        parts = [self.decode_uint64() for _ in range(parts_len)]

        final_hex = '0x'
        for part in parts:
            final_hex += hex(part)[2:]

        val = int(final_hex, 16)
        return -val if signed else val

    def decode_float(self):
        val = struct.unpack_from('<d', self.data, self.off)[0]
        self.off += 8
        return val

    def decode_complex(self):
        real, imag = struct.unpack_from('<dd', self.data, self.off)
        self.off += 16
        return complex(real, imag)

    def decode_bytes(self):
        data_size = self.decode_uint32()
        data = self.data[self.off:self.off + data_size]
        self.off += data_size

        return bytes(data)

    def decode_bytearray(self):
        data_size = self.decode_uint32()
        data = self.data[self.off:self.off + data_size]
        self.off += data_size

        return data

    def decode_string(self):
        str_size = self.decode_uint32()
        string = self.data[self.off:self.off + str_size].decode('utf-8')
        self.off += str_size

        return string

    def decode_list(self):
        lst_len = self.decode_uint32()
        return [self._decode() for _ in range(lst_len)]

    def decode_tuple(self):
        tpl_len = self.decode_uint32()
        return tuple(self._decode() for _ in range(tpl_len))

    def decode_set(self):
        st_len = self.decode_uint32()
        return set([self._decode() for _ in range(st_len)])

    def decode_frozenset(self):
        st_len = self.decode_uint32()
        return frozenset((self._decode() for _ in range(st_len)))

    def decode_dict(self):
        dct_len = self.decode_uint32()
        dct = {}

        for _ in range(dct_len):
            key = self._decode()
            val = self._decode()
            dct[key] = val

        return dct

    def decode_range(self):
        start = self._decode()
        stop = self._decode()
        step = self._decode()

        return range(start, stop, step)

    def decode_class(self):
        name = self.decode_string()
        attrs_len = self.decode_uint32()
        attrs_dct = {}

        for _ in range(attrs_len):
            key = self.decode_string()
            val = self._decode()
            attrs_dct[key] = val

        return type(name, (object,), attrs_dct)()

    def decode_none(self):
        return None

    def _decode(self):
        type_str = self._read_type()
        return self._type_function_dict[type_str]()

    def _read_protocol_version(self):
        major = self.decode_uint8()
        minor = self.decode_uint8()

        return '.'.join((str(major), str(minor)))

    def _read_type(self):
        type_id = self.decode_uint8()
        return self._id_type_dict[type_id]
