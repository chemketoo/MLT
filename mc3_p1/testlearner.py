"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import KNNLearner as knn
import BagLearner as bl

if __name__ == "__main__":
    inf = open('Data/ripple.csv')
    data = np.array([map(float, s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    train_rows = math.floor(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    total = 3

    for i in range(total):
        if i == 0:
            print "LinRegLearner"
            learner = lrl.LinRegLearner()  # create a LinRegLearner
        elif i == 1:
            print "KNNLearner"
            learner = knn.KNNLearner(k=3)  # create a KNNLearner
        else:
            print "BagLearner"
            learner = bl.BagLearner(learner=knn.KNNLearner, kwargs={"k": 3}, bags=20, boost=False)  # create a BagLearner

        learner.addEvidence(trainX, trainY)  # train it

        # evaluate in sample
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        print
        print "In sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(predY, y=trainY)
        print "corr: ", c[0, 1]

        # evaluate out of sample
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        print
        print "Out of sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(predY, y=testY)
        print "corr: ", c[0, 1]
        print
