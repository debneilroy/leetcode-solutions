"""
LeetCode 938. Range Sum of BST
Difficulty: Easy
URL: https://leetcode.com/problems/range-sum-of-bst/
"""

# Definition for a binary tree node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Iterative Solution / Preorder traversal with pruning (Preferable)

class Solution:
    def rangeSumBST(self, root, low, high):
        """
        Approach: Iterative DFS using stack with pruning
        
        Time Complexity: O(n) worst case, O(k) average case
        - Worst case: O(n) when range covers all nodes [min_val, max_val]
        - Average case: O(k) where k is number of nodes in range + nodes on path
        - Best case: O(log n) when range is very narrow and tree is balanced
        
        Space Complexity: O(h) where h is height of tree
        - Stack stores at most h nodes (depth of tree)
        - Balanced BST: O(log n) space
        - Skewed BST: O(n) space in worst case
        """
        # Edge case: empty tree
        if not root:
            return 0

        # Edge case: Invalid range (low > high)
        if low > high:
            return 0
        
        total = 0
        
        # Initialize stack with root node
        # Stack will hold nodes to be processed (LIFO - Last In First Out)
        stack = [root]
        
        # Continue while there are nodes to process
        while stack:
            # Pop the most recently added node (DFS behavior)
            node = stack.pop()
            
            # Check if node exists (we might have added None)
            if node:
                # STEP 1: Check if current node's value is in range [low, high]
                # If yes, add it to our running total
                if low <= node.val <= high:
                    total += node.val
                
                # STEP 2: PRUNING - Decide which children to explore
                # This is the key optimization using BST properties!
                
                # Only explore LEFT subtree if current value > low
                # Why? In a BST, all values in left subtree < current value
                # So if current value <= low, left subtree will have even smaller
                # values that are definitely < low, so we can skip it entirely
                if node.val > low:
                    stack.append(node.left)
                
                # Only explore RIGHT subtree if current value < high
                # Why? In a BST, all values in right subtree > current value
                # So if current value >= high, right subtree will have even larger
                # values that are definitely > high, so we can skip it entirely
                if node.val < high:
                    stack.append(node.right)
                
                # Note: We might add None to stack, but we check "if node:" above
        
        return total

# Build the tree: [10,5,15,3,7,null,18]

root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
root.left.left = TreeNode(3)
root.left.right = TreeNode(7)
root.right.left = None
root.right.right = TreeNode(18)

# Best Case - O(log n)

    # Balanced BST with narrow range at a leaf
    #         50
    #       /    \
    #     25      75
    #    /  \    /  \
    #   12  37  62  87
    #  / \  / \ / \ / \
    # 6 18 31 43 56 68 81 93
    #
    # Range: [80, 82] - only looking for 81
    # Nodes visited: 50 -> 75 -> 87 -> 81 (only 4 nodes!)

# Worst Case 1 - O(n)

    # Same tree but range covers ALL nodes                        
    #         50
    #       /    \
    #     25      75
    #    /  \    /  \
    #   12  37  62  87
    #  / \  / \ / \ / \
    # 6 18 31 43 56 68 81 93
    #
    # Range: [1, 100] - covers entire tree
    # Nodes visited: ALL 15 nodes


# Worst Case 2 - O(n)

    # Skewed BST (linked list structure)
    #  1
    #   \
    #    2
    #     \
    #      3
    #       \
    #        4
    #         \
    #          5
    # Range: [3, 5]
    # Even with narrow range, tree structure forces us down the chain


# 1. Using Inorder Traversal (sorted order)

# Inorder traversal of a BST gives sorted values.

# You can do a simple traversal:

class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        self.ans = 0
        def inorder(node):
            if not node:
                return
            inorder(node.left)
            if low <= node.val <= high:
                self.ans += node.val
            inorder(node.right)
        inorder(root)
        return self.ans


# ✅ Works
# ❌ Not optimal — visits every node (no pruning).
# ⏱️ Time: O(n) always
# 🧠 Good if you don’t want to reason about pruning.

# You can slightly improve it with pruning:

def inorder(node):
    if not node:
        return
    if node.val > low:   # left side might have valid nodes
        inorder(node.left)
    if low <= node.val <= high:
        self.ans += node.val
    if node.val < high:  # right side might have valid nodes
        inorder(node.right)

# Now it prunes some branches — closer to optimal.

# 🔸 2. Preorder Traversal

