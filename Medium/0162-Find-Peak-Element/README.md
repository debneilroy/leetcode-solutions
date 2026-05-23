# 162. Find Peak Element

**Difficulty:** 🟡 Medium  
**Tags:** Array, Binary Search  
**Accepted:** 2.4M / 5.2M (47.0%)

---

## Problem

A peak element is an element that is strictly greater than its neighbors.

Given a **0-indexed** integer array `nums`, find a peak element, and return its index. If the array contains multiple peaks, return the index to **any of the peaks**.

You may imagine that `nums[-1] = nums[n] = -&infin;`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.

You must write an algorithm that runs in `O(log n)` time.

 

Example 1:

```

**Input:** nums = [1,2,3,1]
**Output:** 2
**Explanation:** 3 is a peak element and your function should return the index number 2.
```

Example 2:

```

**Input:** nums = [1,2,1,3,5,6,4]
**Output:** 5
**Explanation:** Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.
```

 

**Constraints:**

	
- `1 <= nums.length <= 1000`
	
- `-231 <= nums[i] <= 231 - 1`
	
- `nums[i] != nums[i + 1]` for all valid `i`.

---

## Similar Problems

- [Peak Index in a Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array/) — Medium
- [Find a Peak Element II](https://leetcode.com/problems/find-a-peak-element-ii/) — Medium
- [Pour Water Between Buckets to Make Water Levels Equal](https://leetcode.com/problems/pour-water-between-buckets-to-make-water-levels-equal/) — Medium
- [Count Hills and Valleys in an Array](https://leetcode.com/problems/count-hills-and-valleys-in-an-array/) — Easy
- [Find the Peaks](https://leetcode.com/problems/find-the-peaks/) — Easy

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/find-peak-element/*