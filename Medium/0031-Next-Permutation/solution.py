"""
LeetCode 31. Next Permutation
Difficulty: Medium
URL: https://leetcode.com/problems/next-permutation/
"""

# Brute Force Approach

# Generate all possible permutations of the list.

# Sort them lexicographically.

# Find the current permutation in that sorted list.

# Return the next one, or the first one if the current is the last.

# Time Complexity : O(n!×nlogn) — generating & sorting all permutations
# Space Complexity : O(n!×n) — to store all permutations

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Rearranges numbers into the lexicographically next greater permutation.
        If such arrangement is not possible, it must rearrange it as the lowest 
        possible order (i.e., sorted in ascending order).
        
        Algorithm:
        1. Find the largest index i such that nums[i] < nums[i + 1] (pivot point)
        2. If no such index exists, the permutation is the last permutation
        3. Find the largest index j greater than i such that nums[i] < nums[j]
        4. Swap the value of nums[i] with that of nums[j]
        5. Reverse the sequence from nums[i + 1] up to and including the final element

        Visual Example:

        Array: [1, 3, 5, 4, 2]

        Next Permutation:
        Step 1: Find pivot where nums[i] < nums[i+1]
                [1, 3, 5, 4, 2]
                    ↑
                i=1 (3 < 5)

        Step 2: Find smallest element > nums[i] on the right
                [1, 3, 5, 4, 2]
                    ↑     ↑
                i=1   j=3
                nums[3]=4 is smallest element > 3

        Step 3: Swap nums[1] and nums[3]
                [1, 4, 5, 3, 2]

        Step 4: Reverse from i+1 to end
                [1, 4, 5, 3, 2] → [1, 4, 2, 3, 5]
                        -------
                        reverse

        Result: [1, 4, 2, 3, 5]
        
        Edge Cases Handled:
        1. Single element array [5]: Returns unchanged (only one permutation)
        2. Two elements ascending [1,2]: Swaps to [2,1]
        3. Two elements descending [2,1]: Reverses to [1,2]
        4. Already in descending order [3,2,1]: Wraps to first permutation [1,2,3]
        5. Already in ascending order [1,2,3]: Returns next permutation [1,3,2]
        6. Duplicate elements [1,3,3,2]: Uses >= and <= to skip duplicates correctly
        7. All elements same [2,2,2]: Returns unchanged (only one unique permutation)
        8. Negative numbers [-1,2,3]: Works with any integers
        9. Pivot at second-to-last position [1,2,3]: Handles single-element suffix
        
        Time Complexity: O(n)
            - Finding pivot: O(n) in worst case
            - Finding swap target: O(n) in worst case
            - Reversing suffix: O(n) in worst case
            - Total: O(n) as we traverse the array at most 3 times
        
        Space Complexity: O(1)
            - Only using a constant amount of extra space for variables (i, j, left, right)
            - Modifying the array in-place
        
        Args:
            nums: List[int] - Array of integers to permute
            
        Returns:
            None - Modifies nums in-place
        """
        n = len(nums)
        
        # Optional: Early return for single element (not strictly necessary)
        # The algorithm handles n=1 correctly without this check
        if n <= 1:
            return
        
        # Step 1: Find the pivot point
        # WHY RIGHT-TO-LEFT? We want the SMALLEST possible increase, which means
        # changing the rightmost position possible (like incrementing 1299→1300, 
        # not 1299→2000). For arrays, [1,3,5,4,2]→[1,4,2,3,5] is next, not [2,1,3,4,5].
        # This finds the IMMEDIATE next permutation, not just any larger one.
        
        # Traverse from right to left to find the first pair where nums[i] < nums[i+1]
        # This is the rightmost position where we can make an increase
        # Note: Using >= (not just >) to skip duplicate values
        # Example: [1,3,3,2] correctly skips the duplicate 3's to find pivot at i=0
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        
        # At this point:
        # - If i >= 0: Found a pivot, can create next permutation
        # - If i == -1: No pivot found, array is in descending order (last permutation)
        
        # Step 2: If pivot exists, find the element to swap with
        if i >= 0:
            # Find the smallest element greater than nums[i] to the right of i
            # WHY SMALLEST? We want the minimal increase at position i to get the 
            # IMMEDIATE next permutation, not one further ahead. For [1,3,5,4,2] with 
            # pivot=3, swapping with 4 (smallest>3) gives [1,4,2,3,5] (next), while 
            # swapping with 5 gives [1,5,2,3,4] (jumps too far).

            # Everything to the right of i is in descending order,
            # so we search from right to left for the first element > nums[i]
            # Note: Using <= (not just <) to skip elements equal to nums[i]
            # Example: [1,5,1,1,1] correctly skips duplicate 1's to find j=1 (value 5)
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            
            # Swap nums[i] and nums[j]
            # This creates the next larger permutation at position i
            # IMPORTANT: This swap MUST be inside the if block! When i == -1 (no pivot),
            # j is never created, and swapping outside would cause UnboundLocalError.
            nums[i], nums[j] = nums[j], nums[i]
        
        # Step 3: Reverse the suffix after index i
        # The suffix (from i+1 to end) is currently in descending order
        # Reversing it produces ascending order, giving us the smallest possible suffix
        # This ensures we get the NEXT permutation, not just any larger one

        # Note: We use manual two-pointer reversal instead of Python built-ins because:
        # - nums[i+1:] = nums[i+1:][::-1] creates O(n) space (two temporary lists from slicing)
        # - nums[i+1:] = reversed(nums[i+1:]) creates O(n) space (slicing creates a list)
        # - Manual reversal maintains true O(1) space and is more interview-appropriate
        
        # Special cases handled automatically:
        # - When i == -1 (last permutation): Reverses entire array from index 0
        #   Example: [3,2,1] → i=-1, reverses [3,2,1] → [1,2,3]
        # - When i == n-2 (pivot at second-to-last): Suffix has 1 element, no reversal needed
        #   Example: [1,2,3] → i=1, after swap [1,3,2], suffix is [2] (left=right=2)
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

        
# Variant : Previous Permutation

# A permutation of an array of integers is an arrangement of its members into a sequence or linear order. For example, for arr = [1,2,3], the following are all the permutations of arr: [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1].

# The previous permutation of an array of integers is the previous lexicographically smaller permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the previous permutation of that array is the permutation that precedes it in the sorted container. If such arrangement is not possible, the array must be rearranged as the highest possible order (i.e., sorted in descending order).

# For example, the previous permutation of arr = [1,2,3] is [3,2,1].
# For example, the previous permutation of arr = [2,3,1] is [2,1,3].

# Given an array of integers nums, find the previous permutation of nums.
# The replacement must be in place and use only constant extra memory.

# Example 1:
# Input: nums = [1,4,2,3,5]
# Output: [1,3,5,4,2]
# Explanation: The previous permutation in lexicographical order is [1,3,5,4,2].

# Example 2:
# Input: nums = [3,2,1]
# Output: [3,1,2]
# Explanation: [3,2,1] is not the first (smallest) permutation, so we find the previous one.

# Example 3:
# Input: nums = [1,2,3]
# Output: [3,2,1]
# Explanation: [1,2,3] is the first (smallest) permutation in ascending order, so the previous permutation wraps around to the last (largest) permutation in descending order.

# Example 4:
# Input: nums = [1,1,5]
# Output: [1,1,5]
# Explanation: The previous permutation is [1,1,5] itself (there are only 3 unique permutations: [1,1,5], [1,5,1], [5,1,1]).

# class Solution:
#     def previousPermutation(self, nums: List[int]) -> None:
#         """
#         Rearranges numbers into the lexicographically previous smaller permutation.
#         If such arrangement is not possible, it must rearrange it as the highest 
#         possible order (i.e., sorted in descending order).
        
