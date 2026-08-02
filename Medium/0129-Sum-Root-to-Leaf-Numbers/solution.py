"""
LeetCode 129. Sum Root to Leaf Numbers
Difficulty: Medium
URL: https://leetcode.com/problems/sum-root-to-leaf-numbers/
"""

# Definition for a binary tree node.

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        """
        Approach: DFS (preorder), carrying the "number built so far" down
        from root to each leaf. At a leaf, add that number to a running total.

        nonlocal (over self.root_to_leaf): keeps the running total scoped to
        this call only, avoiding stale state leaking across repeated calls
        on the same Solution instance.

        TC: O(n) - visit every node exactly once
        SC: O(h) - recursion stack depth, h = height of tree
            (worst case O(n) for a skewed/degenerate tree)
        """

        def preorder(node: TreeNode, curr_number: int):
            nonlocal root_to_leaf
            # self version: no line needed here (self is already accessible
            # inside this closure, unlike a plain enclosing-scope variable)

            # Base case: fell off the tree (happens at every leaf's None
            # children too) — nothing to add here, just stop.
            if not node:
                return

            # Extend the number being built along this path.
            # Example: curr_number=12, node.val=3 -> curr_number=123
            curr_number = curr_number * 10 + node.val

            # Leaf check: no children means this root-to-leaf path is complete.
            # Example: node=3 with no left/right -> add 123 to the total
            if not node.left and not node.right:
                root_to_leaf += curr_number
                # self version: self.root_to_leaf += curr_number

                # results-array version (return each path's number instead
                # of a combined total): results.append(curr_number)
                
                # -- note: no nonlocal needed for this one, since
                # results.append(...) mutates the existing list rather
                # than rebinding the name (only rebinding requires nonlocal)
                return

            # Not a leaf yet — keep extending the path in both directions,
            # carrying the current partial number down to each child.
            preorder(node.left, curr_number)
            preorder(node.right, curr_number)

        # root_to_leaf lives in sumNumbers' scope; preorder mutates it
        # via nonlocal rather than returning values back up the call stack.
        root_to_leaf = 0
        # self version: self.root_to_leaf = 0
        # results-array version: results = []  (initialize an empty list
        # instead of a running total)
        preorder(root, 0)
        return root_to_leaf
        # self version: return self.root_to_leaf
        # results-array version: return results

# Another approach : Without any instance or nonlocal variables

class Solution:
    def sumNumbers(self, root):
        """
        Approach: DFS with helper function
        Time: O(n), Space: O(h) where h is height
        """
        def dfs(node, current_num):

            # return 0 here (not None) because this value gets summed via
            # dfs(left) + dfs(right) below — 0 is the identity for +, so a
            # missing child contributes nothing to the total.
            # (Not needed in the self/nonlocal version, since there the
            # return value is never used — the result is set via a side
            # effect instead, so a bare `return` is enough.)
            if not node:
                return 0
            
            # Build current number by appending digit
            current_num = current_num * 10 + node.val
            
            # If leaf node, return the number
            if not node.left and not node.right:
                return current_num
            
            # Sum from left and right subtrees
            return dfs(node.left, current_num) + dfs(node.right, current_num)
        
        return dfs(root, 0)

# Iterative Preorder Traversal

# class Solution:
#     def sumNumbers(self, root):
#         """
#         Approach 2: Iterative DFS using stack
#         Time: O(n), Space: O(h)
#         """
#         if not root:
#             return 0
        
#         stack = [(root, root.val)]
#         total = 0
        
#         while stack:
#             node, current_num = stack.pop()
            
#             # If leaf node, add to total
#             if not node.left and not node.right:
#                 total += current_num
            
#             # Add children to stack with updated numbers
#             if node.right:
#                 stack.append((node.right, current_num * 10 + node.right.val))
#             if node.left:
#                 stack.append((node.left, current_num * 10 + node.left.val))
        
#         return total


# Variant 1: Sum of Root-to-Leaf Path Sums (multi-digit values, addition instead of concatenation)

# Given a binary tree where node values may be multi-digit (not restricted to single digits 0-9), each root-to-leaf path has a path sum = the sum of node values along that path (plain addition). Return the sum of all these path sums across every root-to-leaf path.

# How this differs from the original LC 129 — same tree shape, two different rules:

#         1
#        / \
#       2   3

# Original LC 129: values are restricted to single digits, and each path is built by concatenating digits (not adding them). Path 1 → 2 becomes the number 12 — the "1" and "2" are glued together digit-by-digit, not summed. Path 1 → 3 becomes 13. Total = 12 + 13 = 25.

# This variant, same tree: instead of concatenating, we sum the values. Path 1 → 2 becomes 1+2 = 3. Path 1 → 3 becomes 1+3 = 4. Total = 3 + 4 = 7.

# Now here is  why the variant needs multi-digit values allowed — if the tree instead looks like this:

