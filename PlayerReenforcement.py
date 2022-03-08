from PlayerInterface import PlayerInterface
import tensorflow as tf
from tensorflow import keras
from keras import layers
class PlayerReenforcement(PlayerInterface):
    def __init__(self):
        self.model = keras.Sequential()
        self.model.add(layers.Dense(64, input_dim=9, activation="relu", name="InputLayer"))
        self.model.add(layers.Dense(32, activation="relu", name="HiddenLayer"))
        self.model.add(layers.Dense(32, activation="relu", name="HiddenLayer"))
        self.model.add(layers.Dense(9, activation="sigmoid", name="OutputLayer"))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def makeMove(self, playGrid):
        model = keras.Sequential()
        model.add(layers.Dense(64, input_dim=9, activation="relu", name="InputLayer"))
        model.add(layers.Dense(32, activation="relu", name="HiddenLayer"))
        model.add(layers.Dense(32, activation="relu", name="HiddenLayer"))
        model.add(layers.Dense(9, activation="sigmoid", name="OutputLayer"))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])