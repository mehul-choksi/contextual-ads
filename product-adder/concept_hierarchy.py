import json

class Node():
    def __init__(self, name):
        self.name = name
        self.parent = 0
        self.children = []
        self.confidence = 0;

    def printNode(self):
        print(self.name + ' ' + str(self.confidence))

class Concept_hierarchy():
    def __init__(self, file):
        self.file = file    # JSON file from which the Concept_hierarchy to be read
        self.lookup = {}
        self.root = Node("root")
        self.lookup["root"] = self.root

        with open(self.file, 'r') as f:
            ch_dict = json.load(f)

        self.insert_children(self.root, ch_dict.get("children"))

    def insert_children(self, root, children):
        if children is None:
            return # There are no children
        for child in children:
            new_child = Node(child["name"])
            new_child.parent = child["parent"]

            self.lookup[child["name"]] = new_child

            root.children.append(new_child)
            self.insert_children(new_child, child.get("children"))
