"""
LeetCode 146. LRU Cache
Difficulty: Medium
URL: https://leetcode.com/problems/lru-cache/
"""

class Node:
    """
    Doubly linked list node to store key-value pairs.
    """
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key      # Cache key
        self.value = value  # Cache value
        self.prev = None    # Pointer to previous node
        self.next = None    # Pointer to next node

class LRUCache:
    """
    LRU Cache implementation using HashMap + Doubly Linked List.
    Design where MRU is at the TAIL end. In interview, try to write helper functions ASAP.
    
    List Structure:
        Head (dummy) <-> [LRU] <-> ... <-> [MRU] <-> Tail (dummy)
        - Head.next = Least Recently Used item (evict from here)
        - Tail.prev = Most Recently Used item (add here)
    
    Time Complexity:
        - get(key): O(1)
        - put(key, value): O(1)
    
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int):
        """
        Initialize LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        # Base check: Validate capacity (NOT needed for interviews, needed for production)
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")

        self.capacity = capacity
        self.cache = {}  # HashMap: key -> Node
        
        # Create dummy head and tail nodes
        self.head = Node(-1, -1)  # Dummy head
        self.tail = Node(-1, -1)  # Dummy tail
        
        # Initially empty: Head <-> Tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node: Node) -> None:
        """
        Remove a node from the doubly linked list.
        This doesn't delete the node from memory, just disconnects it from the list.
        
        Time Complexity: O(1) - Only pointer updates, no traversal needed
        
        Before:  prev <-> node <-> next
        After:   prev <----------> next
        
        Args:
            node: Node to remove from the list
        """
        # Base check: Validate node is not None (NOT needed for interviews, needed for production)
        if node is None:
            return

        # Bypass the node by connecting its neighbors directly
        node.prev.next = node.next  # Previous node skips over current node
        node.next.prev = node.prev  # Next node points back to previous node
    
    def _add_to_tail(self, node: Node) -> None:
        """
        Add a node right BEFORE the tail (most recently used position).
        This makes the node the new MRU item.
        
        Time Complexity: O(1)
        
        Before:  ... <-> last_node <-> Tail
        After:   ... <-> last_node <-> node <-> Tail
        
        Args:
            node: Node to add before tail (MRU position)
        """
        # Base check: Validate node is not None (NOT needed for interviews, needed for production)
        if node is None:
            return
            
        # Step 1: Set node's next pointer
        node.next = self.tail

        # Step 2: Set node's prev pointer
        # 'node' here refers to the NEW node we're trying to insert (passed as parameter)
        # We need to set its prev pointer to connect it to the existing list
        #
        # Use self.tail.prev (not self.head) because tail.prev dynamically points to:
        # - Head (if list is empty), OR
        # - The last real node (if list has items)
        # This makes the code work for BOTH cases without conditionals!
        # 
        # Example 1 (empty list, adding Node(2,2)):
        #   Before: Head <-> Tail
        #   tail.prev = Head (the node currently before Tail)
        #   node = Node(2,2) (the new node we're inserting)
        #   So: node.prev = Head means Node(2,2).prev = Head ✓
        #   We're setting Node(2,2)'s prev pointer to point back to Head
        #
        # Example 2 (list has Node(1,1), now adding Node(2,2)):
        #   Before: Head <-> [1:1] <-> Tail
        #   tail.prev = Node(1,1) (the node currently before Tail)
        #   node = Node(2,2) (the new node we're inserting)
        #   So: node.prev = Node(1,1) means Node(2,2).prev = Node(1,1) ✓
        #   We're setting Node(2,2)'s prev pointer to point back to Node(1,1)
        #
        # WRONG alternative (if we used self.head):
        #   node.prev = Head (always points new node's prev to Head!)
        #   When adding Node(2,2) to a list with Node(1,1):
        #     Node(2,2).prev = Head (ignores that Node(1,1) exists)
        #     After all 4 steps: Head <-> [2:2] <-> Tail
        #     Node(1,1) is orphaned and lost! ❌
        node.prev = self.tail.prev
        
        # Step 3: Update the node that's currently before tail to point forward to our new node
        # Use self.tail.prev.next (not self.head.next) because:
        # - If list is empty: tail.prev = head, so we update head.next ✓
        # - If list has items: tail.prev = last_node, so we update last_node.next ✓
        #
        # Example 1 (empty list, adding Node(2,2)):
        #   Before: Head <-> Tail
        #   tail.prev.next means Head.next
        #   Head.next = node means Head.next = Node(2,2)
        #   We're updating Head to point forward to our new Node(2,2)
        #   Result: Head <-> [2:2] <-> Tail ✓
        #
        # Example 2 (list has Node(1,1), now adding Node(2,2)):
        #   Before: Head <-> [1:1] <-> Tail
        #   CORRECT (using tail.prev.next):
        #     tail.prev.next means Node(1,1).next
        #     Node(1,1).next = node means Node(1,1).next = Node(2,2)
        #     We're updating Node(1,1) to point forward to our new Node(2,2)
        #     Result: Head <-> [1:1] <-> [2:2] <-> Tail ✓
        #
        #   WRONG alternative (if we used self.head.next):
        #     self.head.next = node means Head.next = Node(2,2)
        #     This reassigns what Head points to, breaking the link to Node(1,1)!
        #     Result: Head <-> [2:2] <-> Tail
        #             Node(1,1) is orphaned! ❌
        self.tail.prev.next = node
        
        # Step 4: Update tail to point back to the new node
        self.tail.prev = node
    
    def _move_to_tail(self, node: Node) -> None:
        """
        Move an existing node to the tail (mark as most recently used).
        
        Time Complexity: O(1)
        
        Args:
            node: Node to move to the back (MRU position)
        """
        # First remove the node from its current position
        self._remove(node)
        
        # Then add it back before tail (MRU position)
        self._add_to_tail(node)
    
    def get(self, key: int) -> int:
        """
        Get the value of the key if it exists in the cache.
        Mark the key as most recently used by moving to tail.
        
        Time Complexity: O(1)
        
        Args:
            key: The key to look up
            
        Returns:
            Value associated with key, or -1 if key doesn't exist
        """
        # Base check: Return -1 if key doesn't exist (REQUIRED for interviews - problem spec)
        if key not in self.cache:
            return -1
        
        # Key exists - get the node reference
        node = self.cache[key]
        
        # Move this node to tail to mark it as most recently used
        self._move_to_tail(node)
        
        # Return the value
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        If key exists: Update its value and mark as MRU
        If key is new: Add it to the cache
            - If at capacity: Evict the LRU item first
        
        Time Complexity: O(1)
        
        Args:
            key: The key to insert/update
            value: The value to associate with the key
        """
        # Base check: Branch between update vs insert (REQUIRED for interviews - different logic)
        if key in self.cache:
            # Case 1: Key already exists - UPDATE
            
            # Get the existing node
            node = self.cache[key]

            # Check: Handle corrupted cache state
            # NOT NEEDED FOR INTERVIEWS - key exists → node exists
            # NEEDED FOR PRODUCTION - graceful recovery
            if node is None:
                # Treat as new insertion
                new_node = Node(key, value)
                self.cache[key] = new_node
                self._add_to_tail(new_node)
                return  # Exit early - prevents crash from trying to use corrupted node below
            
            # Update the value (don't create a new node!)
            node.value = value
            
            # Move to tail to mark as most recently used
            self._move_to_tail(node)
        else:
            # Case 2: Key is new - INSERT
            
            # Create a new node with the key-value pair
            new_node = Node(key, value)
            
            # Add to HashMap for O(1) access
            self.cache[key] = new_node
            
            # Add to tail of list (mark as most recently used)
            self._add_to_tail(new_node)
            
            # Base check: Evict LRU if exceeded capacity (REQUIRED for interviews - core LRU logic)
            if len(self.cache) > self.capacity:
                # Evict the least recently used item
                
                # Get LRU node (node after head)
                lru_node = self.head.next
                
                # Remove from list using helper (REQUIRED for interviews)
                self._remove(lru_node)
                
                # Remove from HashMap (REQUIRED for interviews - must delete from both structures)
                del self.cache[lru_node.key]  # or, self.cache.pop(lru_node.key)

    def size(self) -> int:
        """Return the current number of items in the cache."""
        return len(self.cache)

    def is_empty(self) -> bool:
        """Check if the cache is empty."""
        return len(self.cache) == 0
    
    def clear(self) -> None:
        """Remove all items from the cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

