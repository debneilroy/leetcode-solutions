"""
LeetCode 987. Vertical Order Traversal of a Binary Tree
Difficulty: Hard
URL: https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/
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

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


# Approach : Brute Force

class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Brute force vertical order traversal using BFS.
        
        Strategy:
        1. Use BFS to collect ALL nodes with their (col, row, val) coordinates
        2. Sort the entire list by (col, row, val) - all at once
        3. Group consecutive nodes by column to build result
        
        This is the "naive" approach - sorting all nodes together instead of
        sorting within each column separately.
        
        Time Complexity: O(N log N)
            - BFS traversal: O(N)
            - Sort all N nodes: O(N log N) - sorting dominates
            - Group by column: O(N)
            - Overall: O(N log N)
            
            Why worse than optimized O(N log(N/k))?
            - We sort ALL N nodes together in one large group
            - Optimized approach sorts k separate smaller groups
            - When k is large (many columns), separate sorting is faster
            
        Space Complexity: O(N)
            - BFS queue: O(W) where W is max width, worst case O(N)
            - nodes list: O(N)
            - Result: O(N)
        """
        # Base case: empty tree
        if root is None:
            return []
        
        # Store all nodes as (col, row, val) tuples
        # We put col first so natural sorting groups by column automatically
        nodes = []
        
        # BFS queue: stores (node, row, col) tuples
        queue = deque([(root, 0, 0)])
        
        # BFS traversal: visit all nodes level by level
        while queue:
            node, row, col = queue.popleft()
            
            # Store (col, row, val) - column first for grouping
            # Python will sort by col first, then row, then val
            nodes.append((col, row, node.val))
            
            # Add left child: row+1, col-1
            if node.left:
                queue.append((node.left, row + 1, col - 1))
            
            # Add right child: row+1, col+1
            if node.right:
                queue.append((node.right, row + 1, col + 1))
        
        # BRUTE FORCE: Sort ALL nodes at once by (col, row, val)
        # This is O(N log N) - sorting the entire list together
        #
        # Example for tree [1,2,3,4,6,5,7]:
        #
        # Tree structure:
        #       1           (row=0, col=0)
        #      / \
        #     2   3         (row=1, col=-1), (row=1, col=1)
        #    / \ / \
        #   4  6 5  7       (row=2, col=-2), (row=2, col=0), (row=2, col=0), (row=2, col=2)
        #
        # Before sort (BFS collection order):
        # [(0,0,1), (-1,1,2), (1,1,3), (-2,2,4), (0,2,6), (0,2,5), (2,2,7)]
        #
        # After sort (by col, then row, then val):
        # [(-2,2,4), (-1,1,2), (0,0,1), (0,2,5), (0,2,6), (1,1,3), (2,2,7)]
        #   col=-2    col=-1    col=0    col=0    col=0    col=1    col=2
        #   row=2     row=1     row=0    row=2    row=2    row=1    row=2
        #   val=4     val=2     val=1    val=5    val=6    val=3    val=7
        #
        # Note: At (col=0, row=2), nodes 5 and 6 are at same position
        #       After sorting: 5 comes before 6 because 5 < 6 ✓
        nodes.sort()
        
        # Group consecutive nodes by column
        # Since nodes are sorted by column, same-column nodes are adjacent
        result = []
        
        # Track the previous column to detect when column changes
        prev_col = float('-inf')  # Initialize to impossible value
        
        for col, row, val in nodes:
            # If this is a new column, start a new list
            if col != prev_col:
                result.append([])  # Add new empty list for this column
                prev_col = col
            
            # Add value to the current column's list
            # We just append because nodes are already sorted
            result[-1].append(val)
        
        return result

# Approach : BFS

