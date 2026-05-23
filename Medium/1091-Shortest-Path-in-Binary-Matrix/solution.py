"""
LeetCode 1091. Shortest Path in Binary Matrix
Difficulty: Medium
URL: https://leetcode.com/problems/shortest-path-in-binary-matrix/
"""

# Approach : BFS with parent map solution (Meta might prefer this)

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        """
        Find shortest path length in n×n binary matrix using BFS.
        
        Time Complexity: O(N²)
            - BFS visits each cell at most once: O(N²)
            - Each cell checks 8 directions: O(1) per cell
            - Path length calculation: O(path_length) ≤ O(N²)
            - Total: O(N²)
        
        Space Complexity: O(N²)
            - Queue: O(N²) cells in worst case
            - Parent dict: O(N²) mappings (serves dual purpose: visited + parent tracking)
            - Total: O(N²)
        
        Note: We don't need a separate visited set because parent dict already
        tracks visited cells. If (r,c) is in parent, we've visited it.
        This saves one O(N²) data structure while maintaining O(1) lookup.
        
        Parent Map Rationale:
            - Enables path reconstruction by storing how we reached each cell
            - Each cell maps to its predecessor: parent[(child)] = (parent_cell)
            - To get actual path: backtrack from end to start, then reverse
            - To get path length: count hops during backtracking (O(path_length))
            - Alternative: store distance in queue as (r, c, dist), but parent map
              is more flexible - can get both path AND length from same structure
            - Useful for follow-up questions like "return the actual path" or
              "return all cells visited along the shortest path"
        
        Args:
            grid: n×n binary matrix where 0 is traversable, 1 is blocked
        
        Returns:
            int: Length of shortest path from (0,0) to (n-1,n-1)
                 -1 if no path exists
        """
        # Edge case: empty grid
        if not grid:
            return -1  # For path: return []
        
        # Edge case: empty first row (e.g., grid = [[]])
        # Without this check, grid[0][0] would raise IndexError
        # Example: grid = [[]] → grid[0] = [] → grid[0][0] = IndexError!
        if not grid[0]:
            return -1 # For path: return []
        
        n = len(grid)
        
        # Edge case: start or end blocked
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1 # For path: return []
        
        # Edge case: single cell (start == end)
        if n == 1:
            return 1 # return 
        
        # BFS initialization
        queue = deque([(0, 0)])  # Cells to explore (FIFO)
        
        # parent: Map each cell to its predecessor (also acts as visited tracker)
        # If (r,c) is in parent dict, it means we've already visited that cell
        # Example after exploring a few cells:
        # {(0,0): None, (0,1): (0,0), (1,0): (0,0), (1,1): (0,1)}
        # This means: (0,1) was reached from (0,0), (1,0) from (0,0), (1,1) from (0,1)
        parent = {(0, 0): None}
        
        # 8 directions: (row_delta, col_delta) for all adjacent cells
        # Each tuple represents how to move from current cell to neighbor:
        #   negative row_delta = move up, positive = move down
        #   negative col_delta = move left, positive = move right
        dirs = [
            (-1, -1),  # up-left diagonal
            (-1,  0),  # up (directly above)
            (-1,  1),  # up-right diagonal
            ( 0, -1),  # left (same row)
            ( 0,  1),  # right (same row)
            ( 1, -1),  # down-left diagonal
            ( 1,  0),  # down (directly below)
            ( 1,  1)   # down-right diagonal
        ]
        
        # BFS traversal
        while queue:
            r, c = queue.popleft()
            
            # Explore all 8 neighbors
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc  # neighbor_row, neighbor_col
                
                # Check: in bounds, traversable, unvisited (not in parent dict)
                if (0 <= nr < n and 0 <= nc < n and 
                    grid[nr][nc] == 0 and (nr, nc) not in parent):
                    
                    parent[(nr, nc)] = (r, c)  # Record parent AND mark as visited
                    
                    # Early exit if destination reached
                    if nr == n-1 and nc == n-1:
                        return self.get_path_length(parent, (nr, nc))
                    
                    queue.append((nr, nc))
        
        # No path found (queue exhausted)
        return -1 # For path: return []
    
    def get_path_length(self, parent: dict, end: tuple) -> int:
        """
        Calculate path length by counting parent hops.
        
        Time Complexity: O(L) where L is path length
            - Backtrack through parent pointers once: O(L)
            - L ≤ N² because:
              * Grid has N² total cells
              * BFS visited set ensures each cell visited at most once
              * Longest path visits all cells: L = N²
              * Example worst case (4×4 grid, spiral path visiting all 16 cells):
                (0,0)→(0,1)→(0,2)→(0,3)→(1,3)→(2,3)→(2,2)→(2,1)→
                (3,1)→(3,0)→(2,0)→(1,0)→(1,1)→(1,2)→(3,2)→(3,3)
              * Best case: L = N (diagonal path from corner to corner)
        
        Space Complexity: O(1)
            - Only uses a counter variable
            - No additional data structures created
        
        If returning actual path instead of length:
            Time Complexity: O(L)
                - Still need to backtrack through parent pointers: O(L)
                - Reversing the path list: O(L)
                - Total: O(L) where L ≤ N²
            
            Space Complexity: O(L)
                - Path list stores all coordinates: O(L)
                - L ≤ N² in worst case
                - So space becomes O(N²) instead of O(1)
        
        Args:
            parent: Dictionary mapping child -> parent coordinate
            end: End coordinate (destination cell)
        
        Returns:
            int: Number of cells in the shortest path
        """
        
        length = 0
        current = end
        # path = [] # to get the actual path
        
        # Count hops back to start (parent = None)
        while current is not None:
            length += 1
            # path.append(current)  # Uncomment to build actual path: adds O(L) space
            current = parent[current]
        
        return length
        # return path[::-1]  # Uncomment to return actual path: O(L) time for reversal