# Example

# cache = LRUCache(2)  # capacity = 2

# cache.put(1, 1)
# List: Head <-> [1:1] <-> Tail
# Cache: {1: Node(1,1)}

# cache.put(2, 2)
# List: Head <-> [1:1] <-> [2:2] <-> Tail
# Cache: {1: Node(1,1), 2: Node(2,2)}
# LRU: key 1, MRU: key 2

# cache.get(1)  # returns 1
# List: Head <-> [2:2] <-> [1:1] <-> Tail (1 moved to tail)
# Cache: {1: Node(1,1), 2: Node(2,2)}
# LRU: key 2, MRU: key 1

# cache.put(3, 3)  # evicts key 2
# List: Head <-> [1:1] <-> [3:3] <-> Tail
# Cache: {1: Node(1,1), 3: Node(3,3)}
# Evicted: key 2 (was LRU)
# LRU: key 1, MRU: key 3

# cache.get(2)  # returns -1 (not found)
# List: Head <-> [1:1] <-> [3:3] <-> Tail (no change)
# Cache: {1: Node(1,1), 3: Node(3,3)}

# cache.put(4, 4)  # evicts key 1
# List: Head <-> [3:3] <-> [4:4] <-> Tail
# Cache: {3: Node(3,3), 4: Node(4,4)}
# Evicted: key 1 (was LRU)
# LRU: key 3, MRU: key 4

