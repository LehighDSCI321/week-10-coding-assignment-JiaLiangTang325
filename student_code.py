from collections import deque

class SortableDigraph:
    """Base class providing basic graph structure and topological sort"""
    def __init__(self):
        self.adj = {}  # adjacency list
        
    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []
    
    def add_edge(self, u, v):
        """May be overridden in subclasses"""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append(v)
    
    def topsort(self):
        """Topological sort - assumed to be implemented"""
        visited = set()
        result = []
        
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in self.adj.get(node, []):
                visit(neighbor)
            result.append(node)
        
        for node in list(self.adj.keys()):
            visit(node)
        
        return result[::-1]


class TraversableDigraph(SortableDigraph):
    def dfs(self, start=None, visited=None):
        """Depth-first search traversal"""
        if start is None:
            start = next(iter(self.adj.keys())) if self.adj else None
        
        if start is None:
            return
        
        if visited is None:
            visited = set()
        
        if start in visited:
            return
        
        visited.add(start)
        yield start
        
        for neighbor in self.adj.get(start, []):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)
    
    def bfs(self, start=None):
        """Breadth-first search traversal using yield"""
        if not self.adj:
            return
        
        if start is None:
            start = next(iter(self.adj.keys()))
        
        visited = {start}
        queue = deque([start])
        
        while queue:
            node = queue.popleft()
            yield node
            
            for neighbor in self.adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


class DAG(TraversableDigraph):
    def add_edge(self, u, v):
        """Add edge while ensuring no cycles are created"""
        if self._has_path(v, u):
            raise ValueError(f"Adding edge ({u} -> {v}) would create a cycle")
        
        super().add_edge(u, v)
    
    def _has_path(self, start, end, visited=None):
        """Check if path exists from start to end"""
        if visited is None:
            visited = set()
        
        if start == end:
            return True
        
        visited.add(start)
        
        for neighbor in self.adj.get(start, []):
            if neighbor not in visited:
                if self._has_path(neighbor, end, visited):
                    return True
        
        return False


# Test code
if __name__ == "__main__":
    print("=== Testing TraversableDigraph ===")
    g = TraversableDigraph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    
    print("DFS:", list(g.dfs("A")))
    print("BFS:", list(g.bfs("A")))
    
    print("\n=== Testing DAG ===")
    dag = DAG()
    dag.add_edge("shirt", "tie")
    dag.add_edge("shirt", "belt")
    dag.add_edge("tie", "jacket")
    dag.add_edge("belt", "jacket")
    dag.add_edge("pants", "shoes")
    dag.add_edge("pants", "belt")
    dag.add_edge("socks", "shoes")
    
    print("Topological sort:", dag.topsort())
    
    try:
        dag.add_edge("jacket", "shirt")
        print("Error: Should have detected cycle!")
    except ValueError as e:
        print("Correctly detected cycle:", e)