# Check Discord post https://discord.com/channels/1356367273614508132/1370878985176875058

# Approach: BFS (Without Overwriting the Input)

# class Solution:
#     def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
#         """
#         Find shortest path length using BFS with distance tracking in queue.
#         Set-based approach with optimizations.

#         Time Complexity: O(N²) for n×n grid, O(M×N) for m×n rectangular grid
#             - BFS visits each cell at most once: O(N²) or O(M×N)
#             - Each cell checks 8 directions: O(1) per cell
#             - Early termination when destination found
#             - Total: O(N²) for square, O(M×N) for rectangular
        
#         Space Complexity: O(N²) for n×n grid, O(M×N) for m×n rectangular grid
#             - Queue: O(N²) or O(M×N) cells in worst case
#             - Visited set: O(N²) or O(M×N) coordinates
#             - Directions tuple: O(1) constant space (8 directions)
#             - Total: O(N²) for square, O(M×N) for rectangular
        
#         Note: This approach stores distance in queue (r, c, dist) instead of
#         using parent map. Trade-off:
#             - Simpler for getting path length only
#             - Cannot reconstruct actual path without parent map
#             - Slightly less flexible for follow-up questions
        
#         Args:
#             grid: n×n binary matrix where 0 is traversable, 1 is blocked
        
#         Returns:
#             int: Length of shortest path from (0,0) to (n-1,n-1)
#                  -1 if no path exists
#         """
#         # Edge case: empty grid
#         if not grid:
#             return -1
        
#         # Edge case: empty first row (e.g., grid = [[]])
#         # Without this check, grid[0][0] would raise IndexError
#         if not grid[0]:
#             return -1

#         # Get grid dimension (assuming square grid)
#         n = len(grid)

#         # if rectangular grid
#         # m = len(grid)        # Number of rows
#         # n = len(grid[0])     # Number of columns
        
#         # Early termination: check if start or end positions are blocked
#         # grid[0][0] is top-left start, grid[n-1][n-1] is bottom-right end

#         if grid[0][0] == 1 or grid[n-1][n-1] == 1: # grid[m-1][n-1] for rectangular grid
#             return -1
        
#         # Edge case: single cell grid
#         # If we can start and end at same position, path length is 1

#         if n == 1: # for rectangular grid, if m == 1 and n == 1:
#             return 1
        
#         # Initialize visited set with starting position
#         # Using set for O(1) average lookup time
#         visited = {(0, 0)}
        
#         # Initialize BFS queue with (row, col, distance)
#         # Start at (0,0) with path length 1 (counting the starting cell)
#         queue = deque([(0, 0, 1)])
        
