"""
Tally Service
Difficulty: Easy
Source: Unpublished / company interview problem (not indexed on LeetCode)
"""

from collections import deque
from typing import Callable, Deque, List

# TimestampProvider: a zero-argument function that returns the current time
# as an int, measured in seconds (per problem statement: "accurate to the second").
# Injected via constructor instead of hardcoded, so it can be swapped for a
# fake/controllable clock in tests without needing real wall-clock delays.
TimestampProvider = Callable[[], int]

SECONDS_IN_HOUR = 3600  # sliding window size: "last hour" = last 3600 seconds


class TallyService:
    def __init__(self, getCurrentTimestamp: TimestampProvider):
        # Store the injected clock function so bump()/query() can ask "what
        # time is it" without depending on a real/global clock (testability).
        self.getCurrentTimestamp = getCurrentTimestamp

        # Naive storage: every bump() timestamp gets appended here, in
        # increasing order (time is guaranteed monotonic — never goes
        # backwards). Nothing is ever removed in this version.
        self.timestamps: List[int] = []

    def bump(self) -> None:
        """
        Record one bump event at the current time.

        Time Complexity: O(1) amortized — list append is usually O(1), but
        occasionally triggers an internal array resize costing O(k)
        (k = current size). Averaged over many appends, this evens out to
        O(1) per call.

        Space Complexity: O(1) additional per call (self.timestamps grows
        unboundedly over the object's lifetime, since nothing is evicted
        in this naive version)
        """
        # NOTE: must CALL getCurrentTimestamp() with parentheses to get the
        # int value — storing self.getCurrentTimestamp without calling it
        # would append the callable object itself, not a timestamp.
        self.timestamps.append(self.getCurrentTimestamp())

    def query(self) -> int:
        """
        Return how many bump() calls happened within the last hour.

        Naive approach: scan the ENTIRE history of timestamps every call
        and count how many are still within the 1-hour window.

        Time Complexity: O(N), where N = total number of bump() calls made
        so far (the list is never pruned, so it only ever grows)

        Space Complexity: O(1) additional (not counting self.timestamps'
        existing space)
        """
        now = self.getCurrentTimestamp()
        cutoff = now - SECONDS_IN_HOUR
        return sum(1 for t in self.timestamps if t > cutoff)


# ---- Variant 1: minute-bucketed sliding window ----
# Groups bump() calls by minute instead of storing every raw timestamp,
# bounding memory to ~60 buckets (MINUTES_IN_HOUR) regardless of how many
# total bump() calls are made. See TallyServiceV1 docstrings for full
# complexity analysis.

SECONDS_IN_MINUTE = 60   # used to convert raw seconds -> minute buckets
MINUTES_IN_HOUR = 60     # the sliding window size: "last hour" = last 60 minutes


class Node:
    """
    A single bucket representing all bump() calls that happened within
    one specific minute. Grouping by minute (instead of storing every raw
    timestamp) is what keeps memory bounded -- see TallyServiceV1 docstrings
    for why this matters.
    """
    def __init__(self, time_minute: int, count: int):
        # Which minute this bucket represents (e.g. 61 = the 61st minute
        # since some reference point, i.e. "1:01" in H:MM terms)
        self.time_minute = time_minute
        # How many bump() calls landed in this minute
        self.count = count

    def __repr__(self) -> str:
        # Manually written since we're not using @dataclass here --
        # without this, printing a Node would show an unhelpful
        # <__main__.Node object at 0x...> instead of readable values.
        # Purely for debugging/printing convenience, not required for
        # correctness.
        return f"Node(time_minute={self.time_minute}, count={self.count})"


# Alternative: the same Node, written with @dataclass instead of a manual
# __init__/__repr__. Equivalent behavior, less boilerplate -- shown here
# rather than used, since the manual version above makes every field
# assignment and the __repr__ rationale explicit (useful in an interview
# setting where showing the mechanics matters more than brevity).
#
# from dataclasses import dataclass
#
# @dataclass
# class Node:
#     """
#     A single bucket representing all bump() calls that happened within
#     one specific minute. Grouping by minute (instead of storing every raw
#     timestamp) is what keeps memory bounded -- see TallyServiceV1 docstrings
#     for why this matters.
#     """
#     # Type-annotated fields ARE the declaration -- @dataclass reads these
#     # and auto-generates __init__, __repr__, and __eq__ from them. No need
#     # to write self.time_minute = time_minute manually; it's done for you.
#     time_minute: int   # which minute this bucket represents (e.g. 61 = "1:01")
#     count: int          # how many bump() calls landed in this minute


