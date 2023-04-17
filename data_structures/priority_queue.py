import heapq

class PriorityQueue:
    def __init__(self):
        self.items = []

    def push(self, item, priority):
        heapq.heappush(self.items, (priority, item))

    def pop(self):
        priority, item = heapq.heappop(self.items)
        return priority, item

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