# Preorder = [root → left → right].
# You can use it as well, but it doesn’t give any benefit over DFS since order doesn’t matter.

# Example:

class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        self.ans = 0
        def preorder(node):
            if not node:
                return
            if low <= node.val <= high:
                self.ans += node.val
            if node.val > low:   # left may contain valid values
                preorder(node.left)
            if node.val < high:  # right may contain valid values
                preorder(node.right)
        preorder(root)
        return self.ans


# ✅ Correct
# ✅ Uses BST property for pruning
# ⚡ Same complexity as optimized DFS:

# Time ≈ O(k), where k = number of nodes visited

# Space ≈ O(h)

# 🔸 3. Postorder Traversal

# Also possible, but unnecessary:

# def postorder(node):
#     if not node:
#         return
#     if node.val > low:
#         postorder(node.left)
#     if node.val < high:
#         postorder(node.right)
#     if low <= node.val <= high:
#         self.ans += node.val

# Order doesn’t matter for sum, so no advantage.

# You can solve the problem using various tree traversals, but efficiency depends on whether you use the BST property for pruning. The simplest methods—standard inorder, preorder, or postorder—visit all nodes and check if each value lies within the range, resulting in O(n) time. More efficient are the pruned versions, which leverage the BST property: if a node’s value is less than low, skip its left subtree; if greater than high, skip its right. This yields O(k) time, where k is the number of visited nodes. Among these, preorder with pruning is the most common and intuitive, as it processes the node first, then selectively explores children. The iterative DFS approach is effectively a preorder traversal with pruning, implemented via a stack; by pushing the right child before the left, it maintains root-left-right order. In contrast, inorder with pruning preserves sorted order while pruning irrelevant branches, and postorder with pruning also works but offers no practical advantage. Overall, the recursive preorder (or iterative DFS) with pruning is the cleanest and most efficient solution.

# Recursive DFS with pruning

class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        def dfs(node):
            if node:
                if low <= node.val <= high:
                    self.total += node.val
                if node.val > low:
                    dfs(node.left)
                if node.val < high:
                    dfs(node.right)

        self.total = 0
        dfs(root)
        return self.total

# Variant 1 : Return the average

# class Solution:
#     def rangeAverageBST_iterative(self, root, low, high):
#         # Edge case: empty tree
#         if not root:
#             return 0

#         if low > high:
#             return 0
            
#         total_sum = 0
#         count = 0
            
#         # Initialize stack with root node
#         stack = [root]
            
#         while stack:
#             # Pop the most recently added node (DFS/Preorder behavior)
#             node = stack.pop()
                
#             if node:
#                 # STEP 1: Process current node (PREORDER)
#                 # Check if current node's value is in range [low, high]
#                 if low <= node.val <= high:
#                     total_sum += node.val
#                     count += 1
                    
#                 # STEP 2: Add LEFT child with pruning
#                 # Only explore left subtree if current value > low
#                 if node.val > low:
#                     stack.append(node.left)
                    
#                 # STEP 3: Add RIGHT child with pruning
#                 # Only explore right subtree if current value < high
#                 if node.val < high:
#                     stack.append(node.right)
            
#         # Handle edge case: no nodes in range
#         if count == 0:
#             return 0
            
#         return total_sum / count


# Variant 2 (Hard) : Given the root node of a binary search tree and two integers low and high, return the sum of values of all nodes with a value in the inclusive range [low, high]. Note: At most 10^4 calls will be made to rangeSumBST.

# class Solution:
#     """
#     OPTIMAL SOLUTION for calculating range sums in a BST with multiple queries.
    
#     Key Idea:
#     - Preprocess the tree ONCE in __init__ to build sorted array + prefix sums
#     - Answer each query in O(log n) time using binary search
    
#     Perfect for when calculate() is called many times (up to 10,000 times).
    
#     Example Usage:
#         root = TreeNode(10)
#         root.left = TreeNode(5)
#         root.right = TreeNode(15)
        
#         sol = Solution(root)  # Preprocessing happens here (O(n))
#         result1 = sol.calculate(7, 15)  # Fast query (O(log n))
#         result2 = sol.calculate(3, 10)  # Fast query (O(log n))
#         # ... can call calculate() 10,000 more times efficiently
#     """
    
#     def __init__(self, root):
#         """
#         Constructor: Preprocess the BST to enable fast range queries.
        
#         This is called ONCE when the Solution object is created.
#         We build two arrays that will be used for ALL future queries:
        
