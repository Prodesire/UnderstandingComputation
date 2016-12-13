

class Number < Struct.new(:value)
  def to_s
    "#{value}"
  end
end

class Add < Struct.new(:left, :right)
  def to_s
    "#{left}+#{right}"
  end
end

class Multiply < Struct.new(:left, :right)
  def to_s
    "#{left}*#{right}"
  end
end

print Add.new(
    Multiply.new(Number.new(2), Number.new(3)),
    Multiply.new(Number.new(4), Number.new(5))
    )
