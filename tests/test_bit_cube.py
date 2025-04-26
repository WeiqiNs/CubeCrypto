import copy
from src.encbit.cube import Cube
from src.helper.constant import CubeMove, WRONG_CUBE_MOVE, \
    WRONG_CUBE_INPUT, WRONG_CUBE_SIDE_LENGTH, Key


# noinspection PyProtectedMember
class TestCubeOperations:
    # Setup testing inputs.
    cube_input = \
        "1010101010101010101010101010101010101010101010101010101010101010" \
        "2020202020202020202020202020202020202020202020202020202020202020" \
        "3030303030303030303030303030303030303030303030303030303030303030" \
        "4040404040404040404040404040404040404040404040404040404040404040" \
        "5050505050505050505050505050505050505050505050505050505050505050" \
        "6060606060606060606060606060606060606060606060606060606060606060"

    # Create the cube.
    cube = Cube(
        cube_input=copy.deepcopy(cube_input),
        cube_side_length=4,
        track_location=10
    )

    def test_cube_content(self):
        assert self.cube.content == self.cube_input

    def test_cube_location_tracker(self):
        assert self.cube.get_tracked_location() == 10

    def test_cube_shift_cubie_content(self):
        self.cube.shift_cubie_content()
        assert self.cube.content == f"{self.cube_input[-1]}" \
            f"{self.cube_input[: -1]}"

    def test_cube_shift_cubie_content_back(self):
        self.cube.shift_cubie_content_back()
        assert self.cube.content == self.cube_input

    def test_top_shift(self):
        # This is the case where the top face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_t(index=2)
        assert cube.content == "01010101010101010101010101010101" \
                               "01010101010101010101010101010101" \
                               "30303030303030302020202020202020" \
                               "20202020202020202020202020202020" \
                               "50505050505050503030303030303030" \
                               "30303030303030303030303030303030" \
                               "40404040404040404040404040404040" \
                               "40404040404040404040404040404040" \
                               "60606060606060605050505050505050" \
                               "50505050505050505050505050505050" \
                               "20202020202020206060606060606060" \
                               "60606060606060606060606060606060"

    def test_down_shift(self):
        # This is the case where the down face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_d(index=2)
        assert cube.content == "10101010101010101010101010101010" \
                               "10101010101010101010101010101010" \
                               "20202020202020202020202020202020" \
                               "20202020202020206060606060606060" \
                               "30303030303030303030303030303030" \
                               "30303030303030302020202020202020" \
                               "04040404040404040404040404040404" \
                               "04040404040404040404040404040404" \
                               "50505050505050505050505050505050" \
                               "50505050505050503030303030303030" \
                               "60606060606060606060606060606060" \
                               "60606060606060605050505050505050"

    def test_right_shift(self):
        # This is the case where the right face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_r(index=2)
        assert cube.content == "10101010101020201010101010102020" \
                               "10101010101020201010101010102020" \
                               "20202020202040402020202020204040" \
                               "20202020202040402020202020204040" \
                               "03030303030303030303030303030303" \
                               "03030303030303030303030303030303" \
                               "40404040404050504040404040405050" \
                               "40404040404050504040404040405050" \
                               "10105050505050501010505050505050" \
                               "10105050505050501010505050505050" \
                               "60606060606060606060606060606060" \
                               "60606060606060606060606060606060"

    def test_left_shift(self):
        # This is the case where the left face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_l(index=2)
        assert cube.content == "50501010101010105050101010101010" \
                               "50501010101010105050101010101010" \
                               "10102020202020201010202020202020" \
                               "10102020202020201010202020202020" \
                               "30303030303030303030303030303030" \
                               "30303030303030303030303030303030" \
                               "20204040404040402020404040404040" \
                               "20204040404040402020404040404040" \
                               "50505050505040405050505050504040" \
                               "50505050505040405050505050504040" \
                               "06060606060606060606060606060606" \
                               "06060606060606060606060606060606"

    def test_front_shift(self):
        # This is the case where the front face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_f(index=2)
        assert cube.content == "10101010101010101010101010101010" \
                               "10101010101010100606060606060606" \
                               "02020202020202020202020202020202" \
                               "02020202020202020202020202020202" \
                               "01013030303030300101303030303030" \
                               "01013030303030300101303030303030" \
                               "03030303030303034040404040404040" \
                               "40404040404040404040404040404040" \
                               "50505050505050505050505050505050" \
                               "50505050505050505050505050505050" \
                               "60606060606004046060606060600404" \
                               "60606060606004046060606060600404"

    def test_back_shift(self):
        # This is the case where the back face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_b(index=2)
        assert cube.content == "03030303030303031010101010101010" \
                               "10101010101010101010101010101010" \
                               "20202020202020202020202020202020" \
                               "20202020202020202020202020202020" \
                               "30303030303004043030303030300404" \
                               "30303030303004043030303030300404" \
                               "40404040404040404040404040404040" \
                               "40404040404040400606060606060606" \
                               "05050505050505050505050505050505" \
                               "05050505050505050505050505050505" \
                               "01016060606060600101606060606060" \
                               "01016060606060600101606060606060"

    def test_middle_shift(self):
        # This is the case where the back face rotate. (4 by 4 by 4 cube)
        cube = Cube(cube_input=self.cube_input, cube_side_length=4)
        cube._shift_r(index=1)
        assert cube.content == "10101010202010101010101020201010" \
                               "10101010202010101010101020201010" \
                               "20202020404020202020202040402020" \
                               "20202020404020202020202040402020" \
                               "30303030303030303030303030303030" \
                               "30303030303030303030303030303030" \
                               "40404040505040404040404050504040" \
                               "40404040505040404040404050504040" \
                               "50501010505050505050101050505050" \
                               "50501010505050505050101050505050" \
                               "60606060606060606060606060606060" \
                               "60606060606060606060606060606060"

    def test_xor(self):
        # Set the cube to be half 1 and half 0.
        cube = Cube(cube_input="0" * 180 + "1" * 36, cube_side_length=3)
        # Xor the cube and test result.
        cube.xor()
        assert cube.content == "1" * 216


