class Stack:
    """
    A basic implementation of a Stack data structure, which follows the Last-In-First-Out (LIFO) principle.
    Elements are added to the top of the stack and removed from the top as well.
    """
    def __init__(self):
        self.items = []

    def push(self, item):
        """
        Adds an item to the top of the stack.

        :param item: The item to be added.
        """
        self.items.append(item)

    def pop(self):
        """
        Removes and returns the item at the top of the stack.

        :return: The item at the top of the stack.
        """
        return self.items.pop()

    def is_empty(self):
        """
        Checks if the stack is empty.

        :return: True if the stack is empty, False otherwise.
        """
        return len(self.items) == 0

    def size(self):
        """
        Returns the number of items in the stack.

        :return: The size of the stack.
        """
        return len(self.items)