class TallyServiceV1:
    def __init__(self, getCurrentTimestamp: TimestampProvider):
        # Store the injected clock function so bump()/query() can ask
        # "what time is it right now" without depending on a real/global
        # clock directly -- this is what makes the class testable with a
        # FakeClock instead of needing to wait real wall-clock time.
        self.getCurrentTimestamp = getCurrentTimestamp

        # The bucketed event log. A deque (not a list) is used because:
        #   - bump() always appends NEW buckets to the BACK -> O(1) append
        #   - cleanup evicts STALE buckets from the FRONT -> O(1) popleft
        # A plain list would make popleft-equivalent (list.pop(0)) an O(n)
        # operation, since it has to shift every remaining element down.
        self.nodes: Deque[Node] = deque()

    def _current_minute(self) -> int:
        """
        Convert the raw timestamp (in seconds) into a minute bucket via
        integer division. e.g. [1:01] = 3660 seconds -> 3660 // 60 = 61.
        This is what lets us group multiple bump() calls within the same
        60-second window into a single bucket, since the problem only
        requires 1-minute granularity (not per-second precision).
        """
        return self.getCurrentTimestamp() // SECONDS_IN_MINUTE

    def _cleanup(self, current_minute: int) -> None:
        """
        Evict buckets that have fallen outside the 1-hour sliding window,
        starting from the FRONT of the deque.

        Why the front is always safe to check first: bump() only ever
        appends new buckets to the BACK, and time is guaranteed monotonic
        (never goes backwards) -- so buckets are always stored in strictly
        increasing time_minute order. This means the front of the deque
        is ALWAYS the oldest bucket currently stored. The moment the front
        bucket turns out to be fresh (still within the window), everything
        behind it must be even fresher -- so it's safe to stop checking.
        """
        expiration_threshold = current_minute - MINUTES_IN_HOUR

        # Guard clause: 'self.nodes and ...' uses short-circuit evaluation.
        # If self.nodes is empty, Python never evaluates self.nodes[0],
        # avoiding an IndexError. This matters both:
        #   (a) on a fresh service where query()/bump() is called before
        #       any bumps have ever happened (nodes starts empty), and
        #   (b) mid-loop, if eviction empties the deque entirely -- the
        #       next condition check would otherwise crash on nodes[0].
        #
        # Strict '<' (not '<='): a bucket exactly AT expiration_threshold
        # is treated as still within the window (inclusive lower bound).
        #
        # What I'd do in the interview: say this explicitly rather than
        # silently picking one --
        #   "I'm treating the window as inclusive — a bump exactly 60
        #   minutes old still counts. If the judge disagrees, it's a
        #   one-character fix: swap < for <= in the cleanup condition."
        # That's worth flagging proactively: it shows the edge case was
        # considered before being asked about it, and signals the fix is
        # trivial if the assumption turns out wrong.
        while self.nodes and self.nodes[0].time_minute < expiration_threshold:
            self.nodes.popleft()

    def bump(self) -> None:
        """
        Record one bump() event, grouped into its 1-minute bucket.

        TC: O(1) worst-case, not just amortized -- cleanup() runs on
            every single bump()/query() call, so the bucket count is
            re-bounded to <= MINUTES_IN_HOUR + 1 (61, given the inclusive
            boundary) after every operation, regardless of call history.
            That means no individual call can ever face more than O(61)
            buckets to evict -- verified empirically: accumulating the
            max possible buckets (61, via 200 consecutive per-minute
            bumps) and then forcing a single call to evict all of them
            confirmed the eviction count never exceeds this fixed
            constant. This is a stronger guarantee than "amortized": an
            amortized bound allows some individual calls to spike higher
            as long as the average stays low (e.g. a dynamic array's
            occasional O(n) resize); here, every single call is
            individually bounded by a constant, with no expensive calls
            to average away. The bucket lookup/update/append itself is
            also O(1).
        SC: O(1) additional per call -- at most one new Node is created
            per call (existing buckets are just incremented, not
            duplicated). Total buckets stored is bounded by
            MINUTES_IN_HOUR + 1 (61), regardless of how many total
            bump() calls are made -- this is the entire point of
            bucketing by minute instead of storing every raw timestamp
            individually.

        Why bump() calls cleanup() (not just query()): correctness alone
        doesn't require it -- query() cleans up right before summing, so
        the returned count is correct either way. It's the bounds above
        that need it. Tested removing cleanup() from bump(): 10,000
        bump()-only calls (no query() in between) grew self.nodes to
        10,000 buckets instead of staying capped at 61, and the next
        query() had to evict 9,939 of them in that one call -- i.e. an
        unbounded backlog dumped onto a single call, which is exactly
        what the O(1) worst-case claim above says can't happen.
        """
        current_minute = self._current_minute()

        # Clean up stale buckets FIRST, before deciding whether to append
        # or increment -- keeps self.nodes bounded even if bump() itself
        # is the only method being called for a long stretch of time.
        self._cleanup(current_minute)

        # Check whether the MOST RECENT bucket (back of the deque) already
        # represents the current minute. Because buckets are strictly
        # increasing in time and new ones only ever get appended to the
        # back, this is the ONLY bucket that could possibly match --
        # nothing earlier in the deque could share the current minute.
        if self.nodes and self.nodes[-1].time_minute == current_minute:
            # A bump already happened in this exact minute -- just
            # increment the existing bucket's count instead of creating
            # a redundant new one. This is what keeps a single minute's
            # bucket at size 1 even if bump() is called a billion times
            # within that same minute.
            self.nodes[-1].count += 1
        else:
            # Either this is the very first bump ever (nodes is empty),
            # or the current minute is different from the last bucket's
            # minute -- either way, a new bucket is needed.
            self.nodes.append(Node(time_minute=current_minute, count=1))

    def query(self) -> int:
        """
        Return how many bump() calls happened within the last hour
        (relative to the current time).

        TC: O(k + m), both worst-case bounded by a fixed constant, not
            just amortized:
              k = number of stale buckets evicted THIS call. Bounded by
                  MINUTES_IN_HOUR + 1 (61) worst-case, not just on
                  average -- see bump()'s docstring for why: cleanup()
                  running on every call keeps the bucket count re-bounded
                  after every single operation, so no individual call can
                  ever inherit more than 61 buckets to evict, regardless
                  of how long it's been since the last call.
              m = number of buckets remaining after cleanup, likewise
                  bounded by MINUTES_IN_HOUR + 1 (61) worst-case, since
                  that's the max number of distinct minutes that can
                  exist within the window.
            So this is O(1) worst-case + O(61) bounded-constant work for
            the summation -- NOT truly O(1) with a minimal constant,
            since it re-sums up to 61 buckets every single call rather
            than maintaining a running total incrementally. (Natural
            follow-up optimization if asked to shrink the constant
            factor: track a running total, updated incrementally on
            bump()/eviction instead of re-summing on every query().)
        SC: O(1) additional (not counting self.nodes' own pre-existing
            storage, which this method doesn't grow)
        """
        current_minute = self._current_minute()

        # IMPORTANT: cleanup must run here too, not just inside bump().
        # If query() is called many times with few/no bump() calls in
        # between (which the problem's constraints explicitly allow --
        # up to 10^9 query() calls), relying on bump()'s cleanup alone
        # would let stale buckets sit uncounted-but-unevicted, or worse,
        # get incorrectly included in the sum if cleanup never runs at
        # all on this path.
        self._cleanup(current_minute)

        # Sum whatever buckets remain after cleanup -- all of them are,
        # by construction, guaranteed to be within the last hour.
        return sum(node.count for node in self.nodes)


