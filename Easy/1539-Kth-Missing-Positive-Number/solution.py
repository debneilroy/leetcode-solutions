"""
LeetCode 1539. Kth Missing Positive Number
Difficulty: Easy
URL: https://leetcode.com/problems/kth-missing-positive-number/
"""

# Approach : Brute Force

# Every time we see a number num that’s ≤ k, it means that number is not missing, so the k-th missing number must occur one step later in the sequence — that’s why we increment k by 1. Once we hit a number greater than k, we know all k missing numbers occur before it,so k itself is our answer.

# Visual analogy

# Think of a line of numbers:

# 1 2 3 4 5 6 7 8 9 10 11

# And the array occupies:

# [2,3,4,7,11]

# We’re initially aiming for the 5th missing number (k = 5).

# Now watch how the target shifts as we see existing numbers:

# Seen    Missing numbers so far    Target shifts to
# 2       [1]                        +1 → k = 6
# 3       [1]                        +1 → k = 7
# 4       [1]                        +1 → k = 8
# 7       [1, 5, 6]                  +1 → k = 9
# 11      [1, 5, 6, 8, 9, 10]        stop (since 11 > 9)

# So the 5th missing number is 9.

# Why Target Shifts by +1?

# The key is: we only shift when we see a number ≤ k.
# When we see a number ≤ k, it means:

# This number is occupying one of the first k positions
# So one of the positions we were counting is "taken"
# We need to look one position further to find the kth missing

# Detailed Explanation
# Initial: k = 5 (we want the 5th missing number)
# When we see 2:
# Question: Is 2 ≤ 5? YES

# Think of positions 1,2,3,4,5:
# - Position 2 is occupied by the number 2
# - So position 2 is NOT a missing number
# - Originally we thought: "5th missing is somewhere in positions 1-5"
# - But position 2 is taken, so we need to expand our search
# - New range: positions 1-6 (shift by +1)

# k = 5 + 1 = 6
# When we see 3:
# Question: Is 3 ≤ 6? YES

# Position 3 is also occupied
# We lose another position to a present number
# Need to expand search range again

# k = 6 + 1 = 7
# When we see 4:
# Question: Is 4 ≤ 7? YES

# Position 4 is occupied
# Shift again

# k = 7 + 1 = 8
# When we see 7:
# Question: Is 7 ≤ 8? YES

# Position 7 is occupied
# Shift again

# k = 8 + 1 = 9
# When we see 11:
# Question: Is 11 ≤ 9? NO

# 11 is beyond our current target position
# This number doesn't affect our search
# Don't shift, STOP here

# Answer: k = 9

class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        """
        Linear approach: iterate through the array and count missing numbers.
        
        Key Idea: If a number in the array is <= k, it means one of the first k
        positive integers is present, so we need to look one position further.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """

        # Defensive check (not required by LeetCode constraints)
        if k <= 0:
            return -1

        # If array is empty, kth missing number is simply k
        if not arr:
            return k
            
        # Iterate through each number in the array
        for num in arr:
            # If num <= k, it means num is occupying a spot in the first k positions
            # So we need to shift our target forward by 1
            if num <= k:
                k += 1  # Increment k to compensate for this present number
            else: # or elif num > k:
                # Once we find a number > k, we can stop early
                # All remaining numbers won't affect our answer
                break
        
        # After adjusting k for all present numbers, k is our answer
        return k

# Approach : Binary Search 

