import unicodedata
from unidecode import unidecode


def isChrLatin(c: str):
    return c.isalpha() and unicodedata.category(c) != 'Mn'


def toLatin(text: str):
    return ''.join(unidecode(c) for c in unicodedata.normalize('NFKD', text) if isChrLatin(c))


def latinAlphabet(uppercase: bool = False):
    a: int = 0x61 - 0x20 * uppercase
    return [chr(asciiVal) for asciiVal in range(a, a + 26)]