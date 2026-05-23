"""
LeetCode 489. Robot Room Cleaner
Difficulty: Hard
URL: https://leetcode.com/problems/robot-room-cleaner/
"""

# """
# This is the robot's control interface.
# You should not implement it, or speculate about its implementation
# """
class Robot:
   def move(self):
       """
       Returns true if the cell in front is open and robot moves into the cell.
       Returns false if the cell in front is blocked and robot stays in the current cell.
       :rtype bool
       """

   def turnLeft(self):
       """
       Robot will stay in the same cell after calling turnLeft/turnRight.
       Each turn will be 90 degrees.
       :rtype void
       """

   def turnRight(self):
       """
       Robot will stay in the same cell after calling turnLeft/turnRight.
       Each turn will be 90 degrees.
       :rtype void
       """

   def clean(self):
       """
       Clean the current cell.
       :rtype void
       """

class Robot:
    """
    Mock Robot interface for local testing.
    Simulates the robot API provided by LeetCode.
    """
    
    def __init__(self, room: list[list[int]], row: int, col: int):
        """
        Args:
            room: 2D grid where 1 = accessible, 0 = blocked
            row:  Robot's starting row
            col:  Robot's starting col
        """
        self.room = room
        self.row = row
        self.col = col
        self.direction = 0  # 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
        self.cleaned = set()
        
        # Direction vectors: UP, RIGHT, DOWN, LEFT (clockwise)
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def move(self) -> bool:
        """
        Move robot one step in current facing direction.
        Returns True if move succeeded, False if blocked or out of bounds.
        """
        dr, dc = self.directions[self.direction]
        new_row = self.row + dr
        new_col = self.col + dc
        
        # Check bounds and accessibility
        if (0 <= new_row < len(self.room) and
            0 <= new_col < len(self.room[0]) and
            self.room[new_row][new_col] == 1):
            self.row = new_row
            self.col = new_col
            return True
        return False
    
    def turnRight(self) -> None:
        """Rotate robot 90° clockwise."""
        self.direction = (self.direction + 1) % 4
    
    def turnLeft(self) -> None:
        """Rotate robot 90° counter-clockwise."""
        self.direction = (self.direction - 1) % 4
    
    def clean(self) -> None:
        """Clean current cell."""
        self.cleaned.add((self.row, self.col))
    
    def get_cleaned(self) -> set:
        """Helper for testing: returns all cleaned cells (actual coordinates)."""
        return self.cleaned


class Solution:
    def cleanRoom(self, robot):
        """
        Clean entire room using robot with limited API.
        
        ============================================================
        COMPLEXITY ANALYSIS - INTERPRETATION 1 (STANDARD)
        ============================================================
        When N = number of rows, M = number of columns:
        
        Time Complexity: O(N × M)
            - Visit each accessible cell exactly once
            - O(1) work per cell (try 4 directions)
            - Total: O(N × M)
        
        Space Complexity: O(N × M)
            - visited set: O(N × M) in worst case (no obstacles)
            - Recursion stack: O(N × M) depth in worst case
            - Total: O(N × M)
        
        ============================================================
        COMPLEXITY ANALYSIS - INTERPRETATION 2 (ALTERNATIVE)
        ============================================================
        When N = total cells, M = number of obstacles:
        
        Time Complexity: O(N - M)
            - N = total cells in grid
            - M = number of obstacles
            - Visit each accessible cell once: N - M cells
            - Total: O(N - M)
        
        Space Complexity: O(N - M)
            - visited set: O(N - M) accessible cells
            - Recursion stack: O(N - M) depth
            - Total: O(N - M)
        
        ============================================================
        NOTE: Both interpretations are equivalent!
        Use Interpretation 1 (O(N × M)) for interviews - it's standard.
        ============================================================
        
        :type robot: Robot
        :rtype: None
        """
        
        # WHY RELATIVE COORDINATES INSTEAD OF ACTUAL ONES?
        # =================================================
        # The problem description shows: room, row, col in the example input,
        # which might suggest we have access to the robot's actual position.
        #
        # However, the actual function signature is:
        #
        #     def cleanRoom(self, robot):   ← no room, no row, no col
        #
        # The judge uses room/row/col internally to simulate robot.move()
        # (checking if the next cell is accessible), but your code never
        # receives them. The only API available is:
        #
        #     robot.move()      → returns True/False (moved or blocked)
        #     robot.clean()     → cleans current cell
        #     robot.turnRight() → rotates 90° clockwise
        #     robot.turnLeft()  → rotates 90° counter-clockwise
        #
        # So actual coordinates are unknowable from inside your function.
        # We pick (0, 0) as the robot's starting position and track all
        # movement as offsets from that origin — giving us a consistent
        # label per cell to answer the only question we need:
        #
        #     "Have I visited this cell before?"
        #
        # Relative coordinates do exactly that, without needing real-world position.
        
        # Direction vectors: UP, RIGHT, DOWN, LEFT (clockwise)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Track visited cells using relative coordinates
        # We don't know actual position, so we start from (0, 0) as origin
        visited = set()
        
        def backtrack(row, col, direction):
            """
            DFS with backtracking to clean all accessible cells.
            
            Args:
                row, col: Current position in relative coordinates
                direction: Current facing (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT)
            """
            
            # Clean current cell and mark as visited
            robot.clean()
            visited.add((row, col))
            
            # Try all 4 directions in clockwise order
            for i in range(4):
                # Calculate new direction using clockwise rotation
                # 
                # How (direction + i) % 4 works:
                # ================================
                # The loop variable i goes from 0 to 3
                # We add i to current direction and mod by 4 to wrap around
                # 
                # Example: If currently facing UP (direction = 0):
                #   i=0: (0+0)%4 = 0 → UP     (try current direction first)
                #   i=1: (0+1)%4 = 1 → RIGHT  (turn right once)
                #   i=2: (0+2)%4 = 2 → DOWN   (turn right twice = opposite)
                #   i=3: (0+3)%4 = 3 → LEFT   (turn right three times)
                # 
                # Example: If currently facing RIGHT (direction = 1):
                #   i=0: (1+0)%4 = 1 → RIGHT  (try current direction first)
                #   i=1: (1+1)%4 = 2 → DOWN   (turn right once)
                #   i=2: (1+2)%4 = 3 → LEFT   (turn right twice = opposite)
                #   i=3: (1+3)%4 = 4%4 = 0 → UP (turn right three times, wraps around)
                # 
                # Example: If currently facing DOWN (direction = 2):
                #   i=0: (2+0)%4 = 2 → DOWN   (try current direction first)
                #   i=1: (2+1)%4 = 3 → LEFT   (turn right once)
                #   i=2: (2+2)%4 = 4%4 = 0 → UP (turn right twice = opposite, wraps around)
                #   i=3: (2+3)%4 = 5%4 = 1 → RIGHT (turn right three times, wraps around)
                # 
                # Pattern: Starting from ANY direction, we always explore:
                #   current → clockwise → opposite → counter-clockwise
                # 
                # Why % 4? Because we have 4 directions (0,1,2,3) and need to wrap:
                #   direction 3 + 1 = 4, but 4%4 = 0 (wraps back to UP)
                #   direction 3 + 2 = 5, but 5%4 = 1 (wraps to RIGHT)
                new_direction = (direction + i) % 4

                # Get the new position
                new_row = row + directions[new_direction][0]
                new_col = col + directions[new_direction][1]
                
                # Move if cell not visited and accessible

                # WHY THIS ORDER: (not in visited) checked BEFORE robot.move()
                # ===============================================================
                # Short-circuit evaluation means if (new_row, new_col) is already
                # visited, robot.move() is never called — avoiding physically moving
                # the robot into a cleaned cell, which would break backtracking state.
                #
                # Swapping the order to: robot.move() and (new_row, new_col) not in visited
                # would move the robot first, then realize the cell was already visited —
                # wasting an API call and leaving the robot in the wrong position.
                #
                # NO OTHER BASE CHECKS NEEDED:
                # ===============================================================
                # - Bounds/obstacle checks: handled by robot.move() returning False
                # - Empty grid:             guaranteed non-empty by constraints
                # - Start on valid cell:    guaranteed room[row][col] == 1
                # - All directions blocked: loop simply ends, recursion unwinds naturally
                if (new_row, new_col) not in visited and robot.move():
                    # Recursively clean from new position
                    backtrack(new_row, new_col, new_direction)
                    
                    # Backtrack: return to previous position and direction
                    # Turn 180° (2 right turns)
                    robot.turnRight()
                    robot.turnRight()
                    # Move back
                    robot.move()
                    # Turn 180° again to restore original direction
                    robot.turnRight()
                    robot.turnRight()
                
                # Turn right to try next direction (ensures clockwise exploration)
                robot.turnRight()
        
        # Start from (0, 0) facing UP
        # We use relative coordinates since actual position is unknown
        backtrack(0, 0, 0)


# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    # Grid from the scenario walkthrough:
    #   Col:  0  1  2
    # Row 0:  0  1  0
    # Row 1:  1  R  1  (Robot starts at row=1, col=1)
    # Row 2:  0  1  0
    room = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
    start_row, start_col = 1, 1

    robot = Robot(room, start_row, start_col)
    solution = Solution()
    solution.cleanRoom(robot)

    # Compute all accessible cells (actual coordinates)
    accessible = {
        (r, c)
        for r in range(len(room))
        for c in range(len(room[0]))
        if room[r][c] == 1
    }

    cleaned = robot.get_cleaned()

    print("Accessible cells:", accessible)
    print("Cleaned cells:   ", cleaned)
    print("All cleaned?     ", accessible == cleaned)


# ============================================================
# Walkthrough Example
# ============================================================
"""
Room:
    Col: 0  1  2
Row 0:   0  1  0
Row 1:   1  R  1  (Robot at 1,1)
Row 2:   0  1  0

Relative coordinates (robot start = origin):
    Col: -1  0  1
Row -1:   0  1  0
Row  0:   1  R  1  <- (0,0)
Row  1:   0  1  0

Accessible cells (relative): (0,0), (-1,0), (0,-1), (0,1), (1,0)
Directions: UP=(-1,0), RIGHT=(0,1), DOWN=(1,0), LEFT=(0,-1)

SCENARIO 1: Start at (0,0), facing UP (direction=0), i=0
============================================================

backtrack(row=0, col=0, direction=0)
    robot.clean()  →  clean (0,0)
    visited = {(0,0)}

    i=0: new_direction = (0+0)%4 = 0  →  UP
         new_row = 0 + (-1) = -1
         new_col = 0 + 0    =  0
         (-1,0) not in visited ✓
         robot.move() → tries to move UP → SUCCESS ✓

         → recurse: backtrack(row=-1, col=0, direction=0)
             robot.clean()  →  clean (-1,0)
             visited = {(0,0), (-1,0)}

             i=0: new_direction = (0+0)%4 = 0  →  UP
                  new_row = -1 + (-1) = -2
                  new_col =  0 +  0  =  0
                  (-2,0) not in visited ✓
                  robot.move() → tries to move UP → BLOCKED ✗
                  robot.turnRight()  →  now facing RIGHT

             i=1: new_direction = (0+1)%4 = 1  →  RIGHT
                  new_row = -1 + 0 = -1
                  new_col =  0 + 1 =  1
                  (-1,1) not in visited ✓
                  robot.move() → tries to move RIGHT → BLOCKED ✗
                  robot.turnRight()  →  now facing DOWN

             i=2: new_direction = (0+2)%4 = 2  →  DOWN
                  new_row = -1 + 1 = 0
                  new_col =  0 + 0 = 0
                  (0,0) IN visited ✗  →  skip
                  robot.turnRight()  →  now facing LEFT

             i=3: new_direction = (0+3)%4 = 3  →  LEFT
                  new_row = -1 + 0  = -1
                  new_col =  0 + (-1) = -1
                  (-1,-1) not in visited ✓
                  robot.move() → tries to move LEFT → BLOCKED ✗
                  robot.turnRight()  →  now facing UP (restored)

         ← backtrack from (-1,0) to (0,0):
             robot.turnRight()   →  facing RIGHT
             robot.turnRight()   →  facing DOWN  (180° turn)
             robot.move()        →  move DOWN back to (0,0)
             robot.turnRight()   →  facing LEFT
             robot.turnRight()   →  facing UP    (restored original direction)

    robot.turnRight()  →  now facing RIGHT (done with i=0)


SCENARIO 2: Back at (0,0), facing RIGHT (direction=1), i=1
============================================================

    i=1: new_direction = (0+1)%4 = 1  →  RIGHT
         new_row = 0 + 0 = 0
         new_col = 0 + 1 = 1
         (0,1) not in visited ✓
         robot.move() → tries to move RIGHT → SUCCESS ✓

         → recurse: backtrack(row=0, col=1, direction=1)
             robot.clean()  →  clean (0,1)
             visited = {(0,0), (-1,0), (0,1)}

             i=0: new_direction = (1+0)%4 = 1  →  RIGHT
                  new_row = 0 + 0 = 0
                  new_col = 1 + 1 = 2
                  (0,2) not in visited ✓
                  robot.move() → tries to move RIGHT → BLOCKED ✗
                  robot.turnRight()  →  now facing DOWN

             i=1: new_direction = (1+1)%4 = 2  →  DOWN
                  new_row = 0 + 1 = 1
                  new_col = 1 + 0 = 1
                  (1,1) not in visited ✓
                  robot.move() → tries to move DOWN → BLOCKED ✗
                  robot.turnRight()  →  now facing LEFT

             i=2: new_direction = (1+2)%4 = 3  →  LEFT
                  new_row = 0 +  0  = 0
                  new_col = 1 + (-1) = 0
                  (0,0) IN visited ✗  →  skip
                  robot.turnRight()  →  now facing UP

             i=3: new_direction = (1+3)%4 = 0  →  UP
                  new_row = 0 + (-1) = -1
                  new_col = 1 +  0  =  1
                  (-1,1) not in visited ✓
                  robot.move() → tries to move UP → BLOCKED ✗
                  robot.turnRight()  →  now facing RIGHT (restored)

         ← backtrack from (0,1) to (0,0):
             robot.turnRight()   →  facing DOWN
             robot.turnRight()   →  facing LEFT  (180° turn)
             robot.move()        →  move LEFT back to (0,0)
             robot.turnRight()   →  facing UP
             robot.turnRight()   →  facing RIGHT (restored original direction)

    robot.turnRight()  →  now facing DOWN (done with i=1)

SCENARIO 3: Back at (0,0), facing DOWN (direction=2), i=2
============================================================

    i=2: new_direction = (0+2)%4 = 2  →  DOWN
         new_row = 0 + 1 = 1
         new_col = 0 + 0 = 0
         (1,0) not in visited ✓
         robot.move() → tries to move DOWN → SUCCESS ✓

         → recurse: backtrack(row=1, col=0, direction=2)
             robot.clean()  →  clean (1,0)
             visited = {(0,0), (-1,0), (0,1), (1,0)}

             i=0: new_direction = (2+0)%4 = 2  →  DOWN
                  new_row = 1 + 1 = 2
                  new_col = 0 + 0 = 0
                  (2,0) not in visited ✓
                  robot.move() → tries to move DOWN → BLOCKED ✗
                  robot.turnRight()  →  now facing LEFT

             i=1: new_direction = (2+1)%4 = 3  →  LEFT
                  new_row = 1 +  0  = 1
                  new_col = 0 + (-1) = -1
                  (1,-1) not in visited ✓
                  robot.move() → tries to move LEFT → BLOCKED ✗
                  robot.turnRight()  →  now facing UP

             i=2: new_direction = (2+2)%4 = 0  →  UP
                  new_row = 1 + (-1) = 0
                  new_col = 0 +  0  = 0
                  (0,0) IN visited ✗  →  skip
                  robot.turnRight()  →  now facing RIGHT

             i=3: new_direction = (2+3)%4 = 1  →  RIGHT
                  new_row = 1 + 0 = 1
                  new_col = 0 + 1 = 1
                  (1,1) not in visited ✓
                  robot.move() → tries to move RIGHT → BLOCKED ✗
                  robot.turnRight()  →  now facing DOWN (restored)

         ← backtrack from (1,0) to (0,0):
             robot.turnRight()   →  facing LEFT
             robot.turnRight()   →  facing UP   (180° turn)
             robot.move()        →  move UP back to (0,0)
             robot.turnRight()   →  facing RIGHT
             robot.turnRight()   →  facing DOWN (restored original direction)

    robot.turnRight()  →  now facing LEFT (done with i=2)

    SCENARIO 4: Back at (0,0), facing LEFT (direction=3), i=3
============================================================

    i=3: new_direction = (0+3)%4 = 3  →  LEFT
         new_row = 0 +  0  = 0
         new_col = 0 + (-1) = -1
         (0,-1) not in visited ✓
         robot.move() → tries to move LEFT → SUCCESS ✓

         → recurse: backtrack(row=0, col=-1, direction=3)
             robot.clean()  →  clean (0,-1)
             visited = {(0,0), (-1,0), (0,1), (1,0), (0,-1)}

             i=0: new_direction = (3+0)%4 = 3  →  LEFT
                  new_row = 0 +  0  = 0
                  new_col = -1 + (-1) = -2
                  (0,-2) not in visited ✓
                  robot.move() → tries to move LEFT → BLOCKED ✗
                  robot.turnRight()  →  now facing UP

             i=1: new_direction = (3+1)%4 = 0  →  UP
                  new_row = 0 + (-1) = -1
                  new_col = -1 + 0  = -1
                  (-1,-1) not in visited ✓
                  robot.move() → tries to move UP → BLOCKED ✗
                  robot.turnRight()  →  now facing RIGHT

             i=2: new_direction = (3+2)%4 = 1  →  RIGHT
                  new_row = 0 + 0 = 0
                  new_col = -1 + 1 = 0
                  (0,0) IN visited ✗  →  skip
                  robot.turnRight()  →  now facing DOWN

             i=3: new_direction = (3+3)%4 = 2  →  DOWN
                  new_row = 0 + 1 = 1
                  new_col = -1 + 0 = -1
                  (1,-1) not in visited ✓
                  robot.move() → tries to move DOWN → BLOCKED ✗
                  robot.turnRight()  →  now facing LEFT (restored)

         ← backtrack from (0,-1) to (0,0):
             robot.turnRight()   →  facing UP
             robot.turnRight()   →  facing RIGHT (180° turn)
             robot.move()        →  move RIGHT back to (0,0)
             robot.turnRight()   →  facing DOWN
             robot.turnRight()   →  facing LEFT (restored original direction)

    robot.turnRight()  →  now facing UP (done with i=3, back to start direction)

FINAL STATE:
============
visited = {(0,0), (-1,0), (0,1), (1,0), (0,-1)}
           center   up     right  down    left

All 5 accessible cells cleaned. ✓
Robot is back at (0,0) facing UP (original state). ✓

Complexity:
- Grid: 3×3 = 9 cells, 4 obstacles, 5 accessible
- Interpretation 1: O(3×3) = O(9)
- Interpretation 2: O(9-4) = O(5)
"""

