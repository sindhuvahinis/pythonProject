"""
Reference : https://github.com/lanking520/djlsdk
"""
import struct
import numpy as np
from typing import List, Tuple

MAGIC_NUMBER = "NDAR"
VERSION = 2


def _set_int(value: int) -> bytes:
    return struct.pack(">i", value)


def _set_long(value: int) -> bytes:
    return struct.pack(">q", value)


def _set_str(value: str) -> bytes:
    return struct.pack(">h", len(value)) + bytes(value, "utf8")


def _set_char(value: str) -> bytes:
    return struct.pack('>h', ord(value))


def shape_encode(shape: Tuple[int], arr: bytearray):
    arr.extend(_set_int(len(shape)))
    layout = ""
    for ele in shape:
        arr.extend(_set_long(ele))
        layout += "?"
    arr.extend(_set_int(len(layout)))
    for ele in layout:
        arr.extend(_set_char(ele))


def djl_encode(ndlist: List[np.ndarray]) -> bytearray:
    arr = bytearray()
    arr.extend(_set_int(len(ndlist)))
    for nd in ndlist:
        arr.extend(_set_str(MAGIC_NUMBER))
        arr.extend(_set_int(VERSION))
        arr.append(0)  # no name
        arr.extend(_set_str("default"))
        arr.extend(_set_str(str(nd.dtype).upper()))
        shape_encode(nd.shape, arr)
        nd_bytes = nd.newbyteorder('>').tobytes("C")
        arr.extend(_set_int(len(nd_bytes)))
        arr.extend(nd_bytes)  # make it big endian
    return arr
