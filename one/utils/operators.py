import operator

OPERATORS = {
    '<': operator.__lt__,
    '<=': operator.__le__,
    '=': operator.__eq__,
    '>': operator.__gt__,
    '>=': operator.__ge__,
    '!=': operator.__ne__
}
