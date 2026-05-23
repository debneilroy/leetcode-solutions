"""
LeetCode 408. Valid Word Abbreviation
Difficulty: Easy
URL: https://leetcode.com/problems/valid-word-abbreviation/
"""

# Brute Force Approach

# Idea:
# Try all possible abbreviations of the given word and check if any of them equals the given abbr.

# At each character in word, you have two choices:

# 1. Keep the character as it is.

# 2. Replace some substring starting here with its length (i.e., start a number).

# Thus, every character can either be “kept” or “counted” → exponential combinations.

# | Decision Path | Abbreviation                  |
# |---------------| ------------------------------|
# | keep all      | "cat"                         |
# | skip 1 char   | "1at"                         |
# | skip 2 chars  | "2t"                          |
# | skip 3 chars  | "3"                           |
# | mix keep/skip | "c1t", "ca1", "1a1", etc.     |

# Time Complexity: O(2^n)

# Each position in word offers two main choices → roughly 2^n possible abbreviation patterns.

# Space Complexity: O(2^n) or O(n)

# O(2^n) if you store all abbreviations in a list or set before comparing.

# O(n) if you compare on the fly during recursion (just recursion stack and a small temporary buffer).

class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        """
        Validates if an abbreviation matches a given word.
        
        Time Complexity: O(n + m) where n = len(word), m = len(abbr)
        - We traverse each character in word once (pointer i moves forward only)
        - We traverse each character in abbr once (pointer j moves forward only)
        
        Space Complexity: O(1)
        - Only using constant extra space for pointers and temporary variables

        """
        # i points to the current character in `word`, j points to `abbr`
        i, j = 0, 0
        
        while i < len(word) and j < len(abbr):
            # Check for alphabetic characters in abbreviation
            if abbr[j].isalpha():
                # Letters must match exactly at current positions
                if word[i] != abbr[j]:
                    return False
                i += 1
                j += 1
            else:
                # Handle numeric parts in abbreviation
                
                # Check for leading zero (invalid abbreviation)
                if abbr[j] == "0":
                    return False
                
                # Compute the number of characters to skip
                skip_count = 0
                # Build complete multi-digit number (e.g., "12" not just "1" and "2")
                while j < len(abbr) and abbr[j].isdigit():
                    skip_count = skip_count * 10 + int(abbr[j])
                    j += 1
                
                # Skip 'skip_count' characters in the original word
                i += skip_count
        
        # Valid only if both strings are completely consumed
        # i should reach end of word, j should reach end of abbr
        return i == len(word) and j == len(abbr)

# Another approach

# class Solution:
#     def validWordAbbreviation(self, word: str, abbr: str) -> bool:
#         i = 0  # pointer for word
#         j = 0  # pointer for abbr
        
#         while i < len(word) and j < len(abbr):
#             # If current char in abbr is a digit
#             if abbr[j].isdigit():
#                 # Check for leading zero
#                 if abbr[j] == '0':
#                     return False
                
#                 # Build the complete number
#                 num = 0
#                 while j < len(abbr) and abbr[j].isdigit():
#                     num = num * 10 + int(abbr[j])
#                     j += 1
                
#                 # Skip 'num' characters in word
#                 i += num
#             else:
#                 # Characters must match
#                 if word[i] != abbr[j]:
#                     return False
#                 i += 1
#                 j += 1
        
#         # Both pointers should reach the end
#         return i == len(word) and j == len(abbr)

# without using  isalpha() or isdigit()

# class Solution:
#     def validWordAbbreviation(self, word: str, abbr: str) -> bool:
#         i, j = 0, 0
        
#         while i < len(word) and j < len(abbr):
#             # Check if current char is a digit (0-9)
#             if '0' <= abbr[j] <= '9':
#                 if abbr[j] == '0':  # Leading zero check
#                     return False
                
#                 tmp = 0
#                 while j < len(abbr) and '0' <= abbr[j] <= '9':
#                     tmp = tmp * 10 + (ord(abbr[j]) - ord('0'))
#                     j += 1
#                 i += tmp
#             else:
#                 # It's a letter
#                 if word[i] != abbr[j]:
#                     return False
#                 i += 1
#                 j += 1
        
#         return i == len(word) and j == len(abbr)

# What is ord()?
# ord() returns the ASCII/Unicode value of a character.
# ord('0') = 48
# ord('1') = 49
# ord('2') = 50
# ...
# ord('9') = 57
# Why subtract ord('0')?
# To convert a digit character to its numeric value:
# ord('5') - ord('0') = 53 - 48 = 5
# ord('7') - ord('0') = 55 - 48 = 7
# ord('0') - ord('0') = 48 - 48 = 0


