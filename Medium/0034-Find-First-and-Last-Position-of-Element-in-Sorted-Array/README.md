# 34. Find First and Last Position of Element in Sorted Array

**Difficulty:** 🟡 Medium  
**Tags:** Array, Binary Search  
**Accepted:** 3.3M / 6.8M (48.9%)

---

## Problem

Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value.

If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with `O(log n)` runtime complexity.

 

Example 1:

```
**Input:** nums = [5,7,7,8,8,10], target = 8
**Output:** [3,4]

```

Example 2:

```
**Input:** nums = [5,7,7,8,8,10], target = 6
**Output:** [-1,-1]

```

Example 3:

```
**Input:** nums = [], target = 0
**Output:** [-1,-1]

```

 

**Constraints:**

	
- `0 <= nums.length <= 105`
	
- `-109 <= nums[i] <= 109`
	
- `nums` is a non-decreasing array.
	
- `-109 <= target <= 109`

---

## Similar Problems

- [First Bad Version](https://leetcode.com/problems/first-bad-version/) — Easy
- [Plates Between Candles](https://leetcode.com/problems/plates-between-candles/) — Medium
- [Find Target Indices After Sorting Array](https://leetcode.com/problems/find-target-indices-after-sorting-array/) — Easy

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/*