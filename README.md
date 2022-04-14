# urine
```urine``` encodes and decodes Python objects to and from binary data securely. It only encodes data and leaves out any functionality, which allows for safe deserialization from untrusted sources. Object types are detected automatically and attributes are encoded/decoded recursively, making ```urine``` very simple to use.
## Why use urine instead of pickle or JSON?
Unlike [```pickle```](https://docs.python.org/3/library/pickle.html), ```urine``` does not encode nor decode functions. For instance, ```pickle``` provides a ```__reduce__``` method that is intended for reconstructing objects. It gets called every time an object is unpickled (deserialized). An attacker could easily return malicious code that would be executed every time the object is unpickled. This is a big deal braker for network applications that want to exchange Python objects between untrusted peers.

[```json```](https://docs.python.org/3/library/json.html) on the other hand does not have mentioned security issue. However, JSON is not a binary serializer. It comes with a huge overhead when converted to binary. Furthermore, JSON does not support serialization of class instances or bytes-like objects by default.

The majority of other binary serializers for Python require you to define a custom serialization scheme, wich is often not worth the effort. I did not find a suitable serializer for my projects, so I decided to run my own.

## Installation
To install ```urine```, type:
```
pip install urine
```

To install ```urine``` with its development dependencies (e.g. to create pull requests), type:
```
pip install urine[dev]
```

## Quickstart guide
First of all, import ```urine``` to make use of its functionality.
```python
import urine
```
Create the object that you want to serialize. This can be any built-in python object or an instance of a class that you defined yourself. Check out the supported object types below for more information. Let's use a list for this example.
```python
obj = ['my data', 50, {3: 'more data'}]
```
Use ```urine.encode()``` to encode your object and turn it into a ```bytearray```.
```python
urine.encode(obj)
```
```
Output:

bytearray(b'\x01\x00\x10\x03\x00\x00\x00\x0f\x07\x00\x00\x00my data\x062\x14\x01\x00\x00\x00\x06\x03\r\t\x00\x00\x00more data')
```
Use ```urine.decode()``` to decode the binary data and turn it back into a Python object.
```python
urine.decode(encoded_obj)
```
```
Output:

['my data', 50, {3: 'more data'}]
```
### **Encoding user defined classes**
```urine``` allows you to encode instances of any class, including classes you defined yourself. Note that methods and functions are not serialized. Only attributes that are objects will be serialized.

Let's start by creating and instantiating a class with arbitrary data attributes.
```python
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

my_class = MyClass(25, [True, {3.3: 'test'}])
```
Use ```urine.encode()``` to encode the class intstance. Note that it does not matter if the instance is part of a list, dictionary or an attribute of another class. It will always be encoded and decoded accordingly.
```python
urine.encode(my_class)
```
```
Output:

bytearray(b'\x01\x00\x16\x07\x00\x00\x00MyClass\x02\x00\x00\x00\x01\x00\x00\x00a\x06\x19\x01\x00\x00\x00b\x10\x02\x00\x00\x00\x01\x01\x14\x01\x00\x00\x00\x0bffffff\n@\x0f\x04\x00\x00\x00test')
```
Use ```urine.decode()``` to decode the binary data back to a class instance.
```python
decoded_class = urine.decode(encoded_class)

print(decoded_class)
print(decoded_class.a)
print(decoded_class.b)
```
```
Output:

<urine.decoder.MyClass object at 0x10e96eb80>
25
[True, {3.3: 'test'}]
```
#### Excluding class attributes
```urine``` provides decorators that can be applied to classes that contain attributes that you want to exclude from serialization.
##### @exclude(\*args)
The ```exclude``` decorator prevents the specified attributes from being encoded.
```python
@urine.exclude('b', 'c')
def MyClass:
    a = 1   # will be encoded
    b = 2   # will not be encoded
    c = 3   # will not be encoded
```
##### @include(\*args)
The ```include``` decorator is the opposite of the ```exclude``` decorator. Only the specified attributes will be encoded.
```python
@urine.include('b', 'c')
def MyClass:
    a = 1   # will not be encoded
    b = 2   # will be encoded
    c = 3   # will be encoded
```

## Extensions
When you want to encode an object type that is not supported and remain its functionality you can write an extension that inherits ```urine.UrineExtension```. The extension must implement an ```encode``` and ```decode``` function to serialize and reconstruct the object. Use ```urine.extend()``` to register the extension.
```python
class MyExtension(urine.UrineExtension):
    def encode(obj):
        # Encode obj to a bytes-like object
        # ...
        return bytes_like_obj

    def decode(data):
        # Reconstruct the object using data
        # ...
        return reconstructed_obj


urine.extend(obj_type, MyExtension)
```
- ```encode(obj)``` is used to encode the object to a bytes-like object
    - ```obj``` is an instance of the object to be serialized
    - returns a bytes-like object (```bytes```, ```bytearray```)
- ```decode(data)``` is used to reconstruct the original object
    - ```data``` is a ```bytearray``` containing the encoded object
    - returns the reconstructed object
- ```obj_type``` is the object type the extension will apply to

Note that an extension must be registered using ```urine.extend()``` during both serialization and deserialization.

### Example: ```datetime.datetime``` extension
```python
import datetime
import struct

class DatetimeExtension(urine.UrineExtension):
    def encode(obj):
        return urine.encode([
            obj.year,
            obj.month,
            obj.day,
            obj.hour,
            obj.minute,
            obj.second,
            obj.microsecond
        ])

    def decode(data):
        decoded_data = urine.decode(data)
        return datetime.datetime(*decoded_data)


urine.extend(obj_type, MyExtension)
```
In order to serialize ```datetime.datetime```, all required attributes are encoded as a list. Inside ```decode()``` the list is decoded and used to instantiate a new, but identical instance of ```datetime.datetime```.<br>
Using this extension will produce the following output:
```python
now = datetime.datetime.today()

encoded_datetime = urine.encode(now)
decoded_datetime = urine.decode(encoded_datetime)

print(decoded_datetime)
print(decoded_datetime == now)
```
```
Output:

datetime.datetime(2022, 4, 13, 20, 15, 13, 289947)
True
```
Because of this extension, ```urine``` created an identical instance of ```datetime.datetime``` with all its functionality still available after deserialization.

## Supported object types
| **Type** | **Scheme** | **Description** |
| -------- | ---------- | ----------------|
| ```bool``` | ```[type<uint8>]```<br>```[bool<uint8>]``` | Boolean |
| ```int``` | ```[type<uint8>]```<br>```[int<(u)int8/16/32/64>]```<br><br>If int exceeds limit of (u)int64:<br>```[type<uint8>]```<br>```[int<bignum>]``` | Integer<br>*(Bignums are converted to a list of uint64 and 1 extra byte indicating positive or negative.)* |
| ```float``` | ```[type<uint8>]```<br>```[float<double>]``` | Floating point number<br>*(Floats are always encoded as a 64 bit double regardless of their value. This is how the Python interpreter treats them.)* |
| ```complex``` | ```[type<uint8>]```<br>```[real<double>]```<br>```[imag<double>]``` | Complex number |
| ```bytes``` | ```[type<uint8>]```<br>```[len<uint32>]```<br>```[data]``` | ```bytes```  object |
| ```bytearray``` | ```[type<uint8>]```<br>```[len<uint32>]```<br>```[data]``` | ```bytearray``` object |
| ```str``` | ```[type<uint8>]```<br>```[len<uint32>]```<br>```[string]``` | String<br>*(UTF-8 encoded)* |
| ```list``` | ```[type<uint8>]```<br>```[list_len<uint32>]```<br>```[content]``` | List |
| ```tuple``` | ```[type<uint8>]```<br>```[tuple_len<uint32>]```<br>```[content]``` | Tuple |
| ```set``` | ```[type<uint8>]```<br>```[set_len<uint32>]```<br>```[content]``` | Set |
| ```frozenset``` | ```[type<uint8>]```<br>```[set_len<uint32>]```<br>```[content]``` | Frozenset |
| ```dict``` | ```[type<uint8>]```<br>```[dict_len<uint32>]```<br>```[content]``` | Dictionary
| ```range``` | ```[type<uint8>]```<br>```[start<int>]```<br>```[stop<int>]```<br>```[step<int>]``` | Range<br>*(```start```, ```stop```, ```step``` are encoded like ```int```)* |
```None``` | ```[type<uint8>]``` | Null object
```UrineExtension``` | ```[type<uint8>]```<br>```[crc32<uin32>]```<br>```[len<uint32>]```<br>```[data]``` | Extension<br>*(```crc32``` is the CRC32 hash of the extension's class name used to identify the extension when decoding.)*
```object``` | ```[type<uint8>]```<br>```[name<str>]```<br>```[attrs_len<uint32>]```<br><br>for each attr:<br>```[attr_name<str>]```<br>```[attr]``` | Objects not listed above (User defined classes)
