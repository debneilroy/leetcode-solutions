"""
LeetCode 236. Lowest Common Ancestor of a Binary Tree
Difficulty: Medium
URL: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
"""

# Definition for a binary tree node.

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# Approach : Recursion (postorder travel left -> right -> root)

class Solution:
     def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
            """ 
            Recursive DFS approach - MOST OPTIMAL for single LCA query.
            
            Algorithm:
            - If current node is None or matches p or q, return current node
            - Recursively search left and right subtrees
            - If both subtrees return non-null, current node is LCA
            - Otherwise, return whichever subtree found a match
            
            Time Complexity: O(n)
                - Visit each node at most once
                - Worst case visits all n nodes (when p and q are in different subtrees and are leaves):

                    e.g.    1
                           / \
                          2   3
                         /     \
                        4       5
                    p = 4, q = 5 -> LCA = 1
                    All 5 nodes are visited before returning.
                - Local pruning: if p is an ancestor of q (or vice versa),
                  recursion stops exploring below that node (its descendants),
                  but ancestor calls may still explore sibling subtrees.
            
            Space Complexity: O(h)
                - Recursion stack depth bounded by tree height h
                Best case (balanced): O(log n)
                    e.g.        3
                              /   \
                             5     1
                            / \   / \
                           6   2 0   8
                    p = 6, q = 8 -> LCA = 3
                    Stack depth example:
                    - Deepest path: LCA(3) -> LCA(5) -> LCA(6), depth = 3 ≈ log n
                    - Right subtree is also explored, but does not increase max depth
                Worst case (degenerate / skewed): O(n)
                    e.g.  1
                           \
                            2
                             \
                              3
                               \
                                4
                                 \
                                  5
                    p = 4, q = 5 -> LCA = 4
                    Stack: LCA(1) -> LCA(2) -> LCA(3) -> LCA(4), depth = 4
                    Depth grows linearly with n (here 4 for n=5). O(h) = O(n)
            """
            # Base case: if the current node is None or matches one of the target nodes, return it
            if root is None or root == p or root == q:
                return root

            # Recursively find p and q in the left and right subtrees
            l = self.lowestCommonAncestor(root.left, p, q)  # Traverse left
            r = self.lowestCommonAncestor(root.right, p, q) # Traverse right

            # Process current node (after visiting children)
            if l and r:
                # If both sides return non-null, this node is the LCA
                return root
            else:
                # Otherwise, return the non-null side (or None if both are null)
                return l if l else r # can also return l or r

# Example

# Build the tree:
#     1
#    / \
#   2   3
#  /     \
# 4       5

# root = TreeNode(1)
# root.left = TreeNode(2)
# root.right = TreeNode(3)
# root.left.left = TreeNode(4)
# root.right.right = TreeNode(5)

# # Grab references to the target nodes directly from the tree
# p = root.left.left    # node with val = 4
# q = root.right.right  # node with val = 5

# sol = Solution()
# res = sol.lowestCommonAncestor(root, p, q)
# print(res.val)  # 1
      
