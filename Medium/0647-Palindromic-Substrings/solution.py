"""
LeetCode 647. Palindromic Substrings
Difficulty: Medium
URL: https://leetcode.com/problems/palindromic-substrings/
"""

# Approach : Brute Force

class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count palindromic substrings by checking every possible substring.
        
        Approach: Brute Force
        ---------------------
        Generate all possible substrings and check if each is a palindrome.
        
        For each starting position i:
          For each ending position j >= i:
            Check if s[i:j+1] is a palindrome
            If yes, increment count
        
        Time Complexity: O(n³)
        ----------------------
        - Outer loop (i): runs n times
        - Inner loop (j): runs n times on average
        - isPalindrome check: O(n) for each substring
        - Total: n × n × n = O(n³)
        
        Why O(n³)?
          Step 1: Generate substrings → O(n²) pairs (i,j)
          Step 2: Check each substring → O(n) per check
          Total: O(n²) × O(n) = O(n³)
        
        Space Complexity: O(1)
        """
        count = 0
        
        # Outer loop: iterate through all possible starting positions
        # Runs n times where n = len(s)
        for i in range(len(s)):
            
            # Inner loop: iterate through all possible ending positions
            # For each start i, check all end positions j where j >= i
            # This generates all n(n+1)/2 = O(n²) possible substrings
            for j in range(i, len(s)):
                
                # Check if substring s[i:j+1] is a palindrome
                # isPalindrome takes O(j-i+1) = O(n) time in worst case
                if self.isPalindrome(s, i, j):
                    count += 1
        
        return count
    
    def isPalindrome(self, s: str, l: int, r: int) -> bool:
        """
        Check if substring s[l:r+1] is a palindrome using two pointers.
        
        Time Complexity: O(n) where n = r - l + 1 (length of substring)
        -----------------------------------------------------------------
        - While loop runs at most (r-l+1)/2 times
        - Each iteration does O(1) work (character comparison)
        - In worst case (palindrome), we check all characters
        
        Space Complexity: O(1)
        ----------------------
        - Only using pointers l and r
        - No additional memory allocation

        """
        # Two-pointer approach: move inward from both ends
        # Continue while left pointer is before right pointer
        while l < r:
            # If characters don't match, it's not a palindrome
            if s[l] != s[r]:
                return False
            
            # Move pointers inward
            l += 1  # Move left pointer right
            r -= 1  # Move right pointer left
        
        # If we've checked all pairs without finding mismatch,
        # the substring is a palindrome
        return True

# Approach : Expand around center

class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count all palindromic substrings in the given string.

        Approach: Expand Around Centers
        --------------------------------
        Key insight: Every palindrome has a center. We can find all palindromes
        by treating each position as a potential center and expanding outward.
        
        Diagram for s = "aba" (odd-length center at index 1):

        index:     0   1   2
        char:      a   b   a
                       ^
                  center (i=1)

        Step 0 (no expansion):  l=1, r=1 -> "b"          (palindrome found)
        Step 1 (expand once):   l=0, r=2 -> "a b a"      (palindrome found)
                                 ^_______________^
                                s[0]=='a' == s[2]=='a'  -> match, keep expanding
        Step 2 (expand again):  l=-1 -> out of bounds, STOP

        Diagram for s = "abba" (even-length center between index 1 and 2):

        index:     0   1   2   3
        char:      a   b   b   a
                       ^   ^
                       l=1  r=2  (center sits BETWEEN these two indices)

        Step 0 (no expansion):  l=1, r=2 -> "b b"        (s[1]==s[2], palindrome found)
        Step 1 (expand once):   l=0, r=3 -> "a b b a"    (s[0]==s[3], palindrome found)
                                       
        Step 2 (expand again):  l=-1 -> out of bounds, STOP

        General picture — two pointers walking outward in lockstep from a center:

        l <--  [center]  --> r
        <---- expand ---->
        ...x x [ c ] x x...        (odd center: single character)
        ...x x [c | c] x x...      (even center: gap between two characters)

        Every time s[l] == s[r], the substring s[l:r+1] is a palindrome,
        and we keep pushing l left / r right until either the characters
        stop matching or we fall off the edge of the string.

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

#             Worked example: s = "aaaa" (n=4)
#             i=0: expand(0,0) → 1 step,  expand(0,1) → 1 step   (2 steps)
#             i=1: expand(1,1) → 2 steps, expand(1,2) → 2 steps  (4 steps)
#             i=2: expand(2,2) → 2 steps, expand(2,3) → 1 step   (3 steps)
#             i=3: expand(3,3) → 1 step,  expand(3,4) → 0 steps  (1 step)
#             Total expansion steps = 2+4+3+1 = 10 = n(n+1)/2 = O(n²) ✓
#             (Each step is O(1) work: one comparison + one append)
        
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

#             Worked example: s = "aaaa" (n=4), 10 index pairs from Phase 1
        
#             (l,r)   slice s[l:r+1]   copy cost (r-l+1)
#             -----   --------------   ------------------
#             (0,0)   "a"              1
#             (0,1)   "aa"             2
#             (1,1)   "a"              1
#             (0,2)   "aaa"            3
#             (1,2)   "aa"             2
#             (0,3)   "aaaa"           4
#             (2,2)   "a"              1
#             (1,3)   "aaa"            3
#             (2,3)   "aa"             2
#             (3,3)   "a"              1
#             -----------------------------------
#             10 iterations, but total copy cost = 1+2+1+3+2+4+1+3+2+1 = 20
        
#             If each slice were truly O(1), 10 iterations → O(n²) total.
#             But cost scales with each palindrome's length, so the real
#             total is 20, matching n(n+1)(n+2)/6 = 4·5·6/6 = 20 — that
#             extra factor of n is exactly what pushes O(n²) → O(n³).
        
#         Overall: O(n²) + O(n³) = O(n³)
        
#         Space Complexity: O(n³)
        
#           The honest accounting: every character we copy in Phase 2 has to
#           live somewhere. Since Phase 2 copies Θ(n³) total characters
#           (same n(n+1)(n+2)/6 quantity as the time analysis — copying a
#           character costs time AND occupies space), the actual memory
#           footprint for string content is Θ(n³).
        
#           Breakdown:
#           • indices list: O(n²) tuples
#             - Θ(n²) palindromes in worst case, each tuple O(1) space
#             - This part really is O(n²) — tuples don't scale with length
          
#           • palindromes result: O(n³) total characters
#             - Θ(n²) string objects, BUT they are not all length 1
#             - Their lengths sum to n(n+1)(n+2)/6 = Θ(n³)
#             - This total is both the TIME to copy each character AND the
#               SPACE each copied character occupies once stored
        
#           Total Space: O(n²) [indices] + O(n³) [string content] = O(n³)
        
#           Worked example: s = "aaaa" (n=4)
#             indices = [(0,0),(0,1),(1,1),(0,2),(1,2),(0,3),
#                        (2,2),(1,3),(2,3),(3,3)]      → 10 tuples = O(n²) ✓
        
#             palindromes = ["a","aa","a","aaa","aa","aaaa",
#                            "a","aaa","aa","a"]         → 10 string objects
        
#             Object-count view:  len(palindromes) = 10 = O(n²)
#             Actual memory view: sum of lengths
#               = 1+2+1+3+2+4+1+3+2+1 = 20 characters = O(n³)
#                                                         ^^^^^^^^^^^^^^^^^
#             Check against formula: n(n+1)(n+2)/6 = 4·5·6/6 = 20 ✓
        
#             10 objects (O(n²)) vs 20 characters stored (O(n³)) — the gap
#             between these two numbers is exactly what the convention note
#             below is about, and it only widens as n grows (e.g. n=100
#             gives 4,950 objects but 171,700 characters).
        
#           Note on the O(n²) convention:
#             Some sources report O(n²) for this problem by counting the
#             NUMBER of string objects rather than their total character
#             content — analogous to calling an array of n integers "O(n)
#             space" while ignoring that each integer takes more than O(1)
#             bits to represent. That convention is defensible for fixed-size
#             elements, but here the elements have variable, length-dependent
#             size, so collapsing to "number of objects" hides a real cubic
#             memory cost. The more rigorous and interview-safe answer is
#             O(n³), since that reflects what's actually allocated.
        
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
#         # Space: O(n²) tuples × O(1) per tuple = O(n²)
#         indices: list[tuple[int, int]] = []
        
#         def expand_from_center(left: int, right: int):
#             """
#             Expand outward from center while characters match.
#             Stores (left, right) indices for each palindrome found.
            
