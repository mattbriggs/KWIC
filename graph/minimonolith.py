import os
from git import Repo

ROOTFOLDER = r"C:\git\mb\KWIC\graph\clone"

def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout

def get_files(inpath, extension="md"):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(inpath):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == extension:
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist

def get_repo(git_url):
    Repo.clone_from(git_url,ROOTFOLDER )

get_repo("https://github.com/MicrosoftDocs/azure-stack-docs.git")
list_of_files = get_files(ROOTFOLDER, "md")
print(list_of_files)


