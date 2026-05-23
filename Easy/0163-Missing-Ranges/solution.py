"""
LeetCode 163. Missing Ranges
Difficulty: Easy
URL: https://leetcode.com/problems/missing-ranges/
"""

# Brute Force Approach

# Idea: Iterate through every single number from lower to upper one by one. For each number, check if it exists in the nums array using linear search. If a number is missing, track it as part of a missing range. When we hit a number that exists in nums, close the current missing range and add it to the result.

# Example: nums = [0, 1, 5], lower = 0, upper = 7
# Step-by-Step Execution:
# We check every number from 0 to 7:

# num = 0: Is 0 in [0,1,5]? YES → Skip it
# num = 1: Is 1 in [0,1,5]? YES → Skip it
# num = 2: Is 2 in [0,1,5]? NO → Start missing range at 2
# num = 3: Is 3 in [0,1,5]? NO → Continue missing range
# num = 4: Is 4 in [0,1,5]? NO → Continue missing range
# num = 5: Is 5 in [0,1,5]? YES → Close range [2, 4], add to result
# num = 6: Is 6 in [0,1,5]? NO → Start new missing range at 6
# num = 7: Is 7 in [0,1,5]? NO → Continue missing range
# End of range → Close range [6, 7], add to result

# Output: [[2, 4], [6, 7]]

# Time Complexity: O((upper - lower) × n)

# We check every number in the range [lower, upper]: O(upper - lower)
# For each number, we do a linear search in nums: O(n)
# Total: O((upper - lower) × n)

# Space Complexity: O(1) auxiliary space (excluding output)

# Why it's bad: If upper - lower = 10^9 and n = 100, we'd do 10^11 operations. The optimal solution only processes the n elements in the array, achieving O(n) time regardless of how large the range is.

# class Solution:
#     def findMissingRanges(
#         self, nums: list[int], lower: int, upper: int
#     ) -> list[list[int]]:
#         """
#         Find all missing ranges between lower and upper that are not in nums.
        
#         Time Complexity: O(n)
#             - We iterate through the nums array once: O(n)
#             - All operations inside the loop are O(1)
#             - Overall: O(n) where n is the length of nums
        
#         Space Complexity: O(n)
#             - Output space:
#                 - Maximum number of missing ranges = n + 1
#                 - 1 gap before first element + (n-1) gaps between elements + 1 gap after last
#                 - Each range takes O(1) space
#                 - Total output space: O(n + 1) = O(n)
#             - Auxiliary space (excluding output): O(1)
#                 - Only use constant extra variables (n, i)
#             - Overall space: O(n)
            
#             Example: nums = [2, 4, 6, 8], lower = 1, upper = 10
#                 Output: [[1,1], [3,3], [5,5], [7,7], [9,10]] → 5 ranges (n+1 where n=4)
#         """
#         n = len(nums)
#         missing_ranges = []
        
#         # If array is empty, the entire range [lower, upper] is missing
#         if n == 0:
#             missing_ranges.append([lower, upper])
#             return missing_ranges
        
#         # Check if there are missing numbers before the first element
#         if lower < nums[0]:
#             missing_ranges.append([lower, nums[0] - 1])
        
#         # Check for missing numbers between consecutive elements
#         for i in range(n - 1):
#             # If difference is 1 or less, no gap exists
#             if nums[i + 1] - nums[i] <= 1:
#                 continue
#             # Add the missing range between current and next element
#             missing_ranges.append([nums[i] + 1, nums[i + 1] - 1])
        
#         # Check if there are missing numbers after the last element
#         if upper > nums[-1]:
#             missing_ranges.append([nums[-1] + 1, upper])
        
#         return missing_ranges

# Check with example : nums = [5,8,9,15,16,18,20], lower = 2, upper = 87. Output : [[2,4],[6,7],[10,14],[17,17],[19,19],[21,87]]

# Approach : Merge all cases in a single loop (may be asked to implement instead of previous approach)