#             Time: O(n) in worst case (expand to string boundaries)

#             Auxiliary Space: O(1)
#             (The palindrome indices are stored in the shared
#             'indices' list, whose total size is O(n²) tuples.
#             That O(n²) is just one part of the overall solution's
#             space — once Phase 2 materializes the actual strings,
#             the total space for the whole solution is O(n³).)
            
#             Example for "aba" with center at index 1:
#               Step 1: left=1, right=1 → s[1]='b' matches → store (1,1) → "b"
#               Step 2: left=0, right=2 → s[0]='a'==s[2]='a' → store (0,2) → "aba"
#               Step 3: left=-1 (out of bounds) → stop
#             """
#             while left >= 0 and right < n and s[left] == s[right]:
#                 indices.append((left, right))  
#                 left -= 1  
#                 right += 1  
        
#         # PHASE 1: Find all palindrome indices - O(n²) time, O(n²) space
#         # ================================================================
        
#         # Check every position as a potential palindrome center
#         # This loop runs n times
#         for i in range(n):
#             expand_from_center(i, i)
#             expand_from_center(i, i + 1)
        
#         # At this point:
#         # - indices has O(n²) elements
#         # - Each element is a tuple (left, right)
#         # - We spent O(n²) time finding them, O(n²) space storing them
        
