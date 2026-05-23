"""
LeetCode 766. Toeplitz Matrix
Difficulty: Easy
URL: https://leetcode.com/problems/toeplitz-matrix/
"""

# Brute Force Approach:
# A brute-force way to check if a matrix is Toeplitz is to explicitly compare all elements along each diagonal. For every cell (i, j), we could traverse its diagonal (i+1, j+1), (i+2, j+2), … and ensure all elements are the same.

# Time Complexity: O((m·n)·min(m, n)) since we potentially recheck elements multiple times.

# Space Complexity: O(1).

# Tradeoff: Very simple to reason about, but inefficient because it redundantly checks the same diagonals multiple times.

# class Solution:
#     def isToeplitzMatrix(self, matrix):
#         """
#         Brute Force: Check every diagonal from every starting position.
        
#         Time Complexity: O(m × n × min(m, n))
#         - Outer loop: O(m) iterations over all rows
#         - Inner loop: O(n) iterations over all columns
#         - While loop: O(min(m, n)) to traverse diagonal from each position
#           (diagonal length is limited by the smaller dimension - either we run
#            out of rows or columns, whichever comes first)
#         - Total: O(m × n × min(m, n))
#         - Highly inefficient due to redundant diagonal checks:
#           Each diagonal is checked multiple times from different starting points.
#           For example, diagonal [matrix[0][0], matrix[1][1], matrix[2][2]] is
#           checked when starting from (0,0), then partially rechecked when starting
#           from (1,1), and again from (2,2), leading to massive redundancy.
        
#         Space Complexity: O(1)
#         - Only constant extra space for variables (i, j, r, c)
#         - No additional data structures
#         """
#         m, n = len(matrix), len(matrix[0])
        
#         for i in range(m):
#             for j in range(n):
#                 # Check all elements on this diagonal
#                 r, c = i, j
#                 while r < m and c < n:
#                     if matrix[r][c] != matrix[i][j]:
#                         return False
#                     r += 1
#                     c += 1
#         return True

# Optimal Approach:
# Instead of rechecking, we can just ensure each element matches its bottom-right neighbor — if every (i, j) equals (i+1, j+1), all diagonals are constant.


class Solution:
    def isToeplitzMatrix(self, matrix: list[list[int]]) -> bool:
        """
        Time Complexity:  O(m * n)
            → We check each element once (except last row/col).
        Space Complexity: O(1)
            → Constant extra space; in-place comparisons only.
        """

        # Get matrix dimensions
        m, n = len(matrix), len(matrix[0])

        # Iterate over all elements except the last row and last column
        for i in range(m - 1):
            for j in range(n - 1):
                # Compare with the element diagonally below-right
                if matrix[i][j] != matrix[i + 1][j + 1]:
                    return False  # Found a mismatch; not Toeplitz

        # All diagonals consistent
        return True


# Variant : Matrix given as list

# Given an array list, return true if the array is Toeplitz. Otherwise, return false.

# A list represents a Toeplitz matrix if, when interpreted as a 2D matrix with rows and cols,
# every diagonal from top-left to bottom-right contains the same elements.

# Example 1:

# Input:
# matrix = [1,2,3,4,5,1,2,3,9,5,1,2], rows = 3, cols = 4

# Output: True

# Explanation:
# In the above grid, the diagonals are:
# [9], [5,5], [1,1,1], [2,2,2], [3,3], [4].
# In each diagonal all elements are the same, so the answer is True.

# Constraints:

# m == matrix.length

# n == matrix[i].length

# 1 <= m, n <= 20

# 0 <= matrix[i][j] <= 99

# class Solution:
#     def hasSameDiagonalValues(self, list: List[int], rows: int, cols: int) -> bool:
#         """
#         Check if a flattened matrix is Toeplitz (all diagonals have same elements).
        
#         Time Complexity: O(rows × cols)
#         - Iterate through every element in the list once
#         - Each comparison operation is O(1)
        
#         Space Complexity: O(1)
#         - Only constant extra space for variables (i, cr, cc)
#         - No additional data structures
#         """
#         # Iterate through each element in the flattened list
#         for i in range(len(list)):
#             # Calculate current row: how many complete rows have we passed?
#             cr = i // cols
            
#             # Calculate current column: position within the current row
#             cc = i % cols
            
#             # Skip elements in the last row or last column
#             # (they don't have a bottom-right diagonal neighbor to check)
#             if cr == rows - 1 or cc == cols - 1:
#                 continue
            
#             # Check if current element matches its bottom-right diagonal neighbor
#             # Moving to bottom-right: +cols (down one row) + 1 (right one column)
#             if list[i] != list[i + (cols + 1)]:
#                 return False
        
#         # All diagonal checks passed - matrix is Toeplitz
#         return True

  
