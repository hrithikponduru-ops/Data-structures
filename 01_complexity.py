"""
01 — Complexity Analysis (Big-O)
================================
WHAT
    A way to describe how running time / memory grows with input size n.
    Every data structure below is judged with this language.

FORMAL DEFINITIONS
    f(n) = O(g(n))  ⇔  ∃ c > 0, n₀ ≥ 1 :  0 ≤ f(n) ≤ c·g(n)   ∀ n ≥ n₀     (upper bound)
    f(n) = Ω(g(n))  ⇔  ∃ c > 0, n₀ ≥ 1 :  f(n) ≥ c·g(n) ≥ 0   ∀ n ≥ n₀     (lower bound)
    f(n) = Θ(g(n))  ⇔  f(n) = O(g(n))  and  f(n) = Ω(g(n))                (tight bound)

KEY SUMS (used throughout data-structure analysis)
    Arithmetic:  Σ_{i=1}^{n} i     = n(n + 1) / 2                → Θ(n²)
                 Σ_{i=0}^{n−1} i   = n(n − 1) / 2                → Θ(n²)
    Geometric:   Σ_{i=0}^{k} 2^i   = 2^{k+1} − 1                 → Θ(2^k)
    Harmonic:    H_n = Σ_{i=1}^{n} 1/i ≈ ln n + γ   (γ ≈ 0.5772)  → Θ(log n)
    Log base:    log_b(n) = log₂(n) / log₂(b)   ⇒ base is irrelevant in Big-O

BEHIND THE SCENES
    We count "basic operations" (comparisons, assignments, memory reads).
    Constants and lower-order terms vanish because the highest-order term
    dominates for large n:
        3n² + 5n + 7 = O(n²)   since   3n² + 5n + 7 ≤ 15n²   for all n ≥ 1.

COMMON GROWTH ORDER
    O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
"""
import math


def linear_ops(n):
    """One loop → n operations → Θ(n)."""
    ops = 0
    for _ in range(n):
        ops += 1
    return ops


def quadratic_ops(n):
    """Triangular nested loop → Σ_{i=0}^{n−1} i = n(n − 1)/2 → Θ(n²)."""
    ops = 0
    for i in range(n):
        for _ in range(i):
            ops += 1
    return ops


def log_ops(n):
    """Halve until 1 → ⌊log₂ n⌋ steps → Θ(log n)."""
    ops = 0
    while n > 1:
        n //= 2
        ops += 1
    return ops


if __name__ == "__main__":
    print(f"{'n':>6} {'log ops':>8} {'⌊log₂n⌋':>8} {'linear':>7} {'quad ops':>9} {'n(n−1)/2':>9}")
    for n in [8, 16, 64, 256, 1024]:
        print(f"{n:>6} {log_ops(n):>8} {math.floor(math.log2(n)):>8} "
              f"{linear_ops(n):>7} {quadratic_ops(n):>9} {n * (n - 1) // 2:>9}")

    k = 10
    print(f"\nGeometric: Σ_(i=0..{k}) 2^i = {sum(2**i for i in range(k + 1))}  vs  2^(k+1) − 1 = {2**(k + 1) - 1}")

    n = 10**6
    H = sum(1 / i for i in range(1, n + 1))
    print(f"Harmonic:  H_n (n=10^6) = {H:.6f}   vs   ln n + γ = {math.log(n) + 0.5772156649:.6f}")
