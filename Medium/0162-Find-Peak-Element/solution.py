"""
LeetCode 162. Find Peak Element
Difficulty: Medium
URL: https://leetcode.com/problems/find-peak-element/
"""

# Linear Scan (TC : O(n) SC : O(1))

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        for i in range(len(nums)-1):
            if nums[i] > nums[i+1]:
                return i
        return len(nums)-1

# Variant:
# Here are the other variants they might ask:
# What if a peak element must be equal or greater than its neighbors?
# What if a valley element must be equal or lower than its neighbors?
# For 1 and 2, you just have to change the equality signs in the If Statement. And yes, this means you'll have duplicate elements in your input array.

# What if you were given duplicate elements in SUCH A WAY that makes binary search unusable?
# Okay, the interviewer won't phrase it like this, but if this is the case, use a O(N) linear search.
# This is also known as the Even Terrain variant. 

# Example Walkthrough:
# Find me the peak (or valley) element, where said element is strictly greater (or lower) than its neighbors.
# Follow-up: What if there were duplicates? The answer is to use linear search. The presence of duplicates will render binary search useless.

# Find me the peak (or valley) element, where said element is equal or greater than (or equal or lower than) its neighbors. Note there are duplicates.
# If this is the first question asked, then chances are you'll have to implement binary search with the >=, <= equality signs.
# Follow-up: What if there weren't duplicates? Change signs to >, <.

# Overall, it's tricky but it all depends on how the input array has duplicate elements.

# How important is this variant?
# Very. LC162 is extremely common, and so are its variants. 

# For the original question, here are the questions you need to ask:

# 1. Does each value in the array only have unique values neighboring it? Yes
# 2. Are we given atleast one element in the array? Yes
# 3. Are there multiple peaks in the array? Can be
# 4. Are we guaranteed atleast one peak in the array? Yes. LeetCode guarantees nums[i] != nums[i+1] and treats out-of-bounds as -∞, so a peak always exists.
# 5. Are the edges of the array negative infinity (nums[-1] = nums[n] = -inf)? Yes

# Original problem (Strict peak, no duplicates)

# LC162 guarantees:

# nums[i] != nums[i+1]

# So:

# 1. no duplicates

# 2. slope always goes up or down

# 3. a peak always exists

# Can use both the versions below 

class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        """
        Version 1: Simpler approach (left < right)
        - Cleaner logic with fewer edge case checks
        - Shrinks search space to single element
        
        Time Complexity: O(log n) - binary search halves search space each iteration
        Space Complexity: O(1) - only uses constant extra space for pointers
        """
        # Edge case: empty array (though problem guarantees n >= 1)
        if not nums:
            return -1
        
        # Base case: single element is always a peak
        if len(nums) == 1:
            return 0
        
        # Base case: two elements - return index of larger one
        if len(nums) == 2:
            return 0 if nums[0] > nums[1] else 1
        
        # Edge case: first element is peak
        if nums[0] > nums[1]:
            return 0
        
        # Edge case: last element is peak
        if nums[-1] > nums[-2]:
            return len(nums) - 1

        left, right = 0, len(nums) - 1
        
        # Use 'while left < right' (not '<=') for two key reasons:
        # 1. It ensures mid + 1 is always a valid index (since mid < right).
        # 2. The loop converges to a single index (left == right) that is guaranteed to be a peak.
        #
        # If we used 'while left <= right':
        #   - When left == right, mid = left = right (last index).
        #   - Then nums[mid + 1] would be out of bounds (IndexError).
        #   - Also, the update logic (right = mid) doesn't require an extra iteration.
        while left < right:
            mid = (left + right) // 2
            
            if nums[mid] < nums[mid + 1]:
                # Peak must be on the right side (mid+1 or beyond)
                left = mid + 1
            else:
                # nums[mid] > nums[mid+1], so peak could be at mid or to the left
                right = mid
        
        # Why return left (or right, they're equal)?
        # - Loop exits when left == right
        # - At this point, we've narrowed down to a single element
        # - This element is GUARANTEED to be a peak because:
        #   1. We always moved toward the "upward slope" direction
        #   2. The algorithm ensures we never eliminate the peak
        #   3. When left == right, it points to a valid peak
        # - We could return either left or right since they're equal
        return left