class Solution:
    def verticalTraversal(self, root):
        """
        Vertical order traversal of binary tree.
        
        Strategy:
        1. Use BFS to traverse tree and assign (row, col) coordinates to each node
        2. Group nodes by column using hashmap
        3. Sort within each column by (row, value)
        4. Build result by processing columns left-to-right
        
        Coordinate system:
        - Root starts at (row=0, col=0)
        - Left child: row+1, col-1 (go down, go left)
        - Right child: row+1, col+1 (go down, go right)

        Why is sorting required?
        Example where multiple nodes share the same (row, col) position:

        Tree:

           1
          / \
         2   3
        / \ / \
       4  6 5  7
        
        Coordinates:
        - Node 1: (row=0, col=0)
        - Node 2: (row=1, col=-1)
        - Node 3: (row=1, col=1)
        - Node 4: (row=2, col=-2)
        - Node 5: (row=2, col=0)  ← Same position!
        - Node 6: (row=2, col=0)  ← Same position!
        - Node 7: (row=2, col=2)
        
        Without sorting:
        - Column 0 might have: [1, 6, 5] (BFS encounter order)
        - This is WRONG! Nodes at same position must be sorted by value
        
        With sorting by (row, val):
        - Column 0: [(0,1), (2,5), (2,6)]
        - After sort: [(0,1), (2,5), (2,6)]  (5 before 6 because 5 < 6)
        - Result: [1, 5, 6] ✓ CORRECT!
        
        The problem requires nodes at same (row, col) to be sorted by value.
        This is why we must sort each column - BFS order alone isn't enough.
        
        Time Complexity: O(N log(N/k))
            Where N = total number of nodes, k = number of unique columns
            
            Breakdown:
            - BFS traversal: O(N) - visit each node exactly once
            - Updating min/max columns: O(1) per node, O(N) total
            - Sorting within columns: O(Σ n_i log n_i) for i=1 to k
              where n_i = number of nodes in column i, and Σn_i = N
              
            Why O(N log(N/k))?
            - When nodes are evenly distributed across k columns
            - Each column has approximately N/k nodes
            - Sorting each column: O((N/k) log(N/k))
            - Total for k columns: k * O((N/k) log(N/k)) = O(N log(N/k))

            Special cases:
            - Worst case: Θ(N) nodes in one column → O(N log N)
            - Best case: 1 node per column → O(N)
            - If nodes are evenly distributed across k columns:
                → O(N log(N/k))  (as noted in LeetCode editorial)
 
            Why better than naive O(N log N)?
            - Naive approach: sort all N nodes together by (col, row, val)
            - Our approach: sort k separate groups independently
            - Sorting smaller groups is more efficient when k is large
            
        Space Complexity: O(N)
            Breakdown:
            - Queue (BFS): O(W) where W = maximum width of tree
              * Complete binary tree: W ≈ N/2 at the last level
              * Worst case: O(N)
            - HashMap (col_map): O(N) - stores all N nodes as (row, val) tuples
            - Result list: O(N) - contains all N node values
            - min_col, max_col: O(1) - just two integers
            
            Overall: O(W) + O(N) + O(N) = O(N)
            
            Note: We don't count the input tree structure in space complexity
        """
        # Base case: empty tree
        if root is None:
            return []
        
        # HashMap: column_index -> list of (row, value) tuples
        # We group by column first to achieve O(N log(N/k)) sorting complexity
        # Storing (row, val) allows us to sort within each column independently
        col_map = defaultdict(list)
        
        # BFS queue stores: (node, row_index, col_index)
        # Start with root at origin (0, 0)
        queue = deque([(root, 0, 0)])
        
        # Track the leftmost and rightmost columns seen
        # This lets us iterate columns in order without sorting keys (saves O(k log k))
        min_col = max_col = 0
        
        # BFS traversal: visit each node and record its coordinates
        while queue:
            node, row, col = queue.popleft()
            
            # Update column boundaries as we discover new columns
            min_col = min(min_col, col)
            max_col = max(max_col, col)

            # if col < min_col:
            #     min_col = col
            # elif col > max_col:
            #     max_col = col
            
            # Store as (row, val) tuple in this column's list
            # 
            # Why (row, val) order?
            # Python sorts tuples lexicographically: compares element-by-element left-to-right
            # (row, val) means: sort by row first, then by value if rows are equal
            # Example: [(2,6), (0,3), (2,5)] sorts to [(0,3), (2,5), (2,6)]
            #          - (0,3) first (row 0 < row 2)
            #          - (2,5) before (2,6) (same row, but 5 < 6)
            #
            # If we stored (val, row) instead:
            # - Would need: col_map[col].append((node.val, row))
            # - Natural sorting would be WRONG: sorts by value first, then row
            # - Example: [(15,0), (5,2), (6,2)] sorts to [(5,2), (6,2), (15,0)]
            #   Row 0 should come first, but 5 < 15 so wrong order!
            # - Would require lambda: items.sort(key=lambda x: (x[1], x[0]))
            #   This swaps comparison order to (row, val)
            # - Extraction would be: [val for val, row in items]

            # defaultdict auto-creates empty list for new keys when accessed
            # This allows us to append directly without checking if key exists
            # 
            # With regular dict, we would need to check first:
            # if col not in col_map:
            #     col_map[col] = []
            # col_map[col].append((row, node.val))
            #
            # Or use setdefault: col_map.setdefault(col, []).append((row, node.val))
            
            col_map[col].append((row, node.val))
            
            # Process left child
            # Goes one level deeper (row+1) and one column left (col-1)
            if node.left:
                queue.append((node.left, row+1, col-1))
            
            # Process right child
            # Goes one level deeper (row+1) and one column right (col+1)
            if node.right:
                queue.append((node.right, row+1, col+1))

        print(col_map) # looks like {0: [(0, 3), (2, 15)], -1: [(1, 9)], 1: [(1, 20)], 2: [(2, 7)]})
        
        # Build final result by processing columns from left to right
        result = []
        
        for col in range(min_col, max_col+1):
            # Get all (row, val) tuples for this column
            items = col_map[col]
            
            # Sort by (row, value) - Python's natural tuple comparison does this automatically
            # Lexicographic ordering: compares first element, then second if first is equal
            # Example: [(0,3), (2,5), (2,6)] -> already sorted correctly
            
            # If we stored (val, row) instead:
            # - Would need: items.sort(key=lambda x: (x[1], x[0]))
            # - Lambda creates new comparison key by swapping indices
            # - (val, row) becomes (row, val) for comparison purposes
            #
            # Example where natural sort fails with (val, row):
            # items = [(15, 0), (5, 2), (6, 2)]
            #          val row  val row  val row
            #
            # Natural sort (WRONG):
            # items.sort() → [(5, 2), (6, 2), (15, 0)]
            # Sorted by value first: 5 < 6 < 15
            # But rows are: 2, 2, 0 ✗ (row 0 should come first!)
            #
            # With lambda (CORRECT):
            # items.sort(key=lambda x: (x[1], x[0]))
            # Creates keys: (0,15), (2,5), (2,6)
            # Sorted by row first: 0 < 2 < 2, then by value: 5 < 6
            # Result: [(15, 0), (5, 2), (6, 2)] ✓

            items.sort() # sort in place, O(1) space complexity
            
            # Extract just the values (discard row information after sorting)
            # List comprehension: iterate through sorted tuples, keep only values
            #
            # If we had stored (val, row):
            # - Would need: [val for val, row in items]
            # - Because val would be at index 0, row at index 1
            result.append([val for row, val in items])

            # Alternative without list comprehension:
            # column_values = []
            # for row, val in items:
            #     column_values.append(val)
            # result.append(column_values)
            #
            # Note: Do NOT use result.append([val]) inside the loop!
            # That creates [[9], [3], [15], [20], [7]] (separate list per value)
            # We need [[9], [3, 15], [20], [7]] (one list per column)
        
        return result

