import argparse
import pandas as pd
import numpy as np
import os

def split_to_domains(file_path):
    df = pd.read_csv(file_path, encoding="cp932")
    print(df.columns)
    text_col = ""
    for c in df.columns:
        if "テキスト" in c:
            text_col = c

    df = df[["教科等",text_col]]
    for domain in df["教科等"].unique():
        out_df = df[df["教科等"]==domain][text_col]
        out_df = out_df.apply(lambda x:x.replace("　"," ").strip())
        # print(out_df.head())
    
        file_base_name = os.path.splitext(file_path)
        out_file = f"{file_base_name[0]}_{domain}.txt"
        
        np.savetxt(out_file, out_df.values, fmt='%s')
    
    # out_df.to_csv(out_file, encoding="utf8")

def main(file_path):
    split_to_domains(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cutoff unnecessary columns")
    parser.add_argument("file_path", help="Path to the CSV file")
    args = parser.parse_args()
    
    main(args.file_path)