# Variant : Valid Word Abbreviation with Wildcard

# A string can be abbreviated by replacing any number of non-adjacent, non-empty substrings with their lengths.
# The lengths do not have leading zeros.

# Moreover, wildcard pattern matching should be supported, where * matches any sequence of characters (including the empty sequence).

# Given a string word and an abbreviation abbr, return whether the string matches the given abbreviation.

# A substring is a contiguous non-empty sequence of characters within a string.

# Example 1
# Input:  word = "abc", abbr = "*"
# Output: true
# Explanation: '*' matches any sequence.

# Example 2
# Input:  word = "tadpoletech", abbr = "*pole*hie"
# Output: false
# Explanation:
# The first '*' matches "tad" and the second '*' matches "tec", but "ie" is not present in the word.

# Example 3
# Input:  word = "minmerhq", abbr = "mi*e2q***"
# Output: true

# Approach : Recursion

# class Solution:
#     def wordPatternMatch(self, word: str, abbr: str) -> bool:
#         """
#         Validates if a word matches an abbreviation pattern with wildcards.
        
#         Time Complexity: O(2^(n+m)) where n = len(word), m = len(abbr)
#         - In worst case with wildcards, we explore exponential paths due to branching
#         - Each wildcard creates 2 choices: skip it or consume a character
#         - Maximum recursion depth is n+m, and each level can branch into 2
#         - Without memoization, we revisit the same states multiple times
        
#         Space Complexity: O(n + m)
#         - Recursion stack depth is at most n + m
#         - We use i from 0 to n and j from 0 to m
#         - Each recursive call uses constant extra space
        
#         Args:
#             word: The original word to validate against
#             abbr: The abbreviation pattern with wildcards (*), numbers, and letters
            
#         Returns:
#             True if word matches the abbreviation pattern, False otherwise
#         """
#         return self.match(word, abbr, 0, 0)
    
#     def match(self, word: str, abbr: str, i: int, j: int) -> bool:
#         """
#         Recursively match word and abbr starting from positions i and j.
        
#         Args:
#             word: The word to match
#             abbr: The abbreviation pattern
#             i: Current position in word (0 to len(word))
#             j: Current position in abbr (0 to len(abbr))
            
#         Returns:
#             True if remaining parts match, False otherwise
#         """
#         # Base case: both strings fully consumed - valid match
#         # Example: word="ab", abbr="ab" → both reach end together ✓
#         if i == len(word) and j == len(abbr):
#             return True
        
#         # Abbr exhausted but word has remaining characters - no match
#         # Example: word="abcde", abbr="ab" → abbr done but word has "cde" left ✗
#         if j == len(abbr):
#             return False
        
#         # Word exhausted but abbr has remaining characters
#         # Example: word="ab", abbr="ab***" or word="ab", abbr="ab**c"
#         if i == len(word):
#             # Valid only if all remaining characters in abbr are wildcards
#             # Wildcards can match empty sequence, so "ab" matches "ab***" ✓
#             # But "ab" does NOT match "ab**c" because we need 'c' ✗
#             while j < len(abbr):
#                 if abbr[j] != '*':
#                     # Found a non-wildcard character, but word is exhausted
#                     # Example: abbr="ab**c" has 'c' at the end → cannot match
#                     return False
#                 j += 1
#             # All remaining characters are wildcards → they match empty sequence
#             # Example: abbr="ab***" has only wildcards left → valid match ✓
#             return True
        
#         # Case 1: Handle wildcard '*' - matches any sequence (0 or more chars)
#         # Example: word="helzzp", abbr="h2*p" where * needs to match "zz"
#         if abbr[j] == '*':
#             # Option A: Match 0 characters (skip the wildcard)
#             # Try to see if skipping this wildcard works
#             # Example: word="abc", abbr="*bc" → skip *, try matching "abc" with "bc"
#             if self.match(word, abbr, i, j + 1):
#                 return True
            
#             # Option B: Match 1+ characters (consume from word, keep wildcard)
#             # Wildcard stays at j while we advance i (consume characters)
#             # Example: word="helzzp", abbr="h2*p" → * consumes 'z', then another 'z'
#             if self.match(word, abbr, i + 1, j):
#                 return True
            
#             # Both options failed - no valid match found
#             return False
        
#         # Case 2: Handle digit - represents number of characters to skip
#         # Example: word="hello", abbr="h2lo" → '2' means skip 2 chars ('e' and 'l')
#         if abbr[j].isdigit():
#             # Leading zeros are invalid
#             # Example: abbr="h0llo" is invalid ✗
#             if abbr[j] == '0':
#                 return False
            
