import os
import re
import argparse
import pandas as pd

from util import exp_to_digit_str

pd.set_option('display.float_format', lambda x:'%,g' % x) 

class CodeNode:
    
    def __init__(self, code, subject, description):
        self.code = code
        self.children = []
        self.description = description
        self.subject = subject
        self.description_chain = ['']

used_code_dict = {}
text_dict = {}
subject_dict = {}

def is_child(parent_code, child_candidate, code_list):
    parent_code_stripped = parent_code.rstrip("0")
    child_candidate_stripped = child_candidate.rstrip("0")
    
    if not child_candidate_stripped.startswith(parent_code_stripped):
        return False
    
    intermediate = child_candidate_stripped[len(parent_code_stripped):]
        
    return len(intermediate) >= 1

def build_tree(parent_node, code_list, level):
    parent_code = parent_node.code
    
    for code in code_list:
        child_candidate = code

        if is_child(parent_code, child_candidate, code_list):
            child_node = CodeNode(code, subject_dict[code], text_dict[code])
            if not used_code_dict[code]:
                used_code_dict[code] = True
                parent_node.children.append(child_node)
                # Add parent node description to the child node description chain
                child_node.description_chain.extend(parent_node.description_chain)
                child_node.description_chain.append(parent_node.description)
                child_node.description_chain =[d for d in child_node.description_chain if d != '']
                build_tree(child_node, code_list, level + 1)
            
def build_code_tree(code_list):
    root_node = CodeNode('','','')
    build_tree(root_node, code_list, 1)
    return root_node

def read_codes_from_csv(file_path, subject_col, code_col, text_col):
    types = str
    # if code_col == "学習指導要領コード":
    #     types = {
    #         "教科等":"str", "No":"str",
    #         "学習指導要領コード":"str",
    #         "学習指導要領テキスト":"str"
    #     }
    
    df = pd.read_csv(file_path, dtype=types, encoding="cp932")
    
    # CSVが"指数表記の文字列 (例: 8.21E+15)になっている場合があるので、
    # その場合に16桁の数値コードに変換する
    df[code_col] = df[code_col].apply(lambda x: exp_to_digit_str(x))
    
    # print(df.head(100))
    return df[code_col].astype(str).tolist(), df[text_col].tolist(), df[subject_col].tolist()


def print_tree(node, level=0):
    if node.code:
        print(f"{'  ' * level}- {node.code},{node.subject},{node.description}, {node.description_chain}")
    for child in node.children:
        print_tree(child, level + 1)

def print_code_tree(node, level=0):
    if node.code:
        print(f"{'  ' * level}- {node.code}")
    for child in node.children:
        print_code_tree(child, level + 1)

def dump_to_csv(node, file_path):
    rows = []

    def dump_node(_node):
        ds = ""
        descriptions = _node.description_chain
        for i, d in enumerate(descriptions):
            if not d in ["第１章　総則"]:
                ds = ds + d.strip() + "|"
        ds = ds + _node.description
        ds = re.sub('\u3000', ' ', ds)
        rows.append([_node.code, _node.subject, ds])
        for child in _node.children:
            dump_node(child)
    dump_node(node)
    
    file_base_name = os.path.splitext(file_path)
    # Omit the blank row
    pd.DataFrame(rows[1:], columns=['Code', 'Subject', 'Descriptions']).to_csv(file_base_name[0] + "_out.csv", encoding="cp932", index=False)
    # print(rows)

def find_deepest_level(node, level=0):
    if not node.children:
        return level + 1
    else:
        return max(find_deepest_level(child, level + 1) for child in node.children)

def main(file_path, stype):
    global used_code_dict
    global text_dict
    global subject_dict

    subject_col = '教科等'
    
    print(f"stype: {stype}")
    
    # 幼稚園指導要領の場合
    if stype == "k":
        code_col = '教育要領コード'
        text_col = '教育要領テキスト'
        
    else:
        code_col = '学習指導要領コード'
        text_col = '学習指導要領テキスト'
        
    codes, texts, subjects = read_codes_from_csv(file_path, subject_col, code_col, text_col)
    used_code_dict = {code: False for code in codes}
    text_dict = {code: texts[i] for i, code in enumerate(codes)}
    subject_dict = {code: subjects[i].strip() for i, code in enumerate(codes)}
    
    root_node = build_code_tree(codes)
    # deepest_level = find_deepest_level(root_node)  
    # print_tree(root_node)
    print_code_tree(root_node)
    dump_to_csv(root_node, file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a CSV file containing codes and build a tree structure.")
    parser.add_argument("file_path", help="Path to the CSV file containing the codes.")
    parser.add_argument("stype", help="幼稚園指導要領の場合、type=k.", default="g")
    
    args = parser.parse_args()
    
    main(args.file_path, args.stype)
