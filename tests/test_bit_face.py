from src.encbit.cubie import Cubie
from src.encbit.face import Face
from src.helper.constant import CubieItem, WRONG_CUBE_FACE_INPUT, \
    WRONG_FRAME_COLUMN_NAME, WRONG_FRAME_INDEX_NAME, \
    WRONG_SIDE_LENGTH


class TestCubeFace:
    # Setup testing input.
    face_input_contents = "000100100101101010101010101010101010"
    face_input = [
        CubieItem(content=content, marked=False)
        for content in face_input_contents
    ]
    cube_face = Face(
        cube_face_input=face_input,
        cube_side_length=3
    )

    def test_cube_face_string(self):
        assert self.cube_face.face_string == "".join(self.face_input_contents)

    def test_cube_face_content(self):
        assert self.cube_face.face_content == self.face_input

    def test_cube_frame_column(self):
        assert self.cube_face.get_frame_column(cube_side_length=4) == \
               ["L2", "L1", "R1", "R2"]
        assert self.cube_face.get_frame_column(cube_side_length=5) == \
               ["L2", "L1", "C", "R1", "R2"]

    def test_cube_frame_index(self):
        assert self.cube_face.get_frame_index(cube_side_length=4) == \
               ["T2", "T1", "D1", "D2"]
        assert self.cube_face.get_frame_index(cube_side_length=5) == \
               ["T2", "T1", "C", "D1", "D2"]

    def test_cube_row(self):
        # Get rows and check if they contain the desired value.
        row_t1 = self.cube_face.get_row(row_name="T1")
        assert row_t1.iloc[0].get_content_string() == "0001"
        row_d1 = self.cube_face.get_row(row_name="D1")
        assert row_d1.iloc[0].get_content_string() == "1010"

    def test_cube_fill_row(self):
        # Create a new testing cube face since the value gets changed.
        cube_face = Face(
            cube_face_input=self.face_input,
            cube_side_length=3
        )
        cube_face.fill_row(
            row_name="T1",
            input_list=[
                Cubie(
                    [CubieItem(content="1", marked=False) for _ in range(4)]
                ),
                Cubie(
                    [CubieItem(content="1", marked=False) for _ in range(4)]
                ),
                Cubie(
                    [CubieItem(content="1", marked=False) for _ in range(4)]
                )
            ]
        )
        # Get rows and check if they contain the desired value.
        row_t1 = cube_face.get_row(row_name="T1")
        assert row_t1.iloc[0].get_content_string() == "1111"
        row_d1 = self.cube_face.get_row(row_name="D1")
        assert row_d1.iloc[0].get_content_string() == "1010"

    def test_cube_col(self):
        # Get cols and check if they contain the desired value.
        col_r1 = self.cube_face.get_col(col_name="R1")
        assert col_r1.iloc[0].get_content_string() == "0101"
        col_l1 = self.cube_face.get_col(col_name="L1")
        assert col_l1.iloc[0].get_content_string() == "0001"

    def test_cube_fill_col(self):
        # Create a new testing cube face since the value gets changed.
        cube_face = Face(
            cube_face_input=self.face_input,
            cube_side_length=3
        )
        cube_face.fill_col(
            col_name="R1",
            input_list=[
                Cubie(
                    [CubieItem(content="1", marked=False) for _ in range(4)]
                ),
                Cubie(
                    [CubieItem(content="1", marked=False) for _ in range(4)]
                ),
                Cubie(
                    [CubieItem(content="1", marked=False) for _ in range(4)]
                )
            ]
        )
        # Get cols and check if they contain the desired value.
        col_r1 = cube_face.get_col(col_name="R1")
        assert col_r1.iloc[0].get_content_string() == "1111"
        col_l1 = cube_face.get_col(col_name="L1")
        assert col_l1.iloc[0].get_content_string() == "0001"

    def test_cube_row_str(self):
        # Get rows as strings and check if they equal to desired value.
        row_t1_str = self.cube_face.get_row_str(row_name="T1")
        row_d1_str = self.cube_face.get_row_str(row_name="D1")
        assert row_t1_str == "|0001|0010|0101|"
        assert row_d1_str == "|1010|1010|1010|"

    def test_cube_face_rotate(self):
        # Create a new testing cube face since the value gets changed.
        cube_face = Face(
            cube_face_input=self.face_input,
            cube_side_length=3
        )
        cube_face.rotate_by_angle(angle=90)
        assert cube_face.face_string == "010101011000010101010001010101011010"


class TestCubeFaceErrorCheck:
    # Setup testing input.
    face_input_contents = "000100100101101010101010101010101010"
    face_input = [
        CubieItem(content=content, marked=False)
        for content in face_input_contents
    ]
    cube_face = Face(
        cube_face_input=face_input,
        cube_side_length=3
    )

    def test_init(self):
        try:
            Face(
                cube_face_input=list("abracadabra"),  # type: ignore
                cube_side_length=3
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBE_FACE_INPUT

    def test_fill_row(self):
        try:
            self.cube_face.fill_row(
                row_name="T1",
                input_list=[
                    Cubie(cubie_input=list("0000"))  # type: ignore
                ]
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_SIDE_LENGTH

        try:
            self.cube_face.fill_row(
                row_name="abracadabra",
                input_list=[
                    Cubie(cubie_input=list("0000")),  # type: ignore
                    Cubie(cubie_input=list("0000")),  # type: ignore
                    Cubie(cubie_input=list("0000"))  # type: ignore
                ]
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_FRAME_INDEX_NAME

    def test_fill_col(self):
        try:
            self.cube_face.fill_col(
                col_name="R1",
                input_list=[
                    Cubie(cubie_input=list("0000"))  # type: ignore
                ]
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_SIDE_LENGTH

        try:
            self.cube_face.fill_col(
                col_name="abracadabra",
                input_list=[
                    Cubie(cubie_input=list("0000")),  # type: ignore
                    Cubie(cubie_input=list("0000")),  # type: ignore
                    Cubie(cubie_input=list("0000"))  # type: ignore
                ]
            )
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_FRAME_COLUMN_NAME
