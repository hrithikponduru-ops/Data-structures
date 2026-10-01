"""
07 — Binary Trees & Binary Search Trees (BST)
=============================================
WHAT
    Binary tree: each node has ≤ 2 children.
    BST invariant: for every node x,
        keys in left subtree  <  x.key  <  keys in right subtree
    ⇒ an in-order traversal visits keys in sorted order.

BINARY TREE FORMULAS  (height h = number of edges on the longest root-leaf path)
    Max nodes on level ℓ:            2^ℓ
    Max nodes with height h:         Σ_{ℓ=0}^{h} 2^ℓ = 2^{h+1} − 1
    Min height with n nodes:         h_min = ⌈log₂(n + 1)⌉ − 1
    Max height with n nodes:         h_max = n − 1        (degenerate "linked list")
    Full binary tree (0 or 2 kids):  L = I + 1             (leaves = internal nodes + 1)
    Edges:                           E = n − 1

COUNTING BSTs — Catalan numbers
    Choosing key i as root leaves i − 1 keys on the left and n − i on the right:
        C_0 = 1,    C_n = Σ_{i=1}^{n} C_{i−1} · C_{n−i} = (1 / (n + 1)) · binom(2n, n)

RANDOM BST (keys inserted in random order)
    Expected internal path length = 2(n + 1)·H_n − 4n
    ⇒ average node depth = 2(1 + 1/n)·H_n − 4 ≈ 2 ln n ≈ 1.386 · log₂ n
    Expected height ~ 4.311 · ln n   (asymptotically)

COMPLEXITY
    search / insert / delete   O(h):  O(log n) if balanced, O(n) worst case
    traversals                 O(n)

DELETE — three cases
    1. leaf               → remove it
    2. one child          → replace node by its child
    3. two children       → copy the in-order successor (min of right subtree),
                            then delete that successor (it has ≤ 1 child)
"""
import math
import random
from collections import deque


class Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = self.right = None


class BST:
    def __init__(self, keys=()):
        self.root = None
        self.size = 0
        for k in keys:
            self.insert(k)

    def insert(self, key):                      # iterative: O(h)
        if self.root is None:
            self.root = Node(key)
            self.size = 1
            return True
        cur = self.root
        while True:
            if key == cur.key:
                return False                    # no duplicates
            if key < cur.key:
                if cur.left is None:
                    cur.left = Node(key)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(key)
                    break
                cur = cur.right
        self.size += 1
        return True

    def search(self, key):                      # O(h)
        cur = self.root
        while cur and cur.key != key:
            cur = cur.left if key < cur.key else cur.right
        return cur is not None

    def min(self):
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.key

    def max(self):
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.key

    def delete(self, key):
        if not self.search(key):
            return False
        self.root = self._delete(self.root, key)
        self.size -= 1
        return True

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:               # cases 1 & 2
                return node.right
            if node.right is None:
                return node.left
            succ = node.right                   # case 3: in-order successor
            while succ.left:
                succ = succ.left
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        return node

    # ---------- traversals ----------
    def inorder(self):                          # Left, Node, Right (sorted)
        out, st, cur = [], [], self.root
        while st or cur:
            while cur:
                st.append(cur)
                cur = cur.left
            cur = st.pop()
            out.append(cur.key)
            cur = cur.right
        return out

    def preorder(self):                         # Node, Left, Right
        out, st = [], [self.root] if self.root else []
        while st:
            n = st.pop()
            out.append(n.key)
            if n.right:
                st.append(n.right)
            if n.left:
                st.append(n.left)
        return out

    def postorder(self):                        # Left, Right, Node
        out, st = [], [self.root] if self.root else []
        while st:
            n = st.pop()
            out.append(n.key)
            if n.left:
                st.append(n.left)
            if n.right:
                st.append(n.right)
        return out[::-1]

    def level_order(self):                      # BFS by levels
        if not self.root:
            return []
        out, q = [], deque([self.root])
        while q:
            level = []
            for _ in range(len(q)):
                n = q.popleft()
                level.append(n.key)
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
            out.append(level)
        return out

    def height_and_avg_depth(self):             # iterative, safe for deep trees
        if not self.root:
            return -1, 0.0
        q, total, h = deque([(self.root, 0)]), 0, 0
        while q:
            n, d = q.popleft()
            total += d
            h = max(h, d)
            if n.left:
                q.append((n.left, d + 1))
            if n.right:
                q.append((n.right, d + 1))
        return h, total / self.size


def count_bsts(n):
    C = [1] + [0] * n
    for k in range(1, n + 1):
        C[k] = sum(C[i - 1] * C[k - i] for i in range(1, k + 1))
    return C[n]


if __name__ == "__main__":
    t = BST([50, 30, 70, 20, 40, 60, 80, 35])
    print("In-order   :", t.inorder())
    print("Pre-order  :", t.preorder())
    print("Post-order :", t.postorder())
    print("Level-order:", t.level_order())
    print("min, max   :", t.min(), t.max(), "| search(60):", t.search(60))
    t.delete(30)                                # two children → successor 35
    print("After delete(30):", t.level_order())

    print("\nNumber of distinct BSTs:  DP recurrence vs binom(2n,n)/(n+1)")
    for n in range(1, 9):
        print(f"  n={n}: {count_bsts(n):>5} vs {math.comb(2 * n, n) // (n + 1):>5}")

    n = 10_000
    keys = list(range(n))
    random.seed(7)
    random.shuffle(keys)
    rt = BST(keys)
    h, avg = rt.height_and_avg_depth()
    H = sum(1 / i for i in range(1, n + 1))
    print(f"\nRandom BST, n={n}:")
    print(f"  height = {h}  (min possible ⌈log₂(n+1)⌉−1 = {math.ceil(math.log2(n + 1)) - 1})")
    print(f"  avg depth = {avg:.2f}  vs  2(1+1/n)H_n − 4 = {2 * (1 + 1 / n) * H - 4:.2f}")

    st = BST(range(1000))
    print(f"\nSorted insertion of 1000 keys → height = {st.height_and_avg_depth()[0]} (= n − 1, degenerate)")
