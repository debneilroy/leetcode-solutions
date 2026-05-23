"""
LeetCode 605. Can Place Flowers
Difficulty: Easy
URL: https://leetcode.com/problems/can-place-flowers/
"""

# Brute Force 

# Approach: Try all possible combinations of placing n flowers in valid positions using backtracking/recursion.

# How it works:

# For each empty position, try planting a flower
# Recursively attempt to place the remaining flowers
# If it fails, backtrack (remove the flower) and try the next position
# Return true if we successfully place all n flowers

# Complexity:

# Time: O(2^n) - exponential, trying many combinations
# Space: O(n) - recursion call stack

# Why it's inefficient: Explores many unnecessary combinations when a simple greedy left-to-right scan works perfectly.

# The key insight: Greedy works! Planting flowers as early as possible never hurts, so we don't need to try all combinations. This reduces O(2^n) → O(n). 

# Input: flowerbed = [0,0,0], n = 2
# Attempt 1: Plant at positions [0, 1]
# [1,1,0] → Invalid! (adjacent flowers) ❌

# Attempt 2: Plant at positions [0, 2]
# [1,0,1] → Valid! ✓ → Return True

# The brute force explores multiple possibilities even though some are obviously invalid.

# ### Greedy approach (optimal):

# Scan left to right:
# i=0: [0,0,0] → empty, left OK, right OK → Plant!
#      [1,0,0], placed=1

# i=1: [1,0,0] → empty, left=1 → Can't plant, skip

# i=2: [1,0,0] → empty, left OK, right OK → Plant!
#      [1,0,1], placed=2 ✓ → Return True

# Approach : Single Scan

class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        """
        Time Complexity: O(n) where n is the length of flowerbed
            - Single pass through the array
            - Each position checked once
        
        Space Complexity: O(1)
            - Only uses constant extra space (count, length, i, empty_left, empty_right)
            - Modifies input array in-place but doesn't use additional data structures
        """
        if n == 0:
            return True

        count = 0
        length = len(flowerbed)
        
        for i in range(length):
            # Check if current position is empty
            if flowerbed[i] == 0:
                # Check left neighbor (empty or out of bounds)
                empty_left = (i == 0) or (flowerbed[i - 1] == 0)
                # Check right neighbor (empty or out of bounds)
                empty_right = (i == length - 1) or (flowerbed[i + 1] == 0)
                
                # If both neighbors are empty, we can plant here
                if empty_left and empty_right:
                    flowerbed[i] = 1  # Plant the flower
                    count += 1
                    
                    # Early exit if we've planted enough flowers
                    if count >= n:
                        return True
        
        # Early exit guarantees count >= n is caught inside the loop for n > 0.
        # Without the n == 0 base check, we'd need `return count >= n` here
        # since count=0 >= n=0 would be True but never caught by the early exit.
        # e.g. flowerbed=[1], n=0 -> loop skipped (flowerbed[0]=1), count=0 >= n=0 -> True, not False.
        return False

# Approach : Intelligent position skipping (preferred in interview)

# class Solution:
#     def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
#         """
#         Determine if n flowers can be planted using an optimized greedy approach
#         with intelligent position skipping.
        
#         Time Complexity: O(n) worst case, but ~O(n/2) average case
#             - Skips positions aggressively (jumps by 2 or 3)
#             - Approximately 2x faster than standard approach in practice
        
#         Space Complexity: O(1)
#             - Only uses constant extra space
#             - Does NOT modify the input array
        
#         Approach:
#             Greedy with optimized skipping:
#             - When we plant: skip next position (i += 2)
#             - When there's a flower: skip next position (i += 2)
#             - When blocked by neighbor: skip 3 positions (i += 3)
#         """
#         i = 0  # Current position
#         placed = 0  # Count of flowers successfully placed
        
#         while i < len(flowerbed):
#             # Check left neighbor: treat boundary as empty (0)
#             empty_left_plot = 0 if i == 0 else flowerbed[i - 1]
            
#             # Check right neighbor: treat boundary as empty (0)
#             empty_right_plot = 0 if i == len(flowerbed) - 1 else flowerbed[i + 1]
            
#             # Case 1: Current position and both neighbors are empty - plant here!
#             if flowerbed[i] == empty_left_plot == empty_right_plot == 0:
#                 placed += 1
#                 i += 2  # Skip next position (can't plant adjacent)
            
#             # Case 2: Current position has a flower - skip it
#             elif flowerbed[i]:
#                 i += 2  # Skip next position (can't plant adjacent to existing flower)
            
#             # Case 3: Current is empty but blocked by a neighbor
#             else:
#                 i += 3  # Jump 3 positions (next valid spot is at least 2 away), flowerbed = [0,1,0,0], n = 2
            
#             # Early exit optimization: if we've placed enough flowers
#             if placed >= n:
#                 return True

#         # Return False instead of (placed >= n) because:
#         # If we had placed >= n flowers, we would have already returned True
#         # in the early exit check above. Reaching here means placed < n.
#         # Using False is clearer and avoids redundant comparison.
        
#         return False

# Variant : Return the most number of flowers that can be planted in the flowerbed without violating the 
# no-adjacent-flowers rule

# class Solution:
#     def placeFlowers(self, flowerbed: List[int]) -> int:
#         i = 0
#         placed = 0
#         while i < len(flowerbed):
#             empty_left_plot = 0 if i == 0 else flowerbed[i - 1]
#             empty_right_plot = 0 if i == len(flowerbed) - 1 else flowerbed[i + 1]
#             if flowerbed[i] == empty_left_plot == empty_right_plot == 0:
#                 placed += 1
#                 i += 2
#             elif flowerbed[i]:
#                 i += 2 
#             else:
#                 i += 3

#         return placed