#         1. vals: Sorted array of all node values (via inorder traversal)
#         2. prefix_sums: Cumulative sums for O(1) range sum calculation
        
#         Time Complexity: O(n) where n = number of nodes
#         Space Complexity: O(n) to store the arrays
        
#         Args:
#             root: The root node of the BST
#         """
#         # Initialize empty arrays that will store preprocessed data
#         self.vals = []         # Will contain: [val1, val2, val3, ...] in sorted order
#         self.prefix_sums = []  # Will contain: [sum1, sum1+sum2, sum1+sum2+sum3, ...]

#         # WHY DO WE NEED prefix_sums (and not just vals)?
#         # Binary search on 'vals' only finds the BOUNDARIES (indices) of our range,
#         # it doesn't give us the SUM of values in that range.
#         # 
#         # Without prefix_sums, we'd have to loop through vals[left:right+1] and
#         # add them up manually -> O(k) time, where k = number of elements in range.
#         # This defeats the purpose of binary search for large ranges!
#         # 
#         # With prefix_sums, we get the range sum in O(1) via simple subtraction:
#         #   range_sum = prefix_sums[right_boundary] - prefix_sums[left_boundary - 1]
#         # 
#         # This is what makes each query O(log n) instead of O(n):
#         #   - Binary search (find boundaries): O(log n)
#         #   - Prefix sum lookup (calculate sum): O(1)

#         # EDGE CASE: Empty tree (root is None)
#         # If root is None, vals and prefix_sums remain empty []
#         # This is handled gracefully - calculate() will return 0 for empty arrays
#         # We don't need explicit check here, but could add:
#         if not root:
#             return  # Early exit, arrays stay empty
        
#         # Perform inorder traversal to populate both arrays
#         # After this call, vals and prefix_sums will be fully built
#         self.inorder(root)
    
#     def inorder(self, root):
#         """
#         Perform inorder traversal to build sorted values array and prefix sums.
        
#         Inorder traversal of BST visits nodes in SORTED order:
#         LEFT → ROOT → RIGHT
        
#         This gives us values in ascending order, which is perfect for binary search.
        
#         Example:
#             Tree:    5
#                     / \
#                    3   7
#                   /
#                  1
            
#             Traversal order: 1 → 3 → 5 → 7
#             Result: vals = [1, 3, 5, 7]
#                     prefix_sums = [1, 4, 9, 16]
        
#         Time: O(n) - visit each node once
#         Space: O(h) for recursion stack where h = height
        
#         Args:
#             root: Current node being processed
#         """
#         # BASE CASE: If node is None, nothing to process
#         if root is None:
#             return
        
#         # STEP 1: Process LEFT subtree first
#         # This ensures we visit smaller values before larger ones
#         # Recursively traverse left, building up our sorted array
#         self.inorder(root.left)
        
#         # STEP 2: Process CURRENT node (happens AFTER left subtree)
#         # At this point, all nodes smaller than current have been added to vals
#         self.vals.append(root.val)
        
#         # STEP 3: Build prefix sum array incrementally
#         # prefix_sums[i] = sum of all values from index 0 to i (inclusive)
        
#         if not self.prefix_sums:
#             # First element: prefix sum equals the value itself
#             # Example: If first node is 1, then prefix_sums = [1]
#             self.prefix_sums.append(root.val)
#         else:
#             # Subsequent elements: add current value to the last prefix sum
#             # This creates cumulative sum
#             self.prefix_sums.append(self.prefix_sums[-1] + root.val)
        
#         # STEP 4: Process RIGHT subtree last
#         # This ensures larger values come after smaller ones in our array
#         self.inorder(root.right)
    
#     def find_right_boundary(self, left, right, upper):
#         """
#         Binary search to find the RIGHTMOST index where vals[i] <= upper.
        
#         Goal: Find the LAST (rightmost) position in our sorted array that
#               contains a value <= upper. This marks the END of our range.
        
#         Why rightmost? We want to include ALL values <= upper in our sum.
        
#         Example:
#             vals = [1, 3, 5, 7, 9]
#             upper = 7
            
#             Values <= 7: [1, 3, 5, 7] at indices [0, 1, 2, 3]
#             We want index 3 (the rightmost one)
        
#         Algorithm:
#             - If vals[mid] <= upper: This could be our answer, but check RIGHT 
#               for potentially larger valid values
#             - If vals[mid] > upper: This is too large, search LEFT
        