# cache.get(1)  # returns -1 (not found)
# cache.get(3)  # returns 3
# cache.get(4)  # returns 4
# Final List: Head <-> [3:3] <-> [4:4] <-> Tail
# Final Cache: {3: Node(3,3), 4: Node(4,4)}
# LRU: key 3, MRU: key 4

# Add to Head Implementation

class LRUCache:
    """
    LRU Cache implementation using HashMap + Doubly Linked List.
    Design where MRU is at the HEAD end.
    
    List Structure:
        Head (dummy) <-> [MRU] <-> ... <-> [LRU] <-> Tail (dummy)
        - Head.next = Most Recently Used item (add here)
        - Tail.prev = Least Recently Used item (evict from here)
    
    Time Complexity:
        - get(key): O(1)
        - put(key, value): O(1)
    
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int):
        """
        Initialize LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # HashMap: key -> Node
        
        # Create dummy head and tail nodes
        self.head = Node(-1, -1)  # Dummy head
        self.tail = Node(-1, -1)  # Dummy tail
        
        # Initially empty: Head <-> Tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node: Node) -> None:
        """
        Remove a node from the doubly linked list.
        This doesn't delete the node from memory, just disconnects it from the list.
        
        Time Complexity: O(1) - Only pointer updates, no traversal needed
        
        Before:  prev <-> node <-> next
        After:   prev <----------> next
        
        Args:
            node: Node to remove from the list
        """
        # Bypass the node by connecting its neighbors directly
        node.prev.next = node.next  # Previous node skips over current node
        node.next.prev = node.prev  # Next node points back to previous node
    
    def _add_to_head(self, node: Node) -> None:
        """
        Add a node right AFTER the head (most recently used position).
        This makes the node the new MRU item.
        
        Time Complexity: O(1)
        
        Before:  Head <-> first_node <-> ...
        After:   Head <-> node <-> first_node <-> ...
        
        Args:
            node: Node to add after head (MRU position)
        """
        # Step 1: Set node's prev pointer
        node.prev = self.head
        
        # Step 2: Set node's next pointer
        # Use self.head.next (not self.tail) because head.next could be:
        # - Tail (if list is empty), OR
        # - First real node (if list has items)
        # This makes the code work for BOTH cases!
        # 
        # Example 1 (empty list):
        #   Before: Head <-> Tail (head.next = Tail)
        #   node.next = Tail ✓
        #
        # Example 2 (has nodes):
        #   Before: Head <-> [1:1] <-> Tail (head.next = Node(1,1))
        #   node.next = Node(1,1) ✓
        #
        # WRONG if we used self.tail:
        #   node.next = Tail (always!)
        #   Result when adding Node(2,2): Head <-> [2:2] <-> Tail
        #   But [1:1] is orphaned! ❌
        node.next = self.head.next
        
        # Step 3: Update the node that's currently after head
        # Use self.head.next.prev (not self.tail.prev) because:
        # - If list is empty: head.next = tail, so we update tail.prev ✓
        # - If list has items: head.next = first_node, so we update first_node.prev ✓
        #
        # Example 1 (empty list):
        #   Before: Head <-> Tail
        #   head.next.prev = tail.prev → points to node
        #   Result: Head <-> node <-> Tail ✓
        #
        # Example 2 (has nodes):
        #   Before: Head <-> [1:1] <-> Tail
        #   CORRECT (using head.next.prev):
        #     head.next.prev means Node(1,1).prev
        #     Node(1,1).prev = node
        #     Result: Head <-> node <-> [1:1] <-> Tail ✓
        #
        #   WRONG (if we used self.tail.prev):
        #     self.tail.prev = node (we're reassigning tail.prev!)
        #     Result: Head <-> node <-> Tail
        #             [1:1] is orphaned! ❌
        #     The old Node(1,1) is lost because Tail no longer points to it!
        self.head.next.prev = node
        
        # Step 4: Update head to point to the new node
        self.head.next = node
    
    def _move_to_head(self, node: Node) -> None:
        """
        Move an existing node to the head (mark as most recently used).
        
        Time Complexity: O(1)
        
        Args:
            node: Node to move to the front (MRU position)
        """
        # First remove the node from its current position
        self._remove(node)
        
        # Then add it back after head (MRU position)
        self._add_to_head(node)
    
    def get(self, key: int) -> int:
        """
        Get the value of the key if it exists in the cache.
        Mark the key as most recently used by moving to head.
        
        Time Complexity: O(1)
        
        Args:
            key: The key to look up
            
        Returns:
            Value associated with key, or -1 if key doesn't exist
        """
        # Check if key exists in cache
        if key not in self.cache:
            return -1
        
        # Key exists - get the node reference
        node = self.cache[key]
        
        # Move this node to head to mark it as most recently used
        self._move_to_head(node)
        
        # Return the value
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        If key exists: Update its value and mark as MRU
        If key is new: Add it to the cache
            - If at capacity: Evict the LRU item first
        
        Time Complexity: O(1)
        
        Args:
            key: The key to insert/update
            value: The value to associate with the key
        """
        if key in self.cache:
            # Case 1: Key already exists - UPDATE
            
            # Get the existing node
            node = self.cache[key]
            
            # Update the value (don't create a new node!)
            node.value = value
            
            # Move to head to mark as most recently used
            self._move_to_head(node)
        else:
            # Case 2: Key is new - INSERT
            
            # Create a new node with the key-value pair
            new_node = Node(key, value)
            
            # Add to HashMap for O(1) access
            self.cache[key] = new_node
            
            # Add to head of list (mark as most recently used)
            self._add_to_head(new_node)
            
            # Check if we've exceeded capacity
            if len(self.cache) > self.capacity:
                # Evict the least recently used item
                
                # Get LRU node (node before tail)
                lru_node = self.tail.prev
                
                # Remove from list using helper
                self._remove(lru_node)
                
                # Remove the LRU node from the HashMap
                del self.cache[lru_node.key]  # or, self.cache.pop(lru_node.key)

# Variant : LRU Cache with Delete and Last Operations

# Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
# Implement the LRUCache class:

# LRUCache(): Initialize the LRU cache.
# int get(int key): Return the value of the key if the key exists, otherwise return -1.
# void put(int key, int value): Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache.
# boolean del(int key): Deletes the key-value pair if the key exists and return true. Otherwise, return false.
# int last(): Returns the value if at least one entry exists. Otherwise, return -1.

# The functions get, put, and del must each run in O(1) average time complexity, with the exception of last which should run in O(1) time complexity.

# Example:

# Input:
# ["LRUCache", "put", "put", "put", "last", "del", "del", "del", "last"]
# [null], [4, 4], [5, 5], [3, 30], [], [5], [4], [3], []

# Output:
# [null, null, null, null, 30, true, true, true, -1]

# Explanation:
# LRUCache lRUCache = new LRUCache();
# lRUCache.put(4, 4);   // cache is {4=4}
# lRUCache.put(5, 5);   // cache is {4=4, 5=5}
# lRUCache.put(3, 30);  // cache is {4=4, 5=5, 3=30}
# lRUCache.last();      // 30
# lRUCache.del(5);      // true
# lRUCache.del(4);      // true
# lRUCache.del(3);      // true
# lRUCache.last();      // -1

# class LRUCache:
#     """
#     LRU Cache with delete and last operations.
#     Design where MRU is at the TAIL end.
    
