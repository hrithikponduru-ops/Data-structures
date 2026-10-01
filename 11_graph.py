"""
11 — Graphs (BFS, DFS, Topological Sort, Dijkstra)
==================================================
WHAT
    G = (V, E): vertices V and edges E ⊆ V × V. Directed or undirected,
    weighted or unweighted. Trees, lists and grids are all special graphs.

BASIC FORMULAS
    Handshake lemma (undirected):   Σ_{v∈V} deg(v) = 2|E|
    Directed:                       Σ in-deg(v) = Σ out-deg(v) = |E|
    Max edges:                      undirected n(n − 1)/2,   directed n(n − 1)
    Density:                        D = 2|E| / (|V|(|V| − 1))
    Tree on n vertices:             exactly n − 1 edges, connected, acyclic

REPRESENTATION                      Space        Edge check   Iterate neighbours
    Adjacency matrix A[i][j]        Θ(V²)        O(1)         O(V)
    Adjacency list                  Θ(V + E)     O(deg)       O(deg)

MATRIX POWER = COUNTING WALKS
    (A^k)[i][j] = number of walks of length k from i to j
    Triangles in an undirected graph = trace(A³) / 6

TRAVERSALS — both O(V + E)
    BFS (queue): visits by distance layers ⇒ shortest paths in unweighted graphs
                 dist(v) = dist(parent(v)) + 1
    DFS (stack / recursion): goes deep first ⇒ cycles, components, topo order

TOPOLOGICAL SORT (Kahn's algorithm, DAG only) — O(V + E)
    Repeatedly output a vertex with in-degree 0 and delete its out-edges.
    If fewer than |V| vertices are output, the graph has a cycle.

DIJKSTRA (non-negative weights) — O((V + E) log V) with a binary heap
    Relaxation:   if d[u] + w(u, v) < d[v]:   d[v] ← d[u] + w(u, v)
    Greedy correctness: the unvisited vertex with smallest d is final,
    because any other path to it must leave through a vertex with d ≥ it
    and weights are ≥ 0.
"""
import heapq
from collections import defaultdict, deque


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = defaultdict(list)            # u → [(v, w), …]

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if self.directed:
            self.adj[v]                         # make sure v exists
        else:
            self.adj[v].append((u, w))

    @property
    def V(self):
        return list(self.adj)

    def num_edges(self):
        total = sum(len(lst) for lst in self.adj.values())
        return total if self.directed else total // 2

    def bfs(self, s):
        dist, parent = {s: 0}, {s: None}
        q = deque([s])
        while q:
            u = q.popleft()
            for v, _ in self.adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
        return dist, parent

    @staticmethod
    def path(parent, t):
        if t not in parent:
            return None
        out = []
        while t is not None:
            out.append(t)
            t = parent[t]
        return out[::-1]

    def dfs(self, s):
        order, seen, st = [], set(), [s]
        while st:
            u = st.pop()
            if u in seen:
                continue
            seen.add(u)
            order.append(u)
            for v, _ in reversed(self.adj[u]):
                if v not in seen:
                    st.append(v)
        return order

    def topo_sort(self):
        indeg = {u: 0 for u in self.adj}
        for u in self.adj:
            for v, _ in self.adj[u]:
                indeg[v] += 1
        q = deque(sorted(u for u, d in indeg.items() if d == 0))
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in self.adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == len(self.adj) else None   # None ⇒ cycle

    def dijkstra(self, s):
        dist = {u: float("inf") for u in self.adj}
        parent = {s: None}
        dist[s] = 0
        pq = [(0, s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue                        # stale entry
            for v, w in self.adj[u]:
                if dist[u] + w < dist[v]:       # relaxation
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        return dist, parent

    def adjacency_matrix(self):
        idx = {u: i for i, u in enumerate(self.V)}
        n = len(idx)
        A = [[0] * n for _ in range(n)]
        for u in self.adj:
            for v, _ in self.adj[u]:
                A[idx[u]][idx[v]] = 1
        return A, idx


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def matpow(A, k):
    n = len(A)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while k:                                    # fast exponentiation: O(n³ log k)
        if k & 1:
            R = matmul(R, A)
        A = matmul(A, A)
        k >>= 1
    return R


if __name__ == "__main__":
    g = Graph()
    for u, v in [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("D", "F")]:
        g.add_edge(u, v)
    degs = {u: len(g.adj[u]) for u in g.V}
    n, m = len(g.V), g.num_edges()
    print("Degrees:", degs)
    print(f"Handshake: Σdeg = {sum(degs.values())} = 2|E| = {2 * m}")
    print(f"Density D = 2|E|/(|V|(|V|−1)) = {2 * m / (n * (n - 1)):.3f}")

    dist, parent = g.bfs("A")
    print("\nBFS distances from A:", dist)
    print("Shortest path A→F:", " → ".join(Graph.path(parent, "F")))
    print("DFS order from A:", g.dfs("A"))

    A, idx = g.adjacency_matrix()
    A3 = matpow(A, 3)
    print(f"\nWalks of length 3 from A to D = (A³)[A][D] = {A3[idx['A']][idx['D']]}")
    print(f"Triangles = trace(A³)/6 = {sum(A3[i][i] for i in range(n)) // 6}")

    dag = Graph(directed=True)
    for u, v in [("Math", "Algorithms"), ("Programming", "Data Structures"),
                 ("Data Structures", "Algorithms"), ("Algorithms", "AI"), ("Math", "AI")]:
        dag.add_edge(u, v)
    print("\nTopological order (course plan):", dag.topo_sort())
    dag.add_edge("AI", "Math")
    print("After adding AI → Math (creates cycle):", dag.topo_sort())

    wg = Graph(directed=True)
    for u, v, w in [("S", "A", 4), ("S", "B", 1), ("B", "A", 2), ("A", "C", 1),
                    ("B", "C", 5), ("C", "T", 3), ("B", "T", 8)]:
        wg.add_edge(u, v, w)
    d, p = wg.dijkstra("S")
    print("\nDijkstra distances from S:", d)
    print("Cheapest S→T:", " → ".join(Graph.path(p, "T")), f"(cost {d['T']})")
