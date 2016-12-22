require('set')
load('deterministic.rb')


class NFARulebook < Struct.new(:rules)
  def next_state(states, character)
    states.flat_map { |state| follow_rules_for(state, character) }.to_set()
  end

  def follow_rules_for(state, character)
    rules_for(state, character).map(&:follow)
  end

  def follow_free_moves(states)
    more_states = next_state(states, nil)

    if more_states.subset?(states)
      states
    else
      follow_free_moves(states + more_states)
    end
  end

  def rules_for(state, character)
    rules.select { |rule| rule.applies_to?(state, character) }
  end
end


class NFA < Struct.new(:current_states, :accept_states, :rulebook)
  def accepting?
    (current_states & accept_states).any?
  end

  def current_states
    rulebook.follow_free_moves(super)
  end

  def read_character(character)
    self.current_states = rulebook.next_state(current_states, character)
  end

  def read_string(string)
    string.chars.each do |character|
      read_character(character)
    end
  end
end


class NFADesign < Struct.new(:start_state, :accept_states, :rulebook)
  def accepts?(string)
    to_nfa.tap { |nfa| nfa.read_string(string) }.accepting?
  end

  def to_nfa
    NFA.new(Set[start_state], accept_states, rulebook)
  end
end


# rulebook = NFARulebook.new([
#     FARule.new(1, 'a', 1), FARule.new(1, 'b', 1), FARule.new(1, 'b', 2),
#     FARule.new(2, 'a', 3), FARule.new(2, 'b', 3),
#     FARule.new(3, 'a', 4), FARule.new(3, 'b', 4)
# ])
#
# # Test NFA
# nfa = NFA.new(Set[1], [4], rulebook)
# nfa.read_string('bbbbb')
# puts nfa.accepting?
#
# # Test NFADesign
# nfa_design = NFADesign.new(1, [4], rulebook)
# puts nfa_design.accepts?('bab')
# puts nfa_design.accepts?('bbbbb')
# puts nfa_design.accepts?('bbabb')


# Test NFA with free move
rulebook = NFARulebook.new([
    FARule.new(1, nil, 2), FARule.new(1, nil, 4),
    FARule.new(2, 'a', 3),
    FARule.new(3, 'a', 2),
    FARule.new(4, 'a', 5),
    FARule.new(5, 'a', 6),
    FARule.new(6, 'a', 4),
])
nfa_design = NFADesign.new(1, [2, 4], rulebook)
puts nfa_design.accepts?('aa')
puts nfa_design.accepts?('aaa')
puts nfa_design.accepts?('aaaaa')
puts nfa_design.accepts?('aaaaaa')
