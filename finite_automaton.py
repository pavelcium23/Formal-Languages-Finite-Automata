import random

class Grammar:
    def __init__(self):
        self.non_terminals = {"S", "B", "D", "Q"}
        self.terminals = {"a", "b", "c", "d"}
        self.start_symbol = "S"
        self.productions = {
            "S": ["aB", "bB"],
            "B": ["cD"],
            "D": ["dQ", "a"],
            "Q": ["bB", "dQ"]
        }
    
    def generate_string(self):
        current_string = self.start_symbol
        while any(symbol in self.non_terminals for symbol in current_string):
            for nt in self.non_terminals:
                if nt in current_string:
                    production = random.choice(self.productions[nt])
                    current_string = current_string.replace(nt, production, 1)
        return current_string
    
    def generate_multiple_strings(self, count=5):
        return [self.generate_string() for _ in range(count)]
    
    def to_finite_automaton(self):
        states = {"S", "B", "D", "Q"}
        alphabet = self.terminals
        transitions = {
            ("S", "a"): "B",
            ("S", "b"): "B",
            ("B", "c"): "D",
            ("D", "d"): "Q",
            ("D", "a"): "ACCEPT",
            ("Q", "b"): "B",
            ("Q", "d"): "Q"
        }
        start_state = "S"
        accept_states = {"ACCEPT"} 
        return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
    
    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.accept_states

grammar = Grammar()
generated_strings = grammar.generate_multiple_strings()
print("Generated Strings:", generated_strings)
fa = grammar.to_finite_automaton()

for generated_string in generated_strings:
    print(f"String '{generated_string}' belongs to language:", fa.string_belongs_to_language(generated_string))

more_tests = ["acda", "bd", "acd", "acddb"] 
for test_string in more_tests:
    print(f"String '{test_string}' belongs to language:", fa.string_belongs_to_language(test_string))
