from queue import PriorityQueue

class StablePriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        self.insertion_order = 0
        self.max_nodes = 0

    def put(self, item):
        """Insert item with a given priority, preserving insertion order for ties."""
        super().put((item.est_total_cost, self.insertion_order, item))
        self.insertion_order += 1

    def get(self):
        """Retrieve the next item while maintaining stability for same-priority items."""
        return super().get()[2]  # Extract only the item