class TestCubeShift:
    # Setup testing inputs.
    cube_input = \
        "123456789012345678901234567890123456789012345678" \
        "123456789012345678901234567890123456789012345678"

    def test_content_message(self):
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        assert cube.message_content == \
            self.cube_input[:int(len(self.cube_input) * 5 / 6)]

    def test_random_message(self):
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        assert cube.random_content == \
            self.cube_input[int(len(self.cube_input) * 5 / 6):]

    def test_right_90(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.right.value, angle=90, index=1))
        assert cube.content == \
            "123412349012901278905678567834564123634585670789" \
            "123478569012907856341234785690123456789012345678"

    def test_left_90(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.left.value, angle=90, index=1))
        assert cube.content == \
            "129056783412345612341234901290123456789012345678" \
            "789056785678345678901290567834124123634585670789"

    def test_front_90(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.front.value, angle=90, index=1))
        assert cube.content == \
            "123456788567078985670789290141232901789063455678" \
            "412363459012345678901234567890123456412312348567"

    def test_back_90(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.back.value, angle=90, index=1))
        assert cube.content == \
            "890767859012345678901234567890123456456312340129" \
            "123456784563234185670789290141236785789023415678"

    def test_top_90(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.top.value, angle=90, index=1))
        assert cube.content == \
            "290141236345856734567890567890127890123412345678" \
            "123456789012345634567890567890127890123412345678"

    def test_down_90(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        cube.shift(Key(move=CubeMove.down.value, angle=90, index=1))
        assert cube.content == \
            "123456789012345678901234123456783456789056789012" \
            "290141236345856778901234123456783456789056789012"

    def test_location_null(self):
        # Create the cube without location tracker.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        try:
            cube.get_tracked_location()
            raise AssertionError("Error message did not raise.")
        except ValueError as error:
            assert str(error) == "No Tracked Location"

    def test_special(self):
        # Create the cube.
        cube = Cube(cube_input=self.cube_input, cube_side_length=2)
        try:
            cube.shift(Key(move="abracadabra", angle=90, index=0))
            raise AssertionError("Error message did not raise.")
        except ValueError as error:
            assert str(error) == WRONG_CUBE_MOVE


class TestCubeErrorCheck:
    def test_wrong_input_length(self):
        try:
            Cube(cube_input="abracadabra", cube_side_length=100)
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBE_INPUT

    def test_wrong_cube_side_length(self):
        try:
            Cube(cube_input="1" * 24, cube_side_length=1)
            raise AssertionError("Error message did not raise.")
        except AssertionError as error:
            assert str(error) == WRONG_CUBE_SIDE_LENGTH
