"""
LeetCode 314. Binary Tree Vertical Order Traversal
Difficulty: Medium
URL: https://leetcode.com/problems/binary-tree-vertical-order-traversal/
"""

# LC 314 vs LC 987 - Key Difference

# The only difference: What to do when multiple nodes are at the same (row, col) position.

# Example Where They Differ

# Tree:
#       1
#      / \
#     2   3
#    / \ / \
#   4  6 5  7

# Column 0 has three nodes:
# - Node 1 at row 0
# - Node 5 at row 2  ← Same position
# - Node 6 at row 2  ← Same position

# LC 314: Nodes at same position follow BFS encounter order

# Output: [[4], [2], [1, 6, 5], [3], [7]]
# #                     ↑  ↑
# # 6 before 5 (left child processed before right)

# LC 987: Nodes at same position sorted by value

# Output: [[4], [2], [1, 5, 6], [3], [7]]
# #                     ↑  ↑
# # 5 before 6 (5 < 6)

# Algorithm Difference

# LC 314:

# # Store only values (no row tracking)
# col_map[col].append(node.val)

# # No sorting - BFS order is enough
# result.append(col_map[col])

# LC 987:

# # Store (row, val) tuples
# col_map[col].append((row, node.val))

# # Must sort by (row, val)
# col_map[col].sort()
# result.append([val for row, val in col_map[col]])

# Complexity

# Problem     Time                      Why
# LC 314      O(N)                      No sorting
# LC 987      O(N log(N/k))             Sort within columns

# Bottom line: LC 987 requires sorting by value when nodes share the same position. LC 314 just uses BFS order. 


# Before starting to code, clarify these points with the interviewer:

# 1. Input? Pointer to root node
#    - What if the tree is empty? Return empty list []

# 2. Null root node? 
#    - Should we return [] or None? Return []

# 3. Output? 
#    - Return list of lists (nested) OR print it out?
#    - If print: each column on separate line OR all on one line?

# 4. Duplicates? 
#    - Can nodes have duplicate values? Yes, handle them

# 5. Value of nodes? 
#    - Are node values integers? Yes
#    - Any constraints on value range? Assume standard int range

# 6. Implement Node class? 
#    - Is TreeNode class provided? Yes, use provided definition

# 7. Follow-up variations?
#    - LC 314: top-to-bottom, left-to-right order
#    - LC 987: top-to-bottom, sorted by value at same position
#    - Which one should we solve? (Clarify requirements)

# 8. Approach preference?
#    - BFS or DFS? BFS is cleaner for LC 314 (O(N) vs O(N log N))
#    - Should we optimize for time or simplicity?


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# Approach : BFS without sorting

