"""
LeetCode 303. Range Sum Query - Immutable
Difficulty: Easy
URL: https://leetcode.com/problems/range-sum-query-immutable/
"""

class NumArray:
    """
    Time Complexity:
        - Constructor: O(n) where n is the length of nums
        - sumRange: O(1) per query
    
    Space Complexity: O(n) for the prefix sum array
    """
    
    def __init__(self, nums: List[int]):
        """
        Initialize the prefix sum array.
        
        Time Complexity: O(n) - iterate through all elements once
        Space Complexity: O(n) - store n+1 elements in prefix array
        
        Approach:
            Preallocate array and fill it iteratively.
            prefix[i] represents sum of first i elements.
        """
        n = len(nums)
        self.n = n  # Store length for bounds checking in sumRange

        # Preallocate array of size n+1, initialized with zeros
        self.prefix = [0] * (n + 1)
        
        # Build prefix sum array
        # prefix[0] = 0 (sum of zero elements)
        # prefix[i+1] = sum of first i+1 elements
        for i in range(n):
            # Compute prefix[i+1] from prefix[i] + nums[i]
            self.prefix[i + 1] = self.prefix[i] + nums[i]
    
    def sumRange(self, left: int, right: int) -> int:
        """
        Calculate sum of elements between indices left and right (inclusive).
        
        Time Complexity: O(1) - simple subtraction operation
        Space Complexity: O(1) - no extra space used
        
        Formula:
            sum(left to right) = prefix[right+1] - prefix[left]

        Defensive check (single combined condition):
        - left > right: invalid/reversed range
        - left < 0: out of bounds on the left
        - right >= self.n: out of bounds on the right (also catches empty array,
          since n == 0 makes any right >= 0 satisfy this condition)
        """

        # Optional : Handles invalid range, out-of-bounds indices, and empty array all at once
        if left > right or left < 0 or right >= self.n:
            return 0

        return self.prefix[right + 1] - self.prefix[left]

# prefix[i] = sum of the FIRST i elements (nums[0] to nums[i-1])
# Not the sum up to index i, but the sum of i elements.
# Visual Example
# nums =   [-2,  0,  3, -5,  2, -1]
# index:     0   1   2   3   4   5

# prefix = [0, -2, -2,  1, -4, -2, -3]
# index:    0   1   2   3   4   5   6
#           ↑   ↑   ↑   ↑   ↑   ↑   ↑
#           │   │   │   │   │   │   └─ sum of 6 elements (entire array)
#           │   │   │   │   │   └───── sum of 5 elements
#           │   │   │   │   └───────── sum of 4 elements
#           │   │   │   └───────────── sum of 3 elements
#           │   │   └───────────────── sum of 2 elements
#           │   └───────────────────── sum of 1 element
#           └───────────────────────── sum of 0 elements
# Why right + 1?
# Let's calculate sumRange(2, 5) step by step:
# We want: nums[2] + nums[3] + nums[4] + nums[5]

# That's: 3 + (-5) + 2 + (-1) = -1

# Using prefix sums:
# prefix[6] = sum of first 6 elements = nums[0..5] = -3
# prefix[2] = sum of first 2 elements = nums[0..1] = -2

# prefix[6] - prefix[2] = -3 - (-2) = -1 ✓
# Why this works:

# prefix[6] includes everything from index 0 to 5
# prefix[2] includes everything from index 0 to 1
# Subtracting removes indices 0 and 1, leaving indices 2 to 5!

# The Pattern
# prefix[0] = 0              # sum of 0 elements
# prefix[1] = nums[0]        # sum of 1 element
# prefix[2] = nums[0..1]     # sum of 2 elements
# prefix[3] = nums[0..2]     # sum of 3 elements
# ...
# prefix[i] = nums[0..i-1]   # sum of i elements
        
# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)


# Variant : Given an array of 1's and 0's, we want to return the number of 1's in specified subarrays. This will be called multiple times and the array is an enormous size. The algorithm must be efficient.

