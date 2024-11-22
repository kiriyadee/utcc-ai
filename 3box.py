# from collections import deque

# from graphviz import Digraph

# # Define the initial state and goal state
# initial_state = {
#     "A": "floor",
#     "B": "floor",
#     "C": "B"
# }

# goal_state = {
#     "A": "B",
#     "B": "C",
#     "C": "floor"
# }

# # Function to check if current state is the goal state
# def is_goal(state):
#     return state == goal_state

# # Function to get possible moves
# def get_possible_moves(state):
#     moves = []
#     for block, position in state.items():
#         if position == "floor" or all(state[other] != block for other in state):
#             # Generate new states by moving the block
#             for new_position in ["floor"] + list(state.keys()):
#                 if new_position != block and new_position != position:
#                     new_state = state.copy()
#                     new_state[block] = new_position
#                     moves.append(new_state)
#     return moves

# # Function to visualize with Graphviz using clusters
# def visualize_tree_with_clusters(tree, algorithm_name):
#     dot = Digraph(format='png')
#     dot.attr(rankdir='TB')
    
#     for parent, children in tree.items():
#         parent_dict = dict(parent)  
#         parent_label = "\n".join([f"{k}: {v}" for k, v in parent_dict.items()]) 
#         dot.node(str(hash(parent)), parent_label, shape="box")
        
#         for child in children:
#             # Convert the child tuple back to a dictionary for labeling
#             child_dict = dict(child) 
#             child_label = "\n".join([f"{k}: {v}" for k, v in child_dict.items()])
#             dot.node(str(hash(child)), child_label, shape="box")
#             dot.edge(str(hash(parent)), str(hash(child)))
    
#     dot.render(f"{algorithm_name}_tree", view=True)

# # DFS implementation with tree construction and clusters
# def dfs_with_tree_and_clusters(start):
#     stack = [(start, [start])]
#     visited = set()
#     tree = {}
    
#     while stack:
#         current_state, path = stack.pop()
#         state_tuple = tuple(sorted(current_state.items()))  # Ensure the tuple is hashable by sorting the items
        
#         if state_tuple in visited:
#             continue
        
#         visited.add(state_tuple)
#         # Use the tuple as the key in the tree
#         tree[state_tuple] = []
        
#         if is_goal(current_state):
#             visualize_tree_with_clusters(tree, "DFS")
#             return path
        
#         for next_state in get_possible_moves(current_state):
#             stack.append((next_state, path + [next_state]))
#             tree[state_tuple].append(tuple(sorted(next_state.items())))
    
#     return None

# # BFS implementation with tree construction and clusters
# def bfs_with_tree_and_clusters(start):
#     queue = deque([(start, [start])])
#     visited = set()
#     tree = {}
    
#     while queue:
#         current_state, path = queue.popleft()
#         state_tuple = tuple(sorted(current_state.items()))  # Ensure the tuple is hashable by sorting the items
        
#         if state_tuple in visited:
#             continue
        
#         visited.add(state_tuple)
#         # Use the tuple as the key in the tree
#         tree[state_tuple] = []
        
#         if is_goal(current_state):
#             visualize_tree_with_clusters(tree, "BFS")
#             return path
        
#         for next_state in get_possible_moves(current_state):
#             queue.append((next_state, path + [next_state]))
#             tree[state_tuple].append(tuple(sorted(next_state.items())))
    
#     return None

# # Run the algorithms with visualization and clusters
# print("DFS Path:")
# dfs_path = dfs_with_tree_and_clusters(initial_state)
# if dfs_path:
#     for step in dfs_path:
#         print(step)
# else:
#     print("No path found using DFS.")

# print("\nBFS Path:")
# bfs_path = bfs_with_tree_and_clusters(initial_state)
# if bfs_path:
#     for step in bfs_path:
#         print(step)
# else:
#     print("No path found using BFS.")

from collections import deque

from graphviz import Digraph

