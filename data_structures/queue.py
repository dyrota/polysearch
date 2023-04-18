class Queue:
    """
    A basic implementation of a Queue data structure, which follows the First-In-First-Out (FIFO) principle.
    Elements are added to the end of the queue and removed from the front.
    """
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """
        Adds an item to the end of the queue.

        :param item: The item to be added.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Removes and returns the item at the front of the queue.

        :return: The item at the front of the queue.
        """
        return self.items.pop(0)

    def is_empty(self):
        """
        Checks if the queue is empty.

        :return: True if the queue is empty, False otherwise.
        """
        return len(self.items) == 0

    def size(self):
        """
        Returns the number of items in the queue.

        :return: The size of the queue.
        """
        return len(self.items)
