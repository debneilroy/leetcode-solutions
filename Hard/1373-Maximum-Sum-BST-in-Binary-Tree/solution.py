"""
LeetCode 1373. Maximum Sum BST in Binary Tree
Difficulty: Hard
URL: https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/
"""

# Lower priority, check the variant instead

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxSumBST(self, root: TreeNode) -> int:
        """
        Postorder DFS, same skeleton as the plain 'largest subtree sum'
        variant problem below -- but each call now returns 4 things instead of 1,
        because a parent can't tell if IT is a valid BST without
        knowing whether each child is a valid BST AND the value range
        each child spans.

        Returns per node: (is_valid_bst, min_val, max_val, subtree_sum)

        Time Complexity:  O(n) - every node visited exactly once
        Space Complexity: O(h) - recursion stack, h = tree height
        """

        # empty tree is a valid BST with sum 0 -- that's our floor.
        # Since 0 is always an available candidate, the final
        # answer can NEVER be negative, even if every node in
        # the tree is negative and/or every valid BST subtree
        # sums to something negative (e.g. [-4,-6,-2]: whole
        # tree IS a valid BST but sums to -12 -- still loses to 0).

        best = 0  

        def postorder(node: TreeNode):
            nonlocal best

            # Base case: null is treated as a valid BST with sum 0.
            # min=+inf / max=-inf are sentinels so that when a REAL
            # parent node checks "is my value > left.max_val" or
            # "is my value < right.min_val", a missing child never
            # accidentally fails that check.
            #
            # Example: node=5 with no left child --
            #   left = (True, +inf, -inf, 0)
            #   check: node.val(5) > left.max_val(-inf)? Yes, trivially true.
            #   (if we'd used 0 instead of -inf, a node valued 0 or
            #    less would wrongly fail this check against an ABSENT child)
            if node is None:
                return (True, float('inf'), float('-inf'), 0)

            is_left_bst, left_min, left_max, left_sum = postorder(node.left)
            is_right_bst, right_min, right_max, right_sum = postorder(node.right)

            # BST validity at this node requires ALL three:
            #   1. left subtree is itself a valid BST
            #   2. right subtree is itself a valid BST
            #   3. node.val strictly greater than everything in left,
            #      strictly less than everything in right
            #
            # Counterexample this guards against: [5, 1, 4, null, null, 3, 6]
            #        5
            #       / \
            #      1   4
            #         / \
            #        3   6
            # node=4's own children (3,6) look locally fine (3<4<6),
            # so a naive check would call node=4 a valid BST. But 4's
            # PARENT is 5, and node=4 is in the right subtree, so
            # node=4's entire range must be > 5. It isn't (3 < 5).
            # That's why we propagate min/max up, not just check locally.
            if (is_left_bst and is_right_bst
                    and left_max < node.val < right_min):
                # Valid BST rooted here -- compute its sum and range.
                curr_sum = node.val + left_sum + right_sum
                curr_min = min(left_min, node.val)
                curr_max = max(right_max, node.val)

                best = max(best, curr_sum)
                return (True, curr_min, curr_max, curr_sum)
            else:
                # NOT a valid BST here. We still must return something,
                # but is_valid=False poisons every ancestor's check above
                # (since 'is_left_bst'/'is_right_bst' will now be False
                # for whoever called us) -- so min/max/sum values no
                # longer matter for correctness. Returning them anyway
                # (rather than sentinel junk) costs nothing and keeps
                # the tuple shape uniform.
                return (False, 0, 0, 0)

        postorder(root)
        return best

# Variant : Find Largest Subtree Sum in a Tree

# Given the root of a binary tree, find the maximum subtree sum among all possible subtrees, and return that sum.

# A subtree of a node consists of the node itself and all of its descendants. (A single leaf node counts as a valid subtree — its sum is just its own value.)

# Example 1:

# Input: root = [10, 8, 2, 3, 5, N, N]

#            10
#           /  \
#          8    2
#         / \
#        3   5

# Output: 28
# Explanation: All node values are positive, so the largest possible 
# subtree sum is the sum of the entire tree: 10+8+2+3+5 = 28.

# Example 2:

# Input: root = [1, -2, 3, 4, 5, -6, 2]

#              1
#            /   \
#          -2     3
#          / \   / \
#         4   5 -6  2

# Output: 7
# Explanation: The subtree rooted at node -2 has sum = -2+4+5 = 7.
# Compare against other candidate subtrees:
#   - subtree at 4        -> 4
#   - subtree at 5        -> 5
#   - subtree at -6       -> -6
#   - subtree at 2        -> 2
#   - subtree at 3        -> 3+(-6)+2 = -1
#   - subtree at root(1)  -> 1+7+(-1) = 7
# The maximum among all of these is 7.
        

# class Solution:
#     def maxSubtreeSum(self, root: TreeNode) -> int:
#         """
#         Postorder DFS: each call returns the sum of the subtree rooted
#         at 'node' to its parent. A nonlocal 'best' tracks the max sum
#         seen across ALL subtrees, updated as we unwind the recursion.

#         Time Complexity:  O(n) - every node visited exactly once
#         Space Complexity: O(h) - recursion stack, h = tree height
#                            (O(n) worst case for a skewed tree, O(log n) balanced)
#         """
#         # best is declared outside the recursive helper so every call
#         # can update the SAME running maximum, not a local copy.
#         # Initialized to -inf (not 0) so that a tree of all-negative
#         # values still reports its true max (e.g. a single node -5
#         # should return -5, not incorrectly clamp to 0).

#         best = float('-inf')

#         def postorder(node: TreeNode) -> int:
#             nonlocal best

#             # Base case: an empty child contributes nothing to its
#             # parent's sum. Returning 0 here is safe and does NOT
#             # pollute 'best', because we only compare 'best' against
#             # currSum for REAL nodes below -- null itself is never
#             # treated as a subtree candidate.
#             if node is None:
#                 return 0

#             # Postorder ordering is the whole trick: fully resolve
#             # left and right subtree sums BEFORE touching node.val.
#             # This guarantees no subtree sum is ever recomputed --
#             # each node's contribution is added exactly once, total
#             # work across the whole tree is O(n).
#             left_sum = postorder(node.left)
#             right_sum = postorder(node.right)

#             # Subtree sum rooted at THIS node = its own value plus
#             # whatever its children already resolved to.
#             #
#             # Example walk on [1,-2,3,4,5,-6,2]:
#             #   node=4  (leaf)      -> currSum = 4
#             #   node=5  (leaf)      -> currSum = 5
#             #   node=-2             -> currSum = -2 + 4 + 5 = 7
#             #   node=-6 (leaf)      -> currSum = -6
#             #   node=2  (leaf)      -> currSum = 2
#             #   node=3              -> currSum = 3 + (-6) + 2 = -1
#             #   node=1  (root)      -> currSum = 1 + 7 + (-1) = 7
#             currSum = node.val + left_sum + right_sum

#             # Update the global best BEFORE returning -- every node,
#             # not just the root, is a candidate subtree.
#             best = max(best, currSum)

#             # Return currSum (not best!) to the parent. The parent
#             # needs the RAW sum of this subtree to compute its own
#             # currSum -- if we returned 'best' instead, a parent could
#             # silently absorb an unrelated, disconnected subtree's sum
#             # into its own total, which is wrong (subtree sums must
#             # stay contiguous/rooted).
#             return currSum

#         postorder(root)
#         return best