#         15
#        /  \
#       9    28
#      /
#     6

# This variant only (concatenation wouldn't make sense here — imagine trying to glue "15" and "9" together digit-by-digit; it's unclear whether that means "159" or "1509" or something else, which is exactly why concatenation breaks down once values aren't single digits):

# Path 15 → 9 → 6 → sum = 15+9+6 = 30
# Path 15 → 28 → sum = 15+28 = 43
# Total = 30 + 43 = 73

# class Solution:
#     def sumRootToLeafPathSums(self, root: Optional[TreeNode]) -> int:
#         """
#         Approach: DFS, carrying the running sum of node values down each
#         path (plain addition, not digit concatenation). At a leaf, add
#         that path's sum into self.total_sum.

#         Difference from LC 129: original problem restricts node values to
#         single digits (0-9) and builds a number via concatenation
#         (curr_number * 10 + node.val). Here, values can be multi-digit,
#         so we simply add (curr_sum + node.val) instead of shifting digits.

#         self.total_sum (instance variable): mutated as a side effect inside
#         dfs, rather than returned and combined via +. Works, but ties the
#         result to the Solution object's state rather than keeping it local
#         to this call — must be reset each call, or stale values leak across
#         repeated calls on the same instance.

#         TC: O(n) - visit every node exactly once
#         SC: O(h) - recursion stack depth, h = height of tree
#         """
#         def dfs(node, path_sum_so_far):
#             if not node:
#                 return

#             path_sum_so_far += node.val

#             if not node.left and not node.right:
#                 self.total_sum += path_sum_so_far
#                 return

#             dfs(node.left, path_sum_so_far)
#             dfs(node.right, path_sum_so_far)

#         self.total_sum = 0
#         dfs(root, 0)
#         return self.total_sum

# Another version : no instance variables

# class Solution:
#     def sumRootToLeafPathSums(self, root: Optional[TreeNode]) -> int:
#         """
#         Approach: DFS, carrying the running sum of node values down each
#         path (plain addition, not digit concatenation). At a leaf, add
#         that path's sum into a running total across all paths.

#         Difference from LC 129: original problem restricts node values to
#         single digits (0-9) and builds a number via concatenation
#         (curr_number * 10 + node.val). Here, values can be multi-digit,
#         so we simply add (curr_sum + node.val) instead of shifting digits.

#         TC: O(n) - visit every node exactly once
#         SC: O(h) - recursion stack depth, h = height of tree
#         """
#         def dfs(node, path_sum_so_far):
#             if not node:
#                 return 0

#             # Plain addition — no *10 shift, since values aren't
#             # restricted to single digits here.
#             # Example: path_sum_so_far=15, node.val=9 -> 24
#             path_sum_so_far += node.val

#             if not node.left and not node.right:
#                 return path_sum_so_far

#             return dfs(node.left, path_sum_so_far) + dfs(node.right, path_sum_so_far)

#         return dfs(root, 0)


# Variant 2: Sum Root to Leaf Numbers (multi-digit values)

# You are given the root of a binary tree containing numbers from 0 to 999 (not restricted to single digits).

# Each root-to-leaf path in the tree represents a number, formed by concatenating the values along the path — not adding them.

# For example, the root-to-leaf path 10 -> 88 -> 555 represents the number 1088555 (digits glued together: "10" + "88" + "555").

# Return the total sum of all root-to-leaf numbers.

# How this differs from the "classic" single-digit version of LC 129: with single-digit values, concatenating just means num * 10 + val (shift left by exactly one decimal place each time). With multi-digit values (0-999), the shift amount depends on how many digits val has — shifting by a fixed *10 would be wrong. E.g. concatenating "15" after "3" should give "315," not 3*10+15=45.

# Example (using the tree from the screenshot):

#         3
#        / \
#       79   2
#      /
#    111

# Path 3 → 79 → 111: concatenate → "3" + "79" + "111" → 379111
# Path 3 → 2: concatenate → "3" + "2" → 32
# Total = 379111 + 32 = 379143

# class Solution:
#     def sumNumbers(self, root: Optional[TreeNode]) -> int:
#         """
#         Approach: DFS, building each root-to-leaf number by concatenating
#         node values (not just digits) — values can range from 0 to 999,
#         so we shift by the correct power of 10 based on how many digits
#         the current node's value actually has.

#         Difference from the single-digit version of LC 129: there,
#         current_num * 10 + node.val works because every value is exactly
#         one digit. Here, node.val can be multi-digit (e.g. 79, 111), so a
#         fixed *10 shift would be wrong — we need *10^(digit count of val).

#         TC: O(n) - visit every node once; count_digits is O(log(val)) per
#             node, so more precisely O(n * log(max_val)), a small constant
#             factor here since max_val = 999 (at most 3 digits)
#         SC: O(h) - recursion stack depth, h = height of tree
#         """

