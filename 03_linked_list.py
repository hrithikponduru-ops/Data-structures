"""
03 — Linked Lists (singly & doubly)
===================================
WHAT
    A chain of nodes; each node stores data plus a pointer to the next node
    (and to the previous one in a doubly linked list). Nodes are scattered in
    memory, so there is NO address formula — you must walk the chain.

COMPLEXITY               Singly (head+tail)   Doubly (sentinel)
    access k-th            O(k)                 O(min(k, n − k))
    push front             O(1)                 O(1)
    push back              O(1)                 O(1)
    delete a given node    O(n)                 O(1)
    search                 O(n)                 O(n)

MEMORY
    Singly:  n · (w_data + w_ptr)
    Doubly:  n · (w_data + 2·w_ptr)

FLOYD'S CYCLE DETECTION (tortoise & hare) — the math
    μ = tail length before the cycle,  λ = cycle length.
    slow moves 1 step, fast moves 2 steps. At their first meeting slow walked
        s  = μ + k                 (k = distance into the cycle)
    and fast walked
        2s = μ + k + m·λ           (m extra full laps)
    Subtract:  s = m·λ   ⇒   μ + k = m·λ   ⇒   μ = m·λ − k
    So walking μ steps from the meeting point lands on the cycle start,
    because k + μ ≡ 0 (mod λ). Reset one pointer to head, move both 1 step
    at a time: they meet exactly at the start of the cycle.

MIDDLE NODE
    fast moves 2 steps per 1 step of slow ⇒ when fast hits the end,
    slow is at index ⌊n / 2⌋.
"""


class Node:
    __slots__ = ("data", "next")

    def __init__(self, data, nxt=None):
        self.data = data
        self.next = nxt


class SinglyLinkedList:
    def __init__(self, items=()):
        self.head = self.tail = None
        self.size = 0
        for x in items:
            self.append(x)

    def push_front(self, x):                    # O(1)
        self.head = Node(x, self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def append(self, x):                        # O(1) thanks to tail pointer
        node = Node(x)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def find(self, x):                          # O(n)
        cur, idx = self.head, 0
        while cur:
            if cur.data == x:
                return idx
            cur, idx = cur.next, idx + 1
        return -1

    def delete(self, x):                        # O(n): must find predecessor
        prev, cur = None, self.head
        while cur and cur.data != x:
            prev, cur = cur, cur.next
        if cur is None:
            return False
        if prev:
            prev.next = cur.next
        else:
            self.head = cur.next
        if cur is self.tail:
            self.tail = prev
        self.size -= 1
        return True

    def reverse(self):                          # O(n), O(1) extra space
        prev, cur = None, self.head
        self.tail = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def middle(self):                           # slow/fast pointers
        slow = fast = self.head
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
        return slow.data if slow else None

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def __repr__(self):
        return " → ".join(map(str, self)) + " → None"


def floyd_cycle(head):
    """Returns (μ, λ) if a cycle exists, else None."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            break
    else:
        return None
    slow, mu = head, 0                          # phase 2: find μ
    while slow is not fast:
        slow, fast = slow.next, fast.next
        mu += 1
    lam, fast = 1, slow.next                    # phase 3: find λ
    while fast is not slow:
        fast, lam = fast.next, lam + 1
    return mu, lam


class DNode:
    __slots__ = ("data", "prev", "next")

    def __init__(self, data=None):
        self.data = data
        self.prev = self.next = None


class DoublyLinkedList:
    """Circular with one sentinel node: no special cases for empty list."""

    def __init__(self):
        self.sentinel = DNode()
        self.sentinel.prev = self.sentinel.next = self.sentinel
        self.size = 0

    def _insert_after(self, node, x):
        new = DNode(x)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        self.size += 1
        return new

    def push_front(self, x):
        return self._insert_after(self.sentinel, x)

    def push_back(self, x):
        return self._insert_after(self.sentinel.prev, x)

    def remove(self, node):                     # O(1): we know both neighbours
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node.data

    def __iter__(self):
        cur = self.sentinel.next
        while cur is not self.sentinel:
            yield cur.data
            cur = cur.next

    def __reversed__(self):
        cur = self.sentinel.prev
        while cur is not self.sentinel:
            yield cur.data
            cur = cur.prev


if __name__ == "__main__":
    sll = SinglyLinkedList([10, 20, 30, 40, 50])
    print("Singly:      ", sll)
    sll.push_front(5)
    sll.delete(30)
    print("push 5, del 30:", sll, f"(size={sll.size})")
    print("Middle node (index ⌊n/2⌋):", sll.middle())
    sll.reverse()
    print("Reversed:    ", sll)

    nodes = [Node(i) for i in range(10)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    nodes[-1].next = nodes[3]                   # tail 0..2 (μ=3), cycle 3..9 (λ=7)
    print("\nFloyd on list with cycle → (μ, λ) =", floyd_cycle(nodes[0]))
    print("Floyd on list without cycle →", floyd_cycle(SinglyLinkedList([1, 2, 3]).head))

    dll = DoublyLinkedList()
    for x in "BCD":
        dll.push_back(x)
    a = dll.push_front("A")
    print("\nDoubly forward: ", list(dll))
    print("Doubly backward:", list(reversed(dll)))
    dll.remove(a)
    print("After O(1) remove of 'A':", list(dll))
