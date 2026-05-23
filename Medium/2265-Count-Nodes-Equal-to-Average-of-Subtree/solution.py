"""
LeetCode 2265. Count Nodes Equal to Average of Subtree
Difficulty: Medium
URL: https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


# Brute Force Approach (conceptually):

# For each node in the tree:

# Traverse the entire subtree rooted at that node.

# Collect all node values in that subtree (via DFS or BFS).

# Compute the average = sum(subtree_values) // len(subtree_values).

# Check if it equals the node’s value — if yes, increment the count.

# Repeat this for every node.

# So essentially, you’re running a full subtree traversal per node — doing redundant work many times.

# Complexity:

# Time: O(n²) in the worst case (e.g., a skewed tree) because for each node you might traverse almost all nodes again.

# Space: O(h) for recursion stack + O(n) for temporary list of subtree nodes.

# The optimal O(n) version avoids this repetition by computing sum and count in one post-order traversal.

# Approach : Postorder traversal DFS
        
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        """
        Count nodes where value equals the average of its subtree.
        
        Time Complexity: O(n) - visit each node exactly once
        Space Complexity: O(h) - recursion stack depth where h is tree height
        """
        # Counter to track nodes where value equals subtree average
        self.count = 0
        
        def dfs(node):
            """
            Post-order DFS to calculate subtree sum and count.
            
            Time Complexity: O(1) per node, O(n) overall
            Space Complexity: O(h) for recursion stack
            """
            # Base case: empty node (None)
            # sum = 0: no values to add (neutral element for addition)
            # count = 0: no nodes to count (neutral element for counting)
            if not node:
                return 0, 0
            
            # Recursively get info from left subtree
            # left_sum = sum of all values in left subtree
            # left_count = number of nodes in left subtree
            left_sum, left_count = dfs(node.left)
            
            # Recursively get info from right subtree
            # right_sum = sum of all values in right subtree
            # right_count = number of nodes in right subtree
            right_sum, right_count = dfs(node.right)
            
            # Calculate current subtree's total sum
            # curr_sum = sum of ALL values in the subtree rooted at this node
            # (left subtree values + right subtree values + current node's value)
            curr_sum = left_sum + right_sum + node.val
            
            # Calculate current subtree's total node count
            # curr_count = total number of nodes in the subtree rooted at this node
            # (left subtree nodes + right subtree nodes + 1 for current node)
            curr_count = left_count + right_count + 1
            
            # Check if current node's value equals the average of its subtree
            # Average = total sum / total count (integer division rounds down)
            if node.val == curr_sum // curr_count:
                self.count += 1
            
            # Return sum and count for parent node to use in its calculations
            # Parent will use these values to compute ITS subtree sum and count
            return curr_sum, curr_count
        
        # Start DFS from root
        dfs(root)
        return self.count


# Approach : BFS

# from collections import deque

# class Solution:
#     def averageOfSubtree(self, root: TreeNode) -> int:
#         """
#         Count nodes where value equals the average of its subtree using BFS.
        
#         Time Complexity: O(n²) - O(n) for BFS traversal × O(n) for subtree calculation
#         Space Complexity: O(n) - queue can hold up to n/2 nodes at the last level
        
#         Note: BFS is less efficient than DFS for this problem because we need
#         subtree information, which requires additional traversals.
#         """
#         if not root:
#             return 0
        
#         count = 0
#         # BFS queue to process nodes level by level
#         queue = deque([root])
        
#         def calculate_subtree(node):
#             """
#             Helper function to calculate sum and count of a subtree.
#             Uses its own BFS traversal starting from the given node.
            
#             Time Complexity: O(k) where k is the size of the subtree
#             Space Complexity: O(k) for the queue
#             """
#             if not node:
#                 return 0, 0
            
#             total_sum = 0
#             total_count = 0
            
#             # BFS to traverse entire subtree rooted at 'node'
#             sub_queue = deque([node])
            
#             while sub_queue:
#                 curr = sub_queue.popleft()
#                 total_sum += curr.val
#                 total_count += 1
                
#                 # Add children to queue
#                 if curr.left:
#                     sub_queue.append(curr.left)
#                 if curr.right:
#                     sub_queue.append(curr.right)
            
#             return total_sum, total_count
        
#         # Main BFS traversal - visit each node in the tree
#         while queue:
#             node = queue.popleft()
            
#             # Calculate subtree sum and count for current node
#             # This does a separate BFS traversal for each node's subtree
#             subtree_sum, subtree_count = calculate_subtree(node)
            
