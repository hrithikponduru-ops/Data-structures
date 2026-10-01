"""
05 — Queue (FIFO: First In, First Out) & Deque
==============================================
WHAT
    Insert at the rear (enqueue), remove from the front (dequeue).

WHY NOT A PLAIN LIST?
    list.pop(0) shifts every remaining element: O(n). A queue needs O(1).

CIRCULAR QUEUE — modular arithmetic
    Fixed array of capacity m, front index f, current size s:
        next free slot (rear)   r = (f + s) mod m
        after a dequeue         f ← (f + 1) mod m
        i-th element            A[(f + i) mod m]
        full ⇔ s = m,    empty ⇔ s = 0
    "mod m" wraps the indices around so freed slots at the start get reused.

QUEUE FROM TWO STACKS — amortized analysis
    in_stack receives enqueues. When out_stack is empty, pour all of in_stack
    into it (this reverses the order). Every element is pushed ≤ 2 times and
    popped ≤ 2 times ⇒ n operations cost ≤ 4n ⇒ O(1) amortized.

DEQUE (double-ended queue)
    collections.deque = doubly linked list of fixed-size blocks:
    O(1) append/pop at both ends, O(n) indexing in the middle.

APPLICATION — JOSEPHUS PROBLEM (0-indexed survivor)
    n people in a circle, every k-th is eliminated:
        J(1, k) = 0,       J(n, k) = (J(n − 1, k) + k) mod n
    Closed form for k = 2: write n = 2^a + L with 0 ≤ L < 2^a, then
        J(n, 2) = 2L

COMPLEXITY
    enqueue, dequeue, peek   O(1)        space O(m)
"""
from collections import deque


class CircularQueue:
    def __init__(self, capacity):
        self.A = [None] * capacity
        self.m = capacity
        self.f = 0
        self.s = 0

    def enqueue(self, x):
        if self.s == self.m:
            raise OverflowError("queue full")
        self.A[(self.f + self.s) % self.m] = x      # r = (f + s) mod m
        self.s += 1

    def dequeue(self):
        if self.s == 0:
            raise IndexError("queue empty")
        x = self.A[self.f]
        self.A[self.f] = None
        self.f = (self.f + 1) % self.m              # f ← (f + 1) mod m
        self.s -= 1
        return x

    def peek(self):
        return self.A[self.f] if self.s else None

    def __iter__(self):
        for i in range(self.s):
            yield self.A[(self.f + i) % self.m]

    def __repr__(self):
        return f"front→ {list(self)} ←rear   raw={self.A} f={self.f} s={self.s}"


class TwoStackQueue:
    def __init__(self):
        self.inbox, self.outbox = [], []
        self.moves = 0

    def enqueue(self, x):
        self.inbox.append(x)

    def dequeue(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
                self.moves += 1
        return self.outbox.pop()


def josephus_sim(n, k):
    q = deque(range(n))
    while len(q) > 1:
        q.rotate(-(k - 1))      # skip k − 1 people
        q.popleft()             # eliminate the k-th
    return q[0]


def josephus_formula(n, k):
    j = 0
    for m in range(2, n + 1):
        j = (j + k) % m
    return j


def josephus_k2_closed(n):
    a = n.bit_length() - 1
    return 2 * (n - (1 << a))


if __name__ == "__main__":
    cq = CircularQueue(5)
    for x in range(1, 6):
        cq.enqueue(x)
    cq.dequeue()
    cq.dequeue()
    cq.enqueue(6)
    cq.enqueue(7)               # these wrap around to indices 0 and 1
    print("Circular queue:", cq)

    tq = TwoStackQueue()
    n = 1000
    out = []
    for i in range(n):
        tq.enqueue(i)
        if i % 3 == 0:
            out.append(tq.dequeue())
    while tq.inbox or tq.outbox:
        out.append(tq.dequeue())
    print(f"\nTwo-stack queue keeps FIFO order: {out == list(range(n))}, "
          f"element moves = {tq.moves} (≤ n = {n})")

    d = deque([2, 3])
    d.appendleft(1)
    d.append(4)
    print("\nDeque:", d, "| popleft →", d.popleft(), "| pop →", d.pop())

    print("\nJosephus (0-indexed survivor):")
    for n, k in [(7, 3), (41, 3), (41, 2), (100, 2)]:
        line = f"  n={n:>3}, k={k}: simulation={josephus_sim(n, k):>3}, recurrence={josephus_formula(n, k):>3}"
        if k == 2:
            line += f", closed form 2L={josephus_k2_closed(n):>3}"
        print(line)