#         The replacement must be in place and use only constant extra memory.
        
#         Algorithm:
#         1. Find the largest index i such that nums[i] > nums[i + 1] (pivot point)
#            [REVERSED from next: was nums[i] < nums[i + 1]]
#         2. If no such index exists, the permutation is the first permutation
#         3. Find the largest index j greater than i such that nums[j] < nums[i]
#            [REVERSED from next: was nums[j] > nums[i]]
#         4. Swap the value of nums[i] with that of nums[j]
#         5. Reverse the sequence from nums[i + 1] up to and including the final element

#         Visual Example:

#         Array: [1, 4, 2, 3, 5]

#         Previous Permutation:
#         Step 1: Find pivot where nums[i] > nums[i+1]
#                 [1, 4, 2, 3, 5]
#                     ↑
#                 i=1 (4 > 2)

#         Step 2: Find largest element < nums[i] on the right
#                 [1, 4, 2, 3, 5]
#                     ↑     ↑
#                 i=1   j=3
#                 nums[3]=3 is largest element < 4

#         Step 3: Swap nums[1] and nums[3]
#                 [1, 3, 2, 4, 5]

#         Step 4: Reverse from i+1 to end
#                 [1, 3, 2, 4, 5] → [1, 3, 5, 4, 2]
#                         -------
#                         reverse

#         Result: [1, 3, 5, 4, 2]
        
#         Edge Cases Handled:
#         1. Single element array [5]: Returns unchanged (only one permutation)
#         2. Two elements descending [2,1]: Swaps to [1,2]
#         3. Two elements ascending [1,2]: Reverses to [2,1]
#         4. Already in ascending order [1,2,3]: Wraps to last permutation [3,2,1]
#         5. Already in descending order [3,2,1]: Returns previous permutation [3,1,2]
#         6. Duplicate elements [5,1,1]: Uses <= and >= to skip duplicates correctly
#         7. All elements same [2,2,2]: Returns unchanged (only one unique permutation)
#         8. Negative numbers [-1,3,2]: Works with any integers
#         9. Pivot at second-to-last position [3,2,1]: Handles single-element suffix
        