# Another version of solution:

class Solution:
    def __init__(self):
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.visited = set()
    
    def backtrack(self, robot, row, col, direction):
        robot.clean()
        self.visited.add((row, col))
        
        for i in range(4):
            new_direction = (direction + i) % 4
            new_row = row + self.directions[new_direction][0]
            new_col = col + self.directions[new_direction][1]
            
            if (new_row, new_col) not in self.visited and robot.move():
                self.backtrack(robot, new_row, new_col, new_direction)
                
                robot.turnRight()
                robot.turnRight()
                robot.move()
                robot.turnRight()
                robot.turnRight()
            
            robot.turnRight()
    
    def cleanRoom(self, robot):
        self.backtrack(robot, 0, 0, 0)

# Grid Coordinate System
# In most grid/matrix problems, we use this coordinate system:
#         Column (x-axis)
#         0   1   2   3
# R   0   •   •   •   •
# o   1   •   •   •   •
# w   2   •   •   •   •
#     3   •   •   •   •
# 
# (y-axis)

# Key Convention:

# Row increases DOWNWARD (like reading a book)
# Column increases RIGHTWARD (like reading left to right)

# Understanding Direction Vectors
# A direction vector (row_delta, col_delta) tells us how to change our position:

# UP: (-1, 0)
# Starting at (2, 1):
#     0   1   2
# 0   •   •   •
# 1   •   ↑   •    ← Move to (1, 1)
# 2   •   X   •    ← Currently at (2, 1)
# 3   •   •   •

# To go UP: row decreases by 1, column stays same
# New position = (2, 1) + (-1, 0) = (1, 1)


# RIGHT: (0, 1)
# Starting at (2, 1):
#     0   1   2
# 0   •   •   •
# 1   •   •   •
# 2   •   X → •    ← Move to (2, 2)
# 3   •   •   •

# To go RIGHT: row stays same, column increases by 1
# New position = (2, 1) + (0, 1) = (2, 2)


# DOWN: (1, 0)
# Starting at (2, 1):
#     0   1   2
# 0   •   •   •
# 1   •   •   •
# 2   •   X   •    ← Currently at (2, 1)
# 3   •   ↓   •    ← Move to (3, 1)

# To go DOWN: row increases by 1, column stays same
# New position = (2, 1) + (1, 0) = (3, 1)


# LEFT: (0, -1)
# Starting at (2, 1):
#     0   1   2
# 0   •   •   •
# 1   •   •   •
# 2   • ← X   •    ← Move to (2, 0)
# 3   •   •   •

