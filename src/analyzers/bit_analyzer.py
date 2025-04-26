"""Check how many bits of input will be changed."""

from typing import List
from src.helper.constant import Key
from src.encbit.cube import Cube


def analyze_bit(key: List[Key],
                side_length: int,
                random_bits: str,
                message_bits: str):
    """Given input and key, count how the number of bits changes afterward.

    :param message_bits: Bits for the actual message.
    :param random_bits: Bits for the randomness.
    :param key: The desired key to use.
    :param side_length: Desired length of the Rubik's Cube.
    :return: Number of zeros and number of ones in the encrypted result.
    """
    # Concatenate the input to get cube input.
    cube_input = message_bits + random_bits
    # Initialize the cube.
    cube = Cube(cube_input=cube_input, cube_side_length=side_length)

    # Xor, Shift, and apply move onto the cube.
    for each_key in key:
        cube.xor()
        cube.shift_cubie_content()
        cube.shift(key=each_key)

    # Count number of zeros and number of ones.
    return {
        "0": cube.content.count("0"),
        "1": cube.content.count("1")
    }
