import numpy as np

from src.encitem.face import Face
from src.helper.constant import WRONG_CUBE_FACE_INPUT, WRONG_FRAME_COLUMN_NAME, \
    WRONG_FRAME_INDEX_NAME, \
    WRONG_SIDE_LENGTH


class TestCubeFace:
    # Setup testing input.
    face_input = [item for item in range(9)]
    cube_face = Face(face_input=face_input, side_length=3)

    def test_cube_face(self):
        assert np.array_equal(self.cube_face.get_item_list, self.face_input)

    def test_cube_row(self):
        # Get rows and check if they contain the desired value.
        assert self.cube_face.get_row(row_name="T1").iloc[0] == 0
        assert self.cube_face.get_row(row_name="D1").iloc[0] == 6

    def test_cube_fill_row(self):
        # Create a new testing cube face since the value gets changed.
        cube_face = Face(
            face_input=self.face_input, side_length=3
        )
        cube_face.fill_row(row_name="T1", input_list=[100, 200, 300])
        # Get a row and check if it contains the desired value.
        assert cube_face.get_row(row_name="T1").iloc[0] == 100

    def test_cube_col(self):
        # Get cols and check if they contain the desired value.
        assert self.cube_face.get_col(col_name="R1").iloc[0] == 2
        assert self.cube_face.get_col(col_name="L1").iloc[0] == 0

    def test_cube_fill_col(self):
        # Create a new testing cube face since the value gets changed.
        cube_face = Face(
            face_input=self.face_input,
            side_length=3
        )
        cube_face.fill_col(col_name="R1", input_list=[100, 200, 300])
        # Get col and check if it contains the desired value.
        assert cube_face.get_col(col_name="R1").iloc[0] == 100

    def test_cube_rotate(self):
        # Create a new testing cube face since the value gets changed.
        cube_face = Face(
            face_input=self.face_input,
            side_length=3
        )
        # Rotate the face and check if it contains the desired value.
        cube_face.rotate_by_angle(angle=90)
        assert np.array_equal(
            cube_face.get_item_list, [6, 3, 0, 7, 4, 1, 8, 5, 2]
        )


class TestCubeFaceErrorCheck:
    # Setup testing input.
    face_input = [item for item in range(9)]
    cube_face = Face(face_input=face_input, side_length=3)

    def test_init(self):
        try:
            Face(face_input=list("wrong"), side_length=3)
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBE_FACE_INPUT

    def test_fill_row(self):
        try:
            self.cube_face.fill_row(row_name="T1", input_list=[1])
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_SIDE_LENGTH

        try:
            self.cube_face.fill_row(
                row_name="abracadabra",
                input_list=[1, 2, 3]
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_FRAME_INDEX_NAME

    def test_fill_col(self):
        try:
            self.cube_face.fill_col(col_name="R1", input_list=[1])
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_SIDE_LENGTH

        try:
            self.cube_face.fill_col(
                col_name="abracadabra",
                input_list=[1, 2, 3]
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_FRAME_COLUMN_NAME
