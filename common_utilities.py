''' Name

    This script will 
    Input
    Output

    Matt Briggs V0.0: X.X.2019
'''

import os
import csv
from datetime import datetime, timedelta
from prettytable import PrettyTable

THISDATE = str(datetime.now().strftime("%Y-%m-%d"))

def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout


def write_text(outbody, path):
    '''Write text file to the path.'''
    out_file = open(path, "w")
    for line in outbody:
        out_file.write(line)
        #out_file.write("\n")
    out_file.close()


def write_csv(outbody, path):
    '''Write CSV file to the path.'''
    csvout = open(path, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in outbody:
        csvwrite.writerow(r)
    csvout.close()


def output_table(indict):
    '''With the dict provided by the term rank, print a list for pretty print'''
    x = PrettyTable()
    x.field_names = ["Count"]
    for i in indict.keys():
        x.add_row([str(indict[i])])
    x.align["Count"] = "l"
    print(x)


def get_files(inpath):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(inpath):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == "md":
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist


def main():
    print("This is the developer relations utility.")


if __name__ == "__main__":
    main()
