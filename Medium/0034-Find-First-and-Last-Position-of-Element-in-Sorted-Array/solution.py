"""
LeetCode 34. Find First and Last Position of Element in Sorted Array
Difficulty: Medium
URL: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
"""

# Brute Force Approach : Linear Scan

# class Solution:
#     def searchRange(nums, target):
#         """
#         Brute Force: Single pass to find both positions.
        
#         Time Complexity: O(n) - scan entire array once
#         Space Complexity: O(1)

#         This violates the problem's requirement of O(log n) time.
#         """
#         if not nums:
#             return [-1, -1]

#         if target < nums[0] or target > nums[-1]:
#             return [-1, -1]
        
#         left_pos = -1
#         right_pos = -1
        
#         # Single pass: Update positions as we find target
#         for i in range(len(nums)):
#             if nums[i] == target:
#                 if left_pos == -1:
#                     # First occurrence found
#                     left_pos = i
#                 # Always update right position when we find target
#                 right_pos = i
        
#         # If target never found, both will be -1
#         return [left_pos, right_pos]

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        Find the starting and ending position of a given target value in a sorted 
        array.
    
        Args:
            nums: List[int] - sorted array in non-decreasing order
            target: int - target value to search for
        
        Returns:
            List[int] - [start_pos, end_pos] or [-1, -1] if not found
        
        Time Complexity: O(log n)
        Space Complexity: O(1)

        """

        def findLeft(nums, target):
            """
            Find the leftmost (first) occurrence of target using binary search.
            
            Strategy: When we find the target, we don't stop - we continue
            searching in the left half to find an earlier occurrence.
            """
            left, right = 0, len(nums) - 1
            result = -1  # -1 indicates target not found
            
            # WHY left <= right and NOT left < right?
            # We use <= because we need to check the case when left == right
            # (single element remaining). If we used <, we'd miss checking
            # the last remaining element.
            # Example: nums = [5], target = 5
            #   - Initially: left = 0, right = 0
            #   - With <=: We enter loop, check nums[0], find target ✓
            #   - With <: We skip loop entirely, return -1 ✗
            while left <= right:
                # Calculate middle index (avoids overflow compared to (left+right)/2)
                mid = (left + right) // 2
                
                if nums[mid] == target:
                    # Found target! But there might be earlier occurrences
                    result = mid  # Save this position
                    right = mid - 1  # Continue searching in left half
                    
                elif nums[mid] < target:
                    # Target is in the right half
                    left = mid + 1
                    
                else:  # nums[mid] > target
                    # Target is in the left half
                    right = mid - 1
                    
            return result
    
        def findRight(nums, target):
            """
            Find the rightmost (last) occurrence of target using binary search.
            
            Strategy: When we find the target, we don't stop - we continue
            searching in the right half to find a later occurrence.
            """
            left, right = 0, len(nums) - 1
            result = -1  # -1 indicates target not found
            
            # WHY left <= right and NOT left < right?
            # Same reason as findLeft - we need to check when left == right
            # to handle single element or last remaining element cases.
            while left <= right:
                # Calculate middle index
                mid = (left + right) // 2
                
                if nums[mid] == target:
                    # Found target! But there might be later occurrences
                    result = mid  # Save this position
                    left = mid + 1  # Continue searching in right half
                    
                elif nums[mid] < target:
                    # Target is in the right half
                    left = mid + 1
                    
                else:  # nums[mid] > target
                    # Target is in the left half
                    right = mid - 1
                    
            return result
        
        # ==================== Main Logic ====================
        
        # Base case: empty array
        if not nums:
            return [-1, -1]
        
        # Early exit optimization: Check if target is outside array bounds
        # Since array is sorted, if target is smaller than first element
        # or larger than last element, it cannot be in the array
        if target < nums[0] or target > nums[-1]:
            return [-1, -1]
        
        # Find the leftmost position of target
        left_pos = findLeft(nums, target)

        # Early exit: If leftmost position is -1, target doesn't exist
        # No need to search for rightmost position
        if left_pos == -1:
            return [-1, -1]
        
        # Find the rightmost position of target
        # We know target exists, so this will definitely find a position
        right_pos = findRight(nums, target)
        
        # Return the range [leftmost, rightmost]
        return [left_pos, right_pos]

# Alternative one-pass solution using single binary search function
class Solution:
    def searchRange(self, nums, target):
        """
        Alternative approach using a single helper function with a flag.
        
        Instead of two separate functions (findLeft and findRight), we use
        one function with a boolean parameter to control search direction.
        
        Pros: Less code duplication
        Cons: Slightly less readable than two separate functions
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        """
        
        def binarySearch(nums, target, findLeft):
            """
            Generic binary search that can find either leftmost or rightmost occurrence.
            
            Args:
                nums: sorted array
                target: value to search for
                findLeft: boolean flag
                    - True: find leftmost (first) occurrence
                    - False: find rightmost (last) occurrence
            
            Returns:
                Index of target (leftmost or rightmost based on flag), or -1 if not found
            """
            left, right = 0, len(nums) - 1
            result = -1  # -1 indicates target not found
            
            # WHY left <= right?
            # We need to check when left == right (single element remaining)
            # Using < would skip the last element
            while left <= right:
                # Calculate middle index
                mid = (left + right) // 2
                
                if nums[mid] == target:
                    # Found the target! But don't stop yet
                    result = mid  # Save current position
                    
                    # KEY DIFFERENCE: Direction controlled by findLeft flag
                    if findLeft:
                        # Looking for LEFTMOST occurrence
                        # Continue searching in left half for earlier occurrence
                        right = mid - 1
                    else:
                        # Looking for RIGHTMOST occurrence
                        # Continue searching in right half for later occurrence
                        left = mid + 1
                        
                elif nums[mid] < target:
                    # Target is in the right half
                    left = mid + 1
                    
                else:  # nums[mid] > target
                    # Target is in the left half
                    right = mid - 1
                    
            return result
        
        # ==================== Main Logic ====================
        
        # Base case: empty array
        if not nums:
            return [-1, -1]
        
        # Early exit optimization: Check if target is outside array bounds
        # Since array is sorted, if target is smaller than first element
        # or larger than last element, it cannot be in the array
        # This saves us from doing TWO binary searches unnecessarily
        if target < nums[0] or target > nums[-1]:
            return [-1, -1]
        
        # First call: Find LEFTMOST occurrence
        # Pass True to search for the first occurrence
        left_pos = binarySearch(nums, target, True)
        
        # Early exit: If leftmost position is -1, target doesn't exist
        # No need to search for rightmost position
        if left_pos == -1:
            return [-1, -1]
        
        # Second call: Find RIGHTMOST occurrence
        # Pass False to search for the last occurrence
        # We know target exists (left_pos != -1), so this will find a position
        right_pos = binarySearch(nums, target, False)
        
        # Return the range [leftmost, rightmost]
        return [left_pos, right_pos]



# Variant 1 : Count Occurrences of Target in Sorted Array

# Given an array of integers nums sorted in non-decreasing order, 
# count the number of occurrences of a given target value.

# You must write an algorithm with O(log n) runtime complexity.

# Example:
# Input: nums = [5,7,7,8,8,10], target = 8
# Output: 2
# Explanation: 8 appears twice in the array

# def countTarget(nums, target):
#     """
#     Count the number of occurrences of target in a sorted array.
    