class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        """
        Version 2: Explicit peak checking (left <= right)
        - Checks if current mid is a peak before moving
        - Uses traditional binary search pattern

        Examples:
        - [1, 2, 3, 1]: Returns 2 (value 3 is peak, 3 > 2 and 3 > 1)
        - [1, 2, 1, 3, 5, 6, 4]: Returns 5 (value 6 is peak, could also return 1)
        - [1, 3, 2]: Returns 1 (value 3 is peak at middle)
        - [3, 1]: Returns 0 (value 3 is peak at boundary)
        - [1, 5]: Returns 1 (value 5 is peak at boundary)
        - [5]: Returns 0 (single element is always a peak)
        
        Time Complexity: O(log n) - binary search halves search space each iteration
        Space Complexity: O(1) - only uses constant extra space for pointers
        """

        left = 0
        right = len(nums) - 1
        
        # Using left <= right (not left < right) because:
        # - We explicitly CHECK if mid is a peak inside the loop
        # - We need to examine every potential position, including when left == right
        # - We move PAST mid (left = mid + 1 or right = mid - 1), so we won't infinite loop
        # - This pattern is for "find exact target" style binary search
        # 
        # Alternative (left < right) is used when:
        # - You DON'T check for answer inside loop
        # - You return left/right AFTER loop ends
        # - You do right = mid (not mid - 1) to avoid skipping the answer
        while left <= right:
            mid = (left + right) // 2
            
            # Check if mid is a peak (greater than both neighbors)
            # A peak must satisfy BOTH conditions (connected by AND):
            # 
            # Why check "mid == len(nums) - 1" and "mid == 0"?
            # - These prevent INDEX OUT OF BOUNDS errors
            # - If mid is last element (mid == len(nums) - 1), we CAN'T access nums[mid+1]
            #   So we treat last element as having no right neighbor (auto-satisfies right condition)
            # - If mid is first element (mid == 0), we CAN'T access nums[mid-1]
            #   So we treat first element as having no left neighbor (auto-satisfies left condition)
            # - By problem definition, elements outside array are considered -infinity
            #   So boundary elements only need to beat their ONE existing neighbor
            # 
            # Why use OR within each condition?
            # - Left condition: (mid == 0 OR nums[mid] > nums[mid-1])
            #   Reads as: "Left side OK if we're at boundary OR we beat left neighbor"
            #   The OR allows short-circuiting: if mid==0, skip the comparison (prevents index error)
            # 
            # - Right condition: (mid == len(nums)-1 OR nums[mid] > nums[mid+1])
            #   Reads as: "Right side OK if we're at boundary OR we beat right neighbor"
            #   The OR allows short-circuiting: if at last position, skip the comparison
            # 
            # Why use AND between the two conditions?
            # - A peak must satisfy BOTH left AND right
            # - Format: (left side OK) AND (right side OK)
            # - Not enough to beat just one neighbor
            # 
            # Example [1, 3, 2] at mid=1:
            #   Left:  (False OR 3>1) = True ✓
            #   Right: (False OR 3>2) = True ✓
            #   Result: True AND True = Peak found!
            if (mid == 0 or nums[mid - 1] < nums[mid]) and \
            (mid == len(nums) - 1 or nums[mid + 1] < nums[mid]):
                return mid
            
            # Move towards higher neighbor
            if nums[mid] < nums[mid+1]:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1  # Unreachable

# Variant A — STRICT Peak + Duplicates

# 1️⃣ Definition (UNCHANGED)

# Peak is still:

