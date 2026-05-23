"""
LeetCode 827. Making A Large Island
Difficulty: Hard
URL: https://leetcode.com/problems/making-a-large-island/
"""

# Check the BFS approach and the DSU solution

# Brute force

# The brute force approach would be to try flipping each 0 to 1, run DFS from that position to count the resulting island size, then flip it back. We'd track the maximum size across all attempts.

# Complexity
# Time Complexity: O(n² × m²) ~ O(n^4) when n = m

# Iterate through all cells: O(n×m)
# For each 0, run DFS: O(n×m)
# Total: O(n×m) × O(n×m) = O(n² × m²)

# Space Complexity: O(n×m) ~ O(n^2) when n = m

# Visited array: O(n×m)
# DFS recursion stack: O(n×m)


# Approach : DFS

class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        """

        APPROACH:
        ---------
        1. Label all islands with unique IDs (2, 3, 4, ...) and store their sizes
        2. For each 0, check which islands it touches and calculate potential size
        3. Return maximum size found

        
        TIME COMPLEXITY: O(n²)
        ----------------------
        - Phase 1 (Island labeling with DFS): Visit each cell once = O(n²)
        - Each land cell is labeled exactly once across all DFS calls
        - Once a cell is labeled (changed from 1 to island_id), it is never processed again
        
        - Phase 2 (Check each 0 for flipping): Check each cell and its neighbors = O(n²)
        - For each 0, check at most 4 neighboring cells
        - Set operations (add, membership check) are O(1)
        - Summing adjacent island sizes from set is O(4) = O(1) in worst case
        
        - Total: O(n²) + O(n²) = O(n²)

        Worst case examples:
        - All land (one giant island):
        Still O(n²) because every cell is visited once
        Example (n=3):
        [[1,1,1],
        [1,1,1],
        [1,1,1]]
        Phase 1: DFS visits all 9 cells once
        Phase 2: No 0s to check
        
        - Many small islands (checkerboard pattern):
        Still O(n²) because each cell is processed constant times
        Example (n=4):
        [[1,0,1,0],
        [0,1,0,1],
        [1,0,1,0],
        [0,1,0,1]]
        Phase 1: 8 separate DFS calls, but total visits = 8 cells
        Phase 2: Check 8 water cells, each examines 4 neighbors = 32 checks = O(n²)
        
        - Snake-shaped island:
        Still O(n²) because DFS visits each cell once
        Example (n=5):
        [[1,1,1,1,1],
        [0,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,1]]
        DFS traverses 21 cells in one call, but each cell visited once

        SPACE COMPLEXITY: O(n²)
        -----------------------
        Worst case is O(n²), but comes from DIFFERENT sources depending on grid:

        Components:

        1. island_sizes dictionary: O(k) where k = number of islands
        - Best case: O(1)
            No islands (all water):
            [[0,0],
            [0,0]]
            → island_sizes = {}
            
            Single island (all land):
            [[1,1],
            [1,1]]
            → island_sizes = {2: 4}
            
        - Worst case: O(n²) asymptotically
            Checkerboard pattern has n²/2 islands
            Example (n=4, 16 cells, 8 islands):
            [[1,0,1,0],
            [0,1,0,1],
            [1,0,1,0],
            [0,1,0,1]]
            → island_sizes = {2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1}
            ← Dictionary dominates: O(n²), Stack is O(1)
            
        2. DFS recursion stack: Depth = longest path in DFS traversal
        - Best case: O(1) when no land exists
            [[0,0],
            [0,0]]
            → No DFS calls made
            
        - Typical case: O(n) for compact, roughly square-shaped islands
            [[1,1],
            [1,1]]
            → Stack depth ≈ 2 or 3 levels (much less than 4)
            
        - Worst case: O(n²) for a snake-like island spanning entire grid
            Example (n=3, snake has 7 land cells):
            [[1,1,1],
            [0,0,1],
            [1,1,1]]
            → Stack depth reaches 7 (linear path through all land cells)
            → DFS is recursive: each call adds frame to stack
            → Doesn't return until path is fully explored
            ← Recursion stack dominates: O(n²), Dictionary is O(1)
            
            Stack depth visualization (n=2 example for clarity):
            
            Grid:      Positions:     DFS explores in order (one possible path):
            [1, 1]     [(0,0) (0,1)]  (0,0) → (0,1) → (1,1) → (1,0)
            [1, 1]     [(1,0) (1,1)]
            
            All 4 cells form one connected island
            
            Stack growth during DFS (assuming directions: up, right, down, left):
            
            Step 1: Start at (0,0)
            Stack: [dfs(0,0)]
            Marked: (0,0)
            
            Step 2: From (0,0), explore right to (0,1)
            Stack: [dfs(0,0), dfs(0,1)]
            Marked: (0,0), (0,1)
            
            Step 3: From (0,1), explore down to (1,1)
            Stack: [dfs(0,0), dfs(0,1), dfs(1,1)]
            Marked: (0,0), (0,1), (1,1)
            
            Step 4: From (1,1), explore left to (1,0)
            Stack: [dfs(0,0), dfs(0,1), dfs(1,1), dfs(1,0)]  ← MAX depth = 4
            Marked: (0,0), (0,1), (1,1), (1,0)
            All 4 cells on stack simultaneously!
            
            Step 5: (1,0) has no unvisited neighbors, returns
            Stack: [dfs(0,0), dfs(0,1), dfs(1,1)]
            
            Step 6: (1,1) has no more unvisited neighbors, returns
            Stack: [dfs(0,0), dfs(0,1)]
            
            Step 7: (0,1) has no more unvisited neighbors, returns
            Stack: [dfs(0,0)]
            
            Step 8: (0,0) has no more unvisited neighbors, returns
            Stack: []  ← Done
            
            Maximum stack depth = 4 (at Step 4) = n² for this 2×2 grid
            
            Key insight: In worst case (linear/snake path), all n² cells 
            can be on the recursion stack simultaneously before any return!
            
            For larger snake example (n=3): [[1,1,1], [0,0,1], [1,1,1]]
            - 7 land cells in snake path: (0,0)→(0,1)→(0,2)→(1,2)→(2,2)→(2,1)→(2,0)
            - Maximum stack depth = 7 frames
            - General pattern: stack depth = number of cells in longest path ≤ n²
            
        3. Grid modification: O(1) extra space
        - Islands are labeled in-place (1 → 2, 3, 4, ...)
        - No additional grid copy needed

        Overall worst-case space complexity: O(n²)
        - Scenario 1 (Checkerboard): Dictionary = O(n²), Stack = O(1) → Total O(n²)
        - Scenario 2 (Snake island): Dictionary = O(1), Stack = O(n²) → Total O(n²)
        - Both scenarios reach O(n²), just from different components!
        """
        n = len(grid)
        
        # Four directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # ============================================================
        # PHASE 1: Label each island with unique ID and calculate size
        # ============================================================
        
        # Start island IDs from 2 (since 0=water, 1=unlabeled land)
        island_id = 2
        
        # Dictionary to store: {island_id: size}
        # Example: {2: 5, 3: 3} means island-2 has 5 cells, island-3 has 3 cells
        island_sizes = {}
        
        def dfs(r, c, island_id):
            """
            DFS to explore and label an entire island.
            
            Args:
                r, c: Current cell coordinates
                island_id: The ID to label this island with
            
            Returns:
                The total size of this island
            """
            # Base case: out of bounds or not unlabeled land
            if r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1:
                return 0
            
            # Label this cell with the island ID
            # This also marks it as "visited" so we don't revisit
            grid[r][c] = island_id
            
            # Start counting: this cell counts as 1
            size = 1
            
            # Explore all 4 neighbors and add their contributions
            for dr, dc in directions:
                size += dfs(r + dr, c + dc, island_id)
            
            return size
        
        # Iterate through entire grid to find and label all islands
        for i in range(n):
            for j in range(n):
                # Found unlabeled land (value = 1)
                if grid[i][j] == 1:
                    # Run DFS to label entire island and get its size
                    size = dfs(i, j, island_id)
                    
                    # Store this island's size
                    island_sizes[island_id] = size
                    
                    # Increment ID for next island
                    island_id += 1
        
        # ============================================================
        # EDGE CASE: Grid is all water (no islands found)
        # ============================================================
        # If island_sizes is empty, the entire grid is 0s
        # We can flip one 0 to 1, creating an island of size 1
        if not island_sizes:
            return 1
        
        # ============================================================
        # Initialize max_size with the largest existing island
        # ============================================================
        # This handles the case where grid is all land (no 0s to flip)
        # It also serves as our baseline that we'll try to beat
        max_size = max(island_sizes.values())

        # max_size = 0
        # for val in island_sizes.values():
        #     if val > max_size:
        #         max_size = val
        
        # ============================================================
        # PHASE 2: Try flipping each 0 and calculate potential island size
        # ============================================================
        
        for i in range(n):
            for j in range(n):
                # Only consider water cells (0s) as flip candidates
                if grid[i][j] == 0:
                    # Set to track unique adjacent island IDs
                    # Why set? To avoid counting same island multiple times
                    # Example: If cell touches same island from 2 sides,
                    # we should only count that island once
                    adjacent_islands = set()
                    
                    # Check all 4 neighbors
                    for dr, dc in directions:
                        nr, nc = i + dr, j + dc
                        
                        # If neighbor is within bounds AND is land (ID > 1)
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 1:
                            # Add this island ID to our set
                            adjacent_islands.add(grid[nr][nc])
                    
                    # Calculate potential island size if we flip this 0 to 1
                    # Start with 1 (the flipped cell itself)
                    potential_size = 1
                    
                    # Add the size of each unique adjacent island
                    for island in adjacent_islands:
                        potential_size += island_sizes[island]
                    
                    # Update max if this flip gives us a larger island
                    max_size = max(max_size, potential_size)
                    
                    # if potential_size > max_size:
                    #     max_size = potential_size

        return max_size


