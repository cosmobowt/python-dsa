# =============================================================================
# PYTHON DSA CHEATSHEET  —  built for revision
# Containers + idioms + traps. Algorithms live in patterns.py / templates.py.
# =============================================================================
import sys, math, copy
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop, heapify, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from itertools import permutations, combinations, product, accumulate, pairwise
from functools import lru_cache, cache, cmp_to_key


# =============================================================================
# 0. THE TRAPS  (re-read this section before any interview — these lose points)
# =============================================================================

# T1. Copying a 2D list with a slice is SHALLOW: the inner rows are SHARED.
g = [[1, 2], [3, 4]]
bad = g[:]                          # also: list(g), g.copy()  -> all shallow!
bad[0][0] = 99                      # g is now [[99, 2], [3, 4]]   BUG
ok = [row[:] for row in g]          # correct for 2D (fast, idiomatic)
ok = copy.deepcopy(g)               # correct for any nesting (slow, general)
flat2 = [1, 2, 3][:]                # a slice IS enough for a FLAT list

# T2. 2D init: never multiply a list of lists — every row is the same object.
grid = [[0] * cols for _ in range(rows)]     # RIGHT
# grid = [[0] * cols] * rows                 # WRONG: rows all alias each other

# T3. Backtracking must append a COPY, not the live path object.
res, path = [], [1, 2]
res.append(path)                    # BUG: stores a reference; later mutations show up
res.append(path[:])                 # FIX: snapshot it

# T4. Heap tie on priority compares the NEXT field -> TypeError on objects.
# heappush(h, (dist, node_obj))     # BUG if two dists tie and node isn't comparable
# heappush(h, (dist, idx, node))    # FIX: unique int tiebreak in the middle

# T5. Floor division rounds toward -infinity, not toward zero.
-7 // 2                             # -4   (not -3!)
int(-7 / 2)                         # -3   (truncate toward zero)
-7 % 3                              # 2    (Python mod is always non-negative)

# T6. Mutable default argument persists across calls.
# def f(x, acc=[]):  ...            # BUG: same list every call
# def f(x, acc=None): acc = acc or []   # FIX

# T7. list is unhashable -> can't be a dict key or set member. Use tuple/frozenset.
seen = {(1, 2), frozenset([1, 2])}  # OK      |   {[1,2]} -> TypeError

# T8. {} is an empty DICT. An empty set is set().

# T9. Recursion limit is 1000 and calls are slow. For deep DFS:
sys.setrecursionlimit(10 ** 6)      # ...or rewrite iteratively (preferred)


# =============================================================================
# 1. FAST I/O  (first thing you type in any judge problem)
# =============================================================================
input = sys.stdin.readline                   # replace the slow built-in
n = int(input())                             # one int
a = list(map(int, input().split()))          # a row of ints
# print("\n".join(map(str, out)))            # ONE print, never print in a loop
# data = sys.stdin.buffer.read().split()     # tokenize whole stream (heaviest input)


# =============================================================================
# 2. LIST
# =============================================================================
a = [0] * n                                  # preallocate
a.append(x); a.pop()                         # end ops              O(1)
a.pop(i); a.insert(i, x)                     # middle ops           O(n)
a[-1]                                        # last (no .back())
len(a); a.count(x); a.index(x)               # size / freq / 1st idx
x in a                                       # membership           O(n)
a.remove(x)                                  # delete 1st occurrence O(n)
a += b; a.extend(b)                          # append all
a.reverse(); a[::-1]                         # in place / new copy
max(a); min(a); sum(a)
a.index(max(a))                              # argmax
[x * x for x in a if x > 0]                  # comprehension
for i, x in enumerate(a, start=1): pass      # index+value, custom start
x, y = y, x                                  # swap


# --- SLICING (r is exclusive) ---
a[l:r]; a[:k]; a[-k:]; a[::-1]; a[::2]; a[l:r:step]
a[l:r] = [1, 2]                              # slice ASSIGNMENT splices in place


