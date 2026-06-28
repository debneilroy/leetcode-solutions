# 227. Basic Calculator II

**Difficulty:** 🟡 Medium  
**Tags:** Math, String, Stack  
**Accepted:** 961.9K / 2M (47.0%)

---

## Problem

Given a string `s` which represents an expression, *evaluate this expression and return its value*. 

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in the range of `[-231, 231 - 1]`.

**Note:** You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

 

Example 1:

```
**Input:** s = "3+2*2"
**Output:** 7

```

Example 2:

```
**Input:** s = " 3/2 "
**Output:** 1

```

Example 3:

```
**Input:** s = " 3+5 / 2 "
**Output:** 5

```

 

**Constraints:**

	
- `1 <= s.length <= 3 * 105`
	
- `s` consists of integers and operators `('+', '-', '*', '/')` separated by some number of spaces.
	
- `s` represents **a valid expression**.
	
- All the integers in the expression are non-negative integers in the range `[0, 231 - 1]`.
	
- The answer is **guaranteed** to fit in a **32-bit integer**.

---

## Similar Problems

- [Basic Calculator](https://leetcode.com/problems/basic-calculator/) — Hard
- [Expression Add Operators](https://leetcode.com/problems/expression-add-operators/) — Hard
- [Basic Calculator III](https://leetcode.com/problems/basic-calculator-iii/) — Hard
- [Evaluate Valid Expressions](https://leetcode.com/problems/evaluate-valid-expressions/) — Hard

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/basic-calculator-ii/*