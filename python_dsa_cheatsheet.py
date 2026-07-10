# ============================================================
# PYTHON DSA CHEATSHEET  (syntax you reach for mid-problem)
# Algorithms live in patterns.py / templates.py. This is containers only.
# ============================================================
import sys
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right, insort
from functools import lru_cache
import math


# ---------- FAST I/O (write this first, every time) ----------
input = sys.stdin.readline                      # slow built-in -> fast
n = int(input())                                # one int
a = list(map(int, input().split()))             # a row of ints
# print("\n".join(map(str, results)))           # batch output, one call
# data = sys.stdin.buffer.read().split()        # tokenize whole stream


# ---------- LIST (dynamic array) ----------
a = [1, 2, 3, 4, 5]
a = [0] * n                                     # size n, all zeros
grid = [[0] * cols for _ in range(rows)]        # 2D. NEVER [[0]*c]*r (shared row)

a.append(x)                                     # add to end       O(1)
a.pop()                                         # remove+return last O(1)
a.pop(i)                                        # remove+return at i O(n)
a.insert(i, x)                                  # insert at i        O(n)
a[-1]                                           # last element (no .back())
len(a); a.count(x); a.index(x)                  # size / freq / first index
x in a                                          # membership        O(n)

a.sort(); a.sort(reverse=True)                  # in place
a.sort(key=lambda p: (p[0], -p[1]))             # multi-key: asc, then desc
b = sorted(a)                                   # new sorted list
a.reverse(); rev = a[::-1]                      # reverse
a + b; a.extend(b)                              # concat / append-all
max(a); min(a); sum(a)                          # aggregates
[x * x for x in a if x > 0]                     # comprehension
for i, x in enumerate(a): pass                  # index + value
x, y = y, x                                     # swap


# ---------- SLICING ----------
a[l:r]        # [l, r)          a[:k]   # first k       a[-k:]  # last k
a[::-1]       # reversed        a[::2]  # every 2nd      a[l:r:s]


# ---------- DICT (hash map) ----------
d = {}
d[k] = v                                        # set / update
d.get(k, 0)                                     # safe read w/ default
k in d                                          # key check         O(1)
d.pop(k, None); del d[k]                        # remove
for k, v in d.items(): pass
freq = defaultdict(int)                         # missing key -> 0
groups = defaultdict(list)                      # missing key -> []
cnt = Counter(a)                                # {val: count}
cnt.most_common(3)                              # top-3 by count


# ---------- SET (unique) ----------
s = set()                                       # {} is a dict!
s.add(x); s.discard(x)                          # discard = no error if absent
x in s                                          # O(1)
A | B; A & B; A - B; A ^ B                       # union/inter/diff/symdiff


# ---------- STACK / QUEUE / DEQUE ----------
st = []; st.append(x); st.pop(); st[-1]         # stack (LIFO) on a list
q = deque(); q.append(x); q.popleft(); q[0]     # queue (FIFO); popleft O(1)
dq = deque()                                    # double-ended
dq.appendleft(x); dq.pop(); dq.popleft()
deque(maxlen=k)                                 # fixed window, auto-drops


# ---------- HEAP (heapq = MIN-heap) ----------
h = []
heappush(h, x); heappop(h); h[0]                # push / pop-min / peek-min
heapify(a)                                      # list -> heap in O(n)
heappush(h, -x); -heappop(h)                    # MAX-heap: negate
heappush(h, (priority, item))                   # sorts by first field


# ---------- BINARY SEARCH (sorted list) ----------
bisect_left(a, x)                               # first idx >= x  (lower_bound)
bisect_right(a, x)                              # first idx >  x  (upper_bound)
insort(a, x)                                    # insert, keep sorted  O(n)
i = bisect_left(a, x); found = i < len(a) and a[i] == x


# ---------- STRING (immutable: build via list + join) ----------
"".join(chars)                                  # list -> str (the fast way)
s.split(); s.split(",")                         # -> list of tokens
s[l:r]                                          # substring by slice
s.find("ab")                                    # index or -1;  "ab" in s
s.replace("a", "b"); s.strip()
s.lower(); s.upper()
ord('a'); chr(97); ord(c) - ord('a')            # char <-> int, alphabet index
c.isdigit(); c.isalpha(); c.isalnum()
str(42); int("42")                              # int <-> str


# ---------- NUMBERS ----------
INF = float('inf'); NINF = float('-inf')
7 // 2      # 3    |   -7 // 2   # -4  (floors toward -inf!)
int(-7 / 2) # -3   (truncate toward zero instead)
divmod(17, 5)                                   # (3, 2)
math.gcd(a, b); math.lcm(a, b); math.isqrt(x)   # exact int sqrt
pow(b, e, mod)                                  # fast modular exponentiation
pow(a, -1, mod)                                 # modular inverse (3.8+)
# ints are unbounded: no overflow, no need for 'long'


# ---------- BITS ----------
x & 1; x >> 1; x << 1                            # odd? / //2 / *2
x | (1 << k); x & ~(1 << k); x ^ (1 << k)       # set / clear / toggle bit k
(x >> k) & 1                                    # read bit k
x.bit_count(); x.bit_length()                   # popcount / high-bit pos
sub = mask                                      # iterate submasks of mask:
while sub: sub = (sub - 1) & mask


# ---------- MEMOIZATION ----------
@lru_cache(maxsize=None)                         # top-down DP cache
def f(state):
    ...


# ---------- BOILERPLATE STRUCTS (start of list/tree problems) ----------
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val; self.next = nxt

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