# ============================================================
# EXAMPLE WALKTHROUGH
# ============================================================
"""
Input: grid = [[1, 0],
               [0, 1]]

PHASE 1: Labeling
-----------------
Start: grid[0][0] = 1 → DFS labels it as 2
       island_sizes = {2: 1}
       
After: grid = [[2, 0],
               [0, 1]]

Next: grid[1][1] = 1 → DFS labels it as 3
      island_sizes = {2: 1, 3: 1}
      
After: grid = [[2, 0],
               [0, 3]]

max_size = max([1, 1]) = 1

PHASE 2: Flipping
-----------------
Check grid[0][1] = 0:
  - Neighbors: 2 (left), 3 (down)
  - adjacent_islands = {2, 3}
  - potential_size = 1 + 1 + 1 = 3
  - max_size = max(1, 3) = 3

Check grid[1][0] = 0:
  - Neighbors: 2 (up), 3 (right)
  - adjacent_islands = {2, 3}
  - potential_size = 1 + 1 + 1 = 3
  - max_size = max(3, 3) = 3

Output: 3
"""

# Approach : Using visited set

class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        """
        Find the largest island after flipping at most one 0 to 1.
        
        This version uses a VISITED SET instead of modifying the grid in-place.
        
        SPACE COMPLEXITY DIFFERENCE:
        - Grid modification approach: O(1) extra space
        - Visited set approach: O(n²) extra space for visited + island_map
        
        TRADE-OFFS:
        - ✓ Preserves original grid
        - ✗ Uses more memory
        - ✗ More complex code
        
        For full complexity analysis, see grid modification approach.
        """
        n = len(grid)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # ============================================================
        # PHASE 1: Label each island with unique ID and calculate size
        # ============================================================
        
        island_id = 2  # Start from 2 (0=water, 1=land)
        island_sizes = {}  # {island_id: size}
        
        # NEW: Data structures for visited set approach
        visited = set()  # Track visited cells: {(r, c), ...}
        island_map = {}  # Map cell to island ID: {(r, c): island_id}
        
        def dfs(r, c, island_id):
            """
            DFS to explore and label an entire island using visited set.
            
            Args:
                r, c: Current cell coordinates
                island_id: The ID to label this island with
            
            Returns:
                The total size of this island
            """
            # Base case: out of bounds, already visited, or not land
            if r < 0 or r >= n or c < 0 or c >= n or (r, c) in visited or grid[r][c] != 1:
                return 0
            
            # Mark this cell as visited (replaces grid modification)
            visited.add((r, c))
            
            # Store which island this cell belongs to (needed for Phase 2)
            island_map[(r, c)] = island_id
            
            # Start counting: this cell counts as 1
            size = 1
            
            # Explore all 4 neighbors and add their contributions
            for dr, dc in directions:
                size += dfs(r + dr, c + dc, island_id)
            
            return size
        
        # Iterate through entire grid to find and label all islands
        for i in range(n):
            for j in range(n):
                # Found unlabeled land that hasn't been visited
                if grid[i][j] == 1 and (i, j) not in visited:
                    # Run DFS to label entire island and get its size
                    size = dfs(i, j, island_id)
                    
                    # Store this island's size
                    island_sizes[island_id] = size
                    
                    # Increment ID for next island
                    island_id += 1
        
        # ============================================================
        # EDGE CASE: Grid is all water (no islands found)
        # ============================================================
        if not island_sizes:
            return 1
        
        # ============================================================
        # Initialize max_size with the largest existing island
        # ============================================================
        max_size = max(island_sizes.values())
        
        # ============================================================
        # PHASE 2: Try flipping each 0 and calculate potential island size
        # ============================================================
        
        for i in range(n):
            for j in range(n):
                # Only consider water cells (0s) as flip candidates
                if grid[i][j] == 0:
                    # Set to track unique adjacent island IDs
                    adjacent_islands = set()
                    
                    # Check all 4 neighbors
                    for dr, dc in directions:
                        nr, nc = i + dr, j + dc
                        
                        # Check if neighbor cell belongs to an island
                        # (lookup in island_map instead of checking grid value)
                        if (nr, nc) in island_map:
                            # Add this island ID to our set
                            adjacent_islands.add(island_map[(nr, nc)])
                    
                    # Calculate potential island size if we flip this 0 to 1
                    potential_size = 1  # The flipped cell itself
                    
                    # Add the size of each unique adjacent island
                    for island in adjacent_islands:
                        potential_size += island_sizes[island]
                    
                    # Update max if this flip gives us a larger island
                    max_size = max(max_size, potential_size)
        
        return max_size


