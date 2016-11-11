'''
Created on Aug 25, 2016
This class is a decision tree implementation taken from Hal Daume.

@author: km_dh and noah_Blumenfeld for DTConstruct/ DTPredict
'''
import numpy as np
from scipy import stats

class DT(object):
    '''
    classdocs TODO: Fill this in
    '''   
    def __init__(self):
        '''
        constructor
        '''
        
    def res(self,mode='name', model={}, test_case=np.zeros(1), X=np.zeros(1), Y=np.zeros(1), h_param = 1):
        '''
        usage is of the two following:
        learn = DT()
        model = learn.res('train', X=, Y=, cutoff=)
        Y = learn.res('predict', model=, X=)
        '''
        mode = mode.lower()
        
        if(mode == 'name'):
            return 'DT'
        
        if(mode == 'train'):
            if(len(X) < 2 or len(Y) < 1 or h_param < 0):
                print("Error: training requires three arguments: X, Y")
                return 0
            sizeX = X.shape
            sizeY = Y.shape
            if(sizeX[0] != sizeY[0]):
                print("Error: there must be the same number of data points in X and Y")
                return 0
            if(sizeY[1] != 1):
                print("Error: Y must have only 1 column")
                return 0
            if(h_param not in range(1000)):
                print("Error: cutoff must be a positive scalar")
                return 0
            res = {}
            res = self.DTconstruct(X,Y,h_param)
            return res
        
        if(mode == 'predict'):
            if(len(model) < 1 or len(test_case) < 1):
                print("Error: prediction requires two arguments: the model and X")
                return 0
            if('isLeaf' not in model.keys()):
                print("Error: model does not appear to be a DT model")
                return 0
            
            #set up output
            rowCol = test_case.shape
            if(len(rowCol) < 2):
                res = self.DTpredict(model, test_case)
            else:
                N = rowCol[0]
                res = np.zeros((N,1))
                for n in range(N):
                    ans = self.DTpredict(model, test_case[n,:])
                    res[n,:] = ans
            return res
        print("Error: unknown DT mode: need train or predict")
        
    
       
    def DTconstruct(self,X,Y,cutoff):
        # the Data comes in as X which is NxD and Y which is Nx1.
        # cutoff is a scalar value. We should stop splitting when N is <= cutoff
        #
        # features (X) may not be binary... you should *threshold* them at
        # 0.5, so that anything < 0.5 is a "0" and anything >= 0.5 is a "1"
        #
        # we want to return a *tree*. the way we represent this in our model 
        # is that the tree is a Python dictionary.
        #
        # to represent a *leaf* that predicts class 3, we can say:
        #    tree = {}
        #    tree['isLeaf'] = 1
        #    tree['label'] = 3
        #
        # to represent a split node, where we split on feature 5 and then
        # if feature 5 has value 0, we go down the left tree and if feature 5
        # has value 1, we go down the right tree.
        #    tree = {}
        #    tree['isLeaf'] = 0
        #    tree['split'] = 5
        #    tree['left'] = ...some other tree...
        #    tree['right'] = ...some other tree...

        tree = {}
        rowCol = X.shape
        # print rowCol
        #Find the possible classes for the data
        classes = np.unique(Y)
        # print 'classes', classes

        guess = stats.mode(Y)
        # print 'guess', guess

        #if you have reached cutoff make a leaf or only 1 feature or example
        #if there is only one class make a leaf
        if rowCol[0] <= cutoff or rowCol[1] <= 1 or rowCol[0] <= 1 or len(classes) == 1:
            tree = {'isLeaf':1, 'label':[int(guess[0][0])]}
            return tree

        highScore = 0
        split_feat = -1
        for i in range(rowCol[1]):
            # separate Y into rows where X[:,i] <= 0 (100 for MNIST)
            neg_classes = Y[np.where(X[:, i] <= 100)]
            # print neg_classes

            # the max number of these that are in the same class
            majorityNo = [[0],[0]] if len(neg_classes) < 1 else stats.mode(neg_classes)
            # print 'majority no', majorityNo
            #separate Y into rows where X[:,1] > 0 (100 for MNIST)
            pos_classes = Y[np.where(X[:, i] > 100)]
            # print pos_classes

            # the max number of these that are in the same class
            majorityYes = [[0], [0]] if len(pos_classes) < 1 else stats.mode(pos_classes)
            # print 'majority yes', majorityYes

            score = majorityNo[1][0] + majorityYes[1][0]
            # print 'score', score
            # keeps the column with the highest score
            if score > highScore:
                highScore = score
                split_feat = i

        # print split_feat

        # get the left valuse <= .5 for book (100 for MNIST)
        left = X[X[:,split_feat] <= 100]
        Yleft = Y[X[:,split_feat] <= 100]
        left_sp = left.shape
        Yleft_sp = Yleft.shape

        left_tree = {}
        if left_sp[0] != Yleft_sp[0] or Yleft_sp[0] < 1:
            left_tree = {'isLeaf':1, 'label':[int(guess[0][0])]}
        else:
            left = np.delete(left,split_feat,1)
            # print 'left', left, 'Y left', Yleft
            left_tree = self.DTconstruct(left,Yleft,cutoff)

        # get the right values > 0.5 for book (100 for MNIST)
        right = X[X[:,split_feat] > 100]
        Yright = Y[X[:,split_feat] > 100]
        right_sp = right.shape
        Yright_sp = Yright.shape

        right_tree = {}
        if Yright_sp[0] < 1 or right_sp[0] != Yright_sp[0]:
            right_tree = {'isLeaf': 1, 'label': [int(guess[0][0])]}
        else:
            right = np.delete(right,split_feat, 1)
            # print 'right', right, 'Y right', Yright
            right_tree = self.DTconstruct(right,Yright,cutoff)

        # make tree
        tree = {'isLeaf': 0, 'split': split_feat, 'left': left_tree, 'right': right_tree}

        return tree

        
    def DTpredict(self,model,X):
        # here we get a tree (in the same format as for DTconstruct) and
        # a single 1xD example that we need to predict with
        
        if model['isLeaf'] == 1:
            #print "Got to leaf ", model['label']
            return model['label']
        split = model['split']

        # print "split is ", split, "X here is ". X[split]
        # remember to change this to 100 for MNIST
        if X[split] <= 0.5:
            X = np.delete(X,split)
            return self.DTpredict(model['left'], X)

        X = np.delete(X, split)
        return self.DTpredict(model['right'], X)
    
    def DTdraw(self,model,level=0):
        indent = ' '
        if model is None:
            return
        print indent*4*level + 'isLeaf: ' + str(model['isLeaf'])
        if model['isLeaf']==1:
            print indent*4*level + 'Y: ' + str(model['label'])
            return
        print indent*4*level + 'split ' + str(model['split'])
        left_tree = str(self.DTdraw(model['left'],level+1))
        if left_tree != 'None':
            #print model['left']
            print indent*4*level + 'left: ' + left_tree
        right_tree = str(self.DTdraw(model['right'],level+1))
        if right_tree != 'None':
            #print model['right']
            print indent*4*level + 'right: ' + right_tree
        