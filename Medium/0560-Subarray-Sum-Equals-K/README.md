# 560. Subarray Sum Equals K

**Difficulty:** 🟡 Medium  
**Tags:** Array, Hash Table, Prefix Sum  
**Accepted:** 2.5M / 5.3M (47.6%)

---

## Problem

Given an array of integers `nums` and an integer `k`, return *the total number of subarrays whose sum equals to* `k`.

A subarray is a contiguous **non-empty** sequence of elements within an array.

 

Example 1:

```
**Input:** nums = [1,1,1], k = 2
**Output:** 2

```

Example 2:

```
**Input:** nums = [1,2,3], k = 3
**Output:** 2

```

 

**Constraints:**

	
- `1 <= nums.length <= 2 * 104`
	
- `-1000 <= nums[i] <= 1000`
	
- `-107 <= k <= 107`

---

## Hints

<details><summary>Hint 1</summary>

Will Brute force work here? Try to optimize it.

</details>

<details><summary>Hint 2</summary>

Can we optimize it by using some extra space?

</details>

<details><summary>Hint 3</summary>

What about storing sum frequencies in a hash table? Will it be useful?

</details>

<details><summary>Hint 4</summary>

sum(i,j)=sum(0,j)-sum(0,i), where sum(i,j) represents the sum of all the elements from index i to j-1.

Can we use this property to optimize it.

</details>

---

## Similar Problems

- [Two Sum](https://leetcode.com/problems/two-sum/) — Easy
- [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) — Medium
- [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) — Medium
- [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) — Easy
- [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) — Medium
- [Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) — Medium
- [K Radius Subarray Averages](https://leetcode.com/problems/k-radius-subarray-averages/) — Medium
- [Maximum Sum Score of Array](https://leetcode.com/problems/maximum-sum-score-of-array/) — Medium

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/subarray-sum-equals-k/*