"""
LeetCode 543. Diameter of Binary Tree
Difficulty: Easy
URL: https://leetcode.com/problems/diameter-of-binary-tree/
"""

# Review defintiions of complete, balanced, skewed trees

# Tree Diameter Quick Review
# 1. Height of a node

# Definition: Number of nodes on the longest path from this node down to a leaf.

# Base case: Null node → height = 0.

# Formula: height(node) = 1 + max(height(left), height(right))

# Example:

#     2
#    / \
#   4   5


# height(4) = 1

# height(5) = 1

# height(2) = 1 + max(1,1) = 2

# 2. Diameter of a tree

# Definition: The length (in edges) of the longest path between any two nodes.

# Formula at a node:
# diameter_through_node = left_height + right_height

# Global diameter:
# diameter = max(diameter, diameter_through_node) across all nodes.

# 3. Edges vs Nodes

# Height counts in nodes.

# Diameter counts in edges.

# That’s why a leaf has height = 1 but diameter = 0.


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# Approach : DFS

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        """
        Find the diameter of a binary tree using DFS.
        
        Approach:
        - Use DFS to traverse the tree
        - For each node, calculate the height of left and right subtrees
        - The diameter through current node = left_height + right_height
        - Track the maximum diameter found across all nodes
        - Return height of current subtree for parent calculations
        
        Time Complexity: O(n) where n is the number of nodes
        Space Complexity: O(h) where h is the height of the tree (recursion stack)
        
        Args:
            root: TreeNode - Root of the binary tree
            
        Returns:
            int - Length of the diameter (number of edges in longest path)
        """
        # Track global maximum diameter across all nodes visited
        # Need this because diameter might not pass through root - could be entirely within a subtree
        self.max_diameter = 0
        
        def dfs(node):
            """
            Returns the height of the subtree rooted at node.
            Updates max_diameter as a side effect.
            
            Args:
                node: TreeNode - Current node being processed
                
            Returns:
                int - Height of the subtree rooted at node
            """
            if not node:
                return 0
            
            # Get heights of left and right subtrees
            left_height = dfs(node.left)
            right_height = dfs(node.right)
            
            # Diameter through current node = left_height + right_height
            # Note: This counts EDGES. To count NODES instead, use: left_height + right_height + 1
            # Path: 4 -> 2 -> 1 -> 3 has 3 EDGES
            # Path: 4 -> 2 -> 1 -> 3 has 4 NODES
            current_diameter = left_height + right_height
            
            # Update global maximum diameter
            self.max_diameter = max(self.max_diameter, current_diameter)
            
            # Return height of current subtree
            return 1 + max(left_height, right_height)
        
        dfs(root)
        return self.max_diameter


# Alternative solution without using instance variable

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        def dfs(node):
            """
            Returns tuple of (height, max_diameter_in_subtree).
            
            Args:
                node: TreeNode - Current node being processed
                
            Returns:
                tuple: (height of subtree, maximum diameter in subtree)
            """
            if not node:
                return 0, 0
            
            left_height, left_diameter = dfs(node.left)
            right_height, right_diameter = dfs(node.right)
            
            # Diameter through current node
            # Note: This counts EDGES. To count NODES instead, use: left_height + right_height + 1
            current_diameter = left_height + right_height
            
            # Maximum diameter in this subtree
            max_diameter = max(current_diameter, left_diameter, right_diameter)
            
            # Height of current subtree
            height = 1 + max(left_height, right_height)
            
            return height, max_diameter
        
        _, diameter = dfs(root)
        return diameter

# Approach : BFS

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        """
        BFS + reverse level-order solution.
        
        Idea:
        1. Use BFS to collect all nodes in level order (top-down).
        2. Process nodes in reverse order so children are handled
           before their parents (bottom-up).
        3. Compute subtree heights and diameter at each node.
        
        Why reverse? Heights depend on children, so we need children's
        heights before computing parent's height.
        
        Time Complexity: O(n) - two passes through all nodes
        Space Complexity: O(n) - store all nodes + heights map
        """
        if not root:
            return 0
        
        # ---------- Step 1: BFS traversal (top-down) ----------
        # Collect all nodes level by level using a queue
        queue = deque([root])
        all_nodes = []  # Store nodes in level-order
        
        while queue:
            node = queue.popleft()
            all_nodes.append(node)
            
            # Add children to queue for next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # ---------- Step 2: Bottom-up processing (reverse order) ----------
        heights = {}  # node -> height (number of edges to deepest leaf)
        max_diameter = 0
        
        # Process in reverse: leaves first, then their parents, up to root
        # This ensures when we process a node, its children's heights are already computed
        for node in reversed(all_nodes):
            # Get heights of children (0 if child is None)
            left_height = heights.get(node.left, 0)
            right_height = heights.get(node.right, 0)
            
            # Diameter through this node = sum of left and right subtree heights
            # This represents the longest path passing through this node
            # Note: This counts EDGES. To count NODES instead, use: left_height + right_height + 1
            current_diameter = left_height + right_height
            max_diameter = max(max_diameter, current_diameter)
            
            # Height of current node = 1 + max of children's heights
            # The +1 represents the edge from this node to its taller child
            heights[node] = 1 + max(left_height, right_height)
        
        return max_diameter


