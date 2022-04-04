import numpy as np
import pandas as pd

# Gets the abundance vectors of species 
# (rows with label kingdom_|phylum_|...|species_) for abundance
# (rows label )
# (columns are each individual)
# The categorical labels are identical for abundance and marker data
# The individuals occur in the same column in each dataset
def getData(path):
    f = open(path,'r')
    data = f.read().splitlines()
    
    bacteriaVectors = []
    bacteriaLabels = []
    startLine = 211 # Where the bacterial abundances start
    for lineNum in range(startLine,len(data)):
        line = data[lineNum]
        rowVector = line.split('\t')
        bacteriaVectors.append(rowVector[1:])
        bacteriaLabels.append(rowVector[0])

    categoricalVectors = []
    categoricalLabels = []
    for lineNum in range(0,startLine):
        line = data[lineNum]
        rowVector = line.split('\t')
        if 'nd' in rowVector:
            continue
        else:
            categoricalVectors.append(rowVector[1:])
            categoricalLabels.append(rowVector[0])

    return (np.asarray(bacteriaVectors),np.asarray(bacteriaLabels),
            np.asarray(categoricalVectors),np.asarray(categoricalLabels))

# Returns 4 pandas dataframes: abundance,marker,categorical,forbidden
# and the labels for cancer as a np array
def main():
    # Process for abundance data
    abundancePath = '../processed data/abundance/abundance_Colorectal.txt'
    markerPath = '../processed data/marker/marker_Colorectal.txt'
    bVectors,bLabels,cVectors,cLabels = getData(abundancePath)
    
    
    # Process for marker data
    mVectors,mLabels,cVectors,cLabels = getData(markerPath)
    

    # Process for categorical data
    groundTruth = cVectors[np.where(cLabels=='disease')] # 'n','cancer','small_adenoma'

    print(cLabels) # Not sure which of these has info about cancer we dont want
                   # to give to model
    dataIndices = np.asarray([5,6,10]) # 'age','gender','bmi'
    categoricalVectors = cVectors[dataIndices]
    id = cVectors[1]

    markerData = pd.DataFrame(data=mVectors,index=mLabels,columns=id)
    abundanceData = pd.DataFrame(data=bVectors,index=bLabels,columns=id)
    categoricalData = pd.DataFrame(data=categoricalVectors,
                                    index=cLabels[dataIndices],columns=id)
    forbiddenData = pd.DataFrame(data=cVectors,index=cLabels,columns=id)

    # Save to dir
    pathRoot = '../processed data'
    # Use pandas.read_pickle
    markerData.to_pickle(pathRoot+'/marker.pickle')
<<<<<<< HEAD
    markerData.to_csv(pathRoot+'/marker.csv')
    abundanceData.to_pickle(pathRoot+'/abundance.pickle')
    abundanceData.to_csv(pathRoot+'/abundance.csv')
    categoricalData.to_pickle(pathRoot+'/categorical.pickle')
    categoricalData.to_csv(pathRoot+'/categorical.csv')
    forbiddenData.to_pickle(pathRoot+'/forbidden.pickle')
    forbiddenData.to_csv(pathRoot+'/forbidden.csv')
    # Use np.load
    np.save(pathRoot+'/groundTruth.npy',groundTruth)
    #np.savetxt("groundTruth.csv", groundTruth, delimiter=",")
=======
    abundanceData.to_pickle(pathRoot+'/abundance.pickle')
    categoricalData.to_pickle(pathRoot+'/categorical.pickle')
    forbiddenData.to_pickle(pathRoot+'/forbidden.pickle')
    # Use np.load
    np.save(pathRoot+'/groundTruth.npy',groundTruth)
>>>>>>> 65eed69f83b654a752d3ecc8a83142de8e8310b1
    return markerData,abundanceData,categoricalData,forbiddenData,groundTruth

    

if __name__ == '__main__':
    main()
