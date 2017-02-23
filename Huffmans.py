'''
Implementation of Huffmans

Noah Blumenfeld
'''

import sys
import heapq

from Node import Node

def traverse(tree,levelsDict,level):
    if tree.isLeafNode():
        tree.setLevel(level) 
        levelsDict[tree.getCh()] = level       
    else:
        traverse(tree.getLeftChild(),levelsDict,level + 1)
        traverse(tree.getRightChild(),levelsDict,level + 1)

'''
This function is passed a string and returns the 
number of bits that would be required to encode 
the string using a Huffman tree.
'''
def huffmans(line):

    '''
    constructs a dictionary that 
    determines the frequency of each character
    '''
    frequency = { }
    
    for c in line:
        if c in frequency.keys():
            frequency[c] += 1
        else:
            frequency[c] = 1

    '''
    demonstrate how to create node objects representing a 
    character and frequency of that character
    
    *** This is hardcoded for the input string "barry andy barbara"
    '''
    # char_1 = 'b'
    # char_2 = 'r'
    # node1 = Node(frequency[char_1],char_1)
    # node2 = Node(frequency[char_2],char_2)
    #
    # '''
    # demonstrate how to create an interior node
    # that stores the sum of the frequencies of
    # two leaf nodes.
    #
    # *** This is essentially a tree rooted at node3 with node1
    # as its left child and node2 as its right child
    #
    #     node3
    #    /     \
    #   /       \
    # node1   node2
    #
    # '''
    # f1 = node1.getFrequency()
    # f2 = node2.getFrequency()
    # node3 = Node(f1+f2,None,node1,node2)
    #
    # # the frequency of this new node
    # f3 = node3.getFrequency()
    #
    # # return the frequency of this new node
    # return f3

    #Initialize the algorithm
    nodeDict = huffmanConstruct(frequency)
    levelList = huffmanTraverse(nodeDict)
    return huffmanTotal(frequency,levelList)


'''
constructs a huffman tree from a frequency dictionary
'''
def huffmanConstruct(frequencyList):
    # set up instance variables
    keys = frequencyList.keys()[:]
    keysFreqIndex = []
    for key in keys:
        keysFreqIndex.append(frequencyList[key])
    NodeDict = {}

    #construct the tree
    while len(keys) > 1:
        #pull out the 2 smallest "nodes"
        index1 = keysFreqIndex.index(min(keysFreqIndex))
        key1 = keys[index1]
        keysFreqIndex.remove(min(keysFreqIndex))
        keys.remove(key1)
        index2 = keysFreqIndex.index(min(keysFreqIndex))
        key2 = keys[index2]
        keysFreqIndex.remove(min(keysFreqIndex))
        keys.remove(key2)

        #obtain 2 child nodes
        if key1 not in NodeDict.keys():
            node1 = Node(frequencyList[key1], key1)
            NodeDict[key1] = node1
        else:
            node1 = NodeDict[key1]

        if key2 not in NodeDict.keys():
            node2 = Node(frequencyList[key2], key2)
            NodeDict[key2] = node2
        else:
            node2 = NodeDict[key2]

        #get child frequencies
        f1 = node1.getFrequency()
        f2 = node2.getFrequency()

        #create parent node and set levels of children
        node3 = Node(f1+f2, key1+key2, node1, node2)
        setChildrenLevel(node3)

        #add new parent node to node dictionary, keys list and index list
        NodeDict[key1+key2] = node3
        keys.append(key1+key2)
        keysFreqIndex.append(f1+f2)

    return NodeDict

'''
Increments the children of specified node by 1
'''
def setChildrenLevel(node):
    if node is None:
        return
    else:
        #recursively call
        left = node.getLeftChild()
        right = node.getRightChild()
        setChildrenLevel(left)
        setChildrenLevel(right)
        #increment level
        if left is not None and right is not None:
            leftLevel = left.getLevel() + 1
            left.setLevel(leftLevel)
            rightLevel = right.getLevel() + 1
            right.setLevel(rightLevel)

#traverse the tree to obtain the level of each leaf node
'''
Returns a list with all the levels of the leaf nodes within the huffman tree
'''
def huffmanTraverse(nodeDict):
    #loop through node dictionary and get the level for each node
    levelDict = {}
    for key in nodeDict.keys():
        current = nodeDict[key]
        levelDict[key] = current.getLevel()

    return levelDict


 #total up amount of bits and return
'''
Returns the total number of bits used to encode the string
'''
def huffmanTotal(frequencyList,levelList):
    total = 0
    for key in frequencyList.keys():
        total = total + (frequencyList[key] * levelList[key])

    return total



if __name__ == '__main__':
    print huffmans('barry andy barbara')
