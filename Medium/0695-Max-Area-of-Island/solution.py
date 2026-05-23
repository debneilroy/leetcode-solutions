"""
LeetCode 695. Max Area of Island
Difficulty: Medium
URL: https://leetcode.com/problems/max-area-of-island/
"""

# Approach : Iterative DFS (grid not modified)

# class Solution:
#     def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
#         """
#         Find the maximum area of an island in a binary grid.
        
#         An island is a group of connected 1s (land) surrounded by 0s (water).
#         Cells are connected horizontally or vertically (not diagonally).
        
#         Approach: Iterative Depth-First Search (DFS) with Stack and Visited Set
#         - Use explicit stack instead of recursion to avoid stack overflow
#         - Use a separate visited set to track explored cells (preserves original grid)
#         - Explore each island completely before moving to the next cell
        
#         Time Complexity: O(rows * cols)
#         - We visit each cell exactly once in the worst case
#         - Each cell is added to visited set when first encountered
        
#         Space Complexity: O(rows * cols)
#         - Visited set: O(rows * cols) to store all visited coordinates
#         - Stack: O(min(rows, cols)) on average, O(rows * cols) worst case
#         - Total: O(rows * cols)
        
#         Args:
#             grid: 2D binary grid where 1 = land, 0 = water
            
#         Returns:
#             Maximum area of any island, or 0 if no islands exist
            
#         """
#         # Handle edge cases: empty grid or empty rows
#         if not grid or not grid[0]:
#             return 0
        
#         rows, cols = len(grid), len(grid[0])
#         visited = set()  # Track visited cells without modifying grid
#         max_area = 0
        
#         # Iterate through every cell in the grid
#         for row in range(rows):
#             for col in range(cols):
#                 # Found an unvisited land cell - start exploring the island
#                 if grid[row][col] == 1 and (row, col) not in visited:
#                     # Initialize DFS using an explicit stack
#                     current_area = 0
#                     stack = [(row, col)]
                    
#                     # Mark starting cell as visited
#                     visited.add((row, col))
                    
#                     # Explore all connected land cells iteratively
#                     while stack:
#                         curr_row, curr_col = stack.pop()
                        
#                         # Count this cell as part of the island
#                         current_area += 1
                        
#                         # Explore all 4 adjacent directions: down, up, right, left
#                         for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
#                             next_row = curr_row + dr
#                             next_col = curr_col + dc
                            
#                             # Check if neighbor is within bounds, is land, and not visited
#                             if (0 <= next_row < rows and 
#                                 0 <= next_col < cols and 
#                                 grid[next_row][next_col] == 1 and
#                                 (next_row, next_col) not in visited):
                                
#                                 # Mark as visited to prevent duplicates in stack
#                                 visited.add((next_row, next_col))
                                
#                                 # Add to stack for exploration
#                                 stack.append((next_row, next_col))
                    
#                     # Update maximum area found so far
#                     max_area = max(max_area, current_area)

#         return max_area

        # Example Dry Run:
        #     Input: grid = [[0, 1, 0],
        #                   [1, 1, 0],
        #                   [0, 1, 1]]
            
        #     Step-by-step execution:
            
        #     Initial state:
        #     - visited = set()
        #     - max_area = 0
            
        #     1. Scan (0,0): value=0, skip
            
        #     2. Scan (0,1): value=1 and not visited, begin DFS
        #        - visited.add((0,1))
        #        - stack=[(0,1)], current_area=0
               
        #        Pop (0,1): current_area=1
        #        - Check (1,1): land and not visited
        #          * visited.add((1,1)), stack=[(1,1)]
        #        - Check (-1,1): out of bounds
        #        - Check (0,2): water, skip
        #        - Check (0,0): water, skip
               
        #        Pop (1,1): current_area=2
        #        - Check (2,1): land and not visited
        #          * visited.add((2,1)), stack=[(2,1)]
        #        - Check (0,1): already in visited, skip
        #        - Check (1,2): water, skip
        #        - Check (1,0): land and not visited
        #          * visited.add((1,0)), stack=[(2,1), (1,0)]
               
        #        Pop (1,0): current_area=3
        #        - Check (2,0): water, skip
        #        - Check (0,0): water, skip
        #        - Check (1,1): already in visited, skip
        #        - Check (1,-1): out of bounds
               
        #        Pop (2,1): current_area=4
        #        - Check (2,2): land and not visited
        #          * visited.add((2,2)), stack=[(2,2)]
        #        - Check (1,1): already in visited, skip
        #        - Check (2,0): water, skip
               
        #        Pop (2,2): current_area=5
        #        - Check (2,1): already in visited, skip
        #        - All other neighbors are water or out of bounds
               
        #        Stack empty: Island complete
        #        - current_area = 5
        #        - max_area = max(0, 5) = 5
        #        - visited = {(0,1), (1,1), (2,1), (1,0), (2,2)}
            
        #     3. Continue scanning (0,2): water, skip
        #     4. Scan (1,0): already in visited, skip
        #     5. Scan (1,1): already in visited, skip
        #     6. Scan (1,2): water, skip
        #     7. Scan (2,0): water, skip
        #     8. Scan (2,1): already in visited, skip
        #     9. Scan (2,2): already in visited, skip
            
        #     Output: 5


