# Data Structures in Python — Code, Math & What Happens Behind the Scenes

Each file is a standalone, runnable program (`python3 01_complexity.py`).
The docstring at the top of every file explains **what** the structure is, the
**math** behind it (formulas kept in their original form), its **complexity**,
and **how it works internally**. The `__main__` demo then *verifies the formulas
numerically* against the real implementation.

| # | File | Concept | Key math verified by the demo |
|---|------|---------|-------------------------------|
| 01 | `01_complexity.py` | Big-O, Ω, Θ | Σi = n(n+1)/2, Σ2^i = 2^{k+1} − 1, H_n ≈ ln n + γ |
| 02 | `02_dynamic_array.py` | Arrays, dynamic arrays, Python `list` | addr = base + i·w, amortized cost < 3n |
| 03 | `03_linked_list.py` | Singly / doubly linked lists | Floyd cycle: μ = m·λ − k |
| 04 | `04_stack.py` | Stack, brackets, postfix, shunting-yard | Catalan C_n = binom(2n,n)/(n+1) |
| 05 | `05_queue.py` | Circular queue, two-stack queue, deque | r = (f + s) mod m, Josephus J(n,k) |
| 06 | `06_hash_table.py` | Hash tables, Python `dict` | α = n/m, ½(1 + 1/(1−α)²), birthday paradox |
| 07 | `07_binary_search_tree.py` | Binary trees, BST, traversals | 2^{h+1} − 1, ⌈log₂(n+1)⌉ − 1, 2(1+1/n)H_n − 4 |
| 08 | `08_heap.py` | Binary heap, heapsort, `heapq` | parent = ⌊(i−1)/2⌋, build-heap ≤ n |
| 09 | `09_avl_tree.py` | AVL tree, rotations | N(h) = F_{h+3} − 1, h < 1.4405·log₂(n+2) − 0.3277 |
| 10 | `10_trie.py` | Trie / prefix tree | nodes ≤ 1 + Σ\|w_i\| |
| 11 | `11_graph.py` | Graphs, BFS, DFS, topo sort, Dijkstra | Σdeg = 2\|E\|, (A^k)[i][j], trace(A³)/6 |
| 12 | `12_union_find.py` | Disjoint set union, Kruskal MST | size ≥ 2^rank, α(n) ≤ 4 |
| 13 | `13_segment_fenwick.py` | Segment tree, Fenwick tree | size < 4n, lowbit(i) = i & (−i) |

## Notation used in the formulas
- ⌊x⌋ floor, ⌈x⌉ ceiling, `mod` remainder
- Σ sum, Π product, binom(n, k) = n! / (k!(n−k)!)
- log₂ base-2 log, ln natural log, H_n harmonic number, γ ≈ 0.5772
- φ = (1 + √5)/2 golden ratio, F_k Fibonacci numbers
- α load factor (hash tables) **or** inverse Ackermann (union-find) — stated in each file

## Suggested study order
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13
