import uuid
import mdparser as MDP

def clear_line(instring):
    '''Clear problem characters'''
    instring = instring.replace("\\", "\\\\")
    instring = instring.replace("\"", "\\\"")
    instring = instring.replace("\'", "\\\'")
    return instring

infile = r"C:\git\mb\KWIC\graph\clone\azure-stack\user\azure-stack-compute-overview.md"

mdparser = MDP.MDParser()

text_as_lines = mdparser.get_raw_body(infile).split("\n")
metadata = mdparser.process_meta()

print(metadata)

for indx, i in enumerate(text_as_lines):
    line_text = clear_line(i)
    line_no = indx+1
    line_id = str(uuid.uuid4())
    print(line_text)
    print(line_no)
    print(line_id)
    line_map = "{ lineid : '" + line_id + "', "
    line_map += "lineno: '" + str(line_no) + "', "
    line_map += "text: '" + line_text + "' }"
    print(line_map)