class UrineExtension:
    """Base class that every urine extension implements
    """
    def encode(obj):
        """Encodes the extension object.

        Args:
            obj (object): Object to be encoded

        Returns:
            bytes, bytearray: Encoded object

        Raises:
            NotImplementedError: Function not implemented
        """
        raise NotImplementedError('Extension has no encode() function implemented')

    def decode(data):
        """Decodes the extension object.

        Args:
            data (bytearray): Data to be decoded

        Returns:
            object: Decoded object

        Raises:
            NotImplementedError: Function not implemented
        """
        raise NotImplementedError('Extension has no decode() function implemented')
