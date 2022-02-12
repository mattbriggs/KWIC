''' Extract terms from repository.

    Input: repo
    Output: csv of terms

    Matt Briggs V0.1: 5.9.2019
'''

import json
import common_utilities as  CU
import terms as TM

ONPAGE_TABLE = [["file", "date", "score", "keyword" ]]

def add_ranks_table(indict):
    '''Insert the logic to process the return from the function.'''

    global ONPAGE_TABLE

    for k in list(indict.keys()):
        record = []
        record.append(indict[k]["page"])
        record.append(CU.THISDATE)
        record.append(indict[k]["score rank"])
        record.append(indict[k]["keyword"])
        ONPAGE_TABLE.append(record)

def main():
    '''
    Add Instructions.
    '''
    print("Starting")
    config_file = open("config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    filelist =  CU.get_files(path_in)
    for f in filelist:
        try:
            print("Processing: {}".format(f))
            term_list = TM.get_top_fifty(f, False)
            add_ranks_table(term_list)
        except Exception as e:
            print("A problem with: {} : {}".format(f, e))
    reportname = path_out + "entity_extraction.csv"
    CU.write_csv(ONPAGE_TABLE,reportname)
    print("Completed processing.")

if __name__ == "__main__":
    main()
