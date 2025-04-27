"""Define contents and operations of one cube face that contains items."""

import numpy as np
import pandas as pd

from src.helper.constant import WRONG_CUBE_FACE_INPUT, \
    WRONG_FRAME_COLUMN_NAME, WRONG_FRAME_INDEX_NAME, WRONG_SIDE_LENGTH
from src.helper.utility import get_frame_column, get_frame_index


class Face:
    """Create a cube face with the required side length on inputs."""

    def __init__(self, face_input: list, side_length: int):
        """Initialize one cube face.

        :param face_input: The input to fill in the cube face.
        :param side_length: The required side length of the cube.
        """
        # Error check. The input length should be side length squared.
        assert len(face_input) == side_length ** 2, WRONG_CUBE_FACE_INPUT

        # Save the cube side length.
        self._side_length = side_length

        # Fill in the cube face matrix with the cubies.
        self._face_item_frame = pd.DataFrame(
            data=np.array_split(
                ary=face_input,
                indices_or_sections=side_length
            ),
            index=get_frame_index(cube_side_length=side_length),
            columns=get_frame_column(cube_side_length=side_length)
        )

    @property
    def get_item_list(self) -> list:
        """Get the entire cube face as a list."""
        # Return the frame value as a flat list.
        return list(self._face_item_frame.values.flat)

    def get_row(self, row_name: str) -> pd.Series:
        """Get one row in the cube face by index as a list."""
        # Return a deep copy of the desired row.
        return self._face_item_frame.loc[row_name].copy()

    def fill_row(self, row_name: str, input_list: list):
        """Fill one row in the cube face by index with a list."""
        # Error check. The input length is the same as the side length.
        assert len(input_list) == self._side_length, WRONG_SIDE_LENGTH
        # Error check. The index is not out of the list.
        assert row_name in self._face_item_frame.index, WRONG_FRAME_INDEX_NAME
        # Fill the desired row.
        self._face_item_frame.loc[row_name] = input_list

    def get_col(self, col_name: str) -> pd.Series:
        """Get one column in the cube face by index as a list."""
        # Return a deep copy of the desired row.
        return self._face_item_frame[col_name].copy()

    def fill_col(self, col_name: str, input_list: list):
        """Fill one column in the cube face by index with a list."""
        # Error check. The input length is the same as the side length.
        assert len(input_list) == self._side_length, WRONG_SIDE_LENGTH
        # Error check. The index is not out of the list.
        assert col_name in self._face_item_frame.columns, \
            WRONG_FRAME_COLUMN_NAME
        # Fill the desired column.
        self._face_item_frame[col_name] = input_list

    def rotate_by_angle(self, angle: int):
        """Rotate the cube face by the desired angle."""
        # Rotate the face itself.
        self._face_item_frame.update(
            pd.DataFrame(
                data=np.rot90(
                    self._face_item_frame.values, int(4 - angle / 90)
                ),
                index=self._face_item_frame.index,
                columns=self._face_item_frame.columns
            )
        )
