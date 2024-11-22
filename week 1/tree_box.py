from graphviz import Digraph


class Node:
    def __init__(self, state, g, h, moves):
        self.state = state    # สถานะของบล็อก
        self.g = g            # ค่า g (ระยะทางจากจุดเริ่มต้น)
        self.h = h            # ค่า h (การประเมินระยะทางถึงเป้าหมาย)
        self.f = g + h        # ค่า f (g + h)
        self.moves = moves    # การเคลื่อนไหวที่ใช้จนถึงโหนดนี้

def scoring_function(state):
    target_state = ('A', 'B', 'C')
    score = sum(1 for i in range(3) if state[i] == target_state[i])
    return 3 - score  # ยิ่งคะแนนมาก ยิ่งไกลจากเป้าหมาย

def generate_moves(node):
    state = node.state
    moves = []
    if state[0] != 'A':  # ย้าย A ไปวางที่ด้านบนสุด
        new_state = ('A', state[1], state[2])
        moves.append(Node(new_state, node.g + 1, scoring_function(new_state), node.moves + ["Move A to top"]))
    if state[1] != 'B':  # ย้าย B ไปวางที่ตำแหน่งกลาง
        new_state = (state[0], 'B', state[2])
        moves.append(Node(new_state, node.g + 1, scoring_function(new_state), node.moves + ["Move B to middle"]))
    if state[2] != 'C':  # ย้าย C ไปวางที่ด้านล่างสุด
        new_state = (state[0], state[1], 'C')
        moves.append(Node(new_state, node.g + 1, scoring_function(new_state), node.moves + ["Move C to bottom"]))
    return moves

def build_graph(initial_state):
    graph = Digraph(comment="A* Search Tree")
    target_state = ('A', 'B', 'C')
    open_list = [Node(initial_state, 0, scoring_function(initial_state), [])]
    closed_set = set()

    while open_list:
        current_node = open_list.pop(0)
        
        # สร้างโหนดในกราฟพร้อมแสดงคะแนน
        node_label = f"{current_node.state}\ng={current_node.g}, h={current_node.h}, f={current_node.f}"
        graph.node(str(current_node.state), label=node_label)

        if current_node.state == target_state:
            break

        closed_set.add(current_node.state)

        for move in generate_moves(current_node):
            if move.state not in closed_set:
                open_list.append(move)
                move_label = move.moves[-1]  # แสดงการเคลื่อนไหว
                graph.edge(str(current_node.state), str(move.state), label=move_label)

    return graph

def create_tree_diagram(initial_state, filename='tree_diagram'):
    # สร้างกราฟ
    graph = build_graph(initial_state)
    
    # ตั้งค่าสไตล์ของกราฟ
    graph.attr(rankdir='TB')  # Top to Bottom layout
    graph.attr('node', shape='rectangle', style='rounded')
    graph.attr('edge', arrowsize='0.5')
    
    # บันทึกเป็นไฟล์ PNG และ PDF
    graph.render(filename, format='png', cleanup=True)
    graph.render(filename, format='pdf', cleanup=True)

# ตัวอย่างการใช้งาน
initial_state = ('A', 'C', 'B')
create_tree_diagram(initial_state)
