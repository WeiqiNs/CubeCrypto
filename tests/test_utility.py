from collections import deque

import pandas as pd

import src.helper.utility as utility
from src.helper.constant import CUBE_MOVE, Key, MOVE_ANGLE


class TestUtility:
    def test_key_gen(self):
        # Generate key and extract important information to test.
        keys = utility.generate_random_keys(length=50, max_index=2)
        key_angle = [key.angle for key in keys]
        key_move = [key.move for key in keys]
        key_index = [key.index for key in keys]
        assert set(key_angle).issubset(MOVE_ANGLE)
        assert set(key_move).issubset(CUBE_MOVE)
        assert set(key_index).issubset([1, 2])

    def test_key_table(self):
        pd.testing.assert_frame_equal(
            utility.get_key_table(
                key=[
                    Key(move="right", index=1, angle=180),
                    Key(move="top", index=2, angle=90),
                    Key(move="back", index=1, angle=270),
                ]
            ),
            pd.DataFrame(
                data=[["right", 1, 180], ["top", 2, 90], ["back", 1, 270]],
                index=[1, 2, 3],
                columns=["Movement", "Index", "Angle"]
            )
        )

    def test_cube_layout(self):
        pd.testing.assert_frame_equal(
            utility.get_cube_layout(cube_side_length=2),
            pd.DataFrame(data=0, index=["T1", "D1"], columns=["L1", "R1"])
        )

    def test_cube_frame_column(self):
        assert utility.get_frame_column(cube_side_length=4) == \
            deque(["L2", "L1", "R1", "R2"])
        assert utility.get_frame_column(cube_side_length=5) == \
            deque(["L2", "L1", "C", "R1", "R2"])

    def test_cube_frame_index(self):
        assert utility.get_frame_index(cube_side_length=4) == \
            deque(["T2", "T1", "D1", "D2"])
        assert utility.get_frame_index(cube_side_length=5) == \
            deque(["T2", "T1", "C", "D1", "D2"])

    def test_xor(self):
        assert utility.xor(str_one="1001", str_two="1100") == "0101"

    def test_string_to_binary(self):
        assert utility.string_to_binary(input_string="A") == "01000001"

    def test_binary_to_string(self):
        assert utility.binary_to_string(input_binary="01000001") == "A"
