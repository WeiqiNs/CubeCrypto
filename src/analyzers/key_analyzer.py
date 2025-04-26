"""Defines the key length analyzer."""
import operator
from functools import reduce
from typing import List, Optional
from collections import namedtuple
from src.helper.constant import Key, CUBE_MOVE, COMMUTE_MOVE


class KeyAnalyzer:
    """Merge commute keys to check the effective length of the input key."""

    def __init__(self, key: List[Key]):
        """Initialize the analyzer with the key to be analyzing.

        :param key: A list of key object.
        """
        # Store the input list of keys to a class instance.
        self._key = key

    @staticmethod
    def _commute(move_one: CUBE_MOVE, move_two: CUBE_MOVE) -> bool:
        """Check if two keys commute.

        :param move_one: Name of the move.
        :param move_two: Name of the other move.
        :return: True if the two input moves commute, otherwise False.
        """
        # Two moves commute if they are the same.
        if move_one == move_two:
            return True
        # Check if the two different moves commute.
        elif {move_one, move_two} in COMMUTE_MOVE:
            return True
        # Otherwise, return False.
        else:
            return False

    @staticmethod
    def _merge_commute_key_list(commute_key: List[Key]) -> Optional[List[Key]]:
        """Given a list of commute keys, merge keys with same move and index.

        :param commute_key: A list of commute keys.
        :return: The reduced list of keys.
        """
        # Set the starting index to 0 and initialize the key index list.
        start_index = 0

        # Keep checking keys until all are checked.
        while start_index < len(commute_key):
            # Check all keys after the starting key.
            for each_key in commute_key[start_index + 1:]:
                # If the key share same index and move with the starting key.
                if each_key.move == commute_key[start_index].move \
                      and each_key.index == commute_key[start_index].index:
                    # Do the merge and replace start key.
                    commute_key[start_index] = Key(
                        move=commute_key[start_index].move,
                        index=commute_key[start_index].index,
                        angle=commute_key[start_index].angle + each_key.angle
                    )
                    # Remove the merged key.
                    commute_key.remove(each_key)
            # Move to the next key.
            start_index += 1

        # Only return the keys whose move angle is not a multiple of 360.
        return [
            Key(
                move=each_key.move,
                index=each_key.index,
                angle=each_key.angle % 360
            )
            for each_key in commute_key if each_key.angle % 360 != 0
        ]

    def _get_commute_key_list(self) -> List[List[Key]]:
        """Split list of keys to list of lists of commute keys."""
        # Set the starting index to 0 and initialize the key index list.
        start_index = 0
        key_index_list = []

        # Define commute key index named tuple.
        commute_key_index = namedtuple("index", ("start_index", "end_index"))

        # While not at the end of the key list, keep checking.
        while start_index < len(self._key):
            # Let end index be the same as the start index.
            end_index = start_index
            # If current key and next key commute, increase end index by 1.
            while end_index + 1 < len(self._key) and \
                self._commute(move_one=self._key[end_index].move,
                              move_two=self._key[end_index + 1].move):
                end_index += 1
            # When the key stop commuting, store the start and end indexes.
            key_index_list.append(
                commute_key_index(start_index=start_index, end_index=end_index)
            )
            # Increase start index by 1.
            start_index = end_index + 1

        # Based on the start and end index, get list of lists of commute keys.
        commute_key_list = [
            self._key[key_index.start_index: key_index.end_index + 1]
            if key_index.start_index != key_index.end_index
            else [self._key[key_index.start_index]]
            for key_index in key_index_list
        ]

        return commute_key_list

    def _merge_key(self) -> bool:
        """Merge the given list of keys once.

        :return: If merge performed, return True, otherwise return False.
        """
        # Get the list of merged key lists.
        merged_key_lists = [
            self._merge_commute_key_list(commute_key=commute_key)
            for commute_key in self._get_commute_key_list()
        ]

        # Flatten the list of lists to one list.
        merged_key = reduce(operator.concat, merged_key_lists)

        # See if the number of keys were reduced, if yes return True.
        if len(merged_key) != len(self._key):
            self._key = merged_key
            return True
        # Otherwise, return false.
        else:
            return False

    def analyze(self):
        """Keep reducing key size until no key can be merged."""
        # Assume there are more key to be reduced.
        while True:
            # If no more key can be reduced, break the while loop.
            if not self._merge_key():
                break

        # Return the reduced key.
        return self._key
