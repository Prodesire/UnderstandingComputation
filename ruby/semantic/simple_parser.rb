require('treetop')


Treetop.load('simple')
parse_tree = SimpleParser.new.parse('while (x < 5) { x = x * 3 }')

# # Test small step with grammar parser
# load('small_step.rb')
# statement = parse_tree.to_ast
# Machine.new(statement, {x: Number.new(1)}).run

# # Test big step with grammar parser
# load('big_step.rb')
# statement = parse_tree.to_ast
# puts statement.eval({x: Number.new(1)})

# # Test denotation with grammar parser
# load('denotation.rb')
# statement = parse_tree.to_ast
# puts eval(statement.to_ruby).call({x: 1})