# Example:
# Input
# ["Solution", "numOnes", "numOnes", "numOnes"]
# [[[1, 1, 0, 0, 1, 0]], [0, 2], [2, 5], [0, 5]]

# Output
# [null, 2, 1, 3]

# Follow up questions to ask:

# 1. How are we given the input array?

# The input array is given to you in the constructor when you initialize your class. So you'll receive the entire binary array upfront, and then the numOnes method will be called multiple times with different left and right indices to query different subarrays.
# Something like this:

# The array is passed to constructor
# solution = Solution([1, 1, 0, 0, 1, 0])

# Then numOnes is called multiple times
# result1 = solution.numOnes(0, 2)  # Query 1
# result2 = solution.numOnes(2, 5)  # Query 2
# result3 = solution.numOnes(0, 5)  # Query 3

# 2. How do we know the subarray's start and end?

# The subarray's start and end are given as parameters to the numOnes method. You'll receive two integers:

# left: the starting index (inclusive)
# right: the ending index (inclusive)

# So when we call numOnes(left, right), you need to count the number of 1's in the subarray from index left to index right, including both endpoints.

# arr = [1, 1, 0, 0, 1, 0]
#        0  1  2  3  4  5  (indices)

# numOnes(0, 2)  # Count 1's in arr[0], arr[1], arr[2] → [1, 1, 0] → 2
# numOnes(2, 5)  # Count 1's in arr[2], arr[3], arr[4], arr[5] → [0, 0, 1, 0] → 1

# 3. What is the length of the array, how many function invocations are there, do we prioritize TC or SC?

# Array size: The array can be very large - think millions of elements, possibly up to 10^6 or even 10^7.

# Number of queries: The numOnes function will be called many times - could be thousands or even millions of calls. So if you have an inefficient query method, it will really add up.

# Time vs Space tradeoff: Given that we have a huge array and tons of queries, we want to prioritize query time complexity. We're willing to use extra space and do some preprocessing upfront if it means we can answer each query very quickly.

# So ideally:
# Preprocessing in constructor: Can be O(n) - that's fine
# Each query: Should be as fast as possible - O(1) would be ideal
# Extra space: O(n) is acceptable


# class Solution:
#     """
#     Count number of 1's in subarrays efficiently using prefix sum.
    
#     Time Complexity:
#         - Constructor: O(n) where n is length of array
#         - numOnes: O(1) per query
    
#     Space Complexity: O(n) for prefix sum array
#     """
    
#     def __init__(self, arr: List[int]):
#         """
#         Build prefix sum array to count 1's efficiently.
        
#         Args:
#             arr: List[int] - Binary array of 0's and 1's
        
#         Time: O(n), Space: O(n)
        
#         prefix[i] represents count of 1's in first i elements
#         """
#         n = len(arr)
#         self.n = n

#         # Pre-allocate prefix array of size n+1
#         self.prefix = [0] * (n + 1)
        
#         # Build prefix sum array
#         # prefix[i+1] = count of 1's in arr[0..i]
#         for i in range(n):
#             # Add 1 if arr[i] is 1, otherwise add 0
#             self.prefix[i + 1] = self.prefix[i] + arr[i]
    
#     def numOnes(self, left: int, right: int) -> int:
#         """
#         Return count of 1's in subarray arr[left..right] (inclusive).
        
#         Args:
#             left: int - Starting index (inclusive)
#             right: int - Ending index (inclusive)
        
#         Returns:
#             int - Number of 1's in the range
        
#         Time: O(1), Space: O(1)
#         """

#         # Optional : Handles invalid range, out-of-bounds indices, and empty array all at once
#         if left > right or left < 0 or right >= self.n:
#             return 0

#         return self.prefix[right + 1] - self.prefix[left]


# Follow up : What if digits were 0-9 instead of binary?

# class Solution:
#     """
#     Count occurrences of any digit (0-9) in subarrays efficiently.
    
#     Time Complexity:
#         - Constructor: O(n) where n is length of array
#         - countDigit: O(1) per query
    
