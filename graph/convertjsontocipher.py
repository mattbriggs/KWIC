import json

example_json = '''{"title": "Azure Stack Hub overview",
"description": "An overview of what Azure Stack Hub is and how it lets you run Azure services in your datacenter.",
"author": "PatAltimore",
"ms.topic": "overview",
"ms.date": "03/22/2021",
"ms.author": "patricka",
"ms.reviewer": "unknown",
"ms.lastreviewed": "11/08/2019",
"ms.custom": "conteperfq4" }'''

def create_cipher(in_dict):
    keys = list(in_dict.keys())
    roll_cipher = "{ "
    size = len(keys)
    for indx, i in enumerate(keys):
        slug = '{} : "{}"'.format(i, in_dict[i])
        if indx == size-1:
            roll_cipher += slug + " }"
        else:
            roll_cipher += slug + ", "
    return roll_cipher

example_dict = json.loads(example_json)
example_dict["path"] = r'C:\git\mb\markdown-validator\testdata\azure-stack-overview.md'
print(create_cipher(example_dict))