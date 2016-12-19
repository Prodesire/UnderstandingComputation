

class Number < Struct.new(:value)
  def to_s
    "#{value}"
  end

  def inspect
    "<<#{self}>>"
  end

  def reducible?
    false
  end
end


class Add < Struct.new(:left, :right)
  def to_s
    "#{left}+#{right}"
  end

  def reducible?
    true
  end

  def reduce(env)
    if left.reducible?
      Add.new(left.reduce(env), right)
    elsif right.reducible?
      Add.new(left, right.reduce(env))
    else
      Number.new(left.value + right.value)
    end
  end
end


class Multiply < Struct.new(:left, :right)
  def to_s
    "#{left}*#{right}"
  end

  def reducible?
    true
  end

  def reduce(env)
    if left.reducible?
      Multiply.new(left.reduce(env), right)
    elsif right.reducible?
      Multiply.new(left, right.reduce(env))
    else
      Number.new(left.value * right.value)
    end
  end
end


class Boolean < Struct.new(:value)
  def to_s
    value.to_s
  end

  def inspect
    "<<#{self}>>"
  end

  def reducible?
    false
  end
end


class LessThan < Struct.new(:left, :right)
  def to_s
    "#{left} < #{right}"
  end

  def reducible?
    true
  end

  def reduce(env)
    if left.reducible?
      LessThan.new(left.reduce(env), right)
    elsif right.reducible?
      LessThan.new(left, right.reduce(env))
    else
      Boolean.new(left.value < right.value)
    end
  end
end


class Variable < Struct.new(:name)
  def to_s
    name.to_s
  end

  def reducible?
    true
  end

  def reduce(env)
    env[name]
  end
end


class DoNothing
  def to_s
    'do_nothing'
  end

  def ==(other_statement)
    other_statement.instance_of?(DoNothing)
  end

  def reducible?
    false
  end
end


class Assign < Struct.new(:name, :expr)
  def to_s
    "#{name} = #{expr}"
  end

  def reducible?
    true
  end

  def reduce(env)
    if expr.reducible?
      [Assign.new(name, expr.reduce(env)), env]
    else
      [DoNothing.new, env.merge({name => expr})]
    end
  end
end


class If < Struct.new(:condition, :consequence, :alternative)
  def to_s
    "if (#{condition}) { #{consequence} } else { #{alternative} }"
  end

  def reducible?
    true
  end

  def reduce(env)
    if condition.reducible?
      [If.new(condition.reduce(env), consequence, alternative), env]
    else
      case condition
        when Boolean.new(true)
          [consequence, env]
        when Boolean.new(false)
          [alternative, env]
      end
    end
  end
end


class Sequence < Struct.new(:first, :second)
  def to_s
    "#{first}; #{second}"
  end

  def reducible?
    true
  end

  def reduce(env)
    case first
      when DoNothing.new
        [second, env]
      else
        reduced_first, reduced_env = first.reduce(env)
        [Sequence.new(reduced_first, second), reduced_env]
    end
  end
end


class While < Struct.new(:condition, :body)
  def to_s
    "while (#{condition}) { #{body} }"
  end

  def reducible?
    true
  end

  def reduce(env)
    [If.new(condition, Sequence.new(body, self), DoNothing.new), env]
  end
end


class Machine < Struct.new(:statement, :env)
  def step
    self.statement, self.env = statement.reduce(env)
  end

  def run
    while statement.reducible?
      puts "#{statement}, #{env}"
      step
    end

    puts "#{statement}, #{env}"
  end
end


# Test "If", "Sequence", "Assign"
statement = If.new(Variable.new(:x),
                   Sequence.new(Assign.new(:y, Number.new(1)),
                                Assign.new(:z, Number.new(2))),
                   DoNothing.new)
env = {x: Boolean.new(true)}
Machine.new(statement, env).run

# Test "While"
statement = While.new(
                     LessThan.new(Variable.new(:x), Number.new(6)),
                     Assign.new(:x, Multiply.new(Variable.new(:x), Number.new(2)))
                     )
env = {x: Number.new(1)}

Machine.new(statement, env).run