# To go LEFT: row stays same, column decreases by 1
# New position = (2, 1) + (0, -1) = (2, 0)

# Using turnLeft()

class Solution:
    def cleanRoom(self, robot):
        """
        Clean entire room using turnLeft() for counter-clockwise exploration.
        """
        
        # Direction vectors: UP, LEFT, DOWN, RIGHT (counter-clockwise order)
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        visited = set()
        
        def backtrack(row, col, direction):
            # Clean current cell and mark as visited
            robot.clean()
            visited.add((row, col))
            
            # Try all 4 directions in counter-clockwise order
            for i in range(4):
                new_direction = (direction + i) % 4
                new_row = row + directions[new_direction][0]
                new_col = col + directions[new_direction][1]
                
                if (new_row, new_col) not in visited and robot.move():
                    backtrack(new_row, new_col, new_direction)
                    
                    # Backtrack using turnLeft
                    robot.turnLeft()
                    robot.turnLeft()
                    robot.move()
                    robot.turnLeft()
                    robot.turnLeft()
                
                # Turn left for next direction (counter-clockwise)
                robot.turnLeft()
        
        backtrack(0, 0, 0)


# Variant : Mouse and Cheese (check Leetcode 1778)

# You are given a mouse that starts at position (0, 0) in a maze represented as a 2D grid. The mouse has limited vision and can only use two API methods to navigate:

# move(direction, row, col) - Checks if the mouse can move in the specified direction from position (row, col). Returns True if the move is valid (no wall, within bounds), False otherwise.

# KNOWN BUG: Even when this method returns False (blocked by wall or boundary), the mouse still incorrectly moves in that direction. To remedy this, you must immediately call move() in the opposite direction to compensate and return the mouse to its original position.

# hasCheese(row, col) - Returns True if there is cheese at position (row, col), False otherwise.

# The maze contains:

# 'S' or '.' - Empty walkable cells
# 'X' - Walls/obstacles (cannot pass through)
# '#' - Cheese (goal location)

# Your task: Implement the getCheese() method that:

# Returns True if the mouse successfully finds the cheese (cheese is reachable from starting position)
# Returns False if no cheese is reachable from the starting position

# Constraints

# 1. The mouse starts at position (0, 0)
# 2. The maze is a rectangular grid with dimensions N × M where 1 ≤ N, M ≤ 100
# 3. There is at most one cheese in the maze
# 4. The mouse can only move in 4 directions: UP, RIGHT, DOWN, LEFT
# 5. A move is considered "valid" only if:
#     The target position is within grid boundaries (0 ≤ row < N, 0 ≤ col < M)
#     The target position is not a wall (grid[row][col] != 'X')
# 6. Critical Bug: The move() API has a bug - it moves the mouse even when returning False. You must compensate by calling move() in the opposite direction immediately after any failed move attempt.
# 7. You can only use the two provided API methods: move(direction, row, col) and hasCheese(row, col)
# Mouse position is tracked logically via function parameters in your implementation - the actual mouse position is managed by the buggy API

# Example:

# Grid (2×2):

# S .
# X #

# Cheese location: (1, 1)

# Explanation:

# The mouse navigates around an obstacle to find cheese.

# Step-by-step:
# 1. Start at (0,0): hasCheese(0,0)? No
# 2. Try UP from (0,0): move((-1,0), 0, 0) → False (out of bounds)
#    BUG: Mouse moved to (-1,0) anyway!
#    FIX: Immediately call move((1,0), -1, 0) to compensate → back at (0,0)
# 3. Try RIGHT from (0,0): move((0,1), 0, 0) → True ✓
#    Logically track position as (0,1), recursively explore
# 4. At (0,1): hasCheese(0,1)? No
# 5. Try DOWN from (0,1): move((1,0), 0, 1) → True ✓
#    Logically track position as (1,1), recursively explore
# 6. At (1,1): hasCheese(1,1)? Yes! ✓

# Logical path: (0,0) → (0,1) → (1,1)
# Cheese found!