#         # PHASE 2: Convert indices to actual strings - O(n³) time, O(n³) space
#         # ======================================================================
        
#         # This list comprehension does TWO things:
#         # 1. Iterates through ALL indices: O(n²) iterations
#         # 2. For each index pair, slices string: O(r-l+1) per slice
#         #
#         # Key insight: Total characters copied AND stored = O(n³)
#         # Example "aaaa": copies/stores 1+2+1+3+2+4+1+3+2+1 = 20 = O(n³)
#         #
#         # Why O(n³) and not O(n²)?
#         # - We have O(n²) palindromes
#         # - BUT they're not all length 1!
#         # - Palindromes near the middle are long (up to length n)
#         # - Total length summed = n(n+1)(n+2)/6 = O(n³)
#         # - This total is both the TIME to copy each character AND the
#         #   SPACE each copied character occupies once stored
        
#         palindromes = []
        
#         for l, r in indices:
#             palindromes.append(s[l:r+1])

#         return palindromes


# Print the palindromes

# class Solution:
#     def printPalindromicSubstrings(self, s: str) -> None:
#         """
#         Print every palindromic substring of s (duplicates included).

#         Approach: Expand Around Centers, in two separate phases
#         ---------------------------------------------------------
#         Phase 1: Find all palindromes by expanding around each of the n
#                  centers (odd + even), storing only their (left, right)
#                  indices — no string is created yet.
#         Phase 2: Walk through the stored indices and print each substring.

#         Time Complexity: O(n³)
#         -----------------------
#         Phase 1 - Finding indices: O(n²)
#           • n centers, each expands up to O(n) times in the worst case
#           • Each step is O(1): just a comparison + tuple append
#           • Total: n × O(n) = O(n²)

#         Phase 2 - Printing substrings: O(n³)
#           • indices has Θ(n²) entries in the worst case (e.g. "aaaa" → 10)
#           • Each s[l:r+1] slice COPIES (r-l+1) characters before printing
#           • That per-slice cost is NOT O(1) — it scales with palindrome length
#           • Total characters copied across all palindromes = Θ(n³)
#             Example "aaaa": 1+2+1+3+2+4+1+3+2+1 = 20 = n(n+1)(n+2)/6

#         Overall: O(n²) + O(n³) = O(n³)
#           Printing the indices alone would be O(n²), but printing the
#           actual substring text requires materializing it via slicing,
#           which is what pushes the total to O(n³).

#         Space Complexity: O(n²) auxiliary
#         -----------------------------------
#           • indices: Θ(n²) tuples, each O(1) → O(n²)
#           • No list of palindrome strings is ever built — each substring
#             is sliced, printed, and discarded immediately, so there's no
#             O(n³) string-storage cost like in allPalindromicSubstrings
#           • Each iteration creates a temporary substring of length O(n)
#             which is immediately printed and becomes eligible for garbage
#             collection. Although Θ(n³) total characters are created over
#             the entire execution, only O(n) characters exist at once, so
#             they do not contribute Θ(n³) auxiliary space.

#         Examples:
#           "aba" → prints: a, b, aba, a
#           "aaa" → prints: a, aa, aaa, a, aa, a

#         Args:
#             s: Input string

#         Returns:
#             None (prints directly, does not return the palindromes)
#         """
#         n = len(s)
#         indices: list[tuple[int, int]] = []

#         def expand_from_center(left: int, right: int) -> None:
#             """
#             Expand outward from center, storing indices only (no slicing).
#             Time: O(n) worst case. Auxiliary space: O(1) (mutates shared
#             `indices` list via closure; its total Θ(n²) size is accounted
#             for in the outer function's space analysis).
#             """
#             while left >= 0 and right < n and s[left] == s[right]:
#                 indices.append((left, right))
#                 left -= 1
#                 right += 1

#         # Phase 1: O(n²) — find all palindrome indices, no strings yet
#         for i in range(n):
#             expand_from_center(i, i)       # odd-length centers
#             expand_from_center(i, i + 1)   # even-length centers

#         # Phase 2: O(n³) — slicing here is what dominates total time
#         for l, r in indices:
#             print(s[l:r + 1])