#     Args:
#         nums: List[int] - sorted array in non-decreasing order
#         target: int - target value to count
    
#     Returns:
#         int - count of target occurrences
    
#     Time Complexity: O(log n)
#     Space Complexity: O(1)
#     """
#     def findLeft(nums, target):
#         """Find the leftmost occurrence of target"""
#         left, right = 0, len(nums) - 1
#         result = -1
        
#         while left <= right:
#             mid = (left + right) // 2
            
#             if nums[mid] == target:
#                 result = mid
#                 right = mid - 1  # Continue searching left
#             elif nums[mid] < target:
#                 left = mid + 1
#             else:
#                 right = mid - 1
                
#         return result
    
#     def findRight(nums, target):
#         """Find the rightmost occurrence of target"""
#         left, right = 0, len(nums) - 1
#         result = -1
        
#         while left <= right:
#             mid = (left + right) // 2
            
#             if nums[mid] == target:
#                 result = mid
#                 left = mid + 1   # Continue searching right
#             elif nums[mid] < target:
#                 left = mid + 1
#             else:
#                 right = mid - 1
                
#         return result
    
#     if not nums:
#         return 0

#     if target < nums[0] or target > nums[-1]:
#         return 0

#     left_pos = findLeft(nums, target)

#     if left_pos == -1:
#         return 0  # Target not found
    
#     right_pos = findRight(nums, target)
    
#     # Count = right_pos - left_pos + 1
#     return right_pos - left_pos + 1


# Variant 2 : Count Unique Elements in Sorted Array

# Given an array of integers nums sorted in non-decreasing order, count the number of unique (distinct) elements in the array.

# Examples:
#     Input: nums = [1, 1, 2, 2, 2, 3]
#     Output: 3
#     Explanation: The unique elements are 1, 2, and 3
    
#     Input: nums = [1, 2, 3, 4, 5]
#     Output: 5
#     Explanation: All elements are unique
    
