"""
10 — Trie (Prefix Tree)
=======================
WHAT
    A tree where each edge is a character and each root-to-node path spells a
    prefix. Words sharing a prefix share nodes. Used for autocomplete, spell
    checking, IP routing (binary tries), and word games.

COMPLEXITY  (L = length of the word / prefix, independent of n = number of words!)
    insert, search, starts_with    O(L)
    compare: BST of strings        O(L · log n)
             hash set              O(L) average, but no prefix queries

SPACE
    Number of nodes   ≤ 1 + Σ_{i=1}^{n} |w_i|        (equality when no prefixes are shared)
    Nodes at depth d  ≤ |Σ|^d                        (Σ = alphabet, |Σ| = 26 for a–z)
    Array children    → nodes · |Σ| pointers  (fast, memory-hungry)
    Dict children     → only existing edges   (what this file uses)

BEHIND THE SCENES
    Each node stores:
        children : dict char → node
        is_end   : True if a word ends here
        count    : number of stored words passing through this node
    count makes "how many words start with p?" an O(|p|) query.
"""


class TrieNode:
    __slots__ = ("children", "is_end", "count")

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0


class Trie:
    def __init__(self, words=()):
        self.root = TrieNode()
        self.nodes = 1
        self.words = 0
        for w in words:
            self.insert(w)

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def insert(self, word):                     # O(L)
        if self.search(word):
            return False
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self.nodes += 1
            node = node.children[ch]
            node.count += 1
        node.is_end = True
        self.words += 1
        return True

    def search(self, word):                     # O(L)
        node = self._walk(word)
        return node is not None and node.is_end

    def count_prefix(self, prefix):             # O(|prefix|)
        if prefix == "":
            return self.words
        node = self._walk(prefix)
        return node.count if node else 0

    def autocomplete(self, prefix, limit=10):
        node = self._walk(prefix)
        out = []

        def dfs(n, path):
            if len(out) >= limit:
                return
            if n.is_end:
                out.append(path)
            for ch in sorted(n.children):
                dfs(n.children[ch], path + ch)

        if node:
            dfs(node, prefix)
        return out

    def delete(self, word):
        if not self.search(word):
            return False
        node = self.root
        for ch in word:
            child = node.children[ch]
            child.count -= 1
            if child.count == 0:                # rest of path belongs only to this word
                self.nodes -= self._subtree_size(child)
                del node.children[ch]
                self.words -= 1
                return True
            node = child
        node.is_end = False
        self.words -= 1
        return True

    def _subtree_size(self, n):
        return 1 + sum(self._subtree_size(c) for c in n.children.values())


if __name__ == "__main__":
    words = ["car", "card", "care", "careful", "cart", "cat", "dog", "dot", "do"]
    t = Trie(words)
    print("search('care')     :", t.search("care"))
    print("search('ca')       :", t.search("ca"), "(only a prefix)")
    print("count_prefix('car'):", t.count_prefix("car"))
    print("autocomplete('car'):", t.autocomplete("car"))
    print("autocomplete('do') :", t.autocomplete("do"))

    total = sum(len(w) for w in words)
    print(f"\nnodes = {t.nodes}  ≤  1 + Σ|w_i| = {1 + total}  (savings from shared prefixes: {1 + total - t.nodes})")

    t.delete("careful")
    print("after delete('careful'):", t.autocomplete("car"), "| nodes =", t.nodes)
