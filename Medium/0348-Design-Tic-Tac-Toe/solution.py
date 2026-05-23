"""
LeetCode 348. Design Tic-Tac-Toe
Difficulty: Medium
URL: https://leetcode.com/problems/design-tic-tac-toe/
"""

# Approach 1: Brute Force

# The straightforward approach would be to store the entire n×n board in a 2D array. After each move, we'd scan the affected row, column, and potentially the two diagonals to check if all cells contain the same player's mark.

# This would be:
# Space: O(n²) to store the full board
# Time per move: O(n) because we'd scan up to 4 lines of length n

# For a 3×3 board this is fine, but for larger boards or many moves, we're doing a lot of redundant checking.

class TicTacToe:
    def __init__(self, n: int):
        """
        Initialize the Tic-Tac-Toe board of size n x n.
        
        Time Complexity: O(n²) - initialize n x n board
        Space Complexity: O(n²) - store entire board
        """
        self.n = n
        self.board = [[0] * n for _ in range(n)]  # 0 = empty, 1 = player 1, 2 = player 2
    
    def move(self, row: int, col: int, player: int) -> int:
        """
        Place a player's mark at (row, col) and check for win.
        
        Time Complexity: O(n) - check row, column, and potentially 2 diagonals
        Space Complexity: O(1) - no additional space used
        """
        n = self.n
        
        # Place the mark on the board
        self.board[row][col] = player
        
        # Check row: scan all columns in this row
        if all(self.board[row][c] == player for c in range(n)):
            return player
        
        # Check column: scan all rows in this column
        if all(self.board[r][col] == player for r in range(n)):
            return player
        
        # Check main diagonal (top-left to bottom-right)
        # Only check if this move is on the main diagonal (row == col)
        if row == col:
            if all(self.board[i][i] == player for i in range(n)):
                return player
        
        # Check anti-diagonal (top-right to bottom-left)
        # Only check if this move is on the anti-diagonal (row + col == n - 1)
        if row + col == n - 1:
            if all(self.board[i][n - 1 - i] == player for i in range(n)):
                return player
        
        # No winner yet
        return 0

# Approach 2: Optimal - Track Sums

# Here's the key insight: we don't actually need to see the board or recount every time. We can just track running sums for each row, column, and the two diagonals.

# The trick is:

# Player 1's move: add +1 to the sum
# Player 2's move: add -1 to the sum

# A player wins when any sum reaches +n (player 1) or -n (player 2).
# When a move happens at position (row, col), we only update:

# The sum for that row
# The sum for that column
# The diagonal sums if the position is on a diagonal

# Then we just check if any of those sums equals ±n. That's it!

# This gives us:
# Space: O(n) - just store n row sums, n column sums, and 2 diagonal values
# Time per move: O(1) - update at most 4 counters and check them

# Much more efficient, especially for large boards or many moves.

