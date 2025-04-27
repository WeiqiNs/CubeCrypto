"""Define contents and operations of one cube face that contains bits."""

import itertools
import math
from collections import deque
from typing import List

import numpy as np
import pandas as pd

from src.encbit.cubie import Cubie
from src.helper.constant import CUBIE_LENGTH, CubieItem, WRONG_CUBE_FACE_INPUT, \
    WRONG_FRAME_COLUMN_NAME, \
    WRONG_FRAME_INDEX_NAME, WRONG_SIDE_LENGTH


class Face:
    """Create a cube face with the desired side length on inputs."""

    def __init__(self,
                 cube_face_input: List[CubieItem],
                 cube_side_length: int):
        """Initialize one cube face.

        :param cube_face_input: The input needed to fill in the cube face.
        :param cube_side_length: The desired side length of the cube.
        """
        # Error check. The input length should be cube face size times 4.
        assert len(cube_face_input) == cube_side_length ** 2 * CUBIE_LENGTH, \
            WRONG_CUBE_FACE_INPUT

        # Save the cube side length.
        self._side_length = cube_side_length

        # Split the cube face input to chunks with length of 4.
        face_input_list = [
            cube_face_input[index: index + 4]
            for index in range(0, len(cube_face_input), 4)
        ]

        # Create a list of cubies.
        face_input_cubie_list = [
            Cubie(cubie_input=cubie_input) for cubie_input in face_input_list
        ]

        # Fill in the cube face matrix with the cubies.
        self._face_cubie_frame = pd.DataFrame(
            data=np.array_split(
                ary=face_input_cubie_list,
                indices_or_sections=cube_side_length
            ),
            index=self.get_frame_index(cube_side_length=cube_side_length),
            columns=self.get_frame_column(cube_side_length=cube_side_length)
        )

    @property
    def face_string(self) -> str:
        """Get the entire cube face as a concatenated string."""
        # Convert each cubie to its string format.
        cubie_strings = [
            cubie.get_content_string()
            for cubie in list(self._face_cubie_frame.values.flat)
        ]

        # Concatenate the list to a string.
        return "".join(cubie_strings)

    @property
    def face_content(self) -> List[CubieItem]:
        """Get the entire cube face as a concatenated list."""
        # Get each cubie as a list and concatenate the lists.
        return list(itertools.chain.from_iterable(
            [
                cubie.get_content()
                for cubie in list(self._face_cubie_frame.values.flat)
            ]
        ))

    @staticmethod
    def get_frame_column(cube_side_length: int) -> list:
        """Get column names for the cube face data frame.

        :param cube_side_length: The desired side length of the cube.
        :return: A list object with the column names.
        """
        # If the side length is even, start with an empty queue.
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

        return list(column_queue)

    @staticmethod
    def get_frame_index(cube_side_length: int) -> list:
        """Get index names for the cube face data frame.

        :param cube_side_length: The desired side length of the cube.
        :return: A list object with the index names.
        """
        # If the side length is even, start with an empty queue.
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

        return list(index_queue)

    def get_row(self, row_name: str) -> pd.Series:
        """Get one row in the cube face by index as a list of cubies."""
        # Return a deep copy of the desired row.
        return self._face_cubie_frame.loc[row_name].copy()

    def fill_row(self, row_name: str, input_list: List[Cubie]):
        """Fill one row in the cube face by index with a list of cubies."""
        # Error check. The input length is the same as the side length.
        assert len(input_list) == self._side_length, WRONG_SIDE_LENGTH

        # Error check. The index is not out of the list.
        assert row_name in self._face_cubie_frame.index, WRONG_FRAME_INDEX_NAME

        # Fill the desired row.
        self._face_cubie_frame.loc[row_name] = input_list

    def get_col(self, col_name: str) -> pd.Series:
        """Get one column in the cube face by index as a list of cubies."""
        # Return a deep copy of the desired row.
        return self._face_cubie_frame[col_name].copy()

    def fill_col(self, col_name: str, input_list: List[Cubie]):
        """Fill one column in the cube face by index with a list of cubies."""
        # Error check. The input length is the same as the side length.
        assert len(input_list) == self._side_length, WRONG_SIDE_LENGTH

        # Error check. The index is not out of the list.
        assert col_name in self._face_cubie_frame.columns, \
            WRONG_FRAME_COLUMN_NAME

        # Fill the desired column.
        self._face_cubie_frame[col_name] = input_list

    def get_row_str(self, row_name: str) -> str:
        """Get one row in the cube face by index as a string."""
        # Get the desired cube row.
        cubie_row = self.get_row(row_name=row_name)

        # Convert each cubie to its string format.
        cubie_str_row = [cubie.get_content_string() for cubie in cubie_row]

        # Concatenate the list to a string.
        return "".join(["|", "|".join(cubie_str_row), "|"])

    def rotate_by_angle(self, angle: int):
        """Rotate the cube face and its cubies by the desired angle."""
        # Iterate over and rotate each cubie in the cube face.
        for cubie in list(self._face_cubie_frame.values.flat):
            cubie.rotate_by_angle(angle=angle)

        # Rotate the face itself.
        self._face_cubie_frame.update(
            pd.DataFrame(
                data=np.rot90(
                    self._face_cubie_frame.values, int(4 - angle / 90)
                ),
                index=self._face_cubie_frame.index,
                columns=self._face_cubie_frame.columns
            )
        )
