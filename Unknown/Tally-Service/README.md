# 8. Tally Service

**Difficulty:** 🟢 Easy
**Source:** Unpublished / company interview problem (not indexed on LeetCode)

---

## Problem

Tally is a real-time counter service used at Minmer Headquarters. Design a simplified version of Tally Service. It should support 2 functions, `bump()` and `query()`. `query()` returns the total number of times `bump()` was called in the last hour, with a granularity of 1 minute.

A helper function `getCurrentTimestamp()` can be provided to give current system time in `int`, accurate to the second. You can assume that `bump()` and `query()` will be called in the same process, and that the system time is monotonic (i.e., it will never go backwards).

Example 1:

```
Input:
[1:01],[1:02],[1:10],[1:15],[1:30],[2:05],[2:08],[2:08],[2:08],[3:04]
bump(),bump(),query(),bump(),query(),query(),bump(),bump(),bump(),query()
Output: [2,3,1,3]
Explanation: The first query at 1:10 returns 2
the second query at 1:30 returns 3
The third query at 2:05 returns 1
The fourth query at 3:04 returns 3
```

**Constraints:**

- `bump()` will be called at most 10^9 times per test case.
- `query()` will be called at most 10^9 times per test case.

---

### Walkthrough of Example 1

The `[H:MM]` timestamps here are the platform's illustrative units, not literal seconds — treat each as **elapsed minutes** (`1:10` = 1×60+10 = 70) and the "last hour" window as the last **60** of those units. (In the real problem, `getCurrentTimestamp()` returns real seconds and the window is a literal 3600 seconds — see `solution.py`'s own `FakeClock`-based example for that version.) Walking through the 10 operations in order:

| # | Op | Time (elapsed min) | `timestamps` after | Result |
|---|----|---------------------|---------------------|--------|
| 1 | `bump()` | 61 | `[61]` | — |
| 2 | `bump()` | 62 | `[61, 62]` | — |
| 3 | `query()` | 70 | `[61, 62]` | cutoff = 70−60 = 10 → both `>10` → **2** |
| 4 | `bump()` | 75 | `[61, 62, 75]` | — |
| 5 | `query()` | 90 | `[61, 62, 75]` | cutoff = 90−60 = 30 → all three `>30` → **3** |
| 6 | `query()` | 125 | `[61, 62, 75]` | cutoff = 125−60 = 65 → only `75` qualifies (61, 62 are now too old) → **1** |
| 7–9 | `bump()` ×3 | 128 | `[61, 62, 75, 128, 128, 128]` | — |
| 10 | `query()` | 184 | `[61, 62, 75, 128, 128, 128]` | cutoff = 184−60 = 124 → only the three `128`s qualify (`61, 62, 75` are all `≤124`) → **3** |

Output: `[2, 3, 1, 3]` — matches. The key thing the walkthrough shows: `query()` at step 6 is where the window actually starts evicting old bumps (61 and 62 fall out), which is the case that would break a solution that doesn't correctly re-check every timestamp against a moving cutoff each call.

### Why inject a clock (`FakeClock`) instead of using real time

`TallyService` takes `getCurrentTimestamp` as a constructor argument rather than calling `time.time()` internally. This is a standard dependency-injection pattern for anything time-based:

