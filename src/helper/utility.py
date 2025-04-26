"""Define the helper functions that may accessed by different parts."""

import math
import random
import binascii
import pandas as pd
from typing import List
from collections import deque
from src.helper.constant import Key, CUBE_MOVE, MOVE_ANGLE


def generate_random_keys(length: int, max_index: int) -> List[Key]:
    """Generate a random key with cube moves for a certain size cube.

    :param length: Desired number of moves of the key.
    :param max_index: Max index of the cube side.
    :return: A list of random keys.
    """
    return [
        Key(
            move=random.choice(CUBE_MOVE),
            angle=random.choice(MOVE_ANGLE),
            index=random.randint(1, max_index)
        ) for _ in range(length)
    ]


def get_key_table(key: List[Key]) -> pd.DataFrame:
    """Get list of keys as a DataFrame."""
    # Extract the values from NamedTuple to list.
    key_value_list = [[key.move, key.index, key.angle] for key in key]

    # Pack values into a DataFrame.
    return pd.DataFrame(
        data=key_value_list,
        index=[index + 1 for index in range(len(key))],
        columns=["Movement", "Index", "Angle"]
    )


def get_cube_layout(cube_side_length: int) -> pd.DataFrame:
    """Show the cube layout by returning a DataFrame."""
    # Create the pandas DataFrame filled with 0.
    return pd.DataFrame(
        data=0,
        index=get_frame_index(cube_side_length=cube_side_length),
        columns=get_frame_column(cube_side_length=cube_side_length)
    )


def get_frame_column(cube_side_length: int) -> deque:
    """Get column names for the cube face data frame.

    :param cube_side_length: The desired side length of the cube.
    :return: A deque object with the column names.
    """
    # If side length is even, start with empty queue.
    if cube_side_length % 2 == 0:
        column_queue = deque()
        # Pad R on the right side and L on the left side.
        for move_index in range(1, int(cube_side_length / 2) + 1):
            column_queue.appendleft(f"L{move_index}")
            column_queue.append(f"R{move_index}")

    # If side length is odd, start the queue with a "C" at the center.
    else:
        column_queue = deque("C")
        # Pad R on the right side and L on the left side.
        for move_index in range(1, int(math.ceil(cube_side_length / 2))):
            column_queue.appendleft(f"L{move_index}")
            column_queue.append(f"R{move_index}")

    return column_queue


def get_frame_index(cube_side_length: int) -> deque:
    """Get index names for the cube face data frame.

    :param cube_side_length: The desired side length of the cube.
    :return: A deque object with the index names.
    """
    # If side length is even, start with empty queue.
    if cube_side_length % 2 == 0:
        index_queue = deque()
        # Pad D on the right side and T on the left side.
        for move_index in range(1, int(cube_side_length / 2) + 1):
            index_queue.appendleft(f"T{move_index}")
            index_queue.append(f"D{move_index}")

    # If side length is odd, start the queue with a "C" at the center.
    else:
        index_queue = deque("C")
        # Pad D on the right side and T on the left side.
        for move_index in range(1, int(math.ceil(cube_side_length / 2))):
            index_queue.appendleft(f"T{move_index}")
            index_queue.append(f"D{move_index}")

    return index_queue


def string_to_binary(input_string: str) -> str:
    """Convert Ascii string to binary string.

    :param input_string: An input Ascii encoded string.
    :return: The binary encoded equivalence of the input Ascii string.
    """
    byte_from_str = binascii.a2b_qp(input_string)
    binary_from_byte = bin(int.from_bytes(byte_from_str, byteorder="big"))
    binary_from_byte = binary_from_byte.replace("b", "")
    # Make sure what ever being returned is multiple of 8.
    return f"{'0' * (8 - len(binary_from_byte) % 8)}{binary_from_byte}" \
        if len(binary_from_byte) % 8 != 0 \
        else binary_from_byte


def binary_to_string(input_binary: str) -> str:
    """Convert binary string to Ascii string.

    :param input_binary: An input binary encoded string.
    :return: The Ascii encoded equivalence of the input binary string.
    """
    binary_from_str = int(input_binary, 2)
    byte_from_binary = binary_from_str.to_bytes(
        length=(binary_from_str.bit_length() + 7) // 8, byteorder="big"
    )
    return byte_from_binary.decode("utf-8")


def xor(str_one: str, str_two: str) -> str:
    """Find the XOR result of two strings.

    :param str_one: The first input string.
    :param str_two: The second input string.
    :return: The XOR result of these two input strings.
    """
    return "".join(
        [
            "0" if value == str_two[index] else "1"
            for index, value in enumerate(str_one)
        ]
    )
