"""
LeetCode 133. Clone Graph
Difficulty: Medium
URL: https://leetcode.com/problems/clone-graph/
"""

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# Approach : DFS

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:  # Optional['Node'] is just shorthand for Union['Node', None], meaning the value can be either a Node object or None
        """
        Clone a connected undirected graph using recursive DFS.

        Input is given as an adjacency list which LeetCode internally converts
        into linked Node objects before calling this function:
            adjList = [[2,4],[1,3],[2,4],[1,3]] becomes
            Node(1, neighbors=[Node(2), Node(4)]),
            Node(2, neighbors=[Node(1), Node(3)]), and so on.
        This function receives the Node object for node 1 as the entry point.

        For each unvisited node, create a clone and recursively clone all
        its neighbors. A visited map prevents re-cloning and handles cycles
        by returning the already-created clone on revisit.

        Args:
            node: Entry point into the original graph, or None if empty.

        Returns:
            Clone of the input node (entry point into the cloned graph),
            or None if the input is None.

        TC: O(V + E)  — each node and edge visited exactly once
        SC: O(V)      — visited map + recursion stack, both O(V)
        """
        # Maps each original node to its corresponding clone.
        # Serves two purposes:
        #   1. Deduplication — avoids re-cloning already-visited nodes
        #   2. Cycle handling — returns the in-progress clone on back-edges
        #
        # For a graph 1 <-> 2 <-> 3, it ends up as:
        #   { Node(1): Node(1)', Node(2): Node(2)', Node(3): Node(3)' }
        #   where Node(x)' denotes the cloned counterpart of Node(x)
        # Initialised as empty — unlike BFS, we never look up original_to_clone[curr]
        # for the current node being processed. clone is always a local variable
        # created at the top of _dfs and in hand before any wiring happens.
        original_to_clone: dict['Node', 'Node'] = {}

        def _dfs(original: 'Node') -> 'Node':
            # Base case: node already cloned — return its clone directly.
            # This is what breaks cycles (e.g. A→B→A hits A again here).
            if original in original_to_clone:
                return original_to_clone[original]

            # We pass original.val (an int) because Node.__init__ expects val=int.
            # Node(original) would pass the entire Node object as val — wrong type.
            # We omit neighbors entirely (defaults to []) and populate them in the
            # for-loop below with proper clones, not references to original nodes.
            #
            # e.g. if original = Node(1, neighbors=[Node(2), Node(3)])
            #      then clone   = Node(1, neighbors=[])   ← neighbors filled in later
            clone = Node(original.val)

            # Register BEFORE recursing into neighbors.
            #
            # Example — simple cycle: A <-> B
            #
            #   _dfs(A) called:
            #     clone_A created, original_to_clone[A] = clone_A   ← registered here
            #     iterate A.neighbors → calls _dfs(B)
            #       clone_B created, original_to_clone[B] = clone_B
            #       iterate B.neighbors → calls _dfs(A)
            #         A is in original_to_clone → returns clone_A   ← cycle broken
            #       clone_B.neighbors = [clone_A]
            #       returns clone_B
            #     clone_A.neighbors = [clone_B]
            #     returns clone_A
            #
            # If the registration line were AFTER the for-loop instead:
            #   _dfs(A) → _dfs(B) → _dfs(A) → _dfs(B) → ... → RecursionError
            #   because A is never in original_to_clone when the back-edge is hit.
            original_to_clone[original] = clone

            for neighbor in original.neighbors:
                # _dfs returns the clone of `neighbor` (creating it if needed),
                # which we wire directly into this node's cloned neighbor list.
                clone.neighbors.append(_dfs(neighbor))

            return clone

        # Base check: empty graph — nothing to clone
        if node is None:
            return None

        # node is the entry point Node object, e.g. for adjList = [[2,3],[1],[1]]:
        #   node = Node(1, neighbors=[Node(2), Node(3)])
        #   where Node(2).neighbors = [Node(1)], Node(3).neighbors = [Node(1)]
        # The full graph is reachable by traversing .neighbors from this node.
        return _dfs(node)


# # Build graph for adjList = [[2,3],[1],[1]]
# #   1 -- 2
# #   |
# #   3

# node1 = Node(1)
# node2 = Node(2)
# node3 = Node(3)

# node1.neighbors = [node2, node3]
# node2.neighbors = [node1]
# node3.neighbors = [node1]

# # Run solution
# cloned_node1 = Solution().cloneGraph(node1)

# # `is` checks identity (same object in memory) — should be False for all clones
# # `==` on .val checks value equality — should be True for all clones
# print(cloned_node1.val)                                        # 1
# print(cloned_node1 is node1)                                   # False — different object ✓
# print(cloned_node1.val == node1.val)                           # True  — same value ✓

