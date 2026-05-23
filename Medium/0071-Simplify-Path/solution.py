"""
LeetCode 71. Simplify Path
Difficulty: Medium
URL: https://leetcode.com/problems/simplify-path/
"""

# Brute Force — O(N²) TC, O(N) SC

# Repeatedly apply string rewrites until the path stops changing

# // → / (collapse duplicate slashes)

# /./ → / (current directory)

# /dir/../ → / (remove parent directory pairs)

# Each rewrite pass scans the string → O(N)

# In worst case only one dir/.. pair is removed per pass

# Up to O(N) passes → O(N²) total

# O(N) SC — each rewrite creates a new string copy

# Hard to implement cleanly due to overlapping patterns



# Optimal Approach : Using stacks

# Testcase : path = "/a/b/c/.././././//d"   Output : "/a/b/d"

class Solution:
    def simplifyPath(self, path: str) -> str:
        """
        Simplify a Unix-style absolute path to its canonical form.

        Approach: Split on '/' and use a stack to process components.
        - Skip '' and '.' (no-ops)
        - '..' pops the stack (go up one level)
        - Any other token is a valid directory name → push

        Base cases:
        - path is None or empty string  → return "/"
        - path = "/"  → len 1, returned directly
        - path = "."  → len 1, not '/' → return "/"
        - path = "/." → '.' skipped → stack = [] → return "/"
        - path = "/.."→ '..' on empty stack → stack = [] → return "/"
        - path = "/a" → one valid component → stack = ['a'] → return "/a"

        TC: O(N), where N = len(path)
            - .split('/')      : O(N)
            - loop over tokens : each token processed once → O(N)
            - '/'.join(stack)  : worst case join all tokens → O(N)

        SC: O(N) → effectively O(2N)
            - parts (split result) : O(N)
            - stack                : O(N) in worst case (no '..' or '.')
            - simplifies to O(N) after dropping constant
        """
        # Guard: None, empty string
        if not path:
            return "/"

        # Guard: single character — only '/' is valid canonical; anything else (e.g. '.') → root
        if len(path) == 1:
            return path if path == '/' else '/'

        parts = path.split('/')

        stack = []

        for part in parts:
            if part == '' or part == '.':
                continue
            elif part == '..':
                if stack:
                    stack.pop()
            else:
                stack.append(part)

        return '/' + '/'.join(stack)

        # Manually build the simplified path string
        # result = '/'
        # for j in range(len(stack)):
        #     result += stack[j]
        #     if j != len(stack) - 1:
        #         result += '/'

        # return result

# Without split function

class Solution:
    def simplifyPath(self, path: str) -> str:
        """
        TC: O(N), where N = len(path)
            - single pass through path with pointer i    : O(N)
            - token extraction (inner while)             : each char visited once → O(N)
            - '/'.join(stack)                            : worst case join all tokens → O(N)

        SC: O(N)
            - stack : O(N) in worst case (no '..' or '.')
            - no parts array unlike the split() approach → true O(N), not O(2N)
        """
        # Guard: None, empty string
        if not path:
            return "/"

        # Guard: single character — only '/' is valid canonical; anything else (e.g. '.') → root
        if len(path) == 1:
            return path if path == '/' else '/'

        stack = []
        i = 0
        n = len(path) # n = 19 for path = "/a/b/c/.././././//d"

        while i < n:
            # Skip over consecutive '/' characters (e.g. '///a' → jump to 'a')
            while i < n and path[i] == '/':
                i += 1

            # Extract the next token character by character until next '/' or end
            # e.g. path = "/abc/../d" → tokens extracted in order: "abc", "..", "d"
            token = ""
            while i < n and path[i] != '/':
                token += path[i]
                i += 1

            if token == '' or token == '.':
                continue
            elif token == '..':
                if stack:
                    stack.pop()
            else:
                stack.append(token)

        # Reconstruct canonical path with a leading '/'
        return "/" + "/".join(stack)


# Variant

# Description
# You are given:

# A string cwd representing the current working directory in a Unix-style file system.

# A string cd representing a relative or absolute path to change into, using Unix shell conventions.

# Write a function changeDirectory(cwd: str, cd: str) -> str that returns the resulting absolute path after applying the cd command to cwd.

# Example 1:
# Input : cwd = "/a/b/c", cd = "../d"
# Output: "/a/b/d"
# Description: cd is relative, so we resolve from cwd.
#              ".." moves up one level from "/a/b/c" → "/a/b",
#              then "d" moves into "/a/b/d".

