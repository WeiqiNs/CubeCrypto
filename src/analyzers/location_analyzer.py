"""Defines the CubieItem location analyzer."""

import math
from typing import List
from src.encbit.cube import Cube
from src.helper.constant import Key, CUBE_MOVE, MOVE_ANGLE


class CubieLocationAnalyzer:
    """Create the location analyzer based on the location to keep track of."""

    def __init__(self, cube_side_length: int, track_item_location: int):
        """Initialize the cubie location analyzer with desired parameters.

        :param cube_side_length: Length of the cube desired to be analyzed.
        :param track_item_location: Locations of item interested.
        """
        # Store the cube side length.
        self._side_length = cube_side_length
        # Store the total cube size.
        self._cube_size = cube_side_length ** 2 * 24
        # Store the location of the tracked item.
        self._track_item_location = track_item_location

    def _get_basic_key(self) -> List[Key]:
        """Get all the possible keys with fixed 90 degrees.

        :return: A list of basic keys.
        """
        return [
            Key(move=move, angle=90, index=index)
            for move in CUBE_MOVE
            for index in range(1, math.floor(self._side_length / 2) + 1)
        ]

    def _check_effective_key(self, key: Key) -> bool:
        """Check if the given key moves the tracked item.

        :param key: The possible key that moves the location.
        :return: If the key actually moves the item. (Not Equal = True)
        """
        # Make a new copy of the cube.
        temp_cube = Cube(
            cube_input="_" * self._cube_size,
            cube_side_length=self._side_length,
            track_location=self._track_item_location
        )
        # Perform the desired shift.
        temp_cube.shift(key=key)
        # Return True if the location is changed.
        return temp_cube.get_tracked_location() != self._track_item_location

    def _get_effective_key(self) -> List[Key]:
        """Get all the keys that moves the tracked item with fixed 90 degrees.

        :return: A list of effective keys with fixed 90 degrees.
        """
        return [
            key for key in self._get_basic_key()
            if self._check_effective_key(key=key)
        ]

    def _get_all_effective_key(self) -> List[Key]:
        """Get all the keys that moves the tracked item with any angles.

        :return: A list of effective keys with any degree.
        """
        return [
            key._replace(angle=angle)
            for key in self._get_effective_key()
            for angle in MOVE_ANGLE
        ]

    def _get_location(self, key: Key) -> int:
        """Get location of the tracked item after performing a effective key.

        :param key: One known effective effective key.
        :return: New location of the tracked item.
        """
        # Make a new copy of the cube.
        temp_cube = Cube(
            cube_input="_" * self._cube_size,
            cube_side_length=self._side_length,
            track_location=self._track_item_location
        )
        # Perform the desired shift and shift the src.
        temp_cube.shift(key=key)
        temp_cube.shift_cubie_content()

        # Return the new location of the tracked item.
        return temp_cube.get_tracked_location()

    def get_all_location(self) -> List[int]:
        """Get all possible locations of the tracked item.

        :return: A list of possible locations of the tracked item.
        """
        return [(self._track_item_location + 1) % self._cube_size] + [
            self._get_location(key=key)
            for key in self._get_all_effective_key()
        ]

    @staticmethod
    def _get_location_after_key(key: Key, cube: Cube) -> int:
        """Perform a move on the cube and find the tracked bit.

        :param key: Indicate the movement on the cube.
        :param cube: The cube object.
        :return: The new location of the tracked bit.
        """
        cube.shift(key=key)
        cube.shift_cubie_content()
        return cube.get_tracked_location()

    def location_tracker(self, keys: List[Key]) -> List[int]:
        """Track position of a specific bit when moves are performed.

        :param keys: A list of cube movements.
        :return: A list of integers which each represent a location.
        """
        cube = Cube(
            cube_input="_" * self._cube_size,
            cube_side_length=self._side_length,
            track_location=self._track_item_location
        )

        return [self._track_item_location] + [
            self._get_location_after_key(key=key, cube=cube) for key in keys
        ]
