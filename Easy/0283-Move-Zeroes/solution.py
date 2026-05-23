"""
LeetCode 283. Move Zeroes
Difficulty: Easy
URL: https://leetcode.com/problems/move-zeroes/
"""

# Brute Force : Keep bubbling zeros to the right

# class Solution:
#     def moveZeroes(self, nums):
#         """
#         Time Complexity : O(n^2)
#         Space Complexity : O(1)
#         """
#         # OUTER LOOP: Make multiple passes through the array
#         # We need len(nums) passes to ensure all zeros reach the end
#         for i in range(len(nums)):
#             for j in range(len(nums) - 1):
#                 if nums[j] == 0 and nums[j+1] != 0:
#                     # This moves the zero one step closer to the end
#                     # and moves the non-zero one step closer to the front
#                     nums[j], nums[j+1] = nums[j+1], nums[j]

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        This version swaps elements.
        
        Advantage: Preserves original values during the process
        Time Complexity: O(n) - single pass through array
        Space Complexity: O(1) - only using two pointer variables
        """
        # BASE CASE: Empty array or single element
        if not nums or len(nums) == 1:
            return

        # 'left' pointer: tracks position of next zero that needs to be swapped
        left = 0
        
        # Scan through entire array
        for right in range(len(nums)):
            # When we find a non-zero element
            if nums[right] != 0:
                # Swap it with element at 'left' position
                # This moves non-zero elements forward and zeros backward
                nums[left], nums[right] = nums[right], nums[left]
                
                # Move 'left' pointer forward
                # Now nums[left-1] is guaranteed to be non-zero
                left += 1

# Variant : Move zeros to the front

# def move_zeroes_to_front(nums):
#     """
#     Move all zeroes to the front while maintaining relative order of non-zero elements.
    
#     Key insight: Scan backwards, swap non-zeros backwards → preserves forward order!
    
#     Args:
#         nums: List[int] - input array to modify in-place
    
#     Time Complexity: O(n) - single pass
#     Space Complexity: O(1) - only using swap_index variable
    
#     Example: [0,1,0,3,12] becomes [0,0,1,3,12]
#     """
#     if not nums or len(nums) == 1:
#         return
    
#     # Start swap_index at the rightmost position
#     swap_index = len(nums) - 1
    
#     # Scan backwards through the array
#     for i in range(len(nums) - 1, -1, -1):
#         # When we find a non-zero element
#         if nums[i] != 0:
#             # Swap it with the element at swap_index
#             nums[i], nums[swap_index] = nums[swap_index], nums[i]
#             # Move swap_index one position to the left
#             swap_index -= 1

        