#             # Build the complete multi-digit number
#             # Example: abbr="h12o" → skip_count=12 (not just 1 and 2 separately)
#             skip_count = 0
#             while j < len(abbr) and abbr[j].isdigit():
#                 skip_count = skip_count * 10 + int(abbr[j])
#                 j += 1
            
#             # Check if we can skip that many characters without exceeding word length
#             # Example: word="hi", abbr="h5" → can't skip 5 chars from position 1 ✗
#             if i + skip_count > len(word):
#                 return False
            
#             # Recursively match after skipping skip_count characters
#             # Example: word="hello", abbr="h2lo" → skip 2 chars, match from "llo" vs "lo"
#             return self.match(word, abbr, i + skip_count, j)
        
#         # Case 3: Handle letter - must match exactly
#         # Example: word="abc", abbr="abc" → each letter must match exactly
#         if abbr[j].isalpha():
#             # Characters must be identical
#             # Example: word="abc", abbr="axc" → 'b' != 'x' ✗
#             if word[i] != abbr[j]:
#                 return False
            
#             # Move both pointers forward
#             # Example: word="abc", abbr="abc" → match 'a', continue with "bc" vs "bc"
#             return self.match(word, abbr, i + 1, j + 1)
        
#         # Invalid character in abbr (shouldn't happen with valid input)
#         return False

# Time Complexity: O(2^(n+m))
# For time complexity, in the worst case we have exponential time. Here's why:
# When we hit a wildcard, we branch into 2 recursive calls - one where we skip it, one where we consume a character. If we have multiple wildcards, each one creates this branching behavior.
# The maximum depth of our recursion is n+m since we can advance through both strings. At each level with a wildcard, we might explore 2 paths, giving us roughly 2^(n+m) in the absolute worst case.
# Without memoization, we end up revisiting the same (i, j) states multiple times through different paths, which is why it's exponential.

# Space Complexity: O(n+m)
# For space, it's O(n+m) because that's the maximum depth of our recursion stack.
# In the worst case, we might go through all n characters in word and all m characters in abbr before hitting the base case. Each recursive call adds a frame to the stack, so the stack depth is at most n+m.
# We're not storing any additional data structures - just the call stack.

# Complete Recursion Trace
# Example: word = "helzzpme", abbr = "h2*p*me"

# Call 1: match(word, abbr, i=0, j=0)
# Current state:

# word[0] = 'h'
# abbr[0] = 'h'

# Processing:

# abbr[0] is a letter
# Check: word[0] == abbr[0]? → 'h' == 'h' ✓
# Recurse: match(word, abbr, i=1, j=1)


# Call 2: match(word, abbr, i=1, j=1)
# Current state:

# word[1] = 'e'
# abbr[1] = '2'

# Processing:

# abbr[1] is a digit ('2')
# Not a leading zero ✓
# Build number: skip_count = 2
# Move j forward: j becomes 2 (past the '2')
# Check: i + skip_count = 1 + 2 = 3 ≤ 8 ✓
# Recurse: match(word, abbr, i=3, j=2)
# This skips word[1]='e' and word[2]='l'


# Call 3: match(word, abbr, i=3, j=2)
# Current state:

# word[3] = 'z'
# abbr[2] = '*'

# Processing:

# abbr[2] is a wildcard *
# We have 2 options:

# Option A: Skip the wildcard (match 0 characters)

# Try: match(word, abbr, i=3, j=3)
# word[3]='z', abbr[3]='p'
# 'z' != 'p' ✗
# Returns False

# Option B: Consume a character (match 1+ characters)

# Try: match(word, abbr, i=4, j=2)
# This consumes word[3]='z', wildcard stays at j=2


# Call 4: match(word, abbr, i=4, j=2)
# Current state:

# word[4] = 'z'
# abbr[2] = '*' (same wildcard)

# Processing:

# abbr[2] is still the wildcard *
# We have 2 options again:

# Option A: Skip the wildcard

# Try: match(word, abbr, i=4, j=3)
# word[4]='z', abbr[3]='p'
# 'z' != 'p' ✗
# Returns False

# Option B: Consume another character

# Try: match(word, abbr, i=5, j=2)
# This consumes word[4]='z', wildcard stays at j=2


# Call 5: match(word, abbr, i=5, j=2)
# Current state:

# word[5] = 'p'
# abbr[2] = '*' (same wildcard)

# Processing:

# abbr[2] is still the wildcard *
# We have 2 options again:

# Option A: Skip the wildcard

