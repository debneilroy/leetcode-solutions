# 283. Move Zeroes

**Difficulty:** 🟢 Easy  
**Tags:** Array, Two Pointers  
**Accepted:** 5.2M / 8.1M (63.8%)

---

## Problem

Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

**Note** that you must do this in-place without making a copy of the array.

 

Example 1:

```
**Input:** nums = [0,1,0,3,12]
**Output:** [1,3,12,0,0]

```

Example 2:

```
**Input:** nums = [0]
**Output:** [0]

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`
	
- `-231 <= nums[i] <= 231 - 1`

 

**Follow up:** Could you minimize the total number of operations done?

---

## Hints

<details><summary>Hint 1</summary>

In-place means we should not be allocating any space for extra array. But we are allowed to modify the existing array. However, as a first step, try coming up with a solution that makes use of additional space. For this problem as well, first apply the idea discussed using an additional array and the in-place solution will pop up eventually.

</details>

<details><summary>Hint 2</summary>

A two-pointer approach could be helpful here. The idea would be to have one pointer for iterating the array and another pointer that just works on the non-zero elements of the array.

</details>

---

## Similar Problems

- [Remove Element](https://leetcode.com/problems/remove-element/) — Easy
- [Apply Operations to an Array](https://leetcode.com/problems/apply-operations-to-an-array/) — Easy

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/move-zeroes/*