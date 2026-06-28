# 347. Top K Frequent Elements

**Difficulty:** 🟡 Medium  
**Tags:** Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue), Bucket Sort, Counting, Quickselect  
**Accepted:** 3.7M / 5.5M (66.7%)

---

## Problem

Given an integer array `nums` and an integer `k`, return *the* `k` *most frequent elements*. You may return the answer in **any order**.

 

Example 1:

**Input:** nums = [1,1,1,2,2,3], k = 2

**Output:** [1,2]

Example 2:

**Input:** nums = [1], k = 1

**Output:** [1]

Example 3:

**Input:** nums = [1,2,1,2,1,2,3,1,3,2], k = 2

**Output:** [1,2]

 

**Constraints:**

	
- `1 <= nums.length <= 105`
	
- `-104 <= nums[i] <= 104`
	
- `k` is in the range `[1, the number of unique elements in the array]`.
	
- It is **guaranteed** that the answer is **unique**.

 

**Follow up:** Your algorithm's time complexity must be better than `O(n log n)`, where n is the array's size.

---

## Similar Problems

- [Word Frequency](https://leetcode.com/problems/word-frequency/) — Medium
- [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) — Medium
- [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) — Medium
- [Split Array into Consecutive Subsequences](https://leetcode.com/problems/split-array-into-consecutive-subsequences/) — Medium
- [Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) — Medium
- [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) — Medium
- [Sort Features by Popularity](https://leetcode.com/problems/sort-features-by-popularity/) — Medium
- [Sender With Largest Word Count](https://leetcode.com/problems/sender-with-largest-word-count/) — Medium
- [Most Frequent Even Element](https://leetcode.com/problems/most-frequent-even-element/) — Easy
- [Linked List Frequency](https://leetcode.com/problems/linked-list-frequency/) — Easy

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/top-k-frequent-elements/*