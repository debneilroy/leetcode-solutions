"""
LeetCode 347. Top K Frequent Elements
Difficulty: Medium
URL: https://leetcode.com/problems/top-k-frequent-elements/
"""

# Approach : Bucket Sort

# Count frequencies of each number using a dictionary.

# Group numbers into buckets where the index represents the frequency (e.g., buckets[3] holds numbers that appear 3 times).

# Traverse the buckets in reverse (from highest frequency to lowest) and collect numbers until we have k elements.

class Solution:
    def topKFrequent(self, nums, k):
        # Step 1: Count the frequency of each number
        freq_map = {}
        for num in nums:
            if num in freq_map:
                freq_map[num] += 1
            else:
                freq_map[num] = 1

        # Step 2: Create buckets where index = frequency
        # We need n + 1 buckets because the max frequency of any element is at most n (length of nums)
        # buckets[0] will remain empty because no number appears 0 times
        n = len(nums)
        buckets = [[] for _ in range(n + 1)]

        # Step 3: Fill the buckets with numbers based on their frequency
        for num, freq in freq_map.items():
            buckets[freq].append(num)

        # Step 4: Collect top k frequent elements starting from highest frequency
        result = []
        for freq in range(n, 0, -1):  # Start from highest frequency
            for num in buckets[freq]:
                result.append(num)
                if len(result) == k:
                    return result  # Return once we have k elements

        # In theory, we should never reach this return if inputs are valid
        # return result



# Time Complexity: O(n)
# 1. Count frequencies: O(n)

# 2. Fill buckets: O(n)

# 3. Collect top k elements: O(n)

# Space Complexity: O(n)
# 1. Frequency map: O(n)

# 2. Buckets: O(n)

# 3. Result array: up to O(k) ⊆ O(n)


        