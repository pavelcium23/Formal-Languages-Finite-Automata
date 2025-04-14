import random
import re

MAX_REPEAT = 5

def generate_from_regex(regex, trace=False):
    pos = 0
    trace_steps = []

    def log(step):
        if trace:
            trace_steps.append(step)

    def parse_expression():
        nonlocal pos
        result = ""

        while pos < len(regex):
            char = regex[pos]

            if char == '(':
                pos += 1
                group = parse_group()
                result += group
            elif char == ')':
                return result
            elif char == '|':
                return result  # return left side of alternation
            elif char in "*+?":
                prev = result[-1]
                repeat = ""
                if char == '*':
                    count = random.randint(0, MAX_REPEAT)
                    repeat = prev * count
                    log(f"Repeat '*' → {count} times: '{repeat}'")
                elif char == '+':
                    count = random.randint(1, MAX_REPEAT)
                    repeat = prev * count
                    log(f"Repeat '+' → {count} times: '{repeat}'")
                elif char == '?':
                    include = random.choice([True, False])
                    repeat = prev if include else ''
                    log(f"Optional '?' → {'include' if include else 'exclude'}: '{repeat}'")
                result = result[:-1] + repeat
                pos += 1
            else:
                result += char
                pos += 1
        return result

    def parse_group():
        nonlocal pos
        options = []
        group = ""
        while pos < len(regex) and regex[pos] != ')':
            if regex[pos] == '|':
                options.append(group)
                group = ""
                pos += 1
            elif regex[pos] == '(':
                pos += 1
                group += parse_group()
            else:
                group += regex[pos]
                pos += 1
        options.append(group)
        pos += 1  # skip ')'
        chosen = random.choice(options)
        log(f"Group ({'|'.join(options)}) → '{chosen}'")
        return chosen

    final_result = parse_expression()
    return (final_result, trace_steps) if trace else final_result

# Example usage with regex from Variant 1
regexes = [
    "(a|b)(c|d)E+G?",
    "P(Q|R|S)T(uv|w|x)*Z+",
    "1(0|1)*2(3|4)5"
]

for r in regexes:
    result, steps = generate_from_regex(r, trace=True)
    print(f"Regex: {r}")
    print(f"Generated: {result}")
    print("Trace:")
    for s in steps:
        print(f"  - {s}")
    print("-" * 40)
