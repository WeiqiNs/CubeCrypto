from src.helper.constant import Key
from src.analyzers.key_analyzer import KeyAnalyzer


# noinspection PyProtectedMember
class TestKeyAnalyzer:
    # Set up the test key.
    key = [
        Key(move="right", angle=90, index=2),
        Key(move="left", angle=90, index=0),
        Key(move="right", angle=270, index=2),
        Key(move="top", angle=90, index=0),
        Key(move="right", angle=90, index=2),
        Key(move="right", angle=270, index=2),
        Key(move="down", angle=90, index=2),
        Key(move="top", angle=90, index=0),
        Key(move="left", angle=90, index=0),
        Key(move="front", angle=90, index=2),
        Key(move="back", angle=90, index=0),
        Key(move="front", angle=90, index=2),
        Key(move="right", angle=90, index=2),
        Key(move="right", angle=90, index=2)
    ]
    # Set up the key analyzer object.
    analyzer = KeyAnalyzer(key=key)

    def test_check_commute(self):
        assert self.analyzer._commute(move_one="left", move_two="left")
        assert self.analyzer._commute(move_one="right", move_two="left")
        assert not self.analyzer._commute(move_one="top", move_two="left")

    def test_get_commute_key_list(self):
        assert self.analyzer._get_commute_key_list() == [
            [
                Key(move="right", angle=90, index=2),
                Key(move="left", angle=90, index=0),
                Key(move="right", angle=270, index=2)
            ],
            [
                Key(move="top", angle=90, index=0)
            ],
            [
                Key(move="right", angle=90, index=2),
                Key(move="right", angle=270, index=2),
            ],
            [
                Key(move="down", angle=90, index=2),
                Key(move="top", angle=90, index=0)
            ],
            [
                Key(move="left", angle=90, index=0)
            ],
            [
                Key(move="front", angle=90, index=2),
                Key(move="back", angle=90, index=0),
                Key(move="front", angle=90, index=2)
            ],
            [
                Key(move="right", angle=90, index=2),
                Key(move="right", angle=90, index=2)
            ]
        ]

    def test_merge_commute_key_list(self):
        # This is the first test case.
        test_key = [
            Key(move="right", angle=90, index=2),
            Key(move="left", angle=90, index=0),
            Key(move="right", angle=180, index=2),
            Key(move="right", angle=90, index=2)
        ]
        assert \
            self.analyzer._merge_commute_key_list(commute_key=test_key) == \
            [Key(move="left", angle=90, index=0)]

        # This is the second test case.
        test_key = [
            Key(move="right", angle=90, index=2),
            Key(move="right", angle=90, index=1),
            Key(move="right", angle=90, index=0)
        ]
        assert \
            self.analyzer._merge_commute_key_list(commute_key=test_key) == \
            test_key

    def test_merge_key(self):
        self.analyzer._merge_key()
        assert self.analyzer._key == [
            Key(move="left", angle=90, index=0),
            Key(move="top", angle=90, index=0),
            Key(move="down", angle=90, index=2),
            Key(move="top", angle=90, index=0),
            Key(move="left", angle=90, index=0),
            Key(move="front", angle=180, index=2),
            Key(move="back", angle=90, index=0),
            Key(move="right", angle=180, index=2)
        ]

    def test_analyze(self):
        assert self.analyzer.analyze() == [
            Key(move="left", angle=90, index=0),
            Key(move="top", angle=180, index=0),
            Key(move="down", angle=90, index=2),
            Key(move="left", angle=90, index=0),
            Key(move="front", angle=180, index=2),
            Key(move="back", angle=90, index=0),
            Key(move="right", angle=180, index=2)
        ]