class TicTacToe:
    def __init__(self, n: int):
        """
        Initialize the Tic-Tac-Toe board of size n x n.
        
        We use a sum-based approach instead of storing the full board:
        - Player 1's move adds +1 to sums
        - Player 2's move adds -1 to sums
        - A sum of +n means Player 1 filled that line
        - A sum of -n means Player 2 filled that line
        
        Time Complexity: O(n) - initialize arrays of size n
        Space Complexity: O(n) - store n rows + n columns + 2 diagonals + 1 counter
        
        Base checks NOT included (LeetCode 348 guarantees valid inputs):
        - n is guaranteed to be ≥ 1
        - No need to validate board size in __init__
        """
        self.n = n
        
        # Track running sum for each row (index 0 to n-1)
        # Example: self.rows[0] tracks the sum for row 0
        # If row 0 has marks [X, X, X], self.rows[0] = 1+1+1 = 3
        self.rows = [0] * n
        
        # Track running sum for each column (index 0 to n-1)
        # Example: self.cols[1] tracks the sum for column 1
        # If col 1 has marks [O, O, O], self.cols[1] = -1-1-1 = -3
        self.cols = [0] * n
        
        # Track running sum for the main diagonal (top-left to bottom-right)
        # Only ONE main diagonal exists: positions (0,0), (1,1), (2,2), etc.
        # Positions on main diagonal satisfy: row == col
        self.diagonal = 0
        
        # Track running sum for the anti-diagonal (top-right to bottom-left)
        # Only ONE anti-diagonal exists: positions (0,n-1), (1,n-2), ..., (n-1,0)
        # Positions on anti-diagonal satisfy: row + col == n - 1
        self.anti_diagonal = 0
        
        # Count total moves made (used for draw detection)
        # When move_count reaches n², the board is completely full
        # We can detect a draw without storing the full board by counting moves
        self.move_count = 0
        
        # ============================================================
        # Additional attributes needed for base checks (NOT in optimal solution)
        # ============================================================
        # Uncomment these if you need validation (increases space to O(n²)):
        
        # self.board = [[0] * n for _ in range(n)]  # Track which cells are occupied
        # self.winner = 0                            # Track if game already finished
    
    def move(self, row: int, col: int, player: int) -> int:
        """
        Place a player's mark at (row, col) and check for win or draw.
        
        Args:
            row: Row index (0 to n-1)
            col: Column index (0 to n-1)
            player: Player number (1 or 2)
        
        Returns:
            - player (1 or 2): if that player wins with this move
            - -1: if the board is full with no winner (draw)
            - 0: if the game continues (no win, no draw yet)
        
        Time Complexity: O(1) - constant time updates and checks
        Space Complexity: O(1) - no additional space used per move
        
        Base checks NOT included (LeetCode 348 guarantees valid inputs):
        - Player is guaranteed to be 1 or 2
        - Position (row, col) is guaranteed to be in bounds: 0 ≤ row, col < n
        - Cell at (row, col) is guaranteed to be empty
        - No moves will be made after a win
        """
        
        # ============================================================
        # BASE CHECKS (Optional - commented out for LeetCode)
        # ============================================================
        # Uncomment these for production code with untrusted inputs
        # Note: Requires self.board and self.winner initialized in __init__
        
        # # 1. Validate player is 1 or 2
        # if player not in [1, 2]:
        #     raise ValueError("Player must be 1 or 2"")
        
        # # 2. Bounds check - ensure position is within board
        # # Valid positions: 0 ≤ row < n and 0 ≤ col < n
        # if not (0 <= row < self.n and 0 <= col < self.n):
        #     raise ValueError("Move out of bounds")
        
        # # 3. Game already finished - prevent moves after someone won
        # # Requires: self.winner initialized to 0 in __init__
        # if self.winner != 0:
        #     raise ValueError(f"Game already finished. Player {self.winner} won.")
        
        # # 4. Cell already occupied - prevent overwriting existing moves
        # # Requires: self.board initialized to [[0]*n for _ in range(n)] in __init__
        # # This increases space complexity from O(n) to O(n²)
        # if self.board[row][col] != 0:
        #     raise ValueError("Cell already occupied")
        
        # # Record move on board (needed for check #4 above)
        # self.board[row][col] = player
        
        # ============================================================
        # STEP 1: Convert player to increment value
        # ============================================================
        # Player 1 → +1, Player 2 → -1
        # This encoding allows us to use a single sum to track both players:
        # - Positive sum: Player 1 is ahead in that line
        # - Negative sum: Player 2 is ahead in that line
        # - Sum of +n: Player 1 completely filled that line (win!)
        # - Sum of -n: Player 2 completely filled that line (win!)
        value = 1 if player == 1 else -1
        
        # ============================================================
        # STEP 2: Update affected row sum
        # ============================================================
        # A move at (row, col) contributes to completing this specific row
        # We only update self.rows[row], not all rows, because only this row changed
        # Example: Move at (1, 2) updates self.rows[1] (row 1's sum)
        self.rows[row] += value
        
        # ============================================================
        # STEP 3: Update affected column sum
        # ============================================================
        # The same move also contributes to completing this specific column
        # We only update self.cols[col], not all columns
        # Example: Move at (1, 2) updates self.cols[2] (column 2's sum)
        self.cols[col] += value
        
        # ============================================================
        # STEP 4: Update main diagonal sum (conditionally)
        # ============================================================
        # Only update if this move is ON the main diagonal
        # Main diagonal condition: row == col
        # Example positions on main diagonal for 3x3: (0,0), (1,1), (2,2)
        # Example: Move at (1, 1) is on diagonal, so update self.diagonal
        #          Move at (1, 2) is NOT on diagonal, so skip this
        if row == col:
            self.diagonal += value
        
        # ============================================================
        # STEP 5: Update anti-diagonal sum (conditionally)
        # ============================================================
        # Only update if this move is ON the anti-diagonal
        # Anti-diagonal condition: row + col == n - 1
        # For n=3: positions (0,2), (1,1), (2,0) all satisfy 0+2=2, 1+1=2, 2+0=2
        # Example: Move at (0, 2) where n=3: 0+2=2=3-1 ✓ so update self.anti_diagonal
        #          Move at (0, 1) where n=3: 0+1=1≠2 ✗ so skip this
        if row + col == self.n - 1:
            self.anti_diagonal += value
        
        # ============================================================
        # STEP 6: Increment move counter
        # ============================================================
        # Track how many moves have been made total
        # Used for draw detection: when move_count == n², board is full
        # This is O(1) space - just one integer counter
        # self.move_count += 1
        
        # ============================================================
        # STEP 7: Check for WIN (must check BEFORE draw)
        # ============================================================
        # A player wins when ANY line is completely filled (sum reaches ±n)
        # We use abs() because:
        # - Player 1 win: sum = +n, abs(+n) = n
        # - Player 2 win: sum = -n, abs(-n) = n
        #
        # We check ONLY the lines affected by this move:
        # 1. self.rows[row]: The specific row where the move was placed
        # 2. self.cols[col]: The specific column where the move was placed
        # 3. self.diagonal: The main diagonal (if move is on it)
        # 4. self.anti_diagonal: The anti-diagonal (if move is on it)
        #
        # Why these specific checks?
        # - self.rows[row] is the sum for THIS row (e.g., row 0, 1, or 2), NOT sum of all rows
        # - self.cols[col] is the sum for THIS column (e.g., col 0, 1, or 2), NOT sum of all columns
        # - self.diagonal is the sum for THE one main diagonal
        # - self.anti_diagonal is the sum for THE one anti-diagonal
        #
        # We DON'T check sum(self.rows) because winning requires ONE complete line,
        # not marks scattered across multiple rows
        #
        # Example win scenarios (n=3):
        # - Row win: Player 1 fills row 0 → [X,X,X] → self.rows[0] = 3 → abs(3) == 3 ✓
        # - Col win: Player 2 fills col 1 → [O,O,O]ᵀ → self.cols[1] = -3 → abs(-3) == 3 ✓
        # - Diag win: Player 1 fills diagonal → self.diagonal = 3 → abs(3) == 3 ✓
        if (abs(self.rows[row]) == self.n or 
            abs(self.cols[col]) == self.n or
            abs(self.diagonal) == self.n or 
            abs(self.anti_diagonal) == self.n):
            # Optional: Track winner for base check #3
            # self.winner = player
            return player  # This player wins!
        
        # ============================================================
        # STEP 8: Check for DRAW (must check AFTER win)
        # ============================================================
        # Draw occurs when:
        # - Board is completely full (all n×n cells occupied), AND
        # - No player has won
        #
        # We detect full board by: move_count == n²
        # - n×n board has exactly n² cells
        # - Each move fills one cell (guaranteed unique per problem constraints)
        # - After n² moves, all cells are filled
        #
        # Important: We check this AFTER win detection because the last move
        # could complete a winning line. Example on 3×3 board:
        # - Move 9 (last move) completes row → return winner, not draw
        #
        # We can detect draw in O(1) space without storing the board!
        # if self.move_count == self.n * self.n:
        #     return -1  # Draw: board full, no winner
        
        # ============================================================
        # STEP 9: Game continues
        # ============================================================
        # No win detected, board not full → return 0 (game continues)
        return 0