# Special cases:
# - Worst case: O(N log N)
#   When Θ(N) nodes fall into a single column
#   Example (zig-zag pattern, N=7):
#       1        (col=0)
#        \
#         2      (col=1)
#        /
#       3        (col=0)
#        \
#         4      (col=1)
#        /
#       5        (col=0)
#        \
#         6      (col=1)
#        /
#       7        (col=0)

#   Column distribution:
#   - col=0 → [1, 3, 5, 7] → 4 nodes (dominates)
#   - col=1 → [2, 4, 6] → 3 nodes
#   Sorting largest column dominates → total time is O(N log N)
  
# - Best case: O(N)
#   When each column has at most one node
#   Example (left-skewed tree, N=5):
#       1       (col=0)
#      /
#     2         (col=-1)
#    /
#   3           (col=-2)
#  /
# 4             (col=-3)
# /
# 5             (col=-4)

#   Column distribution:
#   - Each of 5 columns has exactly 1 node
#   Sorting cost: 5 × O(1 log 1) = O(N)
  
# - Average/Typical case (balanced tree): O(N log N)
#   Example (complete binary tree, N=7):
#        1           (col=0)
#       / \
#      2   3         (col=-1, col=1)
#     / \ / \
#    4  5 6  7       (col=-2, col=0, col=0, col=2)

#   Column distribution:
#   - col=-2 → [4]      (1 node)
#   - col=-1 → [2]      (1 node)
#   - col=0  → [1,5,6]  (3 nodes, largest)
#   - col=1  → [3]      (1 node)
#   - col=2  → [7]      (1 node)

#   Observations:
#   - Number of columns: k = Θ(log N)
#     (Θ means a tight bound — grows on the order of log N)
#   - Largest column has Θ(N / √log N) nodes, not Θ(N)
#     (grows on the order of N/√log N)
#   - Distribution is uneven but no single column fully dominates
#   Overall sorting cost: O(N log N)

# Note on notation:
# - O(f(N)) = upper bound (runtime grows at most proportional to f(N))
# - Θ(f(N)) = tight bound (runtime grows on the order of f(N))
# - Ω(f(N)) = lower bound (runtime grows at least proportional to f(N))

# Approach : DFS

# class Solution:
#     def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
#         """
#         Vertical order traversal of binary tree using DFS.
        
