import numpy as np

from src.encitem.cube import Cube
from src.helper.constant import CubeMove, Key, WRONG_CUBE_INPUT, \
    WRONG_CUBE_MOVE, WRONG_CUBE_SIDE_LENGTH


# noinspection PyProtectedMember
class TestCubeOperations:
    # Setup testing inputs and create the cube.
    cube_input = [item for item in range(24)]
    cube = Cube(cube_input=cube_input, cube_side_length=2)

    def test_cube_content(self):
        assert self.cube.content == self.cube_input

    def test_cube_shift_cubie_content(self):
        self.cube.shift_content()
        assert self.cube.content == \
            [self.cube_input[-1]] + self.cube_input[:-1]

    def test_cube_shift_cubie_content_back(self):
        self.cube.shift_content_back()
        assert self.cube.content == self.cube_input

    def test_top_shift(self):
        # This is the case where the top face rotates.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.top.value, angle=90, index=1))
        assert np.array_equal(
            cube.content,
            [2, 0, 3, 1, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18,
             19, 20, 21, 22, 23]
        )

    def test_down_shift(self):
        # This is the case where the down face rotates.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.down.value, angle=90, index=1))
        assert np.array_equal(
            cube.content,
            [0, 1, 2, 3, 4, 5, 18, 19, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14,
             15, 22, 20, 23, 21]
        )

    def test_right_shift(self):
        # This is the case where the right face rotates.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.right.value, angle=90, index=1))
        assert np.array_equal(
            cube.content,
            [0, 5, 2, 7, 4, 21, 6, 23, 10, 8, 11, 9, 3, 13, 1, 15, 16, 17, 18,
             19, 20, 14, 22, 12]
        )

    def test_left_shift(self):
        # This is the case where the left face rotates.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.left.value, angle=90, index=1))
        assert np.array_equal(
            cube.content,
            [15, 1, 13, 3, 0, 5, 2, 7, 8, 9, 10, 11, 12, 22, 14, 20, 18, 16,
             19, 17, 4, 21, 6, 23]
        )

    def test_front_shift(self):
        # This is the case where the front face rotates.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.front.value, angle=90, index=1))
        assert np.array_equal(
            cube.content,
            [0, 1, 19, 17, 6, 4, 7, 5, 2, 9, 3, 11, 12, 13, 14, 15, 16, 20, 18,
             21, 10, 8, 22, 23]
        )

    def test_back_shift(self):
        # This is the case where the back face rotates.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.back.value, angle=90, index=1))
        assert np.array_equal(
            cube.content,
            [9, 11, 2, 3, 4, 5, 6, 7, 8, 23, 10, 22, 14, 12, 15, 13, 1, 17, 0,
             19, 20, 21, 16, 18]
        )

    def test_special(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        try:
            # Use an invalid key.
            cube.shift(Key(move="abracadabra", angle=90, index=0))
            raise AssertionError("Error message did not raise.")
        except ValueError as error:
            assert str(error) == WRONG_CUBE_MOVE


class TestCubeErrorCheck:
    def test_wrong_input_length(self):
        try:
            Cube(cube_input=[1], cube_side_length=100)
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBE_INPUT

    def test_wrong_cube_side_length(self):
        try:
            Cube(cube_input=[i for i in range(6)], cube_side_length=1)
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBE_SIDE_LENGTH