# Approach : Iterative using parent pointers (can be asked as follow up)

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """
        Find the Lowest Common Ancestor using parent pointers approach.
        
        Algorithm:
        1. Build a parent pointer map for all nodes (or until p and q are found)
        2. Collect all ancestors of p in a set
        3. Traverse ancestors of q until we find one that's also an ancestor of p
        
        Time Complexity: O(n)
            - Building parent map: O(n) in worst case when p and q are last nodes visited
            - Collecting p's ancestors: O(h) where h is height of tree
            - Finding common ancestor: O(h)
            - Overall: O(n) + O(h) + O(h) = O(n)
        
        Space Complexity: O(n)
            - Parent map: O(n) to store parent pointer for each node
            - Ancestors set: O(h) for p's ancestor chain
            - Stack for traversal: O(n) in worst case for iterative DFS
            - Overall: O(n) due to parent map
            
        Note: This approach uses MORE space than recursive DFS O(h) but can be
        beneficial if we need to answer multiple LCA queries on the same tree.

        Multi-query advantage:
            - For a single LCA query, recursive DFS wins on space: O(h) vs O(n).
            - For k queries on the SAME tree, the parent map can be built once
              and reused across all queries:
                - Recursive: O(k * n) total — each query re-traverses the tree.
                - Iterative (reusing map): O(n + k * h) total — build once, then
                  each query is just two upward walks of O(h).
            - Example: tree with 1M nodes (balanced, h ~ 20), k = 1000 queries:
                - Recursive: ~10^9 operations
                - Iterative (reused): ~1.02 * 10^6 operations (~1000x faster)
            - To enable reuse, lift `parent` out of the method and build it once
              in the constructor of a wrapper class.

              class TreeWithLCA:
                def __init__(self, root):
                    self.root = root
                    self.parent = {root: None}
                    # Build parent map once, for the whole tree
                    stack = [root]
                    while stack:
                        node = stack.pop()
                        if node.left:
                            self.parent[node.left] = node
                            stack.append(node.left)
                        if node.right:
                            self.parent[node.right] = node
                            stack.append(node.right)
                
                def lca(self, p, q):
                    # O(h) per query — just the two walks, no re-traversal
                    ancestors = set()
                    cur = p
                    while cur:
                        ancestors.add(cur)
                        cur = self.parent[cur]
                    cur = q
                    while cur not in ancestors:
                        cur = self.parent[cur]
                    return cur

        Trade-offs vs. recursive DFS:
        - Time: both O(n), equivalent.
        - Space:
            - Recursive: O(h) call stack (O(log n) balanced, O(n) skewed)
            - Iterative: O(n) parent map regardless of tree shape
            - Recursive is more space-efficient on balanced trees
            - On skewed trees, both are O(n), but iterative has higher constants
        - Code clarity:
            - Recursive is shorter and more elegant
            - Iterative is more explicit but verbose
        - Robustness:
            - Recursive risks stack overflow on deep trees (~1000 depth in Python)
            - Iterative handles arbitrarily deep trees safely
        - When to prefer iterative:
            - Tree depth may exceed recursion limit
            - Need explicit control over traversal
            - Stack limits are constrained
            - Multiple LCA queries on the same tree (build parent map once)
        """

        # Pre-check: handle None inputs before doing any work. 
        # LeetCode guarantees p and q exist, but this makes the function robust
        # Note: we can only check for None here — we can't verify that p and q
        # are actually in the tree without traversing it first. Tree membership
        # is checked AFTER building the parent map (see safety check below).
        if not root or not p or not q:
            return None

        # Optional micro-optimization: if root is one of the targets,
        # it must be the LCA. NOT REQUIRED for correctness, can be removed.
        # if root == p or root == q:
        #     return root
        
        # Step 1: Build parent pointer map
        # Key: node, Value: parent node (root's parent is None)
        parent = {root: None}
        
        # Use stack for iterative DFS traversal
        stack = [root]
        
        # Continue until both p and q are found in parent map
        # This is an optimization to avoid traversing entire tree
        # Robustness: add `stack and` guard to avoid IndexError if p or q
        # isn't in the tree, i.e. `while stack and (p not in parent or q not in parent):`
        while p not in parent or q not in parent:
            node = stack.pop()
            
            # Process left child
            if node.left:
                parent[node.left] = node  # Store parent relationship
                stack.append(node.left)    # Add to stack for further traversal
            
            # Process right child
            if node.right:
                parent[node.right] = node  # Store parent relationship
                stack.append(node.right)   # Add to stack for further traversal

        # Safety check: if p or q is not in the tree, return None.
        # Paired with the `stack and` guard above — that guard lets the loop
        # exit without crashing, and this check catches the resulting missing
        # entries before they'd trigger a KeyError in the ancestor walk below.

        # This check belongs AFTER the build (not before) because the parent
        # map IS our membership index — we can't know if a node is reachable
        # from root without traversing. Not needed for LC 236 (guarantees both
        # exist), but prevents KeyError on parent[cur] lookup below:
        
        # if p not in parent or q not in parent: 
        #     return None
        
        # Step 2: Collect all ancestors of p in a set
        # Use set (not list) for O(1) lookup instead of O(h) - critical for performance!
        # This creates the "ancestor chain" from p to root
        ancestors = set()
        
        # Traverse from p to root, adding each node to ancestors set
        # Use `cur` instead of mutating `p` — keeps the original input
        # reference intact and makes the code easier to read/debug
        cur = p
        while cur:
            ancestors.add(cur)  # Add current node (includes p itself - allows p to be LCA!)
            cur = parent[cur]   # Move up to parent
        # Mutating version (works, but overwrites the input parameter):
        # while p:
        #     ancestors.add(p)
        #     p = parent[p]
        
        # At this point, ancestors contains: {p, p's parent, ..., root}
        
        # Step 3: Find first common ancestor by traversing q's path
        # Walk up from q until we find a node that's also an ancestor of p
        # Each "cur not in ancestors" check is O(1) due to set (would be O(h) with list!)
        # Use `cur` instead of mutating `q` for the same reason as above
        cur = q
        while cur not in ancestors:
            cur = parent[cur]  # Move up q's ancestor chain
        # Mutating version (works, but overwrites the input parameter):
        # while q not in ancestors:
        #     q = parent[q]
        # return q
        
        # When loop exits, cur is the first node that appears in both ancestor chains
        # This is the Lowest Common Ancestor
        return cur

