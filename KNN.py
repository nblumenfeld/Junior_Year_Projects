'''
Created on Aug 29, 2016
This class is a decision tree implementation taken from Hal Daume.

@author: km_dh
'''
import numpy as np
import scipy.spatial.distance as sciDist
from scipy import stats

class KNN(object):
    '''
    classdocs TODO: Fill this in
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def res(self, mode='name', model={}, test_case=np.zeros(1), X=np.zeros(1), Y=np.zeros(1), h_param =0):
        '''
        usage is of the two following:
        learn = KNN()
        model = learn.res('train', X=, Y=, K=)
        Y = learn.res('predict', model=, X=)
        '''
        mode = mode.lower()
        
        if(mode == 'name'):
            return 'KNN'
        
        if(mode == 'train'):
            if(len(X) < 2 or len(Y) < 1 or h_param < 1):
                print("Error: training requires three arguments: X, Y, and cutoff")
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
            res = {'X': X, 'Y': Y, 'K': h_param}
            return res
        
        if(mode == 'predict'):
            if(len(model) < 1 or len(test_case) < 1):
                print("Error: prediction requires two arguments: the model and X")
                return 0
            if('K' not in model.keys() and 'X' not in model.keys() and 'Y' not in model.keys()):
                print("Error: model does not appear to be a KNN model")
                return 0
            X = model['X']
            sizeModel = X.shape
            sizeX = test_case.shape
            if(len(sizeX) < 2):
                if(sizeModel[1] != sizeX[0]):
                    print("Error: there must be the same number of features in the model and X")
                res = self.KNNpredict(model, test_case)
            else:
                if(sizeModel[1] != sizeX[1]):
                    print("Error: there must be the same number of features in the model and X")
                N = sizeX[0]
                res = np.zeros((N,1))
                for n in range(N):
                    ans = self.KNNpredict(model, test_case[n,:])
                    res[n,:] = ans
            return res
        print("Error: unknown KNN mode: need train or predict")
        
    def KNNpredict(self,
                   model, test_case):
        # model contains trainX which is NxD, trainY which is Nx1, K which is int. X is 1xD
        # We return a singe value 'y' which is the predicted class

        #TODO: write this function
        X = model['X']
        sizeX = X.shape
        Y = model['Y']
        # get the top K [label,dist] pairs
        distances = []
        for i in range(sizeX[0]):
            dist = sciDist.euclidean(test_case, X[i,:])
            distances.append([Y[i][0], dist])

        #You have an array of labels in distances
        distances = np.array(distances)

        #sort the array on distances
        distances = distances[distances[:,1].argsort()]

        #get the top K labels
        neighbors = distances[0:model['K']]

        mostCommon = stats.mode(neighbors[:,0])

        #return the mode of the labels
        return mostCommon[0][0]

        