# DFS vs BFS Tradeoffs

# Space Complexity:

# DFS (Depth-First Search):
# Space: O(h) where h is the height of the tree
# Uses the call stack (or explicit stack)
# Only stores nodes along the current path from root to leaf

# BFS (Breadth-First Search):
# Space: O(w) where w is the maximum width of the tree
# Uses a queue
# Stores all nodes at the current level

# Key Insight for Space:
# For a complete/balanced binary tree with n nodes:
# Height h = O(log n) ← This is the formula.
# Maximum width w = O(n) (at the last level, approximately n/2 nodes)

# Therefore:
# DFS space: O(log n) for balanced trees
# BFS space: O(n) for balanced trees



# Note: Using NODE-COUNT height throughout (None → 0, leaf → 1),
# consistent with the Height/Diameter sections above.

# Case 1: Complete Binary Tree
# Definition: All levels completely filled except possibly the last, which is filled left to right.

# Example 1: n = 7 nodes

#        1          ← Level 0
#       / \
#      2   3        ← Level 1
#     /|   |\
#    4 5   6 7      ← Level 2

# Path from root to leaf: 1 → 2 → 4

# Formulas & Analysis:
# Height (nodes): h = ⌊log₂(n)⌋ + 1 = ⌊log₂(7)⌋ + 1 = 2 + 1 = 3 nodes
# DFS Space: O(h) = O(3) = O(log n) ✓ WINNER

# Stack frames: dfs(1) → dfs(2) → dfs(4) = 3 frames

# BFS Space: O(w) = O(n)
# Max width at level 2: queue = [4,5,6,7] = 4 nodes ≈ n/2


# Case 2: Balanced Binary Tree
# Definition: For every node, |left_height - right_height| ≤ 1

# Example 1: n = 6 nodes (balanced but NOT complete)

#        1          ← Level 0
#       / \
#      2   3        ← Level 1
#     / \   \
#    4   5   6      ← Level 2

# Note: Not complete because last level is not filled left-to-right (gap after node 5)

# Path from root to deepest leaf: 1 → 2 → 4

# Formulas & Analysis:
# Height (nodes): h ≈ ⌊log₂(6)⌋ + 1 = 2 + 1 = 3 nodes
# DFS Space: 3 stack frames = O(log n) ✓ WINNER
# BFS Space: Max width at level 2 = 3 nodes = O(n)

# Balance check at each node:
# height(4) = 1, height(5) = 1, height(6) = 1
# height(2) = 1 + max(1,1) = 2
# height(3) = 1 + max(0,1) = 2   (node 3 has no left child → height(None)=0)
# height(1) = 1 + max(2,2) = 3

# Node 1: |height(left=2)=2 - height(right=3)=2| = 0 ≤ 1 ✓
# Node 2: |height(left=4)=1 - height(right=5)=1| = 0 ≤ 1 ✓
# Node 3: |height(left=None)=0 - height(right=6)=1| = 1 ≤ 1 ✓


# Case 3: Skewed/Unbalanced Tree
# Definition: Essentially a linked list (worst case)

# Example: n = 4 nodes

# 1                 ← Level 0
#  \
#   2               ← Level 1
#    \
#     3             ← Level 2
#      \
#       4           ← Level 3

# Path from root to leaf: 1 → 2 → 3 → 4

# Formulas & Analysis:
# Height (nodes): h = 4 nodes = n  (NOT using log formula!)
# DFS Space: O(n) = O(4) = 4 stack frames

# Full path on stack: dfs(1) → dfs(2) → dfs(3) → dfs(4)

# BFS Space: O(1) ✓ WINNER
# Only 1 node per level: queue = [1] → [2] → [3] → [4] (max size = 1)


# Summary Table - DFS vs BFS Space Complexity

# Tree Type    DFS Space (stack frames)      BFS Space (queue size)        Winner
# Complete     O(log n)                      O(n)                          DFS ✓
# Balanced     O(log n)                      O(n) worst case               DFS ✓
# Skewed       O(n)                          O(1)                          BFS ✓