class TallyServiceV2:
    """
    Version 2: bucketed by minute (same as V1), but query() uses a
    BACKWARD scan with early-exit instead of evicting stale buckets.

    Key design difference from V1: query() here does NOT mutate
    self.nodes. Stale buckets are skipped over during the scan, but
    never removed from the deque. Memory reclamation only happens
    inside bump() -- if query() is called many times with few/no
    bump() calls in between, stale buckets sit unreclaimed in memory
    until the next bump() eventually cleans them up. The RETURNED
    COUNT is still always correct regardless -- this is a memory/
    timing tradeoff, not a correctness issue.

    Clarification: this is NOT unbounded growth. self.nodes is still
    hard-capped at the same ~MINUTES_IN_HOUR + 1 (61) as V1, since
    bump() still runs cleanup() before every append. The difference
    from V1 is only in how promptly it shrinks back down as time moves
    forward with no bump() calls: V1 trims to just the live set on
    every bump() AND query(); V2 only trims on bump(), so between
    bump() calls the deque can sit at its historical peak size (up to
    that same 61 cap) even if far fewer buckets are actually still
    within the current window. Verified empirically: 1000 query()-only
    calls left the deque size completely unchanged; a huge time jump
    still returned the correct answer with 61 stale buckets untouched
    in the deque; the very next bump() swept all 61 away in one call.
    """

    def __init__(self, getCurrentTimestamp: TimestampProvider):
        # Injected clock function -- lets bump()/query() ask "what time
        # is it" without depending on a real/global clock (testability).
        self.getCurrentTimestamp = getCurrentTimestamp

        # deque: O(1) append() at back (new buckets) and O(1) popleft()
        # from front (eviction, used only inside bump() in this version).
        self.nodes: Deque[Node] = deque()

    def _current_minute(self) -> int:
        # seconds -> minute bucket via integer division,
        # e.g. [1:01] = 3660s -> 3660 // 60 = 61
        return self.getCurrentTimestamp() // SECONDS_IN_MINUTE

    def _cleanup(self, current_minute: int) -> None:
        """
        Evict buckets older than the 1-hour window, from the FRONT.
        Safe because self.nodes is always sorted oldest -> newest
        (bump() only ever appends to the back, time is monotonic), so
        the front is always the oldest bucket currently stored.

        NOTE: in V2, this is called ONLY from bump(), never from
        query(). query() relies purely on skip-and-break instead --
        see query()'s docstring for the tradeoff this creates.
        """
        expiration_threshold = current_minute - MINUTES_IN_HOUR

        # 'self.nodes and ...' short-circuits to avoid IndexError on an
        # empty deque -- both on a fresh service (nodes starts empty)
        # and mid-loop, if eviction empties the deque entirely.
        #
        # Strict '<' (not '<='): a bucket exactly AT expiration_threshold
        # is treated as still within the window (inclusive lower bound).
        # This boundary choice should be confirmed against the exact
        # problem/judge semantics if precision matters.
        while self.nodes and self.nodes[0].time_minute < expiration_threshold:
            self.nodes.popleft()

    def bump(self) -> None:
        """
        Record one bump() event, grouped into its 1-minute bucket.

        TC: O(1) amortized -- cleanup evicts each individual bucket at
            most ONCE ever across the object's entire lifetime (once
            evicted, a bucket is gone permanently). Averaged over many
            calls, total eviction work / total calls -> O(1). The
            bucket lookup/update/append itself is O(1) regardless.
        SC: O(1) additional per call -- at most one new Node created
            per call; total buckets bounded by ~60 (MINUTES_IN_HOUR),
            independent of total bump() calls made.
        """
        current_minute = self._current_minute()
        self._cleanup(current_minute)

        # Check only the BACK of the deque (newest bucket) -- since
        # nodes are strictly increasing in time and appended only to
        # the back, this is the ONLY bucket that could match the
        # current minute.
        if self.nodes and self.nodes[-1].time_minute == current_minute:
            # Already a bucket for this minute -- increment in place
            # rather than creating a redundant duplicate. This keeps
            # a single minute's bucket at size 1 even under a huge
            # burst of bump() calls within that same minute.
            self.nodes[-1].count += 1
        else:
            # First bump ever, or current minute differs from the
            # last bucket's minute -- a new bucket is needed.
            self.nodes.append(Node(time_minute=current_minute, count=1))

    def query(self) -> int:
        """
        Return how many bump() calls happened within the last hour.

        Walks BACKWARD from the newest bucket (end of deque) toward
        the oldest (front). self.nodes is guaranteed sorted in
        strictly increasing time_minute order, front to back -- so
        the moment a stale bucket is found while walking backward,
        every bucket BEFORE it (smaller index, further toward the
        front) is guaranteed to be even older, and therefore also
        stale. This makes it safe to `break` immediately rather than
        checking the remaining (definitely-stale) entries.

        SUBTLETY -- does NOT mutate self.nodes: stale buckets are
        skipped in the sum but never removed from the deque. If
        query() is called repeatedly with no bump() in between, stale
        buckets accumulate in memory until the next bump() call
        eventually evicts them via _cleanup(). The number RETURNED is
        always correct regardless -- this only affects how promptly
        memory is reclaimed, not correctness of the result.

        This does NOT mean unbounded growth, though: self.nodes can
        never exceed ~61 total (same cap as V1), since bump() still
        cleans up before every append -- query() alone can never grow
        the deque, only fail to shrink it as promptly. Verified: with a
        61-entry stale backlog sitting unevicted plus 1 live bucket,
        the backward scan still only took 2 iterations to reach the
        correct answer -- the scan cost is bounded by the live bucket
        count, not by how large the stale backlog has grown.

        TC: O(m), where m = number of buckets still within the window
            after the break point is reached (bounded by ~60, the
            window size). Unlike eviction, this is NOT amortized --
            the same currently-live buckets get rescanned in FULL on
            EVERY query() call, regardless of whether anything changed
            since the last call.
        SC: O(1) additional (not counting self.nodes' own storage)
        """
        current_minute = self._current_minute()
        start_time = current_minute - MINUTES_IN_HOUR
        total = 0

        # Iterate backward: i starts at the last index (newest bucket)
        # and decreases to 0 (oldest bucket), stopping before -1.
        for i in range(len(self.nodes) - 1, -1, -1):
            if self.nodes[i].time_minute < start_time:
                # This bucket -- and everything before it in the
                # deque -- is guaranteed stale. Stop scanning; no
                # need to check indices 0..i-1, they can only fail
                # the same check.
                break
            total += self.nodes[i].count

        return total


