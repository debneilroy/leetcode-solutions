# 1539. Kth Missing Positive Number

**Difficulty:** 🟢 Easy  
**Tags:** Array, Binary Search  
**Accepted:** 870.7K / 1.4M (63.6%)

---

## Problem

Given an array `arr` of positive integers sorted in a **strictly increasing order**, and an integer `k`.

Return *the* `kth` ***positive** integer that is **missing** from this array.*

 

Example 1:

```

**Input:** arr = [2,3,4,7,11], k = 5
**Output:** 9
**Explanation: **The missing positive integers are [1,5,6,8,9,10,12,13,...]. The 5th missing positive integer is 9.

```

Example 2:

```

**Input:** arr = [1,2,3,4], k = 2
**Output:** 6
**Explanation: **The missing positive integers are [5,6,7,...]. The 2nd missing positive integer is 6.

```

 

**Constraints:**

	
- `1 <= arr.length <= 1000`
	
- `1 <= arr[i] <= 1000`
	
- `1 <= k <= 1000`
	
- `arr[i] < arr[j]` for `1 <= i < j <= arr.length`

 

**Follow up:**

Could you solve this problem in less than O(n) complexity?

---

## Hints

<details><summary>Hint 1</summary>

Keep track of how many positive numbers are missing as you scan the array.

</details>

---

## Similar Problems

- [Append K Integers With Minimal Sum](https://leetcode.com/problems/append-k-integers-with-minimal-sum/) — Medium

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/kth-missing-positive-number/*