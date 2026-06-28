# 647. Palindromic Substrings

**Difficulty:** 🟡 Medium  
**Tags:** Two Pointers, String, Dynamic Programming  
**Accepted:** 1.2M / 1.7M (72.9%)

---

## Problem

Given a string `s`, return *the number of **palindromic substrings** in it*.

A string is a **palindrome** when it reads the same backward as forward.

A **substring** is a contiguous sequence of characters within the string.

 

Example 1:

```

**Input:** s = "abc"
**Output:** 3
**Explanation:** Three palindromic strings: "a", "b", "c".

```

Example 2:

```

**Input:** s = "aaa"
**Output:** 6
**Explanation:** Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".

```

 

**Constraints:**

	
- `1 <= s.length <= 1000`
	
- `s` consists of lowercase English letters.

---

## Hints

<details><summary>Hint 1</summary>

How can we reuse a previously computed palindrome to compute a larger palindrome?

</details>

<details><summary>Hint 2</summary>

If “aba” is a palindrome, is “xabax” a palindrome? Similarly is “xabay” a palindrome?

</details>

<details><summary>Hint 3</summary>

Complexity based hint:
If we use brute force and check whether for every start and end position a substring is a palindrome we have O(n^2) start - end pairs and O(n) palindromic checks. Can we reduce the time for palindromic checks to O(1) by reusing some previous computation?

</details>

---

## Similar Problems

- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) — Medium
- [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) — Medium

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/palindromic-substrings/*