# Approach : Iterative DFS (grid modified)

# class Solution:
#     def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
#         """
#         Find the maximum area of an island in a binary grid.
        
#         An island is a group of connected 1s (land) surrounded by 0s (water).
#         Cells are connected horizontally or vertically (not diagonally).
        
#         Approach: Iterative Depth-First Search (DFS) with Stack
#         - Use explicit stack instead of recursion to avoid stack overflow
#         - Mark cells as visited by modifying the grid (set to 0)
#         - Explore each island completely before moving to the next cell
        
#         Time Complexity: O(rows * cols)
#         - We visit each cell exactly once in the worst case
#         - Each cell is marked as visited (set to 0) when first encountered
        
#         Space Complexity: O(rows * cols)
#         - In the worst case (entire grid is one island), the stack can grow
#           to contain all cells before we start popping
#         - More typically, O(min(rows, cols)) for a snake-shaped island
        
#         Args:
#             grid: 2D binary grid where 1 = land, 0 = water
            
#         Returns:
#             Maximum area of any island, or 0 if no islands exist
#         """
#         # Handle edge cases: empty grid or empty rows
#         if not grid or not grid[0]:
#             return 0
        
#         rows, cols = len(grid), len(grid[0])
#         max_area = 0
        
#         # Iterate through every cell in the grid
#         for row in range(rows):
#             for col in range(cols):
#                 # Found an unvisited land cell - start exploring the island
#                 if grid[row][col] == 1:
#                     # Initialize DFS using an explicit stack
#                     current_area = 0
#                     stack = [(row, col)]
                    
#                     # Mark starting cell as visited to avoid revisiting
#                     grid[row][col] = 0
                    
#                     # Explore all connected land cells iteratively
#                     while stack:
#                         curr_row, curr_col = stack.pop()
                        
#                         # Count this cell as part of the island
#                         current_area += 1
                        
#                         # Explore all 4 adjacent directions: down, up, right, left
#                         for delta_row, delta_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
#                             next_row = curr_row + delta_row
#                             next_col = curr_col + delta_col
                            
#                             # Check if neighbor is within bounds and is unvisited land
#                             if (0 <= next_row < rows and 
#                                 0 <= next_col < cols and 
#                                 grid[next_row][next_col] == 1):
                                
#                                 # Mark as visited immediately to prevent duplicates in stack
#                                 grid[next_row][next_col] = 0
                                
#                                 # Add to stack for exploration
#                                 stack.append((next_row, next_col))
                    
#                     # Update maximum area found so far
#                     max_area = max(max_area, current_area)
        
#         return max_area

# Approach : BFS

# from collections import deque

# class Solution:
#     def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
#         """
#         Find the maximum area of an island in a binary grid.
        
#         An island is a group of connected 1s (land) surrounded by 0s (water).
#         Cells are connected horizontally or vertically (not diagonally).
        
#         Approach: Iterative Breadth-First Search (BFS) with Queue and Visited Set
#         - Use queue (deque) for level-by-level exploration
#         - Use a separate visited set to track explored cells (preserves original grid)
#         - Process cells in order of distance from starting point
        
#         Time Complexity: O(rows * cols)
#         - We visit each cell exactly once in the worst case
#         - Each cell is added to visited set when first encountered
        
