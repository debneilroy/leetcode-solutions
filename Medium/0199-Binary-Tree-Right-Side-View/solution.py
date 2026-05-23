"""
LeetCode 199. Binary Tree Right Side View
Difficulty: Medium
URL: https://leetcode.com/problems/binary-tree-right-side-view/
"""

# Binary Tree Types 

# 1. Full Binary Tree

# Every node has either 0 or 2 children (no nodes with exactly 1 child). Also called a "strict" or "proper" binary tree.

#     1
#    / \
#   2   3
#  / \
# 4   5

# Properties: Min nodes = 2h+1, Max nodes = 2^(h+1)-1
# Use cases: Expression trees, decision trees

# Traversals (all types):

# TC: O(n) - visit each node once
# SC: O(h) recursive call stack / O(n) iterative stack worst case

# h = height, for full tree: O(log n) ≤ h ≤ O(n)

# 2. Complete Binary Tree

# All levels filled except possibly the last, which fills left-to-right. Used in heap implementations.

#     1
#    / \
#   2   3
#  / \
# 4   5

# Properties: Height = ⌊log₂(n)⌋, efficiently stored in array
# Use cases: Binary heaps, priority queues

# Traversals:

# TC: O(n)
# SC:

# DFS (Inorder/Preorder/Postorder): O(log n) - height guaranteed O(log n)
# Level-order: O(w) where w = max width = O(n/2) = O(n) at last level


# 3. Perfect Binary Tree (Subset of balanced trees)

# All internal nodes have exactly 2 children AND all leaves at same level. Most balanced possible tree.

#     1
#    / \
#   2   3
#  / \ / \
# 4  5 6  7

# Properties: Exactly 2^(h+1)-1 nodes, exactly 2^h leaves
# Use cases: Theoretical optimal cases, divide-and-conquer

# Traversals:

# TC: O(n)
# SC:

# DFS: O(log n) - height = ⌊log₂(n)⌋
# Level-order: O(2^h) = O(n/2) = O(n) at last level (half the nodes are leaves)


# 4. Balanced Binary Tree

# For every node, height difference between left and right subtrees ≤ 1. Guarantees O(log n) operations. At each level of a balanced tree, you can have at most double the nodes of the previous level (since each node can have at most 2 children).

# Height: number of edges on longest path from node to leaf. Leaves have height 0.

#     1         height = 2
#    / \
#   2   3       heights: 1, 0
#  /
# 4             height = 0

# At node 1: |height(left) - height(right)| = |1 - 0| = 1 

# Properties: Height always O(log n), balance factor ∈ {-1, 0, 1}
# Types: AVL trees, Red-Black trees
# Use cases: Databases, file systems, associative arrays

# Traversals:

# TC: O(n)
# SC:

# DFS: O(log n) - height guaranteed O(log n)
# Level-order: O(n) worst case

# 5. Degenerate/Skewed Tree

# Each parent has only one child, degenerates into a linked list. Worst-case scenario for BST.
# 1          1
#  \        /
#   2      2
#    \    /
#     3  3

# Properties: Height = n-1, all operations degrade to O(n)
# Why it matters: Shows need for self-balancing trees

# Traversals:

# TC: O(n)
# SC:

# DFS: O(n) - height = n-1, full recursion depth
# Level-order: O(1) - only one node per level in queue

# 6. Binary Search Tree (BST)

# For each node: left subtree < node < right subtree. Enables efficient search operations.

#     5
#    / \
#   3   7
#  / \   \
# 1   4   9

# Properties: Inorder traversal gives sorted sequence
# Operations: Search/Insert/Delete O(log n) avg, O(n) worst
# Use cases: Dynamic sets, symbol tables, range queries

# Traversals:

# TC: O(n)
# SC:

# DFS: O(h) where h = height

# Balanced BST: O(log n)
# Skewed BST: O(n)

# Level-order: O(w) where w = max width

# Balanced: O(n/2) = O(n)
# Skewed: O(1)



# DFS (Inorder/Preorder/Postorder):

# TC: Always O(n)
# SC: O(h) for recursion stack

# Best case (balanced): O(log n)
# Worst case (skewed): O(n)
# Iterative uses explicit stack: same SC

# BFS (Level-order):

# TC: Always O(n)
# SC: O(w) where w = maximum width

