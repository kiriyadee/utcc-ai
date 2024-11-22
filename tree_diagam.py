from heapq import heappop, heappush

import graphviz

# Initial and goal states
initial_state = (['A', 'B', 'C'], [], [])
goal_state = ([], [], ['A', 'B', 'C'])

# Function to generate possible moves
def generate_moves(state):
    moves = []
    for i, stack in enumerate(state):
        if stack:  # if stack is not empty
            block = stack[-1]
            for j in range(len(state)):
                if i != j:  # move to a different stack
                    new_state = [list(s) for s in state]  # deep copy
                    new_state[i].pop()  # remove block from stack i
                    new_state[j].append(block)  # add block to stack j
                    moves.append(tuple(map(tuple, new_state)))
    return moves

# Heuristic function
def heuristic(state):
    score = 0
    target_stack = goal_state[2]
    for i, stack in enumerate(state):
        if i == 2:
            # Calculate misplaced blocks in the target stack
            for j, block in enumerate(stack):
                if j < len(target_stack) and block != target_stack[j]:
                    score += 1
        else:
            # All blocks in non-target stacks are considered misplaced
            score += len(stack)
    return score

# Function to create node label
def create_node_label(state):
    return f"Stack1: {state[0]}\nStack2: {state[1]}\nStack3: {state[2]}"

# A* Search function with visualization
def a_star_search(initial_state, goal_state):
    # Create a new directed graph
    dot = graphviz.Digraph(comment='A* Search Tree')
    dot.attr(rankdir='LR')
    
    open_list = []
    heappush(open_list, (0, 0, initial_state, []))  # (f, counter, state, path)
    visited = set()
    visited.add(initial_state)
    counter = 1  # Counter for unique comparison
    
    # Add initial state to graph
    dot.node(str(hash(initial_state)), create_node_label(initial_state))
    
    while open_list:
        f, _, current_state, path = heappop(open_list)
        
        # Check if we reached the goal state
        if current_state == goal_state:
            final_path = path + [current_state]
            # Highlight solution path
            for i in range(len(final_path)-1):
                dot.edge(str(hash(final_path[i])), str(hash(final_path[i+1])), color='red', penwidth='2.0')
            # Save the graph
            dot.render('search_tree', view=True, format='png')
            return final_path
            
        # Generate new moves and explore them
        for move in generate_moves(current_state):
            if move not in visited:
                visited.add(move)
                g = len(path) + 1
                h = heuristic(move)
                heappush(open_list, (g + h, counter, move, path + [current_state]))
                counter += 1
                
                # Add node and edge to graph
                dot.node(str(hash(move)), create_node_label(move))
                dot.edge(str(hash(current_state)), str(hash(move)))

    # If no solution found, still save the graph
    dot.render('search_tree', view=True, format='png')
    return None  # no solution found

# Run A* Search to find the solution path
solution_path = a_star_search(initial_state, goal_state)

# Display the solution path
if solution_path:
    print("Solution found:")
    for step, state in enumerate(solution_path):
        print(f"Step {step}: {state}")
else:
    print("No solution found.")
