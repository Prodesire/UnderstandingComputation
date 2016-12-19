# coding: utf-8
import marshal, types


class Number(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def to_python(self):
        return 'lambda e: {}'.format(self.value)


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} + {1}'.format(self.left, self.right)

    def to_python(self):
        return 'lambda e: ({0})(e) + ({1})(e)'.format(
            self.left.to_python(), self.right.to_python()
        )


class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} * {1}'.format(self.left, self.right)

    def to_python(self):
        return 'lambda e: ({0})(e) * ({1})(e)'.format(
            self.left.to_python(), self.right.to_python()
        )


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def to_python(self):
        return 'lambda e: {}'.format(self.value)


class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} < {1}'.format(self.left, self.right)

    def to_python(self):
        return 'lambda e: ({0})(e) < ({1})(e)'.format(
            self.left.to_python(), self.right.to_python()
        )


class Variable(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def to_python(self):
        return 'lambda e: e["{}"]'.format(self.name)


class DoNothing(object):
    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

    def __repr__(self):
        return 'do_nothing'

    def to_python(self):
        return 'lambda e: e'


class Assign(object):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return '{0} = {1}'.format(self.name, self.expr)

    def to_python(self):
        return 'lambda e: e.update({{ "{0}": ({1})(e) }}) or e'.format(
            self.name, self.expr.to_python()
        )


class If(object):
    def __init__(self, condition, sequence, alternative):
        self.condition = condition
        self.sequence = sequence
        self.alternative = alternative

    def __repr__(self):
        return 'If ({0}) {{ {1} }} else {{ {2} }}'.format(
            self.condition, self.sequence, self.alternative
        )

    def to_python(self):
        return 'lambda e: ({0})(e) if ({1})(e) else ({2})(e)'.format(
            self.sequence.to_python(),
            self.condition.to_python(),
            self.alternative.to_python()
        )


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return '{0}; {1}'.format(self.first, self.second)

    def to_python(self):
        return 'lambda e: ({0})( ({1})(e) )'.format(
            self.second.to_python(), self.first.to_python()
        )


class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'while ({0}) {{ {1} }}'.format(self.condition, self.body)

    def to_python_loop(self):
        exec('def loop(e):\n'
             '    while ({0})(e):\n'
             '        e = ({1})(e)\n'
             '    return e'.format(self.condition.to_python(), self.body.to_python()))
        return loop


# Test "Number"
python = Number(23).to_python()
print python
print eval(python)({})

# Test "Boolean"
python = Boolean(True).to_python()
print python
print eval(python)({})

# Test "Variable"
python = Variable('x').to_python()
print python
print eval(python)({'x': 7})

# Test "Add", "Multiply", "LessThan"
python = LessThan(Add(Variable('x'), Number(2)),
                  Multiply(Variable('y'), Number(1))).to_python()
print python
print eval(python)({'x': 1, 'y': 3})

# Test "Assign"
python = Assign('y', Add(Variable('x'), Number(1))).to_python()
print python
print eval(python)({'x': 3})

# Test "If"
python = If(Variable('x'),
            Assign('y', Number(1)),
            DoNothing()).to_python()
print python
print eval(python)({'x': True})

# Test "Sequence"
python = Sequence(Assign('y', Number(1)),
                  Assign('z', Number(2))).to_python()
print python
print eval(python)({})

# Test "While"
python_loop = While(LessThan(Variable('x'), Number(6)),
               Assign('x', Multiply(Variable('x'), Number(2)))).to_python_loop()
print python_loop
print python_loop({'x': 1})