# nums[i] > nums[i-1] and nums[i] > nums[i+1]

# ⚠️ Strictly greater — equality NOT allowed.

# 2️⃣ What changed?

# Now duplicates are allowed.

# Example:

# [1, 2, 2, 2, 1]

# 3️⃣ First big realization (VERY IMPORTANT)

# A strict peak may NOT exist.

# Check the middle:

# 2 > 2   ❌

# So:

# No strict peak exists.

# This is already very different from OG LC162.

# Why we don’t use binary search?

# Binary search relies on comparing:

# nums[mid] vs nums[mid+1]

# With duplicates, they may be equal:

# nums[mid] == nums[mid+1]

# Then there is no clear direction to discard half the array safely.

# So we switch to linear scan.

class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        """
        Strict peak (> neighbors), duplicates allowed.
        Linear Scan Solution

        Time: O(n)
        Space: O(1)
        """
        n = len(nums)

        for i in range(n):
            left = nums[i - 1] if i > 0 else float("-inf")
            right = nums[i + 1] if i < n - 1 else float("-inf")

            if nums[i] > left and nums[i] > right:
                return i

        return -1   # no strict peak

# Variant B — NON-STRICT Peak (>=) + Duplicates

# Definition

# Peak means:

# nums[i] >= nums[i-1] and nums[i] >= nums[i+1]

# Equality is allowed.

# So plateaus are valid peaks.

# Example:

# [1, 2, 2, 2, 1]

# Any 2 is a peak.

# Key idea

# Because equality is allowed:

# nums[mid] == nums[mid+1] is NOT a problem anymore — either side can still contain a valid peak.

# ➡️ Binary search works again.

# class Solution:
#     def findPeakElement(self, nums: list[int]) -> int:
#         """
#         Variant: Non-strict peak (>= neighbors) with duplicates
#         Peak = >= neighbors, duplicates allowed

#         Time: O(log n)
#         Space: O(1)
#         """
#         left, right = 0, len(nums) - 1

#         while left < right:
#             mid = (left + right) // 2

#             # Same condition as original, but else now handles equality too
#             if nums[mid] < nums[mid + 1]:
#                 left = mid + 1
#             else:  # nums[mid] >= nums[mid + 1]
#                 right = mid

#         return left

# class Solution:
#     def findPeakElement(self, nums: list[int]) -> int:
#         """
#         Variant 3:
#         Peak = >= neighbors
#         Explicit mid-check version
#         """

#         left, right = 0, len(nums) - 1

#         while left <= right:
#             mid = (left + right) // 2

#             # explicit peak check (NON-STRICT)
#             if (mid == 0 or nums[mid] >= nums[mid - 1]) and \
#                (mid == len(nums) - 1 or nums[mid] >= nums[mid + 1]):
#                 return mid

#             # move toward higher side
#             if nums[mid] < nums[mid + 1]:
#                 left = mid + 1
#             else:
#                 right = mid - 1

#         return -1

# Variant C — NON-STRICT Peak (>=) with No Duplicates
# Definition

# Peak means:

# nums[i] >= nums[i-1] and nums[i] >= nums[i+1]

# But the array has no duplicates.

# Key observation

# If there are no duplicates:

# >=   is effectively the same as   >

# Because equality never happens.

# So:

# ➡️ Variant 4 behaves exactly like the OG problem.

# Find all peaks 

# class Solution:
#     def findAllPeaks(self, nums: List[int]) -> List[int]:
#         """
#         Find all peak indices.
#         A peak is an index i such that nums[i] > nums[i-1] and nums[i] > nums[i+1].
#         Endpoints are compared against -inf, so index 0 is a peak if nums[0] > nums[1],
#         and index n-1 is a peak if nums[n-1] > nums[n-2].
#         (Original LC162 also assumes nums[i] != nums[i+1], but this works regardless.)