class Mouse:
    """
    Mouse with limited API to find cheese in a maze.
    
    IMPORTANT: move() has a bug - even when returning False, 
    it still moves the mouse. We compensate by calling move() 
    in the opposite direction to undo the buggy movement.
    
    Time Complexity: O(N × M)
        - Visit each cell at most once due to visited set
        - Each cell performs O(1) work (try 4 directions)
        
    Space Complexity: O(N × M)
        - visited set stores up to N × M cells
        - Recursion stack depth up to N × M in worst case
    """
    
    def __init__(self, grid: List[List[str]], cheese_location: Tuple[int, int]):
        """
        Initialize the mouse in the maze.
        
        Args:
            grid: 2D maze where 'S'/'.' = empty, 'X' = wall, '#' = cheese
            cheese_location: (row, col) position of the cheese
        """
        self.grid = grid
        self.cheese_location = cheese_location
        
        # Direction vectors: UP, RIGHT, DOWN, LEFT
        # These represent how to change (row, col) for each direction
        self.directions = [
            (-1, 0),  # UP: row decreases by 1
            (0, 1),   # RIGHT: col increases by 1
            (1, 0),   # DOWN: row increases by 1
            (0, -1)   # LEFT: col decreases by 1
        ]
        
        # Opposite direction vectors for backtracking and bug compensation
        # Each index i corresponds to the opposite of directions[i]
        # Used to undo moves when backtracking or compensating for API bug
        self.opposite_directions = [
            (1, 0),   # DOWN (opposite of UP)
            (0, -1),  # LEFT (opposite of RIGHT)
            (-1, 0),  # UP (opposite of DOWN)
            (0, 1)    # RIGHT (opposite of LEFT)
        ]
        
        # Track visited cells to prevent infinite loops and redundant exploration
        self.visited = set()
    
    def move(self, direction: Tuple[int, int], row: int, col: int) -> bool:
        """
        Check if move in direction from (row, col) is valid.
        Does NOT actually track mouse position - just validates the move.
        
        Args:
            direction: (dr, dc) direction vector to move
            row: Current row position
            col: Current column position
        
        Returns:
            True if move is valid (within bounds and not a wall)
            False if move is invalid (out of bounds or wall)
        
        KNOWN BUG (in actual API):
            Even when this returns False, the physical mouse still moves!
            The caller MUST compensate by immediately calling move() in 
            the opposite direction to undo the buggy movement.
        
        Implementation Note:
            This is a stateless validation function - it doesn't update
            any instance variables. Position is tracked via function 
            parameters in the DFS recursion.
        """
        dr, dc = direction
        # LOCAL variables new_row and new_col are calculated here
        # These are DIFFERENT from any new_row/new_col in dfs()
        # These local variables exist only within this function scope
        new_row = row + dr
        new_col = col + dc
        
        # Check if new position is within grid boundaries
        if new_row < 0 or new_row >= len(self.grid):
            return False
        
        if new_col < 0 or new_col >= len(self.grid[0]):
            return False
        
        # Check if new position is a wall
        if self.grid[new_row][new_col] == 'X':
            return False
        
        # Move is valid
        return True
    
    def hasCheese(self, row: int, col: int) -> bool:
        """
        Check if cheese is at the given position.
        
        Args:
            row: Row position to check
            col: Column position to check
        
        Returns:
            True if cheese is at (row, col), False otherwise
        """
        return row == self.cheese_location[0] and col == self.cheese_location[1]
    
    def dfs(self, row: int, col: int) -> bool:
        """
        Depth-First Search with backtracking to find cheese.
        
        Args:
            row: Current row position in the maze
            col: Current column position in the maze
        
        Returns:
            True if cheese found from this position, False otherwise
        
        Algorithm:
            1. Check if current position has cheese (base case)
            2. Mark current position as visited
            3. Try all 4 directions:
               a. Skip if already visited
               b. Validate move with move() API
               c. If invalid: compensate for bug and skip
               d. If valid: recursively explore new position
               e. If cheese found: return True (stay at cheese)
               f. If not found: implicit backtrack via recursion return
            4. Return False if no cheese found in any direction
        """
        # Base case: Check if we found the cheese at current position
        if self.hasCheese(row, col):
            return True
        
        # Mark current position as visited to avoid revisiting
        # This prevents infinite loops in the search
        self.visited.add((row, col))
        
        # Try exploring in all 4 directions (UP, RIGHT, DOWN, LEFT)
        for i in range(len(self.directions)):
            # Get the direction vector
            dr, dc = self.directions[i]
            
            # Calculate the new position if we move in this direction
            new_row = row + dr
            new_col = col + dc
            
            # Skip this direction if we've already visited the new position
            # This prevents redundant exploration and cycles
            if (new_row, new_col) in self.visited:
                continue
            
            # Check if the move is valid using the buggy API
            # CRITICAL: Even if this returns False, the physical mouse
            # will still move due to the API bug!
            if not self.move(self.directions[i], row, col):
                # Move is invalid (wall or out of bounds)
                # BUT: The physical mouse still moved due to the bug!
                # 
                # COMPENSATION: Immediately call move() in opposite direction
                # to undo the buggy movement and return mouse to current position
                # 
                # Note: We pass (new_row, new_col) as the position because
                # that's where the mouse physically is now due to the bug
                self.move(self.opposite_directions[i], new_row, new_col)
                
                # Skip this direction since it's not valid
                continue
            
            # Move is valid - recursively explore from the new position
            # Position is tracked via parameters (new_row, new_col)
            if self.dfs(new_row, new_col):
                # Cheese found in this recursive branch!
                # Return True to propagate success up the call stack
                # No need to backtrack - we want to stay at cheese location
                return True
            
            # Cheese not found in this direction
            # 
            # STATELESS APPROACH - NO EXPLICIT BACKTRACKING NEEDED:
            # Position is tracked via parameters (row, col), not instance variables
            # When recursion returns, we're automatically back at (row, col)
            # The call stack preserves the parameter values automatically
            # 

            # The following line is REDUNDANT and does nothing useful:
            # self.move(self.opposite_directions[i], new_row, new_col)

            # Why it's redundant:
            # - Only validates that we CAN move back (return value ignored)
            # - Doesn't change row, col (they're already correct from parameters)
            # - Doesn't change new_row, new_col (recalculated next iteration)
            # - Doesn't update any state (stateless approach)
            # - Just wastes CPU cycles on unnecessary validation
        
        # Tried all 4 directions from this position, no cheese found
        return False
    
    def getCheese(self) -> bool:
        """
        Find cheese starting from position (0, 0) using DFS.
        
        Returns:
            True if cheese is reachable from (0, 0)
            False if cheese is not reachable
        
        Implementation:
            1. Clear any previous search state (visited set)
            2. Start DFS from (0, 0)
            3. Return result of DFS
        """
        # Clear visited set from any previous search (optional)
        self.visited.clear()

        # Start DFS from the starting position (0, 0)
        # Position tracking is done via function parameters
        return self.dfs(0, 0)

# Dry Run: Stateless Mouse DFS - Step by Step
# Setup

# Grid (2×2):

# S X
# . #

# S = Start at (0, 0)
# X = Wall at (0, 1)
# . = Empty at (1, 0)
# # = Cheese at (1, 1)

# Cheese location: (1, 1)

# Initial State
# visited = {}
# directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # UP, RIGHT, DOWN, LEFT
# opposite_directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

# # Execution Begins

# CALL 1: dfs(row=0, col=0)

# Stack Frame 1:
# ├─ row = 0
# ├─ col = 0
# └─ Local scope for this call
# Step 1.1: Check for cheese
# hasCheese(0, 0)?
#     return (0 == 1 and 0 == 1)
#     return False
# No cheese here.
# Step 1.2: Mark as visited
# visited.add((0, 0))
# visited = {(0, 0)}
# Step 1.3: Try all 4 directions

# Direction i=0: Try UP
# i = 0
# dr, dc = directions[0] = (-1, 0)
# new_row = row + dr = 0 + (-1) = -1
# new_col = col + dc = 0 + 0 = 0

# # Check if already visited
# (-1, 0) in visited? No

# # Validate move
# move((-1, 0), row=0, col=0):
#     dr, dc = (-1, 0)
#     new_row = 0 + (-1) = -1
#     new_col = 0 + 0 = 0
    
#     # Check bounds
#     if -1 < 0:  # True!
#         return False

# # Move invalid!
# # ⚠️ BUG: Physical mouse moved to (-1, 0) anyway!

# # Bug compensation:
# move(opposite_directions[0], new_row=-1, new_col=0):
#     # opposite_directions[0] = (1, 0) = DOWN
#     dr, dc = (1, 0)
#     new_row = -1 + 1 = 0
#     new_col = 0 + 0 = 0
    
#     # Check if (0, 0) is valid
#     0 >= 0 and 0 < 2? Yes
#     0 >= 0 and 0 < 2? Yes
#     grid[0][0] = 'S' (not 'X')? Yes
#     return True

# # Compensation validated moving back from (-1,0) to (0,0)
# # Continue to next direction
# State after i=0:

# visited = {(0, 0)}
# Still in CALL 1 at (row=0, col=0)


# Direction i=1: Try RIGHT
# i = 1
# dr, dc = directions[1] = (0, 1)
# new_row = row + dr = 0 + 0 = 0
# new_col = col + dc = 0 + 1 = 1

# # Check if already visited
# (0, 1) in visited? No

# # Validate move
# move((0, 1), row=0, col=0):
#     dr, dc = (0, 1)
#     new_row = 0 + 0 = 0
#     new_col = 0 + 1 = 1
    
#     # Check bounds
#     0 >= 0 and 0 < 2? Yes
#     1 >= 0 and 1 < 2? Yes
    
#     # Check wall
#     grid[0][1] = 'X'  # Wall!
#     return False

# # Move invalid!
# # ⚠️ BUG: Physical mouse moved to (0, 1) - inside wall!

# # Bug compensation:
# move(opposite_directions[1], new_row=0, new_col=1):
#     # opposite_directions[1] = (0, -1) = LEFT
#     dr, dc = (0, -1)
#     new_row = 0 + 0 = 0
#     new_col = 1 + (-1) = 0
    
#     # Check if (0, 0) is valid
#     0 >= 0 and 0 < 2? Yes
#     0 >= 0 and 0 < 2? Yes
#     grid[0][0] = 'S' (not 'X')? Yes
#     return True