#     List Structure:
#         Head (dummy) <-> [LRU] <-> ... <-> [MRU] <-> Tail (dummy)
#         - Head.next = Least Recently Used item
#         - Tail.prev = Most Recently Used item
    
#     Time Complexity:
#         - get(key): O(1)
#         - put(key, value): O(1)
#         - del(key): O(1)
#         - last(): O(1)
#     """
    
#     def __init__(self):
#         """Initialize the LRU cache (no capacity limit in this variant)."""
#         self.cache = {}  # HashMap: key -> Node
        
#         # Create dummy head and tail nodes
#         self.head = Node(-1, -1)
#         self.tail = Node(-1, -1)
        
#         # Initially empty: Head <-> Tail
#         self.head.next = self.tail
#         self.tail.prev = self.head
    
#     def _remove(self, node: Node) -> None:
#         """
#         Remove a node from the doubly linked list.
        
#         Time Complexity: O(1)
#         """
#         node.prev.next = node.next
#         node.next.prev = node.prev
    
#     def _add_to_tail(self, node: Node) -> None:
#         """
#         Add a node right BEFORE the tail (most recently used position).
        
#         Time Complexity: O(1)
#         """
#         node.next = self.tail
#         node.prev = self.tail.prev
#         self.tail.prev.next = node
#         self.tail.prev = node
    
