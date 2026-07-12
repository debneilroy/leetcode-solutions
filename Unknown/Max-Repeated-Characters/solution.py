"""
7. Max Repeated Characters
Difficulty: Easy
Source: Unpublished / company interview problem (not indexed on LeetCode)
"""

class MaxConsecutiveChars:
    def find_max_consecutive(self, text):
        """
        Find the maximum length of consecutive identical characters (excluding
        whitespace) and return all characters that occur consecutively with
        this maximum length, in order of appearance.

        Time Complexity: O(n)
        - Single pass through the string
        - The inner while loop only advances i, so total iterations across
          both loops is bounded by n

        Space Complexity: O(k)
        - k = number of characters tied for the max run length
        - No auxiliary data structures beyond the result list

        Best case: O(1) when a single run is strictly longest (k = 1)
        Worst case: O(n) when every run has the same length, e.g. "ababab"
        (every character ties for the max, so k grows to n)
        """
        if not text:
            return []

        max_length = 0
        result = []
        i = 0
        while i < len(text):
            char = text[i]

            # Whitespace breaks a run and is never a candidate itself
            if char.isspace():
                i += 1
                continue

            # Extend the run while the next character matches
            length = 1
            while i + 1 < len(text) and text[i + 1] == char:
                length += 1
                i += 1

            # New max: reset result. Tie: append to result.
            if length > max_length:
                max_length = length
                result = [char]
            elif length == max_length:
                result.append(char)

            i += 1

        return result


# Variant 1 : Repeating Characters — instead of only the longest run(s),
# it returns every character that occurs as part of ANY consecutive run
# of length >= 2 (excluding whitespace), in order of appearance.

# Example 1:
# Input: text = "taadpoole teeechies eek"
# Output: ['a', 'o', 'e', 'e']
# Explanation:
# Consecutive sequences: "aa" (length 2), "oo" (length 2), "eee" (length 3), "ee" (length 2).

# Example 2:
# Input: text = "hello"
# Output: ['l']
# Explanation:
# Consecutive sequences: "ll" (length 2). No other characters repeat consecutively.

# def find_repeating_characters(text):
#     """
#     Find all characters that occur as part of a consecutive run of length
#     >= 2 (excluding whitespace), in order of appearance.
#
#     Time Complexity: O(n)
#     - Single pass through the string
#     - The inner while loop only advances i, so total iterations across
#       both loops is bounded by n
#
#     Space Complexity: O(k)
#     - k = number of qualifying runs (length >= 2)
#
#     Best case: O(1) when no character repeats consecutively
#     Worst case: O(n) when the whole string is one repeated character,
#     or alternates between two repeated-pair blocks, e.g. "aabbcc..."
#     """
#     result = []
#     i = 0
#     n = len(text)
#     while i < n:
#         char = text[i]
#
#         # Whitespace breaks a run and is never a candidate itself
#         if char.isspace():
#             i += 1
#             continue
#
#         # Extend the run while the next character matches
#         length = 1
#         while i + 1 < n and text[i + 1] == char:
#             length += 1
#             i += 1
#
#         # Any run of 2+ qualifies, unlike the main solution above, which
#         # only keeps the longest run(s)
#         if length > 1:
#             result.append(char)
#
#         i += 1
#
#     return result
