"""Constants for the project."""
from enum import Enum
from typing import NamedTuple

# ------------------------------- Constants ----------------------------------
# Each cubie should hold four bits binary.
CUBIE_LENGTH = 4
# All possible rotations angles for one move.
MOVE_ANGLE = [90, 180, 270]
# All possible movements.
CUBE_MOVE = ["right", "left", "top", "down", "front", "back"]
# List of tuples, each tuple represent two movements that are commute.
COMMUTE_MOVE = [{"right", "left"}, {"top", "down"}, {"front", "back"}]


# The item we want to fill in the cubie.
class CubieItem(NamedTuple):
    """Define the item that each cubie holds."""

    content: str
    marked: bool


# The src of one key.
class Key(NamedTuple):
    """Define the components of a legal key."""

    move: str
    angle: int
    index: int


# Set enum object for moves.
class CubeMove(Enum):
    """Define the legal moves for a cube."""

    left = "left"
    right = "right"
    top = "top"
    down = "down"
    front = "front"
    back = "back"


# ---------------------------- Error Messages --------------------------------
# Error messages for the Cubie class.
WRONG_CUBIE_INPUT = "The input length does not match the length of a cubie."

# Error messages for the CubeFaceForItem class.
WRONG_SIDE_LENGTH = "The input length does not match the cube side length."
WRONG_FRAME_INDEX_NAME = "The input index name is not in the frame index."
WRONG_FRAME_COLUMN_NAME = "The input column name is not in the frame column."
WRONG_CUBE_FACE_INPUT = "The input length does not match the desired length " \
                        "of a cube face"

# Error messages for the CubeForCubie class.
WRONG_CUBE_MOVE = "The input cube move is undefined."
WRONG_CUBE_SIDE_LENGTH = "The input cube side length is too short."
WRONG_CUBE_INPUT = "The input length does not match size of the entire cube."

# Error messages for cross-project usage.
WRONG_ROTATION_ANGLE = "Wrong rotation angle for the cube."
