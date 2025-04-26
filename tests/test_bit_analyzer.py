from src.helper.utility import generate_random_keys
from src.analyzers.bit_analyzer import analyze_bit


def test_bit_analyzer():
    key = generate_random_keys(length=20, max_index=1)
    result = analyze_bit(
        key=key,
        side_length=3,
        random_bits="0" * 36,
        message_bits="0" * 180
    )
    assert result["0"] == 216
