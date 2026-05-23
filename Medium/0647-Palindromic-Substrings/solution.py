"""
LeetCode 647. Palindromic Substrings
Difficulty: Medium
URL: https://leetcode.com/problems/palindromic-substrings/
"""

# Approach : Brute Force

# class Solution:
#     def countSubstrings(self, s: str) -> int:
#         """
#         Count palindromic substrings by checking every possible substring.
        
#         Approach: Brute Force
#         ---------------------
#         Generate all possible substrings and check if each is a palindrome.
        
#         For each starting position i:
#           For each ending position j >= i:
#             Check if s[i:j+1] is a palindrome
#             If yes, increment count
        
#         Time Complexity: O(n³)
#         ----------------------
#         - Outer loop (i): runs n times
#         - Inner loop (j): runs n times on average
#         - isPalindrome check: O(n) for each substring
#         - Total: n × n × n = O(n³)
        
#         Why O(n³)?
#           Step 1: Generate substrings → O(n²) pairs (i,j)
#           Step 2: Check each substring → O(n) per check
#           Total: O(n²) × O(n) = O(n³)
        
#         Space Complexity: O(1)
#         """
#         count = 0
        
#         # Outer loop: iterate through all possible starting positions
#         # Runs n times where n = len(s)
#         for i in range(len(s)):
            
#             # Inner loop: iterate through all possible ending positions
#             # For each start i, check all end positions j where j >= i
#             # This generates all n(n+1)/2 = O(n²) possible substrings
#             for j in range(i, len(s)):
                
#                 # Check if substring s[i:j+1] is a palindrome
#                 # isPalindrome takes O(j-i+1) = O(n) time in worst case
#                 if self.isPalindrome(s, i, j):
#                     count += 1
        
#         return count
    
#     def isPalindrome(self, s: str, l: int, r: int) -> bool:
#         """
#         Check if substring s[l:r+1] is a palindrome using two pointers.
        
#         Time Complexity: O(n) where n = r - l + 1 (length of substring)
#         -----------------------------------------------------------------
#         - While loop runs at most (r-l+1)/2 times
#         - Each iteration does O(1) work (character comparison)
#         - In worst case (palindrome), we check all characters
        
#         Space Complexity: O(1)
#         ----------------------
#         - Only using pointers l and r
#         - No additional memory allocation

#         """
#         # Two-pointer approach: move inward from both ends
#         # Continue while left pointer is before right pointer
#         while l < r:
#             # If characters don't match, it's not a palindrome
#             if s[l] != s[r]:
#                 return False
            
#             # Move pointers inward
#             l += 1  # Move left pointer right
#             r -= 1  # Move right pointer left
        
#         # If we've checked all pairs without finding mismatch,
#         # the substring is a palindrome
#         return True

        

# Approach : Expand around center
# TC : O(n^2), SC : O(1)

