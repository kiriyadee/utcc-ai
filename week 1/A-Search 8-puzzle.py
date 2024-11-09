from queue import PriorityQueue

from graphviz import Digraph

# Define start and goal states
start_state = ((1, 2, 3), (8, 5, 6), (4, 7, 0))
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

# Helper functions
def find_blank_position(state):
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value == 0:
                return i, j

def is_goal(state):
    return state == goal_state

def get_neighbors(state):
    neighbors = []
    blank_row, blank_col = find_blank_position(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in state]
            new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
            neighbors.append(tuple(tuple(row) for row in new_state))
    
    return neighbors

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                target_row, target_col = divmod(value - 1, 3)
                distance += abs(target_row - i) + abs(target_col - j)
    return distance

# A* search with diagram generation
def a_star_search_with_diagram(start_state):
    open_set = PriorityQueue()
    open_set.put((0, start_state))
    came_from = {start_state: None}
    cost_so_far = {start_state: 0}

    # Initialize the graph
    diagram = Digraph()
    h_score = manhattan_distance(start_state)
    diagram.node(str(start_state), label=format_state_with_scores(start_state, 0, h_score), shape='box')

    while not open_set.empty():
        _, current = open_set.get()

        if is_goal(current):
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, diagram, cost_so_far

        for neighbor in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heuristic = manhattan_distance(neighbor)
                priority = new_cost + heuristic
                open_set.put((priority, neighbor))
                came_from[neighbor] = current

                # Add nodes and edges to the diagram with g and h scores
                diagram.node(str(neighbor), label=format_state_with_scores(neighbor, new_cost, heuristic), shape='box')
                diagram.edge(str(current), str(neighbor), label=f"g+h={new_cost}+{heuristic}")

    return None, diagram, {}  # No solution found

def format_state_with_scores(state, g_score, h_score):
    """Format the 3x3 state with g and h scores as a string for visualization."""
    state_str = "\n".join(" ".join(str(x) if x != 0 else " " for x in row) for row in state)
    return f"{state_str}\ng={g_score}, h={h_score}"

# Solve and display the diagram
solution_path, diagram, cost_so_far = a_star_search_with_diagram(start_state)
if solution_path:
    print("Solution found in", len(solution_path) - 1, "moves:")
    for step in solution_path:
        # Get the g_score from the cost_so_far dictionary that was returned with the solution
        g_score = cost_so_far[step]
        h_score = manhattan_distance(step)
        for row in step:
            print(row)
        print(f"g = {g_score}, h = {h_score}")
        print("----")
    
    # Render and display the diagram with g and h scores
    diagram.render('8_puzzle_solution_with_g_h_scores', format='png', view=True)
else:
    print("No solution found.")