#         Time Complexity: O(n)  — you must inspect each element at least once to list all peaks.
#         Space Complexity: O(1) extra (excluding the output list).
#         """
#         n = len(nums)
#         if n == 0:
#             return []
#         if n == 1:
#             return [0]

#         peaks = []
#         for i in range(n):
#             left  = nums[i - 1] if i > 0 else float("-inf")
#             right = nums[i + 1] if i < n - 1 else float("-inf")
#             if nums[i] > left and nums[i] > right:
#                 peaks.append(i)
#         return peaks


# Another Variant : Find Valley Element

# A valley element is an element that is strictly less than its neighbors.

# Given a 0-indexed integer array nums, find a valley element, and return its index.
# If the array contains multiple valleys, return the index to any of the valleys.

# You may imagine that nums[-1] = nums[n] = +∞.
# In other words, an element is always considered to be strictly lesser than a neighbor that is outside the array.

# You must write an algorithm that runs in O(log n) time.

# Example 1:
# Input: nums = [1, 2, 3, 1]
# Output: 0
# Explanation: 0 is a valley element and your function should return the index number 0.

# Constraints:

# 1 <= nums.length <= 1000

# -2^31 <= nums[i] <= 2^31 - 1

# nums[i] != nums[i + 1] for all valid i

# Original LC162 - Valley Version (Strict valley, no duplicates)

# class Solution:
#     def findValleyElement(self, nums: list[int]) -> int:
#         """
#         Version 1: Simpler approach (left < right)
#         Find a valley element where valley < both neighbors
        
#         Time Complexity: O(log n)
#         Space Complexity: O(1)
#         """
#         # Edge case: empty array
#         if not nums:
#             return -1
        
#         # Base case: single element is always a valley
#         if len(nums) == 1:
#             return 0
        
#         # Base case: two elements - return index of smaller one
#         if len(nums) == 2:
#             return 0 if nums[0] < nums[1] else 1
        
#         # Edge case: first element is valley
#         if nums[0] < nums[1]:
#             return 0
        
#         # Edge case: last element is valley
#         if nums[-1] < nums[-2]:
#             return len(nums) - 1

#         left, right = 0, len(nums) - 1
        
#         while left < right:
#             mid = (left + right) // 2
            
#             if nums[mid] > nums[mid + 1]:
#                 # Valley must be on the right side (mid+1 or beyond)
#                 left = mid + 1
#             else:
#                 # nums[mid] < nums[mid+1], so valley could be at mid or to the left
#                 right = mid
        
#         # Loop exits when left == right (single element remaining)
#         # This element is guaranteed to be a valley
#         return left


# class Solution:
#     def findValleyElement(self, nums: list[int]) -> int:
#         """
#         Version 2: Explicit valley checking (left <= right)
#         Find a valley element where valley < both neighbors
        
#         Examples:
#         - [3, 2, 1, 3]: Returns 2 (value 1 is valley)
#         - [3, 1, 2]: Returns 1 (value 1 is valley at middle)
#         - [1, 5]: Returns 0 (boundary valley)
        
#         Time Complexity: O(log n)
#         Space Complexity: O(1)
#         """
#         left = 0
#         right = len(nums) - 1
        
#         # Use left <= right because we check for valley inside loop
#         while left <= right:
#             mid = (left + right) // 2
            
#             # Check if mid is a valley (less than both neighbors)
#             # Valley check: (left OK) AND (right OK)
#             # - OR within condition: skip comparison at boundary OR beat neighbor
#             # - AND between conditions: must satisfy both sides
#             if (mid == 0 or nums[mid] < nums[mid - 1]) and \
#                (mid == len(nums) - 1 or nums[mid] < nums[mid + 1]):
#                 return mid
            
#             # Move towards lower neighbor
#             if nums[mid] > nums[mid + 1]:
#                 left = mid + 1
#             else:
#                 right = mid - 1
        
#         return -1  # Unreachable


# # Variant A — STRICT Valley + Duplicates

