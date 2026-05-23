"""
LeetCode 863. All Nodes Distance K in Binary Tree
Difficulty: Medium
URL: https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/
"""

# Check the without graph approach

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

# Approach : BFS on equivalent graph

# class Solution:
#     def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
#         """
#         Find all nodes at distance K from target node in a binary tree.
        
#         Approach: Build parent map to enable upward movement, then BFS from target
#         1. Build parent pointers to create undirected graph representation
#         2. Perform BFS from target node to find all nodes at distance k
        
#         Time: O(n) where n is number of nodes
#         Space: O(n) for parent map and BFS queue
#         """
        
#         # ============================================
#         # EDGE CASES - DEFENSIVE CHECKS
#         # ============================================
#         # These checks are NOT needed per LeetCode constraints,
#         # but included for defensive programming / production code
        
#         # Check 1: Null root (NOT needed per constraints, but good practice)
#         if not root:
#             return []
        
#         # Check 2: Null target (NOT needed per constraints)
#         if not target:
#             return []
        
#         # Check 3: Negative k (NOT needed per constraints)
#         if k < 0:
#             return []

#         # Check 4: Target not in tree (NOT needed per constraints)
#         # LeetCode guarantees target exists in tree, but for production code:
#         # We'd need to verify target is actually in the tree
#         # 
#         # HOW TO CHECK: Search for target in tree
#         # def is_in_tree(node, target):
#         #     if not node:
#         #         return False
#         #     if node == target:
#         #         return True
#         #     return is_in_tree(node.left, target) or is_in_tree(node.right, target)
#         # 
#         # if not is_in_tree(root, target):
#         #     return []
#         # 
#         # WHY is this check expensive?
#         # - Requires O(n) traversal just to validate
#         # - In LeetCode, this is guaranteed, so we skip it
#         # - In production, you might validate input before calling this function
        
#         # ============================================
#         # EDGE CASES - REQUIRED HANDLING
#         # ============================================
        
#         # Edge Case: k = 0 (MUST handle - optimization + clarity)
#         # If distance is 0, we want nodes at distance 0 from target
#         # That's just the target itself!
#         if k == 0:
#             return [target.val]
        
#         # ============================================
#         # STEP 1: Build Parent Map
#         # ============================================
#         # WHY do we need a parent map?
#         # - In a tree, nodes only know their children (node.left, node.right)
#         # - To find nodes at distance k, we might need to go UP to parent, then DOWN another branch
#         # - Parent map allows us to move UP the tree (child → parent)
#         # 
#         # Example: Tree structure
#         #       1
#         #      / \
#         #     2   3
#         #    /
#         #   4
#         # 
#         # If target=4 and k=2, answer is node 3
#         # Path: 4 → 2 (up) → 1 (up) → 3 (down)
#         # Without parent map, we can't go 4→2 or 2→1
        
#         parent = {}  # Maps each node → its parent node
#                      # Example: parent[node_2] = node_1
#                      # Root will map to None: parent[root] = None

#         # ============================================
#         # CRITICAL: Parent Map Uses NODE OBJECTS as Keys
#         # ============================================
#         # 
#         # IMPORTANT: parent dictionary uses TreeNode OBJECTS as keys, not node.val
#         # 
#         # This means the solution works PERFECTLY with duplicate values!
#         # 
#         # Example with duplicate values:
#         #       1
#         #      / \
#         #     2   2  ← Two different nodes, both with value 2
#         #    /     \
#         #   3       4
#         # 
#         # When we build parent map:
#         # - left_node_2 is one TreeNode object (memory address: 0x1234)
#         # - right_node_2 is another TreeNode object (memory address: 0x5678)
#         # 
#         # parent = {
#         #     left_node_2: node_1,   ← Key is the object at 0x1234
#         #     right_node_2: node_1,  ← Key is the object at 0x5678
#         #     node_3: left_node_2,
#         #     node_4: right_node_2
#         # }
#         # 
#         # Even though left_node_2.val == right_node_2.val == 2,
#         # they are DIFFERENT keys in the dictionary!
#         # 
#         # Python uses object identity (id/memory address) for dictionary keys,
#         # NOT the values stored inside the objects.
#         # 
#         # This is why:
#         # - If target is left_node_2, BFS finds nodes 1 and 3
#         # - If target is right_node_2, BFS finds nodes 1 and 4
#         # - Both work correctly even with duplicate values!
#         # 
#         # The LeetCode constraint "All Node.val values are unique" is actually
#         # UNNECESSARY for our algorithm - we handle duplicates automatically!
        
#         def build_parent_map(node, par=None):
#             """
#             DFS to build parent-child relationships for all nodes.
            
#             Parameters:
#             - node: current node being processed
#             - par: parent of current node (None for root)
#             """
#             if not node:
#                 return

#             parent[node] = par

#             build_parent_map(node.left, node)
#             build_parent_map(node.right, node)
        
#         # Start building from root (root's parent is None)
#         build_parent_map(root)
        