# # Compensation validated moving back from (0,1) to (0,0)
# # Continue to next direction
# State after i=1:

# visited = {(0, 0)}
# Still in CALL 1 at (row=0, col=0)


# Direction i=2: Try DOWN
# i = 2
# dr, dc = directions[2] = (1, 0)
# new_row = row + dr = 0 + 1 = 1
# new_col = col + dc = 0 + 0 = 0

# # Check if already visited
# (1, 0) in visited? No

# # Validate move
# move((1, 0), row=0, col=0):
#     dr, dc = (1, 0)
#     new_row = 0 + 1 = 1
#     new_col = 0 + 0 = 0
    
#     # Check bounds
#     1 >= 0 and 1 < 2? Yes
#     0 >= 0 and 0 < 2? Yes
    
#     # Check wall
#     grid[1][0] = '.' (not 'X')? Yes
#     return True

# # Move is VALID! ✓
# # Physical mouse moved to (1, 0) - this time intentionally

# # Recursive call
# dfs(new_row=1, new_col=0)

# CALL 2: dfs(row=1, col=0)

# Stack Frame 2 (NEW):
# ├─ row = 1
# ├─ col = 0
# └─ Local scope for THIS call

# Stack Frame 1 (PRESERVED):
# ├─ row = 0  ← Still 0!
# ├─ col = 0  ← Still 0!
# └─ Waiting at i=2
# Step 2.1: Check for cheese
# hasCheese(1, 0)?
#     return (1 == 1 and 0 == 1)
#     return False
# No cheese here.
# Step 2.2: Mark as visited
# visited.add((1, 0))
# visited = {(0, 0), (1, 0)}
# Step 2.3: Try all 4 directions

# Direction i=0: Try UP
# i = 0
# dr, dc = directions[0] = (-1, 0)
# new_row = row + dr = 1 + (-1) = 0
# new_col = col + dc = 0 + 0 = 0

# # Check if already visited
# (0, 0) in visited? YES!

# # Skip this direction
# continue

# Direction i=1: Try RIGHT
# i = 1
# dr, dc = directions[1] = (0, 1)
# new_row = row + dr = 1 + 0 = 1
# new_col = col + dc = 0 + 1 = 1

# # Check if already visited
# (1, 1) in visited? No

# # Validate move
# move((0, 1), row=1, col=0):
#     dr, dc = (0, 1)
#     new_row = 1 + 0 = 1
#     new_col = 0 + 1 = 1
    
#     # Check bounds
#     1 >= 0 and 1 < 2? Yes
#     1 >= 0 and 1 < 2? Yes
    
#     # Check wall
#     grid[1][1] = '#' (not 'X')? Yes
#     return True

# # Move is VALID! ✓
# # Physical mouse moved to (1, 1)

# # Recursive call
# dfs(new_row=1, new_col=1)

# CALL 3: dfs(row=1, col=1)

# Stack Frame 3 (NEW):
# ├─ row = 1
# ├─ col = 1
# └─ Local scope for THIS call

# Stack Frame 2 (PRESERVED):
# ├─ row = 1  ← Still 1!
# ├─ col = 0  ← Still 0!
# └─ Waiting at i=1

# Stack Frame 1 (PRESERVED):
# ├─ row = 0  ← Still 0!
# ├─ col = 0  ← Still 0!
# └─ Waiting at i=2
# Step 3.1: Check for cheese
# hasCheese(1, 1)?
#     return (1 == 1 and 1 == 1)
#     return True  ✓✓✓

# # CHEESE FOUND!
# return True

# RETURN to CALL 2

# Back in Stack Frame 2:
# ├─ row = 1
# ├─ col = 0
# └─ At i=1 (RIGHT direction)

# Code location:
# if self.dfs(new_row=1, new_col=1):  # This just returned True!
#     return True  # Propagate success

# # Return True to CALL 1

# RETURN to CALL 1
# Back in Stack Frame 1:
# ├─ row = 0  ← Still 0!
# ├─ col = 0  ← Still 0!
# └─ At i=2 (DOWN direction)

# Code location:
# if self.dfs(new_row=1, new_col=0):  # This just returned True!
#     return True  # Propagate success

# # Return True to getCheese()

# Final Result
# getCheese() returns: True
# visited = {(0, 0), (1, 0), (1, 1)}

# Path taken:
# (0, 0) → (1, 0) → (1, 1) ✓

# Cheese found!

# Another version : Mouse physically moves into out of bound areas and then backtracks

# Dry run the below setup to see the effect of final backtracking:

# Grid (2×2):

# S X
# . .

# S = Start at (0, 0)
# X = Wall at (0, 1)
# . = Empty at (1, 0)
# . = Empty at (1, 1)

# NO CHEESE!

# class Mouse:
#     """
#     Mouse with limited API to find cheese in a maze.
    
#     IMPORTANT: move() has a bug - even when returning False, 
#     it still moves the mouse. We compensate by calling move() 
#     in the opposite direction to undo the buggy movement.

#     Time Complexity: O(N x M)
#         - Each cell is visited at most once due to visited set
#         - Each cell performs O(1) work (try 4 directions)
#         - Worst case: cheese unreachable, all N x M cells explored

#     Space Complexity: O(N x M)
#         - visited set stores at most N x M cells
#         - Recursion stack depth up to N x M in worst case

#     Example (worst case - no cheese, all 4 cells explored):
#         Grid:
#             S .
#             . .
#         Cheese at (-1,-1). DFS explores all 4 cells:
#         (0,0) → (0,1) → (1,1) → (1,0) → return False
#         All 4 cells in visited set → O(N x M) space
#         All 4 cells visited → O(N x M) time

#     Returns:
#         True if cheese found from current position, False otherwise
#     """
    
#     def __init__(self, grid: List[List[str]], cheese_location: Tuple[int, int]):
#         """
#         Initialize the mouse in the maze.
        
#         Args:
#             grid: 2D maze where 'S'/'.' = empty, 'X' = wall, '#' = cheese
#             cheese_location: (row, col) position of the cheese
#         """
#         self.grid = grid
#         self.cheese_location = cheese_location
#         self.rows = len(grid)
#         self.cols = len(grid[0])
        
#         # Track actual physical mouse position as instance variables
#         # This allows dfs() to work without parameters - position is
#         # stored in the object state rather than passed as arguments
#         self.current_row = 0
#         self.current_col = 0
        
#         self.directions = [
#             (-1, 0),  # UP
#             (0, 1),   # RIGHT
#             (1, 0),   # DOWN
#             (0, -1)   # LEFT
#         ]
        
#         self.opposite_directions = [
#             (1, 0),   # DOWN (opposite of UP)
#             (0, -1),  # LEFT (opposite of RIGHT)
#             (-1, 0),  # UP (opposite of DOWN)
#             (0, 1)    # RIGHT (opposite of LEFT)
#         ]
        
#         self.visited = set()
    
#     def move(self, direction: Tuple[int, int]) -> bool:
#         """
#         Actually moves the mouse - updates self.current_row/col.
        
#         Args:
#             direction: (dr, dc) direction vector to move
        
#         Returns:
#             True if move is valid (within bounds and not a wall)
#             False if move is invalid (out of bounds or wall)
        