#         # Use tuple for directions (slightly faster than list)
#         # 8-directional movement: up, down, left, right, and 4 diagonals
#         # Format: (row_offset, col_offset)
#         dirs = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        
#         # BFS main loop - continue until queue is empty
#         while queue:
#             # Get current position and distance from queue
#             r, c, dist = queue.popleft()
            
#             # Explore all 8 possible directions from current position
#             for dr, dc in dirs:
#                 # Calculate new position coordinates
#                 nr, nc = r + dr, c + dc
                
#                 # Check if new position is valid:
#                 # 1. Within grid boundaries (0 <= nr < n and 0 <= nc < n)
#                 # 2. Cell is passable (not grid[nr][nc] means grid[nr][nc] == 0)
#                 # 3. Not already visited ((nr, nc) not in visited)
#                 if (0 <= nr < n and 0 <= nc < n and 
#                     not grid[nr][nc] and (nr, nc) not in visited): # 0 <= nr < m and 0 <= nc < n for rectangular grid
                    
#                     # Check if we've reached the destination (bottom-right corner)
#                     # Return immediately for optimal performance
#                     # Return dist + 1 because:
#                     #   - dist = path length to reach current cell (r,c)
#                     #   - We're moving to neighbor (nr,nc), which adds 1 to path
#                     #   - Example: if dist=3 at (r,c), moving to (nr,nc) makes path length 4

#                     if nr == n-1 and nc == n-1: # if nr == m-1 and nc == n-1 for rectangular grid
#                         return dist + 1
                    
#                     # Mark new position as visited to avoid revisiting
#                     # Do this BEFORE adding to queue to prevent duplicates
#                     # Done AFTER destination check since we return immediately above
#                     # This saves one set.add() operation when destination is found
#                     visited.add((nr, nc))
                    
#                     # Add new position to queue with incremented distance
#                     # dist + 1 represents the path length to reach this new cell
#                     queue.append((nr, nc, dist + 1))
        
#         # If we exit the loop without finding destination, no path exists
#         return -1


# # Approach : Optimized BFS (Overwriting the input)

# class Solution:
#     def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
#         """
#         Find shortest path length using BFS with in-place grid modification.
#         Space-optimized approach that marks visited cells directly in the grid.
        
#         TC: O(N²) for n×n grid, O(M×N) for m×n rectangular grid
#         SC: O(N²) for n×n grid, O(M×N) for m×n rectangular grid
        
#         Time Complexity: O(N²) for n×n grid, O(M×N) for m×n rectangular grid
#             - BFS visits each cell at most once: O(N²) or O(M×N)
#             - Each cell checks 8 directions: O(1) per cell
#             - Early termination when destination found
#             - Total: O(N²) for square, O(M×N) for rectangular
        
#         Space Complexity: O(N²) for n×n grid, O(M×N) for m×n rectangular grid
#             - Queue: O(N²) or O(M×N) cells in worst case
#             - No separate visited set (uses grid in-place)
#             - Directions list: O(1) constant space (8 directions)
#             - Total: O(N²) for square, O(M×N) for rectangular

#         Note: This approach modifies the input grid by marking visited cells as 1.
        
#         Advantages:
#         ✅ Memory: 67% reduction (1 structure vs 3: queue only, no visited/parent)
#         ✅ Simple: grid[nr][nc] == 0 checks both passable AND unvisited
#         ✅ Performance: Better cache locality, fewer pointer dereferences
#         ✅ Practical: For 10K×10K grid, saves ~1.6GB memory
        
#         Disadvantages:
#         ❌ Destructive: Grid permanently modified, cannot restore
#         ❌ No path: Cannot return actual coordinates (no parent tracking)
#         ❌ Single use: Grid cannot be reused for multiple queries
        
#         Use when: Grid disposable, only need length, memory constrained
#         Avoid when: Need actual path, grid must be preserved, multiple queries
        
#         Args:
#             grid: n×n binary matrix where 0 is traversable, 1 is blocked
#                   WARNING: This grid will be modified in-place
        
#         Returns:
#             int: Length of shortest path from (0,0) to (n-1,n-1)
#                  -1 if no path exists
#         """
#         # Edge case: empty grid
#         if not grid:
#             return -1
        