# Key Insight:
#   • DFS space = O(height) = O(depth of tree) = path length (in nodes)
#   • BFS space = O(width) = O(breadth of tree) = max nodes at any level
#   • For balanced trees: DFS wins with O(log n) vs O(n)
#   • For skewed trees: BFS wins with O(1) vs O(n)



# Variant : Find diameter path

# class Solution:
#     def diameterOfBinaryTreePath(self, root: TreeNode):
#         """
#         Return both the diameter (in edges) and the actual longest path.

#         CONVENTION USED (node-count height):
#             height(None) = 0
#             height(leaf) = 1
#             height(node) = 1 + max(height(left), height(right))

#         DIAMETER FORMULA:
#             diameter_through_node = left_height + right_height
#             (no correction needed, because of the node-count convention above)

#         PATH CONVENTION:
#             Every recursive call returns a path in ROOT-TO-LEAF order:
#             [this_node, child, grandchild, ..., deepest_leaf]

#         Time Complexity: O(n) - each node visited once
#         Space Complexity: O(h) - recursion stack + path storage, h = tree height
#         """
#         # Best diameter (edges) seen across ALL nodes so far. Tracked
#         # globally because the longest path may not pass through the root.
#         self.max_diameter = 0

#         # The actual node values forming that best diameter path.
#         self.diameter_path = []

#         def dfs(node):
#             """
#             Returns (height, path_to_deepest_leaf) for the subtree at `node`.
#             height: node-count height (None->0, leaf->1)
#             path:   ROOT-TO-LEAF values along the single deepest branch.
#             Side effect: updates self.max_diameter/self.diameter_path.
#             """
#             # Empty subtree: no height, no path.
#             if not node:
#                 return 0, []

#             # Get info from both children first (post-order).
#             left_height, left_path = dfs(node.left)
#             right_height, right_path = dfs(node.right)

#             # Longest path THROUGH this node = left side + right side.
#             current_diameter = left_height + right_height

#             if current_diameter > self.max_diameter:
#                 self.max_diameter = current_diameter
#                 # left_path is ROOT-TO-LEAF from node.left down; reverse it
#                 # so it reads LEAF-TO-ROOT leading INTO node from the left.
#                 # right_path is already ROOT-TO-LEAF, which is the direction
#                 # we want going OUT of node to the right. Keep as-is.
#                 self.diameter_path = left_path[::-1] + [node.val] + right_path

#             # Return only the deeper branch to the parent, since the parent
#             # only needs ONE path from each child to combine with the other
#             # child's path for its own diameter check.
#             if left_height >= right_height:
#                 return left_height + 1, [node.val] + left_path
#             else:
#                 return right_height + 1, [node.val] + right_path

#         dfs(root)
#         return self.max_diameter, self.diameter_path

# Variant : Find diameter of N-ary tree (https://leetcode.com/problems/diameter-of-n-ary-tree/description/)

# Definition for a Node.
# class Node:
#     def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
#         self.val = val
#         self.children = children if children is not None else []

# class Solution:
#     def diameter(self, root: 'Node') -> int:
#         """
#         Approach:
#         - Use DFS to traverse the tree
#         - For each node, find the two largest heights among its children
#         - Diameter through current node = first_max + second_max
#         - Track global maximum diameter across all nodes
        
#         Time Complexity: O(n) where n is the number of nodes
#         Space Complexity: O(h) where h is the height of the tree
#         """
#         # Track global maximum diameter across all nodes visited
#         # Needed because diameter might not pass through root - could be entirely within a subtree
#         self.max_diameter = 0
        
#         def dfs(node):
#             # Base case: empty node has height 0
#             if not node:
#                 return 0
            
#             # Track the two largest heights among all children
#             # These represent the two deepest paths from current node
#             first_max = second_max = 0
            
#             # Process each child to get its subtree height
#             for child in node.children:
#                 child_height = dfs(child)
                
#                 # Maintain first_max and second_max without sorting
#                 if child_height > first_max:
#                     # New largest found - demote current largest to second place
#                     second_max = first_max
#                     first_max = child_height
#                 elif child_height > second_max:
#                     # New second largest found - update second_max only
#                     second_max = child_height
#                 # If child_height <= second_max, no updates needed
            
#             # Calculate diameter through current node
#             # This is the longest path that passes through current node:
#             # path goes down first_max steps, through current node, then down second_max steps
#             current_diameter = first_max + second_max
            
#             # Update global maximum diameter if current node gives us a longer path
#             # We check every node because the optimal path might not include the root
#             self.max_diameter = max(self.max_diameter, current_diameter)
            
#             # Return height of current subtree for parent node's calculations
#             # Height = 1 (current node) + height of tallest child subtree
#             return 1 + first_max
        
#         # Start DFS from root
#         dfs(root)
#         return self.max_diameter






        