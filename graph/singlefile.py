import mdparser as MDP

def get_metadata(infile):
    pass

def get_body_by_line(infile):
    pass

infile = r"C:\git\mb\KWIC\graph\clone\azure-stack\user\azure-stack-compute-overview.md"

mdparser = MDP.MDParser()

text_as_lines = mdparser.get_raw_body(infile).split("\n")
metadata = mdparser.process_meta()

print(metadata)

for indx, i in enumerate(text_as_lines):
    line_no = indx+1
    print("{} : {}".format(line_no, i))