#     Space Complexity: O(10n) = O(n) for 10 prefix sum arrays
#     """
    
#     def __init__(self, arr: List[int]):
#         """
#         Build 10 prefix sum arrays, one for each digit 0-9.
        
#         Args:
#             arr: List[int] - Array of digits 0-9
        
#         Time: O(n), Space: O(10n)
        
#         prefix[d][i] = number of times digit d appears in arr[0..i-1]
#         """
#         n = len(arr)
#         self.n = n

#         # Create 10 prefix arrays (one for each digit 0-9)
#         # prefix[d] = prefix sum array for digit d
#         self.prefix = [[0] * (n + 1) for _ in range(10)]
        
#         # Build prefix sum arrays for all digits
#         for i in range(n):
#             current_digit = arr[i]
            
#             # Step 1: Copy ALL previous counts (carry forward the running totals)
#             # This preserves the cumulative nature - each position knows the
#             # count of all digits seen so far
#             #
#             # Example: arr = [1, 2, 1], at i=1 (about to process arr[1]=2)
#             #   Before this step: prefix[0..9][1] holds counts after processing arr[0]
#             #     prefix[1] = [0, 1, 0, 0, ...]   (one '1' seen so far)
#             #     prefix[2] = [0, 0, 0, 0, ...]   (no '2' seen yet)
#             #   This step copies column i=1 into column i+1=2 for ALL digits:
#             #     prefix[1][2] = prefix[1][1] = 1
#             #     prefix[2][2] = prefix[2][1] = 0
#             #     ... (same copy happens for digits 0, 3, 4, ..., 9)
#             #   So before incrementing, every digit's count just "carries over"
#             for digit in range(10):
#                 self.prefix[digit][i + 1] = self.prefix[digit][i]
            
#             # Step 2: Increment count ONLY for the digit we just saw
#             # 
#             # WHY DUPLICATES WORK:
#             # ====================
#             # This += 1 happens EVERY TIME we encounter the digit,
#             # regardless of whether we've seen it before.
#             # 
#             # Example trace for arr = [1, 1, 1]:
#             #   i=0: arr[0]=1 → prefix[1][1] = 0 + 1 = 1  (first 1)
#             #   i=1: arr[1]=1 → prefix[1][2] = 1 + 1 = 2  (second 1, duplicate!)
#             #   i=2: arr[2]=1 → prefix[1][3] = 2 + 1 = 3  (third 1, duplicate!)
#             # 
#             # Result: prefix[1] = [0, 1, 2, 3]
#             #         All three 1's are counted!
#             # 
#             # The algorithm doesn't distinguish between "first occurrence"
#             # and "duplicate occurrence" - it just counts every occurrence.

#             # if 0 <= current_digit <= 9:
#             self.prefix[current_digit][i + 1] += 1
    
#     def countDigit(self, left: int, right: int, digit: int) -> int:
#         """
#         Return count of 'digit' in subarray arr[left..right] (inclusive).
        
#         Args:
#             left: int - Starting index (inclusive)
#             right: int - Ending index (inclusive)
#             digit: int - Digit to count (0-9)
        
#         Returns:
#             int - Number of occurrences of digit in the range
        
#         Time: O(1), Space: O(1)
        
#         Formula:
#             count(left, right, digit) = prefix[digit][right+1] - prefix[digit][left]
#         """
#         # Validate digit is in range 0-9
#         if digit < 0 or digit > 9:
#             return 0

#         # Handle case where left > right
#         if left > right:
#             return 0

#         # Another option: swap if left > right
#         # if left > right:
#         #     left, right = right, left
        
#         # Handle out of bounds
#         if left < 0 or right >= self.n:
#             return 0

#         # Combined checks: invalid digit, invalid range, or out of bounds
#         # if digit < 0 or digit > 9 or left > right or left < 0 or right >= self.n:
#         #     return 0
        
#         return self.prefix[digit][right + 1] - self.prefix[digit][left]