# Perfect/Complete: O(n) - last level has ~n/2 nodes
# Skewed: O(1) - only one node per level

# Morris Traversal (Advanced):

# TC: O(n)
# SC: O(1) - no stack/recursion, modifies tree temporarily



# Definition for a binary tree node.

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# Approach : BFS Level Order Traversal

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        Returns the right side view of a binary tree using BFS (Level-order traversal).
        
        Approach: 
        Traverse the tree level by level and capture the last (rightmost) node at each level.
        Use a queue to process nodes level by level, and track level size to identify
        the rightmost node.
        
        Time Complexity: O(n)
            - We visit each node in the tree exactly once
            - n = total number of nodes in the tree
            - Each node is enqueued once and dequeued once: O(n)
            - All other operations (appending to result, checking children) are O(1)
            - Total: O(n)
        
        Space Complexity: O(w) where w is the maximum width of the tree
            - Queue space: O(w) - stores all nodes at the widest level
            - Result array: O(h) where h is height (number of levels with visible nodes)
            - w is the maximum number of nodes at any single level
            - For a perfect binary tree: w ≈ n/2, so O(n) worst case
            - For a skewed tree: w = 1, so O(1) best case
            - For a balanced tree: w ≈ n/2, so O(n)
            - The queue dominates space complexity: O(w)
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            
            # Process all nodes at current level
            for i in range(level_size):
                node = queue.popleft()
                
                # If this is the last node in the level, add to result
                if i == level_size - 1:
                    result.append(node.val)
                
                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return result

# Approach : Recursive DFS