#         # After this step, parent map looks like:
#         # parent = {
#         #     root: None,
#         #     node_2: root,
#         #     node_3: root,
#         #     node_4: node_2,
#         #     ...
#         # }
        
#         # ============================================
#         # STEP 2: BFS from Target Node
#         # ============================================
#         # Now we can treat the tree as an undirected graph!
#         # Each node has 3 possible neighbors:
#         # 1. Left child (node.left)
#         # 2. Right child (node.right)  
#         # 3. Parent (parent[node]) ← this is NEW, enabled by parent map!
        
#         # BFS Initialization
#         queue = deque([target])  # Start BFS from target node
#         visited = {target}       # Mark target as visited
#         distance = 0             # Current distance level
        
#         # WHY distance = 0?
#         # We START at target, which is 0 edges away from itself
#         # As we expand: distance 0 → 1 → 2 → ... → k
        
#         # ============================================
#         # BFS LOOP - Level by Level Traversal
#         # ============================================
        
#         # WHY "distance < k" and NOT "distance <= k"?
#         # 
#         # We want to stop when queue contains nodes at distance k (our answer)
#         # Let's trace for k=2:
#         # 
#         # Start:     distance=0, queue=[target]         ← nodes at distance 0
#         #            Loop check: 0 < 2? YES, continue
#         #            ↓
#         # Iteration: distance=1, process target's neighbors
#         #            After: queue has distance 1 nodes
#         #            Loop check: 1 < 2? YES, continue
#         #            ↓
#         # Iteration: distance=2, process distance 1 nodes
#         #            After: queue has distance 2 nodes  ← THIS IS OUR ANSWER!
#         #            Loop check: 2 < 2? NO, STOP!
#         #
#         # If we used distance <= k:
#         #            Loop check: 2 <= 2? YES, continue  ← WRONG!
#         #            Would process distance 2 nodes and add distance 3 nodes
        
#         while queue and distance < k:
#             # WHY check "queue" in the condition?
#             # If tree is small and we run out of nodes before reaching distance k,
#             # we should stop early (queue will be empty)
#             # Example: k=10 but tree only has 3 nodes
            
#             # ========================================
#             # PROCESS ONE COMPLETE DISTANCE LEVEL
#             # ========================================
            
#             size = len(queue)  # How many nodes are at CURRENT distance?
            
#             # WHY do we need "size"?
#             # As we process nodes, we ADD their neighbors to the queue
#             # We need to know where the current level ends
            
#             distance += 1  # Moving to next distance level
            
#             # WHY increment distance HERE (before processing)?
#             # Because we're about to process current level nodes
#             # and ADD their neighbors, which will be at distance+1
#             # 
#             # Think: "I'm taking one step further from target"
#             # 
#             # Detailed trace for k=2:
#             # Initially: distance=0, queue=[target]
#             # 
#             # Iteration 1:
#             #   - distance becomes 1
#             #   - Process target (distance 0 node)
#             #   - Add target's neighbors → they're at distance 1
#             #   - After: queue has distance 1 nodes
#             # 
#             # Iteration 2:
#             #   - distance becomes 2
#             #   - Process distance 1 nodes
#             #   - Add their neighbors → they're at distance 2
#             #   - After: queue has distance 2 nodes ← ANSWER!
#             # 
#             # Loop check: 2 < 2? NO, stop!
            
#             # Process exactly "size" nodes (one complete level)
#             for _ in range(size):
#                 node = queue.popleft()  # Get one node from current level
                
#                 # ====================================
#                 # EXPLORE ALL NEIGHBORS
#                 # ====================================
                
#                 neighbors = [node.left, node.right, parent[node]]
                
#                 for neighbor in neighbors:
#                     if neighbor and neighbor not in visited:
#                         visited.add(neighbor)      # Mark as visited to prevent cycles
#                         queue.append(neighbor)     # Add to queue for next level
                        
#                         # This neighbor will be processed when distance increases
        
#         # ============================================
#         # STEP 3: Extract Result
#         # ============================================
        
#         # After BFS loop terminates, what's in the queue?
#         # Answer: ALL nodes at EXACTLY distance k from target!
#         # 
#         # Why?
#         # - Loop stops when distance = k (condition: distance < k fails)
#         # - The last iteration (when distance became k):
#         #   * Processed all nodes at distance k-1
#         #   * Added all their neighbors (which are at distance k)
#         #   * Those distance-k nodes are now in the queue
#         # - We never process them, so they remain in the queue
#         # 
#         # Example for k=2:
#         # - Last iteration: distance=2, processed distance-1 nodes
#         # - Added their neighbors (distance-2 nodes) to queue
#         # - Loop check: 2 < 2? NO, exit loop
#         # - Queue = [all distance-2 nodes] ← Our answer!
        
#         return [node.val for node in queue]

# TC : The overall time complexity is O(N), where N is the number of nodes in the binary tree, due to graph construction and BFS traversal.
# SC : The space complexity is also O(N), accounting for the graph storage, BFS queue, visited set, and output list.


