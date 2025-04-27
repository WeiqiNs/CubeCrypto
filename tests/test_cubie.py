from src.encbit.cubie import Cubie
from src.helper.constant import CubieItem, WRONG_CUBIE_INPUT, \
    WRONG_ROTATION_ANGLE


class TestCubie:
    # Setup testing input.
    CubieItem(content="0", marked=False)
    cubie = Cubie(
        cubie_input=[
            CubieItem(content=content, marked=False) for content in "1010"
        ]
    )

    def test_get_content(self):
        assert self.cubie.get_content() == [
            CubieItem(content=content, marked=False) for content in "1010"
        ]

    def test_get_content_string(self):
        assert self.cubie.get_content_string() == "1010"

    def test_rotation(self):
        self.cubie.rotate_by_angle(angle=90)
        assert self.cubie.get_content_string() == "0101"

    def test_get_rotation(self):
        assert self.cubie == self.cubie.get_rotate_by_angle(angle=90)


class TestCubieErrorCheck:
    def test_init(self):
        try:
            Cubie(cubie_input=list("abracadabra"))  # type: ignore
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBIE_INPUT

    def test_rotate(self):
        try:
            Cubie(
                cubie_input=[
                    CubieItem(content=content, marked=False)
                    for content in "1010"
                ]
            ).rotate_by_angle(angle=123)
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_ROTATION_ANGLE
