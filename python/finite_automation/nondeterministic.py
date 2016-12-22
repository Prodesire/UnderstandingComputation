# coding: utf-8
from itertools import chain
from deterministic import FARule


class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, states, character):
        return set(chain(*[self.follow_rules_for(state, character)
                         for state in states]))

    def follow_rules_for(self, state, character):
        return [rule.follow() for rule in self.rules
                if rule.applies_to(state, character)]

    def follow_free_moves(self, states):
        more_states = self.next_state(states, None)
        if more_states < states:
            return states
        return set(self.follow_free_moves(more_states | states))


class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return bool(self.get_current_states() & self.accept_states)

    def get_current_states(self):
        return self.rulebook.follow_free_moves(self.current_states)

    def read_character(self, character):
        self.current_states = self.rulebook.next_state(self.get_current_states(), character)

    def read_string(self, string):
        for c in string:
            self.read_character(c)


class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string):
        nfa = NFA({self.start_state}, self.accept_states, self.rulebook)
        nfa.read_string(string)
        return nfa.accepting()


# rulebook = NFARulebook([
#     FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
#     FARule(2, 'a', 3), FARule(2, 'b', 3),
#     FARule(3, 'a', 4), FARule(3, 'b', 4)
# ])

# # Test NFA
# nfa = NFA(1, {4}, rulebook)
# nfa.read_string('bbbbb')
# print nfa.accepting()
#
# # Test NFADesign
# nfa_design = NFADesign(1, {4}, rulebook)
# print nfa_design.accepts('bab')
# print nfa_design.accepts('bbbbb')
# print nfa_design.accepts('bbabb')


# Test NFA with free move
rulebook = NFARulebook([
    FARule(1, None, 2), FARule(1, None, 4),
    FARule(2, 'a', 3),
    FARule(3, 'a', 2),
    FARule(4, 'a', 5),
    FARule(5, 'a', 6),
    FARule(6, 'a', 4),
])
nfa_design = NFADesign(1, {2, 4}, rulebook)
print nfa_design.accepts('aa')
print nfa_design.accepts('aaa')
print nfa_design.accepts('aaaaa')
print nfa_design.accepts('aaaaaa')