#         Time: O(log n)
        
#         """
#         # Standard binary search loop
#         # IMPORTANT: We use "left <= right" (not "left < right")
#         # This ensures we check the FINAL element when left == right
#         # Example: If left=2, right=2, we still need to check vals[2]
#         # With "left < right", the loop would exit without checking it!
#         while left <= right:
#             mid = (right - left) // 2 + left 
#             # Check if middle element is within our upper bound
#             if self.vals[mid] <= upper:
#                 left = mid + 1
#             else:
#                 right = mid - 1

#         return right
    
#     def find_left_boundary(self, left, right, lower):
#         """
#         Binary search to find the LEFTMOST index where vals[i] >= lower.
        
#         Goal: Find the FIRST (leftmost) position in our sorted array that
#               contains a value >= lower. This marks the START of our range.
        
#         Why leftmost? We want to include ALL values >= lower in our sum.
        
#         Example:
#             vals = [1, 3, 5, 7, 9]
#             lower = 3
            
#             Values >= 3: [3, 5, 7, 9] at indices [1, 2, 3, 4]
#             We want index 1 (the leftmost one)
        
#         Algorithm:
#             - If vals[mid] >= lower: This could be our answer, but check LEFT
#               for potentially smaller valid values
#             - If vals[mid] < lower: This is too small, search RIGHT
        
#         Time: O(log n)
#         """
#         # Standard binary search loop
#         while left <= right:
#             mid = (right - left) // 2 + left

#             if self.vals[mid] >= lower:
#                 right = mid - 1
#             else:
#                 left = mid + 1

#         return left
    
#     def calculate(self, lower, upper):
#         """
#         Calculate the sum of all node values in the range [lower, upper].
        
#         This is the main query function that gets called multiple times.
#         It uses the preprocessed data (vals and prefix_sums) to answer
#         queries very quickly.
        
#         Process:
#         1. Use binary search to find range boundaries in the sorted array
#         2. Use prefix sums to calculate the range sum in O(1)
        
#         Example:
#             vals = [1, 3, 5, 7]
#             prefix_sums = [1, 4, 9, 16]
            
#             Query: lower=3, upper=7
            
#             Step 1: Find boundaries
#                 left_boundary = 1 (first index where vals[i] >= 3)
#                 right_boundary = 3 (last index where vals[i] <= 7)
            
#             Step 2: Calculate sum
#                 We want: vals[1] + vals[2] + vals[3] = 3 + 5 + 7 = 15
#                 Using prefix sums: prefix_sums[3] - prefix_sums[0] = 16 - 1 = 15
        
#         Time: O(log n) for binary searches + O(1) for sum calculation = O(log n)
#         Space: O(1)
        
#         """
#         # =================================================================
#         # EDGE CASE 1: Empty tree (vals is empty)
#         # =================================================================
#         # If tree was empty, vals = [] and prefix_sums = []
#         # No nodes to sum, return 0
#         # Example: Solution(None) then calculate(5, 10) → 0
#         if not self.vals:
#             return 0
        
#         # =================================================================
#         # EDGE CASE 2: Invalid range (lower > upper)
#         # =================================================================
#         # Although problem guarantees lower <= upper, we add safety check
#         # Example: calculate(10, 5) → 0 (invalid range)
#         if lower > upper:
#             return 0
        
#         # STEP 1: Find the rightmost index where value <= upper
#         # This gives us the END of our range
#         # Time: O(log n)
#         right_boundary = self.find_right_boundary(0, len(self.vals) - 1, upper)
        
#         # STEP 2: Find the leftmost index where value >= lower
#         # This gives us the START of our range
#         # Time: O(log n)
#         left_boundary = self.find_left_boundary(0, len(self.vals) - 1, lower)

#         # =================================================================
#         # EDGE CASE 3: No values in range (right_boundary < left_boundary)
#         # =================================================================
#         # This can happen in several scenarios:
#         # 
#         # Scenario A: All values are below lower
#         # Example: vals=[1,2,3], lower=10, upper=20
#         # left_boundary will be len(vals)=3, right_boundary will be 2
#         # Result: 3 > 2, so no values in range
#         # 
#         # Scenario B: All values are above upper
#         # Example: vals=[10,20,30], lower=1, upper=5
#         # left_boundary will be 0, right_boundary will be -1
#         # Result: 0 > -1, so no values in range
#         # 
#         # Scenario C: Range falls in gap between values
#         # Example: vals=[1,2,10,20], lower=5, upper=8
#         # left_boundary = 2 (first value >= 5 is 10)
#         # right_boundary = 1 (last value <= 8 is 2)
#         # Result: 2 > 1, so no values in range
#         if right_boundary < left_boundary:
#             return 0
        