#         KNOWN BUG (in actual API):
#             Even when this returns False, the mouse physically moves!
#             Caller must compensate by immediately calling move() in 
#             the opposite direction to undo the buggy movement.
#         """
#         dr, dc = direction
#         new_row = self.current_row + dr
#         new_col = self.current_col + dc

#         is_valid = (0 <= new_row < self.rows and 
#                     0 <= new_col < self.cols and 
#                     self.grid[new_row][new_col] != 'X')
        
#         # BUG: Mouse physically moves regardless of validity!
#         # This updates the actual position even when returning False
#         self.current_row = new_row
#         self.current_col = new_col
        
#         return is_valid
    
#     def hasCheese(self) -> bool:
#         """
#         Check if cheese at current mouse position.
        
#         Uses instance variables (self.current_row/col) which is why
#         dfs() doesn't need parameters - the position is in object state.
#         """
#         return (self.current_row == self.cheese_location[0] and 
#                 self.current_col == self.cheese_location[1])
    
#     def dfs(self) -> bool:
#         """
#         DFS with backtracking to find cheese.
        
#         WHY NO PARAMETERS?
#         ------------------
#         Position is tracked via instance variables (self.current_row/col)
#         rather than function parameters. This means:
#         - The mouse's position is part of the object's state
#         - When move() is called, it updates this state
#         - When we recurse, the state is already updated
#         - This models actual physical mouse movement
        
#         Returns:
#             True if cheese found from current position, False otherwise
#         """
#         if self.hasCheese():
#             return True
        
#         # Use instance variables for current position
#         self.visited.add((self.current_row, self.current_col))
        
#         for i in range(len(self.directions)):
#             dr, dc = self.directions[i]
#             new_row = self.current_row + dr
#             new_col = self.current_col + dc
            
#             if (new_row, new_col) in self.visited:
#                 continue
            
#             # Try to move - this PHYSICALLY moves the mouse
#             # Updates self.current_row/col regardless of return value (bug!)
#             move_success = self.move(self.directions[i])
            
#             if not move_success:
#                 # WHY CALL move() AGAIN? (First time - Bug Compensation)
#                 # =====================================================
#                 # Move failed (wall/boundary) BUT mouse still moved due to bug!
#                 # Mouse is now at invalid position (new_row, new_col)
#                 # We must immediately move in opposite direction to undo
#                 # and return mouse to the original valid position
#                 self.move(self.opposite_directions[i])
#                 # Now mouse is back at (current_pos) where it should be
#                 continue
            
#             # Move succeeded - mouse is now physically at (new_row, new_col)
#             # self.current_row = new_row, self.current_col = new_col
            
#             # Recursively explore from new position
#             # No parameters needed - position already updated in instance variables
#             if self.dfs():
#                 return True  # Cheese found, stay at this position
            
#             # WHY CALL move() AGAIN? (Second time - Explicit Backtracking)
#             # ===========================================================
#             # Cheese not found in this direction, need to backtrack
#             # Mouse is still physically at (new_row, new_col) after dfs() returns
#             # We need to return to previous position to try other directions
#             # 
#             # This is DIFFERENT from the first move() call:
#             # - First call: Compensates for bug when move failed
#             # - Second call: Backtracks after successful exploration that found no cheese
#             # 
#             # Without this, the mouse would stay at (new_row, new_col) and
#             # the next iteration would try directions from wrong position!

#             self.move(self.opposite_directions[i])

#             # Now mouse is back at original position for next direction attempt

#             # The final backtrack is reached when the recursive dfs() call returns False, which happens in two  cases:

#             # No cheese exists - backtrack executed for every failed exploration
#             # Cheese is unreachable - backtrack executed for every failed exploration
#             # Cheese IS found - return True executes immediately, skipping backtrack
                
#         return False
    
#     def getCheese(self) -> bool:
#         """
#         Find cheese starting from position (0, 0) using DFS.
        
#         Returns:
#             True if cheese is reachable from (0, 0)
#             False if cheese is not reachable
#         """
#         # Position already initialized to (0,0) in __init__
#         # No need to re-initialize for single-use pattern
#         return self.dfs()

# Example where backtrack is used

# Grid:
# (0,0)S  (0,1).  (0,2)X
# (1,0)#  (1,1)X  (1,2)X

# Cheese at (1,0). Mouse starts at (0,0).

# dfs() — mouse at (0,0)

# hasCheese()? No
# visited = {(0,0)}
# Try UP: new=(-1,0) → move(UP) → out of bounds, bug fires, current=(-1,0), returns False

# compensate: move(DOWN) → current=(-1+1, 0)=(0,0) ✅


# Try RIGHT: new=(0,1) → move(RIGHT) → current=(0+0, 1+1)=(0,1), returns True

# dfs() — mouse at (0,1)
# hasCheese()? No
# visited = {(0,0),(0,1)}
# Try UP: new=(-1,1) → move(UP) → out of bounds, bug fires, current=(0-1,1)=(-1,1), returns False

# compensate: move(DOWN) → current=(-1+1,1)=(0,1) ✅


# Try RIGHT: new=(0,2) → move(RIGHT) → wall, bug fires, current=(0,1+1)=(0,2), returns False

# compensate: move(LEFT) → current=(0,2-1)=(0,1) ✅


# Try DOWN: new=(1,1) → move(DOWN) → wall, bug fires, current=(0+1,1)=(1,1), returns False

# compensate: move(UP) → current=(1-1,1)=(0,1) ✅


# Try LEFT: new=(0,0) → already in visited → skip
# Dead end! return False


# Gets False → FINAL BACKTRACK FIRES: move(LEFT) → current=(0,1-1)=(0,0) ✅
# Try DOWN: new=(1,0) → move(DOWN) → current=(0+1,0)=(1,0), returns True

# dfs() — mouse at (1,0)
# hasCheese()? Yes → return True


# Gets True → return True ✅


# Another version : Mouse moves only to valid positions

# Mouse position in parameters, no compensation or backtracking needed

# class Mouse:
#     """
#     Mouse with limited API to find cheese in a maze - STATELESS VERSION.
    
#     In this version, move() does NOT have a bug and position is tracked
#     via function parameters rather than instance variables.
    
#     Time Complexity: O(N × M)
#         - Visit each cell at most once due to visited set
#         - Each cell performs O(1) work (try 4 directions)
        
#     Space Complexity: O(N × M)
#         - visited set stores up to N × M cells
#         - Recursion stack depth up to N × M in worst case
#     """
    
#     def __init__(self, grid: List[List[str]], cheese_location: Tuple[int, int]):
#         """
#         Initialize the mouse in the maze.
        
#         Args:
#             grid: 2D maze where 'S'/'.' = empty, 'X' = wall, '#' = cheese
#             cheese_location: (row, col) position of the cheese
#         """
#         self.grid = grid
#         self.cheese_location = cheese_location
#         self.rows = len(grid)
#         self.cols = len(grid[0])
        
#         # NO instance variables for position tracking!
#         # Position is tracked via function parameters
        
#         # Direction vectors: UP, RIGHT, DOWN, LEFT
#         self.directions = [
#             (-1, 0),  # UP
#             (0, 1),   # RIGHT
#             (1, 0),   # DOWN
#             (0, -1)   # LEFT
#         ]
        
#         # Track visited cells to prevent infinite loops
#         self.visited = set()
    