# Approach : Adjacency List (Bidirectional Graph) Solution

# class Solution:
#     def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
#         """
#         Find all nodes at distance K from target node in a binary tree.
        
#         Approach: Build undirected graph using adjacency list, then BFS from target
        
#         Time: O(n) - build graph O(n) + BFS O(n)
#         Space: O(n) - graph storage + BFS queue
#         """
        
#         # ============================================
#         # EDGE CASES
#         # ============================================
        
#         # Defensive checks (not required by LeetCode)
#         if not root:
#             return []
#         if not target:
#             return []
#         if k < 0:
#             return []
        
#         # k = 0: return only the target node
#         if k == 0:
#             return [target.val]
        
#         # ============================================
#         # STEP 1: Build Undirected Graph (Adjacency List)
#         # ============================================
#         # Convert tree to undirected graph where each node knows ALL its neighbors
#         # (parent and children), enabling movement in any direction
        
#         graph = defaultdict(list)
        
#         # ============================================
#         # WHY defaultdict(list)?
#         # ============================================
#         # 
#         # defaultdict(list) automatically creates empty list for new keys
#         # 
#         # WITH defaultdict:
#         #   graph[node].append(neighbor)  ← Works even if node not in graph!
#         # 
#         # defaultdict eliminates repetitive checks → cleaner code
        
#         def create_undirected_graph(node):
#             """Build bidirectional edges between parent and children"""
#             if node is None:
#                 return
            
#             # WITH defaultdict(list):
#             # Just append directly - no existence checks needed!
            
#             if node.left:
#                 graph[node].append(node.left)        # parent → child
#                 graph[node.left].append(node)        # child → parent
            
#             if node.right:
#                 graph[node].append(node.right)       # parent → child
#                 graph[node.right].append(node)       # child → parent
            
#             # WITHOUT defaultdict (alternative - more verbose):
#             # 
#             # if node.left:
#             #     if node not in graph:
#             #         graph[node] = []
#             #     if node.left not in graph:
#             #         graph[node.left] = []
#             #     graph[node].append(node.left)
#             #     graph[node.left].append(node)
#             # 
#             # if node.right:
#             #     if node.right not in graph:
#             #         graph[node.right] = []
#             #     graph[node].append(node.right)
#             #     graph[node.right].append(node)
#             # 
#             # defaultdict eliminates all the "if not in graph" checks!
            
#             create_undirected_graph(node.left)
#             create_undirected_graph(node.right)
        
#         # Build the complete undirected graph
#         create_undirected_graph(root)
        
#         queue = deque([target])
#         visited = {target}       
#         distance = 0
        
#         while queue and distance < k:
#             size = len(queue)    
#             distance += 1        
            
#             for _ in range(size):
#                 node = queue.popleft()
                
#                 # KEY DIFFERENCE from parent map approach:
#                 # Instead of: [node.left, node.right, parent[node]]
#                 # We use: graph[node] (all neighbors in one list)
                
#                 for neighbor in graph[node]:
#                     # No need to check "if neighbor" because graph only stores
#                     # actual node objects (we never add None to the graph)
                    
#                     if neighbor not in visited:
#                         visited.add(neighbor)
#                         queue.append(neighbor)
        
#         # Queue contains all nodes at exactly distance k
#         return [node.val for node in queue]

# Approach : DFS on equivalent graph

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
        
        result = []
        visited = set()
        
        def dfs(node, distance):
            """
            DFS to find all nodes at exactly distance k from target.
            
            Parameters:
            - node: current node being explored
            - distance: current distance from target
            """
            if not node or node in visited:
                return
            
            # Mark node as visited to prevent cycles
            visited.add(node)
            
            # BASE CASE: Found a node at distance k!
            if distance == k:
                result.append(node.val)
                return  # Don't go further (we want exactly distance k)

                # WHY just "return" and NOT "return result"?
                # 
                # Because result is a SHARED list across ALL recursive calls!
                # Multiple branches can find nodes at distance k.
                # 
                # Example:
                #     1
                #   /   \
                #  2     3
                # /       \
                # 4         5
                # 
                # If target=1, k=2, answer should be [4, 5]
                # 
                # With "return" (correct):
                # dfs(1,0) → dfs(2,1) → dfs(4,2): result=[4], return
                #                     ← back to dfs(2,1), continues
                #         → dfs(3,1) → dfs(5,2): result=[4,5], return
                # Final: [4, 5] ✓
                # 
                # With "return result" (wrong):
                # dfs(1,0) → dfs(2,1) → dfs(4,2): result=[4], return [4]
                #                     ← returns [4], STOPS exploring!
                # Never reaches dfs(3,1) or dfs(5,2)
                # Final: [4] ✗ (missing node 5!)
                # 
                # Key insight: "return" stops THIS branch, not entire recursion
                #              "return result" would exit the whole DFS early
            
            # RECURSIVE CASE: Explore all neighbors at distance + 1
            # WITH ADJACENCY LIST:
            for neighbor in graph[node]:
                if neighbor not in visited:
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



