from collections import defaultdict
from itertools import chain, combinations

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  
        self.start_state = start_state
        self.final_states = final_states

    def is_deterministic(self):
        """Check if the FA is deterministic (DFA)."""
        for state, paths in self.transitions.items():
            for symbol in self.alphabet:
                if len(paths[symbol]) > 1:
                    return False  
        return True

    def to_regular_grammar(self):
        """Convert FA to Regular Grammar."""
        grammar = defaultdict(list)
        for state, paths in self.transitions.items():
            for symbol, next_states in paths.items():
                for next_state in next_states:
                    rule = f"{symbol}{next_state}" if next_state else symbol
                    grammar[state].append(rule)
        return grammar

    def ndfa_to_dfa(self):
        """Convert an NDFA to DFA."""
        dfa_states = {}
        queue = [frozenset([self.start_state])]
        new_transitions = {}
        new_final_states = set()
        
        while queue:
            current_set = queue.pop(0)
            state_name = ''.join(sorted(current_set))  
            dfa_states[current_set] = state_name
            new_transitions[state_name] = {symbol: set() for symbol in self.alphabet}
            
            for state in current_set:
                if state in self.final_states:
                    new_final_states.add(state_name)
                for symbol in self.alphabet:
                    new_transitions[state_name][symbol] |= set(self.transitions[state][symbol])
            
            for new_state in new_transitions[state_name].values():
                if new_state and frozenset(new_state) not in dfa_states:
                    queue.append(frozenset(new_state))
        
        return FiniteAutomaton(set(dfa_states.values()), self.alphabet, new_transitions, dfa_states[frozenset([self.start_state])], new_final_states)

# Given finite automaton
states = {"q0", "q1", "q2", "q3", "q4"}
alphabet = {"a", "b", "c"}
transitions = {
    "q0": {"a": {"q1"}, "b": set(), "c": set()},
    "q1": {"b": {"q2", "q3"}, "a": set(), "c": set()},
    "q2": {"b": set(), "a": set(), "c": {"q0"}},
    "q3": {"a": {"q4"}, "b": {"q0"}, "c": set()},
    "q4": {"a": set(), "b": set(), "c": set()}
}
start_state = "q0"
final_states = {"q4"}

fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

print("Deterministic:", fa.is_deterministic())

grammar = fa.to_regular_grammar()
print("Regular Grammar:")
for state, rules in grammar.items():
    print(f"{state} -> {' | '.join(rules)}")

if not fa.is_deterministic():
    dfa = fa.ndfa_to_dfa()
    print("\nConverted DFA:")
    print("States:", dfa.states)
    print("Final States:", dfa.final_states)
    print("Transitions:")
    for state, paths in dfa.transitions.items():
        for symbol, next_state in paths.items():
            print(f"δ({state}, {symbol}) = {next_state}")
            #hi