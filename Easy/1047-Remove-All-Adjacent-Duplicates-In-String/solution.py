"""
LeetCode 1047. Remove All Adjacent Duplicates In String
Difficulty: Easy
URL: https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/
"""

# The brute force approach would be to repeatedly scan the string from left to right, find the first adjacent duplicate pair, remove it, then restart the scan from the beginning. We keep doing this until no more duplicates are found. This requires multiple passes through the string - in the worst case O(n) passes (since we can remove at most n/2 pairs), each taking O(n) time to scan, giving us O(n) × O(n) = O(n²) time complexity and O(n) space for creating new strings.

class Solution:
    def removeDuplicates(self, s: str) -> str:
        """
        Approach: Use a stack to track characters
        - If current char matches stack top: they form a duplicate pair, so pop
        - Otherwise: push current char onto stack
        
        Time Complexity: O(n) where n = length of string
        - We iterate through the string once: O(n)
        - Each character is pushed at most once: O(n)
        - Each character is popped at most once: O(n)
        - join() operation at the end: O(n)
        - Total: O(n)
        
        Space Complexity: O(n) where n = length of string
        - Stack can grow up to size n in worst case (when no duplicates exist)
        - Example: "abcdef" would result in stack = ['a','b','c','d','e','f']
        - The output string also takes O(n) space
        - Total: O(n)

        Edge Cases:
        - Empty string: "" → ""
        - Single character: "a" → "a" (no duplicates to remove)
        - Two same characters: "aa" → ""
        - All duplicates: "aabbcc" → ""
        - No duplicates: "abcd" → "abcd" (all characters remain)
        - All same character (even): "aaaa" → "" (pairs cancel out)
        - All same character (odd): "aaaaa" → "a" (one remains)
        - Cascading removals: "abccba" → "" 
          (remove "cc" → "abba", remove "bb" → "aa", remove "aa" → "")
        - Large string with no duplicates: maintains O(n) time and space
        - Alternating pattern: "ababab" → "ababab" (no adjacent duplicates)
        """

        # Base case 1: Empty string - return immediately
        if not s:
            return ""
        
        # Base case 2: Single character - no duplicates possible
        if len(s) == 1:
            return s
        
        # Base case 3: Two characters - check if they're duplicates
        if len(s) == 2:
            return "" if s[0] == s[1] else s

        # Initialize empty stack to store characters
        stack = []
        
        # Process each character in the string
        for char in s:
            # Check if stack has elements AND top element matches current char
            if stack and stack[-1] == char:
                # Found adjacent duplicate: remove the previous char
                stack.pop()
            else:
                # No duplicate: add current char to stack
                stack.append(char)
        
        # Convert stack (list of chars) back to string
        return ''.join(stack)

# Variant 1: Remove All Adjacent Duplicate Runs

# You are given a string s consisting of lowercase English letters. A run is defined as a sequence of 2 or more consecutive identical characters. Repeatedly remove all runs from the string until no more runs can be removed. When a run is removed, the characters on either side of it may form a new run, which should also be removed. Return the final string after all runs have been removed.

# Example 1:
# Input: s = "abbbacca"
# Output: "a"

# Explanation:
# Step 1: Remove run "bbb" → string becomes "aacca"
# Step 2: Remove run "aa" → string becomes "cca"  
# Step 3: Remove run "cc" → string becomes "a"
# No more runs can be removed.
# Final result: "a"

# Example 2:
# Input: s = "aabbcc"
# Output: ""

# Explanation:
# Step 1: Remove run "aa" → string becomes "bbcc"
# Step 2: Remove run "bb" → string becomes "cc"
# Step 3: Remove run "cc" → string becomes ""
# Final result: ""

# Check the python code from codingwithminmer.com (the below version is preferred in interview)

