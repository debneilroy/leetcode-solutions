"""
LeetCode 270. Closest Binary Search Tree Value
Difficulty: Easy
URL: https://leetcode.com/problems/closest-binary-search-tree-value/
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# Approach : Iterative

# class Solution:
#     def closestValue(self, root: Optional[TreeNode], target: float) -> int:
#         """
#         Find the value in a BST that is closest to the target value.
        
#         Approach:
#         - Initialize closest as infinity for easier comparison logic
#         - Traverse the BST using its ordering property
#         - Keep track of the closest value seen so far
#         - Navigate left if target < current value, right otherwise
#         - Update closest value whenever we find a node closer to target
        
#         Time Complexity: O(H) where H is the height of the tree
#             - O(log N) for a balanced BST
#             - O(N) worst case for a skewed tree
#             - We traverse at most one path from root to leaf
        
#         Space Complexity: O(1)
#             - Only using constant extra space for variables
#             - Iterative approach doesn't use recursion stack
#         """

#          # --- Step 1: Handle empty tree case (optional safety check)
#         if not root:
#         # If the tree is empty, return None or raise an error depending on design choice
#             return None # or, raise ValueError("BST is empty")

#         # --- Step 2: Initialize closest value
#         # Option 1: Use the root value (LeetCode guarantees non-empty BST)
#         closest = root.val

#         # Option 2: Use float('inf') if you want a generic safe initialization
#         # closest = float('inf')
#         #
#         # Explanation:
#         # - Using root.val is cleaner since it's guaranteed to be a valid BST value.
#         # - float('inf') can be used if the tree might be empty; it ensures the first
#         #   comparison always updates closest. But for LeetCode 270, root.val is preferred.

#         # Traverse the tree until we reach a leaf
#         while root:
#             # Calculate distance from current node to target
#             current_distance = abs(root.val - target)
#             closest_distance = abs(closest - target)
            
#             # Update closest if current node is closer to target
#             if current_distance < closest_distance:
#                 closest = root.val
#             # If distances are equal, choose the smaller value (problem requirement)
#             elif current_distance == closest_distance:
#                 closest = min(closest, root.val)
            
#             # Navigate BST based on target value using BST property
#             # If target is less than current value, go left (smaller values)
#             if target < root.val:
#                 root = root.left
#             # Otherwise, go right (larger values)
#             else:
#                 root = root.right
        
#         return closest

# # Example 1:

# # root = TreeNode(4)
# # root.left = TreeNode(2)
# # root.right = TreeNode(5)
# # root.left.left = TreeNode(1)
# # root.left.right = TreeNode(3)

# # Approach : Recursive

class Solution:
    def closestValue(self, root: Optional[TreeNode], target: float) -> int:
        """
        Find the value in a BST that is closest to the target value.
        
        Recursive Approach:
        - At each node, compare current node's distance to target
        - Update closest if we find a better candidate
        - Recursively search the appropriate subtree based on BST property
        - Carry the closest value through recursive calls
        
        Time Complexity: O(H) where H is the height of the tree
            - O(log N) for a balanced BST
            - O(N) worst case for a skewed tree
            - We traverse at most one path from root to leaf
        
        Space Complexity: O(H) due to recursion call stack
            - O(log N) for balanced BST
            - O(N) worst case for skewed tree
            - Each recursive call adds a frame to the stack
        """
        
        # --- Step 1: Handle empty tree case
        if not root:
            return None
    
        # --- Step 2: Define recursive helper function
        def dfs(node: Optional[TreeNode], closest: int) -> int:
            """
            Recursively traverse BST to find closest value to target.
            
            Args:
                node: Current node being examined
                closest: Best candidate found so far
                
            Returns:
                The value in the subtree closest to target
            """
            # Base case: reached a null node, return current best
            if not node:
                return closest
            
            # Calculate distances from current node and closest to target
            current_distance = abs(node.val - target)
            closest_distance = abs(closest - target)
            
            # Update closest if current node is closer to target
            if current_distance < closest_distance:
                closest = node.val
            # If distances are equal, choose the smaller value (problem requirement)
            elif current_distance == closest_distance:
                closest = min(closest, node.val)
            
            # Navigate BST based on target value using BST property
            # MUST capture the recursive call's return value and pass it onward.
            # The recursive call may find a closer value further down the tree
            # (e.g. node 7's subtree finds 7 is closer than this node's own value).
            # If we just call `dfs(node.left, closest)` without capturing the
            # result, this node would fall through to `return closest` below
            # using its OWN pre-recursion closest, silently discarding whatever
            # the deeper call found.
            #
            # Note: since nothing happens after this branch besides returning
            # closest, we could just as well write `return dfs(node.left, closest)`
            # directly (no separate `return closest` line needed below at all).
            # Assigning to `closest` first is only necessary if you need to use
            # or further modify the value AFTER the recursive call returns —
            # which we don't here, so the direct return is equally correct and
            # slightly more concise.
            if target < node.val:
                closest = dfs(node.left, closest)
            # Otherwise, search right (larger values)
            else:
                closest = dfs(node.right, closest)

            return closest
        
        # --- Step 4: Start recursive traversal from root
        # MUST return here: this sends dfs()'s final result out of
        # closestValue() as the actual answer. Without 'return',
        # closestValue() would compute the correct value internally
        # but still output None.
        return dfs(root, root.val)

# Rare Variant : Leetcode 272