# What is prefix[d][i]?
# prefix[d][i] = count of digit 'd' in the first 'i' elements

# d = which digit we're counting (0, 1, 2, ..., 9)
# i = how many elements from the start (first i elements)

# arr = [1, 2, 1]
#        ↓  ↓  ↓
# index: 0  1  2

# # Prefix arrays (only showing non-zero ones):

# Create 10 prefix arrays (one for each digit 0-9)
# prefix = [[0] * (n + 1) for _ in range(10)]

# # This creates:
# prefix = [
#     [0, 0, 0, 0],  # prefix[0] for digit 0
#     [0, 0, 0, 0],  # prefix[1] for digit 1
#     [0, 0, 0, 0],  # prefix[2] for digit 2
#     [0, 0, 0, 0],  # prefix[3] for digit 3
#     [0, 0, 0, 0],  # prefix[4] for digit 4
#     [0, 0, 0, 0],  # prefix[5] for digit 5
#     [0, 0, 0, 0],  # prefix[6] for digit 6
#     [0, 0, 0, 0],  # prefix[7] for digit 7
#     [0, 0, 0, 0],  # prefix[8] for digit 8
#     [0, 0, 0, 0],  # prefix[9] for digit 9
# ]

# prefix[1] = [0, 1, 1, 2]  # Count of 1's
#             ↑  ↑  ↑  ↑
#             │  │  │  └─ first 3 elements [1,2,1]: two 1's
#             │  │  └──── first 2 elements [1,2]: one 1
#             │  └─────── first 1 element [1]: one 1
#             └────────── first 0 elements: zero 1's

# prefix[2] = [0, 0, 1, 1]  # Count of 2's
#             ↑  ↑  ↑  ↑
#             │  │  │  └─ first 3 elements [1,2,1]: one 2
#             │  │  └──── first 2 elements [1,2]: one 2
#             │  └─────── first 1 element [1]: zero 2's
#             └────────── first 0 elements: zero 2's

# Query: How many 1's in arr[0..2]?
# countDigit(0, 2, 1)

# = prefix[1][2 + 1] - prefix[1][0]
# = prefix[1][3] - prefix[1][0]
# = 2 - 0
# = 2 

# Verify: arr[0..2] = [1, 2, 1] has two 1's

# Why n+1 size?

# self.prefix = [[0] * (n + 1) for _ in range(10)]

# Reason: Need a base case at index 0 to represent "zero elements processed"
# prefix[d][0] = 0 → count in first 0 elements (none)
# prefix[d][i] = count → count in first i elements
# Enables uniform formula for all queries, especially when left = 0

# Why right + 1?

# return self.prefix[digit][right + 1] - self.prefix[digit][left]

# Reason: prefix[d][i] stores count in first i elements, not up to index i
# Array index right is the (right+1)th element
# To include element at index right, need count of first (right+1) elements
# That's prefix[d][right + 1]


# Follow up : What if there is a lot of digits? 

# Use binary search on position lists instead of prefix sums when the number of distinct digits (k) is large or the value range is unbounded.
# Prefix sums require building a full prefix array for every digit, giving O(n·k) time and space, which becomes impractical when many unique values appear.

# The binary-search method stores only the indices where each digit occurs, using O(n) space, builds in O(n) time, and answers each query in O(log f) where f is the frequency of that digit.
# This makes it far more scalable when the digit range is large, the array is sparse across many values, or memory efficiency matters.

# Suppose:

# arr = [105, 7, 105, 42, 999, 7, 105]

# Distinct digits (values) = {105, 7, 42, 999} → k = 4
# But in real scenarios, values might be huge (1e9+), making k very large.

# ❌ Prefix sum approach

# You would need one prefix array per distinct number:

# prefix[105][…]

# prefix[7][…]

# prefix[42][…]

# prefix[999][…]

# Memory grows as O(n·k).
# If k becomes large (hundreds, thousands, millions), this becomes impossible.

# ✅ Binary-search approach

