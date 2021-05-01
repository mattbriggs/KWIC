import terms as TE
import stoplist as SP

def filter_text(instring):
    '''Get a raw string and return a prepped string for entity extraction.'''
    prep = instring.replace("\n", " ").lower()
    stoplist = SP.stoplist.lower()
    stoplist = stoplist.split("\n")
    stopset = set(stoplist)
    filtered = list(filter(lambda x: x not in stopset, prep.split()))
    return filtered

path = r"C:\Users\mabrigg\OneDrive - Microsoft\Review_in\2021_04\kwic-items\corpus\19.md"
bodytext = TE.get_text_from_file(path)
prep_text = TE.filter_text(bodytext)
record_terms = TE.extract_entities(prep_text)
print(record_terms)









