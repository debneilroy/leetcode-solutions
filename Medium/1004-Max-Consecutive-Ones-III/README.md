# 1004. Max Consecutive Ones III

**Difficulty:** 🟡 Medium  
**Tags:** Array, Binary Search, Sliding Window, Prefix Sum  
**Accepted:** 1.4M / 2.1M (67.7%)

---

## Problem

Given a binary array `nums` and an integer `k`, return *the maximum number of consecutive *`1`*'s in the array if you can flip at most* `k` `0`'s.

 

Example 1:

```

**Input:** nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
**Output:** 6
**Explanation:** [1,1,1,0,0,**1**,1,1,1,1,**1**]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
```

Example 2:

```

**Input:** nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
**Output:** 10
**Explanation:** [0,0,1,1,**1**,**1**,1,1,1,**1**,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

```

 

**Constraints:**

	
- `1 <= nums.length <= 105`
	
- `nums[i]` is either `0` or `1`.
	
- `0 <= k <= nums.length`

---

## Hints

<details><summary>Hint 1</summary>

One thing's for sure, we will only flip a zero if it extends an existing window of 1s. Otherwise, there's no point in doing it, right? Think Sliding Window!

</details>

<details><summary>Hint 2</summary>

Since we know this problem can be solved using the sliding window construct, we might as well focus in that direction for hints. Basically, in a given window, we can never have > K zeros, right?

</details>

<details><summary>Hint 3</summary>

We don't have a fixed size window in this case. The window size can grow and shrink depending upon the number of zeros we have (we don't actually have to flip the zeros here!).

</details>

<details><summary>Hint 4</summary>

The way to shrink or expand a window would be based on the number of zeros that can still be flipped and so on.

</details>

---

## Similar Problems

- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) — Medium
- [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) — Medium
- [Max Consecutive Ones](https://leetcode.com/problems/max-consecutive-ones/) — Easy
- [Max Consecutive Ones II](https://leetcode.com/problems/max-consecutive-ones-ii/) — Medium
- [Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) — Medium
- [Maximize the Confusion of an Exam](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/) — Medium
- [Minimum Recolors to Get K Consecutive Black Blocks](https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/) — Easy
- [Longest Nice Subarray](https://leetcode.com/problems/longest-nice-subarray/) — Medium
- [Maximum Sum of Distinct Subarrays With Length K](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/) — Medium
- [Maximum Enemy Forts That Can Be Captured](https://leetcode.com/problems/maximum-enemy-forts-that-can-be-captured/) — Easy

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/max-consecutive-ones-iii/*