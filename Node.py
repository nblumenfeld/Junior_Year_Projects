'''
A node in a Huffmans tree
'''

class Node:
    '''
    data represents:
        leftChild - the left child of this Node
        rightChild - the right child of this Node
        ch - the character
        frequency - the frequency of the character

    NOTE - ch must be set to None for non-leaf nodes
    '''
    def __init__(self, frequency, ch, leftChild = None, rightChild = None):
        self.leftChild = leftChild
        self.rightChild = rightChild

        self.frequency = frequency
        self.ch = ch
        self.level = 0
        while leftChild:
            if leftChild.getLeftChild() is None:
                break
            else:
                leftChild = leftChild.getLeftChild()
                self.level += 1

    # returns the frequency count of this node
    def getFrequency(self):
        return self.frequency
    
    # returns the character of this node
    def getCh(self):
        return self.ch

    # returns the left child of this node
    def getLeftChild(self):
        return self.leftChild
    
    # returns the right child of this node
    def getRightChild(self):
        return self.rightChild

    # returns whether this node is a leaf node or not
    def isLeafNode(self):
        return self.leftChild == None and self.rightChild == None

    # sets the level of this node
    def setLevel(self,level):
        self.level = level
   
    # returns the level of this node 
    def getLevel(self):
        return self.level
