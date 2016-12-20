

class Number < Struct.new(:value)
  def to_s
    "#{value}"
  end

  def inspect
    "<<#{self}>>"
  end

  def eval(env)
    self
  end
end


class Add < Struct.new(:left, :right)
  def to_s
    "#{left}+#{right}"
  end

  def eval(env)
    Number.new(left.eval(env).value + right.eval(env).value)
  end
end


class Multiply < Struct.new(:left, :right)
  def to_s
    "#{left}*#{right}"
  end

  def eval(env)
    Number.new(left.eval(env).value * right.eval(env).value)
  end
end


class Boolean < Struct.new(:value)
  def to_s
    value.to_s
  end

  def inspect
    "<<#{self}>>"
  end

  def eval(env)
    self
  end
end


class LessThan < Struct.new(:left, :right)
  def to_s
    "#{left} < #{right}"
  end

  def eval(env)
    Boolean.new(left.eval(env).value < right.eval(env).value)
  end
end


class Variable < Struct.new(:name)
  def to_s
    name.to_s
  end

  def eval(env)
    env[name]
  end
end


class DoNothing
  def to_s
    'do_nothing'
  end

  def eval(env)
    env
  end
end


class Assign < Struct.new(:name, :expr)
  def to_s
    "#{name} = #{expr}"
  end

  def eval(env)
    env.merge({name => expr.eval(env)})
  end
end


class If < Struct.new(:condition, :consequence, :alternative)
  def to_s
    "if (#{condition}) { #{consequence} } else { #{alternative} }"
  end

  def eval(env)
    case condition.eval(env)
      when Boolean.new(true)
        consequence.eval(env)
      when Boolean.new(false)
        alternative.eval(env)
    end
  end
end


class Sequence < Struct.new(:first, :second)
  def to_s
    "#{first}; #{second}"
  end

  def eval(env)
    second.eval(first.eval(env))
  end
end


class While < Struct.new(:condition, :body)
  def to_s
    "while (#{condition}) { #{body} }"
  end

  def eval(env)
    case condition.eval(env)
      when Boolean.new(true)
        eval(body.eval(env))
      when Boolean.new(false)
        env
    end
  end
end


# # Test "Number"
# puts Number.new(23).eval({})
#
# # Test "Variable"
# puts Variable.new(:x).eval({x: Number.new(3)})
#
# # Test "Add", "LessThan"
# puts LessThan.new(Add.new(Variable.new(:x), Number.new(2)),
#                   Variable.new(:y)
#                   ).eval({x: Number.new(1), y: Number.new(5)})
#
# # Test "Sequence"
# puts Sequence.new(Assign.new(:y, Number.new(1)),
#                   Assign.new(:z, Number.new(2))).eval({})
#
# # Test "If"
# puts If.new(Variable.new(:x),
#             Sequence.new(Assign.new(:y, Number.new(1)),
#                          Assign.new(:z, Number.new(2))),
#             DoNothing.new
#             ).eval({x: Boolean.new(true)})
#
# # Test "While"
# puts While.new(LessThan.new(Variable.new(:x), Number.new(6)),
#                Assign.new(:x, Multiply.new(Variable.new(:x), Number.new(2)))
#                ).eval({x: Number.new(1)})
