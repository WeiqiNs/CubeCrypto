"""Define contents and operations of one cubie."""

from __future__ import annotations

from collections import deque
from typing import List

from src.helper.constant import CUBIE_LENGTH, CubieItem, MOVE_ANGLE, \
    WRONG_CUBIE_INPUT, WRONG_ROTATION_ANGLE


class Cubie:
    """Create a cubie that holds four CubieItems based on the given input."""

    def __init__(self, cubie_input: List[CubieItem]):
        """Create a queue to hold the input four CubieItems.

        :param cubie_input: List of four CubieItem.
        """
        # Error check. Each cubie should only hold four values.
        assert len(cubie_input) == CUBIE_LENGTH, WRONG_CUBIE_INPUT
        # Convert the input list object as a deque object.
        self._content = deque(cubie_input)

    def get_content(self) -> List[CubieItem]:
        """Return the Cubie as a list of CubieItems."""
        return list(self._content)

    def get_content_string(self) -> str:
        """Return the Cubie src as a string."""
        return "".join(map(lambda item: str(item.content), self._content))

    def rotate_by_angle(self, angle: int):
        """Rotate the cubie src by desired angle.

        :param angle: The angle of desired rotation.
        """
        # Error check. Only possible angles are 90, 180 and 270 degrees.
        assert angle in MOVE_ANGLE, WRONG_ROTATION_ANGLE
        # Find how many clockwise 90 degree is needed.
        rotate_step = int(angle / 90)
        # Do the desired amount of rotations.
        self._content.rotate(rotate_step)

    def get_rotate_by_angle(self, angle: int) -> Cubie:
        """Rotate the cubie src by desired angle and return the result.

        :param angle: The angle of desired rotation.
        """
        # Error check. Only possible angles are 90, 180 and 270 degrees.
        assert angle in MOVE_ANGLE, WRONG_ROTATION_ANGLE
        # Find how many clockwise 90 degree is needed.
        rotate_step = int(angle / 90)
        # Do the desired amount of rotations.
        self._content.rotate(rotate_step)
        # Return the desired result.
        return self
