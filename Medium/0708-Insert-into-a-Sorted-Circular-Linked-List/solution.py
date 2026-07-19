"""
LeetCode 708. Insert into a Sorted Circular Linked List
Difficulty: Medium
URL: https://leetcode.com/problems/insert-into-a-sorted-circular-linked-list/
"""

# Definition for a Node
class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


class Solution:
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        """
        Time Complexity:  O(n) - in the worst case we traverse every node
                           once before finding the insertion point or
                           completing a full lap back to head.
        Space Complexity: O(1) - only a constant number of pointers and
                           one new node are allocated, regardless of n.

        Key idea about the input:
        The list IS sorted, but only if you read it starting from the
        node with the MINIMUM value. e.g. ring 3 -> 4 -> 1 -> back to 3
        reads as ascending (1 -> 3 -> 4) only if you start at node 1.
        We are NOT guaranteed to be handed the minimum node - here we're
        handed node 3. So walking forward from head, one edge will look
        "out of order": the edge where the max wraps back to the min
        (here, 4 -> 1). That single seam is the thing this algorithm
        has to detect explicitly (Case 3 below) - everywhere else the
        list behaves like an ordinary sorted list.
        """

        # ---- Case 1: empty list ----
        # There's nothing to attach to, so the new node becomes a
        # circular list of one element: it points to itself.
        # Can't do Node(insertVal, node) in one line - node doesn't
        # exist yet while it's still being constructed, so we create
        # it first, then point next at itself.
        # Example: head=None, insertVal=1
        #   BEFORE: (empty)
        #   AFTER:  1 -> (back to 1)
        if not head:
            node = Node(insertVal)
            node.next = node
            return node

        # We use two pointers, prev and curr, representing a pair of
        # adjacent nodes. We slide this pair around the ring looking
        # for the correct gap to insert into.
        prev, curr = head, head.next

        # Why while True: we don't know in advance how many steps it
        # will take to find the right gap (Case 2), the wrap-around
        # seam (Case 3), or a full lap back to head (Case 4) - it
        # depends entirely on where in the ring we started. A
        # condition-based loop (e.g. "while curr != head") would exit
        # too early and skip checking the pair that includes head
        # itself.
        # Example: head=[1,3,4], insertVal=5 (should become new max,
        # sitting right before the wrap back to the min)
        #   Ring: 1 -> 3 -> 4 -> back to 1. The seam pair we need to
        #   check is prev=4, curr=1(=head).
        #   With "while curr != head": start prev=1,curr=3 -> advance
        #   -> prev=3,curr=4 -> advance -> now curr becomes 1, which
        #   IS head, so the loop condition "curr != head" is False and
        #   we exit BEFORE ever checking the pair prev=4,curr=1 - the
        #   exact pair where 5 belongs. We'd fall through the loop
        #   with no insertion point found and lose the only valid spot.
        #   "while True" with an internal break avoids this: it always
        #   evaluates the prev=4,curr=1 pair first, finds 5>=4 is
        #   True, and breaks correctly.
        while True:
            # ---- Case 2: normal ascending gap ----
            # If insertVal fits between prev and curr in the usual
            # sorted sense, this is our spot.
            # Example: prev=1, curr=3, insertVal=2 -> 1<=2<=3 True -> insert here
            #   BEFORE:  3 -> 4 -> 1 -> (back to 3)
            #   AFTER:   3 -> 4 -> 1 -> 2 -> (back to 3)
            #
            # We break here because prev and curr are now confirmed to
            # be the exact pair we want to splice between. There's no
            # need to keep searching once a valid gap is found - we
            # exit the loop with prev/curr pointing at the insertion
            # spot, and the splice happens right after the loop.
            if prev.val <= insertVal <= curr.val:
                break

            # ---- Case 3: wrap-around point (the "seam") ----
            # prev.val > curr.val can only happen at ONE place in a
            # sorted circular list: where the maximum value loops back
            # to the minimum value (e.g. ...4 -> 1... in ring [3,4,1]).
            # Anything bigger than the max, or smaller than the min,
            # belongs right here.
            # Example: prev=4 (max), curr=1 (min), insertVal=5
            #   -> is 5 >= 4? Yes -> insert here (new max)
            #   BEFORE:  3 -> 4 -> 1 -> (back to 3)
            #   AFTER:   3 -> 4 -> 5 -> 1 -> (back to 3)
            # Example: prev=4 (max), curr=1 (min), insertVal=0
            #   -> is 0 >= 4? No.  is 0 <= 1? Yes -> insert here (new min)
            #   BEFORE:  3 -> 4 -> 1 -> (back to 3)
            #   AFTER:   3 -> 4 -> 1 -> 0 -> (back to 3)
            #
            # We break here for the same reason as Case 2: prev and
            # curr now mark the correct insertion gap (this time it's
            # the special max-to-min seam, not an ordinary ascending
            # pair). Once confirmed, there's nothing left to search for.
            if prev.val > curr.val and (insertVal >= prev.val or insertVal <= curr.val):
                break

            # Neither case matched at this pair - slide the window forward.
            prev, curr = curr, curr.next

            # ---- Case 4: completed a full lap ----
            # Guards against an infinite loop. Fires when every node has
            # the same value (e.g. [3,3,3]), since neither Case 2 nor
            # Case 3 ever triggers (prev.val is never strictly greater
            # than curr.val when all values are equal). Once we're back
            # at head, just insert anywhere - still sorted since all
            # values are equal.
            # Example: ring 3 -> 3 -> 3 -> back to 3, insertVal=2
            #   BEFORE:  3 -> 3 -> 3 -> (back to 3)
            #   AFTER:   3 -> 2 -> 3 -> 3 -> (back to 3)
            #
            # We break here to stop the loop from spinning forever.
            # Without this check, a list where insertVal never satisfies
            # Case 2 or Case 3 (all-equal values) would cause prev/curr
            # to circle the ring endlessly. Breaking here forces
            # termination after exactly one full lap, and it's always
            # safe to insert right after prev at this point.
            #
            # Why AFTER the advance, not before: prev starts equal to
            # head, so checking "prev is head" before advancing would
            # be True on iteration 1 (before any real search) and
            # break immediately. Example: head=[3,4,1], insertVal=2 ->
            # checking before advance breaks instantly at prev=3,
            # inserting after 3 without ever checking the 1->3 gap
            # where 2 actually belongs. Checking after the advance
            # ensures "prev is head" only means "one full lap done".
            if prev is head:
                break

        # Splice new_node in between prev and curr.
        prev.next = Node(insertVal, curr)
        return head # or, return prev.next if we have to return the reference of the newly created node