class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        LC 314 - Binary Tree Vertical Order Traversal
        
        Key difference from LC 987:
        - LC 314: Only needs top-to-bottom order (BFS naturally provides this)
        - LC 987: Needs sorting by value when nodes at same (row, col)
        
        Strategy:
        - Use BFS to traverse level by level (top to bottom)
        - Group nodes by column
        - BFS encounter order = correct output order (no sorting needed!)
        
        Time Complexity: O(N)
            Breakdown:
            - BFS traversal: O(N) - visit each node exactly once
            - Appending to columnTable: O(1) per node, O(N) total
            - Updating min/max column: O(1) per node, O(N) total
            - Building result: O(N) - iterate through all nodes once
            - NO SORTING needed (unlike LC 987)
            
            Overall: O(N) ✓
            
            Why O(N) vs LC 987's O(N log(N/k))?
            - LC 314: BFS order is sufficient (top-to-bottom guaranteed)
            - LC 987: Must sort nodes at same position by value
            
        Space Complexity: O(N)
            Breakdown:
            - Queue (BFS): O(W) where W = maximum width of tree
              * Complete binary tree: W ≈ N/2 at the last level
              * Worst case: O(N)
            - columnTable (HashMap): O(N) - stores all N node values
            - Result list: O(N) - contains all N node values
            - min_column, max_column: O(1) - two integers
            
            Overall: O(W) + O(N) + O(N) + O(1) = O(N)
            
            Note: We don't count the input tree structure in space complexity
        """
        # Base case: empty tree
        if root is None:
            return []

        # HashMap: column_index -> list of node values
        # defaultdict auto-creates empty list for new keys
        # With regular dict: need "if column not in columnTable: columnTable[column] = []"
        columnTable = defaultdict(list)
        
        # Track column boundaries to iterate in order
        min_column = max_column = 0
        
        # BFS queue: (node, column)
        # No need to track row - BFS naturally processes top-to-bottom
        queue = deque([(root, 0)])

        # BFS traversal - processes nodes level by level
        while queue:
            node, column = queue.popleft()

            # Append value directly - no (row, val) tuple needed
            # BFS guarantees top-to-bottom order automatically
            columnTable[column].append(node.val)
                
            # Update column boundaries
            min_column = min(min_column, column)
            max_column = max(max_column, column)

            # Add children to queue
            # Left child: column - 1
            if node.left:
                queue.append((node.left, column - 1))

            # Right child: column + 1
            if node.right:
                queue.append((node.right, column + 1))

        # Build result - no sorting needed!
        # Iterate columns left to right using range
        return [columnTable[x] for x in range(min_column, max_column + 1)]

        # ====================================================================
        # FOLLOW-UP: Print nodes from top down, left right
        # ====================================================================
        # Interviewer might ask: "Instead of returning a list, can you print 
        # the nodes in order from top to bottom, left to right?"
        #
        # Problem: Figure out the order of nodes from top down, left right.
        #
        # Example:
        #          4
        #        /   \
        #       2     6
        #      / \   / \
        #     1   5 3   7
        #
        # Order is 1, 2, 4, 5, 3, 6, 7
        #
        # This is asking for vertical order traversal output but PRINTED
        # instead of returned as a nested list.
        # ====================================================================
        
        # ====================================================================
        # ALTERNATIVE 1: Print each column on a SEPARATE LINE
        # ====================================================================
        # Print values column by column with newlines separating columns
        # for col in range(min_column, max_column + 1):
        #     # Print all values in this column, space-separated
        #     # end=' ' keeps values on same line with space separator
        #     # Example: if column has [3, 15], prints "3 15 "
        #     for val in columnTable[col]:
        #         print(val, end=' ')
        #     
        #     # Newline after each column (moves to next line for next column)
        #     # This line is CRITICAL for separating columns vertically
        #     # Without this, all columns would be on one line
        #     print()
        #
        # Pros: Clear visual separation, each column on own line
        # Cons: Can't return result, only prints
        # Space: O(1) for printing (no string storage)
        #
        # Output example for tree [3,9,20,null,null,15,7]:
        # 9 
        # 3 15 
        # 20 
        # 7 
        # 
        # ↑ Each line represents one column
        
        # ====================================================================
        # ALTERNATIVE 2: Print ALL columns on a SINGLE LINE (streaming)
        # ====================================================================
        # Print values as they're encountered - no string storage
        # All columns concatenated on one line
        # for col in range(min_column, max_column + 1):
        #     for val in columnTable[col]:
        #         print(val, end=' ')  # Prints immediately, stays on same line
        #     # NO print() here - this is the key difference from Alternative 1
        #     # Without newline, next column continues on same line
        # print()  # Optional: single newline at the very end
        #
        # Pros: O(1) space, immediate output, compact single-line format
        # Cons: Can't return result, no visual column separation
        # Space: O(1) for printing (no string storage)
        #
        # Output example for tree [3,9,20,null,null,15,7]:
        # 9 3 15 20 7 
        # ↑ All columns on one line
        #
        # This matches the problem statement: "Order is 1, 2, 4, 5, 3, 6, 7"

        # ====================================================================
        # ALTERNATIVE 3: Build string THEN print (buffered)
        # ====================================================================
        # Accumulate all values in a string first, then print/return
        # All columns concatenated on one line (same visual as Alternative 2)
        # res = ''
        # for col in range(min_column, max_column + 1):
        #     for val in columnTable[col]:
        #         res += str(val) + ' '  # Builds string in memory
        #         # Note: str(val) needed because can't concatenate int to string
        # print(res)   # Print the complete result
        # return res   # Can also return as string for further processing
        #
        # Pros: Can return result as string, can modify before printing
        # Cons: O(N) extra space for string storage, output delayed until loop completes
        # Space: O(N) for string accumulation
        #
        # Output example for tree [3,9,20,null,null,15,7]:
        # 9 3 15 20 7 
        # ↑ All columns on one line (same as Alternative 2)
        #
        # Key difference from Alternative 2:
        # - Alternative 2: Prints immediately (streaming)
        # - Alternative 3: Stores in string first (buffered), can return



# Approach : BFS

# class Solution:
#     def verticalOrder(self, root: TreeNode) -> List[List[int]]:
#         columnTable = defaultdict(list)
#         queue = deque([(root, 0)])

#         while queue:
#             node, column = queue.popleft()

#             if node is not None:
#                 columnTable[column].append(node.val)
                
#                 queue.append((node.left, column - 1))
#                 queue.append((node.right, column + 1))
                        
#         return [columnTable[x] for x in sorted(columnTable.keys())]

# TC : O(N log N), SC : O(N), where N is the number of nodes in the tree 


# Approach : DFS

class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        LC 314 - Binary Tree Vertical Order Traversal using DFS
        
        Strategy:
        1. Use DFS pre-order to collect nodes with (row, val) coordinates
        2. Sort by row ONLY (not by value) using stable sort
        3. Extract values after sorting
        
        Why DFS works for LC 314:
        
            LC 314 requires nodes at same (row, col) to be in left-to-right order.
            
            Key insight: DFS pre-order + stable sort achieves this!
            
            1. DFS Pre-order (node → left → right):
               - Visits left subtree completely before right subtree
               - Within each column, left nodes are encountered and inserted first
               - Then right nodes are encountered and inserted later
               
            2. Stable Sort by row only:
               - Python's sort is stable: equal elements maintain original order
               - We sort by row only (not by value): key=lambda x: x[0]
               - Nodes at same row stay in insertion order (left before right)
               
            3. Result:
               - Top-to-bottom: ensured by sorting by row
               - Left-to-right: ensured by stable sort preserving DFS insertion order
            
            Example:
                Tree:      1 (col=0, row=0)
                          / \
                         2   3 (col=-1, row=1), (col=1, row=1)
                        /\   /\
                       4 10 9 11 (col=-2,row=2), (col=0,row=2), (col=0,row=2), (col=2,row=2)
                        \
                         5 (col=-1, row=3)
                          \
                           6 (col=0, row=4)
            
            DFS pre-order visits: 1 → 2 → 4 → 5 → 6 → 10 → 3 → 9 → 11
            
            Column 0 collection during DFS:
            - Visit 1 (row=0): col_map[0] = [(0, 1)]
            - Visit 10 (row=2): col_map[0] = [(0, 1), (2, 10)]  ← left child inserted
            - Visit 9 (row=2): col_map[0] = [(0, 1), (2, 10), (2, 9)]  ← right child inserted after
            - Visit 6 (row=4): col_map[0] = [(0, 1), (2, 10), (2, 9), (4, 6)]
            
            After sorting by row only (stable sort):
            - (0, 1): row=0
            - (2, 10), (2, 9): row=2, same row → maintains insertion order (10 before 9)
            - (4, 6): row=4
            
            Result: [1, 10, 9, 6] ✓ Correct left-to-right order!
        
        Time Complexity: O(N log N)
            Breakdown:
            - DFS traversal: O(N) - visit each node once
            - Sorting within columns by row: O(Σ n_i log n_i) ≈ O(N log N)
            - Building result: O(N)
            - Overall: O(N log N)
            
            Note: BFS is O(N) because no sorting needed
            
        Space Complexity: O(N)
            - Recursion stack: O(H) where H = height, worst case O(N)
            - HashMap (col_map): O(N) - stores all nodes as (row, val) tuples
            - Result list: O(N)
            - Overall: O(N)
        """
        # Base case: empty tree
        if root is None:
            return []
        
        # HashMap: column_index -> list of (row, value) tuples
        # Store (row, val) to enable sorting by row while preserving insertion order
        col_map = defaultdict(list)
        
        # Track column boundaries to iterate left-to-right
        min_col = max_col = 0
        
        def dfs(node, row, col):
            """
            DFS pre-order traversal: node → left → right
            
            This order is crucial:
            - Processing left before right ensures left nodes are inserted first
            - When nodes at same (row, col), left is inserted before right
            - Stable sort will preserve this left-to-right order
            
            Args:
                node: Current tree node
                row: Current row (depth level, 0 at root)
                col: Current column (horizontal position, 0 at root)
            """
            if node is not None:
                # nonlocal allows modifying outer scope variables
                nonlocal min_col, max_col
                
                # Store (row, val) tuple for this column
                # We need row to sort top-to-bottom later
                # Order of insertion matters: DFS pre-order gives left-to-right
                col_map[col].append((row, node.val))
                
                # Update column boundaries
                min_col = min(min_col, col)
                max_col = max(max_col, col)
                
                # Pre-order DFS: process left subtree first, then right
                # Left child: row+1 (deeper), col-1 (left)
                dfs(node.left, row + 1, col - 1)
                
                # Right child: row+1 (deeper), col+1 (right)
                dfs(node.right, row + 1, col + 1)
        
        # Start DFS from root at position (row=0, col=0)
        dfs(root, 0, 0)
        
        # Build result by processing columns from left to right
        result = []
        
        # Iterate through all columns in order
        for col in range(min_col, max_col + 1):
            # Get all (row, val) tuples for this column
            items = col_map[col]
            
            # CRITICAL: Sort by row ONLY, not by (row, val)
            # key=lambda x: x[0] extracts only the row (first element of tuple)
            # 
            # Why not sort by both row and value?
            # - LC 314 requires left-to-right order for same-row nodes, NOT sorted by value
            # - Sorting by value would give: [1, 9, 10, 6] (9 < 10) ✗ WRONG
            # - Sorting by row only preserves insertion order: [1, 10, 9, 6] ✓ CORRECT
            # 
            # Python's sort is STABLE:
            # - When sort keys are equal (same row), original order is preserved
            # - DFS inserted 10 before 9 (left child before right child)
            # - Stable sort keeps 10 before 9
            # 
            # Example: [(0,1), (2,10), (2,9), (4,6)]
            # Sort keys: [0, 2, 2, 4]
            # After sort: [(0,1), (2,10), (2,9), (4,6)]  ← 10 stays before 9!
            items.sort(key=lambda x: x[0])
            
            # Extract just the values (discard row information after sorting)
            # List comprehension: iterate through sorted tuples, keep only values
            col_vals = [val for row, val in items]
            
            # Add this column's values to result
            result.append(col_vals)
        
        return result

        # ====================================================================
        # FOLLOW-UP: Print nodes from top down, left right
        # ====================================================================
        # Interviewer might ask: "Instead of returning a list, can you print 
        # the nodes in order from top to bottom, left to right?"
        #
        # Problem: Figure out the order of nodes from top down, left right.
        #
        # Example:
        #          4
        #        /   \
        #       2     6
        #      / \   / \
        #     1   5 3   7
        #
        # Order is 1, 2, 4, 5, 3, 6, 7
        #
        # This is asking for vertical order traversal output but PRINTED
        # instead of returned as a nested list.
        # ====================================================================

        # ====================================================================
        # ALTERNATIVE 1: Print each column on a SEPARATE LINE
        # ====================================================================
        # Print values column by column with newlines separating columns
        # for col in range(min_col, max_col + 1):
        #     items = col_map[col]
        #     items.sort(key=lambda x: x[0])  # Sort by row only
        #     
        #     # Print all values in this column, space-separated
        #     for row, val in items:
        #         print(val, end=' ')
        #     
        #     # Newline after each column
        #     print()
        #
        # Pros: Clear visual separation, each column on own line
        # Cons: Can't return result, only prints
        # Space: O(1) for printing (no string storage)
        #
        # Output example for tree from problem statement:
        #          4
        #        /   \
        #       2     6
        #      / \   / \
        #     1   5 3   7
        #
        # 1 
        # 2 
        # 4 5 3 
        # 6 
        # 7 
        
        # ====================================================================
        # ALTERNATIVE 2: Print ALL columns on a SINGLE LINE (streaming)
        # ====================================================================
        # Print values as they're encountered - no string storage
        # for col in range(min_col, max_col + 1):
        #     items = col_map[col]
        #     items.sort(key=lambda x: x[0])  # Sort by row only
        #     
        #     for row, val in items:
        #         print(val, end=' ')  # Prints immediately
        # print()  # Optional: single newline at the very end
        #
        # Pros: O(1) space, immediate output, compact single-line format
        # Cons: Can't return result, no visual column separation
        # Space: O(1) for printing (no string storage)
        #
        # Output example for tree from problem statement:
        # 1 2 4 5 3 6 7 
        #
        # This matches the problem statement: "Order is 1, 2, 4, 5, 3, 6, 7"

        # ====================================================================
        # ALTERNATIVE 3: Build string THEN print (buffered)
        # ====================================================================
        # Accumulate all values in a string first, then print/return
        # res = ''
        # for col in range(min_col, max_col + 1):
        #     items = col_map[col]
        #     items.sort(key=lambda x: x[0])  # Sort by row only
        #     
        #     for row, val in items:
        #         res += str(val) + ' '
        # print(res)
        # return res
        #
        # Pros: Can return result as string, can modify before printing
        # Cons: O(N) extra space for string storage
        # Space: O(N) for string accumulation
        #
        # Output example for tree from problem statement:
        # 1 2 4 5 3 6 7




