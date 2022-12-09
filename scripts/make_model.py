#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[2]:


import tensorflow as tf
import os


# In[3]:


gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus: 
    tf.config.experimental.set_memory_growth(gpu, True)


# In[4]:





# In[5]:


import numpy as np
from matplotlib import pyplot as plt


# In[6]:


data = tf.keras.utils.image_dataset_from_directory('data')


# In[7]:


data_iterator = data.as_numpy_iterator()


# In[8]:


batch = data_iterator.next()


# In[9]:


fig, ax = plt.subplots(ncols=4, figsize=(20,20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])


# In[10]:


data = data.map(lambda x,y: (x/255, y))


# In[20]:


data.as_numpy_iterator().next()


# In[21]:


train_size = int(len(data)*.7)
val_size = int(len(data)*.2)
test_size = int(len(data)*.1)


# In[23]:


train = data.take(train_size)
val = data.skip(train_size).take(val_size)
test = data.skip(train_size+val_size).take(test_size)


# In[25]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout


# In[26]:


model = Sequential()


# In[27]:


model.add(Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)))
model.add(MaxPooling2D())
model.add(Conv2D(32, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(16, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(116, activation='softmax'))


# In[28]:


model.compile('adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# In[30]:


logdir='logs'


# In[31]:


tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)


# In[32]:


hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboard_callback])


# In[35]:


from tensorflow.keras.metrics import Precision, Recall, SparseCategoricalAccuracy


# In[52]:


pre = Precision()
re = Recall()
acc = SparseCategoricalAccuracy()


# In[53]:


for batch in test.as_numpy_iterator(): 
    X, y = batch
    yhat = model.predict(X)
    acc.update_state(y, yhat)


# In[54]:


print(acc.result())


# In[55]:


import cv2


# In[63]:


img = cv2.imread('7317z1.jpg')


# In[64]:


resize = tf.image.resize(img, (256,256))


# In[65]:


yhat = model.predict(np.expand_dims(resize/255, 0))


# In[66]:


path = os.path.join(os.getcwd(), 'data')
template_names = os.listdir(path)
template_names[np.argmax(yhat)]


# In[67]:


from tensorflow.keras.models import load_model


# In[68]:


model.save(os.path.join('models','memeclassifier.h5'))


# In[ ]:




