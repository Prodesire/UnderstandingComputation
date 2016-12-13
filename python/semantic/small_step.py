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


class Varible(object):
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
            return DoNothing(), env.update({self.name: self.expr})


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


statement = Assign('x', Add(Varible('x'), Number(1)))
env = {'x': Number(3)}
Machine(statement, env).run()