# ============================================================
# KEY INTERVIEW POINTS TO REMEMBER
# ============================================================
"""
1. WHY start island_id from 2?
   - 0 = water
   - 1 = unlabeled land
   - 2+ = labeled islands with unique IDs

2. WHY use a set for adjacent_islands?
   - Prevents double-counting if same island touches from multiple sides
   
3. WHAT if entire grid is water?
   - island_sizes will be empty
   - Return 1 (flip one cell)
   
4. WHAT if entire grid is land?
   - No 0s to check in Phase 2
   - max_size already has correct answer from Phase 1
   
5. TIME COMPLEXITY breakdown:
   - Phase 1 (DFS labeling): O(n²) - visit each cell once
   - Phase 2 (check 0s): O(n²) - visit each cell once, constant work per cell
   - Total: O(n²) + O(n²) = O(n²)
   
6. SPACE COMPLEXITY breakdown:
   - island_sizes dictionary: O(k) where k = number of islands ≤ n²
   - DFS call stack: O(n²) worst case (snake-like island)
   - Total: O(n²)
"""

# Variant : You are given an n × m binary matrix grid. You can change as many 0's to 1's as long as they do not touch other islands. All 4 directions should be considered. Return the size of the largest island that can be created in the grid. An island is a 4-directionally connected group of 1s.