#     def _move_to_tail(self, node: Node) -> None:
#         """
#         Move an existing node to the tail (mark as most recently used).
        
#         Time Complexity: O(1)
#         """
#         self._remove(node)
#         self._add_to_tail(node)
    
#     def get(self, key: int) -> int:
#         """
#         Return the value of the key if it exists, otherwise return -1.
        
#         Time Complexity: O(1)
#         """
#         if key not in self.cache:
#             return -1
        
#         node = self.cache[key]
#         self._move_to_tail(node)  # Mark as most recently used
#         return node.value
    
#     def put(self, key: int, value: int) -> None:
#         """
#         Update the value of the key if it exists. Otherwise, add the key-value pair.
        
#         Time Complexity: O(1)
#         """
#         if key in self.cache:
#             # Update existing key
#             node = self.cache[key]
#             node.value = value
#             self._move_to_tail(node)
#         else:
#             # Add new key
#             new_node = Node(key, value)
#             self.cache[key] = new_node
#             self._add_to_tail(new_node)
    
#     def delete(self, key: int) -> bool:
#         """
#         Delete the key-value pair if the key exists and return true.
#         Otherwise, return false.

#         Note: This removes the node entirely from both the list and HashMap.
#         Unlike get() or put(), we do NOT move the node to tail - we're deleting it.
        
#         Time Complexity: O(1)
#         """
#         if key not in self.cache:
#             return False
        
#         # Get the node
#         node = self.cache[key]
        
#         # Remove from list
#         self._remove(node)
        
#         # Remove from HashMap
#         del self.cache[key]

#         return True

#         # if delete has a void return type
#         # if key not in self.cache:
#         # return  # ← Just return (do nothing)
    
#         # node = self.cache[key]
#         # self._remove(node)
#         # del self.cache[key]
#         # ← No return statement needed (implicitly returns None)

#     def last(self) -> int:
#         """
#         Return the value of the most recently used entry if at least one entry exists.
#         Otherwise, return -1.
        
#         Time Complexity: O(1)
        
#         Note: Based on the example, last() returns the MRU value (tail.prev),
#         not the LRU value despite the confusing name.
#         """
#         # Check if cache is empty
#         if self.head.next == self.tail:
#             return -1
        
#         # Return the most recently used value (before tail)
#         return self.tail.prev.value

# # Add to Head Implementation

# class LRUCache:
#     """
#     LRU Cache with delete and last operations.
#     Design where MRU is at the HEAD end.
    
#     List Structure:
#         Head (dummy) <-> [MRU] <-> ... <-> [LRU] <-> Tail (dummy)
#         - Head.next = Most Recently Used item
#         - Tail.prev = Least Recently Used item
    
#     Time Complexity:
#         - get(key): O(1)
#         - put(key, value): O(1)
#         - delete(key): O(1)
#         - last(): O(1)
#     """
    
#     def __init__(self):
#         """Initialize the LRU cache (no capacity limit in this variant)."""
#         self.cache = {}  # HashMap: key -> Node
        
#         # Create dummy head and tail nodes
#         self.head = Node(-1, -1)
#         self.tail = Node(-1, -1)
        
#         # Initially empty: Head <-> Tail
#         self.head.next = self.tail
#         self.tail.prev = self.head
    
#     def _remove(self, node: Node) -> None:
#         """
#         Remove a node from the doubly linked list.
        
#         Time Complexity: O(1)
#         """
#         node.prev.next = node.next
#         node.next.prev = node.prev
    
#     def _add_to_head(self, node: Node) -> None:
#         """
#         Add a node right AFTER the head (most recently used position).
        
#         Time Complexity: O(1)
#         """
#         node.prev = self.head
#         node.next = self.head.next
#         self.head.next.prev = node
#         self.head.next = node
    
#     def _move_to_head(self, node: Node) -> None:
#         """
#         Move an existing node to the head (mark as most recently used).
        
#         Time Complexity: O(1)
#         """
#         self._remove(node)
#         self._add_to_head(node)
    
#     def get(self, key: int) -> int:
#         """
#         Return the value of the key if it exists, otherwise return -1.
        
#         Time Complexity: O(1)
#         """
#         if key not in self.cache:
#             return -1
        
