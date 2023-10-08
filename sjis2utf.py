import argparse
from util import sjis_to_utf, exp_to_digit_str
import pandas as pd
import os


def convert_exp(file_path):
    file_base_name = os.path.splitext(file_path)
    out_file = file_base_name[0] + "_utf8.csv"
     
    df = pd.read_csv(out_file)
    print(df.head(10))
    code_col  = ""
    for c in df.columns:
        if "コード" in c:
            code_col = c
    print(code_col)
    df[code_col] = df[code_col].apply(lambda x: exp_to_digit_str(x))
    df.to_csv(out_file)

def main(file_path):
    sjis_to_utf(file_path)
    
    # Change the code with exponential number into digit
    convert_exp(file_path)  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Change CSV file in Shift JIS format to UTF8")
    parser.add_argument("file_path", help="Path to the CSV file")
    args = parser.parse_args()
    
    main(args.file_path)