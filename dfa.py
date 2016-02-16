#!/usr/bin/env python3

import automaton


class DFA(automaton.Automaton):
    """a deterministic finite automaton"""

    def validate_automaton(self):
        """returns True if this DFA is internally consistent;
        raises the appropriate exception if this DFA is invalid"""

        for state in self.states:
            if state not in self.transitions:
                raise automaton.MissingStateError(
                    'state {} is missing from transition function'.format(
                        state))

        for start_state, paths in self.transitions.items():

            missing_symbols = self.symbols.difference(set(paths.keys()))
            if missing_symbols:
                raise automaton.MissingSymbolError(
                    'state {} is missing transitions for symbols ({})'.format(
                        start_state, ', '.join(missing_symbols)))

            invalid_states = set(paths.values()).difference(self.states)
            if invalid_states:
                raise automaton.InvalidStateError(
                    'states are not valid ({})'.format(
                        ', '.join(invalid_states)))

        if self.initial_state not in self.states:
            raise automaton.InvalidStateError(
                '{} is not a valid state'.format(self.initial_state))

        for state in self.final_states:
            if state not in self.states:
                raise automaton.InvalidStateError(
                    '{} is not a valid state'.format(state))

        return True

    def validate_input(self, input_str):
        """returns True if the given string is accepted by this DFA;
        raises the appropriate exception if the string is not accepted"""

        current_state = self.initial_state

        for symbol in input_str:
            if symbol not in self.symbols:
                raise automaton.InvalidSymbolError(
                    '{} is not a valid symbol'.format(symbol))
            current_state = self.transitions[current_state][symbol]

        if current_state not in self.final_states:
            raise automaton.FinalStateError(
                'the automaton stopped on a non-final state')

        return True