# print(cloned_node1.neighbors[0] is node2)                      # False — different object ✓
# print(cloned_node1.neighbors[0].val == node2.val)              # True  — same value ✓

# print(cloned_node1.neighbors[1] is node3)                      # False — different object ✓
# print(cloned_node1.neighbors[1].val == node3.val)              # True  — same value ✓

# # Verify back-edges point to clones, not originals
# print(cloned_node1.neighbors[0].neighbors[0] is cloned_node1)  # True — clone, not node1 ✓
# print(cloned_node1.neighbors[0].neighbors[0] is node1)         # False — not the original ✓


# Approach : BFS

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        """
        Clone a connected undirected graph using iterative BFS.

        Input is given as an adjacency list which LeetCode internally converts
        into linked Node objects before calling this function:
            adjList = [[2,4],[1,3],[2,4],[1,3]] becomes
            Node(1, neighbors=[Node(2), Node(4)]),
            Node(2, neighbors=[Node(1), Node(3)]), and so on.
        This function receives the Node object for node 1 as the entry point.

        For each unvisited neighbor, create a clone and enqueue it for
        processing. A visited map prevents re-cloning and handles cycles
        by skipping already-registered neighbors during neighbor wiring.

        Args:
            node: Entry point into the original graph, or None if empty.

        Returns:
            Clone of the input node (entry point into the cloned graph),
            or None if the input is None.

        TC: O(V + E)  — each node and edge visited exactly once
        SC: O(V)      — visited map + BFS queue, both O(V)
        """
        # Base check: empty graph — nothing to clone
        if node is None:
            return None

        # Maps each original node to its corresponding clone.
        # Serves two purposes:
        #   1. Deduplication — avoids re-cloning already-visited nodes
        #   2. Cycle handling — skips already-registered nodes during
        #      neighbor wiring instead of creating duplicates
        #
        # Initialised with the entry node so the queue has a starting point.
        # For a graph 1 <-> 2 <-> 3, it ends up as:
        #   { Node(1): Node(1)', Node(2): Node(2)', Node(3): Node(3)' }
        #   where Node(x)' denotes the cloned counterpart of Node(x)
        original_to_clone: dict['Node', 'Node'] = {node: Node(node.val)}

        # BFS queue holds original nodes whose neighbors still need wiring.
        # We enqueue a node the moment we clone it (at discovery time),
        # not when we finish processing it.
        queue: deque['Node'] = deque([node])

        while queue:
            curr = queue.popleft()

            for neighbor in curr.neighbors:
                if neighbor not in original_to_clone:
                    # Discover neighbor for the first time — clone and enqueue.
                    # We register here (at discovery) rather than at processing
                    # time so that if another node points to this same neighbor,
                    # it finds it in original_to_clone and skips re-cloning.
                    original_to_clone[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)

                # Wire the cloned neighbor into the cloned current node.
                # Whether neighbor was just discovered or already existed,
                # its clone is guaranteed to be in original_to_clone by now.
                original_to_clone[curr].neighbors.append(original_to_clone[neighbor])

        # Return the clone of the entry node — the full cloned graph is
        # reachable from here via .neighbors, mirroring the original structure.
        return original_to_clone[node]


# Variant : Clone a disconnected graph

# Given a reference to a disconnected undirected graph input, return a deep copy (clone) of the graph.The graph contains a list (List[Node]) of root nodes, where each root is the entry point to one connected component.

# Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

# class Graph:
#     roots: List[Node]

# class Node:
#     val: int
#     neighbors: List[Node]

# Example 1:
# Input:  graph.roots = [[1,2,3],[4,5]]
# Output: [[1,2],[2,1],[1,3],[3,1],[4,5],[5,4]]

# Explanation: There are 5 nodes across 2 disconnected components.
# Component 1: Node(1) <-> Node(2) <-> Node(3), fully connected among themselves.
# Component 2: Node(4) <-> Node(5).
# Example 2:
# Input:  graph.roots = [[]]
# Output: [[]]

# Explanation: A single node with no neighbors.
# Example 3:
# Input:  graph.roots = []
# Output: []

# Explanation: Empty graph, no components.

# Constraints:

# 1. The number of nodes across all components is in the range [0, 100]
# 2. 1 <= Node.val <= 100
# 3. Node.val is unique across all nodes
# 4. Each component is a connected undirected graph
# 5. Components are guaranteed to share no nodes
# 6. There are no self-loops or repeated edges within a component

# class Node:
#     def __init__(self, val=0, neighbors=None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []


# class Graph:
#     def __init__(self, roots=None):
#         # roots: one entry point per connected component
#         self.roots = roots if roots is not None else []


# class Solution:
#     def cloneGraph(self, graph: Optional['Graph']) -> Optional['Graph']:
#         """
#         Clone a disconnected undirected graph using recursive DFS.

