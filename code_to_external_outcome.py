import os
import argparse
import pandas as pd
from datetime import datetime
import pytz
import csv
import codecs

from constants import school_dict, syllabus_id_dict

def remove_sequential_line_feeds(string):
    #while '\n\n' in string:
    string = string.replace('\n', '')
    return string

def sjis_to_utf(file_path):
    
    file_base_name = os.path.splitext(file_path)
    out_file = file_base_name[0] + "_utf8.csv" 
    
    # Open the source file with Shift-JIS encoding
    with codecs.open(file_path, 'r', 'cp932') as sjis:
        # Read the CSV
        reader = csv.reader(sjis)

        # Open a new file with UTF-8 encoding
        with codecs.open(out_file, 'w', 'utf-8') as utf:
            writer = csv.writer(utf)

            for row in reader:
                new_row = [remove_sequential_line_feeds(field) for field in row]
                writer.writerow(new_row)
pd.options.display.max_columns = None

def main(file_path, syllabus_id):
    df = pd.read_csv(file_path, encoding="cp932")
    
    now = datetime.now(pytz.utc)
    timestamp_string = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    
    partitionKey = "mextJp"
    rowKeyPrefix = partitionKey + "-" + syllabus_id + "-"
    
    primary = False
    secondary = False
    senior = False
    
    # 2nd digit of syllabus id represents the school code. 
    school_code = syllabus_id[1]
    if school_code in ["1","2","5","6"]:
        primary = True
    elif school_code in ["3","4","6","B"]:
        secondary = True
    
    school = school_dict[school_code]
    
    outcome_columns = ["PartitionKey","RowKey","Timestamp",
                       "OutcomeCode","OutcomeCode@type",
                       "OutcomeDescription","OutcomeDescription@type",
                       "Owner","Owner@type","Primary","Primary@type",
                       "Secondary","Secondary@type","Senior","Senior@type",
                       "Subject","Subject@type","Syllabus","Syllabus@type",
                       "SyllabusId","SyllabusId@type"]
    outcome_df = pd.DataFrame(columns=outcome_columns)
    outcome_df["RowKey"] = rowKeyPrefix + df["Code"]
    outcome_df["PartitionKey"] = partitionKey
    outcome_df["Timestamp"] = timestamp_string
    outcome_df["OutcomeCode"] = df["Code"]
    outcome_df["OutcomeCode@type"] = "String"
    outcome_df["OutcomeDescription"] = df["Descriptions"]
    outcome_df["OutcomeDescription@type"] = "String"
    outcome_df["Owner"] = "MEXT of Japan"
    outcome_df["Owner@type"] = "String"
    outcome_df["Primary"] = primary
    outcome_df["Primary@type"] = "Boolean"
    outcome_df["Secondary"] = secondary
    outcome_df["Secondary@type"] = "Boolean"
    outcome_df["Senior"] = senior
    outcome_df["Senior@type"] = "Boolean"
    outcome_df["Subject"] = school + "|" + df["Subject"]
    outcome_df["Subject@type"]="String"
    outcome_df["Syllabus"] = syllabus_id_dict[syllabus_id]
    outcome_df["Syllabus@type"] = "String"
    outcome_df["SyllabusId"] = syllabus_id
    outcome_df["SyllabusId@type"] = "String"
    
    print(outcome_df.head())
    file_base_name = os.path.splitext(file_path)
    outcome_file_path = file_base_name[0] + "_externaloutcomes.csv"
    outcome_df.to_csv(outcome_file_path,  encoding="cp932", index=False)
    
    # Convert to utf-8
    sjis_to_utf(outcome_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a CSV(Index,Code,Subject,Descriptions) file to a format for 'external outcome'.")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("syllabus_id", help="e.g. 83V11 \n 2nd digit represents school type - 1:幼稚園,2:小学校,3:中学校,4:高等学校,5:特別支援学校幼稚部,6:特別支援学校小学部・中学部,B:特別支援学校高等部")
    args = parser.parse_args()
    
    main(args.file_path, args.syllabus_id)