"""
12 — Disjoint Set Union (Union-Find)
====================================
WHAT
    Maintains a partition of {0, …, n − 1} into disjoint sets with two operations:
        find(x)      → representative (root) of x's set
        union(x, y)  → merge the two sets
    Each set is a tree stored in parent[]; a root has parent[r] = r.

TWO OPTIMIZATIONS
    1. Union by rank: attach the shorter tree under the taller one.
    2. Path compression: during find, point every visited node at the root.

THE MATH
    Lemma: a root of rank r has at least 2^r nodes.
        Proof (induction): rank becomes r + 1 only when two rank-r roots merge,
        so size ≥ 2^r + 2^r = 2^{r+1}.  ∎
    ⇒ r ≤ ⌊log₂ n⌋  ⇒ with union by rank alone, find is O(log n).

    With both optimizations, m operations cost O(m · α(n)), where α is the
    inverse Ackermann function:
        A(0, n) = n + 1
        A(m, 0) = A(m − 1, 1)
        A(m, n) = A(m − 1, A(m, n − 1))
        α(n)    = min{ k : A(k, k) ≥ n }
    A(4, 4) is astronomically large, so α(n) ≤ 4 for every practical n
    ⇒ effectively O(1) per operation.

APPLICATION — Kruskal's Minimum Spanning Tree
    Sort edges by weight; add edge (u, v) if find(u) ≠ find(v).
    Total O(E log E) for sorting + O(E · α(V)) for DSU. MST has V − 1 edges.
"""
import math
import random


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.count = n                          # number of disjoint sets

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:           # path compression
            nxt = self.parent[x]
            self.parent[x] = root
            x = nxt
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:       # union by rank
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)


def kruskal(n, edges):
    dsu, mst, total = DSU(n), [], 0
    for w, u, v in sorted(edges):
        if dsu.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break
    return mst, total


if __name__ == "__main__":
    d = DSU(8)
    for a, b in [(0, 1), (2, 3), (1, 3), (4, 5), (6, 7), (5, 7)]:
        d.union(a, b)
    print("Sets:", d.count, "| connected(0,2):", d.connected(0, 2), "| connected(0,4):", d.connected(0, 4))

    n = 1 << 16
    d = DSU(n)
    random.seed(11)
    while d.count > 1:
        d.union(random.randrange(n), random.randrange(n))
    roots = [i for i in range(n) if d.parent[i] == i]
    max_rank = max(d.rank)
    lemma = all(d.size[r] >= 2 ** d.rank[r] for r in roots)
    print(f"\nn = {n}: max rank = {max_rank} ≤ ⌊log₂ n⌋ = {int(math.log2(n))}, size ≥ 2^rank holds: {lemma}")

    edges = [(7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4), (5, 2, 4),
             (15, 3, 4), (6, 3, 5), (8, 4, 5), (9, 4, 6), (11, 5, 6)]
    mst, total = kruskal(7, edges)
    print("\nKruskal MST edges (u, v, w):", mst)
    print(f"MST weight = {total}, edges = {len(mst)} = V − 1")