# Store only positions:

# 105  → [0, 2, 6]
# 7    → [1, 5]
# 42   → [3]
# 999  → [4]

# Now query:
# “Count how many times 105 appears between indices 1 and 6”

# Binary search on [0, 2, 6]:

# lower_bound(1) → index 1 (value = 2)

# upper_bound(6) → index 3 (end)

# Count = 3 − 1 = 2

# Space used: O(n)
# Preprocessing: O(n)
# Query: O(log f) (here f = 3)

# Approach: Use Dictionary/HashMap
# Only create prefix arrays for digits that actually appear in the input.

# If digits range from 0 to 1,000,000:
# # BAD: Creates 1 million arrays!
# self.prefix = [[0] * (n + 1) for _ in range(1000001)]
# # Space: O(1,000,000 * n) - HUGE waste if array only has a few unique digits!


# class Solution:
#     """
#     Count occurrences of any digit in subarrays.
#     Optimized for large digit ranges with few unique values. Not optimal when there are a large number of unique digits. 

#     Example use case:
#         arr = [5, 1000000, 5, 42, 1000000]  # digit values can be huge,
#                                              # but only 3 unique values appear
#         sol = Solution(arr)
#         sol.countDigit(0, 4, 5)        # → 2
#         sol.countDigit(0, 4, 1000000)  # → 2
    
#     This avoids the O(range * n) blowup of a fixed-size array approach
#     (e.g. allocating 1,000,001 prefix arrays just because values go up to 1,000,000),
#     since only digits that actually appear in arr get a prefix array built.
    
#     Time Complexity:
#         - Constructor: O(n * k) where k = unique digits
#         - countDigit: O(1) per query
    
#     Space Complexity: O(k * n) where k = unique digits (not total range!)
#     """
    
#     def __init__(self, arr: List[int]):
#         """
#         Build prefix arrays only for digits that appear in arr.
        
#         Args:
#             arr: List[int] - Array with potentially large digit values
        
#         Time: O(n * k), Space: O(k * n) where k = unique digits
#         """
        
#         n = len(arr)
#         self.n = n
        
#         # Find unique digits in the array
#         unique_digits = set(arr)
        
#         # Create prefix array ONLY for digits that exist
#         # Key: digit, Value: prefix array of size n+1
#         self.prefix = {}
        
#         for digit in unique_digits:
#             # Initialize prefix array for this digit
#             self.prefix[digit] = [0] * (n + 1)
            
#             # Build prefix sum for this digit
#             for i in range(n):
#                 self.prefix[digit][i + 1] = self.prefix[digit][i]

#                 # REQUIRED check: only increment if arr[i] actually equals
#                 # the digit we're currently building a prefix array for.
#                 # Without this, every prefix[digit] would just become
#                 # [0, 1, 2, ..., n] (a plain running count of elements seen),
#                 # identical for every digit and completely wrong.

#                 if arr[i] == digit:
#                     self.prefix[digit][i + 1] += 1
    
#     def countDigit(self, left: int, right: int, digit: int) -> int:
#         """
#         Return count of 'digit' in subarray arr[left..right] (inclusive).
        
#         Args:
#             left: int - Starting index (inclusive)
#             right: int - Ending index (inclusive)
#             digit: int - Digit to count (any value)
        
#         Returns:
#             int - Number of occurrences of digit, or 0 if digit doesn't exist
        
#         Time: O(1), Space: O(1)
#         """
#         # If digit never appeared in array, return 0
#         if digit not in self.prefix:
#             return 0
        
#         # Handle edge cases
#         if left > right or left < 0 or right >= self.n:
#             return 0
        
#         return self.prefix[digit][right + 1] - self.prefix[digit][left]

# Approach : Position lists

# class Solution:
#     """
#     Count occurrences of any digit in subarrays using position lists + binary search.
    
#     WHY THIS WORKS:
#     ===============
#     Core Insight: If we know ALL positions where a digit appears, we can count
#     how many fall within any range [left, right] using binary search.
    
