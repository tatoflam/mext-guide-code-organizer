import os
import argparse
import pandas as pd
from datetime import datetime
import pytz

from constants import school_dict, syllabus_id_dict
from util import sjis_to_utf 

pd.options.display.max_columns = None

def main(file_path, syllabus_id):
    df = pd.read_csv(file_path, encoding="cp932")
    
    now = datetime.now(pytz.utc)
    timestamp_string = current_time = datetime.utcnow().isoformat(timespec='microseconds') + 'Z'
    
    partitionKey = "mextJp"
    rowKeyPrefix = partitionKey + "-" + syllabus_id + "-"
    
    kinder = False
    primary = False
    secondary = False
    senior = False
    
    # 2nd digit of syllabus id represents the school code. 
    school_code = syllabus_id[1]
    if school_code in ["1","5"]:
        kinder = True
    elif school_code in ["2","6"]:
        primary = True
    elif school_code in ["3","6"]:
        secondary = True
    elif school_code in ["4","B"]:
        senior = True
    
    school = school_dict[school_code]
    

    # outcome_columns = ["PartitionKey","RowKey","Timestamp",
    #                    "OutcomeCode","OutcomeCode@type",
    #                    "OutcomeDescription","OutcomeDescription@type",
    #                    "Owner","Owner@type","Primary","Primary@type",
    #                    "Secondary","Secondary@type","Senior","Senior@type",
    #                    "Subject","Subject@type","Syllabus","Syllabus@type",
    #                    "SyllabusId","SyllabusId@type"]
     
    outcome_columns = ["PartitionKey","RowKey",
                       "Code","Code@type","Created","Created@type",
                       "Description","Description@type",
                       "Primary","Primary@type",
                       "Provider","Provider@type",
                       "ProviderId","ProviderId@type",
                       "Secondary","Secondary@type",
                       "Senior","Senior@type",
                       "Subject","Subject@type",
                       "Syllabus","Syllabus@type",
                       "SyllabusId,SyllabusId@type",
                       "Y0","Y0@type","Y1","Y1@type","Y10","Y10@type","Y11","Y11@type","Y12","Y12@type","Y2","Y2@type","Y3","Y3@type","Y4","Y4@type","Y5","Y5@type","Y6","Y6@type","Y7","Y7@type","Y8","Y8@type","Y9","Y9@type"]
    
    outcome_df = pd.DataFrame(columns=outcome_columns)
    outcome_df["RowKey"] = rowKeyPrefix + df["Code"]
    outcome_df["PartitionKey"] = partitionKey
    outcome_df["Code"] = df["Code"]
    outcome_df["Code@type"] = "String"
    outcome_df["Created"] = timestamp_string
    outcome_df["Created@type"] = "DateTime"
    outcome_df["Description"] = df["Descriptions"]
    outcome_df["Description@type"] = "String"
    outcome_df["Primary"] = primary
    outcome_df["Primary@type"] = "Boolean"
    outcome_df["Provider"] = "MEXT of Japan"
    outcome_df["Provider@type"] = "String"
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
    outcome_df["Y0"] = kinder
    outcome_df["Y0@type"] = "Boolean"
    outcome_df["Y1"] = primary
    outcome_df["Y1@type"] = "Boolean"
    outcome_df["Y10"] = senior
    outcome_df["Y10@type"] = "Boolean"
    outcome_df["Y11"] = senior
    outcome_df["Y11@type"] = "Boolean"
    outcome_df["Y12"] = senior
    outcome_df["Y12@type"] = "Boolean"
    outcome_df["Y2"] = primary
    outcome_df["Y2@type"] = "Boolean"
    outcome_df["Y3"] = primary
    outcome_df["Y3@type"] = "Boolean"
    outcome_df["Y4"] = primary
    outcome_df["Y4@type"] = "Boolean"
    outcome_df["Y5"] = primary
    outcome_df["Y5@type"] = "Boolean"
    outcome_df["Y6"] = primary
    outcome_df["Y6@type"] = "Boolean"
    outcome_df["Y7"] = secondary
    outcome_df["Y7@type"] = "Boolean"
    outcome_df["Y8"] = secondary
    outcome_df["Y8@type"] = "Boolean"
    outcome_df["Y9"] = secondary
    outcome_df["Y9@type"] = "Boolean"
    
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