#         # =================================================================
#         # EDGE CASE 4: right_boundary is out of bounds (< 0)
#         # =================================================================
#         # This happens when all values > upper
#         # Example: vals=[10,20,30], upper=5
#         # right_boundary will be -1
#         # Already handled by the check above (since left_boundary >= 0)
#         if right_boundary < 0:
#             return 0
        
#         # =================================================================
#         # EDGE CASE 5: left_boundary is out of bounds (>= len(vals))
#         # =================================================================
#         # This happens when all values < lower
#         # Example: vals=[1,2,3], lower=10
#         # left_boundary will be 3 (len(vals))
#         # Already handled by the check above (since right_boundary < len(vals))
#         if left_boundary >= len(self.vals):
#             return 0
        
#         # STEP 3: Calculate range sum using prefix sums
#         # 
#         # Prefix Sum Formula:
#         # sum(vals[i] to vals[j]) = prefix_sums[j] - prefix_sums[i-1]
#         # 
#         # Why this works:
#         # prefix_sums[j] = vals[0] + vals[1] + ... + vals[j]
#         # prefix_sums[i-1] = vals[0] + vals[1] + ... + vals[i-1]
#         # Difference = vals[i] + vals[i+1] + ... + vals[j] ✓
        
#         # SPECIAL CASE: Starting from the beginning of the array
#         if left_boundary == 0:
#             # We want sum from index 0 to right_boundary
#             # prefix_sums[right_boundary] ALREADY contains this sum
#             # 
#             # Example: vals=[1,3,5,7], prefix_sums=[1,4,9,16]
#             # If we want sum from index 0 to 2 (1+3+5):
#             #   Just return prefix_sums[2] = 9 ✓
#             # 
#             # We can't use the formula because prefix_sums[-1] would give
#             # the LAST element (Python's negative indexing), not what we want
#             return self.prefix_sums[right_boundary]
        
#         # GENERAL CASE: Starting from somewhere in the middle
#         # Use the standard prefix sum formula
#         # 
#         # Example: vals=[1,3,5,7], prefix_sums=[1,4,9,16]
#         # If we want sum from index 1 to 3 (3+5+7):
#         #   prefix_sums[3] - prefix_sums[0] = 16 - 1 = 15 ✓
#         # 
#         # Breakdown:
#         #   prefix_sums[3] = 1+3+5+7 = 16 (sum including unwanted 1)
#         #   prefix_sums[0] = 1          (the part we DON'T want)
#         #   Difference = 3+5+7 = 15     (exactly what we want!)
#         return self.prefix_sums[right_boundary] - self.prefix_sums[left_boundary - 1]


#         # # If we have to return average instead of sum, make the following changes

#         # # Calculate range SUM (same formula as before)
#         # if left_boundary == 0:
#         #     range_sum = self.prefix_sums[right_boundary]
#         # else:
#         #     range_sum = self.prefix_sums[right_boundary] - self.prefix_sums[left_boundary - 1]

#         # # =================================================================
#         # # KEY INSIGHT: Calculate COUNT directly from indices!
#         # # =================================================================
#         # # No need for prefix_counts array
#         # # The indices tell us how many elements are in the range
#         # # 
#         # # Formula: count = right_boundary - left_boundary + 1
#         # # 
#         # # Why the +1?
#         # # - If left_boundary = right_boundary (single element)
#         # #   count = 0 - 0 + 1 = 1 ✓
#         # # - If left_boundary = 0, right_boundary = 2 (three elements)
#         # #   count = 2 - 0 + 1 = 3 ✓
#         # # 
#         # # Example: vals=[3,5,7,10,15,18], range [7,15]
#         # # left_boundary = 2 (index of 7)
#         # # right_boundary = 4 (index of 15)
#         # # count = 4 - 2 + 1 = 3 (elements: 7, 10, 15) ✓
#         # range_count = right_boundary - left_boundary + 1

#         # # Division by zero check (should never happen after edge cases above)
#         # if range_count == 0:
#         #     return 0
        
#         # # Return AVERAGE instead of SUM
#         # return range_sum / range_count
        