# Variant 1 : Find LCA of N-ary tree : Given an n-ary tree where each node can have multiple children, find the LCA of two nodes p and q.

# N-ary tree:
#            1
#         /  |  \
#        2   3   4
#       /|\     / \
#      5 6 7   8   9

# Definition for a Node.
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.children = []  # List of child nodes

# # Recursive Approach:

# class Solution:
#     def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
#         """
#         Recursive DFS for N-ary tree LCA.
        
#         Algorithm:
#         1. If current node is None or matches p or q, return current node
#         2. Recursively search ALL children
#         3. Count how many children found p or q
#         4. If 2+ children found nodes, current is LCA (split point)
#         5. If 1 child found both, propagate that result up
#         6. If current node is p/q and a child found the other, current is LCA
        
#         Time Complexity: O(n)
#             - Visit each node exactly once
#             - n = total number of nodes
        
#         Space Complexity: O(h)
#             - Recursion stack depth
#             - h = height of tree
#             - Best: O(log n) for balanced tree
#             - Worst: O(n) for skewed tree
        
#         Example:
#                         1
#                      /  |  \
#                     2   3   4
#                    / \      |
#                   5   6     7
#                  /
#                 8
        
#             Case 1: p = 8, q = 6 -> LCA = 2 (split across children)
#                 - LCA(8) returns 8, LCA(6) returns 6
#                 - At node 2: two children return non-null -> return 2
#                 - At node 1: one child returns non-null -> propagate 2 upward
            
#             Case 2: p = 2, q = 8 -> LCA = 2 (p is ancestor of q)
#                 - LCA(2) matches p and returns immediately (no recursion into its children)
#                 - At node 1: other children (3, 4) are still explored and return None
#                 - Only one child returns non-null -> propagate 2 upward
        
#         Notes:
#         - Local pruning: when a node matches p or q, its subtree is not explored further.
#         - No global pruning: sibling subtrees may still be explored at ancestor nodes.
#         - Correctness relies on the assumption that both p and q exist in the tree.
#         """
        
#         # Base case: if node is None or matches p or q, return it
#         if not root or root == p or root == q:
#             return root
        
#         # Recursively search in ALL children (not just left/right)
#         #  children_results is LOCAL per call — each recursive invocation
#         # needs its own list to track only ITS children's returns. A global
#         # list would mix results across unrelated subtrees and break the
#         # "how many of my children found a target?" logic. Python's stack
#         # frame isolation gives us this per-call scope for free.
#         children_results = []
#         for child in root.children:
#             result = self.lowestCommonAncestor(child, p, q)
#             if result:  # Only store non-null results
#                 children_results.append(result)
        
