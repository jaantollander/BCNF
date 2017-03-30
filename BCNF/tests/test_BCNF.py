from BCNF.BCNF import closure, fd_projection, \
    decompose_bcnf

assert closure({'A'}, []) == {'A'}

assert closure({'A'},
               [({'A'}, {'B'}),
                ({'B'}, {'C'}),
                ({'A', 'B'}, {'D'})]) == {'A', 'B', 'C', 'D'}

assert closure({'A', 'B'},
               [({'B', 'C'}, {'A', 'D'}),
                ({'A', 'B'}, {'C'}),
                ({'D'}, {'E'}),
                ({'C', 'F'}, {'B'})]) == {'A', 'B', 'C', 'D', 'E'}

fds = [
    ({'A'}, {'C', 'D'}),
    ({'B'}, {'E'}),
    ({'C'}, {'E'}),
    ({'E'}, {'F'}),
]
assert closure({'B'}, fds) == {'B', 'E', 'F'}

assert list(fd_projection(
    {'A', 'C'},
    [({'A'}, {'B'}), ({'B'}, {'C'}), ({'C'}, {'B', 'C'})])) == [({'A'}, {'C'})]


def test_decompose_bcnf():
    relation = {'A', 'B', 'C', 'D', 'E'}
    fds = [
        ({'A'}, {'B'}),
        ({'B'}, {'D', 'E'}),
        ({'C'}, {'E'}),
    ]
    assert decompose_bcnf(relation, fds) == [{'B', 'D', 'E'}, {'A', 'B'},
                                             {'A', 'C'}]


test_decompose_bcnf()
