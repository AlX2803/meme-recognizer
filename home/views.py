from django.shortcuts import render
import cv2
from .forms import ImgForm
from .models import ImgModel
import os
from tensorflow.python.keras.models import load_model
import tensorflow as tf
import numpy as np


# Create your views here.

def home(request):
    context = {}
    
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("select_a_meme")
            obj = ImgModel.objects.create(img = img)
            obj.save()
            
            img_name = obj.filename()
            img = cv2.imread(os.path.join('imagess', img_name))
            
            resize = tf.image.resize(img, (256,256))
            new_model = load_model(os.path.join('models','memeclassifier.h5'))
            yhat = new_model.predict(np.expand_dims(resize/255, 0))
            path = os.path.join(os.getcwd(), 'data')
            template_names = os.listdir(path)
            
            context['template'] = template_names[np.argmax(yhat)+1]
            
            template_path = os.path.join('memes_templates', template_names[np.argmax(yhat)+1])
            template_path = os.path.join(template_path, '0.jpg')
            context['template_path'] = template_path
                
    else:
        form = ImgForm()
    context['form'] = form
    
    return render(request, 'home.html', context)