# The idea is to traverse the tree using a pre-order traversal (visit the node, then go to the right, then to the left), which naturally prioritizes nodes that are more to the right, which are the ones visible from the right side view.

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        Returns the right side view using DFS with right-first traversal.
        
        Approach:
        Perform DFS visiting the right subtree before the left subtree.
        Track the current depth and add a node to the result only when we
        encounter a new depth for the first time. Since we go right-first,
        the first node we see at each depth is the rightmost visible node.
        
        Time Complexity: O(n)
            - We visit each node in the tree exactly once
            - n = total number of nodes in the tree
            - Each recursive call processes one node: O(1) per node
            - Total recursive calls: n
            - Total: O(n)
        
        Space Complexity: O(h) where h is the height of the tree
            - Recursion call stack: O(h) - maximum depth of recursion
            - Result array: O(h) - stores one node per level (h levels total)
            - h is the height/depth of the tree (number of levels)
            - For a balanced tree: h = log(n), so O(log n) best case
            - For a skewed tree: h = n, so O(n) worst case
            - The recursion stack dominates space complexity: O(h)
            
            Comparison with BFS:
            - DFS is more space-efficient for wide, shallow trees
            - BFS is more space-efficient for tall, narrow trees
            - For balanced trees: DFS uses O(log n) vs BFS uses O(n)
        """
        result = []
        
        def dfs(node, depth):
            """
            Helper function for DFS traversal.
            
            Args:
                node: Current node being visited
                depth: Current depth/level in the tree (0-indexed)
            
            The key insight: len(result) equals the number of depths we've seen.
            When depth == len(result), we're seeing this depth for the first time.
            """
            if not node:
                return
            
            # If this is the first time we're seeing this depth, add the node
            # Since we traverse right-first, this is guaranteed to be the rightmost node
            if depth == len(result):
                result.append(node.val)
            
            # Visit right subtree first (prioritize rightmost nodes)
            dfs(node.right, depth + 1)
            # Then visit left subtree (only matters when right doesn't exist)
            dfs(node.left, depth + 1)
        
        dfs(root, 0)
        return result

# ┌─────────────────────┬──────────────┬──────────────┬──────────────┬─────────────────┐
# │   Tree Shape        │  BFS Time    │  BFS Space   │  DFS Time    │   DFS Space     │
# ├─────────────────────┼──────────────┼──────────────┼──────────────┼─────────────────┤
# │ Balanced            │    O(n)      │   O(n)       │    O(n)      │   O(log n) ✓    │
# │ (h = log n)         │              │   (width≈n/2)│              │   (height)      │
# ├─────────────────────┼──────────────┼──────────────┼──────────────┼─────────────────┤
# │ Skewed (Right/Left) │    O(n)      │   O(1) ✓     │    O(n)      │   O(n)          │
# │ (h = n)             │              │   (width=1)  │              │   (height)      │
# ├─────────────────────┼──────────────┼──────────────┼──────────────┼─────────────────┤
# │ Perfect             │    O(n)      │   O(n)       │    O(n)      │   O(log n) ✓    │
# │ (all levels full)   │              │   (width=n/2)│              │   (height)      │
# └─────────────────────┴──────────────┴──────────────┴──────────────┴─────────────────┘

# Another recursive DFS approach using map

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> list[int]:

        if root is None:
            return []

        map = {}

        def dfs(node, level):
            if not node:
                return

            if level not in map:
                map[level] = node

            dfs(node.right, level + 1)
            dfs(node.left, level + 1)

        dfs(root, 0)
        
        # After DFS, map will contain {level : rightmost nodes}

        result = []
        for _, node in map.items():
            result.append(node.val)
        return result


# Iterative DFS version

class Solution:
    def rightSideView(self, root):
        """
        Returns the right side view using DFS with right-first traversal (iterative version).

        Approach:
        Use an explicit stack to simulate the recursive DFS.
        Always visit the right subtree before the left subtree.
        Track the current depth and add a node to the result only when we
        encounter a new depth for the first time. Because we process the
        right child first, the first node we encounter at each depth is
        the rightmost visible node.

        Time Complexity: O(n)
            - Each node is pushed to and popped from the stack exactly once.
            - Work per node is O(1).
            - Total = O(n).

        Space Complexity: O(h) where h is the height of the tree
            - The stack holds at most one frame per tree level during DFS.
            - The result array holds at most one value per level.
            - Best case (balanced tree): O(log n)
            - Worst case (skewed tree): O(n)
        """

        if not root:
            return []

        result = []

        # Stack stores (node, depth)
        # Use right-first ordering by pushing left *after* right.
        stack = [(root, 0)]

        while stack:
            node, depth = stack.pop()

            # if not node: # Not required
            #     continue

            # First time reaching this depth → this node is the rightmost one
            if depth == len(result):
                result.append(node.val)

            # Push LEFT first, RIGHT second
            # because the stack is LIFO, RIGHT is processed first.
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))

        return result

# Iterative DFS version using map

class Solution:
    def rightSideView(self, root):
        if root is None:
            return []

        level_map = {}   # level → first node seen at that level (rightmost)
        
        # Stack holds (node, level)
        # To simulate right-first DFS, push LEFT first, then RIGHT.
        stack = [(root, 0)]

        while stack:
            node, level = stack.pop()

            # if not node:
            #     continue

            # First node reached at this level → rightmost due to right-first traversal
            if level not in level_map:
                level_map[level] = node

            # Push left first, then right → right is processed first (LIFO)
            if node.left:
                stack.append((node.left, level + 1))
            if node.right:
                stack.append((node.right, level + 1))

        # level_map preserves insertion order (Python 3.7+)
        result = []
        for _, node in level_map.items():
            result.append(node.val)

        return result

# Variant 1 : Binary Tree Left-Right Side View

# Given the root of a binary tree, imagine yourself standing on the right side of it and your best friend standing on the left side, both observing the tree from their respective sides. Return the values of the nodes you can both see, first from the left side (bottom to top), followed by those from the right side (top to bottom). Duplicates allowed but consider root node's value only once.

# Example 1:
# Input: root = [1,2,3,null,5,null,4]

# Tree:
#       1
#      / \
#     2   3
#      \   \
#       5   4

# Output: [5, 2, 1, 3, 4]

# Explanation:
# - Left view (bottom-up): [5, 2, 1]
# - Right view (top-down): [1, 3, 4]
# - Combined (skip duplicate root): [5, 2, 1] + [3, 4] = [5, 2, 1, 3, 4]

# Example 2:
# Input: root = [1,2,3,4,null,null,5]

# Tree:
#       1
#      / \
#     2   3
#    /     \
#   4       5

# Output: [4, 2, 1, 3, 5]

# Explanation:
# - Left view (bottom-up): [4, 2, 1]
# - Right view (top-down): [1, 3, 5]
# - Combined (skip duplicate root): [4, 2, 1] + [3, 5] = [4, 2, 1, 3, 5]

# Example 3:
# Input: root = [1,3,5,6,null,7,9,8]

# Tree:
#         1
#        / \
#       3   5
#      /   / \
#     6   7   9
#    /
#   8

# Output: [8, 6, 3, 1, 5, 9]

# - Note: Root 1 appears in both views, so we skip it from right view
# - Note: Node 8 appears in both views (only node at level 3), so we skip it from right view

# Approach : BFS

# class Solution:
#     def leftRightSideView(self, root: Optional[TreeNode]) -> list[int]:
#         """
#         Returns boundary traversal combining left view (bottom-up) and right view (top-down).
        
