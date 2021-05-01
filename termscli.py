''' Terms

    The module will produce a CSV of 
    Input:
    Output:

    Matt Briggs V0.0: X.X.2019
'''

import cmd
import common_utilities as DR
import terms as TM

APPVERSION = "Base CLI Version 0.0.1.20190418\n"

class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "

    def do_terms(self, line):
        '''The main logic of the utility.'''

        try:
            fifty = TM.get_top_files(line)
            print(fifty)
            TM.print_dict_rank(fifty)
            return
        except Exception as e:
            print ("There was some trouble.\nError code: {}".format(e))
            return

    def do_help(self, line):
        '''Type help to get help for the application.'''
        print("Type `terms` <file name> to get the terms in the topic.")
        return

    def do_quit(self, line):
        '''Type quit to exit the application.'''
        return True

    def do_exit(self, line):
        '''Type exit to exit the application.'''
        return True

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    TagTerminal().cmdloop(APPVERSION)