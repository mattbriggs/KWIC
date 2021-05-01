'''Test for Function'''

import function as FU
import common_utilities as DR

INPUTFILE = DR.get_text_from_file("testdata\\dummy-text.md")

def test_method():
    '''Function x.'''

    assert INPUTFILE == INPUTFILE