class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count all palindromic substrings in the given string.

        Approach: Expand Around Centers
        --------------------------------
        Key insight: Every palindrome has a center. We can find all palindromes
        by treating each position as a potential center and expanding outward.
        
        For each position i:
        1. Treat i as center of odd-length palindrome (e.g., "aba")
           - Start with left=i, right=i
           - Expand outward: left--, right++
           - Count each valid palindrome found
        
        2. Treat position between i and i+1 as center of even-length palindrome (e.g., "abba")
           - Start with left=i, right=i+1
           - Expand outward: left--, right++
           - Count each valid palindrome found
        
        Example: s = "aba"
          i=0: expand(0,0) finds "a"
          i=1: expand(1,1) finds "b", then "aba"
          i=2: expand(2,2) finds "a"
          Total: 4 palindromes
        
        Time Complexity: O(n²) where n is the length of string
        - Outer loop iterates n times (each index as potential center)
        - Each expand_around_center call takes O(n) in worst case
        - Worst case: strings with all identical characters like "aaaa"
          where every expansion succeeds and extends to string boundaries
        - Total: n centers × n expansions per center = O(n²)
        
        Space Complexity: O(1)
        - Only using fixed number of variables (total, left, right, count)
        - No data structures that grow with input size
        - No recursion stack (iterative solution)
        - Variables remain constant regardless of input size
        
        Args:
            s: Input string
            
        Returns:
            Total count of palindromic substrings
        """
        
        def expand_around_center(left: int, right: int) -> int:
            """
            Expand outward from center and count palindromes.
            
            Time Complexity: O(n) worst case
            - While loop continues while characters match and within bounds
            - Worst case: all characters are same (e.g., "aaaa")
              where we expand from center to both ends of string
            - If expanding from middle of length-n string, we do n/2 expansions
            - Therefore O(n) in worst case
            
            Space Complexity: O(1)
            - Only uses count, left, right variables
            - No additional memory allocation based on input
            
            Args:
                left: Left pointer starting position
                right: Right pointer starting position
                
            Returns:
                Number of palindromes found during expansion
            """
            count = 0
            
            # Expand while within bounds and characters match
            while left >= 0 and right < len(s) and s[left] == s[right]:
                # Found a palindrome from s[left:right+1]
                count += 1
                
                # Expand outward for next iteration
                left -= 1
                right += 1
            
            return count
        
        total = 0
        
        # Consider each position as a potential palindrome center
        # Time: O(n) iterations
        for i in range(len(s)):
            # Case 1: Odd-length palindromes (single character as center)
            # Examples: "a", "aba", "racecar"
            total += expand_around_center(i, i)
            
            # Case 2: Even-length palindromes (center between two characters)
            # Examples: "aa", "abba", "aabbaa"
            total += expand_around_center(i, i + 1)
        
        return total


# Variant: Return all the palindromic substrings

# class Solution:
#     def allPalindromicSubstrings(self, s: str) -> list[str]:
#         """
        
#         Time Complexity: O(n³)
        
#         Phase 1 - Finding palindrome indices: O(n²)
#           • We check n positions as potential centers
#           • From each center, we expand up to n/2 times (worst case)
#           • Each expansion just appends indices: O(1) operation
#           • Total: n centers × n expansions × O(1) = O(n²)
        
#         Phase 2 - Converting indices to strings: O(n³) 
#           • We have O(n²) palindromes in worst case
#             Example: "aaaa" has 10 palindromes
#             Formula: approximately n(n+1)/2 = O(n²)
#           • Iterating through indices: O(n²) iterations
#           • Each s[l:r+1] slice COPIES characters: O(r-l+1) time
#           • Total characters copied across all palindromes: O(n³)
#             Example: "aaaa" copies 1+2+1+3+2+4+1+3+2+1 = 20 chars
#             Formula: n(n+1)(n+2)/6 = O(n³)
#           • Total: O(n²) iterations × O(average length) = O(n³)
        
#         Overall: O(n²) + O(n³) = O(n³)
        
#         Space Complexity: O(n²)
#           • indices list: O(n²) tuples
#           • palindromes result: O(n²) strings
#           • Note: Total characters in result is O(n³), but we count
#             number of objects (n²), not total character storage
        
#         Why two phases?
#           • Storing indices is O(1) per palindrome
#           • Creating strings is O(length) per palindrome
#           • Separating phases keeps finding step efficient: O(n²)
        
#         Examples:
#           "abc" → ['a', 'b', 'c'] (3 palindromes)
#           "aaa" → ['a', 'aa', 'aaa', 'a', 'aa', 'a'] (6 palindromes)
#           "aba" → ['a', 'b', 'aba', 'a'] (4 palindromes)
        
#         Args:
#             s: Input string to find palindromes in
            
#         Returns:
#             List of all palindromic substrings (duplicates included)
#         """
#         n = len(s)
        
#         # Store (left, right) indices of all palindromes
#         # This list will have O(n²) elements in worst case
#         indices: list[tuple[int, int]] = []
        
