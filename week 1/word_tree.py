from queue import PriorityQueue, Queue

from graphviz import Digraph


class BlockWorld:
    def __init__(self):
        self.initial_state = ['A', 'B', 'C']  # Initial state [B, C, A]
        self.goal_state = ['C', 'B', 'A']     # Goal state [A, B, C]
        self.start_block = 'A'  # Starting block to move
        self.goal_block = 'C'   # Target block position
        print("Starting block:", self.start_block)
        print("Goal block:", self.goal_block)

    def get_possible_moves(self, state):
        moves = []
        # Try moving each block to each position
        for i in range(len(state)):
            for j in range(len(state)):
                if i != j:
                    new_state = state.copy()
                    # Move block from position i to j
                    block = new_state.pop(i)
                    new_state.insert(j, block)
                    moves.append(new_state)
        return moves

    def heuristic(self, state):
        # Count number of blocks in wrong position
        return sum(1 for i in range(len(state)) if state[i] != self.goal_state[i])

    def depth_first_search(self):
        print("Starting DFS from block", self.start_block)
        # Initialize stack with initial state
        stack = [(self.initial_state, [], 0)]  # Added depth g=0
        
        # Keep track of visited states
        visited = set()
        
        # Create digraph for visualization
        dot = Digraph(comment='Block World DFS Tree')
        dot.attr(rankdir='TB')
        
        while stack:
            current_state, path, g = stack.pop()
            current_state_str = str(current_state)
            
            # Add node with g, h and f=g+h values
            h = self.heuristic(current_state)
            f = g + h
            node_label = f"{current_state}\ng={g}, h={h}, f={f}"
            dot.node(current_state_str, node_label)
            
            if current_state == self.goal_state:
                print("Reached goal block", self.goal_block)
                # Save the graph
                dot.render('block_world_tree_dfs', format='png', cleanup=True)
                return path + [current_state]
            
            if current_state_str not in visited:
                visited.add(current_state_str)
                
                # Generate possible moves
                for next_state in self.get_possible_moves(current_state):
                    next_state_str = str(next_state)
                    if next_state_str not in visited:
                        next_g = g + 1  # Increment depth/cost
                        stack.append((next_state, path + [current_state], next_g))
                        
                        # Add node and edge with g, h and f values
                        h = self.heuristic(next_state)
                        f = next_g + h
                        node_label = f"{next_state}\ng={next_g}, h={h}, f={f}"
                        dot.node(next_state_str, node_label)
                        dot.edge(current_state_str, next_state_str)
        
        print("Could not reach goal block", self.goal_block)
        return None  # No solution found

    def best_first_search(self):
        print("Starting Best First Search from block", self.start_block)
        # Initialize priority queue with initial state
        frontier = PriorityQueue()
        frontier.put((self.heuristic(self.initial_state), self.initial_state, 0))  # Added g=0
        
        # Keep track of visited states and paths
        visited = set()
        came_from = {str(self.initial_state): None}
        
        # Create digraph for visualization
        dot = Digraph(comment='Block World Best First Search Tree')
        dot.attr(rankdir='TB')
        
        while not frontier.empty():
            _, current_state, g = frontier.get()
            current_state_str = str(current_state)
            
            # Add node with g, h and f values
            h = self.heuristic(current_state)
            f = g + h
            node_label = f"{current_state}\ng={g}, h={h}, f={f}"
            dot.node(current_state_str, node_label)
            
            if current_state == self.goal_state:
                print("Reached goal block", self.goal_block)
                # Reconstruct path
                path = []
                while current_state is not None:
                    path.append(current_state)
                    current_state = came_from[str(current_state)]
                
                # Save the graph
                dot.render('block_world_tree', format='png', cleanup=True)
                
                return path[::-1]  # Reverse path to get from start to goal
            
            visited.add(current_state_str)
            
            # Generate possible moves
            for next_state in self.get_possible_moves(current_state):
                next_state_str = str(next_state)
                if next_state_str not in visited:
                    next_g = g + 1  # Increment depth/cost
                    h = self.heuristic(next_state)
                    f = next_g + h
                    frontier.put((f, next_state, next_g))  # Use f as priority
                    came_from[next_state_str] = current_state
                    
                    # Add node and edge with g, h and f values
                    node_label = f"{next_state}\ng={next_g}, h={h}, f={f}"
                    dot.node(next_state_str, node_label)
                    dot.edge(current_state_str, next_state_str)
        
        print("Could not reach goal block", self.goal_block)
        return None  # No solution found

def main():
    world = BlockWorld()
    print("Running Depth First Search:")
    solution_dfs = world.depth_first_search()
    
    if solution_dfs:
        print("DFS Solution found!")
        print("Path:")
        for i, state in enumerate(solution_dfs):
            print(f"Step {i}: {state}")
        print("\nDFS Tree diagram has been saved as 'block_world_tree_dfs.png'")
    else:
        print("No DFS solution found!")
        
    print("\nRunning Best First Search:")
    solution_bfs = world.best_first_search()
    
    if solution_bfs:
        print("Best First Search Solution found!")
        print("Path:")
        for i, state in enumerate(solution_bfs):
            print(f"Step {i}: {state}")
        print("\nBest First Search Tree diagram has been saved as 'block_world_tree.png'")
    else:
        print("No Best First Search solution found!")

if __name__ == "__main__":
    main()
