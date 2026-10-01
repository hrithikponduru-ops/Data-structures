"""
04 — Stack (LIFO: Last In, First Out)
=====================================
WHAT
    Only the top is accessible. push(x) puts x on top, pop() removes the top.
    Built on a dynamic array: top = A[n − 1].

COMPLEXITY
    push, pop, peek   O(1) amortized
    space             O(n)

WHERE IT HIDES
    The function call stack, undo/redo, DFS, expression parsing,
    backtracking, the browser "back" button.

THE MATH: CATALAN NUMBERS
    Number of balanced strings with n pairs of brackets
      = number of valid push/pop sequences of n items
      = n-th Catalan number:

        C_n = (1 / (n + 1)) · binom(2n, n) = (2n)! / ((n + 1)! · n!)

    Recurrence (split at the bracket that matches the first "("):
        C_0 = 1,     C_{n+1} = Σ_{i=0}^{n} C_i · C_{n−i}

    C_0 … C_7 = 1, 1, 2, 5, 14, 42, 132, 429

POSTFIX (Reverse Polish) EVALUATION
    Infix:    (3 + 4) × 2 − 5
    Postfix:  3 4 + 2 × 5 −
    Scan left → right: number → push; operator → pop b, pop a, push (a op b).
    Postfix needs no parentheses and no precedence rules.

SHUNTING-YARD (infix → postfix), precedence:
    ^ (right-assoc)  >  × /  >  + −
"""
import itertools
import math
import operator
import re


class Stack:
    def __init__(self):
        self._data = []

    def push(self, x):
        self._data.append(x)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return not self._data

    def __len__(self):
        return len(self._data)


PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(s):
    st = Stack()
    for ch in s:
        if ch in "([{":
            st.push(ch)
        elif ch in PAIRS:
            if st.is_empty() or st.pop() != PAIRS[ch]:
                return False
    return st.is_empty()


PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
RIGHT_ASSOC = {"^"}
OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul,
       "/": operator.truediv, "^": operator.pow}


def tokenize(expr):
    return re.findall(r"\d+(?:\.\d+)?|[()+\-*/^]", expr)


def infix_to_postfix(expr):
    out, ops = [], Stack()
    for tok in tokenize(expr):
        if tok[0].isdigit():
            out.append(tok)
        elif tok == "(":
            ops.push(tok)
        elif tok == ")":
            while ops.peek() != "(":
                out.append(ops.pop())
            ops.pop()                           # discard "("
        else:
            while (not ops.is_empty() and ops.peek() != "(" and
                   (PREC[ops.peek()] > PREC[tok] or
                    (PREC[ops.peek()] == PREC[tok] and tok not in RIGHT_ASSOC))):
                out.append(ops.pop())
            ops.push(tok)
    while not ops.is_empty():
        out.append(ops.pop())
    return out


def eval_postfix(tokens):
    st = Stack()
    for tok in tokens:
        if tok in OPS:
            b, a = st.pop(), st.pop()           # order matters: a op b
            st.push(OPS[tok](a, b))
        else:
            st.push(float(tok))
    return st.pop()


def count_balanced_bruteforce(n):
    return sum(is_balanced("".join(p)) for p in itertools.product("()", repeat=2 * n))


if __name__ == "__main__":
    for s in ["{[()()]}", "([)]", "((()", ""]:
        print(f"is_balanced({s!r:12}) = {is_balanced(s)}")

    for expr in ["(3 + 4) * 2 - 5", "2 ^ 3 ^ 2", "10 / (4 - 2) + 3 * 2"]:
        pf = infix_to_postfix(expr)
        print(f"\n{expr:22} → postfix: {' '.join(pf):18} = {eval_postfix(pf):g}")

    print("\nCatalan check: brute force vs  C_n = binom(2n, n) / (n + 1)")
    for n in range(1, 8):
        print(f"  n={n}: {count_balanced_bruteforce(n):>4}  vs  {math.comb(2 * n, n) // (n + 1):>4}")
