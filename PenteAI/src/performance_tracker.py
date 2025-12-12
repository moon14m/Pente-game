# --- src/performance_tracker.py ---
import time

class PerformanceTracker:
    """Utility class to measure execution time and node count for a search algorithm."""
    
    def __init__(self):
        self.nodes_explored = 0
        self.start_time = 0
        
    def start_timer(self):
        """Resets the tracker and starts the timer."""
        self.nodes_explored = 0
        self.start_time = time.time() * 1000 # Time in milliseconds
        
    def increment_node(self):
        """Increments the count every time a game state is evaluated (a node is visited)."""
        self.nodes_explored += 1
        
    def stop_timer(self):
        """Stops the timer and returns the metrics."""
        end_time = time.time() * 1000
        elapsed = end_time - self.start_time
        return elapsed, self.nodes_explored