#     Example: 
#         arr = [1, 2, 1, 3, 1]
#         Digit 1 appears at positions: [0, 2, 4]
        
#         To count 1's in range [1, 3]:
#         - Find how many positions in [0, 2, 4] fall within [1, 3]
#         - Answer: position 2 is the only one → count = 1 ✓
    
#     WHY BINARY SEARCH?
#     ==================
#     Since positions are naturally sorted (we encounter them left-to-right),
#     we can use binary search to efficiently find:
#     1. First position >= left (lower_bound)
#     2. First position > right (upper_bound)
#     3. Count = positions between these bounds
    
#     Time Complexity:
#         - Constructor: O(n) - single pass through array
#         - countDigit: O(log f) - binary search where f = frequency of digit
    
#     Space Complexity: O(n) - stores all positions (but only once per element)
#     """
    
#     def __init__(self, arr: List[int]):
#         """
#         Build position dictionary mapping each digit to its indices.
        
#         WHY WE STORE POSITIONS:
#         =======================
#         Instead of storing counts (like prefix sum), we store WHERE each digit
#         appears. This gives us flexibility to answer range queries with binary search.
        
#         WHY DEFAULTDICT(LIST)?
#         ======================
#         - defaultdict: automatically creates empty list for new digits
#         - list: positions are naturally appended in sorted order (index increases)
        
#         Example:
#             arr = [1, 2, 1, 3, 2, 1]
            
#             After processing:
#             pos = {
#                 1: [0, 2, 5],  # digit 1 appears at these indices
#                 2: [1, 4],      # digit 2 appears at these indices
#                 3: [3]          # digit 3 appears at this index
#             }
            
#             KEY PROPERTY: Each list is already sorted! (indices are processed 0→n)
#         """
#         self.n = len(arr)
#         self.pos = defaultdict(list)
        
#         # Store the index where each digit occurs
#         for i, val in enumerate(arr):
#             # Append current index to this digit's position list
#             # WHY APPEND WORKS: Indices are processed in order, so list stays sorted
#             self.pos[val].append(i)
    
#     def lower_bound(self, arr: List[int], target: int) -> int:
#         """
#         Find the first index in arr where arr[index] >= target.
        
#         WHY WE NEED THIS:
#         =================
#         To count elements in range [left, right], we need to find the FIRST
#         position that's >= left. This is the starting point of our count.
        
#         Example:
#             positions = [0, 2, 5, 8]
#             target = 3
            
#             We want first position >= 3:
#             [0, 2, 5, 8]
#              x  x  ✓  ✓  ← which are >= 3?
#                    ↑
#                    This one! (index 2, value 5)
        
#         WHY BINARY SEARCH WORKS:
#         ========================
#         Since positions are sorted, we can eliminate half the search space
#         at each step by checking the middle element.
        
#         INVARIANT MAINTAINED:
#         =====================
#         Throughout the loop:
#         - Everything in [0, left) is < target
#         - Everything in [right, len) is >= target
#         - We're searching in [left, right)
        
#         When loop exits: left == right, and this is our answer
#         """
#         left, right = 0, len(arr)
        
#         while left < right:
#             mid = (left + right) // 2

#         # CRITICAL: Why use "< target" not "<= target"?
#         # =============================================
#         # Because we want to INCLUDE positions equal to target!
        
#         # Example with duplicates:
#         #     positions = [0, 2, 2, 2, 5, 8]
#         #     target = 2
            
#         #     lower_bound should find FIRST 2:
#         #     [0, 2, 2, 2, 5, 8]
#         #      x  ✓  ✓  ✓  ✓  ✓  ← all >= 2
#         #         ↑
#         #         Want index 1 (first 2)
            
#         #     If we used "<= target":
#         #         When mid points to 2:
#         #             Is 2 <= 2? YES → left = mid + 1 (SKIP IT!)
#         #             Would miss the first 2! ❌
            