#         Approach:
#         1. Use BFS (level-order traversal) to traverse the tree
#         2. At each level, capture:
#            - First node (leftmost)
#            - Last node (rightmost)
#         3. Build result by combining:
#            - Reversed left_side (bottom to top)
#            - right_side excluding duplicates (top to bottom)
        
#         Time Complexity: O(n)
#             - Single BFS traversal visits each node once: O(n)
#             - Building result array: O(h) where h is height
#             - Total: O(n)
        
#         Space Complexity: O(n)
#             - Queue: O(w) where w is maximum width ≈ O(n/2) for perfect trees
#             - left_side array: O(h)
#             - right_side array: O(h)
#             - result array: O(h)
#             - Total dominated by queue: O(w) ≈ O(n) worst case
#         """
#         # Edge case: empty tree
#         if not root:
#             return []
        
#         left_side = []   # Stores leftmost node at each level
#         right_side = []  # Stores rightmost node at each level
#         q = deque([root])
        
#         # Perform level-order traversal (BFS)
#         while q:
#             size = len(q)  # Number of nodes at current level
            
#             # Process all nodes at current level
#             for i in range(size):
#                 node = q.popleft()
                
#                 # First node in level is the leftmost
#                 if i == 0:
#                     left_side.append(node.val)
                
#                 # Last node in level is the rightmost
#                 if size == i + 1:
#                     right_side.append(node.val)
                
#                 # Add children to queue for next level
#                 if node.left:
#                     q.append(node.left)
#                 if node.right:
#                     q.append(node.right)
        
#         # Build result: left view (bottom-up) + right view (top-down, skip duplicates)
#         result = []
        
#         # Add left view in reverse order (bottom to top)
#         for i in range(len(left_side) - 1, -1, -1):
#             result.append(left_side[i])
#             # print(left_side[i], end=' ') # if we need to print the values
        
#         # Add right view, skipping nodes that are duplicates at the same level
#         # (i.e., when a node is both leftmost and rightmost at a level)
#         for i in range(len(right_side)):
#             # Only add if different from left_side at this level
#             # if left_side[i] != right_side[i]: # if duplicates not allowed
#                 result.append(right_side[i])
#                 # print(right_side[i], end=' ')

#         # if only the root node appears once, but all other nodes which can be seen from both left and right sides appear as they are (in Example 3 above output will be [8, 6, 3, 1, 5, 9, 8])
#         # for i in range(1, len(right_side)):
#         #     result.append(right_side[i])
        
#         return result

# # Solution using DFS

# class Solution:
#     def leftRightSideView(self, root: Optional[TreeNode]) -> List[int]:
#         """
#         Returns boundary view: left side (bottom-up) + right side (top-down).
#         Root appears only ONCE (included in left view, skipped in right view).
#         Other duplicates are allowed.
        
#         Approach: Single DFS traversal with left-first order

#         Time Complexity: ALWAYS O(n)
#         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#         Best Case:    O(n)  ← Must visit all n nodes
#         Average Case: O(n)  ← Must visit all n nodes
#         Worst Case:   O(n)  ← Must visit all n nodes

#         Why always O(n)?
#         - The algorithm must visit EVERY node in the tree to determine left and right views
#         - Tree shape doesn't matter for time - we still visit each node exactly once
#         - No early termination possible
#         - Total operations: n visits × O(1) work per visit = O(n)
                
#         Space Complexity: O(h) where h = height of tree
#         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#         Best Case:    O(log n)  ← Perfectly balanced tree, h = log n
#         Average Case: O(log n)  ← Reasonably balanced tree, h ≈ log n
#         Worst Case:   O(n)      ← Completely skewed tree, h = n