#         # Edge case: empty first row (e.g., grid = [[]])
#         # Without this check, grid[0][0] would raise IndexError
#         if not grid[0]:
#             return -1
            
#         n = len(grid)
        
#         # Early termination: check if start or end is blocked or if grid is empty
#         if not grid or grid[0][0] == 1 or grid[n-1][n-1] == 1:
#             return -1
        
#         # Edge case: single cell
#         if n == 1:
#             return 1
        
#         # Mark start as visited in-place (modifies grid)
#         # Uses grid itself as visited tracker instead of separate set
#         grid[0][0] = 1
        
#         # BFS with deque for O(1) popleft and append operations
#         queue = deque([(0, 0, 1)])
        
#         # 8-directional moves (precomputed for efficiency)
#         # Format: (row_offset, col_offset)
#         dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
#         while queue:
#             r, c, dist = queue.popleft()
            
#             # Check all 8 directions
#             for dr, dc in dirs:
#                 nr, nc = r + dr, c + dc
                
#                 # Boundary check and cell availability in one condition
#                 # grid[nr][nc] == 0 means both: passable AND unvisited
#                 if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
#                     # Reached destination
#                     # Check BEFORE marking as visited for early exit optimization
#                     if nr == n-1 and nc == n-1:
#                         return dist + 1
                    
#                     # Mark as visited in-place and add to queue
#                     # grid[nr][nc] = 1 serves dual purpose:
#                     # 1. Marks cell as visited (prevents revisiting)
#                     # 2. Modifies original grid (cannot restore later)
#                     grid[nr][nc] = 1
#                     queue.append((nr, nc, dist + 1))
        
#         return -1

# # Variant 1 : Return the shortest path itself (included in the first approach)

# # Return shortest path without grid modification (this one is essentially the same, just uses the visted set)

# def shortestPathBinaryMatrix(grid):
#     """
#     Find shortest path in binary matrix without modifying the input grid.
#     Uses separate visited set for tracking. TC: O(N²), SC: O(N²)
#     """
#     n = len(grid)
#     # m×n grid: m = len(grid), n = len(grid[0])
    
#     # Edge cases
#     if not grid or grid[0][0] == 1 or grid[n-1][n-1] == 1:
#         return []
#     # m×n grid: change grid[n-1][n-1] to grid[m-1][n-1]
    
#     if n == 1:
#         return [(0, 0)]
#     # m×n grid: change to "if m == 1 and n == 1"
    
#     # BFS setup
#     queue = deque([(0, 0)])
#     visited = {(0, 0)}  # Separate visited set instead of modifying grid
#     parent = {(0, 0): None}
    
#     # 8 directions: up-left, up, up-right, left, right, down-left, down, down-right
#     dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
#     while queue:
#         r, c = queue.popleft()
        
#         # Explore all 8 neighbors
#         for dr, dc in dirs:
#             nr, nc = r + dr, c + dc
            
#             # Check: in bounds, traversable (0), not visited
#             if (0 <= nr < n and 0 <= nc < n and 
#                 grid[nr][nc] == 0 and (nr, nc) not in visited): 
#                 # m×n grid: change "0 <= nr < n and 0 <= nc < n" to "0 <= nr < m and 0 <= nc < n"
#                 visited.add((nr, nc))  # Mark as visited in separate set
#                 parent[(nr, nc)] = (r, c)
                
#                 # Check if we reached destination
#                 if nr == n-1 and nc == n-1: # m×n grid: change "nr == n-1 and nc == n-1" to "nr == m-1 and nc == n-1"
#                     return reconstruct_path(parent, (nr, nc))
 
#                 queue.append((nr, nc))
    
#     # No path found
#     return []


# def reconstruct_path(parent, end):
#     """
#     Reconstruct path from parent mapping by backtracking.
    
#     Args:
#         parent: Dictionary mapping child -> parent coordinate
#         end: End coordinate (destination)
    
#     Returns:
#         List[Tuple[int, int]]: Path from start to end
    
#     Time Complexity: O(path_length)
#         - Backtrack through parent pointers once
#         - Reverse the list: O(path_length)
    
#     Space Complexity: O(path_length)
#         - Path list stores all coordinates in the path
#     """
#     path = []
#     current = end
    
#     # Backtrack through parents until we reach start (parent = None)
#     while current is not None:
#         path.append(current)
#         current = parent[current]
    
