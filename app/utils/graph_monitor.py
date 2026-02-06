import networkx as nx

class GraphMonitor:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_transaction(self, sender, receiver, amount):
        self.G.add_edge(sender, receiver, amount=amount)
        
        # Detect if this creates a cycle (Money coming back to start)
        try:
            cycle = nx.find_cycle(self.G, source=sender)
            return True, cycle # Laundering detected!
        except:
            return False, None