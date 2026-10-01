r"""
09 — AVL Tree (self-balancing BST)
==================================
WHAT
    A BST that keeps itself balanced after every insert/delete using rotations,
    guaranteeing O(log n) height — so the "sorted input" disaster of a plain BST
    never happens.

BALANCE FACTOR
    BF(x) = height(x.left) − height(x.right)        AVL rule:  BF(x) ∈ {−1, 0, +1}

WHY THE HEIGHT IS LOGARITHMIC — the Fibonacci proof
    Let N(h) = minimum number of nodes in an AVL tree of height h (edges).
    The sparsest tree has one subtree of height h−1 and one of height h−2:
        N(0) = 1,   N(1) = 2,   N(h) = N(h − 1) + N(h − 2) + 1
    This gives  N(h) = F_{h+3} − 1   (F₁ = F₂ = 1, Fibonacci)
    Since F_k ≈ φ^k / √5 with φ = (1 + √5)/2 ≈ 1.618:
        n ≥ N(h) ≈ φ^{h+3}/√5 − 1   ⇒   h < 1.4405 · log₂(n + 2) − 0.3277
    So an AVL tree is at most ≈ 44 % taller than a perfect binary tree.

ROTATIONS (O(1) pointer changes, in-order order preserved)

    RIGHT ROTATION (fixes Left-Left)        LEFT ROTATION (fixes Right-Right)
            y                x                    x                  y
           / \              / \                  / \                / \
          x   T3   ──►     T1  y                T1  y      ──►     x   T3
         / \                  / \                  / \            / \
        T1  T2               T2  T3               T2  T3         T1  T2

    In-order is T1 x T2 y T3 before and after ⇒ BST property is preserved.

THE FOUR CASES (z = first unbalanced node on the way up)
    LL:  BF(z) = +2, BF(z.left)  ≥ 0  → rotate_right(z)
    LR:  BF(z) = +2, BF(z.left)  < 0  → rotate_left(z.left), then rotate_right(z)
    RR:  BF(z) = −2, BF(z.right) ≤ 0  → rotate_left(z)
    RL:  BF(z) = −2, BF(z.right) > 0  → rotate_right(z.right), then rotate_left(z)

COMPLEXITY
    search / insert / delete   O(log n) worst case
    rotations per insert       ≤ 2 (one single or one double rotation)
"""
import math
import random


class Node:
    __slots__ = ("key", "left", "right", "h")

    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.h = 1                              # node-height: leaf = 1, empty = 0


def height(n):
    return n.h if n else 0


def bf(n):
    return height(n.left) - height(n.right)


def update(n):
    n.h = 1 + max(height(n.left), height(n.right))


class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.rotations = 0

    def _rotate_right(self, y):
        x, T2 = y.left, y.left.right
        x.right, y.left = y, T2
        update(y)
        update(x)
        self.rotations += 1
        return x

    def _rotate_left(self, x):
        y, T2 = x.right, x.right.left
        y.left, x.right = x, T2
        update(x)
        update(y)
        self.rotations += 1
        return y

    def _rebalance(self, n):
        update(n)
        b = bf(n)
        if b > 1:
            if bf(n.left) < 0:                  # LR
                n.left = self._rotate_left(n.left)
            return self._rotate_right(n)        # LL
        if b < -1:
            if bf(n.right) > 0:                 # RL
                n.right = self._rotate_right(n.right)
            return self._rotate_left(n)         # RR
        return n

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, n, key):
        if n is None:
            self.size += 1
            return Node(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
        elif key > n.key:
            n.right = self._insert(n.right, key)
        else:
            return n
        return self._rebalance(n)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, n, key):
        if n is None:
            return None
        if key < n.key:
            n.left = self._delete(n.left, key)
        elif key > n.key:
            n.right = self._delete(n.right, key)
        else:
            if n.left is None or n.right is None:
                self.size -= 1
                return n.left or n.right
            s = n.right
            while s.left:
                s = s.left
            n.key = s.key
            n.right = self._delete(n.right, s.key)
        return self._rebalance(n)

    def search(self, key):
        cur = self.root
        while cur and cur.key != key:
            cur = cur.left if key < cur.key else cur.right
        return cur is not None

    def edge_height(self):
        return height(self.root) - 1

    def is_valid(self):
        def check(n, lo, hi):
            if n is None:
                return True, 0
            if not (lo < n.key < hi):
                return False, 0
            okL, hL = check(n.left, lo, n.key)
            okR, hR = check(n.right, n.key, hi)
            h = 1 + max(hL, hR)
            return okL and okR and abs(hL - hR) <= 1 and h == n.h, h
        return check(self.root, -math.inf, math.inf)[0]

    def pretty(self, n=None, prefix="", is_left=True, first=True):
        n = self.root if first else n
        if n is None:
            return ""
        s = self.pretty(n.right, prefix + ("│   " if is_left and not first else "    "), False, False) if n.right else ""
        s += prefix + ("" if first else ("└── " if is_left else "┌── ")) + f"{n.key} (BF={bf(n):+d})\n"
        s += self.pretty(n.left, prefix + ("    " if is_left or first else "│   "), True, False) if n.left else ""
        return s


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    t = AVLTree()
    for k in [10, 20, 30, 40, 50, 25]:          # triggers RR and RL cases
        t.insert(k)
    print("AVL after inserting 10,20,30,40,50,25 (right side = top):")
    print(t.pretty())
    print("valid AVL:", t.is_valid(), "| rotations:", t.rotations)

    print("\nMinimum nodes N(h):  recurrence vs F_{h+3} − 1")
    N = [1, 2]
    for h in range(2, 10):
        N.append(N[-1] + N[-2] + 1)
    for h in range(10):
        print(f"  h={h}: N={N[h]:>4}   F_(h+3) − 1 = {fib(h + 3) - 1:>4}")

    n = 100_000
    avl = AVLTree()
    for k in range(n):                          # sorted input: worst for a plain BST
        avl.insert(k)
    bound = 1.4405 * math.log2(n + 2) - 0.3277
    print(f"\nSorted insert of n={n}: AVL height = {avl.edge_height()}, "
          f"perfect = {math.ceil(math.log2(n + 1)) - 1}, AVL bound = {bound:.2f}, plain BST = {n - 1}")

    random.seed(5)
    keys = random.sample(range(n), n // 2)
    for k in keys:
        avl.delete(k)
    print(f"After {n // 2} random deletes: size={avl.size}, height={avl.edge_height()}, valid={avl.is_valid()}")
