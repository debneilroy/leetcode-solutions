# 56. Merge Intervals

**Difficulty:** 🟡 Medium  
**Tags:** Array, Sorting  
**Accepted:** 4M / 7.8M (51.8%)

---

## Problem

Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return *an array of the non-overlapping intervals that cover all the intervals in the input*.

 

Example 1:

```

**Input:** intervals = [[1,3],[2,6],[8,10],[15,18]]
**Output:** [[1,6],[8,10],[15,18]]
**Explanation:** Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

```

Example 2:

```

**Input:** intervals = [[1,4],[4,5]]
**Output:** [[1,5]]
**Explanation:** Intervals [1,4] and [4,5] are considered overlapping.

```

Example 3:

```

**Input:** intervals = [[4,7],[1,4]]
**Output:** [[1,7]]
**Explanation:** Intervals [1,4] and [4,7] are considered overlapping.

```

 

**Constraints:**

	
- `1 <= intervals.length <= 104`
	
- `intervals[i].length == 2`
	
- `0 <= starti <= endi <= 104`

---

## Similar Problems

- [Insert Interval](https://leetcode.com/problems/insert-interval/) — Medium
- [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) — Easy
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) — Medium
- [Teemo Attacking](https://leetcode.com/problems/teemo-attacking/) — Easy
- [Add Bold Tag in String](https://leetcode.com/problems/add-bold-tag-in-string/) — Medium
- [Range Module](https://leetcode.com/problems/range-module/) — Hard
- [Employee Free Time](https://leetcode.com/problems/employee-free-time/) — Hard
- [Partition Labels](https://leetcode.com/problems/partition-labels/) — Medium
- [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) — Medium
- [Amount of New Area Painted Each Day](https://leetcode.com/problems/amount-of-new-area-painted-each-day/) — Hard
- [Longest Substring of One Repeating Character](https://leetcode.com/problems/longest-substring-of-one-repeating-character/) — Hard
- [Count Integers in Intervals](https://leetcode.com/problems/count-integers-in-intervals/) — Hard
- [Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) — Medium
- [Determine if Two Events Have Conflict](https://leetcode.com/problems/determine-if-two-events-have-conflict/) — Easy
- [Count Ways to Group Overlapping Ranges](https://leetcode.com/problems/count-ways-to-group-overlapping-ranges/) — Medium
- [Points That Intersect With Cars](https://leetcode.com/problems/points-that-intersect-with-cars/) — Easy
- [Count Days Without Meetings](https://leetcode.com/problems/count-days-without-meetings/) — Medium
- [Minimize Connected Groups by Inserting Interval](https://leetcode.com/problems/minimize-connected-groups-by-inserting-interval/) — Medium

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/merge-intervals/*