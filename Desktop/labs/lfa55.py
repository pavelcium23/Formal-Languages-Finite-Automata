from typing import Set, Dict, List, Tuple
from copy import deepcopy


class CFG:
    def __init__(self, non_terminals: Set[str], terminals: Set[str], start_symbol: str, productions: Dict[str, List[str]]):
        self.VN = non_terminals
        self.VT = terminals
        self.S = start_symbol
        self.P = productions

    def eliminate_epsilon_productions(self):
        nullable = {nt for nt, rules in self.P.items() if 'ε' in rules}
        while True:
            new_nullable = nullable.copy()
            for nt, rules in self.P.items():
                if any(all(sym in nullable for sym in rule) for rule in rules if rule != 'ε'):
                    new_nullable.add(nt)
            if new_nullable == nullable:
                break
            nullable = new_nullable

        new_productions = {}
        for nt, rules in self.P.items():
            new_rules = set()
            for rule in rules:
                positions = [i for i, sym in enumerate(rule) if sym in nullable]
                n = len(positions)
                for i in range(2 ** n):
                    temp_rule = list(rule)
                    for j in range(n):
                        if (i >> j) & 1:
                            temp_rule[positions[j]] = ''
                    candidate = ''.join(temp_rule)
                    if candidate:
                        new_rules.add(candidate)
            new_productions[nt] = list(new_rules)
        self.P = new_productions

    def eliminate_renaming(self):
        rename_sets = {nt: {nt} for nt in self.VN}
        changed = True
        while changed:
            changed = False
            for nt in self.VN:
                for rule in self.P[nt]:
                    if rule in self.VN and rule not in rename_sets[nt]:
                        rename_sets[nt].add(rule)
                        changed = True

        new_productions = {nt: [] for nt in self.VN}
        for nt in self.VN:
            for target in rename_sets[nt]:
                new_productions[nt].extend([rule for rule in self.P[target] if rule not in self.VN])
        self.P = new_productions

    def eliminate_inaccessible_symbols(self):
        accessible = {self.S}
        changed = True
        while changed:
            changed = False
            for nt in list(accessible):
                for rule in self.P.get(nt, []):
                    for sym in rule:
                        if sym in self.VN and sym not in accessible:
                            accessible.add(sym)
                            changed = True
        self.VN = accessible
        self.P = {nt: rules for nt, rules in self.P.items() if nt in accessible}

    def eliminate_non_productive_symbols(self):
        productive = set()
        while True:
            new_productive = productive.copy()
            for nt, rules in self.P.items():
                if any(all(sym in self.VT or sym in productive for sym in rule) for rule in rules):
                    new_productive.add(nt)
            if new_productive == productive:
                break
            productive = new_productive

        self.VN = productive
        self.P = {nt: [rule for rule in rules if all(sym in self.VT or sym in productive for sym in rule)]
                  for nt, rules in self.P.items() if nt in productive}

    def convert_to_cnf(self):
        new_productions = {}
        term_map = {}

        def get_new_non_terminal(symbol):
            if symbol not in term_map:
                new_symbol = f"{symbol.upper()}_"
                i = 1
                while new_symbol + str(i) in self.VN:
                    i += 1
                new_nt = new_symbol + str(i)
                self.VN.add(new_nt)
                term_map[symbol] = new_nt
                new_productions[new_nt] = [symbol]
            return term_map[symbol]

        for nt, rules in self.P.items():
            new_rules = []
            for rule in rules:
                if len(rule) == 1 and rule in self.VT:
                    new_rules.append(rule)
                else:
                    temp_rule = ''
                    for sym in rule:
                        if sym in self.VT:
                            temp_rule += get_new_non_terminal(sym)
                        else:
                            temp_rule += sym
                    while len(temp_rule) > 2:
                        new_nt = f"N{len(self.VN)}"
                        self.VN.add(new_nt)
                        new_productions[new_nt] = [temp_rule[:2]]
                        temp_rule = new_nt + temp_rule[2:]
                    new_rules.append(temp_rule)
            new_productions[nt] = new_rules
        self.P = new_productions

    def to_cnf(self):
        self.eliminate_epsilon_productions()
        self.eliminate_renaming()
        self.eliminate_inaccessible_symbols()
        self.eliminate_non_productive_symbols()
        self.convert_to_cnf()

    def print_grammar(self):
        print(f"Non-terminals: {self.VN}")
        print(f"Terminals: {self.VT}")
        print(f"Start Symbol: {self.S}")
        print("Productions:")
        for nt, rules in self.P.items():
            print(f"  {nt} → {', '.join(rules)}")


#Variant 9 Grammar from Image
VN = {'S', 'A', 'B', 'C', 'D'}
VT = {'a', 'b'}
S = 'S'
P = {
    'S': ['bA', 'BC'],
    'A': ['a', 'aS', 'bAaAb'],
    'B': ['A', 'bS', 'aAa'],
    'C': ['ε', 'AB'],
    'D': ['AB']
}

grammar = CFG(VN, VT, S, P)
print("Original Grammar:")
grammar.print_grammar()

# Transform to CNF
grammar.to_cnf()

print("\nGrammar in CNF:")
grammar.print_grammar()
