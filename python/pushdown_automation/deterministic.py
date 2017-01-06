# coding: utf-8


class Stack(object):
    def __init__(self, contents):
        self.contents = contents

    def push(self, character):
        return Stack(self.contents + [character])

    def pop(self):
        self.contents.pop()
        return Stack(self.contents)

    def top(self):
        return self.contents[-1] if len(self.contents) > 0 else ''

    def __repr__(self):
        return '#<Stack> ({0}){1}'.format(self.top(), ''.join(self.contents[-2::-1]))


class PDAConfiguration(object):
    STUCK_STATE = None

    def __init__(self, state, stack):
        self.state = state
        self.stack = stack

    def stuck(self):
        return PDAConfiguration(self.STUCK_STATE, self.stack)

    def is_stuck(self):
        return self.state == self.STUCK_STATE

    def __repr__(self):
        return '#<Configuration> state={0}, stack={1}'.format(self.state, self.stack)


class PDARule(object):
    def __init__(self, state, character, next_state,
                 pop_character, push_characters):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.pop_character = pop_character
        self.push_characters = push_characters

    def applies_to(self, configuration, character):
        return self.state == configuration.state and \
            self.pop_character == configuration.stack.top() and \
            self.character == character

    def follow(self, configuration):
        return PDAConfiguration(self.next_state, self.next_stack(configuration))

    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop()

        for character in self.push_characters:
            popped_stack = popped_stack.push(character)
        return popped_stack


class DPDARuleBook(object):
    def __init__(self, rules):
        self.rules = rules

    def applies_to(self, configuration, character):
        return bool(self.rule_for(configuration, character))

    def follow_free_moves(self, configuration):
        if self.applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(configuration, None))
        else:
            return configuration

    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)

    def rule_for(self, configuration, character):
        for rule in self.rules:
            if rule.applies_to(configuration, character):
                return rule


class DPDA(object):
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook

    def acceptting(self):
        return self.current_configuration_().state in self.accept_states

    def current_configuration_(self):
        return self.rulebook.follow_free_moves(self.current_configuration)

    def next_configuration(self, character):
        if self.rulebook.applies_to(self.current_configuration_(), character):
            print 1
            return self.rulebook.next_configuration(self.current_configuration_(), character)
        else:
            print 2
            return self.current_configuration_().stuck()

    def is_stuck(self):
        return self.current_configuration_().is_stuck()

    def read_character(self, character):
        self.current_configuration = self.next_configuration(character)

    def read_string(self, string):
        print '-------------'
        for character in string:
            if self.is_stuck():
                break
            print self.current_configuration_()
            print character
            self.read_character(character)


class DPDADesign(object):
    def __init__(self, start_state, bottom_character,
                 accept_states, rulebook):
        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string):
        dpda = self.to_dpda()
        dpda.read_string(string)
        return dpda.acceptting()

    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_configuration, self.accept_states, self.rulebook)


# todo result still not right
rulebook = DPDARuleBook([
    PDARule(1, '(', 2, '$', ['$', 'b']),
    PDARule(2, '(', 2, 'b', ['b', 'b']),
    PDARule(2, ')', 2, 'b', []),
    PDARule(2, None, 1, '$', ['$'])
])
dpda_design = DPDADesign(1, '$', [1], rulebook)
print dpda_design.accepts('(()')
print dpda_design.accepts('()(()())')
print dpda_design.accepts('())')