#         Input is a Graph object containing a list of root nodes, one per
#         connected component:
#             graph.roots = [Node(1, neighbors=[Node(2), Node(3)]), Node(4, neighbors=[Node(5)])]
#             represents two components:
#                 component 1: Node(1) <-> Node(2) <-> Node(3)
#                 component 2: Node(4) <-> Node(5)

#         Args:
#             graph: Graph object containing root nodes, one per connected
#                    component. May be None for an empty graph.

#         Returns:
#             A new Graph object whose roots list mirrors the original,
#             with all nodes deeply cloned. Returns None if input is None.

#         TC: O(V + E)  — each node and edge visited exactly once across all components
#         SC: O(V)      — visited map + recursion stack, both O(V)
#         """
#         # Base check: empty graph — nothing to clone
#         if graph is None:
#             return None

#         # Shared across all components — correct regardless of whether components
#         # share nodes. Lives in outer scope so _dfs captures it via closure —
#         # no parameter passing needed.
#         #
#         # For graph.roots = [Node(1), Node(4)] it ends up as:
#         #   { Node(1): Node(1)', Node(2): Node(2)', Node(3): Node(3)',
#         #     Node(4): Node(4)', Node(5): Node(5)' }
#         #   where Node(x)' denotes the cloned counterpart of Node(x)
#         original_to_clone: dict['Node', 'Node'] = {}

#         def _dfs(original: 'Node') -> 'Node':
#             if original in original_to_clone:
#                 return original_to_clone[original]

#             clone = Node(original.val)

#             original_to_clone[original] = clone

#             for neighbor in original.neighbors:
#                 clone.neighbors.append(_dfs(neighbor))

#             return clone

#         # graph.roots is a list of Node objects, one per connected component.
#         # e.g. for adjList = [[1,2,3],[4,5]]:
#         #   graph.roots = [Node(1, neighbors=[Node(2), Node(3)]),
#         #                  Node(4, neighbors=[Node(5)])]
#         # Iterating gives one entry point at a time; the full component
#         # is reachable from each root via .neighbors.
#         cloned_roots = []

#         for root in graph.roots:
#             # self.roots itself is never None (Graph.__init__ normalizes it to at least []),
#             # but individual entries may still be None, e.g. Graph([None]).
            
#             # Skip such invalid component entry points. This is safe because the problem
#             # does not require preserving positional/index correspondence between
#             # input.roots and output.roots.
            
#             # (If index alignment were required, preserve the placeholder instead:
#             #     if root is None:
#             #         output.roots.append(None)
#             #         continue
#             #     output.roots.append(_dfs(root))

#             # so output.roots[i] still corresponds to input.roots[i].)

#             if root is None:
#                 continue

#             # Each _dfs call fully clones one component. The shared map
#             # ensures no node is visited twice even across multiple roots.
#             cloned_roots.append(_dfs(root))

#         # Wrap cloned roots in a new Graph object mirroring the original structure.
#         # e.g. for adjList = [[1,2,3],[4,5]]:
#         #   cloned_roots = [Node(1)', Node(4)']  — plain list
#         #   Graph(cloned_roots).roots = [Node(1)', Node(4)']  — wrapped in Graph
#         #
#         # Returning cloned_roots directly would fail since a list has no .roots
#         # attribute — caller expects a Graph object back, same type as input.
#         return Graph(cloned_roots)


# # ---------------------------------------------------------------------------
# # Build graph for adjList = [[1,2,3],[4,5]]
# #
# #   Component 1:          Component 2:
# #   Node(1) -- Node(2)    Node(4) -- Node(5)
# #      \      /
# #       Node(3)
# # ---------------------------------------------------------------------------
# node1 = Node(1)
# node2 = Node(2)
# node3 = Node(3)
# node4 = Node(4)
# node5 = Node(5)

# # Wire up component 1 — fully connected triangle
# node1.neighbors = [node2, node3]
# node2.neighbors = [node1, node3]
# node3.neighbors = [node1, node2]

# # Wire up component 2 — single edge
# node4.neighbors = [node5]
# node5.neighbors = [node4]

# # Build input graph with one root per component
# input_graph = Graph(roots=[node1, node4])

# # Run solution
# output_graph = Solution().cloneGraph(input_graph)

# # ---------------------------------------------------------------------------
# # Verify — `is` checks identity (different object), `==` checks value equality
# # ---------------------------------------------------------------------------

# # Component 1 root
# cloned_node1 = output_graph.roots[0]
# print(cloned_node1.val)                                          # 1
# print(cloned_node1 is node1)                                     # False — different object ✓
# print(cloned_node1.val == node1.val)                             # True  — same value ✓

# # Component 1 neighbors
# cloned_node2 = cloned_node1.neighbors[0]
# cloned_node3 = cloned_node1.neighbors[1]
# print(cloned_node2 is node2)                                     # False ✓
# print(cloned_node2.val == node2.val)                             # True  ✓
# print(cloned_node3 is node3)                                     # False ✓
# print(cloned_node3.val == node3.val)                             # True  ✓