# Example 1:

# Input: grid = [
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0],
#     [1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0]
# ]

# Visual:
# W L W L W
# W W W W W
# L L L L L
# W W W W W
# (W = Water, L = Land)

# Output: 5
# Explanation:

# Existing islands: (0,1) size 1, (0,3) size 1, middle row size 5
# All water cells border at least one existing land cell → Cannot be converted
# Answer: Largest existing island = 5

# class Solution:
#     def largestIslandVariant(self, grid: List[List[int]]) -> int:
#         """
#         Find the largest island that can be created by converting 0s to 1s,
#         where new 1s cannot touch existing islands.
        
#         APPROACH:
#         ---------
#         We need to find the maximum between:
#         1. Existing land islands (already in the grid)
#         2. Water regions that can be converted (don't border any land)
        
#         ALGORITHM:
#         ----------
#         Phase 1: Use DFS to find and measure all existing LAND islands
#         Phase 2: Use DFS to find and measure all WATER regions that don't touch land
#         Return the maximum size found
        
#         TIME COMPLEXITY: O(n*m)
#         - Phase 1: Visit each cell once for land islands = O(n*m)
#         - Phase 2: Visit each cell once for water regions = O(n*m)
#         - Total: O(n*m) + O(n*m) = O(n*m)
        
#         SPACE COMPLEXITY: O(n*m)
#         - Two visited arrays: 2 * O(n*m) = O(n*m)
#         - DFS recursion stack: O(n*m) in worst case (entire grid connected)
#         - Total: O(n*m)
#         """