#             # Check if node value equals average of its subtree
#             if node.val == subtree_sum // subtree_count:
#                 count += 1
            
#             # Add children to main BFS queue
#             if node.left:
#                 queue.append(node.left)
#             if node.right:
#                 queue.append(node.right)
        
#         return count

# Variant : Given the root of a binary tree, return a boolean whether the value of every node is equal to the average of the values in its subtree.

# Note:

# The average of n elements is the sum of the n elements divided by n and rounded down to the nearest integer.

# A subtree of root is a tree consisting of root and all of its descendants.

# Example 1:
#         4
#        / \
#       8   5
#      / \   \
#     0   1   6


# Input: root = [4,8,5,0,1,null,6]
# Output: False

# Constraints:

# The number of nodes in the tree is in the range [1, 1000].

# 0 ≤ Node.val ≤ 1000

# class Solution:
#     def isSubtreeAverage(self, root):
#         """
#         Check if EVERY node's value equals the average of its subtree.
#         Uses sentinel value (-1, -1) to signal mismatch found in subtree.
        
#         Args:
#             root: Root of the binary tree
        
#         Returns:
#             bool: True if all nodes match their subtree averages, False otherwise
        
#         Time Complexity: O(k) where k <= n (stops at first mismatch)
#         Space Complexity: O(h) where h is tree height (recursion stack)
#         """
        
#         def dfs(node):
#             """
#             Post-order DFS traversal with immediate early exit.
            
#             Args:
#                 node: Current tree node being processed
            
#             Returns:
#                 tuple: (sum_of_subtree, count_of_nodes)
#                 - If all nodes match: (actual_sum, actual_count)
#                 - If any node doesn't match: (-1, -1) as sentinel
            
#             Time Complexity: O(1) per node
#             Space Complexity: O(h) for recursion stack
#             """

#             if node is None:
#                 return 0, 0
            
#             leftSum, leftCount = dfs(node.left)
            
#             # IMMEDIATE EXIT: If left subtree had a mismatch, propagate failure upward
#             # No need to process right subtree or current node - answer is already False
#             if leftCount == -1:
#                 return -1, -1
            
#             rightSum, rightCount = dfs(node.right)
            
#             # IMMEDIATE EXIT: If right subtree had a mismatch, propagate failure upward
#             # No need to check current node - answer is already False
#             if rightCount == -1:
#                 return -1, -1

#             # Equivalently
#             # leftSum, leftCount = dfs(node.left)
#             # rightSum, rightCount = dfs(node.right)

#             # if leftCount == -1 or rightCount == -1:
#             #     return -1, -1

#             currSum = leftSum + rightSum + node.val
#             currCount = leftCount + rightCount + 1
            
#             if node.val != currSum // currCount:
#                 return -1, -1
            
#             return currSum, currCount
        
#         # We don't need the sum, only need to check if result indicates success or failure
#         _, result = dfs(root)
        
#         # If result is -1, at least one node didn't match (return False)
#         # If result is not -1, all nodes matched their averages (return True)
#         return result != -1


# Boolean Flag Approach (Alternative)

# class Solution:
#     def isSubtreeAverage(self, root):
#         """
#         Check if EVERY node's value equals the average of its subtree.
#         Uses boolean flag to track match status.
        
#         Time Complexity: O(k) where k <= n (stops at first mismatch)
#         Space Complexity: O(h) where h is tree height (recursion stack)
#         """
#         # Flag to track if all nodes match
#         self.all_match = True
        
#         def dfs(node):
#             """
#             Post-order DFS with immediate early exit using flag.
            
#             Returns:
#                 tuple: (sum, count) - returns (0, 0) when flag is False
#             """
#             if node is None:
#                 return 0, 0

#             leftSum, leftCount = dfs(node.left)
            
#             # Early exit: if left subtree failed, stop processing
#             if not self.all_match:
#                 return 0, 0
            
#             rightSum, rightCount = dfs(node.right)
            
#             # Early exit: if right subtree failed, stop processing
#             if not self.all_match:
#                 return 0, 0
            
#             currSum = leftSum + rightSum + node.val
#             currCount = leftCount + rightCount + 1

#             if node.val != currSum // currCount:
#                 self.all_match = False
#                 return 0, 0
            
#             return currSum, currCount
        
#         # Run DFS and return flag
#         dfs(root)
#         return self.all_match