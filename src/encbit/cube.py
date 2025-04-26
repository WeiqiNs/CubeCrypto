"""Define contents and operations of the entire cube that holds bits."""

import math
from typing import List

from src.encbit.face import Face
from src.helper.constant import CubeMove, CUBIE_LENGTH, CubieItem, Key, \
    WRONG_CUBE_INPUT, WRONG_CUBE_MOVE, \
    WRONG_CUBE_SIDE_LENGTH
from src.helper.utility import xor


class Cube:
    """Create a full cube with desired side length on inputs."""

    def __init__(self,
                 cube_input: str,
                 cube_side_length: int,
                 track_location: int = None):
        """Initialize entire cube with a string of desired length.

        :param cube_input: The binary representation of the plain text.
        :param cube_side_length: The desired side length of the cube.
        :param track_location: The desired item locations to keep track.
        """
        # Check length of the input.
        assert len(cube_input) == cube_side_length ** 2 * 6 * CUBIE_LENGTH, \
            WRONG_CUBE_INPUT
        assert cube_side_length > 1, WRONG_CUBE_SIDE_LENGTH

        # Save the cube size, side length, max index and the tracked location.
        self._cube_size = len(cube_input)
        self._side_length = cube_side_length
        self._cube_max_index = math.floor(cube_side_length / 2)
        self._track_location = track_location

        # Create the list of cubie items.
        cubie_list = [
            CubieItem(content=content, marked=False) for content in cube_input
        ]

        # Update the marked location, if any.
        if track_location is not None:
            cubie_list[track_location] = \
                cubie_list[track_location]._replace(marked=True)

        # Split the cube input into six arrays.
        cubie_input_list = [
            cubie_list[index: index + cube_side_length ** 2 * 4]
            for index in range(0, len(cubie_list), cube_side_length ** 2 * 4)
        ]

        # Assume that we fill the cube in the following order:
        #   - 1. Top face, first chunk of message
        #   - 2. Front face, second chunk of message
        #   - 3. Right face, third chunk of message
        #   - 4. Back face, second chunk of random
        #   - 5. Left face, third chunk of random
        #   - 6. Down face, first chunk of random
        self._top_face = Face(
            cube_face_input=cubie_input_list[0],
            cube_side_length=cube_side_length
        )
        self._front_face = Face(
            cube_face_input=cubie_input_list[1],
            cube_side_length=cube_side_length
        )
        self._right_face = Face(
            cube_face_input=cubie_input_list[2],
            cube_side_length=cube_side_length
        )
        self._down_face = Face(
            cube_face_input=cubie_input_list[3],
            cube_side_length=cube_side_length
        )
        self._back_face = Face(
            cube_face_input=cubie_input_list[4],
            cube_side_length=cube_side_length
        )
        self._left_face = Face(
            cube_face_input=cubie_input_list[5],
            cube_side_length=cube_side_length
        )

    @property
    def content(self) -> str:
        """Format all cubies into a continuous string.

        :return: A string contains all cubies.
        """
        # Get all cube faces as string in the right order.
        return self.message_content + self.random_content

    @property
    def message_content(self) -> str:
        """Format all cubies that hold message into a continuous string.

        :return: A string contains all cubies that hold message.
        """
        # Get all cube faces as string in the right order.
        return \
            f"{self._top_face.face_string}" \
            f"{self._front_face.face_string}" \
            f"{self._right_face.face_string}" \
            f"{self._down_face.face_string}" \
            f"{self._back_face.face_string}"

    @property
    def message_content_list(self) -> List[str]:
        """Format all cubies that hold message into list of strings by faces.

        :return: A list of strings that hold the actual message.
        """
        # Get all cube faces as string in the right order.
        return [
            self._top_face.face_string,
            self._front_face.face_string,
            self._right_face.face_string,
            self._down_face.face_string,
            self._back_face.face_string
        ]

    @property
    def random_content(self) -> str:
        """Format all cubies that hold random bits into a continuous string.

        :return: A string contains all cubies that hold random bits.
        """
        # Get all cube faces as string in the right order.
        return self._left_face.face_string

    def get_tracked_location(self) -> int:
        """Get location for the tracked cubie.

        :return: The integer index.
        """
        # Get all cubie items as a list.
        all_cubie_item = \
            self._top_face.face_content + self._front_face.face_content + \
            self._right_face.face_content + self._back_face.face_content + \
            self._left_face.face_content + self._down_face.face_content

        # Return the tracked locations.
        for location, cubie in enumerate(all_cubie_item):
            if cubie.marked:
                return location

        # If no location was found, throw value error.
        raise ValueError("No Tracked Location")

    def shift_cubie_content(self):
        """Shift the cube binary representation to right by one bit."""
        # Obtain the shifted src by padding the last bit to the first.
        shifted_content = f"{self.content[-1]}{self.content[:-1]}"

        # Find the the track location.
        track_location = None if self._track_location is None else \
            (self.get_tracked_location() + 1) % self._cube_size

        # Re-Init the class with new src.
        self.__init__(
            cube_input=shifted_content,
            track_location=track_location,
            cube_side_length=self._side_length
        )

    def shift_cubie_content_back(self):
        """Shift the cube binary representation to left by one bit."""
        # Obtain the shifted src by padding the first bit to the last.
        shifted_content = f"{self.content[1:]}{self.content[0]}"

        # Find the the track location.
        track_location = None if self._track_location is None else \
            (self.get_tracked_location() - 1) % self._cube_size

        # Re-Init the class with new src.
        self.__init__(
            cube_input=shifted_content,
            cube_side_length=self._side_length,
            track_location=track_location
        )

    def _shift_t(self, index: int):
        """Shift the top layer with the index clockwise by 90 degrees.

        :param index: The layer selected for the move.
        """
        # If the most outer layer was selected, rotate the corresponding face.
        if index == self._cube_max_index:
            self._top_face.rotate_by_angle(angle=90)

        # Save temp row.
        temp_row = self._left_face.get_row(row_name=f"T{index}").values

        # back -> right -> front -> left -> back
        self._left_face.fill_row(
            row_name=f"T{index}",
            input_list=self._front_face.get_row(row_name=f"T{index}").values
        )
        self._front_face.fill_row(
            row_name=f"T{index}",
            input_list=self._right_face.get_row(row_name=f"T{index}").values
        )
        self._right_face.fill_row(
            row_name=f"T{index}",
            input_list=self._back_face.get_row(row_name=f"T{index}").values
        )
        self._back_face.fill_row(row_name=f"T{index}", input_list=temp_row)

    def _shift_d(self, index: int):
        """Shift the down layer with the index clockwise by 90 degrees.

        :param index: The layer selected for the move.
        """
        # If the most outer layer was selected, rotate the corresponding face.
        if index == self._cube_max_index:
            self._down_face.rotate_by_angle(angle=90)

        # Save temp row.
        temp_row = self._left_face.get_row(row_name=f"D{index}").values

        # back -> left -> front -> right -> back
        self._left_face.fill_row(
            row_name=f"D{index}",
            input_list=self._back_face.get_row(row_name=f"D{index}").values
        )
        self._back_face.fill_row(
            row_name=f"D{index}",
            input_list=self._right_face.get_row(row_name=f"D{index}").values
        )
        self._right_face.fill_row(
            row_name=f"D{index}",
            input_list=self._front_face.get_row(row_name=f"D{index}").values
        )
        self._front_face.fill_row(row_name=f"D{index}", input_list=temp_row)

    def _shift_f(self, index: int):
        """Shift the front layer with the index clockwise by 90 degrees.

        :param index: The layer selected for the move.
        """
        # If the most outer layer was selected, rotate the corresponding face.
        if index == self._cube_max_index:
            self._front_face.rotate_by_angle(angle=90)

        # Save temp row.
        temp_row = self._top_face.get_row(row_name=f"D{index}").values

        # top -> right -> down -> left -> top
        self._top_face.fill_row(
            row_name=f"D{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=90)
                for cubie in
                self._left_face.get_col(col_name=f"R{index}").values[::-1]
            ]
        )
        self._left_face.fill_col(
            col_name=f"R{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=90)
                for cubie in
                self._down_face.get_row(row_name=f"T{index}").values
            ]
        )
        self._down_face.fill_row(
            row_name=f"T{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=90)
                for cubie in
                self._right_face.get_col(col_name=f"L{index}").values[::-1]
            ]
        )
        self._right_face.fill_col(
            col_name=f"L{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=90) for cubie in temp_row
            ]
        )

    def _shift_b(self, index: int):
        """Shift the back layer with the index clockwise by 90 degrees.

        :param index: The layer selected for the move.
        """
        # If the most outer layer was selected, rotate the corresponding face.
        if index == self._cube_max_index:
            self._back_face.rotate_by_angle(angle=90)

        # Save temp row.
        temp_row = self._top_face.get_row(row_name=f"T{index}").values

        # top -> left -> down -> right -> top
        self._top_face.fill_row(
            row_name=f"T{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=270)
                for cubie in
                self._right_face.get_col(col_name=f"R{index}").values
            ]
        )
        self._right_face.fill_col(
            col_name=f"R{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=270)
                for cubie in
                self._down_face.get_row(row_name=f"D{index}").values[::-1]
            ]
        )
        self._down_face.fill_row(
            row_name=f"D{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=270)
                for cubie in
                self._left_face.get_col(col_name=f"L{index}").values
            ]
        )
        self._left_face.fill_col(
            col_name=f"L{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=270)
                for cubie in temp_row[::-1]
            ]
        )

    def _shift_r(self, index: int):
        """Shift the right layer with the index clockwise by 90 degrees.

        :param index: The layer selected for the move.
        """
        # If the most outer layer was selected, rotate the corresponding face.
        if index == self._cube_max_index:
            self._right_face.rotate_by_angle(angle=90)

        # Save temp column.
        temp_col = self._front_face.get_col(col_name=f"R{index}").values

        # top -> back -> down -> front -> top
        self._front_face.fill_col(
            col_name=f"R{index}",
            input_list=[
                cubie
                for cubie in
                self._down_face.get_col(col_name=f"R{index}").values
            ]
        )
        self._down_face.fill_col(
            col_name=f"R{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=180)
                for cubie in
                self._back_face.get_col(col_name=f"L{index}").values[::-1]
            ]
        )
        self._back_face.fill_col(
            col_name=f"L{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=180)
                for cubie in
                self._top_face.get_col(col_name=f"R{index}").values[::-1]
            ]
        )
        self._top_face.fill_col(col_name=f"R{index}", input_list=temp_col)

    def _shift_l(self, index: int):
        """Shift the left layer with the index clockwise by 90 degrees.

        :param index: The layer selected for the move.
        """
        # If the most outer layer was selected, rotate the corresponding face.
        if index == self._cube_max_index:
            self._left_face.rotate_by_angle(angle=90)

        # Save temp column.
        temp_col = self._front_face.get_col(col_name=f"L{index}").values

        # top -> front -> down -> back -> top
        self._front_face.fill_col(
            col_name=f"L{index}",
            input_list=[
                cubie
                for cubie in
                self._top_face.get_col(col_name=f"L{index}").values
            ]
        )
        self._top_face.fill_col(
            col_name=f"L{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=180)
                for cubie in
                self._back_face.get_col(col_name=f"R{index}").values[::-1]
            ]
        )
        self._back_face.fill_col(
            col_name=f"R{index}",
            input_list=[
                cubie.get_rotate_by_angle(angle=180)
                for cubie in
                self._down_face.get_col(col_name=f"L{index}").values[::-1]
            ]
        )
        self._down_face.fill_col(col_name=f"L{index}", input_list=temp_col)

    def shift(self, key: Key):
        """Shift the cube with a move in certain amount of angle.

        :param key: A named tuple that holds information for one shift.
        """
        # Calculate the number of movements.
        number_of_movements = int(key.angle / 90)
        # Perform moves based on the inputs.
        if key.move == CubeMove.left.value:
            for _ in range(number_of_movements):
                self._shift_l(index=key.index)

        elif key.move == CubeMove.right.value:
            for _ in range(number_of_movements):
                self._shift_r(index=key.index)

        elif key.move == CubeMove.top.value:
            for _ in range(number_of_movements):
                self._shift_t(index=key.index)

        elif key.move == CubeMove.down.value:
            for _ in range(number_of_movements):
                self._shift_d(index=key.index)

        elif key.move == CubeMove.back.value:
            for _ in range(number_of_movements):
                self._shift_b(index=key.index)

        elif key.move == CubeMove.front.value:
            for _ in range(number_of_movements):
                self._shift_f(index=key.index)

        # If the input movement was not defined.
        else:
            raise ValueError(WRONG_CUBE_MOVE)

    def xor(self):
        """Xor the random face with each other faces."""
        # Find the xor result and use it as the new src to initiate class.
        xor_result = "".join([
            xor(
                str_one=message_content,
                str_two=self.random_content
            )
            for message_content in self.message_content_list
        ])

        # Re-Init the class with new src.
        self.__init__(
            cube_input=xor_result + self.random_content,
            track_location=self._track_location,
            cube_side_length=self._side_length
        )