#         Space Complexity: O(rows * cols)
#         - Visited set: O(rows * cols) to store all visited coordinates
#         - Queue: O(min(rows, cols)) on average, O(rows * cols) worst case
#         - Total: O(rows * cols)
        
#         Args:
#             grid: 2D binary grid where 1 = land, 0 = water
            
#         Returns:
#             Maximum area of any island, or 0 if no islands exist
#         """
#         # Handle edge cases: empty grid or empty rows
#         if not grid or not grid[0]:
#             return 0
        
#         rows, cols = len(grid), len(grid[0])
#         visited = set()  # Track visited cells without modifying grid
#         max_area = 0
        
#         # Iterate through every cell in the grid
#         for row in range(rows):
#             for col in range(cols):
#                 # Found an unvisited land cell - start exploring the island
#                 if grid[row][col] == 1 and (row, col) not in visited:
#                     # Initialize BFS using a queue (deque for O(1) operations)
#                     current_area = 0
#                     queue = deque([(row, col)])
                    
#                     # Mark starting cell as visited
#                     visited.add((row, col))
                    
#                     # Explore all connected land cells level by level
#                     while queue:
#                         curr_row, curr_col = queue.popleft()  # FIFO for BFS
                        
#                         # Count this cell as part of the island
#                         current_area += 1
                        
#                         # Explore all 4 adjacent directions: down, up, right, left
#                         for delta_row, delta_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
#                             next_row = curr_row + delta_row
#                             next_col = curr_col + delta_col
                            
#                             # Check if neighbor is within bounds, is land, and not visited
#                             if (0 <= next_row < rows and 
#                                 0 <= next_col < cols and 
#                                 grid[next_row][next_col] == 1 and
#                                 (next_row, next_col) not in visited):
                                
#                                 # Mark as visited to prevent duplicates in queue
#                                 visited.add((next_row, next_col))
                                
#                                 # Add to queue for exploration
#                                 queue.append((next_row, next_col))
                    
#                     # Update maximum area found so far
#                     max_area = max(max_area, current_area)
        
#         return max_area


# Approach : Recursive DFS (grid not modified)

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """
        Find the maximum area of an island in a binary grid.
        
        An island is a group of connected 1s (land) surrounded by 0s (water).
        Cells are connected horizontally or vertically (not diagonally).
        
        Approach: Recursive Depth-First Search (DFS) with Visited Set
        - Use recursion call stack for exploration
        - Use a separate visited set to track explored cells (preserves original grid)
        - Explore each island completely using recursive calls
        
        Time Complexity: O(rows * cols)
        - Visit each cell exactly once
        - Each cell is added to visited set when first encountered
        
        Space Complexity: O(rows * cols)
        - Visited set: O(rows * cols) to store all visited coordinates
        - Recursion call stack: O(rows * cols) in worst case (entire grid is one island)
        - Total: O(rows * cols)
        
        Args:
            grid: 2D binary grid where 1 = land, 0 = water
            
        Returns:
            Maximum area of any island, or 0 if no islands exist
        """
        # Handle edge cases: empty grid or empty rows
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        visited = set()  # Track visited cells without modifying grid
        max_area = 0
        
        def dfs(row: int, col: int) -> int:
            """
            Recursively explore island and return its area.
            
            Args:
                row: Current row index
                col: Current column index
                
            Returns:
                Area of island reachable from this cell
            """
            # Base case: out of bounds, water, or already visited
            if (row < 0 or row >= rows or 
                col < 0 or col >= cols or 
                grid[row][col] == 0 or
                (row, col) in visited):
                return 0
            
            # Mark current cell as visited
            visited.add((row, col))
            
            # Count current cell (1) plus all connected cells in 4 directions
            area = 1
            area += dfs(row + 1, col)  # explore down
            area += dfs(row - 1, col)  # explore up
            area += dfs(row, col + 1)  # explore right
            area += dfs(row, col - 1)  # explore left
            
            return area
        
        # Iterate through every cell in the grid
        for row in range(rows):
            for col in range(cols):
                # Found an unvisited land cell - start exploring the island
                if grid[row][col] == 1 and (row, col) not in visited:
                    # Call DFS and get the area of this island
                    current_area = dfs(row, col)
                    # Update maximum area found so far
                    max_area = max(max_area, current_area)
        
        return max_area
        