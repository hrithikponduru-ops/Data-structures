"""
08 — Binary Heap & Priority Queue
=================================
WHAT
    A complete binary tree stored in an ARRAY (no pointers) satisfying the
    heap property:   min-heap: A[parent(i)] ≤ A[i]   (max-heap: ≥)
    The minimum is always at A[0].

INDEX FORMULAS (0-based array)
    parent(i) = ⌊(i − 1) / 2⌋
    left(i)   = 2i + 1
    right(i)  = 2i + 2
    height    = ⌊log₂ n⌋
    leaves    = indices ⌊n/2⌋ … n − 1     (exactly ⌈n/2⌉ leaves)

OPERATIONS
    push:  append at the end, sift UP   → O(log n)
    pop:   move last to root, sift DOWN → O(log n)
    peek:  A[0]                         → O(1)

BUILD-HEAP IS O(n), NOT O(n log n) — the proof
    At most ⌈n / 2^{h+1}⌉ nodes have height h, and sift-down from height h
    costs ≤ h swaps:

        T(n) ≤ Σ_{h=0}^{⌊log₂ n⌋} ⌈n / 2^{h+1}⌉ · h
             ≤ n · Σ_{h=0}^{∞} h / 2^{h+1}
             = (n/2) · Σ_{h=0}^{∞} h · (1/2)^h
             = (n/2) · [ x / (1 − x)² ]_{x = 1/2}
             = (n/2) · 2 = n            ⇒  T(n) = O(n)

HEAPSORT
    build max-heap O(n), then n × (swap root to end + sift down) = O(n log n).
    In place, not stable. Comparison sorting lower bound:
        log₂(n!) = n log₂ n − n log₂ e + O(log n)      (Stirling: n! ≈ √(2πn)·(n/e)^n)

PYTHON
    heapq module = min-heap on a plain list (heappush, heappop, heapify, nlargest).
"""
import heapq
import math
import random


class MinHeap:
    def __init__(self, items=None):
        self.a = list(items) if items else []
        self.swaps = 0
        if self.a:
            self._heapify()

    @staticmethod
    def parent(i):
        return (i - 1) // 2

    def __len__(self):
        return len(self.a)

    def peek(self):
        return self.a[0]

    def push(self, x):
        self.a.append(x)
        self._sift_up(len(self.a) - 1)

    def pop(self):
        if not self.a:
            raise IndexError("pop from empty heap")
        top, last = self.a[0], self.a.pop()
        if self.a:
            self.a[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        a = self.a
        while i > 0 and a[i] < a[self.parent(i)]:
            p = self.parent(i)
            a[i], a[p] = a[p], a[i]
            self.swaps += 1
            i = p

    def _sift_down(self, i):
        a, n = self.a, len(self.a)
        while True:
            l, r, smallest = 2 * i + 1, 2 * i + 2, i
            if l < n and a[l] < a[smallest]:
                smallest = l
            if r < n and a[r] < a[smallest]:
                smallest = r
            if smallest == i:
                return
            a[i], a[smallest] = a[smallest], a[i]
            self.swaps += 1
            i = smallest

    def _heapify(self):                         # start at last internal node
        for i in range(len(self.a) // 2 - 1, -1, -1):
            self._sift_down(i)

    def is_valid(self):
        return all(self.a[self.parent(i)] <= self.a[i] for i in range(1, len(self.a)))


def heapsort(arr):
    a, n = list(arr), len(arr)

    def sift_down(i, size):                     # max-heap version
        while True:
            l, r, big = 2 * i + 1, 2 * i + 2, i
            if l < size and a[l] > a[big]:
                big = l
            if r < size and a[r] > a[big]:
                big = r
            if big == i:
                return
            a[i], a[big] = a[big], a[i]
            i = big

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]             # largest goes to its final spot
        sift_down(0, end)
    return a


if __name__ == "__main__":
    h = MinHeap([9, 4, 7, 1, 8, 2, 6])
    print("Heap array:", h.a, "| valid:", h.is_valid())
    i = 4
    print(f"Index formulas for i={i}: parent={MinHeap.parent(i)}, left={2 * i + 1}, right={2 * i + 2}")
    print("Popping in order:", [h.pop() for _ in range(len(h))])

    random.seed(3)
    n = 100_000
    data = [random.random() for _ in range(n)]
    built = MinHeap(data)
    pushed = MinHeap()
    for x in data:
        pushed.push(x)
    print(f"\nn = {n}")
    print(f"  build-heap swaps   = {built.swaps:>7}   ≤ n = {n}           ⇒ O(n)")
    print(f"  n × push swaps     = {pushed.swaps:>7}   (worst case n·⌊log₂n⌋ = {n * int(math.log2(n))})")

    arr = [random.randint(0, 99) for _ in range(20)]
    print("\nHeapsort:", heapsort(arr) == sorted(arr), heapsort(arr))

    print("Top-3 via heapq.nlargest:", heapq.nlargest(3, arr))

    m = 1_000_000
    lg = math.lgamma(m + 1) / math.log(2)
    stirling = m * math.log2(m) - m * math.log2(math.e) + 0.5 * math.log2(2 * math.pi * m)
    print(f"\nlog₂(n!) for n=10⁶: exact={lg:,.1f}  Stirling={stirling:,.1f}")
