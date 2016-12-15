# coding: utf-8


class Number(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def reducible(self):
        return False


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} + {1}'.format(self.left, self.right)

    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible():
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value + self.right.value)


class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} * {1}'.format(self.left, self.right)

    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible():
            return Multiply(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value * self.right.value)


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def reducible(self):
        return False


class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{0} < {1}'.format(self.left, self.right)

    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible():
            return LessThan(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value < self.right.value)


class Variable(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def reducible(self):
        return True

    def reduce(self, env):
        return env[self.name]


class DoNothing(object):
    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

    def __repr__(self):
        return 'do_nothing'

    def reducible(self):
        return False


class Assign(object):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return '{0} = {1}'.format(self.name, self.expr)

    def reducible(self):
        return True

    def reduce(self, env):
        if self.expr.reducible():
            return Assign(self.name, self.expr.reduce(env)), env
        else:
            env.update({self.name: self.expr})
            return DoNothing(), env


class If(object):
    def __init__(self, condition, sequence, alternative):
        self.condition = condition
        self.sequence = sequence
        self.alternative = alternative

    def __repr__(self):
        return 'If ({0}) {{ {1} }} else {{ {2} }}'.format(
            self.condition, self.sequence, self.alternative
        )

    def reducible(self):
        return True

    def reduce(self, env):
        if self.condition.reducible():
            return [If(self.condition.reduce(env), self.sequence, self.alternative), env]
        else:
            if self.condition.value == Boolean(True).value:
                return [self.sequence, env]
            else:
                return [self.alternative, env]


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return '{0}; {1}'.format(self.first, self.second)

    def reducible(self):
        return True

    def reduce(self, env):
        if isinstance(self.first, DoNothing):
            return self.second, env
        first, env = self.first.reduce(env)
        return Sequence(first, self.second), env


class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'while ({0}) {{ {1} }}'.format(self.condition, self.body)

    def reducible(self):
        return True

    def reduce(self, env):
        return If(self.condition, Sequence(self.body, self), DoNothing()), env


class Machine(object):
    def __init__(self, statement, env):
        self.statement = statement
        self.env = env

    def step(self):
        self.statement, self.env = self.statement.reduce(self.env)

    def run(self):
        while self.statement.reducible():
            print '{0}, {1}'.format(self.statement, self.env)
            self.step()
        print '{0}, {1}'.format(self.statement, self.env)


## Test "If", "Sequence", "Assign"
# statement = If(Variable('x'),
#                Sequence(Assign('y', Number(1)),
#                         Assign('z', Number(2))),
#                DoNothing())
# env = {'x': Boolean(True)}

## Test "While"
statement = While(LessThan(Variable('x'), Number(6)),
                  Assign('x', Multiply(Variable('x'), Number(2))))
env = {'x': Number(1)}

Machine(statement, env).run()