#         Why does space vary?
#         - Space is dominated by recursion stack depth and array sizes
#         - Both depend on HEIGHT (h), not number of nodes (n)
#         - Height varies based on tree shape:
#         * Balanced: h = O(log n)
#         * Skewed:   h = O(n)

#         Components:
#         1. Recursion call stack: O(h)
#            - Maximum depth of recursive calls = tree height
#            - Each call adds a frame to the stack
        
#         2. leftmost array: O(h)
#            - Stores one value per level
#            - Number of levels = height h
        
#         3. rightmost array: O(h)
#            - Stores one value per level
        
#         4. result array: O(h)
#            - Output array, typically not counted as "extra" space
#            - But stores at most 2h - 1 values
        
#         Total auxiliary space: O(h) + O(h) + O(h) = O(3h) = O(h)
        
#         Worst Case Space: O(n)
#         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         Occurs when tree is COMPLETELY SKEWED (all left or all right)
        
#         Example - Right Skewed Tree (h = n):
#             1
#              \
#               2
#                \
#                 3
#                  \
#                   4
#                    \
#                     5
        
#         - Height h = n (5 nodes, 5 levels)
#         - Recursion stack depth = n
#         - leftmost array size = n
#         - rightmost array size = n
#         - Space: O(n)
        
#         Best Case Space: O(log n)
#         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         Occurs when tree is PERFECTLY BALANCED
        
#         Example - Balanced Tree (h = log n):
#                 1
#                / \
#               2   3
#              / \ / \
#             4 5 6  7
        
#         - 7 nodes, height h = log₂(7) ≈ 3
#         - Recursion stack depth = 3
#         - leftmost array size = 3
#         - rightmost array size = 3
#         - Space: O(log n)

#         # General info about space complexity

#         Why O(h), not O(n)?
#         Space depends on HEIGHT, not number of nodes (indirectly related).
#         For the same n nodes, different tree shapes have different heights:
        
#         Example (both have n=7):
#           Balanced tree: h=3 → Space O(3)
#           Skewed tree:   h=7 → Space O(7)
        
#         Height range: log n ≤ h ≤ n
#         Therefore space range: O(log n) ≤ Space ≤ O(n)
#         """
#         if not root:
#             return []
        
#         leftmost = []   # O(h) space - one value per level
#         rightmost = []  # O(h) space - one value per level
        
#         def dfs(node, level):
#             """
#             DFS helper function.
            
#             Recursion Stack Space:
#             - Maximum recursive depth = tree height h
#             - Each call uses O(1) space for parameters and local variables
#             - Total stack space: O(h)
#             """
#             if not node:
#                 return
            
#             # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#             # CAPTURE LEFTMOST: Only on first visit to this level
#             # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#             if level == len(leftmost):
#                 leftmost.append(node.val)  # O(1) amortized
            
#             # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#             # CAPTURE RIGHTMOST: Update on EVERY visit to this level
#             # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#             # Keep OVERWRITING to ensure we capture the LAST (rightmost) node.
#             #
#             # Why overwrite?
#             # - DFS visits nodes left-to-right within each level
#             # - Each visit updates rightmost[level]
#             # - The FINAL update will be the actual rightmost node
#             #
#             # Example at level 1:
#             #       1
#             #      / \
#             #     2   3
#             # Visit 2: rightmost[1] = 2
#             # Visit 3: rightmost[1] = 3 (OVERWRITE)
#             # Result: rightmost[1] = 3 ✓ (correct rightmost)
            
#             if level == len(rightmost):
#                 rightmost.append(node.val)  # O(1) amortized
#             else:
#                 rightmost[level] = node.val  # O(1) - array access and update
            
#             # Recursive calls - each node visited once total
#             dfs(node.left, level + 1)   # O(1) call overhead
#             dfs(node.right, level + 1)  # O(1) call overhead
        
#         # Execute DFS starting from root at level 0
#         dfs(root, 0)  # O(n) total time, O(h) stack space
        
#         result = []  # O(h) space for output
        
#         # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         # BUILD RESULT: O(h) time
#         # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
#         # Add left view in REVERSE order (bottom to top): O(h)
#         for i in range(len(leftmost) - 1, -1, -1):
#             result.append(leftmost[i])  # O(1) amortized
        
#         # Add right view (top to bottom), SKIP root: O(h)
#         for i in range(1, len(rightmost)):
#             result.append(rightmost[i])  # O(1) amortized
        
