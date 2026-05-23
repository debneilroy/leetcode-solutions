# 1216. Valid Palindrome III

**Difficulty:** 🔴 Hard  
**Tags:** String, Dynamic Programming  
**Accepted:** 109.2K / 222K (49.2%)

---

## Problem

Given a string `s` and an integer `k`, return `true` if `s` is a `k`**-palindrome**.

A string is `k`**-palindrome** if it can be transformed into a palindrome by removing at most `k` characters from it.

 

Example 1:

```

**Input:** s = "abcdeca", k = 2
**Output:** true
**Explanation:** Remove 'b' and 'e' characters.

```

Example 2:

```

**Input:** s = "abbababa", k = 1
**Output:** true

```

 

**Constraints:**

	
- `1 <= s.length <= 1000`
	
- `s` consists of only lowercase English letters.
	
- `1 <= k <= s.length`

---

## Hints

<details><summary>Hint 1</summary>

Can you reduce this problem to a classic problem?

</details>

<details><summary>Hint 2</summary>

The problem is equivalent to finding any palindromic subsequence of length at least N-K where N is the length of the string.

</details>

<details><summary>Hint 3</summary>

Try to find the longest palindromic subsequence.

</details>

<details><summary>Hint 4</summary>

Use DP to do that.

</details>

---

## Similar Problems

- [Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) — Easy
- [Valid Palindrome IV](https://leetcode.com/problems/valid-palindrome-iv/) — Medium

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/valid-palindrome-iii/*