# =============================================================================
# 3. SORTING
# =============================================================================
a.sort(); a.sort(reverse=True)               # in place, Timsort, STABLE
b = sorted(a)                                # new list
a.sort(key=lambda p: (p[0], -p[1]))          # multi-key: asc p0, then desc p1
a.sort(key=len)                              # by any computed key
a.sort(key=cmp_to_key(cmp))                  # only when order isn't key-expressible
# tuples compare lexicographically -> free multi-key sort, and free heap priority
(1, 2) < (1, 3)                              # True

sorted(d, key=d.get)                         # dict keys by value
sorted(d.items(), key=lambda kv: -kv[1])     # (k,v) pairs by value desc
sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))   # by count desc, then key asc


# =============================================================================
# 4. DICT
# =============================================================================
d[k] = v; d.get(k, 0)                        # write / safe read w/ default
k in d                                       # O(1)
d.pop(k, None); del d[k]
d.setdefault(k, []).append(x)                # get-or-create
for k, v in d.items(): pass
{**d1, **d2}                                 # merge (right wins)

freq = defaultdict(int)                      # missing -> 0
adj = defaultdict(list)                      # missing -> []
cnt = Counter(a)                             # {val: count}
cnt.most_common(k)                           # top-k by count
c1 - c2; c1 & c2; c1 + c2                    # multiset: subtract / min / add
{x: x * x for x in range(3)}                 # dict comprehension


# =============================================================================
# 5. SET
# =============================================================================
s = set()                                    # NOT {}
s.add(x); s.discard(x)                       # discard: no error if absent
x in s                                       # O(1)
A | B; A & B; A - B; A ^ B                   # union / inter / diff / symdiff
A <= B                                       # subset test
{x for x in a if x > 0}                      # set comprehension


# =============================================================================
# 6. STACK / QUEUE / DEQUE
# =============================================================================
st = []; st.append(x); st.pop(); st[-1]      # stack (LIFO)
q = deque(); q.append(x); q.popleft(); q[0]  # queue (FIFO) — popleft is O(1)
# NEVER list.pop(0) for a queue — that's O(n)
dq = deque([1, 2, 3])
dq.appendleft(x); dq.pop(); dq.popleft()     # double-ended
dq.rotate(k)                                 # rotate right by k
deque(maxlen=k)                              # fixed window, auto-evicts


# =============================================================================
# 7. HEAP  (heapq is a MIN-heap)
# =============================================================================
h = []
heappush(h, x); heappop(h); h[0]             # push / pop-min / peek-min  O(log n)
heapify(a)                                   # list -> heap, in place     O(n)
heappush(h, -x); -heappop(h)                 # MAX-heap: negate on both sides
heappush(h, (priority, i, payload))          # tuple sorts by 1st field; i = tiebreak
nlargest(k, a); nsmallest(k, a)              # top-k without a full sort


# =============================================================================
# 8. BINARY SEARCH  (on a SORTED list)
# =============================================================================
bisect_left(a, x)                            # 1st idx >= x   (C++ lower_bound)
bisect_right(a, x)                           # 1st idx >  x   (C++ upper_bound)
bisect_right(a, x) - bisect_left(a, x)       # count of x
insort(a, x)                                 # insert, stay sorted   O(n)
i = bisect_left(a, x); found = i < len(a) and a[i] == x
# Python has NO built-in ordered set/map (no C++ std::set).
# from sortedcontainers import SortedList    # if the judge allows it


# =============================================================================
# 9. STRING  (immutable — build with a list, then join)
# =============================================================================
"".join(chars)                               # list -> str  (the fast way)
s.split(); s.split(","); s.splitlines()
s[l:r]; s[::-1]                              # substring / reverse
s.find("ab")                                 # idx or -1    |  "ab" in s
s.count("a"); s.replace("a", "b"); s.strip()
s.startswith("ab"); s.endswith("z")
s.lower(); s.upper()
ord('a'); chr(97); ord(c) - ord('a')         # char <-> int, alphabet index
c.isdigit(); c.isalpha(); c.isalnum()
f"{x} and {y}"                               # f-string
Counter(s)                                   # char frequency (anagram check: c1 == c2)


