import heapq

class PriorityQueue:
    """
    A basic implementation of a Priority Queue data structure, which assigns priorities to its elements
    and retrieves elements in order of their priorities. Elements with higher priority (lower priority value)
    are dequeued before elements with lower priority (higher priority value).
    """
    def __init__(self):
        self.items = []

    def push(self, item, priority):
        """
        Adds an item to the priority queue with the given priority.

        :param item: The item to be added.
        :param priority: The priority value for the item.
        """
        heapq.heappush(self.items, (priority, item))

    def pop(self):
        """
        Removes and returns the item with the highest priority (lowest priority value) from the priority queue.

        :return: A tuple containing the priority and the item with the highest priority.
        """
        priority, item = heapq.heappop(self.items)
        return priority, item

    def is_empty(self):
        """
        Checks if the priority queue is empty.

        :return: True if the priority queue is empty, False otherwise.
        """
        return len(self.items) == 0

    def size(self):
        """
        Returns the number of items in the priority queue.

        :return: The size of the priority queue.
        """
        return len(self.items)
