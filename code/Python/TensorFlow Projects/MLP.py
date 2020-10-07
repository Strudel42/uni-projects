import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt


fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data() # load data

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'] # Create class names for label space

train_images = train_images / 255.0 #Scale values to between 0 and 1
test_images = test_images / 255.0

#This is the shape of our model.
# An input layer that is 784 nodes wide
# Next a 128 node wide layer for our feature maps
#Then we have 10 nodes in our label space for catgorisation
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.keras.layers.LeakyReLU(alpha=0.01)),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(40,activation=tf.keras.layers.LeakyReLU(alpha=0.01)),
    keras.layers.Dense(10)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

history = model.fit(train_images, train_labels,verbose=2, epochs=20,validation_data=(test_images,test_labels))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss=history.history['loss']
val_loss=history.history['val_loss']

plt.figure(1)
plt.plot(history.history['accuracy'],"y")
plt.plot(history.history['val_accuracy'],"m")
plt.title('Accuracy of Model')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training', 'Test'], loc='lower right')
plt.grid()

plt.figure(2)
plt.plot(history.history['loss'],"y")
plt.plot(history.history['val_loss'],"m")
plt.title('Loss of Model')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training', 'Test'], loc='upper right')
plt.grid()
plt.show()

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()











#model_2 = keras.Sequential([
#    keras.layers.Flatten(input_shape=(28, 28)),
#    keras.layers.Dense(512, activation='relu'),
#    keras.layers.Dropout(0.2),
#    keras.layers.Dense(10)
#])
#
#model_2.compile(optimizer='adam',
#              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#              metrics=['accuracy'])
#
#model_2.fit(train_images, train_labels,verbose=2, epochs=10)
#
#test_loss_2, test_acc_2 = model_2.evaluate(test_images,  test_labels, verbose=2)
#
#print('\nTest accuracy:', test_acc_2,' Test loss:',test_loss_2)