#         # Analyze results from children
#         # If 2+ children returned non-null, current node is the split point (LCA)
#         if len(children_results) >= 2:
#             return root
        
#         # If exactly 1 child returned non-null, propagate it up.
#         # The result is either p, q, or the LCA (if both targets were already
#         # found deeper in this child's subtree). Either way, the current node
#         # is not the LCA — pass the result up so an ancestor can decide.
#         if len(children_results) == 1:
#             return children_results[0]
        
#         # No children found anything, return None
#         return None

# Example:

# Build the tree:
#                 1
#              /  |  \
#             2   3   4
#            / \      |
#           5   6     7
#          /
#         8

# root = Node(1)
# n2, n3, n4 = Node(2), Node(3), Node(4)
# n5, n6, n7 = Node(5), Node(6), Node(7)
# n8 = Node(8)
# root.children = [n2, n3, n4]
# n2.children = [n5, n6]
# n4.children = [n7]
# n5.children = [n8]

# # Case 1: p = 8, q = 6 -> LCA = 2 (split across children)
# p = n8
# q = n6
# sol = Solution()
# res = sol.lowestCommonAncestor(root, p, q)
# print(res.val)  # 2

# # Case 2: p = 2, q = 8 -> LCA = 2 (p is ancestor of q)
# p = n2
# q = n8
# sol = Solution()
# res = sol.lowestCommonAncestor(root, p, q)
# print(res.val)  # 2


# Cleaner alternative with same logic

# class Solution:
#     def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
#         """
#         Recursive DFS for Lowest Common Ancestor (LCA) in an N-ary tree.
#         Count-based variant: tracks how many children returned non-null,
#         without building a list of results.
        
#         Algorithm:
#         1. If the current node is None or matches p or q, return the current node
#         2. Recursively search all children of the current node
#         3. Count how many children return a non-null result
#         4. If two or more children return non-null, the current node is the LCA (split point)
#         5. If exactly one child returns non-null, propagate that result upward
#         6. If no children return non-null, return None
        
#         Key Insight:
#         - The function returns a node if and only if the subtree rooted at that node
#           contains at least one of {p, q}.
#         - The first node where results come from two different child branches is the LCA.
#         - If one node is an ancestor of the other, the ancestor node is returned via the base case without      exploring its subtree.
        
#         Time Complexity: O(n)
#             - Each node is visited exactly once
#             - n = total number of nodes
        
#         Space Complexity: O(h)
#             - Recursion call stack depth equals tree height
#             - h = height of the tree
#             - Best case (balanced tree): O(log n)
#             - Worst case (skewed tree): O(n)
            
#             Why O(h) and not O(1), even though we use scalars instead of a list?
#             - Total space = (number of active stack frames) * (space per frame)
#             - Per-frame space: O(1) with scalars (O(k) with the list version,
#               where k = number of children). Swapping list -> scalars reduced
#               per-frame space but NOT the number of frames.
#             - Stack depth: O(h), because recursion must descend to find p and q.
#               Each frame on the path from root to a target is paused mid-loop,
#               waiting for its child's result — those frames stay on the stack.
#             - So total is O(h) * O(1) = O(h). The scalar optimization is a
#               constant-factor win, not an asymptotic one.
            
#             Why O(n) in the worst case?
#             - In a skewed/degenerate tree (each node has one child), h = n,
#               so O(h) = O(n). The stack itself holds n frames at peak depth.
#             - This is about tree SHAPE, not about what each frame stores.
            
#             To beat O(h), you need a fundamentally different approach:
#             - Pre-existing parent pointers on nodes: O(1) aux space per query
#               (walk up from p and q without recursion).
#             - Iterative with explicit stack: O(n) worst-case space (like BFS/DFS frontier), though recursion uses only O(h) call stack.
#             - Euler tour + RMQ / sparse table: O(n) preprocessing, O(1) per query;
#               best for multi-query workloads.
#             - Tarjan's offline LCA: O(alpha(n)) per query on average with union-find.
#             - None of these beat O(h) for a SINGLE query on a tree lacking
#               built-in parent pointers.
        
