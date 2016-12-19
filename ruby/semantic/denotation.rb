

class Number < Struct.new(:value)
  def to_s
    "#{value}"
  end

  def inspect
    "<<#{self}>>"
  end

  def to_ruby
    "-> e { #{value.to_s} }"
  end
end


class Add < Struct.new(:left, :right)
  def to_s
    "#{left}+#{right}"
  end

  def to_ruby
    "-> e { (#{left.to_ruby}).call(e) + (#{right.to_ruby}).call(e) }"
  end
end


class Multiply < Struct.new(:left, :right)
  def to_s
    "#{left}*#{right}"
  end

  def to_ruby
    "-> e { (#{left.to_ruby}).call(e) * (#{right.to_ruby}).call(e) }"
  end
end


class Boolean < Struct.new(:value)
  def to_s
    value.to_s
  end

  def inspect
    "<<#{self}>>"
  end

  def to_ruby
    "-> e { #{value.to_s} }"
  end
end


class LessThan < Struct.new(:left, :right)
  def to_s
    "#{left} < #{right}"
  end

  def to_ruby
    "-> e { (#{left.to_ruby}).call(e) < (#{right.to_ruby}).call(e) }"
  end
end


class Variable < Struct.new(:name)
  def to_s
    name.to_s
  end

  def to_ruby
    "-> e { e[#{name.inspect}] }"
  end
end


class DoNothing
  def to_s
    'do_nothing'
  end

  def to_ruby
    "-> e { e }"
  end
end


class Assign < Struct.new(:name, :expr)
  def to_s
    "#{name} = #{expr}"
  end

  def to_ruby
    "-> e { e.merge({ #{name.inspect} => (#{expr.to_ruby}).call(e) }) }"
  end
end


class If < Struct.new(:condition, :consequence, :alternative)
  def to_s
    "if (#{condition}) { #{consequence} } else { #{alternative} }"
  end

  def to_ruby
    "-> e { if (#{condition.to_ruby}).call(e) " +
        "then (#{consequence.to_ruby}).call(e) " +
        "else (#{alternative.to_ruby}).call(e) "+
        "end }"
  end
end


class Sequence < Struct.new(:first, :second)
  def to_s
    "#{first}; #{second}"
  end

  def to_ruby
    "-> e { (#{second.to_ruby}).call( (#{first.to_ruby}).call(e) ) }"
  end
end


class While < Struct.new(:condition, :body)
  def to_s
    "while (#{condition}) { #{body} }"
  end

  def to_ruby
    "-> e { "+
        "while (#{condition.to_ruby}).call(e); e = (#{body.to_ruby}).call(e); end; " +
        "e }"
  end
end


# Test "Number"
ruby = Number.new(23).to_ruby
puts ruby, eval(ruby).call({})

# Test "Boolean"
ruby = Boolean.new(true).to_ruby
puts ruby, eval(ruby).call({})

# Test "Variable"
ruby = Variable.new(:x).to_ruby
puts ruby, eval(ruby).call({x: 7})

# Test "Add", "Multiply", "LessThan"
ruby = LessThan.new(Add.new(Variable.new(:x), Number.new(2)),
                    Multiply.new(Variable.new(:y), Number.new(1))).to_ruby
puts ruby, eval(ruby).call({x: 1, y: 3})

# Test "Assign"
ruby = Assign.new(:y, Add.new(Variable.new(:x), Number.new(1))).to_ruby
puts ruby, eval(ruby).call({x: 3})

# Test "If"
ruby = If.new(Variable.new(:x),
              Assign.new(:y, Number.new(1)),
              DoNothing.new).to_ruby
puts ruby, eval(ruby).call({x: true})

# Test "Sequence"
ruby = Sequence.new(Assign.new(:y, Number.new(1)),
                    Assign.new(:z, Number.new(2))).to_ruby
puts ruby, eval(ruby).call({})

# Test "While"
ruby = While.new(LessThan.new(Variable.new(:x), Number.new(6)),
                 Assign.new(:x, Multiply.new(Variable.new(:x), Number.new(2)))).to_ruby
puts ruby, eval(ruby).call({x: 1})