#         def expand_from_center(left: int, right: int):
#             """
#             Expand outward from center while characters match.
#             Stores (left, right) indices for each palindrome found.
            
#             Time: O(n) in worst case (expand to string boundaries)
#             Space: O(n) in worst case (store n palindrome indices)
            
#             Example for "aba" with center at index 1:
#               Step 1: left=1, right=1 → s[1]='b' matches → store (1,1) → "b"
#               Step 2: left=0, right=2 → s[0]='a'==s[2]='a' → store (0,2) → "aba"
#               Step 3: left=-1 (out of bounds) → stop
#             """
#             while left >= 0 and right < n and s[left] == s[right]:
#                 indices.append((left, right))
#                 left -= 1  
#                 right += 1  
        
#         # PHASE 1: Find all palindrome indices - O(n²) time
#         # ================================================
        
#         # Check every position as a potential palindrome center
#         # This loop runs n times
#         for i in range(n):
#             expand_from_center(i, i)
#             expand_from_center(i, i + 1)
        
#         # At this point:
#         # - indices has O(n²) elements
#         # - Each element is a tuple (left, right)
#         # - We spent O(n²) time finding them
        
#         # PHASE 2: Convert indices to actual strings - O(n³) time
#         # =========================================================
        
#         # This list comprehension does TWO things:
#         # 1. Iterates through ALL indices: O(n²) iterations
#         # 2. For each index pair, slices string: O(r-l+1) per slice
#         #
#         # Key insight: Total characters copied = O(n³)
#         # Example "aaaa": copies 1+2+1+3+2+4+1+3+2+1 = 20 = O(n³)
#         #
#         # Why O(n³) and not O(n²)?
#         # - We have O(n²) palindromes
#         # - BUT they're not all length 1!
#         # - Palindromes near the middle are long (up to length n)
#         # - Total length summed = n(n+1)(n+2)/6 = O(n³)
        
#         palindromes = []
        
#         for l, r in indices:
#             palindromes.append(s[l:r+1])

#         return palindromes

# 1. How many palindromic substrings exist?

# A string of length n can have at most n(n+1) / 2 ~ O(n^2) distinct palindromic occurrences (with duplicates).

# What is the maximum number of palindromic substrings?

# Consider the worst-case string:
# s = "aaaaa"
# Every substring is a palindrome.
# Let n = len(s).

# Length 1 palindromes: n
# Length 2 palindromes: n - 1
# Length 3 palindromes: n - 2
# ...
# Length n palindromes: 1

# Total palindromes:
# n + (n-1) + (n-2) + ⋯ + 1 = n(n+1)/2
# That is Θ(n²).

# What does that mean for indices?

# Each palindrome → one (l, r) tuple
# Each tuple is constant size
# Number of tuples = Θ(n²)

# Therefore:
# Space for indices = Θ(n²)

# Concrete example
# For "aaa" (n = 3):
# Palindromes found:
# (0,0) -> "a"
# (0,1) -> "aa"
# (0,2) -> "aaa"
# (1,1) -> "a"
# (1,2) -> "aa"
# (2,2) -> "a"
# Number of entries in indices = 6
# And:
# 3 · 4 / 2 = 6
# Matches exactly.


# 3. Space for palindromes list

# Each pair generates a substring s[l:r+1].

# Number of substrings = O(n²)

# Each substring has average length O(n/2) in worst case (like "aaaaa")

# So total characters stored across all substrings = O(n³)

# ✅ Output space = O(n³) in worst case.

# 📊 Summary Table
# Component	Count	Size	Space
# indices list	O(n²)	O(1) each	O(n²)
# palindromes list	O(n²)	up to O(n) each	O(n³) total chars
# Auxiliary vars	—	—	O(1)
# ✅ Final Answer

# Auxiliary space (working memory): O(n²) ← from indices

# Total space (including output): O(n³) worst-case

# If interviewer says “space complexity” usually they exclude output, so:

# Space = O(n²) (auxiliary)

# If they include what’s returned, then:

# Space = O(n³) (output substrings)