#         return result

# # Iterative DFS version

# class Solution:
#     def leftRightSideView(self, root):
#         """
#         Computes a combined left-view (bottom→top) and right-view (top→bottom)
#         using an iterative DFS approach.

#         TIME COMPLEXITY: O(n)
#             - Each node is visited exactly once via DFS.
#             - Merging lists is O(h), where h is tree height.
#             - Total = O(n)

#         SPACE COMPLEXITY: O(h)
#             - DFS stack can go as deep as height h.
#             - leftmost and rightmost arrays store one item per level → O(h).
#             - Total = O(h)
#         """
#         if not root:
#             return []

#         leftmost = []    # first node seen at each level
#         rightmost = []   # last node seen at each level

#         # ---------------- ITERATIVE DFS ----------------
#         stack = [(root, 0)]

#         while stack:
#             node, level = stack.pop()

#             # Capture leftmost — only first visit to this level
#             if level == len(leftmost):
#                 leftmost.append(node.val)

#             # Capture rightmost — update EVERY visit to this level
#             if level == len(rightmost):
#                 rightmost.append(node.val)
#             else:
#                 rightmost[level] = node.val

#             # Push RIGHT first, then LEFT, so LEFT is processed first (LIFO)
#             if node.right:
#                 stack.append((node.right, level + 1))
#             if node.left:
#                 stack.append((node.left, level + 1))

#         # ---------------- TWO POINTER MERGE ----------------
#         result = []

#         # Left view (bottom → top)
#         i = len(leftmost) - 1
#         while i >= 0:
#             result.append(leftmost[i])
#             i -= 1

#         # Right view (top → bottom)
#         # Skip ONLY root (index 0)
#         j = 1
#         while j < len(rightmost):
#             result.append(rightmost[j])
#             j += 1

#         return result


# Variant 2 : Binary Tree Top View

# Given the root of a binary tree, imagine yourself standing on the top of it, return the values of the nodes you can see ordered from left to right.

# When looking from the top (bird's eye view), each node has a horizontal position. For nodes at the same horizontal position, only the topmost (shallowest) node is visible.

# Example 1:
# Input: 

# root = [1,2,3,null,5,null,4]

# Tree:
#       1
#      / \
#     2   3
#      \   \
#       5   4

# Output: [2, 1, 3, 4]

# Explanation:
# Looking from top, we see nodes at these horizontal positions:
#   Position -1: Node 2
#   Position  0: Node 1 (Node 5 is hidden below it)
#   Position  1: Node 3
#   Position  2: Node 4

# From left to right: [2, 1, 3, 4]

# Example 2:
# Input: root = [1,2,3,null,4,8,null,null,null,null,null,null,5]

# Tree:
#         1
#        / \
#       2   3
#        \  /
#         4 8
#          \
#           5

# Output: [2, 1, 3]

# Explanation:
# Looking from top, we see nodes at these horizontal positions:
#   Position -1: Node 2
#   Position  0: Node 1 (Nodes 4 and 8 are hidden below it)
#   Position  1: Node 3 (Node 5 is hidden below it)

# From left to right: [2, 1, 3]

# Note: The condition row < map[column][1] triggers when node 3 is visited.
# DFS explores the left subtree first, so node 5 (deeper, row=3) gets added 
# to column 1 before node 3 (shallower, row=1). Node 3 then replaces node 5
# because it's closer to the top.

# Approach : DFS with row and column tracking

# class Solution:
#     def topSideView(self, root: Optional[TreeNode]) -> List[int]:
#         """
#         Returns the top view of a binary tree (nodes visible from above, left to right).
        
#         Approach: DFS with horizontal distance (column) and depth (row) tracking.
        
#         Key Concepts:
#         - Column (horizontal distance): Position of node from root
#           * Root has column = 0
#           * Left child: parent_column - 1
#           * Right child: parent_column + 1
        
#         - Row (depth): Distance from root
#           * Root has row = 0
#           * Children: parent_row + 1
        
#         - For each column, keep only the node with MINIMUM row (topmost/shallowest)
        
#         Time Complexity: O(n) where n is number of nodes
#         Space Complexity: O(h) where h is height (recursion stack)
#         """
#         if root is None:
#             return []
        
