require('treetop')


Treetop.load('pattern')
parse_tree = PatternParser.new.parse('(a(|b))*')

# # Test small step with grammar parser
# load('pattern.rb')
# pattern = parse_tree.to_ast
# puts pattern.matches?('abaab')
# puts pattern.matches?('abba')