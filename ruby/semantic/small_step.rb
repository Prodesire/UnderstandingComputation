

class Number < Struct.new(:value)
  def to_s
    "#{value}"
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


class Varible < Struct.new(:name)
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


statement = Assign.new(:x, Add.new(Varible.new(:x), Number.new(1)))
env = {x: Number.new(3)}
Machine.new(statement, env).run
