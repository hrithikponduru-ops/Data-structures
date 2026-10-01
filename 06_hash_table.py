"""
06 — Hash Tables (how Python's dict and set work)
=================================================
WHAT
    Map a key to an array index with a hash function, giving O(1) average
    insert / search / delete.

HASH FUNCTIONS
    Division method:        h(k) = k mod m
                            (choose m prime, not close to a power of 2)
    Multiplication method:  h(k) = ⌊ m · (k·A mod 1) ⌋,   A = (√5 − 1) / 2 ≈ 0.6180339887  (Knuth)
    Polynomial (strings):   h(s) = ( Σ_{i=0}^{L−1} s[i] · p^i ) mod M,   e.g. p = 31, M = 10⁹ + 9

LOAD FACTOR
    α = n / m        (n = stored keys, m = table slots)
    Resize (rehash into ≈ 2m slots) when α exceeds a threshold, e.g. 0.75.
    Doubling ⇒ rehash cost is O(1) amortized (same argument as dynamic arrays).

EXPECTED PROBES (uniform hashing assumption)
                          Successful search           Unsuccessful search
    Separate chaining     1 + α/2                     1 + α
    Linear probing        ½ (1 + 1/(1 − α))           ½ (1 + 1/(1 − α)²)
    Double hashing        (1/α) · ln(1/(1 − α))       1/(1 − α)
    → Linear probing explodes as α → 1 (primary clustering).

COLLISIONS ARE UNAVOIDABLE (birthday paradox)
    P(no collision among n keys in m slots) = Π_{i=0}^{n−1} (1 − i/m) ≈ e^{−n(n−1)/(2m)}
    For m = 365, n = 23  ⇒  P(collision) ≈ 50.7 %

COLLISION STRATEGIES
    Chaining:          each slot holds a list of (key, value) pairs.
    Open addressing:   probe sequence h(k, i) = (h(k) + i) mod m  (linear),
                       (h(k) + c₁i + c₂i²) mod m (quadratic),
                       (h₁(k) + i·h₂(k)) mod m (double hashing).

BEHIND THE SCENES IN CPYTHON
    dict uses open addressing with perturbed probing
        j = (5·j + 1 + perturb) mod 2^k,   perturb >>= 5
    and keeps α ≤ 2/3. Keys must be hashable (immutable) so h(k) never changes.
"""
import math
import random


class ChainedHashMap:
    def __init__(self, m=8, max_load=0.75):
        self.m, self.n, self.max_load = m, 0, max_load
        self.buckets = [[] for _ in range(m)]
        self.rehashes = 0

    def _h(self, key):
        return hash(key) % self.m                   # division method

    @property
    def load_factor(self):
        return self.n / self.m                      # α = n / m

    def put(self, key, val):
        bucket = self.buckets[self._h(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, val)              # update existing key
                return
        bucket.append((key, val))
        self.n += 1
        if self.load_factor > self.max_load:
            self._rehash(2 * self.m)

    def get(self, key, default=None):
        for k, v in self.buckets[self._h(key)]:
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self.buckets[self._h(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.n -= 1
                return True
        return False

    def _rehash(self, new_m):
        old = self.buckets
        self.m = new_m
        self.buckets = [[] for _ in range(new_m)]
        for bucket in old:
            for k, v in bucket:
                self.buckets[self._h(k)].append((k, v))
        self.rehashes += 1

    def __contains__(self, key):
        return self.get(key, _MISSING) is not _MISSING


_MISSING = object()


def poly_hash(s, p=31, M=10**9 + 9):
    """h(s) = ( Σ s[i] · p^i ) mod M, with 'a'→1, 'b'→2, …"""
    h, power = 0, 1
    for ch in s:
        h = (h + (ord(ch) - ord("a") + 1) * power) % M
        power = (power * p) % M
    return h


def mult_hash(k, m, A=(math.sqrt(5) - 1) / 2):
    """h(k) = ⌊ m · (k·A mod 1) ⌋"""
    return int(m * ((k * A) % 1))


def linear_probing_experiment(m, alpha, trials=4000, seed=1):
    rng = random.Random(seed)
    table = [None] * m
    keys = rng.sample(range(10**9), int(alpha * m))
    succ_total = 0
    for k in keys:
        i, probes = k % m, 1
        while table[i] is not None:
            i, probes = (i + 1) % m, probes + 1
        table[i] = k
        succ_total += probes        # finding k later costs the same probes
    unsucc_total = 0
    for _ in range(trials):
        i, probes = rng.randrange(m), 1
        while table[i] is not None:
            i, probes = (i + 1) % m, probes + 1
        unsucc_total += probes
    return succ_total / len(keys), unsucc_total / trials


if __name__ == "__main__":
    hm = ChainedHashMap()
    for word in "the quick brown fox jumps over the lazy dog".split():
        hm.put(word, hm.get(word, 0) + 1)
    print("Word counts:", {k: v for b in hm.buckets for k, v in b})
    print(f"n={hm.n}, m={hm.m}, α={hm.load_factor:.3f}, rehashes={hm.rehashes}")
    hm.remove("fox")
    print("'fox' in map after remove:", "fox" in hm)

    print("\npoly_hash('abc') =", poly_hash("abc"), " (1·31⁰ + 2·31¹ + 3·31² = 2946)")
    print("Multiplication method, m=16:", [mult_hash(k, 16) for k in range(1, 11)])

    print("\nLinear probing, m = 100003 — measured vs theory")
    print(f"{'α':>5} {'succ':>7} {'½(1+1/(1−α))':>14} {'unsucc':>8} {'½(1+1/(1−α)²)':>15}")
    for a in [0.25, 0.5, 0.75, 0.9]:
        s, u = linear_probing_experiment(100003, a)
        print(f"{a:>5} {s:>7.2f} {0.5 * (1 + 1 / (1 - a)):>14.2f} {u:>8.2f} {0.5 * (1 + 1 / (1 - a) ** 2):>15.2f}")

    m, n = 365, 23
    exact = 1 - math.prod(1 - i / m for i in range(n))
    approx = 1 - math.exp(-n * (n - 1) / (2 * m))
    print(f"\nBirthday paradox (m=365, n=23): exact P(collision)={exact:.4f}, approx={approx:.4f}")