#     # Reverse to get path from start to end
#     return path[::-1]

# # Minh's solution

# class Variant:
#     def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> List[tuple[int]]:
#         """
#         Find shortest path in m×n binary matrix using BFS.
        
#         TC: O(M×N) - visits each cell at most once
#         SC: O(M×N) - queue, visited set, and parent map
        
#         Time Complexity: O(M×N)
#             - BFS visits each cell at most once: O(M×N)
#             - Each cell checks 8 directions: O(1) per cell
#             - Path reconstruction: O(path_length) ≤ O(M×N)
#             - Total: O(M×N)
        
#         Space Complexity: O(M×N)
#             - Queue: O(M×N) cells in worst case
#             - Visited set: O(M×N) coordinates
#             - Parent dict: O(M×N) mappings
#             - Path list: O(M×N) in worst case
#             - Total: O(M×N)
        
#         Args:
#             grid: m×n binary matrix where 0 is traversable, 1 is blocked
        
#         Returns:
#             List[tuple]: Path coordinates from (0,0) to (m-1,n-1)
#             [] if no path exists
#         """
#         # Edge case: empty grid
#         if not grid:
#             return []
        
#         # Edge case: empty first row
#         if not grid[0]:
#             return []
        
#         # Store last valid indices (alternative to storing dimensions)
#         # rows = m-1, cols = n-1 where m and n are dimensions
#         rows, cols = len(grid) - 1, len(grid[0]) - 1
        
#         # Edge case: start or end blocked
#         if grid[0][0] == 1 or grid[rows][cols] == 1:
#             return []
        
#         # Edge case: single cell (when rows=0 and cols=0)
#         if rows == 0 and cols == 0:
#             return [(0, 0)]
        
#         # Parent mapping for path reconstruction
#         # Maps each visited cell to the cell we came from
#         map = {}  # (child) -> (parent)
        
#         # 8 directions: all adjacent cells including diagonals
#         directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
#         # BFS initialization
#         queue = deque([(0, 0)])       # Start from top-left
#         visited = {(0, 0)}            # Track visited cells to avoid cycles
#         reached_end = False           # Flag to track if destination was found
        
#         # BFS traversal to find shortest path
#         while queue:
#             row, col = queue.popleft()  # Get current cell (FIFO)
            
#             # Check if reached destination (bottom-right corner)
#             if row == rows and col == cols:
#                 reached_end = True
#                 break  # Early exit - no need to explore further
            
#             # Explore all 8 neighbors
#             for dr, dc in directions:
#                 nr, nc = row + dr, col + dc  # Calculate neighbor coordinates
                
#                 # Check if neighbor is valid:
#                 # - In bounds (using <= since rows/cols are last indices)
#                 # - Not visited yet
#                 # - Traversable (grid value is 0)
#                 if (0 <= nr <= rows and 
#                     0 <= nc <= cols and 
#                     (nr, nc) not in visited and 
#                     grid[nr][nc] == 0):
                    
#                     map[(nr, nc)] = (row, col)  # Store parent for backtracking
#                     queue.append((nr, nc))       # Add to queue for BFS
#                     visited.add((nr, nc))        # Mark as visited
        
#         # No path found - destination was not reached
#         if not reached_end:
#             return []
        
#         # Reconstruct path by backtracking from end to start using parent map
#         result = []
#         r, c = rows, cols  # Start from destination
        
#         # Follow parent pointers back to origin (0, 0)
#         while (r, c) != (0, 0):
#             result.append((r, c))
#             r, c = map[(r, c)]  # Move to parent cell
        
#         result.append((0, 0))  # Add starting cell
        
#         # Reverse to get path from start to end
#         return result[::-1]

# # Return both the shortest path and its length

# # def shortestPath(grid):
# #     """
# #     Returns:
# #         Tuple[int, List[Tuple[int, int]]]: (path_length, path_coordinates)
# #         (-1, []) if no path exists

# #     TC : O(N^2) SC : O(N^2)
# #     """
# #     n = len(grid)
    
# #     if not grid or grid[0][0] == 1 or grid[n-1][n-1] == 1:
# #         return (-1, [])
    
# #     if n == 1:
# #         return (1, [(0, 0)])
    