- **Testability without waiting:** verifying the "last hour" eviction logic (like step 6 above, or the `solution.py` example's jump to `t+3600`) would otherwise require literally waiting real minutes/hours for a test to reach the boundary. `FakeClock` lets a test set `clock.now` to any value instantly.
- **Determinism:** tests that depend on `time.time()` directly are flaky — the exact millisecond execution happens to run at can shift results. A fake clock makes the "current time" a controlled input instead of a race condition.
- **No production behavior change:** in real use, you'd construct `TallyService(time.time)` (or a similar real clock), so the injection point costs nothing at runtime — it only exists to make the class testable.

---

## Solution

See [solution.py](./solution.py)

**Naive approach:** store every `bump()` timestamp in a list; `query()` scans the entire history each call and counts how many timestamps fall within the last hour. O(N) time per query where N = total bumps so far (nothing is ever evicted), O(1) auxiliary space beyond the growing list.

**Variant 1 — minute-bucketed sliding window (`TallyServiceV1`):** groups `bump()` calls into per-minute buckets in a `deque`, evicting stale buckets from the front on both `bump()` and `query()`. Since time is monotonic and buckets are appended in strictly increasing order, the front of the deque is always the oldest bucket. Because `cleanup()` runs on *every* call, the bucket count is re-bounded to ≤ `MINUTES_IN_HOUR` + 1 (61) after every single operation — this makes both `bump()` and `query()`'s eviction step **O(1) worst-case**, not just amortized (verified: forcing a single call to evict the maximum possible backlog of 61 buckets still only evicted 61, never more). `query()` is O(k + m): k = buckets evicted this call (≤61 worst-case), m = buckets remaining after cleanup (≤61 worst-case) — so it's O(1) worst-case plus a bounded-constant sum, not strictly O(1) with a minimal constant (a running total, updated incrementally, would be the natural next optimization to shrink that constant factor).

### Walkthrough of `TallyServiceV1` (minute-bucketed)

**Minimal example: 4 calls**

```
[1:00] bump()
[1:00] bump()
[2:05] bump()
[2:05] query()
```

```
[1:00] bump()
current_minute = 60
_cleanup(60): threshold = 0. nodes empty → nothing evicted.
nodes empty → append.
nodes = [ 60→1 ]

[1:00] bump()  — same minute again
current_minute = 60
_cleanup(60): threshold = 0. Front 60; 60 < 0? No → nothing evicted.
Last bucket (60) == 60 → increment in place.
nodes = [ 60→2 ]

[2:05] bump()
current_minute = 125
_cleanup(125): threshold = 65. Front 60; 60 < 65? Yes → evict. nodes = []
nodes empty → append.
nodes = [ 125→1 ]

[2:05] query()
current_minute = 125
_cleanup(125): threshold = 65. Front 125; 125 < 65? No → nothing evicted.
Sum: 1
Returns 1
```

**Summary table**

| Call | `current_minute` | threshold | `nodes` after | Returned |
|---|---|---|---|---|
| `[1:00] bump()` | 60 | 0 | `[60→1]` | — |
| `[1:00] bump()` | 60 | 0 | `[60→2]` (incremented) | — |
| `[2:05] bump()` | 125 | 65 | `[125→1]` (60 evicted) | — |
| `[2:05] query()` | 125 | 65 | (unchanged) | 1 |

Four calls, every branch touched: append (call 1), increment-in-place (call 2), eviction + append (call 3), and a clean query with no eviction needed (call 4). Should be fast to redraw from memory or on a whiteboard.

**Boundary-semantics note (inclusive vs. exclusive window):** `TallyServiceV1`'s cleanup evicts buckets with `time_minute < expiration_threshold`, which keeps a bucket sitting exactly *at* the threshold — i.e. a bump exactly 60 minutes old still counts. The naive version instead uses `t > cutoff` (strict), which **excludes** a bump exactly 3600 seconds old. These two disagree at that exact boundary (verified: naive returns `0`, V1 returns `1` for a bump made precisely 60 minutes/3600 seconds before the query).

> **What I'd do in the interview:** say this explicitly rather than silently picking one — "I'm treating the window as inclusive — a bump exactly 60 minutes old still counts. If the judge disagrees, it's a one-character fix: swap `<` for `<=` in the cleanup condition." That's worth flagging proactively — it shows the edge case was considered before being asked about it, and signals the fix is trivial if the assumption turns out wrong.

**Variant 2 — backward scan, no eviction in `query()` (`TallyServiceV2`):** same minute-bucketing as V1, but `query()` never mutates `self.nodes`. Instead, it walks the deque **backward** (newest → oldest) and stops the moment it hits a stale bucket — since buckets are strictly increasing in time, everything before that point is guaranteed stale too, so it's safe to break immediately rather than checking the rest. Eviction only happens inside `bump()`.

The tradeoff this creates: if `query()` is called many times with no `bump()` in between, stale buckets sit unreclaimed in the deque until the next `bump()` finally cleans them up. **This is a memory-promptness tradeoff, not a correctness one** — the returned count is always correct regardless, since the backward scan simply stops summing once it reaches anything stale. It's also not *unbounded* growth: `self.nodes` is still hard-capped at ~61 (same as V1), since `bump()` still runs cleanup before every append — the only difference is how promptly it shrinks back down, not how large it can ever get.

Verified empirically:
- 1,000 `query()`-only calls left the deque size completely unchanged (no shrinkage without a `bump()`)
- A huge time jump correctly returned `0` even with 61 stale buckets still sitting, untouched, in the deque
- The very next `bump()` swept all 61 away in a single call
- With a 61-entry stale backlog plus 1 live bucket, the backward scan still took only 2 iterations to reach the correct answer — scan cost is bounded by the *live* bucket count, not by how large the stale backlog has grown

### Walkthrough of `TallyServiceV2` — stale buckets surviving repeated queries

```
[1:00] bump()                    → nodes = [60→1]
[1:00] bump()                    → nodes = [60→2]

[2:05] query()  (65 min later — bucket 60 is now stale)
  threshold = 125 − 60 = 65. Scanning backward, bucket 60 < 65 → stale, break immediately.
  Returns 0. nodes UNCHANGED: [60→2]  ← stale bucket NOT evicted, just skipped

[2:05] query()  (called again, still no bump() in between)
  Same result: 0. nodes STILL UNCHANGED: [60→2]  ← still sitting there

[2:05] bump()  (finally, a bump — this is the only thing that evicts)
  cleanup(125): threshold = 65. Front bucket 60 < 65 → evicted. nodes = []
  nodes empty → append. nodes = [125→1]

[2:05] query()  → 1
```

The two repeated `query()` calls in the middle are the point: both return the correct `0`, and neither one touches `self.nodes` — the stale `60→2` bucket only disappears once an actual `bump()` happens.

---

### Possible next steps

- **Running total (applies to both V1 and V2):** both variants still re-scan/re-sum up to ~61 buckets on every `query()` call — a bounded constant, but not the *smallest* possible one. Maintaining a running total that's incremented on `bump()` and decremented on eviction would shrink both down to a true single-step O(1) per call, with no per-call loop at all. This is a separate change from the V1-vs-V2 distinction above — it's an optimization *on top of* either variant, not an alternative to them.
- **V1 vs. V2 is a genuinely different tradeoff, not a progression:** V1 always keeps `self.nodes` trimmed to exactly the live set (evicts on both `bump()` and `query()`); V2 only evicts on `bump()`, trading slower memory reclamation for a `query()` that never mutates state. Neither one is strictly better — V2 might be preferable if `query()` needs to stay side-effect-free (e.g. for concurrent reads), while V1 keeps memory usage minimal at all times.