#         # Map: column -> (node, row) - stores the topmost node at each horizontal position
#         # FOR BOTTOM VIEW: Same structure, stores the bottommost node instead
#         col_map = {}
        
#         # Track leftmost and rightmost columns for efficient result building
#         min_col, max_col = 0, 0
        
#         def dfs(node: Optional[TreeNode], row: int, column: int) -> None:
#             """
#             Traverse tree tracking depth and horizontal position.
            
#             Args:
#                 node: Current tree node
#                 row: Vertical depth from root (depth level)
#                 column: Horizontal distance from root (left=-1, right=+1)
#             """
#             # NONLOCAL EXPLANATION:
#             # ─────────────────────────────────────────────────────────────────
#             # We need to track the leftmost and rightmost columns visited during
#             # DFS to know the final range for building our result array.
#             # 
#             # Without 'nonlocal', this line would crash:
#             #   min_col = min(min_col, column)  # ❌ UnboundLocalError!
#             # 
#             # Why? Python sees "min_col = ..." and assumes you want a NEW LOCAL
#             # variable called min_col inside dfs(). But the right side tries to
#             # READ min_col before it's been assigned locally → error.
#             # 
#             # Example with tree:  1
#             #                    /
#             #                   2
#             # 
#             # Without nonlocal:
#             #   dfs(node=1, row=0, col=0) → tries "min_col = min(min_col, 0)"
#             #   Python: "min_col is local, but you're reading it before assigning!"
#             #   ❌ UnboundLocalError
#             # 
#             # With nonlocal:
#             #   dfs(node=1, row=0, col=0) → min_col = min(0, 0) = 0  ✓ modifies outer
#             #   dfs(node=2, row=1, col=-1) → min_col = min(0, -1) = -1  ✓ modifies outer
#             #   Final: min_col=-1, max_col=0 → range(-1, 1) → [2, 1]
#             # 
#             # Note: 'map' doesn't need nonlocal because we modify it (map[x] = ...)
#             #       rather than reassign it (map = ...).
#             # ─────────────────────────────────────────────────────────────────
#             nonlocal min_col, max_col
            
#             if not node:
#                 return
            
#             # Track the range of columns for efficient result building
#             min_col = min(min_col, column)
#             max_col = max(max_col, column)
            
#             # CONDITION: row < map[column][1]
#             # ─────────────────────────────────────────────────────────────────
#             # This triggers when a SHALLOWER node (smaller row) is visited AFTER
#             # a DEEPER node (larger row) in the same column.
#             # 
#             # Example where condition triggers:
#             #         1
#             #        / \
#             #       2   3
#             #        \  /
#             #         4 8
#             #          \
#             #           5
#             # 
#             # DFS order: 1 → 2 → 4 → 5 → 3 → 8
#             # - Visit 5 (col=1, row=3) → map[1] = (5, 3)
#             # - Visit 3 (col=1, row=1) → row < map[1][1]? → 1 < 3? YES! ✓
#             #   TRIGGERED! Replace 5 with 3 (node 3 is shallower, closer to top)
#             # 
#             # Why it happens: DFS explores left subtree fully first, so deeper
#             # node 5 gets added before we backtrack to shallower node 3.

#             # FOR BOTTOM VIEW: Change condition from row < to row >= 
#             # This keeps the DEEPEST (bottommost) node at each column instead
#             # ─────────────────────────────────────────────────────────────────
#             if column not in col_map or row < col_map[column][1]: # FOR BOTTOM VIEW: Change to row >= map[column][1]
#                 col_map[column] = (node, row)
            
#             # Recursive calls: left child (column-1), right child (column+1)
#             dfs(node.left, row + 1, column - 1)
#             dfs(node.right, row + 1, column + 1)
        
#         # Start DFS from root at row=0, column=0
#         dfs(root, 0, 0)

#         # ALTERNATIVE WITHOUT nonlocal:
#         # If we wanted to avoid nonlocal, the DFS function would remain the same
#         # (just remove the nonlocal declaration and min/max updates), then:
#         #   dfs(root, 0, 0)
#         #   min_col = min(map.keys())  # Extract min from keys after DFS - O(k)
#         #   max_col = max(map.keys())  # Extract max from keys after DFS - O(k)
#         # where k = number of unique columns (k ≤ n, typically k ≈ log n for balanced trees)
#         # This adds O(k) extra pass but avoids nonlocal. Both are O(n) overall.
        