# # ---- Test case: head=[3,4,1], insertVal=2 ----

# # Build the ring manually: 3 -> 4 -> 1 -> back to 3
# node3 = Node(3)
# node4 = Node(4)
# node1 = Node(1)

# node3.next = node4
# node4.next = node1
# node1.next = node3   # closes the circle back to the starting node

# # We hand the solution a reference to node3 (not necessarily the min)
# given_node = node3
# insert_val = 2

# solution = Solution()
# result_head = solution.insert(given_node, insert_val)

# # ---- Manually walk the result to see the values, starting at result_head ----
# print(result_head.val)              # 3
# print(result_head.next.val)         # 4
# print(result_head.next.next.val)    # 1
# print(result_head.next.next.next.val)          # 2 (the newly inserted node)
# print(result_head.next.next.next.next.val)      # 3 (confirms it wraps back)
# print(result_head.next.next.next.next is result_head)  # True -> confirms circularity
                 
# Write as a testcase

# def test_given_node_not_minimum(self):
#     # Build the ring inside-out: 3 -> 4 -> 1 -> back to 3.
#     # node3 must exist first since Node(1, node3) references it,
#     # then the whole chain is nested into node3.next in one line.
#     node3 = Node(3)
#     node3.next = Node(4, Node(1, node3))

#     s = Solution()

#     # Insert 2 into the ring, given a reference to node3 - which is
#     # NOT the minimum value in the list. This exercises the "given
#     # node may not be the smallest" property directly: the algorithm
#     # has to walk 3 -> 4 -> 1 -> 3 and find the wrap-around gap
#     # between 1 and 3 before it can place 2 correctly.
#     assert node3 is s.insert(node3, 2)  # must return the original node

#     # Walk the resulting ring node by node and check it now reads
#     # 3 -> 4 -> 1 -> 2 -> back to 3.
#     assert 3 == node3.val
#     assert 4 == node3.next.val
#     assert 1 == node3.next.next.val
#     assert 2 == node3.next.next.next.val          # newly inserted node
#     assert 3 == node3.next.next.next.next.val     # confirms it wraps back to node3
    