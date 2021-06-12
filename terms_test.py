'''Test for Function'''

import terms as TM
import common_utilities as DR

def test_get_top_fifty_double():
    '''Extract and ranks the top 50 (or less) entities. More than 2 words.'''

    fifty = TM.get_top_fifty("testdata\\dummy-text.md")

    assert fifty[1]["keyword"] == "Azure Stack"

def test_get_top_fifty_single():
    '''Extract and ranks the top 50 (or less) entities. 1 word.'''

    fifty = TM.get_top_fifty("testdata\\dummy-text.md", True)
    list_of_entities = []
    for i in fifty.keys():
        list_of_entities.append(fifty[i]["keyword"])

    assert "Bildad" in list_of_entities