#         node = self.cache[key]
#         self._move_to_head(node)  # Mark as most recently used
#         return node.value
    
#     def put(self, key: int, value: int) -> None:
#         """
#         Update the value of the key if it exists. Otherwise, add the key-value pair.
        
#         Time Complexity: O(1)
#         """
#         if key in self.cache:
#             # Update existing key
#             node = self.cache[key]
#             node.value = value
#             self._move_to_head(node)
#         else:
#             # Add new key
#             new_node = Node(key, value)
#             self.cache[key] = new_node
#             self._add_to_head(new_node)
    
#     def delete(self, key: int) -> bool:
#         """
#         Delete the key-value pair if the key exists and return true.
#         Otherwise, return false.
        
#         Time Complexity: O(1)
#         """
#         if key not in self.cache:
#             return False
        
#         # Get the node
#         node = self.cache[key]
        
#         # Remove from list
#         self._remove(node)
        
#         # Remove from HashMap
#         del self.cache[key]
        
#         return True
        
#         # If delete has a void return type:
#         # if key not in self.cache:
#         #     return  # Just return (do nothing)
#         # 
#         # node = self.cache[key]
#         # self._remove(node)
#         # del self.cache[key]
#         # No return statement needed (implicitly returns None)
    
#     def last(self) -> int:
#         """
#         Return the value of the most recently used entry if at least one entry exists.
#         Otherwise, return -1.
        
#         Time Complexity: O(1)
        
#         Note: Based on the example, last() returns the MRU value (head.next),
#         not the LRU value despite the confusing name.
#         """
#         # Check if cache is empty
#         if self.head.next == self.tail:
#             return -1
        
#         # Return the most recently used value (after head)
#         return self.head.next.value


# LRU Cache: Specific Data Type Example (Add to Tail Version)

# Problem Statement
# Design an LRU Cache that stores User objects with the following requirements:

# Key: User ID (integer)
# Value: User object containing:

# user_id: int
# name: str
# email: str
# age: int

# Implement all standard LRU operations plus the ability to:

# 1. Update user information
# 2. Get user by ID
# 3. Delete user
# 4. Get most recently accessed user

# class Node:
#     """Doubly linked list node that stores user information."""
    
#     def __init__(self, user_id: int, name: str, email: str, age: int):
#         self.user_id = user_id
#         self.name = name
#         self.email = email
#         self.age = age
#         self.prev = None
#         self.next = None
    
#     def __repr__(self):
#         """
#         Detailed representation - shows all node data.
        
#         Usage: repr(node), print([node]), or print({node})
#         Note: Cannot use print(node) directly - that calls __str__ instead
        
#         Example: Node(id=101, name='Alice', email='alice@email.com', age=30)
        
#         Optional: This method is NOT required for interviews - can be removed to save time.
#         Helpful for debugging but not essential for core LRU cache functionality.
#         """
#         return f"Node(id={self.user_id}, name='{self.name}', email='{self.email}', age={self.age})"
    
#     def __str__(self):
#         """
#         Simple representation - just name and email.
        
#         Usage: print(node), str(node), or f"{node}"
        
#         Example: Alice (alice@email.com)
        
#         Optional: This method is NOT required for interviews - can be removed to save time.
#         Helpful for debugging but not essential for core LRU cache functionality.
#         """
#         return f"{self.name} ({self.email})"


# class UserLRUCache:
#     """
#     LRU Cache for storing user information directly in nodes.
#     Design where MRU is at the TAIL end.
    
#     List Structure:
#         Head (dummy) <-> [LRU] <-> ... <-> [MRU] <-> Tail (dummy)
#         - Head.next = Least Recently Used user
#         - Tail.prev = Most Recently Used user
    
#     Time Complexity:
#         - get_user(user_id): O(1)
#         - add_user(user_id, name, email, age): O(1)
#         - update_user(user_id, **kwargs): O(1)
#         - delete_user(user_id): O(1)
#         - get_most_recent_user(): O(1)
#         - get_least_recent_user(): O(1)
    
#     Space Complexity: O(n) where n is the number of users
#     """
    
#     def __init__(self, capacity: int):
#         """
#         Initialize the User LRU cache with given capacity.
        
#         Args:
#             capacity: Maximum number of users the cache can hold
#         """
#         if capacity <= 0:
#             raise ValueError("Capacity must be greater than 0")

#         self.capacity = capacity
#         self.cache = {}  # HashMap: user_id -> Node
        
#         # Create dummy head and tail nodes with placeholder values
#         self.head = Node(-1, "", "", -1)  # Dummy head
#         self.tail = Node(-1, "", "", -1)  # Dummy tail
        
