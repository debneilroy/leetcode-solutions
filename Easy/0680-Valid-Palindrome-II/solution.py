"""
LeetCode 680. Valid Palindrome II
Difficulty: Easy
URL: https://leetcode.com/problems/valid-palindrome-ii/
"""

# Brute-force: For each index i in the string (including the case of deleting nothing if you first check the original), form a new string by skipping s[i]:
# t = s[0:i]+s[i+1:]
# Then check if t is a palindrome using two pointers. If any such t is a palindrome (or the original string is already one), return true; otherwise return false.

# Time Complexity: O(n²) - we try n deletions, each palindrome check takes O(n)
# Space Complexity: O(n) - for creating substrings


# Approach : Two Pointers

class Solution:
    def validPalindrome(self, s: str) -> bool:
        """
        Determines if a string can be a palindrome after deleting at most one character. Ex : s = 'abxaaaba' is a palindrome by deleting character x.
        
        Time Complexity: O(n)
            - Main two-pointer scan: O(n)
            - In worst case, isPalindrome helper scans remaining substring: O(n)
            - Overall: O(n)
        
        Space Complexity: O(1)
            - Only using pointer variables
            - No additional data structures needed
        """
        
        def isPalindrome(left: int, right: int) -> bool:
            """
            Helper function to check if substring s[left:right+1] is a palindrome.
            
            Args:
                left: Starting index of substring
                right: Ending index of substring
            
            Returns:
                True if substring is a palindrome, False otherwise
            """
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True
        
        # Initialize two pointers at both ends
        left, right = 0, len(s) - 1
        
        # Move pointers inward, comparing characters
        while left < right:
            # If characters don't match, we found our potential deletion point
            if s[left] != s[right]:
                # Try two options:
                # Option 1: Skip left character, check if rest is palindrome
                # Option 2: Skip right character, check if rest is palindrome
                # If either works, we can make it a palindrome with one deletion
                return isPalindrome(left + 1, right) or isPalindrome(left, right - 1)
            
            # Characters match, continue moving inward
            left += 1
            right -= 1
        
        # Reached the middle without any mismatches - already a palindrome
        return True


# Follow up : Leetcode 1216 (Valid Palindrome III)


        