#         if not grid or not grid[0]:
#             return 0
        
#         # ============================================================
#         # SETUP
#         # ============================================================
#         n, m = len(grid), len(grid[0])
        
#         # Four directions: up, right, down, left
#         # Used to explore neighbors in DFS
#         directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
#         # Track the largest island size found so far
#         largest = 0
        
#         # ============================================================
#         # DFS HELPER FUNCTION
#         # ============================================================
#         def dfs(row, col, target, visited):
#             """
#             Depth-First Search to count the size of a connected region.
            
#             This function works for BOTH land islands and water regions by using
#             the 'target' parameter to specify what we're looking for.
            
#             PARAMETERS:
#             -----------
#             row, col : int
#                 Current cell coordinates to explore
            
#             target : int
#                 The value we're searching for:
#                 - target = 1: Count connected LAND cells (existing islands)
#                 - target = 0: Count connected WATER cells (potential new islands)
            
#             visited : List[List[bool]]
#                 2D array tracking which cells we've already explored
#                 Prevents infinite loops and double-counting
            
#             RETURNS:
#             --------
#             int : Size of the connected region starting from (row, col)
#                   Returns 0 if the cell cannot be included
            
#             KEY LOGIC:
#             ----------
#             For LAND (target=1):
#                 - Simply count all connected 1s
#                 - No special restrictions
            
#             For WATER (target=0):
#                 - Only count water cells that DON'T border any land
#                 - This ensures converted water won't touch existing islands
#                 - Water cells touching land return 0 (excluded from region)
#             """
            
#             # ========================================
#             # BASE CASE 1: Out of Bounds Check
#             # ========================================
#             # If we've gone outside the grid, stop exploring this path
#             if row < 0 or row >= n or col < 0 or col >= m:
#                 return 0
            
#             # ========================================
#             # BASE CASE 2: Already Visited Check
#             # ========================================
#             # If we've already explored this cell, don't count it again
#             # Prevents infinite loops in the recursion
#             if visited[row][col]:
#                 return 0
            
#             # ========================================
#             # BASE CASE 3: Wrong Value Check
#             # ========================================
#             # If this cell doesn't have the value we're looking for, skip it
#             # Example: If target=1 (looking for land), but grid[row][col]=0 (water)
#             if grid[row][col] != target:
#                 return 0
            
#             # ========================================
#             # SPECIAL CASE: Water Border Check
#             # ========================================
#             # This is ONLY for water cells (target=0)
#             # Check if this water cell is adjacent to any land cell
#             # If yes, we CANNOT convert it (would violate "don't touch islands" rule)
#             if target == 0:
#                 # Check all 4 neighbors of this water cell
#                 for dr, dc in directions:
#                     nr, nc = row + dr, col + dc
                    
#                     # Combined check: in bounds AND is land
#                     if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
#                         return 0  # ← EXIT! Cannot convert this water cell
            
#             # ========================================
#             # MAIN DFS LOGIC
#             # ========================================
#             # At this point, we know:
#             # 1. Cell is in bounds
#             # 2. Cell hasn't been visited yet
#             # 3. Cell has the target value we're looking for
#             # 4. If it's water, it doesn't border any land
#             # Therefore, this cell CAN be included in the region!
            