#         Example tree:
#                         1
#                      /  |  \
#                     2   3   4
#                    / \      |
#                   5   6     7
#                  /
#                 8
            
#             Case 1: p = 8, q = 6 -> LCA = 2 (split across children)
#                 - LCA(8) returns 8, LCA(6) returns 6
#                 - At node 2: two children return non-null -> return 2
#                 - At node 1: one child returns non-null -> propagate 2 upward
            
#             Case 2: p = 2, q = 8 -> LCA = 2 (p is ancestor of q)
#                 - LCA(2) matches p and returns immediately (no recursion into its children)
#                 - At node 1: other children (3, 4) are still explored and return None
#                 - Only one child returns non-null -> propagate 2 upward
        
#         Notes:
#         - Local pruning: when a node matches p or q, its subtree is not explored further.
#         - No global pruning: sibling subtrees may still be explored at ancestor nodes.
#         - Early-exit optimization: once `found_count == 2`, the current node is
#           guaranteed to be the LCA, so remaining children can be skipped.
#         - Correctness relies on the assumption that both p and q exist in the tree.
#         """
        
#         # Base case: if node is None or matches p or q, return it
#         if not root or root == p or root == q:
#             return root
        
#         # Track children that contain p or q.
#         # Using two scalars instead of a list: O(1) extra space per call,
#         # and we only ever need the COUNT of matches and the LAST match
#         # (for the count == 1 case). Both are kept local to this call —
#         # a shared/global version would mix results across unrelated subtrees.
#         found_count = 0
#         found_node = None
        
#         # Recursively search in ALL children (not just left/right)
#         for child in root.children:
#             result = self.lowestCommonAncestor(child, p, q)
#             if result:
#                 found_count += 1
#                 found_node = result  # overwritten if more matches come; that's fine
                
#                 # Early exit: once two children have returned non-null,
#                 # we already know `root` is the LCA. Skip remaining siblings.
#                 if found_count == 2:
#                     break
        
#         # Case A: 2+ children returned non-null -> current node is the split point (LCA)
#         # Note: given the early break above, found_count is always 0, 1, or 2 here,
#         # so `>= 2` is effectively `== 2`. Kept for defensiveness — if the break is
#         # ever removed, this still correctly identifies the split case.
#         if found_count >= 2:
#             return root
        
#         # Case B: exactly 1 child returned non-null -> propagate it upward.
#         # `found_node` is either p, q, or the LCA (if both targets were already
#         # found deeper in this child's subtree). Either way, the current node
#         # is NOT the LCA — pass the result up so an ancestor can decide.
#         if found_count == 1:
#             return found_node
        
#         # Case C: no children found anything -> neither p nor q in this subtree
#         return None

# # Another compact version

# class Solution:
#     def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
#         """
#         Recursive DFS for LCA in an N-ary tree. Compact variant.
        
#         Time Complexity: O(n) — each node visited at most once.
#         Space Complexity: O(h) — recursion stack depth.
#             Best case (balanced): O(log n). Worst case (skewed): O(n).
#         """
#         # Base case: None, or the node itself is p or q
#         if not root or root == p or root == q:
#             return root
        
#         # Track the single non-null result from children seen so far.
#         # If we see a SECOND non-null, this node is the split point (LCA).
#         found_node = None
        
#         for child in root.children:
#             result = self.lowestCommonAncestor(child, p, q)
#             if result:
#                 if found_node:
#                     return root  # second match -> current node is LCA
#                 found_node = result  # first match -> remember and keep searching
        
#         # Loop ended with 0 or 1 matches:
#         # - 0 matches: found_node is None -> neither target in this subtree
#         # - 1 match: found_node is p, q, or deeper LCA -> propagate upward
#         return found_node

# # Parent Pointers Approach:

