# pybkt
pybkt is a pure python3 implementation of Burkhard-Keller tree data structure. 

This implementation is based on:
* `ahupp/bktree`_: python2 code recursive implementation.
* `Jetsetter/pybktree`_: very nice implementation not recursive.

Both lookup methods from above implementations are included: 
``query()``: recursive
``find()``: not recursive

Example usage:

Create the tree using linux english words dictionary and levenshtein distance function.

.. code:: python
    
    >>> tree = BKTree(levenshtein, dict_words())    
    >>> tree.query('book', 1)  # Query the tree to find words at most 1 distance from 'book'
    [(0, 'book'), (1, 'Cook'), (1, 'boo'), (1, 'boob'), (1, 'books'), (1, 'boom'), (1, 'boon'), (1, 'boor'), (1, 'boos'), (1, 'boot'), (1, 'brook'), (1, 'cook'), (1, 'gook'), (1, 'hook'), (1, 'kook'), (1, 'look'), (1, 'nook'), (1, 'rook'), (1, 'took')]
    >>> # calling ``find()`` which is not recursive will give the same results
    >>> tree.find('book', 1)
    [(0, 'book'), (1, 'Cook'), (1, 'boo'), (1, 'boob'), (1, 'books'), (1, 'boom'), (1, 'boon'), (1, 'boor'), (1, 'boos'), (1, 'boot'), (1, 'brook'), (1, 'cook'), (1, 'gook'), (1, 'hook'), (1, 'kook'), (1, 'look'), (1, 'nook'), (1, 'rook'), (1, 'took')]

Creating the BkTree data structure using big amounts of data take some time so you can save it into a file and load it after.

.. code:: python
    
    >>> tree = BKTree(levenshtein, dict_words())    
    >>> tree.safe_to_file('tree.json')  # Safe the tree structure in a file, default 'tree.json' 
    >>> # Load the tree
    >>> tree1 = BKTree(levenshtein)
    >>> tree1.load('tree.json')
    >>> tree1.find('book', 1)
    [(0, 'book'), (1, 'Cook'), (1, 'boo'), (1, 'boob'), (1, 'books'), (1, 'boom'), (1, 'boon'), (1, 'boor'), (1, 'boos'), (1, 'boot'), (1, 'brook'), (1, 'cook'), (1, 'gook'), (1, 'hook'), (1, 'kook'), (1, 'look'), (1, 'nook'), (1, 'rook'), (1, 'took')]

Messure time vs brute force

.. code:: python
    
    >>> # Load the saved structure
    >>> tree = BKTree(levenshtein)
    >>> tree.load('tree.json')    
    >>> time_of(brute_query, 'book', list(dict_words()), levenshtein, 1)    
    Time:  5.613326072692871
    >>> time_of(tree.query, 'book', 1)  
    Time:  0.056838035583496094
    
    
TODO: Add python2 support.
