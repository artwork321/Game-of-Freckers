from queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()

        # insertion_order was used to experiment with different expansion orders for nodes with equal f(n)
        self.insertion_order = 0 

    def put(self, item):
        """Insert item with a given priority, preserving insertion order for ties."""
        super().put(item)
        # self.insertion_order += 1

    def get(self):
        """Retrieve the next item while maintaining stability for same-priority items."""
        return super().get()