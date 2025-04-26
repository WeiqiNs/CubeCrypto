import numpy as np

from src.analyzers.location_analyzer import CubieLocationAnalyzer
from src.helper.constant import CUBE_MOVE, Key, MOVE_ANGLE


# noinspection PyProtectedMember
class TestCubieLocationAnalyzer:
    analyzer = CubieLocationAnalyzer(
        cube_side_length=3, track_item_location=0
    )

    def test_get_all_basic_key(self):
        assert self.analyzer._get_basic_key() == [
            Key(move=move, angle=90, index=1) for move in CUBE_MOVE
        ]

    def test_check_effective_key(self):
        assert self.analyzer._check_effective_key(
            key=Key(move="left", angle=90, index=1)
        )

    def test_get_effective_key(self):
        assert self.analyzer._get_effective_key() == [
            Key(move=move, angle=90, index=1)
            for move in ["left", "top", "back"]
        ]

    def test_get_all_effective_key(self):
        assert self.analyzer._get_all_effective_key() == [
            Key(move=move, angle=angle, index=1)
            for move in ["left", "top", "back"]
            for angle in MOVE_ANGLE
        ]

    def test_get_location(self):
        assert self.analyzer._get_location(
            key=Key(move="left", angle=90, index=1)) == 37

    def test_get_all_location(self):
        np.testing.assert_array_equal(
            self.analyzer.get_all_location(),
            [1, 37, 145, 215, 10, 35, 28, 136, 179, 82]
        )

    def test_location_tracker(self):
        # Set up analyzer and the key to perform checking.
        analyzer = CubieLocationAnalyzer(
            cube_side_length=3, track_item_location=0
        )
        keys = [
            Key(move="left", angle=90, index=1),
            Key(move="top", angle=90, index=1),
            Key(move="down", angle=90, index=1)
        ]

        np.testing.assert_array_equal(
            analyzer.location_tracker(keys=keys), [0, 37, 110, 183]
        )
