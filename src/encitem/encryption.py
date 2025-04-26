"""Defines the encryption protocol."""

import random
import string
from collections import deque
from typing import List

import numpy as np

from src.encitem.cube import Cube
from src.helper.constant import Key


class Encryption:
    """Perform encryption and decryption of the input."""

    def __init__(self, message: str, cube_side_length: int):
        """Put the message into a cube and create a queue to hold keys.

        :param message: The message to encrypt.
        :param cube_side_length: The desired length of cube side.
        """
        # Remove blanks and punctuations.
        message = self.process_string(message=message)

        # Store the important information for other method to access.
        chunk_size = cube_side_length ** 2 * 6
        self.pad_size = chunk_size - len(message) % chunk_size

        # Make sure that the message is all lowercase and pad it.
        message += "".join(
            random.choice(string.ascii_lowercase) for _ in range(self.pad_size)
        )

        # Split the message into chunks that fits in the cube.
        messages = np.array_split(
            ary=list(message),
            indices_or_sections=int(len(message) / chunk_size)
        )

        # Get the cubes.
        self._cubes = [
            Cube(cube_input=message, cube_side_length=cube_side_length)
            for message in messages
        ]
        # Set up the holder for the key.
        self._key = deque()

    @staticmethod
    def process_string(message: str) -> str:
        """Remove blanks and punctuations in input and make it lowercase."""
        return "".join([
            char if char in string.ascii_letters else "" for char in message
        ]).lower()

    def get_current_content(self) -> str:
        """Get the input string at the current state."""
        # Note: This implementation assumes that input was a string.
        return "".join(["".join(cube.content) for cube in self._cubes])

    def encrypt(self, key: List[Key]):
        """Encrypt the message based on a given key.

        :param key: A list of keys used for encryption.
        """
        # Loop through all the keys.
        for each_key in key:
            # Shift all the cubes.
            for cube in self._cubes:
                # Shift src.
                cube.shift_content()
                # Perform cube move.
                cube.shift(key=each_key)
            # Append the used key to key list.
            self._key.append(each_key)

    def decrypt(self):
        """Decrypt the message to plain text."""
        # While there are still keys, keep running.
        while self._key:
            # Pop the key from saved keys.
            each_key = self._key.pop()
            for cube in self._cubes:
                # Reverse the cube shift move.
                cube.shift(
                    key=Key(
                        move=each_key.move,
                        angle=360 - each_key.angle,
                        index=each_key.index
                    )
                )
                # Shift src backward.
                cube.shift_content_back()

    def get_decrypted_str(self) -> str:
        """Decrypt the message and return the original input.

        :return: The original message that was encrypted as a string.
        """
        # First make sure that all cubes are decrypted.
        self.decrypt()
        # Return the decrypted string.
        return self.get_current_content()[:-self.pad_size]