#             # Mark this cell as visited so we don't explore it again
#             visited[row][col] = True
            
#             # Count this cell (starts at 1)
#             size = 1
            
#             # ========================================
#             # RECURSIVE EXPLORATION
#             # ========================================
#             # Explore all 4 neighbors (up, right, down, left)
#             # Each recursive call returns the size of the connected region in that direction
#             for dr, dc in directions:
#                 neighbor_row = row + dr
#                 neighbor_col = col + dc
                
#                 # Recursively explore the neighbor
#                 # Add whatever size is found in that direction
#                 size += dfs(neighbor_row, neighbor_col, target, visited)
            
#             # Return the total size of this connected region
#             return size
        
#         # ============================================================
#         # PHASE 1: COUNT ALL EXISTING LAND ISLANDS
#         # ============================================================
#         # Purpose: Find all islands that already exist in the grid
#         # Why: These are valid answers! The largest existing island might be our answer
#         # Target: grid cells with value = 1
        
#         # Create a fresh visited array for Phase 1
#         # All cells start as False (unvisited)
#         visited = [[False] * m for _ in range(n)]
        
#         # Scan through every cell in the grid
#         for row in range(n):
#             for col in range(m):
#                 # Check if this cell is:
#                 # 1. Land (grid[row][col] == 1)
#                 # 2. Not yet visited (not visited[row][col])
#                 if grid[row][col] == 1 and not visited[row][col]:
#                     # Found the start of a new land island!
#                     # Use DFS to explore and count the entire island
#                     island_size = dfs(row, col, target=1, visited=visited)
                    
#                     # Update largest if this island is bigger than what we've seen
#                     largest = max(largest, island_size)
                    
#                     # Note: The visited array now has True for all cells in this island
#                     # So we won't re-explore them in future loop iterations
        
#         # After Phase 1:
#         # - All land islands have been found and measured
#         # - 'largest' contains the size of the biggest land island
#         # - 'visited' array has marked all land cells as True
        
#         # ============================================================
#         # PHASE 2: COUNT WATER REGIONS THAT DON'T BORDER LAND
#         # ============================================================
#         # Purpose: Find water regions that can be safely converted to land
#         # Why: Converting these creates new islands, which might be larger than existing ones
#         # Target: grid cells with value = 0 that don't touch any land
        
#         # Scan through every cell in the grid again
#         for row in range(n):
#             for col in range(m):
#                 # Check if this cell is:
#                 # 1. Water (grid[row][col] == 0)
#                 # 2. Not yet visited (not visited[row][col])
#                 if grid[row][col] == 0 and not visited[row][col]:
#                     # Found a water cell we haven't explored yet!
#                     # Use DFS to explore this water region
#                     # 
#                     # Important: dfs will return 0 if this water borders land
#                     # (the borders_land check inside dfs handles this)
#                     # 
#                     # If the water doesn't border land, dfs returns the region size
#                     water_size = dfs(row, col, target=0, visited=visited)
                    
#                     # Update largest if this water region is bigger
#                     # Note: If water_size=0 (borders land), max doesn't change
#                     largest = max(largest, water_size)
        
#         # After Phase 2:
#         # - All convertible water regions have been found and measured
#         # - 'largest' now contains the maximum between:
#         #   * Largest existing land island (from Phase 1)
#         #   * Largest convertible water region (from Phase 2)
        
#         # ============================================================
#         # RETURN THE ANSWER
#         # ============================================================
#         return largest

# ============================================================
# EXAMPLE WALKTHROUGH
# ============================================================

# Input: grid = [[1, 0, 0, 0],
#                [0, 0, 0, 0],
#                [0, 0, 0, 1]]

# Visual:
#   L  W  W  W
#   W  W  W  W
#   W  W  W  L

# PHASE 1: Largest Land Island
# -----------------------------
# Scan for grid[r][c] == 1, run DFS:

#   (0,0) = 1 → DFS → size 1, largest = 1
#   (2,3) = 1 → DFS → size 1, largest = 1

# PHASE 2: Largest Convertible Water Region
# ------------------------------------------
# Scan for grid[r][c] == 0, skip if any neighbor == 1:

#   (0,1): neighbor (0,0)=1 → ❌ skip
#   (0,2): neighbors (0,1)=0, (0,3)=0, (1,2)=0 → ✅ DFS starts
#          explores (0,3): neighbors (0,2)=0, (1,3)=0 → ✅
#          explores (1,1): neighbors (0,1)=0, (1,0)=0, (1,2)=0, (2,1)=0 → ✅
#          explores (1,2): neighbors (0,2)=0, (1,1)=0, (1,3)=0, (2,2)=0 → ✅
#          explores (2,0): neighbors (1,0)=0, (2,1)=0 → ✅
#          explores (2,1): neighbors (1,1)=0, (2,0)=0, (2,2)=0 → ✅
#          (1,0): neighbor (0,0)=1 → ❌ skip
#          (1,3): neighbor (2,3)=1 → ❌ skip
#          (2,2): neighbor (2,3)=1 → ❌ skip
#          water region = {(0,2),(0,3),(1,1),(1,2),(2,0),(2,1)} → size 6
#          largest = max(1, 6) = 6

# Output: 6

# Variant: You are given an n × m binary matrix grid. Find the size of the largest water region that doesn't border any existing land. Water cells (0s) that are adjacent to any land cell (1s) in the 4 directions are not counted. Return the size of the largest isolated water region in the grid. Return 0 if no such region exists.

# Example
# Input:

# grid = [
#     [1, 1, 1],
#     [1, 1, 1],
#     [0, 0, 0]
# ]

# Visual:

# L L L
# L L L
# W W W

# Output: 0

# Explanation:

# Check water cells in bottom row:

# (2,0): Borders land at (1,0) → Cannot count ❌
# (2,1): Borders land at (1,1) → Cannot count ❌
# (2,2): Borders land at (1,2) → Cannot count ❌


# No isolated water region exists
# Answer: 0

# For the previous variant, output will be 6 since we are finding the size of the largest island that can be created in the grid.

# class Solution:
#     def largestIslandVariantNoLand(self, grid: List[List[int]]) -> int:
#         """
#         Find the largest island that can be created by converting water regions
#         that DON'T border any existing land.
        
#         ❌ LIMITATION: Only counts convertible water regions.
#         Does NOT count existing land islands.
        
#         APPROACH:
#         ---------
#         Single Phase: Find water regions that don't touch any land
        
#         TIME COMPLEXITY: O(n*m)
#         - Visit each cell once during main loop
#         - DFS explores each water cell at most once
        
#         SPACE COMPLEXITY: O(n*m)
#         - visited array: O(n*m)
#         - DFS recursion stack: O(n*m) worst case
#         """
        
#         n, m = len(grid), len(grid[0])
#         directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
#         largest = 0
        
#         def dfs(row, col, visited):
#             """
#             Count water cells that don't border land using DFS.
            
#             Args:
#                 row, col: Current position
#                 visited: 2D array tracking explored cells
            
#             Returns:
#                 Size of convertible water region, or 0 if:
#                 - Out of bounds
#                 - Already visited
#                 - Not water
#                 - Borders any land
#             """
#             # Out of bounds
#             if row < 0 or row >= n or col < 0 or col >= m:
#                 return 0
            
#             # Already visited or not water
#             if visited[row][col] or grid[row][col] != 0:
#                 return 0
            
#             # Check if this water cell borders any land
#             for dr, dc in directions:
#                 nr, nc = row + dr, col + dc
#                 if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
#                     return 0  # Water borders land, cannot convert
            
#             # Mark visited and count this cell
#             visited[row][col] = True
#             size = 1
            
#             # Explore all 4 neighbors
#             for dr, dc in directions:
#                 size += dfs(row + dr, col + dc, visited)
            
#             return size
        
#         # Single Phase: Find convertible water regions
#         visited = [[False] * m for _ in range(n)]
        
#         for row in range(n):
#             for col in range(m):
#                 # Skip all land cells (never count them)
#                 if grid[row][col] == 1:
#                     continue
                
#                 # Process unvisited water cells
#                 if not visited[row][col]:
#                     water_size = dfs(row, col, visited)
#                     largest = max(largest, water_size)
        
#         return largest