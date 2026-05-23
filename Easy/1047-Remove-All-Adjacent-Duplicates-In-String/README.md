# 1047. Remove All Adjacent Duplicates In String

**Difficulty:** 🟢 Easy  
**Tags:** String, Stack  
**Accepted:** 880.9K / 1.2M (73.2%)

---

## Problem

You are given a string `s` consisting of lowercase English letters. A **duplicate removal** consists of choosing two **adjacent** and **equal** letters and removing them.

We repeatedly make **duplicate removals** on `s` until we no longer can.

Return *the final string after all such duplicate removals have been made*. It can be proven that the answer is **unique**.

 

Example 1:

```

**Input:** s = "abbaca"
**Output:** "ca"
**Explanation:** 
For example, in "abbaca" we could remove "bb" since the letters are adjacent and equal, and this is the only possible move.  The result of this move is that the string is "aaca", of which only "aa" is possible, so the final string is "ca".

```

Example 2:

```

**Input:** s = "azxxzy"
**Output:** "ay"

```

 

**Constraints:**

	
- `1 <= s.length <= 105`
	
- `s` consists of lowercase English letters.

---

## Hints

<details><summary>Hint 1</summary>

Use a stack to process everything greedily.

</details>

---

## Similar Problems

- [Remove All Adjacent Duplicates in String II](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/) — Medium
- [Removing Stars From a String](https://leetcode.com/problems/removing-stars-from-a-string/) — Medium
- [Minimize String Length](https://leetcode.com/problems/minimize-string-length/) — Easy

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/*