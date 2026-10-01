"""
13 — Segment Tree & Fenwick Tree (Binary Indexed Tree)
======================================================
PROBLEM
    Array of n numbers with two operations:
        update(i, value)   and   query(l, r) = A[l] ⊕ … ⊕ A[r]
    Plain array: update O(1), query O(n).  Prefix sums: query O(1), update O(n).
    These trees do BOTH in O(log n).

PREFIX-SUM IDENTITY
    P(i) = Σ_{k=0}^{i} A[k]        ⇒      sum(l, r) = P(r) − P(l − 1)

SEGMENT TREE
    Node covering [l, r] stores op(A[l..r]); children cover [l, m] and [m+1, r],
    m = ⌊(l + r) / 2⌋. Works for any associative op (sum, min, max, gcd …).
    1-indexed array storage: children of node i are 2i and 2i + 1.
    Height  h = ⌈log₂ n⌉
    Size    ≤ 2^{h+1} − 1 < 4n     (since 2^{⌈log₂ n⌉} < 2n)
    A range query touches at most 4 nodes per level ⇒ O(log n).

FENWICK TREE (BIT)
    lowbit(i) = i & (−i)   (lowest set bit, using two's complement)
    tree[i] stores the sum of A over the half-open range (i − lowbit(i), i]   (1-indexed)
        prefix(i):  s += tree[i];   i ← i − lowbit(i)      (strip lowest bit)
        add(i, δ):  tree[i] += δ;   i ← i + lowbit(i)      (climb to covering ranges)
    i has ≤ ⌊log₂ n⌋ + 1 bits ⇒ both loops are O(log n). Memory: exactly n + 1.
    Build in O(n): for i = 1…n: j = i + lowbit(i); if j ≤ n: tree[j] += tree[i]
"""
import math
import random


class SegmentTree:
    def __init__(self, data, op=lambda a, b: a + b, identity=0):
        self.n, self.op, self.id = len(data), op, identity
        self.t = [identity] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, l, r):
        if l == r:
            self.t[node] = data[l]
            return
        m = (l + r) // 2
        self._build(data, 2 * node, l, m)
        self._build(data, 2 * node + 1, m + 1, r)
        self.t[node] = self.op(self.t[2 * node], self.t[2 * node + 1])

    def update(self, i, val, node=1, l=0, r=None):
        r = self.n - 1 if r is None else r
        if l == r:
            self.t[node] = val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(i, val, 2 * node, l, m)
        else:
            self.update(i, val, 2 * node + 1, m + 1, r)
        self.t[node] = self.op(self.t[2 * node], self.t[2 * node + 1])

    def query(self, ql, qr, node=1, l=0, r=None):
        r = self.n - 1 if r is None else r
        if qr < l or r < ql:                    # no overlap
            return self.id
        if ql <= l and r <= qr:                 # total overlap
            return self.t[node]
        m = (l + r) // 2                        # partial overlap
        return self.op(self.query(ql, qr, 2 * node, l, m),
                       self.query(ql, qr, 2 * node + 1, m + 1, r))


class FenwickTree:
    def __init__(self, data):
        self.n = len(data)
        self.t = [0] + list(data)               # O(n) build
        for i in range(1, self.n + 1):
            j = i + (i & -i)
            if j <= self.n:
                self.t[j] += self.t[i]

    def add(self, i, delta):                    # A[i] += delta  (0-indexed)
        i += 1
        while i <= self.n:
            self.t[i] += delta
            i += i & -i

    def prefix(self, i):                        # Σ A[0..i]
        i += 1
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):                  # P(r) − P(l − 1)
        return self.prefix(r) - (self.prefix(l - 1) if l > 0 else 0)


if __name__ == "__main__":
    A = [5, 3, 8, 6, 1, 4, 7, 2]
    st = SegmentTree(A)
    mn = SegmentTree(A, op=min, identity=math.inf)
    ft = FenwickTree(A)
    print("A =", A)
    print("sum(2, 5): segment =", st.query(2, 5), "| fenwick =", ft.range_sum(2, 5), "| brute =", sum(A[2:6]))
    print("min(1, 6):", mn.query(1, 6))

    print("\nFenwick coverage: tree[i] = sum over (i − lowbit(i), i]")
    for i in range(1, 13):
        lb = i & -i
        print(f"  i={i:>2} ({i:04b})  lowbit={lb:>2}  covers ({i - lb:>2}, {i:>2}]")

    random.seed(2)
    n = 1000
    arr = [random.randint(-50, 50) for _ in range(n)]
    st, ft = SegmentTree(arr), FenwickTree(arr)
    ok = True
    for _ in range(3000):
        if random.random() < 0.5:
            i, v = random.randrange(n), random.randint(-50, 50)
            ft.add(i, v - arr[i])
            st.update(i, v)
            arr[i] = v
        else:
            l = random.randrange(n)
            r = random.randrange(l, n)
            b = sum(arr[l:r + 1])
            ok &= st.query(l, r) == b == ft.range_sum(l, r)
    print(f"\n3000 random updates/queries on n={n}: all correct = {ok}")
    used = max(i for i, x in enumerate(st.t) if x != 0)
    print(f"Segment tree array size 4n = {4 * n}, highest index used = {used}, "
          f"2^(⌈log₂n⌉+1) − 1 = {2 ** (math.ceil(math.log2(n)) + 1) - 1}")
