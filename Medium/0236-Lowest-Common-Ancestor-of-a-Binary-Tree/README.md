# 236. Lowest Common Ancestor of a Binary Tree

**Difficulty:** 🟡 Medium  
**Tags:** Tree, Depth-First Search, Binary Tree  
**Accepted:** 2.7M / 3.9M (69.8%)

---

## Problem

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the [definition of LCA on Wikipedia](https://en.wikipedia.org/wiki/Lowest_common_ancestor): &ldquo;The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself).&rdquo;

 

Example 1:

```

**Input:** root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
**Output:** 3
**Explanation:** The LCA of nodes 5 and 1 is 3.

```

Example 2:

```

**Input:** root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
**Output:** 5
**Explanation:** The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.

```

Example 3:

```

**Input:** root = [1,2], p = 1, q = 2
**Output:** 1

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[2, 10^5]`.
	
- `-10^9 <= Node.val <= 10^9`
	
- All `Node.val` are **unique**.
	
- `p != q`
	
- `p` and `q` will exist in the tree.

---

## Similar Problems

- [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) — Medium
- [Smallest Common Region](https://leetcode.com/problems/smallest-common-region/) — Medium
- [Find Players With Zero or One Losses](https://leetcode.com/problems/find-players-with-zero-or-one-losses/) — Medium
- [Lowest Common Ancestor of a Binary Tree II](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-ii/) — Medium
- [Lowest Common Ancestor of a Binary Tree III](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/) — Medium
- [Lowest Common Ancestor of a Binary Tree IV](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iv/) — Medium
- [Step-By-Step Directions From a Binary Tree Node to Another](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/) — Medium
- [Cycle Length Queries in a Tree](https://leetcode.com/problems/cycle-length-queries-in-a-tree/) — Hard

---

## Solution

See [solution.py](./solution.py)

*Problem link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/*