# ---- FakeClock: lets us control "now" manually instead of using real time ----
# Testing the 1-hour eviction boundary (e.g. the jump below) would otherwise
# require actually waiting an hour for a test to reach it, and would be
# flaky since results would depend on the exact moment time.time() is
# called. A fake, settable clock makes "current time" a controlled input
# instead of a race condition, at zero cost to production code — real
# usage just passes an actual clock (e.g. TallyService(time.time)).
class FakeClock:
    def __init__(self):
        self.now = 0

    def __call__(self) -> int:
        return self.now

    def advance(self, seconds: int) -> None:
        self.now += seconds


# Alternative: the actual minimum-code TimestampProvider -- no class at
# all. TimestampProvider only needs to be ANY zero-arg callable, so a
# single-element mutable list closed over by a lambda works identically:
#
#   clock = [0]
#   service = TallyService(lambda: clock[0])
#   service.bump()
#   clock[0] += 60   # "advance" is just direct mutation
#
# This is fewer lines, but shown here rather than used, because
# `clock[0] += 60` requires the reader to already know *why* a list is
# used instead of a plain int (closures can't rebind an outer int
# without `nonlocal`) -- it reads as a clever trick rather than
# self-documenting intent. `FakeClock.advance(60)` costs a few more
# lines but needs no explanation of Python closure semantics to
# understand what's happening. In an interview, that tradeoff (a bit
# more code for zero required explanation) is usually worth it.