#     Input: nums = [7, 7, 7, 7]
#     Output: 1
#     Explanation: Only one unique element (7)
    
#     Input: nums = []
#     Output: 0
#     Explanation: Empty array has no elements

# Note: Linear scan is more optimal O(n) vs O(k*log n).
# This binary search approach only wins when k << n (very few unique elements).

# def countUniqueElementsBinarySearch(nums):
#     """
#     Count unique elements using binary search.
    
#     Time: O(k * log n) where k = unique elements
#     Space: O(1)
    
#     Approach:
#         1. Start at first element
#         2. Binary search to find where it ends
#         3. Jump to next unique element
#         4. Repeat
    
#     Example: nums = [1, 1, 2, 2, 2, 3]
#                      ↑     ↑        ↑
#                      i=0   i=2      i=5
#         Step 1: i=0, find end of 1 at index 1, jump to i=2
#         Step 2: i=2, find end of 2 at index 4, jump to i=5
#         Step 3: i=5, find end of 3 at index 5, jump to i=6 (done)
#         Result: 3 unique
    
#     Why not findLeft()?
#         - We scan left-to-right, so 'i' is always the leftmost position
#         - We jump past complete groups: i = right_pos + 1
#         - Calling findLeft would just return 'i' (redundant)
    
#     When Binary Search WINS:
#         nums = [1]*500,000 + [2]*500,000  (n=1M, k=2)
#         Linear:  1,000,000 operations
#         Binary:  2 * log(1M) ≈ 40 operations  ✅ Binary wins!
    
#     When Linear WINS (most common):
#         nums = [1, 2, 3, ..., 1000]  (n=1000, k=1000, all unique)
#         Linear:  1,000 operations  ✅ Linear wins!
#         Binary:  1000 * log(1000) ≈ 10,000 operations
#     """
    
#     if not nums:
#         return 0
    
#     def findRight(nums, target):
#         """Find rightmost occurrence of target."""
#         left, right = 0, len(nums) - 1
#         result = -1
        
#         while left <= right:  # Use <= to check when left == right
#             mid = (left + right) // 2
            
#             if nums[mid] == target:
#                 result = mid
#                 left = mid + 1  # Continue searching right
#             elif nums[mid] < target:
#                 left = mid + 1
#             else:
#                 right = mid - 1
                
#         return result
    
#     unique_count = 0
#     i = 0  # i is always the leftmost position of current element
    
#     # Process array by jumping from one unique element to the next
#     # ⚠️  Note: Even though we "jump", we still examine O(n) positions
#     # in total across all jumps, then add O(k * log n) for binary searches.
#     # This is why the total complexity is O(k * log n), not better.

#     while i < len(nums):
#         current = nums[i]
        
#         # Use binary search to find where this element ends
#         # (rightmost occurrence of current element)
#         # 
#         # Why binary search instead of linear scan from i?
#         # If current element appears many times (e.g., 1000 times),
#         # binary search finds the end in ~log(n) steps,
#         # while linear scan would take 1000 steps.
#         # 
#         # However, this is the ONLY benefit, and it only helps when
#         # individual groups are large AND there are few unique elements.
#         right_pos = findRight(nums, current)
        
#         unique_count += 1
        
#         # Skip to next unique element
#         i = right_pos + 1
    
#     return unique_count

# def countUniqueElementsLinear(nums):
#     """
#     ✅ OPTIMAL SOLUTION - Linear scan
    
#     Time: O(n) - always optimal, matches lower bound
#     Space: O(1)
    
#     Why better than binary search:
#         - Must examine every element anyway (lower bound is Ω(n))
#         - Binary search is O(k*log n), worst case O(n*log n) when k=n
#         - Simpler code, better cache locality
    
#     When Linear WINS (common):
#         Example 1: nums = [1, 2, 3, 4, 5] (all unique, k=n)
#             Linear:  5 operations  ✅
#             Binary:  5 * log(5) ≈ 12 operations
        
#         Example 2: nums = [1,1,2,2,3,3,4,4,5,5] (k=n/2)
#             Linear:  10 operations  ✅
#             Binary:  5 * log(10) ≈ 17 operations
    
#     When Binary WINS (rare):
#         Example: nums = [1]*1M + [2]*1M (only 2 unique, k=2)
#             Linear:  2,000,000 operations
#             Binary:  2 * log(2M) ≈ 42 operations  ✅
#             BUT: This scenario is uncommon in practice!
    
#     Use this for production code!
#     """
#     if not nums:
#         return 0
    
#     unique_count = 1  # First element always unique
    
#     for i in range(1, len(nums)):
#         if nums[i] != nums[i-1]:
#             unique_count += 1
    
#     return unique_count
 
        
        