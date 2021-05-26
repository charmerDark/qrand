##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 25, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from collections import OrderedDict
from typing import Dict, Optional

from .reverse_endian import reverse_endian

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
SYMBOLS = "<>.,:;_-+*=?!|@#$%&/()"


###############################################################################
## ALPHABET
###############################################################################
ALPHABET = UPPER + LOWER + NUMBERS + SYMBOLS


def alphabet_encode(uint: int, alphabet: Optional[str] = None) -> str:
    if not isinstance(uint, int):
        raise TypeError(f"Invalid uint type '{type(uint)}'. Expected int.")
    if uint < 1:
        raise ValueError(f"Invalid uint '{uint}'<1")
    alphabet = (
        _remove_duplicate_chars(alphabet)
        if alphabet and isinstance(alphabet, str)
        else ALPHABET
    )
    base: int = len(alphabet)
    numeral: str = ""
    while uint != 0:
        remainder: int = uint % base
        numeral += alphabet[remainder]
        uint //= base
    return reverse_endian(numeral)  # type: ignore


def alphabet_decode(numeral: str, alphabet: Optional[str] = None) -> int:
    numeral: str = reverse_endian(numeral)  # type: ignore
    alphabet = (
        _remove_duplicate_chars(alphabet)
        if alphabet and isinstance(alphabet, str)
        else ALPHABET
    )
    value_dict: Dict[str, int] = _build_value_dict(alphabet)
    base: int = len(alphabet)
    mult: int = 1
    uint: int = 0
    while numeral:
        uint += mult * value_dict[numeral[0]]
        numeral = numeral[1:]
        mult *= base
    return uint


def _build_value_dict(alphabet: str) -> Dict[str, int]:
    dictionary: Dict[str, int] = {}
    i: int = 0
    for char in alphabet:
        dictionary[char] = i
        i += 1
    return dictionary


def _remove_duplicate_chars(alphabet: str) -> str:
    od = OrderedDict.fromkeys(alphabet)
    return "".join(od)


###############################################################################
## BASE32
###############################################################################
BASE32_ALPHABET = UPPER + "234567"


def encode_base32(uint: int) -> str:
    return alphabet_encode(uint, BASE32_ALPHABET)


def decode_base32(numeral: str) -> int:
    return alphabet_decode(numeral, BASE32_ALPHABET)


###############################################################################
## BASE64
###############################################################################
BASE64_ALPHABET = UPPER + LOWER + NUMBERS + "+/"


def encode_base64(uint: int) -> str:
    return alphabet_encode(uint, BASE64_ALPHABET)


def decode_base64(numeral: str) -> int:
    return alphabet_decode(numeral, BASE64_ALPHABET)