#     def move(self, direction: Tuple[int, int], row: int, col: int) -> bool:
#         """
#         Check if move in direction from (row, col) is valid.
#         Does NOT actually move the mouse - just validates.
        
#         Args:
#             direction: (dr, dc) direction vector to move
#             row: Current row position
#             col: Current column position
        
#         Returns:
#             True if move is valid (within bounds and not a wall)
#             False if move is invalid
        
#         NO BUG: This function only validates, never updates position.
#         Position is tracked via parameters in the DFS recursion.
#         """
#         dr, dc = direction
#         new_row = row + dr
#         new_col = col + dc
        
#         # Check if new position is within bounds
#         if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
#             return False
        
#         # Check if new position is a wall
#         if self.grid[new_row][new_col] == 'X':
#             return False
        
#         # Move is valid
#         return True
    
#     def hasCheese(self, row: int, col: int) -> bool:
#         """
#         Check if cheese is at the given position.
        
#         Args:
#             row: Row position to check
#             col: Column position to check
        
#         Returns:
#             True if cheese is at (row, col)
#         """
#         return (row == self.cheese_location[0] and 
#                 col == self.cheese_location[1])
    
#     def dfs(self, row: int, col: int) -> bool:
#         """
#         DFS with implicit backtracking to find cheese.
#         Position is tracked via parameters.
        
#         Args:
#             row: Current row position
#             col: Current column position
        
#         Returns:
#             True if cheese found from this position, False otherwise
#         """
#         # Check if cheese at current position
#         if self.hasCheese(row, col):
#             return True
        
#         # Mark current position as visited
#         self.visited.add((row, col))
        
#         # Try all 4 directions
#         for i in range(len(self.directions)):
#             dr, dc = self.directions[i]
#             new_row = row + dr
#             new_col = col + dc
            
#             # Skip if already visited
#             if (new_row, new_col) in self.visited:
#                 continue
            
#             # Validate move (doesn't actually move)
#             if not self.move(self.directions[i], row, col):
#                 # Move is invalid (wall or out of bounds)
#                 # No compensation needed - move() doesn't change state
#                 continue
            
#             # Move is valid - recursively explore with new position
#             # Position passed as parameters (new_row, new_col)
#             if self.dfs(new_row, new_col):
#                 return True  # Cheese found
            
#             # Cheese not found in this direction
#             # 
#             # NO EXPLICIT BACKTRACKING NEEDED:
#             # Position is in parameters, not instance variables
#             # When recursion returns, we're automatically back at (row, col)
#             # The call stack preserves parameter values
        
#         return False
    
#     def getCheese(self) -> bool:
#         """
#         Find cheese starting from position (0, 0).
        
#         Returns:
#             True if cheese is reachable from (0, 0)
#             False if cheese is not reachable
#         """
#         return self.dfs(0, 0)

# Mouse physically moves only to valid positions and explicitly backtracks

# class Mouse:
#     """
#     Mouse with limited API to find cheese in a maze.
    
#     IMPORTANT: In this version, move() does NOT have a bug.
#     The mouse only moves when the move is valid. No compensation needed.
    
#     Time Complexity: O(N × M)
#         - Visit each cell at most once due to visited set
#         - Each cell performs O(1) work (try 4 directions)
        
#     Space Complexity: O(N × M)
#         - visited set stores up to N × M cells
#         - Recursion stack depth up to N × M in worst case
#     """
    
#     def __init__(self, grid: List[List[str]], cheese_location: Tuple[int, int]):
#         """
#         Initialize the mouse in the maze.
        
#         Args:
#             grid: 2D maze where 'S'/'.' = empty, 'X' = wall, '#' = cheese
#             cheese_location: (row, col) position of the cheese
#         """
#         self.grid = grid
#         self.cheese_location = cheese_location
#         self.rows = len(grid)
#         self.cols = len(grid[0])
        
#         # Track actual physical mouse position
#         self.current_row = 0
#         self.current_col = 0
        
#         # Direction vectors: UP, RIGHT, DOWN, LEFT
#         self.directions = [
#             (-1, 0),  # UP
#             (0, 1),   # RIGHT
#             (1, 0),   # DOWN
#             (0, -1)   # LEFT
#         ]
        
#         # Opposite direction vectors for backtracking
#         self.opposite_directions = [
#             (1, 0),   # DOWN (opposite of UP)
#             (0, -1),  # LEFT (opposite of RIGHT)
#             (-1, 0),  # UP (opposite of DOWN)
#             (0, 1)    # RIGHT (opposite of LEFT)
#         ]
        
#         # Track visited cells to prevent infinite loops
#         self.visited = set()
    
#     def move(self, direction: Tuple[int, int]) -> bool:
#         """
#         Move the mouse in the specified direction ONLY if valid.
        
#         Args:
#             direction: (dr, dc) direction vector to move
        
#         Returns:
#             True if move was successful (mouse actually moved)
#             False if move was invalid (mouse did NOT move)
        
#         NO BUG: Mouse only moves if the move is valid.
#         If invalid, mouse stays at current position.
#         """
#         dr, dc = direction

#         new_row = self.current_row + dr
#         new_col = self.current_col + dc
        
#         # Check if new position is within bounds
#         if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
#             return False  # Out of bounds - don't move
        
#         # Check if new position is a wall
#         if self.grid[new_row][new_col] == 'X':
#             return False  # Wall - don't move
        
#         # Move is valid - actually move the mouse
#         self.current_row = new_row
#         self.current_col = new_col

#         return True
    
#     def hasCheese(self) -> bool:
#         """Check if cheese at current mouse position."""
#         return (self.current_row == self.cheese_location[0] and 
#                 self.current_col == self.cheese_location[1])
    
#     def dfs(self) -> bool:
#         """
#         DFS with backtracking to find cheese.
        
#         Returns:
#             True if cheese found, False otherwise
#         """
#         # Check if cheese at current position
#         if self.hasCheese():
#             return True
        
#         # Mark current position as visited
#         self.visited.add((self.current_row, self.current_col))
        
#         # Try all 4 directions
#         for i in range(len(self.directions)):
#             dr, dc = self.directions[i]
#             new_row = self.current_row + dr
#             new_col = self.current_col + dc
            
#             # Skip if already visited
#             if (new_row, new_col) in self.visited:
#                 continue
            
#             # Try to move - mouse only moves if valid
#             if not self.move(self.directions[i]):
#                 # Move failed (wall or out of bounds)
#                 # Mouse did NOT move - still at current position
#                 # No compensation needed!
#                 continue
            
#             # Move succeeded - mouse is now at (new_row, new_col)
#             # Recursively explore from new position
#             if self.dfs():
#                 return True  # Cheese found, stay here
            
#             # Cheese not found - backtrack
#             # Move back to previous position
#             self.move(self.opposite_directions[i])
        
#         return False
    
#     def getCheese(self) -> bool:
#         """
#         Find cheese starting from position (0, 0).
        
#         Returns:
#             True if cheese is reachable from (0, 0)
#             False if cheese is not reachable
#         """
#         # Reset state to allow getCheese() to be called multiple times.
#         # __init__ sets these once at construction, but does not re-run
#         # on subsequent calls, so we reset manually here.
#         self.visited.clear()
#         self.current_row = 0
#         self.current_col = 0
#         return self.dfs()




