### "A stand alone python file that reads the json of your graphs or trees."
#### I do not quite understand the meaning of this file since my application directly reads the cached json file (not tree structure)
#### And I have built a tree constructor file to re-organize my data into a tree. There seems no need to read this tree.


import json

with open("my_tree.json", 'r') as file:
    my_tree = json.load(file)
print(my_tree)

