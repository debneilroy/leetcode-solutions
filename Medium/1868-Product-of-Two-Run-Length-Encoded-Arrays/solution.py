"""
LeetCode 1868. Product of Two Run-Length Encoded Arrays
Difficulty: Medium
URL: https://leetcode.com/problems/product-of-two-run-length-encoded-arrays/
"""

class Solution:
    def findRLEArray(self, encoded1, encoded2):
        """
        Find the product of two run-length encoded arrays.
        
        Time Complexity: O(n + m) where n = len(encoded1), m = len(encoded2)
        - We traverse each encoded array exactly once
        - Each element is processed once with constant-time operations
        
        Space Complexity: O(k) where k is the length of the output array
        - Best case: O(1) when all products can be merged into one element
        - Worst case: O(n + m) when no consecutive products can be merged
        - Auxiliary space: O(1) for pointers and temporary variables
        
        Args:
            encoded1: List[List[int]] - RLE array [[val, freq], ...]
            encoded2: List[List[int]] - RLE array [[val, freq], ...]
        
        Returns:
            List[List[int]] - Product array in RLE format
        """
        result = []
        i = j = 0  # Pointers for encoded1 and encoded2
        
        # Track remaining frequencies for current elements
        freq1_remaining = encoded1[0][1]
        freq2_remaining = encoded2[0][1]
        
        # Process both arrays until we've consumed all elements
        while i < len(encoded1) and j < len(encoded2):
            # Get current values from both arrays
            val1 = encoded1[i][0]
            val2 = encoded2[j][0]
            
            # Calculate product of current values
            product = val1 * val2
            
            # Take minimum of remaining frequencies
            # This is how many times we can use this product before
            # one of the arrays moves to its next element
            min_freq = min(freq1_remaining, freq2_remaining)
            
            # Add to result, merging with previous element if same product
            # This keeps the output optimally compressed
            if result and result[-1][0] == product:
                result[-1][1] += min_freq
            else:
                result.append([product, min_freq])
            
            # Decrease remaining frequencies by amount we just used
            freq1_remaining -= min_freq
            freq2_remaining -= min_freq
            
            # Move to next element in encoded1 if current is exhausted
            if freq1_remaining == 0:
                i += 1
                if i < len(encoded1):
                    freq1_remaining = encoded1[i][1]
            
            # Move to next element in encoded2 if current is exhausted
            if freq2_remaining == 0:
                j += 1
                if j < len(encoded2):
                    freq2_remaining = encoded2[j][1]
        
        return result



# class Solution:
#     def findRLEArray(self, encoded1: List[List[int]], encoded2: List[List[int]]):
#         i, j = 0, 0
#         result = []

#         # Loop through both RLE lists until we reach the end of either list
#         while i < len(encoded1) and j < len(encoded2):
#             # Get the value and the count from both encoded arrays
#             val1, freq1 = encoded1[i]
#             val2, freq2 = encoded2[j]

#             # Calculate the product of values
#             product = val1 * val2

#             # The run length for the product is the minimum of both run lengths
#             freq = min(freq1, freq2)

#             # Add product to result if it's not zero, or the result list is empty
#             if not result or result[-1][0] != product:
#                 result.append([product, freq])
#             else:
#                  # If the last product is the same, merge it by increasing its length
#                 result[-1][1] += freq

#             # Update the lengths of current RLE segments
              # These lines MODIFY the input arrays:
#             encoded1[i][1] -= freq
#             encoded2[j][1] -= freq

#             # Move to next segment in RLE if the current segment is exhausted
#             if encoded1[i][1] == 0:
#                 i += 1
#             if encoded2[j][1] == 0:
#                 j += 1

#         return result

# Testcase for segments merge : encoded1 = [[1,3],[2,1],[3,2]], encoded2 = [[2,3],[1,3]]
# TC : O(n + m), n is the number of segments in encoded1 and m is the number of segments in encoded2.
# SC : O(n + m)
        