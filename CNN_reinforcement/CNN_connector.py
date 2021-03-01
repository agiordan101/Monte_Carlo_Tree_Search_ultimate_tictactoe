import numpy as np
import tensorflow as tf

all_yxs = []
for y in range(9):
	for x in range(9):
		all_yxs.append((y, x))

def convert_game_into_nparray(gameT, sign):
	
	game_np = np.zeros((9, 9))

	for y, x in all_yxs:
		if gameT[y][x] != ' ':
			game_np[y, x] = 1 if gameT[y][x] == sign else -1

	# print(f"gameT: {gameT}")
	# print(f"sign: {sign}")
	# print(f"game_np: {game_np}")
	return game_np


class RLModel:

    def __init__(self, name=None):
		if name:
			self.model = tf.keras.models.load_model(name)
		else:
        	self.model = self.get_model()

	def get_model(self):
		i = tf.keras.layers.Input(shape=(9, 9, 1))
		conv = tf.keras.layers.Conv2D(
			filters=16,
			kernel_size=(3, 3),
			strides=(3, 3),
			activation='relu')(i)
		flatten = tf.keras.layers.Flatten()(conv)
		dense1 = tf.keras.layers.Dense(512, activation='relu')(flatten)
		dense2 = tf.keras.layers.Dense(256, activation='relu')(dense1)

		policy = tf.keras.layers.Dense(81, activation='softmax')(dense2)
		value = tf.keras.layers.Dense(1)(dense2)

		# conv = la
		model = tf.keras.Model(inputs=i, outputs=[policy, value])
		model.summary()
		model.compile(
			loss='CategoricalCrossentropy',
			optimizer='Adam',
			metrics='Accuracy'
		)
		model.summary()
		return model

    def fit(self, features, targets, epochs=20):
        return self.model.fit(features, targets, epochs=epochs)
    
    def predict(self, features):
        return self.model.predict(features)