# #     # BFS queue: (row, col)
# #     queue = deque([(0, 0)])
# #     visited = {(0, 0)}
    
# #     # Parent tracking: child -> parent mapping
# #     parent = {(0, 0): None}
    
# #     dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    
# #     while queue:
# #         r, c = queue.popleft()
        
# #         for dr, dc in dirs:
# #             nr, nc = r + dr, c + dc
            
# #             if (0 <= nr < n and 0 <= nc < n and 
# #                 not grid[nr][nc] and (nr, nc) not in visited):
                
# #                 visited.add((nr, nc))
# #                 parent[(nr, nc)] = (r, c)  # Track parent
                
# #                 # Check if reached destination
# #                 if nr == n-1 and nc == n-1:
# #                     # Reconstruct path by backtracking through parents
# #                     path = reconstruct_path(parent, (nr, nc))
# #                     return (len(path), path)
                
# #                 queue.append((nr, nc))
    
# #     return (-1, [])

# # def reconstruct_path(parent, end):
# #     """
# #     Reconstruct path from parent mapping by backtracking.
    
# #     Args:
# #         parent: Dictionary mapping child -> parent coordinate
# #         end: End coordinate (destination)
    
# #     Returns:
# #         List[Tuple[int, int]]: Path from start to end
    
# #     Time Complexity: O(path_length)
# #         - Backtrack through parent pointers once
# #         - Reverse the list: O(path_length)
    
# #     Space Complexity: O(path_length)
# #         - Path list stores all coordinates in the path
# #     """
# #     path = []
# #     current = end
    
# #     # Backtrack through parents until we reach start (parent = None)
# #     while current is not None:
# #         path.append(current)
# #         current = parent[current]
    
# #     # Reverse to get path from start to end
# #     return path[::-1]

# # Follow ups:

# # For most large grids (thousands × thousands), use bidirectional BFS. We search from both start and end simultaneously, meeting in the middle. This typically reduces both time and memory by 50% or more.

# # If the grid is sparse (few obstacles), A* would be even better. We use a distance heuristic to prioritize cells closer to the goal, exploring far fewer cells overall.

# # If memory is the main concern and we don't need to preserve the grid, use in-place modification - marking visited cells directly in the grid saves about 67% memory.

# # For extremely large grids that don't fit in memory (millions × millions), we'd need chunking - processing the grid in tiles and using disk-based storage.


# # Variant : Return any path, not necessarily the shortest one

# # Approach : DFS (preferred)

# class Solution:
#     def pathInBinaryMatrix(self, grid: List[List[int]]) -> List[List[int]]:
#         """
#         Find ANY path (not necessarily shortest) using recursive DFS with backtracking.
#         Uses nested DFS function for cleaner code and direct variable access.
#         Does NOT modify the grid.
        
#         TC: O(M×N) - in worst case, explores all cells with backtracking
#         SC: O(M×N) - recursion stack depth + visited set + path list
        
#         Note: Uses DFS instead of BFS because we only need ANY path, not shortest.
#         DFS is simpler and uses less memory than BFS for this use case.
        
#         To return path length instead of path:
#         - Change return type to int
#         - Replace: return [] with return -1
#         - Replace: return [[0, 0]] with return 1
#         - Replace: return path if dfs(0, 0) else [] 
#           with: return len(path) if dfs(0, 0) else -1
        
#         Args:
#             grid: m×n binary matrix where 0 is traversable, 1 is blocked
        
#         Returns:
#             List[List[int]]: Any valid path from (0,0) to (m-1,n-1)
#             [] if no path exists
            
#             For path length: int (length of path or -1 if no path)
#         """
#         # Edge case: empty grid
#         if not grid:
#             return []  # For length: return -1
        
#         # Edge case: empty first row
#         if not grid[0]:
#             return []  # For length: return -1
        
#         # Get grid dimensions
#         m = len(grid)      # Number of rows
#         n = len(grid[0])   # Number of columns
        
#         # Edge case: start or end blocked
#         if grid[0][0] == 1 or grid[m-1][n-1] == 1:
#             return []  # For length: return -1

#         # Edge case: single cell grid
#         if m == 1 and n == 1:
#             return [[0, 0]]  # For length: return 1