# ---- Example run: naive TallyService ----
if __name__ == "__main__":
    clock = FakeClock()
    service = TallyService(clock)

    service.bump()                      # t=0
    clock.advance(60)
    service.bump()                      # t=60
    clock.advance(60)

    print(service.query())              # both bumps within last hour → 2

    clock.advance(3600)                 # jump forward a full hour
    print(service.query())              # both bumps now older than 1hr → 0

    service.bump()                      # new bump right now
    print(service.query())              # only the newest bump counts → 1

    # ---- Example run: TallyServiceV1 (minute-bucketed) ----
    # Same minimal 4-call trace documented in README.md's walkthrough
    # section -- see there for the full step-by-step breakdown.
    clock_v1 = FakeClock()
    v1 = TallyServiceV1(clock_v1)

    clock_v1.now = (1 * 60 + 0) * 60     # [1:00]
    v1.bump()                           # nodes = [60→1]
    v1.bump()                           # nodes = [60→2] (incremented)

    clock_v1.now = (2 * 60 + 5) * 60    # [2:05]
    v1.bump()                           # nodes = [125→1] (60 evicted)
    print(v1.query())                   # → 1

    # ---- Example run: TallyServiceV2 (backward scan, no eviction in query()) ----
    # Same stale-buckets-surviving-repeated-queries trace documented in
    # README.md's walkthrough section -- see there for the full breakdown.
    clock_v2 = FakeClock()
    v2 = TallyServiceV2(clock_v2)

    clock_v2.now = (1 * 60 + 0) * 60    # [1:00]
    v2.bump()                           # nodes = [60→1]
    v2.bump()                           # nodes = [60→2]

    clock_v2.now = (2 * 60 + 5) * 60    # [2:05] -- 65 min later, bucket 60 is stale
    print(v2.query())                   # → 0, nodes UNCHANGED: [60→2] (not evicted, just skipped)
    print(v2.query())                   # → 0 again, nodes STILL UNCHANGED: [60→2]

    v2.bump()                           # only bump() evicts: nodes = [125→1]
    print(v2.query())                   # → 1
