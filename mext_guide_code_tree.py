import argparse
import pandas as pd

class CodeNode:
    def __init__(self, code):
        self.code = code
        self.children = []

used_code_dict = {}

def is_child(parent_code, child_candidate, code_list):
    parent_code_stripped = parent_code.rstrip("0")
    child_candidate_stripped = child_candidate.rstrip("0")
    
    if not child_candidate_stripped.startswith(parent_code_stripped):
        return False
    
    intermediate = child_candidate_stripped[len(parent_code_stripped):]
        
    return len(intermediate) >= 1

def build_tree(parent_node, code_list, level, used_code_dict):
    parent_code = parent_node.code

    for code in code_list:
        child_candidate = code

#        if is_direct_child(parent_code, child_candidate, code_list):
        if is_child(parent_code, child_candidate, code_list):
            child_node = CodeNode(code)
            if not used_code_dict[code]:
                used_code_dict[code] = True
                parent_node.children.append(child_node)
                build_tree(child_node, code_list, level + 1, used_code_dict)
            
def build_code_tree(code_list, used_code_dict):
    root_node = CodeNode('')
    build_tree(root_node, code_list, 1, used_code_dict)
    return root_node

def read_codes_from_csv(file_path, column_name):
    df = pd.read_csv(file_path, encoding="cp932")
    return df[column_name].tolist()

def print_tree(node, level=0):
    if node.code:
        print(f"{'  ' * level}- {node.code}")
    for child in node.children:
        print_tree(child, level + 1)

def find_deepest_level(node, level=0):
    if not node.children:
        return level + 1
    else:
        return max(find_deepest_level(child, level + 1) for child in node.children)

def main(file_path):
    column_name = '学習指導要領コード' 
    
    codes = read_codes_from_csv(file_path, column_name)
    used_code_dict = {code: False for code in codes}
    root_node = build_code_tree(codes, used_code_dict)
    deepest_level = find_deepest_level(root_node)
    # remove_duplicates_from_deepest_leaves(root_node, deepest_level)
    print_tree(root_node)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a CSV file containing codes and build a tree structure.")
    parser.add_argument("file_path", help="Path to the CSV file containing the codes.")
    args = parser.parse_args()
    
    main(args.file_path)