# Try: match(word, abbr, i=5, j=3)
# word[5]='p', abbr[3]='p'
# 'p' == 'p' ✓
# Continue...


# Call 6: match(word, abbr, i=6, j=4)
# Current state:

# word[6] = 'm'
# abbr[4] = '*'

# Processing:

# abbr[4] is a wildcard *
# We have 2 options:

# Option A: Skip the wildcard

# Try: match(word, abbr, i=6, j=5)
# word[6]='m', abbr[5]='m'
# 'm' == 'm' ✓
# Continue...


# Call 7: match(word, abbr, i=7, j=6)
# Current state:

# word[7] = 'e'
# abbr[6] = 'e'

# Processing:

# abbr[6] is a letter
# Check: word[7] == abbr[6]? → 'e' == 'e' ✓
# Recurse: match(word, abbr, i=8, j=7)


# Call 8: match(word, abbr, i=8, j=7)
# Current state:

# i = 8 = len(word)
# j = 7 = len(abbr)

# Processing:

# Base case: Both exhausted! ✓
# Return True

# Previous Approach with nested function instead of 

# class Solution:
#     def wordPatternMatch(self, word: str, abbr: str) -> bool:
        
#         def match(i: int, j: int) -> bool:
#             # Base case: both strings fully consumed - valid match
#             if i == len(word) and j == len(abbr):
#                 return True
            
#             # Abbr exhausted but word has remaining characters - no match
#             if j == len(abbr):
#                 return False
            
#             # Word exhausted but abbr has remaining characters
#             if i == len(word):
#                 # Valid only if all remaining characters in abbr are wildcards
#                 # (wildcards can match empty sequence)
#                 j_temp = j
#                 while j_temp < len(abbr):
#                     if abbr[j_temp] != '*':
#                         return False
#                     j_temp += 1
#                 return True
            
#             # Case 1: Handle wildcard '*' - matches any sequence (0 or more chars)
#             if abbr[j] == '*':
#                 # Option A: Match 0 characters (skip the wildcard)
#                 if match(i, j + 1):
#                     return True
#                 # Option B: Match 1+ characters (consume from word, keep wildcard)
#                 if match(i + 1, j):
#                     return True
#                 # Both options failed
#                 return False
            
#             # Case 2: Handle digit - represents number of characters to skip
#             if abbr[j].isdigit():
#                 # Leading zeros are invalid
#                 if abbr[j] == '0':
#                     return False
                
#                 # Build the complete multi-digit number
#                 skip_count = 0
#                 j_temp = j
#                 while j_temp < len(abbr) and abbr[j_temp].isdigit():
#                     skip_count = skip_count * 10 + int(abbr[j_temp])
#                     j_temp += 1
                
#                 # Check if we can skip that many characters without exceeding word length
#                 if i + skip_count > len(word):
#                     return False
                
#                 # Recursively match after skipping
#                 return match(i + skip_count, j_temp)
            
#             # Case 3: Handle letter - must match exactly
#             if abbr[j].isalpha():
#                 # Characters must be identical
#                 if word[i] != abbr[j]:
#                     return False
#                 # Move both pointers forward
#                 return match(i + 1, j + 1)
            
#             # Invalid character in abbr
#             return False
        
#         # Start matching from the beginning
#         return match(0, 0)


# Optimized Approach : Recursion with memoization

# class Solution:
#     def wordPatternMatch(self, word: str, abbr: str) -> bool:
#         """
#         Validates if a word matches an abbreviation pattern with wildcards using memoization.
        
#         Time Complexity: O(n × m) where n = len(word), m = len(abbr)
#         - Each unique state (i, j) is computed at most once due to memoization
#         - Total possible states: (n+1) × (m+1) = O(n × m)
#         - Each state computation does O(1) work (excluding recursive calls)
        
#         Space Complexity: O(n × m)
#         - Memoization cache stores up to n × m states
#         - Recursion stack depth is O(n + m)
#         - Total space: O(n × m) + O(n + m) = O(n × m)
        
#         Args:
#             word: The original word to validate against
#             abbr: The abbreviation pattern with wildcards (*), numbers, and letters
            
#         Returns:
#             True if word matches the abbreviation pattern, False otherwise
#         """
#         # Memoization cache: maps (i, j) state to boolean result
#         memo = {}
#         return self.match(word, abbr, 0, 0, memo)
    
#     def match(self, word: str, abbr: str, i: int, j: int, memo: dict) -> bool:
#         """
#         Recursively match word and abbr starting from positions i and j with memoization.
        
