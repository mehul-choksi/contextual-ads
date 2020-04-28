"""
    # TODO:
        Fix:
        - treeToJSON
"""

import collections

class Node():

    def __init__(self, name='', parent='', children=set(), confidence=None):
        self.name = name
        self.parent = parent
        self.children = children
        self.confidence = confidence
        self.synonyms = dict()

        self._visited = False
        self.links = list()

    def __str__(self):
        return 'Name: '+self.name+' Children: '+ str([node.name for node in self.children] + ' Parent: ' + self.parent)

    def print_node(self):
        return 'Name: '+self.name+' Children: '+ str([node.name for node in self.children] + ' Parent: ' + self.parent)


class Tree():
    def __init__(self):
        """
        root - First node in the tree. All searches start from here.
        map - a dict to keep track and easy retreival of nodes
        """

        self.root = Node(name='root',children=set())

        self.map = {}
        self.map['root'] = self.root

        self.jsonStr = ""

    def create_node(self, name, parent):
        """ Create a single node
        Args:
            name: str, name of node
            parent: str, name of parent of new node
        Returns:
            Node object
         """

        try:
            node = self.map[name]
            return node
        except:
            node = Node(name,parent=parent.name)
            parent.children.add(node)

            node.parent = parent.name

            self.map[name] = node

            return node



    def bfs(self):
        """Breadth first search on tree"""

        root = self.root
        dq = collections.deque()

        dq.appendleft(root)
        visited = set()

        while dq:
            curr = dq.popleft()
            if curr in curr.children:
                curr.children.remove(curr)    #Remove child from itself

            print(curr.name)

            currCh = curr.children
            filteredCh = set()

            for child in currCh:
                if child.parent != curr.name:
                    continue
                else:
                    dq.appendleft(child)
                    filteredCh.add(child)
            curr.children = filteredCh


    # Need to fix this
    def treeToJSON(self, curr):
        self.jsonStr += ",{\"name\":" + "\"" + curr.name + "\","

        self.jsonStr += "\"narent\":" + "\"" + curr.parent + "\","
        if len(curr.children) > 0:
            self.jsonStr += "\"children\":["
            currChildren = curr.children

            for c in currChildren:
                self.treeToJSON(c)
            self.jsonStr += "]}"

        else:
            self.jsonStr += "}"


            #break
    def process(self):
        self.jsonStr = self.jsonStr[1:]
        self.jsonStr = self.jsonStr.replace("\"children\":[,", "\"children\":[")
        self.jsonStr = self.jsonStr.replace(",}", "}")
        self.jsonStr = self.jsonStr.replace("[,", "[")


if __name__ == '__main__':
    t = Tree()
