"""Compute BCNF for relation with functional dependencies.

References:
    - https://stackoverflow.com/questions/15102485/decomposing-a-relation-into-bcnf

Attributes:
    A: Type of the attribute. Must be hashable.
    Relation: Namedtuple with attributes 
        - name (str): 
        - attributes (Set[A]): 
    FunctionalDependency: Functional dependency X -> Y
        - X (Set[A]): 
        - Y (Set[A]): 
"""
from collections import namedtuple
from itertools import chain, combinations

from typing import TypeVar, Set, List, Iterator

__all__ = """
Relation
FunctionalDependency
closure
fd_projection
Node
decompose_bcnf_tree
""".split()

A = TypeVar('T')  # Attribute. Hashable.
Relation = namedtuple('Relation', 'name attributes')
FunctionalDependency = namedtuple('FunctionalDependency', 'X Y')


class Node:
    def __init__(self, value, depth=0):
        self.value: Relation = value  # Relation
        self.left: Node = None  # Node
        self.right: Node = None  # Node
        self.depth: int = depth

    def __str__(self):
        return "{value}\n" \
               "{depth}|- {left}\n" \
               "{depth}|- {right}".format(
            value=self.value, left=self.left, right=self.right,
            depth=self.depth * '  ')


def powerset(iterable):
    """Powerset

    >>> powerset([1,2,3]) 
    () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    return map(set, chain.from_iterable(
        combinations(iterable, r) for r in range(len(iterable) + 1)))


def closure(attributes: Set[A],
            fds: List[FunctionalDependency]) -> Set[A]:
    r"""Compute closure of attributes in relation with functional dependencies
    
    Attributes:
        attributes:
            Attributes :math:`X`
        fds:
            Functional dependencies :math:`S`
    
    Returns:
        set: Closure of :math:`X`: :math:`X^{+}`.
    """
    for i, (left, right) in enumerate(fds):
        if left.issubset(attributes):
            return closure(attributes.union(right), fds[:i] + fds[i + 1:])
    return attributes


def fd_projection(attributes: Set[A],
                  fds: List[FunctionalDependency]) -> \
        Iterator[FunctionalDependency]:
    r"""Project of functional dependencies
    
    For :math:`X \to B`, where :math:`X \subset S` to hold, :math:`B`
    conditions must meet following conditions
    
    .. math::
       B \in S \\
       B \in \{X\}^{+} \\
       B \notin X
    
    These conditions become
    
    .. math::
       B \in S \cap (\{X\}^{+} \ X) 
    
    Args:
        attributes: :math:`S` 
        fds: :math:`F`

    Yields:
        FD:
    """
    for x in powerset(attributes):
        for b in attributes.intersection(closure(x, fds) - x):
            yield FunctionalDependency(x, {b})


def decompose_bcnf_tree(root: Node, fds: List[FunctionalDependency]) -> Node:
    r"""Decompose relation to BCNF

    Args:
        root: 
        fds: List of functional dependencies of relation

    Returns:
        Node: Root node
    """
    def _decompose_bcnf_tree(node, fds):
        # Check if we are violating BCNF for any functional dependency in fds
        relation = node.value
        for x, y in fds:
            _closure = closure(x, fds)
            _is_superkey = _closure == relation.attributes

            if not _is_superkey:  # Do we violate BCNF?
                # Partitions of relation
                r1 = _closure
                r2 = (relation.attributes - _closure).union(x)

                # Compute functional dependencies of partitioned dependencies
                fd1 = list(fd_projection(r1, fds))
                fd2 = list(fd_projection(r2, fds))

                node.left = Node(Relation(relation.name + '1', r1),
                                 node.depth + 1)
                node.right = Node(Relation(relation.name + '2', r2),
                                  node.depth + 1)

                _decompose_bcnf_tree(node.left, fd1)
                _decompose_bcnf_tree(node.right, fd2)

    _decompose_bcnf_tree(root, fds)
    return root