#         # Initialize data structures for DFS
#         # Track visited cells to avoid cycles and redundant exploration
#         visited = {(0, 0)}
        
#         # Store current path being explored
#         # Modified during DFS: cells added when exploring, removed when backtracking
#         path = []
        
#         # 8-directional moves (including diagonals)
#         # Format: (row_offset, col_offset)
#         directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
#         def dfs(row, col):
#             """
#             Nested DFS function to find any path from current cell to destination.
#             Has direct access to: grid, m, n, visited, path, directions (closure)
            
#             Args:
#                 row, col: Current cell coordinates
            
#             Returns:
#                 bool: True if path found from this cell to destination, False otherwise
#             """
#             # Add current cell to path
#             path.append([row, col])
            
#             # Base case: reached destination (bottom-right cell)
#             if row == m - 1 and col == n - 1:
#                 return True  # Path found! Keep current path
            
#             # Explore all 8 possible directions from current cell
#             for dr, dc in directions:
#                 nr, nc = row + dr, col + dc  # Calculate neighbor coordinates
                
#                 # Check if neighbor is valid:
#                 # 1. In bounds: 0 <= nr < m and 0 <= nc < n
#                 # 2. Traversable: grid[nr][nc] == 0 (not blocked)
#                 # 3. Unvisited: (nr, nc) not in visited (avoid cycles)
#                 if (0 <= nr < m and 0 <= nc < n and 
#                     grid[nr][nc] == 0 and (nr, nc) not in visited):
                    
#                     # Mark neighbor as visited BEFORE recursive call
#                     # This prevents the neighbor from being visited again in other branches
#                     visited.add((nr, nc))
                    
#                     # Recursively explore from neighbor
#                     if dfs(nr, nc):
#                         return True  # Path found through this neighbor
                    
#                     # Note: We don't remove from visited during backtracking
#                     # This is intentional - once explored and didn't lead to destination,
#                     # no need to explore it again from a different path
            
#             # Backtracking: No valid path found from current cell
#             # Remove current cell from path since it's not part of solution
#             path.pop()
#             return False  # Signal to caller that this path doesn't work
        
#         # Start DFS from (0, 0)
#         # If DFS returns True, path contains the solution
#         # If DFS returns False, no path exists
#         return path if dfs(0, 0) else []
#         # For length: return len(path) if dfs(0, 0) else -1

# # Iterative DFS

# class Solution:
#     def pathInBinaryMatrix(self, grid: List[List[int]]) -> List[List[int]]:
#         """
#         Find ANY path (not necessarily shortest) using iterative DFS with backtracking.
#         Uses explicit stack instead of recursion.
#         Does NOT modify the grid.
        
#         TC: O(M×N) - in worst case, explores all cells with backtracking
#         SC: O(M×N) - stack + visited set + path list
        
#         Note: Uses iterative DFS instead of recursive to avoid stack overflow
#         for very large grids. Still finds ANY path, not necessarily shortest.
        
#         Args:
#             grid: m×n binary matrix where 0 is traversable, 1 is blocked
        
#         Returns:
#             List[List[int]]: Any valid path from (0,0) to (m-1,n-1)
#             [] if no path exists
            
#             For path length: int (length of path or -1 if no path)
#         """
#         # Edge case: empty grid
#         if not grid:
#             return []  # For length: return -1
        
#         # Edge case: empty first row
#         if not grid[0]:
#             return []  # For length: return -1
        
#         # Get grid dimensions
#         m = len(grid)      # Number of rows
#         n = len(grid[0])   # Number of columns
        
#         # Edge case: start or end blocked
#         if grid[0][0] == 1 or grid[m-1][n-1] == 1:
#             return []  # For length: return -1

#         # Edge case: single cell grid
#         if m == 1 and n == 1:
#             return [[0, 0]]  # For length: return 1

#         # Initialize data structures for iterative DFS
#         # Stack stores: (row, col, path_so_far)
#         # path_so_far is the path taken to reach this cell
#         stack = [(0, 0, [[0, 0]])]
        
#         # Track visited cells to avoid cycles
#         visited = {(0, 0)}
        
#         # 8-directional moves (including diagonals)
#         directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
#         while stack:
#             row, col, path = stack.pop()
            