# class Solution:
#     def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
#         """
#         Parent pointer approach for N-ary tree LCA (iterative DFS).
        
#         Algorithm:
#         1. Build parent map using DFS traversal (stops early once p and q found)
#         2. Collect all ancestors of p in a set
#         3. Walk up from q until finding first common ancestor
        
#         Time Complexity: O(n)
#             - Building parent map: O(n) worst case
#             - Collecting p's ancestors: O(h)
#             - Finding common ancestor: O(h)
#             - Overall: O(n)
        
#         Space Complexity: O(n)
#             - Parent map: O(n) for all nodes visited
#             - Ancestors set: O(h) for ancestor chain
#             - Stack for DFS traversal: O(n) worst case
#             - Overall: O(n)
        
#         Multi-query variant:
#             For k LCA queries on the SAME tree, build the parent map ONCE
#             in a constructor and reuse it across all queries:
            
#                 class LCAFinder:
#                     def __init__(self, root):
#                         self.parent = {root: None}
#                         stack = [root]
#                         while stack:
#                             node = stack.pop()
#                             for child in node.children:
#                                 self.parent[child] = node
#                                 stack.append(child)
                    
#                     def lca(self, p, q):
#                         ancestors = set()
#                         cur = p
#                         while cur:
#                             ancestors.add(cur)
#                             cur = self.parent[cur]
#                         cur = q
#                         while cur not in ancestors:
#                             cur = self.parent[cur]
#                         return cur
            
#             Cost breakdown for k queries:
#             - Construction: O(n) time, O(n) space (parent map, kept across queries)
#             - Per query: O(h) time (two upward walks), O(h) space (ancestors set,
#               transient — freed after each call)
#             - Total: O(n + k * h) time, O(n) peak space
            
#             Compared to calling the single-query version k times:
#             - Single-query repeated: O(k * n) time (rebuilds map each call)
#             - Multi-query cached:    O(n + k * h) time (reuses map)
#             - For balanced tree (h ~ log n), this is ~k times faster.
            
#             For very heavy workloads, consider specialized algorithms:
#             - Euler tour + RMQ: O(n log n) preprocessing, O(1) per query
#             - Binary lifting:   O(n log n) preprocessing, O(log n) per query
#         """
        
#         # Pre-check: handle None inputs
#         if not root or not p or not q:
#             return None
        
#         # Optional short-circuit: if root itself is p or q, it's the LCA.
#         # Not strictly needed — the main algorithm handles this correctly
#         # (root ends up in p's ancestor set, and q's walk-up finds it).
#         # Kept as a cheap optimization to skip the parent-map build entirely
#         # in this common edge case. Safe to remove for a leaner implementation.
#         if root == p or root == q:
#             return root
        
#         # Step 1: Build parent pointer map via iterative DFS.
#         # Early termination: stop once both p and q are seen.
#         # `stack and` guard prevents IndexError if p or q isn't in the tree.
#         parent = {root: None}
#         stack = [root]
        
#         while stack and (p not in parent or q not in parent):
#             node = stack.pop()
#             for child in node.children:  # ALL children, not just left/right
#                 parent[child] = node
#                 stack.append(child)
        
#         # Safety check: if p or q weren't reachable from root, return None.
#         # Not needed when inputs are guaranteed valid, but prevents KeyError below.
#         if p not in parent or q not in parent:
#             return None
        
#         # Step 2: Collect all ancestors of p in a set (O(1) lookup)
#         # Use `cur` instead of mutating p — keeps input reference intact
#         ancestors = set()
#         cur = p
#         while cur:
#             ancestors.add(cur)
#             cur = parent[cur]
        
#         # Step 3: Walk up from q to find first common ancestor
#         cur = q
#         while cur not in ancestors:
#             cur = parent[cur]
#         return cur

# Balanced ternary tree (each node has exactly 3 children):

#             1
#          /  |  \
#         2   3   4
#        /|\ /|\ /|\
#       5 6 7 8 9 10 11 12 13

