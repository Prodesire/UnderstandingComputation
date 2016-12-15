# coding: utf-8


class Number(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def eval(self, env):
        return self


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} + {1}'.format(self.left, self.right)

    def eval(self, env):
        return Number(self.left.eval(env).value + self.right.eval(env).value)


class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} * {1}'.format(self.left, self.right)

    def eval(self, env):
        return Number(self.left.eval(env).value * self.right.eval(env).value)


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def eval(self):
        return self


class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} < {1}'.format(self.left, self.right)

    def eval(self, env):
        return Boolean(self.left.eval(env).value < self.right.eval(env).value)


class Variable(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def eval(self, env):
        return env[self.name]


class DoNothing(object):
    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

    def __repr__(self):
        return 'do_nothing'

    def eval(self, env):
        return env


class Assign(object):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return '{0} = {1}'.format(self.name, self.expr)

    def eval(self, env):
        env.update({self.name: self.expr.eval(env)})
        return env


class If(object):
    def __init__(self, condition, sequence, alternative):
        self.condition = condition
        self.sequence = sequence
        self.alternative = alternative

    def __repr__(self):
        return 'If ({0}) {{ {1} }} else {{ {2} }}'.format(
            self.condition, self.sequence, self.alternative
        )

    def eval(self, env):
        if self.condition.eval(env).value == Boolean(True).value:
            return self.sequence.eval(env)
        return self.alternative.eval(env)


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return '{0}; {1}'.format(self.first, self.second)

    def eval(self, env):
        return self.second.eval(self.first.eval(env))


class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'while ({0}) {{ {1} }}'.format(self.condition, self.body)

    def eval(self, env):
        if self.condition.eval(env).value == Boolean(True).value:
            return self.eval(self.body.eval(env))
        return env


# Test "Number"
print Number(23).eval({})

# Test "Variable"
print Variable('x').eval({'x': Number(3)})


# Test "Add", "LessThan"
print LessThan(Add(Variable('x'), Number(2)),
               Variable('y')
               ).eval({'x': Number(1), 'y': Number(5)})

# Test "Sequence"
print Sequence(Assign('y', Number(1)),
                  Assign('z', Number(2))).eval({})

# Test "If"
print If(Variable('x'),
            Sequence(Assign('y', Number(1)),
                         Assign('z', Number(2))),
            DoNothing
            ).eval({'x': Boolean(True)})

# Test "While"
print While(LessThan(Variable('x'), Number(6)),
               Assign('x', Multiply(Variable('x'), Number(2)))
               ).eval({'x': Number(1)})


## Test "If", "Sequence", "Assign"
# statement = If(Variable('x'),
#                Sequence(Assign('y', Number(1)),
#                         Assign('z', Number(2))),
#                DoNothing())
# env = {'x': Boolean(True)}

## Test "While"
# statement = While(LessThan(Variable('x'), Number(6)),
#                   Assign('x', Multiply(Variable('x'), Number(2))))
# env = {'x': Number(1)}
