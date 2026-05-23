# 1249. Minimum Remove to Make Valid Parentheses

**Difficulty:** 🟡 Medium  
**Tags:** String, Stack  
**Accepted:** 1.1M / 1.5M (71.5%)

---

## Problem

Given a string s of `'('` , `')'` and lowercase English characters.

Your task is to remove the minimum number of parentheses ( `'('` or `')'`, in any positions ) so that the resulting *parentheses string* is valid and return **any** valid string.

Formally, a *parentheses string* is valid if and only if:

	
- It is the empty string, contains only lowercase characters, or
	
- It can be written as `AB` (`A` concatenated with `B`), where `A` and `B` are valid strings, or
	
- It can be written as `(A)`, where `A` is a valid string.

 

Example 1:

```

**Input:** s = "lee(t(c)o)de)"
**Output:** "lee(t(c)o)de"
**Explanation:** "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.

```

Example 2:

```

**Input:** s = "a)b(c)d"
**Output:** "ab(c)d"

```

Example 3:

```

**Input:** s = "))(("
**Output:** ""
**Explanation:** An empty string is also valid.

```

 

**Constraints:**

	
- `1 <= s.length <= 105`
	
- `s[i]` is either `'('` , `')'`, or lowercase English letter.

---

## Hints

<details><summary>Hint 1</summary>

Each prefix of a balanced parentheses has a number of open parentheses greater or equal than closed parentheses, similar idea with each suffix.

</details>

<details><summary>Hint 2</summary>

Check the array from left to right, remove characters that do not meet the property mentioned above, same idea in backward way.

</details>

---

## Similar Problems

- [Minimum Number of Swaps to Make the String Balanced](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/) — Medium
- [Check if a Parentheses String Can Be Valid](https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid/) — Medium

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/*