#         Args:
#             word: The word to match
#             abbr: The abbreviation pattern
#             i: Current position in word (0 to len(word))
#             j: Current position in abbr (0 to len(abbr))
#             memo: Dictionary to cache results for (i, j) states
            
#         Returns:
#             True if remaining parts match, False otherwise
#         """
#         # Check if this state has already been computed
#         if (i, j) in memo:
#             return memo[(i, j)]
        
#         # Base case: both strings fully consumed - valid match
#         # Example: word="ab", abbr="ab" → both reach end together ✓
#         if i == len(word) and j == len(abbr):
#             return True
        
#         # Abbr exhausted but word has remaining characters - no match
#         # Example: word="abcde", abbr="ab" → abbr done but word has "cde" left ✗
#         if j == len(abbr):
#             memo[(i, j)] = False
#             return False
        
#         # Word exhausted but abbr has remaining characters
#         # Example: word="ab", abbr="ab***" or word="ab", abbr="ab**c"
#         if i == len(word):
#             # Valid only if all remaining characters in abbr are wildcards
#             # Wildcards can match empty sequence, so "ab" matches "ab***" ✓
#             # But "ab" does NOT match "ab**c" because we need 'c' ✗
#             j_temp = j
#             while j_temp < len(abbr):
#                 if abbr[j_temp] != '*':
#                     # Found a non-wildcard character, but word is exhausted
#                     # Example: abbr="ab**c" has 'c' at the end → cannot match
#                     memo[(i, j)] = False
#                     return False
#                 j_temp += 1
#             # All remaining characters are wildcards → they match empty sequence
#             # Example: abbr="ab***" has only wildcards left → valid match ✓
#             memo[(i, j)] = True
#             return True
        
#         # Case 1: Handle wildcard '*' - matches any sequence (0 or more chars)
#         # Example: word="helzzp", abbr="h2*p" where * needs to match "zz"
#         if abbr[j] == '*':
#             # Option A: Match 0 characters (skip the wildcard)
#             # Try to see if skipping this wildcard works
#             # Example: word="abc", abbr="*bc" → skip *, try matching "abc" with "bc"
#             if self.match(word, abbr, i, j + 1, memo):
#                 memo[(i, j)] = True
#                 return True
            
#             # Option B: Match 1+ characters (consume from word, keep wildcard)
#             # Wildcard stays at j while we advance i (consume characters)
#             # Example: word="helzzp", abbr="h2*p" → * consumes 'z', then another 'z'
#             if self.match(word, abbr, i + 1, j, memo):
#                 memo[(i, j)] = True
#                 return True
            
#             # Both options failed - no valid match found
#             memo[(i, j)] = False
#             return False
        
#         # Case 2: Handle digit - represents number of characters to skip
#         # Example: word="hello", abbr="h2lo" → '2' means skip 2 chars ('e' and 'l')
#         if abbr[j].isdigit():
#             # Leading zeros are invalid
#             # Example: abbr="h0llo" is invalid ✗
#             if abbr[j] == '0':
#                 memo[(i, j)] = False
#                 return False
            
#             # Build the complete multi-digit number
#             # Example: abbr="h12o" → skip_count=12 (not just 1 and 2 separately)
#             skip_count = 0
#             j_temp = j
#             while j_temp < len(abbr) and abbr[j_temp].isdigit():
#                 skip_count = skip_count * 10 + int(abbr[j_temp])
#                 j_temp += 1
            
#             # Check if we can skip that many characters without exceeding word length
#             # Example: word="hi", abbr="h5" → can't skip 5 chars from position 1 ✗
#             if i + skip_count > len(word):
#                 memo[(i, j)] = False
#                 return False
            
#             # Recursively match after skipping skip_count characters
#             # Example: word="hello", abbr="h2lo" → skip 2 chars, match from "llo" vs "lo"
#             result = self.match(word, abbr, i + skip_count, j_temp, memo)
#             memo[(i, j)] = result
#             return result
        
#         # Case 3: Handle letter - must match exactly
#         # Example: word="abc", abbr="abc" → each letter must match exactly
#         if abbr[j].isalpha():
#             # Characters must be identical
#             # Example: word="abc", abbr="axc" → 'b' != 'x' ✗
#             if word[i] != abbr[j]:
#                 memo[(i, j)] = False
#                 return False
            
#             # Move both pointers forward
#             # Example: word="abc", abbr="abc" → match 'a', continue with "bc" vs "bc"
#             result = self.match(word, abbr, i + 1, j + 1, memo)
#             memo[(i, j)] = result
#             return result
        
#         # Invalid character in abbr (shouldn't happen with valid input)
#         memo[(i, j)] = False
#         return False



        