def removeAdjacentDuplicateRuns(s: str) -> str:
    """
    Remove all runs of 2+ consecutive identical characters.
    Continue until no more runs can be removed (cascading).
    
    Approach: Use stack to track [character, count]
    - When we see same char, increment count
    - When we see different char:
        - If previous run has count > 1, remove it (pop)
        - Check if new char matches the new top (cascading!)
    
    Time Complexity: O(n)
    - Each character processed once
    - Each push/pop operation is O(1)
    
    Space Complexity: O(n)
    - Stack can hold up to n characters in worst case
    
    Examples:
    - "abbbacca" → "a" (remove "bbb" → "aacca", remove "aa" → "cca", remove "cc" → "a")
    - "abbaca" → "ca" (remove "bb" → "aaca", remove "aa" → "ca")
    - "abccbd" → "ad" (remove "cc" → "abbd", remove "bb" → "ad")
    
    Edge Cases:
    - Empty string: "" → ""
    - Single character: "a" → "a" (no runs)
    - Two same characters: "aa" → "" (run of 2)
    - Two different characters: "ab" → "ab" (no runs)

    Note ON CASCADING (post-pop recheck is required here, unlike LC 1209):
    1209 pops on count==k -- the matching char itself triggers and is
    consumed by the pop, so nothing's left to recheck. Here, run length
    is unbounded, so a pop is only triggered by a MISMATCH -- the char
    that caused it is still unplaced and may equal the new top.
    Example: "abbbacca" -- popping "bbb" exposes top 'a', and current
    char is also 'a' -> must merge -> [['a',2]], not push a duplicate
    entry. Skip this check and the result corrupts to "aaa" instead of "a".
    
    """
    
    # Base case 1: Empty string has no characters to process
    if not s:
        return ""
    
    # Base case 2: Single character cannot form a run (need 2+)
    # Example: "a" → "a" (no run, keep it)
    if len(s) == 1:
        return s
    
    # [Optional] Base case 3: Two characters - simple direct check 
    # If same → it's a run of 2, remove both
    # If different → no run, keep both
    # Examples: "aa" → "", "ab" → "ab"
    if len(s) == 2:
        return "" if s[0] == s[1] else s
    
    # ============================================================
    # MAIN ALGORITHM - Process strings with 3+ characters
    # ============================================================
    
    # Stack stores [character, count] pairs
    # Example: [['a', 1], ['b', 2]] means "a" appears once, then "b" appears twice
    stack = []
    
    # Process each character in the string
    for char in s:
        
        # CASE 1: Current character continues the existing run
        # Example: stack = [['a', 2]], char = 'a' → increment to [['a', 3]]
        if stack and stack[-1][0] == char:
            stack[-1][1] += 1  # Increment count of current run
            
        # CASE 2: Current character is different - potential run removal
        else:
            # Step 2a: Check if the previous run needs to be removed
            # A run has 2+ characters, so if count > 1, it's a run
            # Example: stack = [['a', 1], ['b', 3]], 'b' is a run → remove it
            if stack and stack[-1][1] > 1:
                stack.pop()  # Remove the completed run
            
            # Step 2b: CASCADING CHECK - After removing, check if current char
            # matches what's now at the top of the stack
            # This is KEY for handling cascading removals!
            # Example: stack was [['a', 2], ['b', 3]], removed 'bbb'
            #          Now stack = [['a', 2]], and if current char is 'a',
            #          they should merge!
            if stack and stack[-1][0] == char:
                # Current char matches the newly exposed top!
                # Increment the count of that existing run
                # Example: [['a', 2]] + char 'a' → [['a', 3]]
                stack[-1][1] += 1
            else:
                # Current char doesn't match top (or stack is empty)
                # Start a brand new run with count 1
                # Example: [['a', 1]] + char 'b' → [['a', 1], ['b', 1]]
                stack.append([char, 1])
    
    # ============================================================
    # FINAL CLEANUP - Handle the last run if it exists
    # ============================================================
    
    # After processing all characters, check if the last entry is a run
    # Example: stack = [['a', 1], ['b', 3]] → 'bbb' is a run, remove it
    if stack and stack[-1][1] > 1:
        stack.pop()
    
    # ============================================================
    # BUILD RESULT - Convert stack back to string
    # ============================================================
    
    # Reconstruct the final string from remaining characters
    # Each stack entry is [char, count], so repeat char 'count' times
    # Example: [['a', 1], ['b', 2]] → "a" + "bb" = "abb"
    result = []
    for char, count in stack:
        result.append(char * count)  # Repeat character 'count' times
    
    # Join all parts into final string
    return ''.join(result)

# If input is a list instead of a string

def removeAdjacentDuplicateRuns(arr):
    """
    Remove all runs of 2+ consecutive identical characters.
    Continue until no more runs can be removed (cascading).
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        ['a','b','b','b','a','c','c','a'] → ['a']
        ['a','b','b','a','c','a'] → ['c', 'a']
        ['a','a','b','b','c','c'] → []
    
    Args:
        arr: List of single characters
        
    Returns:
        List of characters after all run removals
    """
    # Base cases
    if not arr:
        return []
    if len(arr) == 1:
        return arr
    if len(arr) == 2:
        return [] if arr[0] == arr[1] else arr
    
    # Stack stores [character, count] pairs
    stack = []
    
    for ch in arr:
        # CASE 1: Current char continues existing run
        if stack and stack[-1][0] == ch:
            # Increment count of current run
            stack[-1][1] += 1
            
        # CASE 2: Current char is different
        else:
            # Step 2a: Check if previous run needs removal (count > 1)
            if stack and stack[-1][1] > 1:
                stack.pop()
            
            # Step 2b: CASCADING - Check if current char matches NEW top
            if stack and stack[-1][0] == ch:
                # Matches! Increment existing run
                stack[-1][1] += 1
            else:
                # Doesn't match (or stack empty) - start new run
                stack.append([ch, 1])
    
    # Final check: Remove last run if it has 2+ chars
    if stack and stack[-1][1] > 1:
        stack.pop()
    
    # Build result - all remaining entries have count = 1
    # (since we removed all runs with count > 1)
    result = []
    for char, count in stack:
        result.append(char)  # count is always 1 here
    
    return result

# Variant 2: Leetcode 1209



        