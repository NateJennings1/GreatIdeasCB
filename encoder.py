import tensorflow as tf
from tensorflow.keras import layers, losses
from tensorflow.keras.models import Model
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

class deepEncoder(Model):
    
    def __init__(self,latentSize,encodeLayers,inputSize):
        super(deepEncoder,self).__init__()
        
        
        # Input layer
        self.encoder = tf.keras.Sequential([
            layers.Input(shape=inputSize),
        ])
        # Encoding layers
        for depth in range(encodeLayers):
            size = latentSize * 2 ** (encodeLayers-depth)
            self.encoder.add(layers.Dense(size,activation='relu'))
        # Latent layer
        self.encoder.add(layers.Dense(latentSize))
        
        # Decoding layers
        self.decoder = tf.keras.Sequential()
        for depth in range(encodeLayers):
            size = latentSize * 2 ** (depth+1)
            self.decoder.add(layers.Dense(size,activation='relu'))
        # Output
        self.decoder.add(layers.Dense(inputSize[0]))

    def call(self,x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class mlp(Model):
    def __init__(self,dims,inputShape):
        super(mlp,self).__init__()

        # Input layer
        self.model = tf.keras.Sequential([
            layers.Input(shape=inputShape),
        ])
        
        # Hidden layers
        for dim in dims:
            self.model.add(layers.Dense(dim,activation='relu'))
        
        # Output layer
        self.model.add(layers.Dense(2,activation='sigmoid'))

    def call(self,x):
        return self.model(x)

def main():
    # Load marker/abundance data
    path = './processed data'
    abundanceData = pd.read_pickle(path+'/abundance.pickle')
    markerData = pd.read_pickle(path+'/marker.pickle')
    labels = pd.read_pickle(path+'/forbidden.pickle')

    categories = {'cancer':1,'small_adenoma':0,'n':0}
    
    # Binary lable
    diseaseStatus = labels.loc['disease'].replace(categories).to_numpy().reshape(-1,1)

    # Or as separate dimensions
    diseaseStatus = np.concatenate((np.where(diseaseStatus==1,1,0),np.where(diseaseStatus==0,1,0)),axis=1)

    abundanceData = np.transpose(abundanceData.to_numpy()).astype('float64')

    markerData = np.transpose(markerData.to_numpy()).astype('int32')


    a_train,a_test,m_train,m_test,y_train,y_test = train_test_split(abundanceData,markerData,diseaseStatus,train_size=0.8,stratify=diseaseStatus)




    # Training 
    inputShape = (m_train.shape[1],)
    latent = 64
    depth = 0
    ae = deepEncoder(latent,2,inputShape)
    ae.compile(optimizer='adam', loss=losses.MeanSquaredError())
    #history = ae.fit(m_train,m_train,epochs=10,batch_size=4,verbose=1,shuffle=True,validation_data=(m_test,m_test))
    #loss = history.history['val_loss'][-1]
    #ae.save(f'savedModels/markerDeepEncoder{latent}-{depth}-loss-{round(loss,2)}')
    #ae = tf.keras.models.load_model('savedModels/abundanceDeepEncoder64-loss-0.49')
    #aEncoded_train = ae.encoder.predict(a_train)
    #aEncoded_test = ae.encoder.predict(a_test)
    me = tf.keras.models.load_model('savedModels/markerDeepEncoder64-0-loss-0.08')
    mEncoded_train = me.encoder.predict(m_train)
    mEncoded_test = me.encoder.predict(m_test)


    # MLP Output
    inputShape = (64,)
    dims = [32,32,32]
    diseaseModel = mlp(dims,inputShape)
    diseaseModel.compile(optimizer='adam',loss=losses.binary_crossentropy,metrics='accuracy')
    history = diseaseModel.fit(mEncoded_train,y_train,epochs=40,batch_size=4,verbose=1,shuffle=True,validation_data=(mEncoded_test,y_test))



if __name__ == '__main__':
    main()
        