#             # Check if reached destination (bottom-right cell)
#             if row == m - 1 and col == n - 1:
#                 return path  # Found a path! For length: return len(path)
            
#             # Explore all 8 possible directions from current cell
#             for dr, dc in directions:
#                 nr, nc = row + dr, col + dc  # Calculate neighbor coordinates
            
#                 if (0 <= nr < m and 0 <= nc < n and 
#                     grid[nr][nc] == 0 and (nr, nc) not in visited):
                    
#                     visited.add((nr, nc))
                    
#                     new_path = path + [[nr, nc]]
                    
#                     # Push neighbor onto stack with its path
#                     stack.append((nr, nc, new_path))
        
#         # Stack exhausted without finding destination - no path exists
#         return []  # For length: return -1

# # Using parent tracking

# class SolutionOptimized:
#     def pathInBinaryMatrix(self, grid: List[List[int]]) -> List[List[int]]:
#         """
#         Space-optimized iterative DFS using parent tracking instead of storing paths.
#         Reconstructs path only when destination found.
        
#         TC: O(M×N)
#         SC: O(M×N) - more efficient than storing full paths in stack
        
#         Advantage: Uses less memory by storing only parent relationships,
#         not full path copies for each stack entry.
#         """
#         if not grid or not grid[0]:
#             return []  # For length: return -1
        
#         m, n = len(grid), len(grid[0])
        
#         if grid[0][0] == 1 or grid[m-1][n-1] == 1:
#             return []  # For length: return -1
        
#         if m == 1 and n == 1:
#             return [[0, 0]]  # For length: return 1

#         # Stack stores only coordinates (not full paths)
#         stack = [(0, 0)]
#         visited = {(0, 0)}
#         parent = {(0, 0): None}  # Track parent for path reconstruction
        
#         directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
#         while stack:
#             row, col = stack.pop()  # Only coordinates, not path
            
#             # Check if reached destination
#             if row == m - 1 and col == n - 1:
#                 # Reconstruct path by backtracking through parents
#                 return self.reconstruct_path(parent, (row, col))
#                 # For length: return self.get_path_length(parent, (row, col))
            
#             for dr, dc in directions:
#                 nr, nc = row + dr, col + dc
                
#                 if (0 <= nr < m and 0 <= nc < n and 
#                     grid[nr][nc] == 0 and (nr, nc) not in visited):
                    
#                     visited.add((nr, nc))
#                     parent[(nr, nc)] = (row, col)  # Record parent
#                     stack.append((nr, nc))  # Only coordinates
        
#         return []  # For length: return -1
    
#     def reconstruct_path(self, parent: dict, end: tuple) -> List[List[int]]:
#         """
#         Reconstruct path by backtracking through parent pointers.
        
#         TC: O(path_length)
#         SC: O(path_length)
#         """
#         path = []
#         current = end
        
#         # Backtrack from end to start
#         while current is not None:
#             path.append(list(current))
#             current = parent[current]
        
#         # Reverse to get start -> end order
#         return path[::-1]
    
#     def get_path_length(self, parent: dict, end: tuple) -> int:
#         """
#         Calculate path length by counting parent hops.
#         Use this method instead of reconstruct_path() to return length.
        
#         TC: O(path_length)
#         SC: O(1) - only uses a counter
#         """
#         length = 0
#         current = end
        
#         # Count hops back to start (parent = None)
#         while current is not None:
#             length += 1
#             current = parent[current]
        
#         return length

# Approach : DFS with in cell modification

# def pathInBinaryMatrix(grid):
#     n = len(grid)

#     if not grid or grid[0][0] == 1 or grid[n-1][n-1] == 1:
#         return []

#     # Single cell grid
#     if n == 1:
#         return [(0,0)]
    
#     directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
#     path = []
    
#     def dfs(row, col):
#         path.append([row, col])
#         if row == n - 1 and col == n - 1:
#             return True
        
#         # Mark as visited in-place
#         grid[row][col] = -1
        
#         for dr, dc in directions:
#             nr, nc = row + dr, col + dc
#             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
#                 if dfs(nr, nc):
#                     return True
        
#         # Backtrack
#         path.pop()
#         # Optional: restore grid value if you want to preserve grid (comment out if not needed)
#         # grid[row][col] = 0
#         return False
    
#     return path if dfs(0, 0) else []