# # Back-edges within component 1 point to clones, not originals
# print(cloned_node2.neighbors[0] is cloned_node1)                 # True  — clone ✓
# print(cloned_node2.neighbors[0] is node1)                        # False — not original ✓

# # Component 2 root
# cloned_node4 = output_graph.roots[1]
# print(cloned_node4.val)                                          # 4
# print(cloned_node4 is node4)                                     # False ✓
# print(cloned_node4.val == node4.val)                             # True  ✓

# # Component 2 neighbor
# cloned_node5 = cloned_node4.neighbors[0]
# print(cloned_node5 is node5)                                     # False ✓
# print(cloned_node5.val == node5.val)                             # True  ✓

# # Back-edge within component 2
# print(cloned_node5.neighbors[0] is cloned_node4)                 # True  — clone ✓
# print(cloned_node5.neighbors[0] is node4)                        # False — not original ✓

# Another solution : Use cloneGraph as a separate function 

# class Solution:
#     def _dfs(self, original: 'Node', original_to_clone: dict) -> 'Node':
#         """
#         Recursively clone a node and all nodes reachable from it.

#         Args:
#             original:           The node to clone.
#             original_to_clone:  Shared map of original → clone, passed in
#                                 explicitly since this is a class method and
#                                 cannot capture it via closure.

#         Returns:
#             The clone of the input node.

#         TC: O(V + E)  — each node and edge visited exactly once

#         SC: O(V)          
#             - recursion stack depth is O(V) in the worst case
#             - additionally uses a shared O(V) hashmap (original_to_clone) allocated by the caller
#         """

#         if original in original_to_clone:
#             return original_to_clone[original]

#         clone = Node(original.val)
#         original_to_clone[original] = clone

#         for neighbor in original.neighbors:
#             clone.neighbors.append(self._dfs(neighbor, original_to_clone))

#         return clone

#     def cloneGraph(self, graph: Optional['Graph']) -> Optional['Graph']:
#         """
#         Clone a disconnected undirected graph using recursive DFS.

#         Input is a Graph object containing a list of root nodes, one per
#         connected component:
#             graph.roots = [Node(1, neighbors=[Node(2), Node(3)]), Node(4, neighbors=[Node(5)])]
#             represents two components:
#                 component 1: Node(1) <-> Node(2) <-> Node(3)
#                 component 2: Node(4) <-> Node(5)

#         Difference from previous version:
#             Instead of building an intermediate cloned_roots list and wrapping
#             it in Graph() at the end, we initialize output = Graph() upfront
#             and append directly to output.roots — removing the need for a
#             separate list entirely.

#             Previous:                           Current:
#               cloned_roots = []                   output = Graph()
#               for root in graph.roots:            for root in graph.roots:
#                   cloned_roots.append(...)            output.roots.append(...)
#               return Graph(cloned_roots)          return output

#         Args:
#             graph: Graph object containing root nodes, one per connected
#                    component. May be None for an empty graph.

#         Returns:
#             A new Graph object whose roots list mirrors the original,
#             with all nodes deeply cloned. Returns None if input is None.

#         TC: O(V + E)  — each node and edge visited exactly once across all components
#         SC: O(V)      — visited map + recursion stack, both O(V)
#         """
#         # Base check: empty graph — nothing to clone
#         if graph is None:
#             return None

#         # Passed explicitly to self._dfs on every call because self._dfs is a
#         # class method — it has no enclosing scope to capture variables from
#         # via closure, unlike a nested _dfs function.
#         #
#         # A fresh map per root would also work here since the problem guarantees
#         # components share no nodes — each component is fully isolated.
#         #
#         # Fresh map per root (works given guarantee):
#         #   for root in graph.roots:
#         #       original_to_clone = {}               ← reset each iteration
#         #       output.roots.append(self._dfs(root, original_to_clone))
#         #
#         # Shared map (preferred — no assumption needed):
#         #   original_to_clone = {}                   ← created once outside loop
#         #   for root in graph.roots:
#         #       output.roots.append(self._dfs(root, original_to_clone))

#         original_to_clone: dict['Node', 'Node'] = {}

#         # Initialize output Graph upfront and append cloned roots directly —
#         # no intermediate list needed.
#         # e.g. for adjList = [[1,2,3],[4,5]]:
#         #   after loop: output.roots = [Node(1)', Node(4)']
#         output = Graph()

#         for root in graph.roots:
#             if root is None:
#                 continue
#             # Each _dfs call fully clones one component. The shared map
#             # ensures no node is visited twice even across multiple roots.
#             output.roots.append(self._dfs(root, original_to_clone))

#         return output