# # Example 1: Player 1 wins with diagonal
# ticTacToe = TicTacToe(3)
# ticTacToe.move(0, 0, 1)  # return 0 (no winner)
# ticTacToe.move(0, 1, 2)  # return 0
# ticTacToe.move(1, 1, 1)  # return 0
# ticTacToe.move(0, 2, 2)  # return 0
# ticTacToe.move(2, 2, 1)  # return 1 (Player 1 wins)

# # Board state:
# # X O O
# # . X .
# # . . X
# # Player 1 completes main diagonal


# # Example 2: Player 2 wins with column
# ticTacToe = TicTacToe(3)
# ticTacToe.move(0, 0, 1)  # return 0
# ticTacToe.move(0, 1, 2)  # return 0
# ticTacToe.move(1, 0, 1)  # return 0
# ticTacToe.move(1, 1, 2)  # return 0
# ticTacToe.move(2, 2, 1)  # return 0
# ticTacToe.move(2, 1, 2)  # return 2 (Player 2 wins)

# # Board state:
# # X O .
# # X O .
# # . O X
# # Player 2 completes column 1


# # Example 3: Draw
# ticTacToe = TicTacToe(3)
# ticTacToe.move(0, 0, 1)  # return 0
# ticTacToe.move(0, 1, 2)  # return 0
# ticTacToe.move(0, 2, 1)  # return 0
# ticTacToe.move(1, 0, 2)  # return 0
# ticTacToe.move(1, 2, 1)  # return 0
# ticTacToe.move(1, 1, 1)  # return 0
# ticTacToe.move(2, 0, 2)  # return 0
# ticTacToe.move(2, 2, 2)  # return 0
# ticTacToe.move(2, 1, 1)  # return -1 (Draw)