#         def count_digits(n: int) -> int:
#             """
#             Counts the number of digits in a non-negative integer.
#             Used to determine how much to shift current_num when
#             concatenating in the next value.

#             Examples: 5 -> 1 digit, 42 -> 2 digits, 999 -> 3 digits
#             """
#             if n == 0:
#                 return 1

#             count = 0
#             while n > 0:
#                 count += 1
#                 n //= 10
#             return count

#         def dfs(node: TreeNode, current_num: int) -> None:
#             if not node:
#                 return

#             # Count how many digits node.val occupies, so we shift by
#             # exactly that many decimal places before adding it in.
#             digits = count_digits(node.val)

#             # Shift current_num left by 10^digits, then concatenate node.val.
#             # Example: current_num=123, node.val=45 (2 digits)
#             # -> 123 * 10^2 + 45 = 12300 + 45 = 12345
#             current_num = current_num * (10 ** digits) + node.val

#             # Leaf check: path is complete — accumulate into self.total
#             # instead of returning the value back up the call stack.
#             if not node.left and not node.right:
#                 self.total += current_num
#                 return

#             dfs(node.left, current_num)
#             dfs(node.right, current_num)

#         self.total = 0
#         dfs(root, 0)
#         return self.total


# Variant 3: Sum Root to Leaf Numbers (signed variant)

# You are given the root of a binary tree containing digits from -9 to 9 only.

# Each root-to-leaf path in the tree represents a number whose sign is:

# 1. negative if there is an odd number of negative nodes in the path
# 2. positive if there is an even number of negative nodes in the path (including zero)

# These are known as a negative path and a positive path, respectively.

# For example, the root-to-leaf path 1 -> -2 -> 3 represents the number -123.

# Note: the sign of a node should not affect any root-to-leaf calculations other than the consideration of a negative path — i.e., only the absolute value of each digit is used when building the number itself; the sign only determines whether the final number is positive or negative.

# Return the total sum of all root-to-leaf numbers. Test cases are generated so the answer fits in a 32-bit integer.

# A leaf node is a node with no children.

# Example:

# Input: root = [1, -2, 3]
# Output: 1

# Explanation:

# The root-to-leaf path 1 -> -2 represents the number -12.
# The root-to-leaf path 1 -> 3 represents the number 13.
# Therefore, sum = -12 + 13 = 1.

# Second example, using a deeper tree:

#               -1
#              /   \
#            -2     4
#            /        \
#          -9          -5

# Path -1 → -2 → -9: digits (absolute values) concatenate to 129; three negative nodes (-1, -2, -9) → odd count → number is -129
# Path -1 → 4 → -5: digits concatenate to 145; two negative nodes (-1, -5) → even count → number is +145
# Total = -129 + 145 = 16     


# class Solution:
#     def sumNumbers(self, root: Optional[TreeNode]) -> int:
#         """
#         Variant: Sum root-to-leaf numbers with sign based on negative node count

#         Rules:
#         - Each root-to-leaf path represents a number formed by concatenating
#           the ABSOLUTE VALUES of node digits (sign never affects the digits)
#         - If path has an ODD number of negative nodes -> final number is NEGATIVE
#         - If path has an EVEN number of negative nodes -> final number is POSITIVE

#         Example: Path [1, -2, 3]
#         - Absolute number: 123... but wait, only the -2 branch matters per
#           leaf. Concretely: path 1 -> -2 gives abs digits "1","2" -> 12,
#           with 1 negative node (odd) -> final = -12.

#         Difference from original LC 129: digits are still single-digit
#         (-9 to 9), so the *10 shift still applies unchanged. What's new:
#         (a) use abs(node.val) when concatenating, and (b) separately track
#         parity of negative nodes seen, applied as a sign only at the leaf.

#         TC: O(n) - visit every node once
#         SC: O(h) - recursion stack depth, h = height of tree
#         """
#         def dfs(node, current_num, negative_count):
#             if not node:
#                 # Identity for +: a missing child contributes 0 to the sum,
#                 # since this return value is combined via left_sum + right_sum.
#                 return 0

#             # Build the absolute value of the number — ignore sign here,
#             # sign is handled separately via negative_count.
#             # Example: current_num=1, node.val=-2 -> current_num=12
#             current_num = current_num * 10 + abs(node.val)

#             # Track how many negative nodes we've seen on this path so far.
#             if node.val < 0:
#                 negative_count += 1

#             # Leaf check: path is complete — apply sign based on parity.
#             if not node.left and not node.right:
#                 # Odd number of negatives -> negative result
#                 # Even number of negatives -> positive result
#                 if negative_count % 2 == 1:
#                     return -current_num
#                 else:
#                     return current_num

#             # Continue DFS for left and right subtrees, carrying both
#             # current_num and negative_count down each branch.
#             left_sum = dfs(node.left, current_num, negative_count)
#             right_sum = dfs(node.right, current_num, negative_count)

#             return left_sum + right_sum

#         return dfs(root, 0, 0)