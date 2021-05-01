Python best way to remove multiple strings from string

remove = {'is', 'this', 'a', 'string'}
clear = 'this is a test string'
a = list(filter(lambda x: x not in remove, clear.split()))
print(a)