"""
LeetCode 1209. Remove All Adjacent Duplicates in String II
Difficulty: Medium
URL: https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/
"""

# Approach : Stack

class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        """
        Remove k consecutive duplicate characters using a stack.
        
        Approach:
        - Use stack to store [character, count] pairs
        - When we see same char, increment count
        - When count reaches k, pop (remove all k chars)
        - When we see different char, start new entry
        
        Time Complexity: O(n)
        - Single pass through string: O(n)
        - Each character pushed once: O(n)
        - Each character popped once: O(n)
        - Building result: O(n)
        - Total: O(n)
        
        Space Complexity: O(n)
        - Stack can hold up to n entries in worst case
        - Example: "abcdef" with k=2 → stack has 6 entries
        """
        # Stack stores [character, count] pairs
        stack = []
        
        for char in s:
            # If stack not empty and top character matches current
            if stack and stack[-1][0] == char:
                # Increment count for this character
                stack[-1][1] += 1
                
                # If count reaches k, remove all k occurrences
                if stack[-1][1] == k:
                    stack.pop()
            else:
                # New character, push with count 1
                stack.append([char, 1])
        
        # Build result string from stack
        result = []
        for char, count in stack:
            result.append(char * count)  # Repeat char 'count' times
        
        return ''.join(result)

# Approach : Two pointer

# class Solution:
#     def removeDuplicates(self, s: str, k: int) -> str:
#         """
#         Two-pointer in-place approach (simulating stack).
        
#         Key Idea:
#         - 'write' pointer indicates where to write next character (stack top + 1)
#         - When we see k consecutive chars, move write pointer back by k
#         - This simulates popping k elements from stack
        
#         Time Complexity: O(n)
#         Space Complexity: O(n) for chars array + counts array
#         """
#         # Convert to list for in-place modification
#         chars = list(s)
        
#         # counts[i] = number of consecutive identical chars ending at position i
#         counts = [0] * len(s)
        
#         # Write pointer (stack top position)
#         write = 0
        
#         for read in range(len(s)):
#             # Place current character at write position
#             chars[write] = chars[read]
            
#             # Calculate count for this position
#             if write == 0:
#                 # First position
#                 counts[write] = 1
#             elif chars[write] == chars[write - 1]:
#                 # Same as previous character
#                 counts[write] = counts[write - 1] + 1
#             else:
#                 # Different from previous character
#                 counts[write] = 1
            
#             # If we've accumulated k consecutive chars, remove them
#             if counts[write] == k:
#                 write -= k  # Move write pointer back (simulate k pops)
            
#             # Move write pointer forward for next character
#             write += 1
        
#         # Return valid portion of the array
#         return ''.join(chars[:write])

        
        