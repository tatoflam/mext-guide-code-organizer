import codecs
import csv
import os

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
                
def exp_to_digit_str(x):
    if x[-4:-2] == "E+" :
        d = str(int(float(x)))
        # print(d)
    else:
        d = x
    return d