class Solution:
    def findKthPositive(self, arr: list[int], k: int) -> int:
        """
        Find the kth missing positive number in a sorted array using binary search.
        
        Time Complexity: O(log n) where n is the length of arr
        Space Complexity: O(1)
        """
        left, right = 0, len(arr) - 1  # Search in [0, len(arr)-1]
        
        # Binary search to find the position where kth missing number lies
        # We use 'left <= right' template (standard for finding boundaries):
        #   - Allows left and right to meet at the same index
        #   - Loop ends when left = right + 1
        #   - Gives clear boundary: arr[right] has missing<k, arr[left] has missing>=k
        #
        # Alternative: 'left < right' template would require:
        #   1. Initialize: right = len(arr) (not len(arr)-1)
        #   2. Update: right = pivot (not pivot-1)
        #   3. Same return: left + k
        while left <= right:
            # Calculate middle index
            # Two equivalent formulas:
            #   1. pivot = (left + right) // 2
            #      - Simpler but can overflow in languages like C++/Java when left+right > INT_MAX
            #   2. pivot = left + (right - left) // 2  (recommended)
            #      - Prevents overflow, works in all languages
            #      - Note: Use // (integer division), not / (float division)
            pivot = (left + right) // 2 
            
            # Count of missing positive integers before arr[pivot]
            # Formula derivation:
            #   - Total positive integers in range [1, arr[pivot]] = arr[pivot]
            #   - Existing elements from index 0 to pivot = pivot + 1
            #   - Missing = Total - Existing
            #             = arr[pivot] - (pivot + 1)
            # 
            # Example: arr=[2,3,4,7,11], pivot=3
            #   Range [1, 7]: total integers = 7
            #   Existing elements at indices [0,1,2,3] = 4 elements
            #   Missing = 7 - 4 = 3 (which are: 1, 5, 6) ✓
            missing = arr[pivot] - pivot - 1
            
            if missing < k:
                # Not enough missing numbers before arr[pivot]
                # The kth missing must be to the right
                left = pivot + 1
            else:
                # We have k or more missing numbers before arr[pivot]
                # The kth missing could be before or at this position
                right = pivot - 1
        
        # Loop ends when left = right + 1
        # At this point:
        # - arr[right] is the LAST element where (arr[right] - right - 1) < k
        # - arr[left] is the FIRST element where (arr[left] - left - 1) >= k  
        #   (or left = len(arr) if we've gone past the array)
        #
        # Derivation of left + k:
        # Missing before arr[right] = arr[right] - right - 1
        # We need k missing numbers total
        # Additional missing needed after arr[right] = k - (arr[right] - right - 1)
        # kth missing number = arr[right] + additional missing
        #                    = arr[right] + k - (arr[right] - right - 1)
        #                    = arr[right] + k - arr[right] + right + 1
        #                    = k + right + 1
        #                    = k + left  (since left = right + 1)

        # Quick explanation (for interview):
        # After binary search, we have 'right+1' array elements before our answer.
        # These elements "push" the kth missing number forward by (right+1) positions.
        # So kth missing is at position: k + (right + 1) = k + left
        return left + k


# Variant (Leetcode 1060) : Given an integer array nums which is sorted in ascending order and all of its elements are unique, and also given an integer k, return the kᵗʰ missing number starting from the leftmost number of the array.

# Example 1

# Input:
# nums = [4,7,9,10], k = 1
# Output:
# 5
# Explanation:
# The first missing number is 5.

# Example 2

# Input:
# nums = [4,7,9,10], k = 3
# Output:
# 8
# Explanation:
# The missing numbers are [5,6,8,...], hence the 3rd missing number is 8.

# Example 3

# Input:
# nums = [1,2,4], k = 3
# Output:
# 6
# Explanation:
# The missing numbers are [3,5,6,7,...], hence the 3rd missing number is 6.

# Constraints

# 1 ≤ nums.length ≤ 5 × 10⁴

# 1 ≤ nums[i] ≤ 10⁷

# nums is sorted in ascending order, and all elements are unique.

# 1 ≤ k ≤ 10⁸

# class Solution:
#     def missingElement(self, nums: list[int], k: int) -> int:
#         """
#         Find the kth missing number starting from nums[0].
        
#         Key difference from LC1539: We start counting from nums[0], not from 1.
        
#         Time Complexity: O(log n) using binary search
#         Space Complexity: O(1)
#         """
#         left = 0
#         right = len(nums) - 1  # Search in [0, len(nums)-1]
        
#         # Binary search to find the position where kth missing number lies
#         while left <= right:
#             mid = (right - left) // 2 + left
            
#             # Count of missing numbers between nums[0] and nums[mid]
#             # Formula derivation:
#             #   - Total positive integers in range [nums[0], nums[mid]] = nums[mid] - nums[0] + 1
#             #   - Existing positive inetgers from index 0 to mid = mid + 1
#             #   - Missing = Total - Existing
#             #             = (nums[mid] - nums[0] + 1) - (mid + 1)
#             #             = nums[mid] - nums[0] - mid
#             # 
#             # Example: nums=[4,7,9,10], mid=2
#             #   Range [4, 9]: total integers = 9-4+1 = 6 integers
#             #   Existing elements at indices [0,1,2] = 3 elements
#             #   Missing = 6 - 3 = 3 (which are: 5, 6, 8) ✓
#             missing = nums[mid] - nums[0] - mid
            
