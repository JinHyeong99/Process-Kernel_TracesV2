from collections import deque, OrderedDict

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"Node({self.name})"

def build_node_tree(commands):
    def get_or_create_node(parent, name):
        for child in parent.children:
            if child.name == name:
                return child
        new_node = Node(name)
        parent.add_child(new_node)
        return new_node

    root = Node("Root")
    for command in commands:
        current_node = root
        for step in command:
            current_node = get_or_create_node(current_node, step)
        current_node.add_child(Node("None"))
    return root

def bfs_backtrack_on_range(root, previous_level):
    if not root:
        return []
    queue = deque([(root, [root.name], 0)])
    completed_subtrees = []
    visited_levels = {}
    while queue:
        node, path, level = queue.popleft()
        if node.name == "None":
            completed_subtrees.append(path[:-1])
            continue
        if node.name in visited_levels and level - visited_levels[node.name] <= previous_level:
            continue
        visited_levels[node.name] = level
        for child in node.children:
            queue.append((child, path + [child.name], level + 1))
    return completed_subtrees

def ordered_set(log):
    converted_lst = [tuple(item) if isinstance(item, list) else item for item in log]
    return list(OrderedDict.fromkeys(converted_lst))

def extract_activity_name(log):
    log_activity = []
    for trace in log:
        temp = []
        for event in trace:
            temp.append(event['concept:name'])
        log_activity.append(temp)
    return log_activity

def set_log_first(log_activity):
    set_log_activity = ordered_set(log_activity)
    return set_log_activity

def set_log_second(self, first_set_log_activity, previous_level=1):
    result_log = []
    for case_index, case in enumerate(first_set_log_activity):
        temp = []
        for event_index, event in enumerate(case):
            # previous_level 범위 내에서 중복 확인
            is_unique = True
            for prev_index in range(max(0, len(temp) - previous_level), len(temp)):
                if temp[prev_index] == event:
                    is_unique = False
            if is_unique or len(temp) == 0:
                temp.append(event)
        if temp not in result_log:
            result_log.append(temp)
    return result_log