#         #     With "< target":
#         #         When mid points to 2:
#         #             Is 2 < 2? NO → right = mid (KEEP IT!)
#         #             Correctly finds first 2! ✓
            
#             if arr[mid] < target:
#                 # arr[mid] is too small
#                 # WHY left = mid + 1?
#                 # Because mid is definitely NOT the answer (it's < target)
#                 # So we can skip it and search [mid+1, right)
#                 left = mid + 1
#             else:
#                 # arr[mid] >= target
#                 # WHY right = mid?
#                 # Because mid COULD be the answer (it's >= target)
#                 # But there might be an earlier position that's also >= target
#                 # So we search [left, mid) but keep mid as a candidate
#                 right = mid
        
#         # WHY RETURN left?
#         # When loop exits, left == right, and this is the first index >= target
#         return left
    
#     def upper_bound(self, arr: List[int], target: int) -> int:
#         """
#         Find the first index in arr where arr[index] > target.
        
#         WHY WE NEED THIS:
#         =================
#         To count elements in range [left, right], we need to find the FIRST
#         position that's > right. This marks the END of our count (exclusive).
        
#         Example:
#             positions = [0, 2, 5, 8]
#             target = 5
            
#             We want first position > 5:
#             [0, 2, 5, 8]
#              x  x  x  ✓  ← which are > 5?
#                       ↑
#                       This one! (index 3, value 8)
        
#         WHY USE > INSTEAD OF >=?
#         ========================
#         Because we want to INCLUDE the target value in our count.
#         If target = right, we want to count positions == right.
#         So we find first position AFTER right.
        
#         INVARIANT MAINTAINED:
#         =====================
#         Throughout the loop:
#         - Everything in [0, left) is <= target
#         - Everything in [right, len) is > target
#         - We're searching in [left, right)
#         """
#         left, right = 0, len(arr)
        
#         while left < right:
#             mid = (left + right) // 2

#         # CRITICAL: Why use "<= target" not "< target"?
#         # =============================================
#         # Because we want to EXCLUDE positions equal to target!
#         # We need to skip over all equal values.
        
#         # Example with duplicates:
#         #     positions = [0, 2, 2, 2, 5, 8]
#         #     target = 2
            
#         #     upper_bound should find FIRST position AFTER all 2's:
#         #     [0, 2, 2, 2, 5, 8]
#         #      x  x  x  x  ✓  ✓  ← which are > 2?
#         #                  ↑
#         #                  Want index 4 (first value > 2)
            
#         #     If we used "< target":
#         #         When mid points to 2:
#         #             Is 2 < 2? NO → right = mid (STOP HERE!)
#         #             Would return a position with value 2! ❌
            
#         #     With "<= target":
#         #         When mid points to 2:
#         #             Is 2 <= 2? YES → left = mid + 1 (SKIP IT!)
#         #             Correctly skips all 2's! ✓
            
#             if arr[mid] <= target:
#                 # arr[mid] is too small or equal
#                 # WHY left = mid + 1?
#                 # Because mid is definitely NOT the answer (it's <= target)
#                 # We need something STRICTLY greater than target
#                 left = mid + 1
#             else:
#                 # arr[mid] > target
#                 # WHY right = mid?
#                 # Because mid COULD be the answer (it's > target)
#                 # But there might be an earlier position that's also > target
#                 right = mid
        
#         return left
    
#     def countDigit(self, left: int, right: int, digit: int) -> int:
#         """
#         Count occurrences of 'digit' in subarray arr[left..right] (inclusive).
        
#         WHY THIS ALGORITHM WORKS:
#         =========================
        
#         Key insight: If we know all positions where digit appears (sorted),
#         counting how many fall in [left, right] is just finding a range!
        
#         Visual example:
#             arr = [1, 2, 1, 3, 2, 1]
#                    0  1  2  3  4  5  ← indices
            
#             pos[1] = [0, 2, 5]  ← all positions where 1 appears
            
#             Query: countDigit(1, 4, 1) - count 1's in arr[1..4]
            