# # Board state:
# # X O X
# # O X X
# # O X O
# # Board full, no winner

# Variant : isWin Function

# Problem Statement
# Assume the following rules are for the tic-tac-toe game on an 3 x 3 board between two players:

# A move is guaranteed to be valid and is placed on an empty block.
# Once a winning condition is reached, no more moves are allowed.
# A player who succeeds in placing n of their marks in a horizontal, vertical, or diagonal row wins the game.

# Write a function isWin(board, player, row, col) that takes a board state, player, and move and returns true if that player has won the game, and false otherwise.

# Constraints:

# 1. n == 3
# 2. player is 1 or 2.
# 3. 0 <= row, col < n
# 4. Only one call will be made to isWin.


# Example 1:

# Input:

# board = [
#     [1, 1, 0],
#     [2, 2, 0],
#     [0, 0, 0]
# ]

# player = 1
# row = 0
# col = 2

# Output: True

# Explanation:

# After move at (0, 2):

# [1, 1, 1]  ← Player 1 completes row 0
# [2, 2, 0]
# [0, 0, 0]

# Player 1 has 3 marks in row 0 (horizontal win).

# Example 2:

# Input:

# board = [
#     [1, 2, 0],
#     [2, 1, 0],
#     [0, 0, 0]
# ]
# player = 1
# row = 2
# col = 1

# Output: False

# Explanation:

# After move at (2, 1):
# [1, 2, 0]
# [2, 1, 0]
# [0, 1, 0]  ← Player 1 places mark

# def isWin(board, player, row, col):
#     """
#     Check if the move at (row, col) by player resulted in a win.
    
#     A player wins by placing n marks in a line. There are 4 possible winning lines:
#     1. Horizontal (complete row)
#     2. Vertical (complete column)
#     3. Main diagonal (top-left to bottom-right)
#     4. Anti-diagonal (top-right to bottom-left)
    
#     This version uses a SINGLE LOOP to check all 4 directions simultaneously,
#     making it more efficient than checking each line separately.
    
#     Args:
#         board: List[List[int]] - n x n board (0 = empty, 1 = player 1, 2 = player 2)
#         player: int - player number (1 or 2)
#         row: int - row index of the move (0 to n-1)
#         col: int - column index of the move (0 to n-1)
    
#     Returns:
#         bool - True if player won with this move, False otherwise
    
#     Time Complexity: O(n) - single pass through n positions
#     Space Complexity: O(1) - only use 4 counter variables
#     """
    