# Example 2:
# Input : cwd = "/x/y", cd = "/foo/bar/../baz"
# Output: "/foo/baz"
# Description: cd starts with '/', so it is absolute — cwd is ignored entirely.
#              Simplify "/foo/bar/../baz": "bar" is pushed then popped by "..",
#              leaving "/foo/baz".

# Example 3:
# Input : cwd = "/", cd = "../../../../."
# Output: "/"
# Description: cd is relative, so we resolve from cwd = "/".
#              Each ".." attempts to go up from root, but root has no parent —
#              all four ".." are silently ignored.
#              Final "." is a no-op. Result stays "/".

# Example 4:
# Input : cwd = "/a/b/c", cd = "."
# Output: "/a/b/c"
# Description: cd is relative and a single ".'" — current directory, no-op.
#              cwd is returned unchanged.

# Example 5:
# Input : cwd = "/home/user/docs", cd = "../../music/jazz"
# Output: "/home/music/jazz"
# Description: cd is relative, so we resolve from cwd.
#              First ".."  : "/home/user/docs" → "/home/user"
#              Second "..": "/home/user"       → "/home"
#              Then "music/jazz" is appended   → "/home/music/jazz"


# class Solution:
#     def changeDirectory(self, cwd: str, cd: str) -> str:
#         """
#         Apply a Unix cd command to a current working directory.

#         Approach:
#         - If cd is absolute (starts with '/'), ignore cwd entirely
#         - Otherwise, seed the stack with cwd components, then process cd on top
#         - '..' pops the stack (go up), '.' and '' are no-ops, else push

#         Base / edge cases:
#         - cd is None or empty          → return cwd if valid, else '/'
#         - cwd is None                  → treat as root '/'
#         - cd = "."                     → no-op token, cwd processed through stack
#         - cd = "/"                     → absolute, cwd zeroed, stack stays empty → "/"
#         - cd = "../../../.." from "/"  → all ".." ignored at root, return "/"
#         - cd is absolute               → cwd ignored, simplify cd alone

#         TC: O(N + M), where N = len(cwd), M = len(cd)
#             - split + iterate cwd tokens : O(N)
#             - split + iterate cd tokens  : O(M)
#             - '/'.join(tokens)           : O(N + M) worst case

#         SC: O(N + M)
#             - tokens stack holds at most all components of cwd + cd
#         """

#         # Guard: None or empty cd → no directory change
#         #
#         # Scenario 1 — cwd is always simplified (e.g. result of a previous
#         # changeDirectory call): safe to return cwd directly.
#         # Also guard cwd being None/empty → fallback to root '/'
#         #   if not cd:
#         #       return cwd if cwd else '/'
#         #
#         # Scenario 2 — cwd could be unsimplified (e.g. "/a//b/"):
#         # change cd to '.' so cwd still gets processed through the stack
#         # '.' is a no-op token so it won't affect the final result
#         #   if not cd:
#         #       cd = '.'

#         if not cd:
#             cd = '.'  # assuming cwd may be unsimplified

#         # Guard: None cwd → treat as root (empty string is safe, None is not)
#         # Can't early return '/' here — cd may have content that still needs
#         # to be processed e.g. cwd=None, cd="foo/bar" → should return "/foo/bar"
#         if cwd is None:
#             cwd = '/'

#         # If cd is absolute, ignore cwd entirely — can't return cd as-is since
#         # it may need simplification e.g. "/foo/bar/../baz" → "/foo/baz"
#         if cd[0] == '/':
#             cwd = ''

#         tokens = []

#         # Step 1: seed stack with cwd components
#         for token in cwd.split('/'):
#             if token:  # skip empty strings from leading/multiple slashes
#                 tokens.append(token)

#         # Step 2: process cd on top of the seeded stack
#         for token in cd.split('/'):
#             if token == '' or token == '.':
#                 # empty string (consecutive slashes) or '.' (current dir) → no-op
#                 continue
#             elif token == '..':
#                 # go one level up — silently ignore if already at root
#                 if tokens:
#                     tokens.pop()
#             else:
#                 # valid directory name → descend into it
#                 tokens.append(token)

#         # Step 3: reconstruct absolute path; empty stack means we're at root
#         return '/' + '/'.join(tokens) if tokens else '/'
