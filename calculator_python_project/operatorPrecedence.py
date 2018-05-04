class OperatorPrecedence(object):
    def __init__(self, operator, precedence):
        self._operator = operator
        self._precedence = precedence

    @property
    def precedence(self):
        return self._precedence

    @property
    def operator(self):
        return self._operator

    def __call__(self, *args):
        return self.operator(*args)

    @property
    def __hash__(self):
        return hash(str(self.operator))

    def __eq__(self, other):
        return other.precedence == self.precedence

    def __str__(self):
        return self.operator

    def __le__(self, other):
        return self.precedence <= other.precedence