# Total nodes: n = 13
# Height: h = 2 (levels: 0, 1, 2)
# Max width: w = 9 (at level 2)

# Space Complexity Breakdown for parent pointers

# 1. Parent Map: O(n)
# Parent map stores ALL nodes:

# parent = {
#     1: None,
#     2: 1, 3: 1, 4: 1,
#     5: 2, 6: 2, 7: 2,
#     8: 3, 9: 3, 10: 3,
#     11: 4, 12: 4, 13: 4
# }

# Total entries: 13 = n
# Space: O(13) = O(n)

# 2. Stack (DFS): O(w) or O(h)

# DFS traversal with stack:

# Initial:
# stack = [1]

# Step 1: Pop 1, push its 3 children
# stack = [2, 3, 4]  ← Size = 3

# Step 2: Pop 4, push its 3 children
# stack = [2, 3, 11, 12, 13]  ← Size = 5

# Step 3: Pop 13 (leaf, no children)
# stack = [2, 3, 11, 12]  ← Size = 4

# Step 4: Pop 12 (leaf) ← Found q!
# stack = [2, 3, 11]  ← Size = 3

# Step 5: Pop 11 (leaf)
# stack = [2, 3]  ← Size = 2

# Step 6: Pop 3, push its 3 children
# stack = [2, 8, 9, 10]  ← Size = 4

# Step 7: Pop 10 (leaf)
# stack = [2, 8, 9]  ← Size = 3

# Step 8: Pop 9 (leaf)
# stack = [2, 8]  ← Size = 2

# Step 9: Pop 8 (leaf)
# stack = [2]  ← Size = 1

# Step 10: Pop 2, push its 3 children
# stack = [5, 6, 7]  ← Size = 3

# Step 11: Pop 7 (leaf)
# stack = [5, 6]  ← Size = 2

# Step 12: Pop 6 (leaf) ← Found p! Stop
# stack = [5]

# Maximum stack size during traversal: 5
# Stack space: O(5)

# General formula for balanced k-ary tree:
# Max stack ≈ k * h (where k = children per node, h = height)
# For our tree: 3 * 2 = 6 (close to our observed 5)

# However, in worst case (complete tree), max stack = O(w)
# where w = max width = number of nodes at last level

# 3. Ancestors Set: O(h)

# Finding ancestors of p = node6:

# Path: 6 → 2 → 1 → None

# ancestors = set()

# Step 1: ancestors.add(6) → {6}
# Step 2: ancestors.add(2) → {6, 2}
# Step 3: ancestors.add(1) → {6, 2, 1}

# Size: 3 = height + 1 = h + 1
# Space: O(h) = O(2) for this tree

# Balanced Ternary Tree (n=13, h=2, w=9):

# ┌──────────────────┬──────────┬──────────────┐
# │ Component        │ Size     │ Big-O        │
# ├──────────────────┼──────────┼──────────────┤
# │ Parent map       │ 13       │ O(n)         │
# │ Stack (DFS)      │ ~5       │ O(h) or O(w) │
# │ Ancestors set    │ 3        │ O(h)         │
# ├──────────────────┼──────────┼──────────────┤
# │ Total            │ ~21      │ O(n)         │
# └──────────────────┴──────────┴──────────────┘

# Breakdown:
# - Parent map: 13 nodes (DOMINATES)
# - Stack: ~5 nodes (small compared to n)
# - Ancestors: 3 nodes (small compared to n)

# Overall: O(n) due to parent map

# Worst Case: Wide N-ary Tree - Space Complexity
# Example: Flat Tree (Root with Many Children)

# Worst case for stack space: All nodes at one level (maximum width)

#                     1
#     / / / / / / / / | \ \ \ \ \ \ \ \
#    2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17

# Total nodes: n = 17
# Height: h = 1 (only 2 levels: root and children)
# Max width: w = 16 (all nodes except root at level 1)

# Space Complexity Breakdown
# 1. Parent Map: O(n)

# Parent map stores ALL nodes:

# parent = {
#     1: None,
#     2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1,
#     10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1
# }

# Total entries: 17 = n
# Space: O(17) = O(n)

# 2. Stack (DFS): O(w) = O(n) WORST CASE!

# DFS traversal - THIS IS WHERE IT GETS BAD:

# Initial:
# stack = [1]

# Step 1: Pop 1, push ALL 16 children at once
# stack = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
#         ↑___________________________________________________↑
#                     16 nodes in stack!
                    
# MAXIMUM STACK SIZE: 16 = O(w) = O(n) ← WORST CASE! ⚠️

# Step 2: Pop 17 (leaf, no children)
# stack = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  ← Still 15!

# Step 3: Pop 16 (found q!)
# stack = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  ← Still 14!

# ... continues popping until we find p at node 5

# The stack stays HUGE because all children are at same level!

# 3. Ancestors Set: O(h) = O(1)

# Finding ancestors of p = node 5:

# Path: 5 → 1 → None

# ancestors = set()

# Step 1: ancestors.add(5) → {5}
# Step 2: ancestors.add(1) → {5, 1}

# Size: 2 = height + 1 = O(h) = O(1) for flat tree

# This is SMALL because tree is flat (h=1)

# Complete Space Analysis - Worst Case

# Wide/Flat Tree (n=17, h=1, w=16):

# ┌──────────────────┬──────────┬──────────────┐
# │ Component        │ Size     │ Big-O        │
# ├──────────────────┼──────────┼──────────────┤
# │ Parent map       │ 17       │ O(n)         │
# │ Stack (DFS)      │ 16 !!!   │ O(w) = O(n)  │ ← WORST!
# │ Ancestors set    │ 2        │ O(h) = O(1)  │
# ├──────────────────┼──────────┼──────────────┤
# │ Total            │ ~35      │ O(n)         │
# └──────────────────┴──────────┴──────────────┘

# Key issue: Stack holds almost ALL nodes simultaneously!
# Stack = 16 ≈ n (where n=17)

# Variant : Find LCA of Binary Search Tree

#            6
#          /   \
#         2     8
#        / \   / \
#       0   4 7   9
#          / \
#         3   5

# p = 3, q = 5  LCA is 4

# Approach : Recursive

# class Solution:
#     def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
#         """
#         LCA in BST - leverages BST property for optimization.
        
#         Key Insight:
#         - If both p and q < root: LCA is in left subtree
#         - If both p and q > root: LCA is in right subtree
#         - Otherwise: root is the LCA (split point)
        
#         Time Complexity: O(h)
#             - Only traverse ONE path from root to LCA
#             - h = height of tree
#             - Best: O(log n) for balanced BST
#             - Worst: O(n) for skewed BST
        
#         Space Complexity: O(h)
#             - Recursion stack depth
#             - Best: O(log n) for balanced
#             - Worst: O(n) for skewed
#         """
        
#         # Both p and q are smaller than root - LCA is in left subtree
#         if p.val < root.val and q.val < root.val:
#             return self.lowestCommonAncestor(root.left, p, q)
        
#         # Both p and q are greater than root - LCA is in right subtree
#         elif p.val > root.val and q.val > root.val:
#             return self.lowestCommonAncestor(root.right, p, q)
        
#         # Split point: one on left, one on right (or one is root)
#         # This means current root is the LCA
#         else:
#             return root

# Approach : Iterative (Better space, optimal solution)

# class Solution:
#     def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
#         """
#         Iterative approach - OPTIMAL space for BST.
        
#         Time Complexity: O(h)
#         Space Complexity: O(1) - No recursion, no extra data structures! 
#         """
        
#         current = root
        
#         while current:
#             # Both in left subtree
#             if p.val < current.val and q.val < current.val:
#                 current = current.left
            
#             # Both in right subtree
#             elif p.val > current.val and q.val > current.val:
#                 current = current.right
            
#             # Found split point - this is LCA
#             else:
#                 return current
        
#         return None  # Should never reach if p and q exist in tree




                    