# Define the initial state and goal state
initial_state = {
    "A": "floor",
    "B": "floor",
    "C": "B"
}

goal_state = {
    "A": "B",
    "B": "C",
    "C": "floor"
}

# Function to check if current state is the goal state
def is_goal(state):
    return state == goal_state

# Function to get possible moves
def get_possible_moves(state):
    moves = []
    for block, position in state.items():
        if position == "floor" or all(state[other] != block for other in state):
            # Generate new states by moving the block
            for new_position in ["floor"] + list(state.keys()):
                if new_position != block and new_position != position:
                    new_state = state.copy()
                    new_state[block] = new_position
                    moves.append(new_state)
    return moves

# Function to visualize with Graphviz using clusters
def visualize_tree_with_clusters(tree, algorithm_name, start, target):
    dot = Digraph(format='png')
    dot.attr(rankdir='TB')
    dot.node('start', start, shape="box")
    dot.node('target', target, shape="box")
    
    for parent, children in tree.items():
        parent_dict = dict(parent)  
        parent_label = "\n".join([f"{k}: {v}" for k, v in parent_dict.items()]) 
        dot.node(str(hash(parent)), parent_label, shape="box")
        
        for child in children:
            # Convert the child tuple back to a dictionary for labeling
            child_dict = dict(child) 
            child_label = "\n".join([f"{k}: {v}" for k, v in child_dict.items()])
            dot.node(str(hash(child)), child_label, shape="box")
            dot.edge(str(hash(parent)), str(hash(child)))
    
    dot.render(f"{algorithm_name}_tree", view=True)

# DFS implementation with tree construction and clusters
def dfs_with_tree_and_clusters(start):
    stack = [(start, [start])]
    visited = set()
    tree = {}
    clusters = {}
    
    while stack:
        current_state, path = stack.pop()
        state_tuple = tuple(sorted(current_state.items()))  # Ensure the tuple is hashable by sorting the items
        
        if state_tuple in visited:
            continue
        
        visited.add(state_tuple)
        # Use the tuple as the key in the tree
        tree[state_tuple] = []
        if is_goal(current_state):
            visualize_tree_with_clusters(tree, "DFS", start, current_state)
            return path
        
        for next_state in get_possible_moves(current_state):
            stack.append((next_state, path + [next_state]))
            tree[state_tuple].append(tuple(sorted(next_state.items())))
            # Assign clusters based on the block positions
            cluster_key = tuple(sorted([block for block, position in next_state.items() if position != "floor"]))
            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(tuple(sorted(next_state.items())))
    
    return None

# BFS implementation with tree construction and clusters
def bfs_with_tree_and_clusters(start):
    queue = deque([(start, [start])])
    visited = set()
    tree = {}
    clusters = {}
    
    while queue:
        current_state, path = queue.popleft()
        state_tuple = tuple(sorted(current_state.items()))  # Ensure the tuple is hashable by sorting the items
        
        if state_tuple in visited:
            continue
        
        visited.add(state_tuple)
        # Use the tuple as the key in the tree
        tree[state_tuple] = []
        if is_goal(current_state):
            visualize_tree_with_clusters(tree, "BFS", start)
            return path
        
        for next_state in get_possible_moves(current_state):
            queue.append((next_state, path + [next_state]))
            tree[state_tuple].append(tuple(sorted(next_state.items())))
            # Assign clusters based on the block positions
            cluster_key = tuple(sorted([block for block, position in next_state.items() if position != "floor"]))
            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(tuple(sorted(next_state.items())))
    
    return None

# Run the algorithms with visualization and clusters
print("DFS Path:")
dfs_path = dfs_with_tree_and_clusters(initial_state)
if dfs_path:
    for step in dfs_path:
        print(step)
else:
    print("No path found using DFS.")

print("\nBFS Path:")
bfs_path = bfs_with_tree_and_clusters(initial_state)
if bfs_path:
    for step in bfs_path:
        print(step)
else:
    print("No path found using BFS.")
