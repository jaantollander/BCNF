from BCNF.BCNF import Relation, FunctionalDependency
from pyparsing import OneOrMore, alphanums, Word, ZeroOrMore, Suppress

__all__ = """
parse_relation
parse_functional_dependency
parse_functional_dependencies
""".split()


def parse_relation(string):
    """Parse relation
    
    >>> s = 'Courses(courseCode, courseName, credits, teacherID, teacherName)'
    >>> parse_relation(s)
    Relation(name='Courses', attributes={'courseCode', 'courseName', 'credits', 
             'teacherName', 'teacherID'})
    """
    word = Word(alphanums)
    csv = OneOrMore(Word(alphanums) + Suppress(ZeroOrMore(',')))
    csv.setParseAction(set)
    relation = word('name') + Suppress('(') + csv('attributes') + Suppress(')')

    result = relation.parseString(string)
    return Relation(**result)


def parse_functional_dependency(string):
    """Parse dependency
    
    >>> s = 'courseCode -> courseName credits teacherID' 
    >>> parse_functional_dependency(s)
    FunctionalDependency(X={'courseCode'}, Y={'teacherID', 'courseName', 'credits'})
    """
    attributes = OneOrMore(Word(alphanums))
    attributes.setParseAction(set)
    dependency = attributes('X') + Suppress('->') + attributes('Y')
    result = dependency.parseString(string)
    return FunctionalDependency(**result)


def parse_functional_dependencies(strings):
    """Parse dependencies
    
    >>> list(parse_functional_dependencies([
    >>> "courseCode -> courseName credits teacherID",
    >>> "teacherID -> teacherName"
    >>> ]))
    [FunctionalDependency(X={'courseCode'}, Y={'credits', 'teacherID', 'courseName'}),
     FunctionalDependency(X={'teacherID'}, Y={'teacherName'})]
    """
    _strings = strings.split('\n') if isinstance(strings, str) else strings
    return map(parse_functional_dependency, filter(len, _strings))