#         Time Complexity: O(n)
#             - Finding pivot: O(n) in worst case
#             - Finding swap target: O(n) in worst case
#             - Reversing suffix: O(n) in worst case
#             - Total: O(n) as we traverse the array at most 3 times
        
#         Space Complexity: O(1)
#             - Only using a constant amount of extra space for variables (i, j, left, right)
#             - Modifying the array in-place
        
#         Args:
#             nums: List[int] - Array of integers to permute
            
#         Returns:
#             None - Modifies nums in-place
#         """
#         n = len(nums)
        
#         # Optional: Early return for single element (not strictly necessary)
#         # The algorithm handles n=1 correctly without this check
#         if n <= 1:
#             return
        
#         # Step 1: Find the pivot point
#         # Traverse from right to left to find the first pair where nums[i] > nums[i+1]
#         # This is the rightmost position where we can make a decrease
#         # [KEY DIFFERENCE: Next uses < to find increase, Previous uses > to find decrease]
#         # Note: Using <= (not just <) to skip duplicate values
#         # Example: [5,3,3,1] correctly skips the duplicate 3's to find pivot at i=0
#         i = n - 2
#         while i >= 0 and nums[i] <= nums[i + 1]:  # [REVERSED: Next uses >=]
#             i -= 1
        
#         # At this point:
#         # - If i >= 0: Found a pivot, can create previous permutation
#         # - If i == -1: No pivot found, array is in ascending order (first permutation)
        
#         # Step 2: If pivot exists, find the element to swap with
#         if i >= 0:
#             # Find the largest element smaller than nums[i] to the right of i
#             # [KEY DIFFERENCE: Next finds smallest element greater than nums[i]]
#             # Everything to the right of i is in ascending order,
#             # [REVERSED: Next has descending order]
#             # so we search from right to left for the first element < nums[i]
#             # Note: Using >= (not just >) to skip elements equal to or greater than nums[i]
#             # Example: [5,1,5,5,5] correctly skips duplicate 5's to find j=1 (value 1)
#             j = n - 1
#             while nums[j] >= nums[i]:  # [REVERSED: Next uses <=]
#                 j -= 1
            
#             # Swap nums[i] and nums[j]
#             # This creates the previous smaller permutation at position i
#             # IMPORTANT: This swap MUST be inside the if block! When i == -1 (no pivot),
#             # j is never created, and swapping outside would cause UnboundLocalError.
#             nums[i], nums[j] = nums[j], nums[i]
        
#         # Step 3: Reverse the suffix after index i
#         # The suffix (from i+1 to end) is currently in ascending order
#         # Reversing it produces descending order, giving us the largest possible suffix
#         # This ensures we get the PREVIOUS permutation, not just any smaller one
#         # 
#         # Special cases handled automatically:
#         # - When i == -1 (first permutation): Reverses entire array from index 0
#         #   Example: [1,2,3] → i=-1, reverses [1,2,3] → [3,2,1]
#         # - When i == n-2 (pivot at second-to-last): Suffix has 1 element, no reversal needed
#         #   Example: [3,2,1] → i=1, after swap [3,1,2], suffix is [2] (left=right=2)
#         left, right = i + 1, n - 1
#         while left < right:
#             nums[left], nums[right] = nums[right], nums[left]
#             left += 1
#             right -= 1



# Core Principle

# Next Permutation: Make the smallest possible increase by finding where we can "bump up" a digit
# Previous Permutation: Make the smallest possible decrease by finding where we can "bump down" a digit


# Example: [1, 2, 3]
# Finding NEXT Permutation: [1, 2, 3] → ?
# Step-by-step thinking:

# "Where can I make an increase?"

# Scan from right to left looking for a pair where left < right (an upward step)
# [1, 2, 3]: Start at the end
# [1, 2, 3]: Is 2 < 3? YES! Found an upward step!
# We can increase position 2 by swapping with 3

# Make the swap:

# [1, 2, 3] → [1, 3, 2] ✓

# Intuition: We found the rightmost "upward step" (2 < 3), swapped them to make the smallest increase!



# Finding PREVIOUS Permutation: [1, 2, 3] → ?
# Step-by-step thinking:

# "Where can I make a decrease?"

# Scan from right to left looking for a pair where left > right (a downward step/drop)
# [1, 2, 3]: Start at the end
# [1, 2, 3]: Is 2 > 3? NO (2 < 3, it's going UP, not down)
# [1, 2, 3]: Is 1 > 2? NO (1 < 2, still going UP)
# No downward step found! The array is continuously ascending.

# "It's already the first (smallest) permutation!"

# Since everything is increasing (1 < 2 < 3), there's no way to make it smaller
# Wrap around to the LAST (largest) permutation
# Reverse everything: [1, 2, 3] → [3, 2, 1] ✓