# # Definition:
# # Valley is: nums[i] < nums[i-1] and nums[i] < nums[i+1]
# # Strictly less — equality NOT allowed

# # With duplicates allowed, a strict valley may NOT exist.
# # Example: [3, 2, 2, 2, 3] - no strict valley exists (2 is not < 2)

# # Why linear search?
# # When nums[mid] == nums[mid+1], no clear direction to eliminate half safely.

# class Solution:
#     def findValleyElement(self, nums: list[int]) -> int:
#         """
#         Strict valley (< neighbors), duplicates allowed.
#         Linear Scan Solution

#         Time: O(n)
#         Space: O(1)
#         """
#         n = len(nums)

#         for i in range(n):
#             left = nums[i - 1] if i > 0 else float("inf")
#             right = nums[i + 1] if i < n - 1 else float("inf")

#             if nums[i] < left and nums[i] < right:
#                 return i

#         return -1  # no strict valley


# # Variant B — NON-STRICT Valley (<=) + Duplicates

# # Definition:
# # Valley means: nums[i] <= nums[i-1] and nums[i] <= nums[i+1]
# # Equality is allowed, so plateaus are valid valleys

# # Example: [3, 2, 2, 2, 3]
# # Any 2 is a valley

# # Binary search works because equality is not a problem

# class Solution:
#     def findValleyElement(self, nums: list[int]) -> int:
#         """
#         Variant: Non-strict valley (<= neighbors) with duplicates
#         Valley = <= neighbors, duplicates allowed

#         Time: O(log n)
#         Space: O(1)
#         """
#         left, right = 0, len(nums) - 1

#         while left < right:
#             mid = (left + right) // 2

#             # Same condition as original, but else now handles equality too
#             if nums[mid] > nums[mid + 1]:
#                 left = mid + 1
#             else:  # nums[mid] <= nums[mid + 1]
#                 right = mid

#         return left


# class Solution:
#     def findValleyElement(self, nums: list[int]) -> int:
#         """
#         Variant: Non-strict valley (<= neighbors) with duplicates
#         Explicit mid-check version

#         Time: O(log n)
#         Space: O(1)
#         """
#         left, right = 0, len(nums) - 1

#         while left <= right:
#             mid = (left + right) // 2

#             # Explicit valley check (NON-STRICT)
#             if (mid == 0 or nums[mid] <= nums[mid - 1]) and \
#                (mid == len(nums) - 1 or nums[mid] <= nums[mid + 1]):
#                 return mid

#             # Move toward lower side
#             if nums[mid] > nums[mid + 1]:
#                 left = mid + 1
#             else:
#                 right = mid - 1

#         return -1


# # Variant C — NON-STRICT Valley (<=) with No Duplicates

# # Definition:
# # Valley means: nums[i] <= nums[i-1] and nums[i] <= nums[i+1]
# # But no duplicates allowed

# # Key observation:
# # If no duplicates, <= is effectively the same as 
# # Behaves exactly like the original problem


# # Find All Valleys

# class Solution:
#     def findAllValleys(self, nums: List[int]) -> List[int]:
#         """
#         Find all valley indices.
#         A valley is an index i such that nums[i] < nums[i-1] and nums[i] < nums[i+1].
#         Endpoints are compared against +inf, so index 0 is a valley if nums[0] < nums[1],
#         and index n-1 is a valley if nums[n-1] < nums[n-2].

#         Time Complexity: O(n) — must inspect each element to list all valleys
#         Space Complexity: O(1) extra (excluding output list)
#         """
#         n = len(nums)
#         if n == 0:
#             return []
#         if n == 1:
#             return [0]

#         valleys = []
#         for i in range(n):
#             left  = nums[i - 1] if i > 0 else float("inf")
#             right = nums[i + 1] if i < n - 1 else float("inf")
#             if nums[i] < left and nums[i] < right:
#                 valleys.append(i)
#         return valleys











         
        