#             Step 1: Find first position >= 1
#                     [0, 2, 5]
#                      x  ✓  ✓  ← which are >= 1?
#                         ↑
#                         start = 1 (index in pos[1], not in arr!)
            
#             Step 2: Find first position > 4
#                     [0, 2, 5]
#                      x  ✓  x  ← which are > 4?
#                            ↑
#                            end = 2 (index in pos[1], not in arr!)
            
#             Step 3: Count = end - start
#                     Positions in range: pos[1][1:2] = [2]
#                     So there's 1 occurrence at arr[2] = 1 ✓
        
#         WHY end - start WORKS:
#         ======================
#         start = first valid position (inclusive)
#         end = first invalid position (exclusive)
#         Count = number of elements in [start, end) = end - start
        
#         This is the same as slicing: pos[digit][start:end] has (end - start) elements
        
#         Example:
#             indices = [0, 2, 5, 8, 10]
#             start = 1, end = 4
            
#             indices[start:end] = indices[1:4] = [2, 5, 8]
#             length = 4 - 1 = 3 ✓

#         WHAT IS f?
#         ==========
#         f = len(self.pos[digit]) = the number of times 'digit' appears
#         anywhere in the original arr (its frequency).
        
#         It's not a separate stored variable — it's simply the length of
#         the 'indices' list below, which both lower_bound and upper_bound
#         binary search over. A rare digit (small f) means a short list and
#         a fast search; a very common digit (large f) means a longer list
#         and a slightly slower (but still logarithmic) search.
        
#         Example: arr = [1, 2, 1, 3, 2, 1] → pos[1] = [0, 2, 5] → f = 3 for digit 1
        
#         WHY O(log f) TIME?
#         ==================
#         We do two binary searches on a list of f positions.
#         Each binary search is O(log f).
#         Total: O(log f) + O(log f) = O(log f)
#         """
#         # Handle invalid range
#         # WHY CHECK THIS? Prevents incorrect results for malformed queries
#         if left > right:
#             return 0

#         # Optional: Explicit bounds check (recommended for clarity)
#         if left < 0 or right >= self.n:
#             return 0
        
#         # Get sorted list of positions where digit appears
#         # WHY .get(digit, [])? Returns empty list if digit never appears
#         indices = self.pos.get(digit, [])
        
#         # If digit never appears in array, return 0
#         # WHY CHECK THIS? Avoids binary search on empty list
#         if not indices:
#             return 0
        
#         # Find first position >= left
#         # WHY? This is where our count starts
#         # Result is an INDEX into the 'indices' list, not an array index!
#         start = self.lower_bound(indices, left)
        
#         # Find first position > right
#         # WHY? This is where our count ends (exclusive)
#         # Result is an INDEX into the 'indices' list, not an array index!
#         end = self.upper_bound(indices, right)
        
#         # Count = number of positions in range [left, right]
#         # WHY end - start?
#         # - start: first valid position (inclusive)
#         # - end: first invalid position (exclusive)
#         # - Number of elements from start to end (exclusive) = end - start
#         return end - start


# Alternative : Using Python's bisect

# from bisect import bisect_left, bisect_right

# class Solution:
#     """
#     Cleaner version using Python's built-in bisect module.
#     """
    
#     def __init__(self, arr: List[int]):
#         """
#         Build position dictionary.
        
#         Time: O(n), Space: O(n)
#         """
#         self.pos = defaultdict(list)
#         for i, val in enumerate(arr):
#             self.pos[val].append(i)
    
#     def countDigit(self, left: int, right: int, digit: int) -> int:
#         """
#         Count occurrences using bisect_left and bisect_right.
        
#         Time: O(log f), Space: O(1)
#         """
#         if left > right:
#             return 0
        
#         indices = self.pos.get(digit, [])
#         if not indices:
#             return 0
        
#         # bisect_left: first position >= left
#         start = bisect_left(indices, left)
        
#         # bisect_right: first position > right
#         end = bisect_right(indices, right)
        
#         return end - start