#         # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         # BUILD RESULT
#         # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#         # CRITICAL: We use range() to iterate in SORTED ORDER, not dict order!
#         # 
#         # Dictionary maintains INSERTION order, NOT numerical order:
#         #   If map keys were inserted as [0, -1, 1], iterating gives [0, -1, 1]
#         #   This would produce WRONG result: [1, 2, 3] instead of [2, 1, 3]
#         # 
#         # Using range(min_col, max_col + 1) gives SORTED order:
#         #   range(-1, 2) = [-1, 0, 1] → correct left-to-right order
#         # 
#         # Example from tree above:
#         #   map insertion order: {0: (1,0), -1: (2,1), 1: (3,1)}
#         #   for col in map         → 0, -1, 1  → [1, 2, 3] ✗ WRONG
#         #   for col in range(-1,2) → -1, 0, 1  → [2, 1, 3] ✓ CORRECT
#         # 
#         # This is why we track min_col and max_col during DFS!

#         result = []
#         for column in range(min_col, max_col + 1):
#             result.append(col_map[column][0].val)
        
#         return result

# Approach : BFS

# class Solution:
#     def topView(self, root: Optional[TreeNode]) -> List[int]:
#         """
#         BFS solution for top view of binary tree.
        
#         Approach:
#         - Use BFS (level-order traversal) with horizontal distance tracking
#         - Queue stores (node, column) pairs
#         - For each column, keep only the FIRST node encountered (topmost)
#         - BFS naturally processes top-to-bottom, so first seen = topmost
        
#         Key Insight:
#         BFS processes nodes level by level from top to bottom.
#         The first time we see a column, that node is the topmost at that column.

#         DFS doesn't visit nodes level-by-level (top-to-bottom). It explores
#         depth-first, so a deeper node might be visited before a shallower node
#         in the same column. We need row to determine which is closer to the top.

#         BFS doesn't need row tracking because it naturally visits nodes
#         level-by-level (row 0, then row 1, then row 2...).

#         Time Complexity: O(n)
#         - Each node is processed exactly once in BFS
#         - Hash map operations (lookup, insert) are O(1)
#         - Final result construction takes O(k), where k ≤ n
#         - Total: O(n + k) = O(n)

#         Space Complexity: O(w + k)
#         - w = maximum width of the tree (queue size)
#         - k = number of unique columns (hash map size)

#         Worst case:
#         - w = O(n), k = O(n) → O(n)

#         More precisely:
#         - Balanced tree: w = O(n), k = O(log n) → O(n)
#         - Skewed tree: w = O(1), k = O(n) → O(n)

#         Note:
#         - For balanced trees, BFS uses O(n) space due to large queue width.
#         - A DFS approach can use O(h + k) space:
#         - Balanced tree: O(log n + log n) = O(log n)
#         - Skewed tree: O(n + n) = O(n)
#         - Thus, DFS is more space-efficient for balanced trees, but both have O(n) worst-case    space.

#         """
#         # Edge case: empty tree
#         if not root:
#             return []
        
#         # Map: column -> node_value (first seen at this column)
#         column_map = {}
        
#         # Queue: (node, column)
#         # Start with root at column 0
#         queue = deque([(root, 0)])
        
#         # Track min and max columns for result building
#         min_col = max_col = 0
        
#         # BFS traversal
#         while queue:
#             node, col = queue.popleft()
            
#             # Update column range
#             min_col = min(min_col, col)
#             max_col = max(max_col, col)
            
#             # KEY: Only store if this column hasn't been seen before
#             # First node encountered at each column = topmost node
#             if col not in column_map:
#                 column_map[col] = node.val
            
#             # For bottom view KEY DIFFERENCE: ALWAYS update (no "if col not in" check)
#             # This ensures we keep the LAST (bottommost) node at each column
#             # column_map[col] = node.val
            
#             # Add children to queue with updated columns
#             if node.left:
#                 queue.append((node.left, col - 1))
#             if node.right:
#                 queue.append((node.right, col + 1))
        
#         # Build result from leftmost to rightmost column
#         result = []
#         for col in range(min_col, max_col + 1):
#             result.append(column_map[col])
        
#         return result