class Solution:
    def findMissingRanges(
        self, nums: list[int], lower: int, upper: int
    ) -> list[list[int]]:
        """
        Find missing ranges between lower and upper that are not in nums.
        
        Approach: Track the next expected number (curr_lower) and calculate
        the gap between it and each number in the array. This unifies all
        three cases (before first, between elements, after last) into one loop.
        
        Time Complexity: O(n)
            Rationale:
            - We iterate through (n + 1) elements once: O(n + 1)
            - Inside the loop, all operations are O(1):
            - Total: O(n + 1) × O(1) = O(n)
            - Where n is the length of the input array nums
        
        Space Complexity: O(n)
            Rationale:
            - Output space:
                * Maximum number of missing ranges = n + 1
                * Why n + 1? We can have:
                    - 1 gap before the first element
                    - (n - 1) gaps between n consecutive elements
                    - 1 gap after the last element
                    - Total: 1 + (n - 1) + 1 = n + 1
                * Each range [start, end] takes O(1) space
                * Total output space: (n + 1) × O(1) = O(n)
            
            - Auxiliary space (excluding output):
                * Variables (curr_lower, i, curr, gap): O(1)
                * No additional data structures created
                * Total auxiliary: O(1)
            
            - Overall: O(n) (output) + O(1) (auxiliary) = O(n)
        
        Example: nums = [0, 1, 3, 50, 75], lower = 0, upper = 99
            curr_lower tracks: 0 → 1 → 2 → 4 → 51 → 76
            Output: [[2, 2], [4, 49], [51, 74], [76, 99]]
        """
        missing_ranges = []
        
        # curr_lower represents the next expected number in our range [lower, upper]
        # We start with lower because that's where our valid range begins
        curr_lower = lower
        
        # Loop (n + 1) times to process all n elements plus one extra for upper boundary
        # Why n + 1?
        #   - First n iterations (i = 0 to n-1): process actual array elements
        #   - Last iteration (i = n): use upper + 1 as sentinel to detect missing
        #     numbers after the last element
        for i in range(len(nums) + 1):
            # Determine current number to compare against
            # If i < len(nums): use the actual array element at index i
            # If i == len(nums): use (upper + 1) as a virtual boundary
            # 
            # Why upper + 1 for the last iteration?
            #   - It acts as a sentinel to detect missing numbers after nums[-1]
            #   - Example: If nums[-1] = 75 and upper = 99
            #     Setting curr = 100 will create gap = 100 - 76 = 24
            #     This correctly identifies [76, 99] as missing
            curr = nums[i] if i < len(nums) else upper + 1


            # Skip if curr is outside valid range, e.g., nums = [-10, 0, 5, 100], lower = 0, upper = 10. Additional check, not required for this problem since lower <= nums[i] <= upper
            # if curr < lower:
            #     continue
            
            # Calculate the gap between the current expected number and actual number
            # gap represents how many positions are between curr_lower and curr
            # Examples:
            #   - If curr_lower = 2 and curr = 3: gap = 1 (only 2 is missing)
            #   - If curr_lower = 2 and curr = 5: gap = 3 (2, 3, 4 are missing)
            #   - If curr_lower = 2 and curr = 2: gap = 0 (no missing numbers)
            gap = curr - curr_lower
            
            # If gap >= 1, there's at least one missing number
            # The missing range is [curr_lower, curr - 1]
            # Why curr - 1?
            #   - curr_lower is the first missing number
            #   - curr - 1 is the last missing number (since curr itself is present)
            # Examples:
            #   - curr_lower = 2, curr = 3: missing [2, 2] (just 2)
            #   - curr_lower = 4, curr = 50: missing [4, 49] (4 through 49)
            if gap >= 1:
                missing_ranges.append([curr_lower, curr - 1])
            
            # Update curr_lower to the next number after curr
            # Why curr + 1?
            #   - curr is either in the array or is (upper + 1)
            #   - Either way, we've accounted for it, so the next expected number is curr + 1
            # Example: If curr = 3, then curr_lower becomes 4 for the next iteration
            curr_lower = curr + 1
        
        return missing_ranges

# Variant : Formatting Rules

# You are given an inclusive range [lower, upper] and a sorted unique integer array nums, where all elements are within the inclusive range.

# A number x is considered missing if x is in the range [lower, upper] and x is not in nums.
# Additionally, there are formatting rules:

# If there are more than two consecutive missing numbers, then use a "–" between the missing lower- and upper-numbers.

# If there is one missing number, push it as an individual string.

# If there are exactly two consecutive missing numbers, push them individually.

# Return the shortest sorted list of ranges that exactly covers all the missing numbers as a list of strings.

# Example 1

# Input:

# nums = [5,8,9,15,16,18,20], lower = 2, upper = 87


# Output:

# ["2-4", "6", "7", "10-14", "17", "19", "21-87"]

# Constraints

# 0 <= lower <= upper <= 10^9

# 0 <= nums.length <= 100

# lower <= nums[i] <= upper

# All values of nums are unique


# class Solution:
#     def findMissingRanges(
#         self, nums: list[int], lower: int, upper: int
#     ) -> list[str]:
#         """
#         Find missing ranges with specific formatting rules:
#         - Single missing number: "x"
#         - Two consecutive missing numbers: "x", "y" (separately)
#         - More than two consecutive: "x->y"
        
#         Approach: Track the next expected number (curr_lower) and calculate
#         the gap between it and each number, using index-based iteration to
#         avoid creating a new list.
        
#         Time Complexity: O(n)
#             Rationale:
#             - We iterate through (n + 1) elements once: O(n + 1)
#             - Inside the loop, all operations are O(1):
#             - Total: O(n + 1) × O(1) = O(n)
#             - Where n is the length of the input array nums
        
