"""
LeetCode 863. All Nodes Distance K in Binary Tree
Difficulty: Medium
URL: https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
        """
        Find all nodes at distance K from target node using DFS.
        
        Approach: Build graph, then DFS from target with distance tracking
        
        Time: O(n) - build graph O(n) + DFS O(n)
        Space: O(n) - graph storage + recursion stack
        """
        
        # Edge cases
        if not root or not target or k < 0:
            return []
        
        if k == 0:
            return [target.val]
        
        # ============================================
        # STEP 1: Build Undirected Graph
        # ============================================
        
        graph = defaultdict(list)
        
        def create_undirected_graph(node):
            if node is None:
                return
            
            if node.left:
                graph[node].append(node.left)
                graph[node.left].append(node)
            
            if node.right:
                graph[node].append(node.right)
                graph[node.right].append(node)
            
            create_undirected_graph(node.left)
            create_undirected_graph(node.right)
        
        create_undirected_graph(root)
        
        # ============================================
        # ALTERNATIVE: Parent Map Approach (instead of undirected graph)
        # ============================================
        # 
        # Instead of building full adjacency list, build parent map only:
        # 
        # parent = {}
        # 
        # def build_parent_map(node, par=None):
        #     if not node:
        #         return
        #     parent[node] = par
        #     build_parent_map(node.left, node)
        #     build_parent_map(node.right, node)
        # 
        # build_parent_map(root)
        # 
        # KEY DIFFERENCES:
        # - Adjacency list: graph[node] gives ALL neighbors in one list
        # - Parent map: Need to combine [node.left, node.right, parent[node]]
        # 
        # Storage comparison:
        # - graph: stores ~2n edges (bidirectional)
        # - parent: stores n parent pointers
        # - Both are O(n) space
        
        # ============================================
        # STEP 2: DFS from Target Node
        # ============================================
        # Instead of BFS level-by-level, use DFS with distance parameter
        
        # SPACE COMPLEXITY: BFS vs DFS
        # ----------------------------
        # Both O(n) worst case, but different in practice:
        # 
        # BFS: Queue holds one complete LEVEL at a time
        # DFS: Stack holds one PATH from root to current node
        # 
        # Balanced tree (height = log n):
        #   BFS queue: O(n/2) = O(n) at leaf level (wide)
        #   DFS stack: O(log n) depth (tall) ← BETTER for balanced trees
        # 
        # Skewed tree (like linked list, height = n):
        #   BFS queue: O(1) only one node per level (narrow) ← BETTER for skewed trees
        #   DFS stack: O(n) depth (very tall)
        # 
        # For this problem: Both work fine, BFS more intuitive for "distance k"
        
        result = []
        visited = {target}
        
        def dfs(node, distance):
            """
            DFS to find all nodes at exactly distance k from target.
            
            Parameters:
            - node: current node being explored
            - distance: current distance from target
            """
            if not node:
                return
            
            # Mark node as visited to prevent cycles
            # visited.add(node)
            
            # BASE CASE: Found a node at distance k!
            if distance == k:
                result.append(node.val)
                return result  # Don't go further (we want exactly distance k)
                
                # "return" vs "return result" -- in THIS code, they behave IDENTICALLY.
                # 
                # Why? Because the caller (the for-loop below) never captures or
                # uses the return value:
                #     for neighbor in graph[node]:
                #         if neighbor not in visited:
                #             dfs(neighbor, distance + 1)   # return value discarded!
                # 
                # So whether dfs(4,2) does "return" (implicitly returns None) or
                # "return result" (returns the list), dfs(2,1)'s for-loop just
                # ignores it either way and moves on to its next neighbor.
                # No upward propagation happens -- each call only exits itself.
                # 
                # Trace for target=1, k=2 on:
                #     1
                #   /   \
                #  2     3
                # /       \
                # 4         5
                # 
                # dfs(1,0) → dfs(2,1) → dfs(4,2): result=[4], return (or return result)
                #                     ← back to dfs(2,1), loop continues (no more neighbors)
                #          → dfs(3,1) → dfs(5,2): result=[4,5], return (or return result)
                # Final either way: [4, 5] ✓
                # 
                # Bare "return" is still preferred style: it doesn't imply a
                # meaningful return value, and it stays correct even if the loop
                # is later refactored to something like "return dfs(neighbor, ...)",
                # which WOULD propagate the early exit upward and break correctness.
            
            # RECURSIVE CASE: Explore all neighbors at distance + 1
            # WITH ADJACENCY LIST:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor, distance + 1)
            
            # ============================================
            # WITH PARENT MAP (alternative - comment above, uncomment below):
            # ============================================
            # 
            # neighbors = [node.left, node.right, parent[node]]
            # 
            # for neighbor in neighbors:
            #     if neighbor and neighbor not in visited:
            #         dfs(neighbor, distance + 1)
            # 
            # KEY DIFFERENCE:
            # - Adjacency list: for neighbor in graph[node]
            #   * All neighbors in one unified list
            #   * No need to check "if neighbor" (only actual nodes stored)
            # 
            # - Parent map: for neighbor in [node.left, node.right, parent[node]]
            #   * Combine neighbors from TWO sources:
            #     1. Tree structure: node.left, node.right
            #     2. Parent map: parent[node]
            #   * Must check "if neighbor" (could be None)
            # 
            # Both work identically! Just different ways to access neighbors.
        
        # Start DFS from target with distance 0
        dfs(target, 0)
        
        return result
        