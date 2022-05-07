"""Hide messages in Zero-width characters."""

from typing import Final


CHARACTERS: Final = (
    "\u200b",  # zero-width space
    "\u200c",  # zero-width non-joiner
    "\u200d",  # zero-width joiner
    "\u200e",  # left-to-right mark
    "\u200f",  # right-to-left mark
    "\u202a",  # left-to-right embedding
    "\u202b",  # right-to-left embedding
    "\u2060",  # word joiner
)


ENCODING: Final = tuple(
    CHARACTERS[i1] + CHARACTERS[i2] + CHARACTERS[i3]
    for i1 in range(8)
    for i2 in range(8)
    for i3 in range(2)
)[:95]  # ASCII support : 95 printable characters


def _encode(message: str) -> str:
    """Encode a message into Zero-width characters.

    :param message: Message to encode.
    :type message: str
    :raises ValueError: Non-ASCII message
    :return: Encoded message
    :rtype: str
    """
    result = ""
    for char in message:
        code = ord(char)
        if code < 0x20 or code > 0x7e:
            raise ValueError(f"Message contains non-ASCII character: {char}")
        result += ENCODING[code - 0x20]
    return result


def _decode(message: str) -> str:
    """Decode a message from Zero-width characters.

    :param message: Message to encode.
    :type message: str
    :raises ValueError: Non-ASCII-encoded message
    :return: Encoded message
    :rtype: str
    """
    result = ""
    if len(message) % 3 != 0:
        raise ValueError("The message isn't Zero-width encoded.")
    for i in range(0, len(message), 3):
        code = ENCODING.index(message[i: i + 3]) + 0x20
        result += chr(code)
    return result


def hide(secret: str, carrier: str) -> str:
    """Hide a message in a carrier.

    :param secret: Message to hide.
    :type secret: str
    :param carrier: Carrier to hide the message in.
    :type carrier: str

    :raises ValueError: Non-ASCII secret

    :return: Carrier with the message hidden.
    """
    to_hide = _encode(secret)
    return carrier[:len(carrier) // 2] + to_hide + carrier[len(carrier) // 2:]


def retrieve(carrier: str) -> str:
    """Retrieve a message from a carrier.

    :param carrier: Carrier to retrieve the message from.
    :type carrier: str

    :raises ValueError: Invalid encoded message

    :return: Message retrieved from the carrier.
    """
    encoded = ""
    for char in carrier:
        if char in CHARACTERS:
            encoded += char
    return _decode(encoded)
