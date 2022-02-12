import common_utilities as CU
import stoplist as SP

text = CU.get_text_from_file(r"C:\Users\mabrigg\OneDrive - Microsoft\Review_in\2021_06\kwic\corpus\12.md")
remove_list = SP.stoplist.split("\n")
for i in remove_list:
    text = text.replace(i, "")

print(text)