"""
BK-tree data structure to allow fast querying of "close" matches.
This code is licensed under a permissive MIT license -- see LICENSE.txt.
GitHub https://github.com/elpinal/pybkt
"""

from collections import deque, Iterable
from operator import itemgetter
import numpy as np

__all__ = ['levenshtein', 'BKTree']

__version__ = '1.0'


class BKTree:
    """
    Implementation of Burkhard-Keller tree

    :param distance_func: a function that returns the distance between two words.
                          Return value is a non-negative integer. The distance function must be a metric space.

    :param words: an iterable. Produces values that can be passed to distance_func
    """
    def __init__(self, distance_func: callable, words: Iterable = list()):
        self.distance_func = distance_func
        self.tree = None

        if words and isinstance(words, Iterable):
            it = iter(words)
            root = next(it)
            self.tree = (root, {})

            for i in it:
                self.add_word(i)

    def add_word(self, word: str) -> None:
        """
        Adds a word to the tree
        :param word: str
        """
        node = self.tree
        if node is None:
            self.tree = (word, {})
            return

        # Slight speed optimization -- avoid lookups inside the loop
        _distance_func = self.distance_func

        while True:
            parent, children = node
            distance = _distance_func(word, parent)
            # noinspection PyUnresolvedReferences
            node = children.get(str(distance))
            if node is None:
                children[str(distance)] = (word, {})
                break

    def query(self, word: str, n: int) -> list:
        """
        Return all words in the tree that are within a distance of `n'
        from `word`.
        :param word: str a word to query on
        :param n: int a non-negative integer that specifies the allowed distance from the query word.
        :return: list of tuples (distance, word), sorted in ascending order of distance.
        """

        def rec(parent):
            p_word, children = parent
            distance = self.distance_func(word, p_word)
            results = []
            if distance <= n:
                results.append((distance, p_word))

            for i in range(distance - n, distance + n + 1):
                child = children.get(str(i))
                if child is not None:
                    results.extend(rec(child))
            return results

        # sort by distance
        return sorted(rec(self.tree))

    def find(self, item: str, n: int) -> list:
        """
        Find items in this tree whose distance is less than or equal to n
        from given item, and return list of (distance, item) tuples ordered by
        distance.
        :param item: str word to find
        :param n: int maximum distance
        """
        if self.tree is None:
            return []

        candidates = deque([self.tree])
        found = []

        # Slight speed optimization -- avoid lookups inside the loop
        _candidates_popleft = candidates.popleft
        _candidates_extend = candidates.extend
        _found_append = found.append
        _distance_func = self.distance_func

        while candidates:
            candidate, children = _candidates_popleft()
            distance = _distance_func(candidate, item)
            if distance <= n:
                _found_append((distance, candidate))

            if children:
                lower = distance - n
                upper = distance + n
                _candidates_extend(c for d, c in children.items() if lower <= int(d) <= upper)

        found.sort(key=itemgetter(0))

        return found

    def save_to_file(self, file_path: str = None) -> None:
        """
        Stores the tree object in file
        :param file_path: str file to safe the tree
        """
        import json
        if not file_path:
            import os
            file_path = os.path.join(os.getcwd(), 'tree.json')
        with open(file_path, 'w') as file:
            file.write(json.dumps(self.tree))

    def load_from_file(self, file_path: str = None) -> None:
        """
        Load the tree object from file
        :param file_path: str file to load the tree
        """
        import json
        if not file_path:
            import os
            file_path = os.path.join(os.getcwd(), 'tree.json')
        with open(file_path, 'r') as file:
            self.tree = json.loads(file.read())


# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(source: str, target: str) -> int:
    """
    Calculates the levenshtein distance between two words
    :param source: str
    :param target: str
    :return:int distance

    """
    if len(source) < len(target):
        return levenshtein(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]


def dict_words(dict_file: str="/usr/share/dict/american-english") -> filter:
    """
    Return an iterator that produces words in the given dictionary.
    :param dict_file: str path to the dict file
    :return: filter iterator of words
    """
    return filter(len,
                  map(str.strip,
                      open(dict_file)))


def time_of(fn: callable, *args) -> object:
    """
    Calculates a function execution time
    :param fn: callable
    :param args: fn arguments
    :return: fn return
    """
    import time
    t = time.time()
    res = fn(*args)
    print("Time: ", (time.time() - t))
    return res


if __name__ == '__main__':
    # Create tree (takes some time ) and save to file
    # print("Creating the tree...")
    # tree = BKTree(levenshtein_dist, dict_words())
    # tree.save_to_file()

    # Create tree and load from file (fast)
    print("Loading the tree...")
    tree = BKTree(levenshtein)
    tree.load_from_file()

    print("Tree depth: %s\n" % tree_depth(tree.tree))

    print("Brute Force Time: ")
    print(time_of(brute_query, 'book', list(dict_words()), levenshtein, 1))

    print("\nBKTree time: ")
    print(time_of(tree.query, 'book', 1))
