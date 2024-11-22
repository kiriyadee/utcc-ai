import copy
import os
from collections import deque

import graphviz


class BlockWorld:
    def __init__(self):
        # สถานะเริ่มต้น [B, C, A]
        self.initial_state = ['B', 'C', 'A']
        # สถานะเป้าหมาย [A, B, C]
        self.goal_state = ['A', 'B', 'C']
        self.node_count = 0

    def state_to_string(self, state):
        return '\n'.join(state)

    def create_tree_visualization(self, path, algorithm_name):
        dot = graphviz.Digraph(comment=f'Block World {algorithm_name} Tree')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='rectangle', style='rounded')
        dot.attr('edge', arrowsize='0.5')
        
        # สร้าง node สำหรับแต่ละสถานะในเส้นทาง
        for i, state in enumerate(path):
            node_id = f"node_{i}"
            h_value = self.calculate_h_value(state)
            g_value = i  # g คือระยะทางจากจุดเริ่มต้น
            f_value = g_value + h_value
            label = f"State {i}\ng={g_value}, h={h_value}, f={f_value}\n{self.state_to_string(state)}"
            
            # กำหนดสีและสไตล์ให้ node
            if i == 0:  # สถานะเริ่มต้น
                dot.node(node_id, label, style='filled,rounded', fillcolor='lightblue')
            elif i == len(path) - 1:  # สถานะเป้าหมาย
                dot.node(node_id, label, style='filled,rounded', fillcolor='lightgreen')
            else:  # สถานะระหว่างทาง
                dot.node(node_id, label, style='rounded')
            
            # สร้างเส้นเชื่อมพร้อมแสดงการเคลื่อนที่
            if i > 0:
                move_label = self.get_move_description(path[i-1], state)
                dot.edge(f"node_{i-1}", node_id, label=move_label)
        
        # บันทึกไฟล์
        filename = f"block_world_{algorithm_name.lower()}"
        dot.render(filename, view=True, format='png', cleanup=True)
        dot.render(filename, format='pdf', cleanup=True)
        dot.save(filename + '.dot')  # Save source file
        return filename + '.png'

    def get_move_description(self, prev_state, curr_state):
        # หาตำแหน่งที่เปลี่ยนแปลง
        changes = []
        for i, (prev, curr) in enumerate(zip(prev_state, curr_state)):
            if prev != curr:
                changes.append((prev, i, curr_state.index(prev)))
        if changes:
            block, from_pos, to_pos = changes[0]
            return f"Move {block}: {from_pos}→{to_pos}"
        return ""

    def get_possible_moves(self, state):
        moves = []
        for i in range(len(state)):
            for j in range(len(state)):
                if i != j:
                    new_state = state.copy()
                    block = new_state.pop(i)
                    new_state.insert(j, block)
                    moves.append(new_state)
        return moves

    def calculate_h_value(self, state):
        # คำนวณจำนวนบล็อกที่ไม่อยู่ในตำแหน่งที่ถูกต้อง
        return sum(1 for i in range(len(state)) if state[i] != self.goal_state[i])

    def bfs(self):
        print("\nการค้นหาแบบ BFS:")
        visited = set()
        queue = deque([(self.initial_state, [self.initial_state])])
        
        while queue:
            current_state, path = queue.popleft()
            state_tuple = tuple(current_state)
            
            if current_state == self.goal_state:
                self.create_tree_visualization(path, 'BFS')
                return path
            
            if state_tuple not in visited:
                visited.add(state_tuple)
                print(f"สถานะปัจจุบัน: {current_state}, h={self.calculate_h_value(current_state)}")
                
                for next_state in self.get_possible_moves(current_state):
                    if tuple(next_state) not in visited:
                        new_path = path + [next_state]
                        queue.append((next_state, new_path))
        return None

    def dfs(self):
        print("\nการค้นหาแบบ DFS:")
        visited = set()
        stack = [(self.initial_state, [self.initial_state])]
        
        while stack:
            current_state, path = stack.pop()
            state_tuple = tuple(current_state)
            
            if current_state == self.goal_state:
                self.create_tree_visualization(path, 'DFS')
                return path
            
            if state_tuple not in visited:
                visited.add(state_tuple)
                print(f"สถานะปัจจุบัน: {current_state}, h={self.calculate_h_value(current_state)}")
                
                for next_state in self.get_possible_moves(current_state):
                    if tuple(next_state) not in visited:
                        new_path = path + [next_state]
                        stack.append((next_state, new_path))
        return None

def print_solution(path):
    if path:
        print("\nเส้นทางการแก้ปัญหา:")
        for i, state in enumerate(path):
            print(f"ขั้นตอนที่ {i}: {state}")
    else:
        print("ไม่พบคำตอบ")

# ทดสอบการทำงาน
if __name__ == "__main__":
    block_world = BlockWorld()
    
    print("สถานะเริ่มต้น:", block_world.initial_state)
    print("สถานะเป้าหมาย:", block_world.goal_state)
    
    # ทดสอบ BFS
    bfs_solution = block_world.bfs()
    print_solution(bfs_solution)
    
    # ทดสอบ DFS
    dfs_solution = block_world.dfs()
    print_solution(dfs_solution)