# =============================================================================
# 10. NUMBERS
# =============================================================================
INF = float('inf'); NINF = float('-inf')     # or math.inf
divmod(17, 5)                                # (3, 2)
math.gcd(a, b); math.lcm(a, b)
math.isqrt(x)                                # exact int sqrt (no float error)
math.ceil(x); math.floor(x)
math.comb(n, r); math.perm(n, r)             # exact nCr / nPr
pow(b, e, mod)                               # fast modular exponentiation
pow(a, -1, mod)                              # modular inverse (3.8+)
round(x, 2)
# ints are UNBOUNDED: no overflow, no 'long long'


# =============================================================================
# 11. BITS
# =============================================================================
x & 1; x >> 1; x << 1                        # odd? / //2 / *2
x | (1 << k); x & ~(1 << k); x ^ (1 << k)    # set / clear / toggle bit k
(x >> k) & 1                                 # read bit k
x & -x                                       # lowest set bit
x & (x - 1)                                  # clear lowest set bit
x.bit_count(); x.bit_length()                # popcount / high-bit position
bin(x); int("101", 2)                        # to/from binary string
for mask in range(1 << n): pass              # all subsets of n items
sub = mask                                   # all SUBMASKS of mask:
while sub: sub = (sub - 1) & mask


# =============================================================================
# 12. ITERTOOLS + BUILTINS  (free algorithms)
# =============================================================================
permutations(a); permutations(a, k)          # all orderings
combinations(a, k)                           # choose k, order-independent
product([0, 1], repeat=n)                    # cartesian power = all n-bit tuples
list(accumulate(a))                          # PREFIX SUMS in one line
list(accumulate(a, max))                     # running max
list(pairwise(a))                            # [(a0,a1), (a1,a2), ...]
zip(a, b); zip(*pairs)                       # pair up / unzip
all(cond); any(cond)                         # short-circuiting
map(int, xs); filter(None, xs)
reversed(a); sorted(a)


# =============================================================================
# 13. MATRIX IDIOMS
# =============================================================================
R, C = len(g), len(g[0])
[list(r) for r in zip(*g)]                   # TRANSPOSE
[list(r) for r in zip(*g[::-1])]             # rotate 90 CW
[list(r) for r in zip(*g)][::-1]             # rotate 90 CCW
[x for row in g for x in row]                # flatten
for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):        # 4-neighbours
    nr, nc = r + dr, c + dc
    if 0 <= nr < R and 0 <= nc < C: pass     # bounds check
# 8-neighbours: ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))


# =============================================================================
# 14. MEMO / RECURSION
# =============================================================================
@cache                                       # 3.9+; same as lru_cache(maxsize=None)
def f(i, j):
    ...
# args must be HASHABLE -> pass tuples, not lists
# use `nonlocal x` to write an outer variable from a nested dfs()


# =============================================================================
# 15. COMPLEXITY BUDGET  (pick the algorithm from n)
# =============================================================================
#   n <= 11        O(n!)         permutations
#   n <= 22        O(2^n)        subset / bitmask DP
#   n <= 500       O(n^3)        Floyd-Warshall
#   n <= 5,000     O(n^2)        quadratic DP
#   n <= 1e5       O(n log n)    sort / heap / bisect / segment tree
#   n <= 1e6       O(n)          two pointers / prefix sums
#   n >= 1e9       O(log n)      binary search / math
# CPython budget ~1e7 ops/sec (PyPy ~1e8). C++ is ~1e8-1e9.


# =============================================================================
# 16. BOILERPLATE
# =============================================================================
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val; self.next = nxt

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

class Item:                                  # custom object in a heap
    def __init__(self, cost): self.cost = cost
    def __lt__(self, other): return self.cost < other.cost   # makes it heap-safe