#     # ============================================================
#     # BASE CHECKS (Optional - uncomment for production)
#     # ============================================================
#     # if not board or len(board) == 0:
#     #     raise ValueError("Board cannot be empty")
    
#     # n = len(board)
#     # for i, r in enumerate(board):
#     #     if not r or len(r) != n:  # Handles None/empty rows + wrong length
#     #         raise ValueError("Board must be square")
    
#     # if player not in [1, 2]:
#     #     raise ValueError("Player must be 1 or 2")
    
#     # if not (0 <= row < n and 0 <= col < n):
#     #     raise ValueError("Move out of bounds")
    
#     # if board[row][col] != 0:
#     #     raise ValueError("Cell already occupied")

#     # # Validate all board values are 0, 1, or 2
#     # for i in range(n):
#     #     for j in range(n):
#     #         if board[i][j] not in [0, 1, 2]:
#     #             raise ValueError("Invalid board value")
    
    
#     # ============================================================
#     # CORE LOGIC
#     # ============================================================
    
#     board[row][col] = player
#     n = len(board)
    
#     # Initialize counters for all possible winning lines
#     rows = 0
#     cols = 0
#     diagonal = 0
#     anti_diagonal = 0
    
#     # Single loop to count all lines simultaneously (more efficient than 4 separate loops)
#     for i in range(n):
#         # Check row: count marks in affected row
#         if board[row][i] == player:
#             rows += 1
        
#         # Check column: count marks in affected column
#         if board[i][col] == player:
#             cols += 1
        
#         # Check main diagonal: ONLY if move is on it (row == col)
#         # Saves n comparisons when move is NOT on diagonal
#         if row == col and board[i][i] == player:
#             diagonal += 1
        
#         # Check anti-diagonal: ONLY if move is on it (row + col == n - 1)
#         # Saves n comparisons when move is NOT on anti-diagonal
#         if row + col == n - 1 and board[i][n - 1 - i] == player:
#             anti_diagonal += 1

#         # Optional: Early exit optimization
#         # Uncomment to return immediately when win is detected (can save iterations)
#         # Trade-off: Adds extra check per iteration but can exit early
#         # if rows == n or cols == n or diagonal == n or anti_diagonal == n:
#         #     return True
    
#     # Win if any line has n marks
#     # If diagonal wasn't checked (move not on it), diagonal stays 0, so diagonal == n is False (no false positive)
#     return rows == n or cols == n or diagonal == n or anti_diagonal == n


# Another approach : Built in function

# def isWin(board, player, row, col):
#     """
#     Check if the move at (row, col) by player resulted in a win.
    
#     A player wins by placing n marks in a line. There are 4 possible winning lines:
#     1. Horizontal (complete row)
#     2. Vertical (complete column)
#     3. Main diagonal (top-left to bottom-right)
#     4. Anti-diagonal (top-right to bottom-left)
    
#     This version uses a built-in function (all) instead of explicit loops.
    
#     Args:
#         board: List[List[int]] - n x n board (0 = empty, 1 = player 1, 2 = player 2)
#         player: int - player number (1 or 2)
#         row: int - row index of the move (0 to n-1)
#         col: int - column index of the move (0 to n-1)
    
#     Returns:
#         bool - True if player won with this move, False otherwise
    
#     Time Complexity: O(n) - check up to 4 lines of length n
#     Space Complexity: O(1) - no additional space used
#     """
    
#     board[row][col] = player
#     n = len(board)
    
#     # Check row: all cells in this row match player
#     if all(board[row][c] == player for c in range(n)):
#         return True
    
#     # Check column: all cells in this column match player
#     if all(board[r][col] == player for r in range(n)):
#         return True
    
#     # Check main diagonal: ONLY if move is on it (row == col)
#     if row == col and all(board[i][i] == player for i in range(n)):
#         return True
    
#     # Check anti-diagonal: ONLY if move is on it (row + col == n - 1)
#     if row + col == n - 1 and all(board[i][n - 1 - i] == player for i in range(n)):
#         return True
    
#     return False