#             if missing < k:
#                 # Not enough missing numbers before nums[mid]
#                 # The kth missing must be to the right
#                 left = mid + 1
#             else:
#                 # We have k or more missing numbers before nums[mid]
#                 # The kth missing could be before or at this position
#                 right = mid - 1
        
#         # Loop ends when left = right + 1
#         # At this point:
#         # - nums[right] is the LAST element where nums[right] - nums[0] - right < k
#         # - nums[left] is the FIRST element where nums[left] - nums[0] - left >= k (or left = len(nums))
#         # - The kth missing number is BETWEEN nums[right] and nums[left]
#         #
#         # Derivation of nums[0] + k + right:
#         # Missing before nums[right] = nums[right] - nums[0] - right
#         # We need k missing numbers total
#         # Additional missing needed after nums[right] = k - (nums[right] - nums[0] - right)
#         # kth missing number = nums[right] + additional missing
#         #                    = nums[right] + k - (nums[right] - nums[0] - right)
#         #                    = nums[right] + k - nums[right] + nums[0] + right
#         #                    = nums[0] + k + right
#         return nums[0] + k + right

# class Solution:
#     def missingElement(self, nums: list[int], k: int) -> int:
#         """
#         Linear approach: iterate and count missing numbers.
        
#         Strategy: Check each gap between consecutive elements to see if 
#         the kth missing number falls within that gap.

#         Note: This "gap-checking" approach is different from the "shift k" 
#         linear approach used in LC1539 (finding kth missing from 1). This 
#         approach checks intervals between elements, while the shift approach 
#         increments k for each array element ≤ k.
        
#         Time Complexity: O(n)
#         Space Complexity: O(1)
#         """
#         n = len(nums)
        
#         # Iterate through consecutive pairs of elements
#         for i in range(1, n):
#             # Calculate the gap (missing numbers) between nums[i-1] and nums[i]
#             # Example: nums[i-1]=4, nums[i]=7 → gap = 7-4-1 = 2 (missing: 5,6)
#             gap = nums[i] - nums[i-1] - 1
            
#             # Check if the kth missing number is within this gap
#             if gap >= k:
#                 # The kth missing number is in this gap
#                 # It's k positions after nums[i-1]
#                 # Example: nums[i-1]=4, k=2 → answer is 4+2=6 (the 2nd number after 4)
#                 return nums[i-1] + k
            
#             # The kth missing is NOT in this gap
#             # We just passed 'gap' missing numbers, so reduce k accordingly
#             # Think of k as a countdown: if k=5 and gap=2, we've found 2 of the 5 missing numbers
#             # Now we need to find the remaining (5-2)=3 missing numbers in subsequent gaps
#             k -= gap
        
#         # If we've exhausted all gaps between array elements
#         # The kth missing number must be beyond the last element
#         # Note: k has been reduced by all the gaps we've passed
#         # Example: nums=[4,7,9,10], k=5
#         # After all gaps: k becomes 2 (we passed gaps with 5,6,8 = 3 missing numbers)
#         # → answer is nums[-1] + k = 10 + 2 = 12
#         return nums[-1] + k


# Rephrasing in interview

# PROJECT DEADLINE PROBLEM

# You are given a list of integers 'days' representing the days in a calendar year on which 
# you CANNOT work (these are holidays). The list is sorted in strictly increasing order, 
# and all values are unique.

# Days are numbered starting from 1 (so day 1 is the first day of the year).

# You are also given an integer 'k', which denotes the number of working days required 
# to finish a project.

# You can only work on non-holiday days (i.e., days NOT present in the days array).

# Return the earliest calendar day on which the project will be completed if you start 
# working on day 1.

# Example 1:
# Input: days = [2, 5, 7], k = 3
# Output: 4
# Explanation: 
#   Day 1: work (1st working day)
#   Day 2: holiday
#   Day 3: work (2nd working day)
#   Day 4: work (3rd working day) ✓ Project complete!
#   Working days are [1, 3, 4, 6, 8, ...], the 3rd working day is 4.

# Example 2:
# Input: days = [1, 2, 3, 4, 5], k = 2
# Output: 7
# Explanation:
#   Day 1-5: holidays
#   Day 6: work (1st working day)
#   Day 7: work (2nd working day) ✓ Project complete!