#         # Initially empty: Head <-> Tail
#         self.head.next = self.tail
#         self.tail.prev = self.head
    
#     def _remove(self, node: Node) -> None:
#         """
#         Remove a node from the doubly linked list.
        
#         Time Complexity: O(1)
        
#         Args:
#             node: Node to remove from the list
#         """
#         node.prev.next = node.next
#         node.next.prev = node.prev
    
#     def _add_to_tail(self, node: Node) -> None:
#         """
#         Add a node right BEFORE the tail (most recently used position).
        
#         Time Complexity: O(1)
        
#         Args:
#             node: Node to add before tail (MRU position)
#         """
#         node.next = self.tail
#         node.prev = self.tail.prev
#         self.tail.prev.next = node
#         self.tail.prev = node
    
#     def _move_to_tail(self, node: Node) -> None:
#         """
#         Move an existing node to the tail (mark as most recently used).
        
#         Time Complexity: O(1)
        
#         Args:
#             node: Node to move to the back (MRU position)
#         """
#         self._remove(node)
#         self._add_to_tail(node)
    
#     def get_user(self, user_id: int) -> Node:
#         """
#         Get a user by ID and mark as most recently used.
        
#         Time Complexity: O(1)
        
#         Args:
#             user_id: The user ID to look up
            
#         Returns:
#             Node object containing user data if found, None otherwise
#         """

#         if user_id is None:
#             raise ValueError("user_id cannot be None")

#         if user_id not in self.cache:
#             return None
        
#         node = self.cache[user_id]
#         self._move_to_tail(node)  # Mark as most recently used
#         return node
    
#     def add_user(self, user_id: int, name: str, email: str, age: int) -> None:
#         """
#         Add a new user to the cache or update existing user.
#         If at capacity, evict the least recently used user.
        
#         Time Complexity: O(1)
        
#         Args:
#             user_id: Unique user identifier
#             name: User's name
#             email: User's email address
#             age: User's age
#         """

#         if user_id is None:
#             raise ValueError("user_id cannot be None")
#         if not name or not email:
#             raise ValueError("name and email cannot be empty")
#         if age < 0:
#             raise ValueError("age cannot be negative")

#         if user_id in self.cache:
#             # Update existing user - use direct update instead of calling update_user()
#             # Reason: add_user() requires ALL fields (name, email, age are mandatory)
#             #         update_user() allows partial updates (fields are optional with None checks)
#             # Example: add_user(101, "Alice", "alice@email.com", 30) - full update
#             #          update_user(101, age=31) - partial update (only age)
#             # Direct assignment is more efficient - avoids 3 unnecessary None checks
#             node = self.cache[user_id]
#             node.name = name
#             node.email = email
#             node.age = age
#             self._move_to_tail(node)
#         else:
#             # Add new user
#             new_node = Node(user_id, name, email, age)
#             self.cache[user_id] = new_node
#             self._add_to_tail(new_node)
            
#             # Check if we've exceeded capacity
#             if len(self.cache) > self.capacity:
#             # Evict the least recently used user
#             # Must capture reference BEFORE _remove(): that call rewires head.next to the
#             # next node, so accessing self.head.next afterwards returns the wrong node.
#             #
#             # Without storing lru_node first:
#             #   BEFORE: head <-> [Alice/LRU] <-> [Bob] <-> [Charlie/MRU] <-> tail
#             #                         ↑
#             #                    head.next = Alice
#             #
#             #   self._remove(self.head.next)  → removes Alice
#             #
#             #   AFTER:  head <-> [Bob] <-> [Charlie/MRU] <-> tail
#             #                       ↑
#             #                  head.next = Bob now!
#             #
#             #   del self.cache[self.head.next.user_id]  → deletes Bob, not Alice! ❌
#             #   print(self.head.next)                   → prints Bob, not Alice!  ❌
#             #
#             #   RESULT: Alice removed from list but still in cache (memory leak!)
#             #           Bob deleted from cache but still in list (dangling reference!)
#             lru_node = self.head.next         # Store reference BEFORE any modifications
#             self._remove(lru_node)            # Remove from list
#             del self.cache[lru_node.user_id]  # Remove from HashMap
#             print(f"Evicted user: {lru_node}")  # __repr__ on Node formats the output

#     def update_user(self, user_id: int, name: str = None, email: str = None, age: int = None) -> bool:
#         """
#         Update specific fields of a user and mark as most recently used.
        
#         Time Complexity: O(1)
        
