"""
02 — Arrays & Dynamic Arrays (how Python's list works)
=====================================================
WHAT
    A contiguous block of memory holding elements of equal size w.
    Random access is O(1) because the address is COMPUTED, not searched.

MEMORY ADDRESS FORMULAS
    1-D:            addr(A[i])    = base + i · w
    2-D row-major:  addr(A[i][j]) = base + (i · C + j) · w        (C = number of columns)
    2-D col-major:  addr(A[i][j]) = base + (j · R + i) · w        (R = number of rows)

DYNAMIC ARRAY (growth by doubling)
    When full (n = capacity), allocate 2·capacity and copy all n elements.

    Cost of n appends = n (writes) + copies made during resizes
                      = n + Σ_{k=0}^{⌊log₂ n⌋} 2^k
                      = n + (2^{⌊log₂ n⌋ + 1} − 1)
                      < n + 2n = 3n
    ⇒ amortized cost per append = 3n / n = O(1)

    Shrinking: halve the capacity when n ≤ capacity / 4.
    (Shrinking at n = capacity / 2 causes "thrashing": alternating push/pop
     at the boundary would trigger an O(n) copy on every operation.)

COMPLEXITY
    access A[i]          O(1)
    append               O(1) amortized, O(n) worst case (during a resize)
    insert/delete at i   O(n − i)   (elements must shift)
    search               O(n)

BEHIND THE SCENES IN CPYTHON
    list stores an array of pointers (PyObject*). It over-allocates roughly as
        new_allocated ≈ n + (n >> 3) + 6        (growth factor ≈ 1.125, not 2)
    Any geometric growth factor r > 1 still gives O(1) amortized append,
    because Σ copies ≤ n · r / (r − 1).
"""
import ctypes
import sys


class DynamicArray:
    def __init__(self):
        self._n = 0                         # number of stored elements
        self._capacity = 1                  # number of allocated slots
        self._A = self._make_array(1)
        self.copies = 0                     # instrumentation for the proof

    @staticmethod
    def _make_array(c):
        return (c * ctypes.py_object)()     # raw C array of object pointers

    def __len__(self):
        return self._n

    def __getitem__(self, i):
        if i < 0:
            i += self._n
        if not 0 <= i < self._n:
            raise IndexError("index out of range")
        return self._A[i]                   # O(1): base + i·w

    def append(self, x):
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._A[self._n] = x
        self._n += 1

    def insert(self, i, x):
        if not 0 <= i <= self._n:
            raise IndexError("index out of range")
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        for k in range(self._n, i, -1):     # shift right: O(n − i)
            self._A[k] = self._A[k - 1]
        self._A[i] = x
        self._n += 1

    def pop(self):
        if self._n == 0:
            raise IndexError("pop from empty array")
        x = self._A[self._n - 1]
        self._A[self._n - 1] = None
        self._n -= 1
        if 0 < self._n <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return x

    def _resize(self, c):
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
            self.copies += 1
        self._A, self._capacity = B, c

    def __repr__(self):
        items = ", ".join(repr(self._A[k]) for k in range(self._n))
        return f"[{items}]  (n={self._n}, capacity={self._capacity})"


if __name__ == "__main__":
    base, w, C = 1000, 4, 5
    i, j = 2, 3
    print(f"Row-major addr(A[{i}][{j}]) = {base} + ({i}·{C} + {j})·{w} = {base + (i * C + j) * w}\n")

    arr = DynamicArray()
    last = arr._capacity
    for x in range(1, 33):
        arr.append(x)
        if arr._capacity != last:
            print(f"  resize while appending element #{len(arr):>2}: capacity {last:>2} → {arr._capacity:>2}")
            last = arr._capacity
    n = len(arr)
    print(f"\nn = {n}, total copies = {arr.copies} (< 2n = {2 * n}), "
          f"total cost = {n + arr.copies} (< 3n = {3 * n})  ⇒ O(1) amortized")

    small = DynamicArray()
    for x in "ACD":
        small.append(x)
    small.insert(1, "B")
    print("\nAfter insert(1, 'B'):", small)
    for _ in range(3):
        small.pop()
    print("After 3 pops (shrinks at n ≤ cap/4):", small)

    print("\nCPython list over-allocation (sys.getsizeof):")
    lst, prev = [], sys.getsizeof([])
    for k in range(40):
        lst.append(k)
        s = sys.getsizeof(lst)
        if s != prev:
            print(f"  len={len(lst):>2} → {s} bytes")
            prev = s