#         Strategy:
#         1. Use DFS to traverse tree and assign (row, col) coordinates to each node
#         2. Group nodes by column using hashmap
#         3. Sort within each column by (row, value)
#         4. Build result by processing columns left-to-right
        
#         Coordinate system:
#         - Root starts at (row=0, col=0)
#         - Left child: row+1, col-1 (go down, go left)
#         - Right child: row+1, col+1 (go down, go right)
        
#         Time Complexity: O(N log(N/k))
#             Where N = total number of nodes, k = number of unique columns
#             - DFS traversal: O(N)
#             - Sorting within columns: O(N log(N/k))
            
#         Space Complexity: O(N)
#             - Recursion stack: O(H) where H = height, worst case O(N)
#             - HashMap: O(N)
#             - Result: O(N)
#         """
#         # Base case: empty tree
#         if root is None:
#             return []
        
#         # HashMap: column_index -> list of (row, value) tuples
#         # defaultdict auto-creates empty list for new keys when accessed
#         # With regular dict: need "if col not in col_map: col_map[col] = []" first
#         col_map = defaultdict(list)
        
#         # Track the leftmost and rightmost columns seen
#         # Using nonlocal keyword to modify these variables in nested function
#         # 
#         # Alternative approach using instance variables:
#         # self.min_col = 0
#         # self.max_col = 0
#         # Then access with self.min_col and self.max_col in dfs()
#         min_col = 0
#         max_col = 0
        
#         def dfs(node, row, col):
#             """
#             Recursively traverse tree and record node coordinates.
            
#             Args:
#                 node: Current tree node
#                 row: Current row (depth level, 0 at root)
#                 col: Current column (horizontal position, 0 at root)
#             """
#             # nonlocal declares we want to modify outer scope variables
#             # Without this: UnboundLocalError (Python thinks min_col is local variable)
#             # Alternative: use instance variables (self.min_col, self.max_col)
#             nonlocal min_col, max_col
            
#             # Base case: reached null node
#             if not node:
#                 return
            
#             # Update column boundaries
#             # These modify the outer scope variables (enabled by nonlocal)
#             min_col = min(min_col, col)
#             max_col = max(max_col, col)
            
#             col_map[col].append((row, node.val))
            
#             # Recurse on left subtree
#             # Go one level deeper (row+1) and one column left (col-1)
#             dfs(node.left, row + 1, col - 1)
            
#             # Recurse on right subtree
#             # Go one level deeper (row+1) and one column right (col+1)
#             dfs(node.right, row + 1, col + 1)
        
#         # Start DFS from root at position (0, 0)
#         dfs(root, 0, 0)
        
#         # Build final result by processing columns from left to right
#         result = []
        
#         for col in range(min_col, max_col + 1):
#             items = col_map[col]
#             items.sort()
#             result.append([val for row, val in items])
        
#         return result

# Variant 1 : Print the vertical order traversal of the binary tree, separating each column by a new line. Clarify the formatting with interviewer.

# Tree:
#       3
#      / \
#     9  20
#       /  \
#      15   7

# Vertical Traversal:
# 9 
# 3 15 
# 20 
# 7 

# Print each column on a new line

# for col in range(min_col, max_col + 1):
#     # Get all (row, val) tuples for this column
#     items = col_map[col]
            
#     # Sort by (row, val) - natural tuple ordering
#     items.sort()

#     Print all values in this column, space-separated
#     end=' ' keeps values on same line with space separator
#     Example: for items = [(0,3), (2,15)]
#     With end=' ': prints "3 15 " (on same line)
#     Without end:  prints "3\n15\n" (each on separate line)
#     for row, val in items:
#         print(val, end=' ')
            
#     # Newline after each column (REQUIRED to separate columns)
#     print()

# As list comprehension + join

# Print each column on a new line
# for col in range(min_col, max_col + 1):
#     items = col_map[col]
#     items.sort() 
#     # Extract values, convert to strings, and join with spaces
#     # str(val) needed because .join() requires strings, not integers
#     print(' '.join(str(val) for row, val in items))

# Print each column as a list on a new line
# for col in range(min_col, max_col + 1):
#     items = col_map[col]
#     items.sort()
    
#     # Extract values into a list
#     values = [val for row, val in items]
    
#     # Print the list
#     print(values)

# Output:

# [9]
# [3, 15]
# [20]
# [7]


# Variant : Return traversal as a single 1D list (check Leetcode 314 Binary Tree Vertical Order Traversal)

# result = []
# for col in range(min_col, max_col + 1):
#     items = col_map[col]
#     items.sort() # Sort by (row, val)
            
#     # Add all values from this column to result
#     for row, val in items:
#         result.append(val)

# return result



