import time
import os
import psutil

class PerformanceTracker:
    """Utility class to measure execution time, node count, and memory usage for a search algorithm."""
    
    def __init__(self):
        self.nodes_explored = 0
        self.start_time = 0
        self.process = psutil.Process(os.getpid()) 

    def _get_current_memory_usage_mb(self):
        """Returns the current process's Resident Set Size (RSS) in MB."""
        
        # Resident Set Size (RSS) is the non-swapped physical memory a process is using.
        return self.process.memory_info().rss / (1024 * 1024)

    def start_timer(self):
        """Resets the tracker and starts the timer and memory tracking."""
        self.nodes_explored = 0
        self.start_time = time.time() * 1000 # Time in milliseconds
        
        # We don't need to store start_mem_rss here unless we want to calculate the delta (change)
        # We will instead calculate the final memory usage in stop_timer.
        
    def increment_node(self):
        """Increments the count every time a game state is evaluated (a node is visited)."""
        self.nodes_explored += 1
        
    def stop_timer(self):
        """
        Stops the timer and returns the metrics: 
        (elapsed_time_ms, nodes_explored, final_memory_MB).
        """
        end_time = time.time() * 1000
        elapsed = end_time - self.start_time
        
        # Get the memory usage at the end of the search.
        final_mem_usage = self._get_current_memory_usage_mb()
        
        # Return the three standard metrics: time, nodes, and final memory usage.
        return elapsed, self.nodes_explored, final_mem_usage