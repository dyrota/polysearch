import heapq

class PriorityQueue:
    def __init__(self):
        self.items = []

    def push(self, item, priority):
        heapq.heappush(self.items, (priority, item))

    def pop(self):
        return heapq.heappop(self.items)[1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