#         Args:
#             user_id: The user ID to update
#             name: New name (optional)
#             email: New email (optional)
#             age: New age (optional)
            
#         Returns:
#             True if user was found and updated, False otherwise
#         """

#         if user_id is None:
#             raise ValueError("user_id cannot be None")
#         if age is not None and age < 0:
#             raise ValueError("age cannot be negative")
#         if name is not None and not name:
#             raise ValueError("name cannot be empty string")
#         if email is not None and not email:
#             raise ValueError("email cannot be empty string")

#         if user_id not in self.cache:
#             return False
        
#         node = self.cache[user_id]
        
#         # Update only the specified fields
#         if name is not None:
#             node.name = name
#         if email is not None:
#             node.email = email
#         if age is not None:
#             node.age = age
        
#         self._move_to_tail(node)  # Mark as most recently used
#         return True
    
#     def delete_user(self, user_id: int) -> bool:
#         """
#         Delete a user from the cache.
        
#         Time Complexity: O(1)
        
#         Args:
#             user_id: The user ID to delete
            
#         Returns:
#             True if user was found and deleted, False otherwise
#         """

#         if user_id is None:
#             raise ValueError("user_id cannot be None")

#         if user_id not in self.cache:
#             return False
        
#         node = self.cache[user_id]
#         self._remove(node)
#         del self.cache[user_id]
#         return True
    
#     def get_most_recent_user(self) -> Node:
#         """
#         Get the most recently accessed user without updating access time.
        
#         Time Complexity: O(1)
        
#         Returns:
#             Node object if cache is non-empty, None otherwise
#         """
#         if self.head.next == self.tail:
#             return None
        
#         return self.tail.prev
    
#     def get_least_recent_user(self) -> Node:
#         """
#         Get the least recently accessed user without updating access time.
        
#         Time Complexity: O(1)
        
#         Returns:
#             Node object if cache is non-empty, None otherwise
#         """
#         if self.head.next == self.tail:
#             return None
        
#         return self.head.next
    
#     def get_all_users(self) -> list:
#         """
#         Get all users in order from least to most recently used.
        
#         Time Complexity: O(n)
        
#         Returns:
#             List of Node objects ordered from LRU to MRU
#         """
#         users = []
#         current = self.head.next
        
#         while current != self.tail:
#             users.append(current)
#             current = current.next
        
#         return users
    
#     def size(self) -> int:
#         """Return the number of users in the cache."""
#         return len(self.cache)
    
#     def is_empty(self) -> bool:
#         """Check if the cache is empty."""
#         return len(self.cache) == 0
    
#     def clear(self) -> None:
#         """Remove all users from the cache."""
#         self.cache.clear()
#         self.head.next = self.tail
#         self.tail.prev = self.head


# # Initialize cache with capacity 3
# cache = UserLRUCache(3)
# # head <-> tail

# cache.add_user(101, "Alice", "alice@email.com", 25)
# cache.add_user(102, "Bob", "bob@email.com", 30)
# cache.add_user(103, "Charlie", "charlie@email.com", 35)
# # head <-> [Alice] <-> [Bob] <-> [Charlie] <-> tail
# #            ↑ LRU                               ↑ MRU

# cache.get_least_recent_user()  # → Alice (no order change)
# cache.get_most_recent_user()   # → Charlie (no order change)
# cache.get_all_users()          # → [Alice, Bob, Charlie]

# cache.get_user(101)            # Alice accessed → moves to tail
# # head <-> [Bob] <-> [Charlie] <-> [Alice] <-> tail

# cache.add_user(104, "Diana", "diana@email.com", 28)  # over capacity → evict Bob
# # head <-> [Charlie] <-> [Alice] <-> [Diana] <-> tail

# cache.update_user(103, age=36) # Charlie accessed → moves to tail
# # head <-> [Alice] <-> [Diana] <-> [Charlie] <-> tail

# cache.add_user(101, "Alice", "alice@gmail.com", 26)  # existing key → update + move to tail
# # head <-> [Diana] <-> [Charlie] <-> [Alice] <-> tail

# cache.delete_user(104)         # explicit delete, no eviction logic
# # head <-> [Charlie] <-> [Alice] <-> tail

# cache.add_user(105, "Eve", "eve@email.com", 22)  # under capacity → no eviction
# # head <-> [Charlie] <-> [Alice] <-> [Eve] <-> tail

# cache.get_all_users()          # → [Charlie, Alice, Eve]
# cache.get_least_recent_user()  # → Charlie
# cache.get_most_recent_user()   # → Eve

# # Final: cache = {103: Charlie, 101: Alice, 105: Eve}