# Example 4:
# Input: days = [], k = 5
# Output: 5
# Explanation: No holidays, so the 5th working day is simply day 5.

# class SolutionLinear:
#     def projectDeadline(self, days: list[int], k: int) -> int:
#         """
#         Linear approach: iterate through holidays and adjust k.
        
#         Strategy: For each holiday ≤ current target day, shift the target forward by 1.
#         Similar to LC1539's linear solution.
        
#         Time Complexity: O(n)
#         Space Complexity: O(1)
#         """
#         # Edge case: if no holidays, project finishes on day k
#         if not days:
#             return k
        
#         # Iterate through each holiday
#         for holiday in days:
#             # If this holiday is on or before our current target completion day
#             # we need to push the completion day forward by 1
#             # Think: if we thought we'd finish on day 5, but day 3 is a holiday,
#             # then day 3 is NOT a working day, so we need one more day → finish on day 6
#             if holiday <= k:
#                 k += 1  # Shift target forward by 1 day
#             else:
#                 # Once we find a holiday beyond our target, we can stop
#                 # No further holidays will affect our answer
#                 break
        
#         # After adjusting for all relevant holidays, k is the completion day
#         return k

# class Solution:
#     def projectDeadline(self, days: list[int], k: int) -> int:
#         """
#         Find the earliest day when project is completed after k working days.
#         Working days are days NOT in the holidays list.
        
#         Time Complexity: O(log n) where n is the length of days
#         Space Complexity: O(1)
#         """
#         # Edge case: if no holidays, project finishes on day k
#         if not days:
#             return k
        
#         left = 0
#         right = len(days) - 1
        
#         # Binary search to find where the kth working day falls
#         while left <= right:
#             mid = (right - left) // 2 + left
            
#             # Count of working days before and up to day days[mid]
#             # Total days from 1 to days[mid]: days[mid]
#             # Holidays up to and including days[mid]: mid + 1
#             # Working days available = days[mid] - (mid + 1)
#             working_before_mid = days[mid] - (mid + 1)
            
#             if working_before_mid < k:
#                 # Not enough working days before days[mid]
#                 # The kth working day is after this
#                 left = mid + 1
#             else:
#                 # We have k or more working days before days[mid]
#                 # The kth working day is before or at this position
#                 right = mid - 1
        
#         return k + left

# Bonus: Get list of all k working days

# class SolutionWithWorkingDaysList:
#     def projectDeadlineWithList(self, days: list[int], k: int) -> tuple[int, list[int]]:
#         """
#         Return both the completion day and the list of k working days.
        
#         Time Complexity: O(n + k)
#             - n: length of holidays array (we may scan through all holidays)
#             - k: number of working days (in worst case, we iterate through k days)
#             - We iterate at most through all holidays + k working days
#             - Worst case example: days=[1,2,3,...,100], k=50
#               → Must scan through all 100 holidays + find 50 working days
#               → Total iterations: 100 + 50 = 150 = O(n + k)
        
#         Space Complexity: O(k)
#             - Auxiliary space (extra space used by algorithm): O(k)
#             - We store k working days in the result list
#             - All other variables (current_day, holiday_idx) use O(1) space
#             - Note: Input array 'days' of size n is not counted in auxiliary space
#             - Total space including input would be O(n + k)
#             - Example: k=1000 → list stores 1000 integers = O(1000) = O(k)
        
#         Returns:
#             tuple: (completion_day, working_days_list)
#         """
#         working_days_list = []
        
#         # Edge case: no holidays, working days are simply [1, 2, 3, ..., k]
#         if not days:
#             for i in range(1, k + 1):
#                 working_days_list.append(i)
#             return k, working_days_list
        
#         current_day = 1
#         holiday_idx = 0
        
#         # Keep going until we have k working days
#         while len(working_days_list) < k:
#             # Check if current day is a holiday
#             if holiday_idx < len(days) and current_day == days[holiday_idx]:
#                 # It's a holiday, skip it
#                 holiday_idx += 1
#             else:
#                 # It's a working day, add to list
#                 working_days_list.append(current_day)
            
#             current_day += 1
        
#         # Last working day is the completion day
#         completion_day = working_days_list[-1]
#         return completion_day, working_days_list
        