#         Space Complexity: O(n)
#             Rationale:
#             - Output space:
#                 * Maximum number of string ranges = n + 1
#                 * For two consecutive missing, we add 2 strings, so worst case
#                   could be more than n+1, but still O(n)
#                 * Example: nums = [2,4,6,8], lower=1, upper=9
#                   Output has 5 strings for 4 elements
#                 * Each string takes O(log(upper)) space for number representation
#                 * Total output space: O(n × log(upper))
            
#             - Auxiliary space (excluding output):
#                 * Variables (curr_lower, i, curr, gap): O(1)
#                 * No additional data structures created
#                 * Total auxiliary: O(1)
            
#             - Overall: O(n × log(upper)) for output + O(1) auxiliary
#                        Simplified as O(n) when log(upper) is considered constant
        
#         Example: nums = [5,8,9,15,16,18,20], lower = 2, upper = 87
#             Output: ["2->4", "6", "7", "10->14", "17", "19", "21->87"]
#         """
#         missing_ranges = []
        
#         # curr_lower represents the next expected number in our range [lower, upper]
#         # We start with lower because that's where our valid range begins
#         curr_lower = lower
        
#         # Loop (n + 1) times to process all n elements plus one extra for upper boundary
#         # Why n + 1?
#         #   - First n iterations (i = 0 to n-1): process actual array elements
#         #   - Last iteration (i = n): use upper + 1 as sentinel to detect missing
#         #     numbers after the last element
#         for i in range(len(nums) + 1):
#             # Determine current number to compare against
#             # If i < len(nums): use the actual array element at index i
#             # If i == len(nums): use (upper + 1) as a virtual boundary
#             # 
#             # Why upper + 1 for the last iteration?
#             #   - It acts as a sentinel to detect missing numbers after nums[-1]
#             #   - Example: If nums[-1] = 20 and upper = 87
#             #     Setting curr = 88 will create gap = 88 - 21 = 67
#             #     This correctly identifies [21, 87] as missing
#             curr = nums[i] if i < len(nums) else upper + 1
            
#             # Calculate the gap between the current expected number and actual number
#             # gap represents how many numbers are missing between curr_lower and curr
#             # Examples:
#             #   - If curr_lower = 6 and curr = 8: gap = 2 (6, 7 are missing)
#             #   - If curr_lower = 10 and curr = 15: gap = 5 (10-14 are missing)
#             #   - If curr_lower = 8 and curr = 8: gap = 0 (no missing numbers)
#             gap = curr - curr_lower
            
#             # Format the output based on the number of missing values
#             # We check gap instead of checking gap >= 1 because we need different
#             # formatting for different gap sizes
            
#             if gap > 2:
#                 # More than 2 missing numbers: use "x->y" format
#                 # Example: curr_lower = 4, curr = 50, gap = 46
#                 #   Missing: [4, 5, 6, ..., 49]
#                 #   Output: "4->49"
#                 missing_ranges.append(f"{curr_lower}->{curr - 1}")
#             elif gap == 2:
#                 # Exactly 2 missing numbers: push them individually
#                 # Example: curr_lower = 6, curr = 8, gap = 2
#                 #   Missing: [6, 7]
#                 #   Output: "6", "7" (two separate strings)
#                 missing_ranges.append(str(curr_lower))
#                 missing_ranges.append(str(curr_lower + 1))
#             elif gap == 1:
#                 # Exactly 1 missing number: push as single string
#                 # Example: curr_lower = 17, curr = 18, gap = 1
#                 #   Missing: [17]
#                 #   Output: "17"
#                 missing_ranges.append(str(curr_lower))
#             # If gap == 0: no missing numbers (curr_lower == curr), do nothing
            
#             # Update curr_lower to the next number after curr
#             # Why curr + 1?
#             #   - curr is either in the array or is (upper + 1)
#             #   - Either way, we've accounted for it, so the next expected number is curr + 1
#             # Example: If curr = 8, then curr_lower becomes 9 for the next iteration
#             curr_lower = curr + 1
        
#         return missing_ranges

# Space for String Representation:
# When we do str(curr_lower) or f"{curr_lower}->{curr - 1}":

# The largest number we can represent is upper
# upper has approximately log₁₀(upper) digits
# Storing this string takes O(log₁₀(upper)) space
# In Big-O notation, we write this as O(log(upper))

# Number of Digits Formula:
# For a number x, the number of digits = ⌊log₁₀(x)⌋ + 1
# Examples:

# x = 9: 1 digit → log₁₀(9) ≈ 0.95 → ⌊0.95⌋ + 1 = 1
# x = 99: 2 digits → log₁₀(99) ≈ 1.99 → ⌊1.99⌋ + 1 = 2
# x = 999: 3 digits → log₁₀(999) ≈ 2.99 → ⌊2.99⌋ + 1 = 3
# x = 87: 2 digits → log₁₀(87) ≈ 1.94 → ⌊1.94⌋ + 1 = 2



