from django.db import models
import os

# Create your models here.

class ImgModel(models.Model):
    img = models.ImageField(upload_to = "imagess/")
    
    def filename(self):
        return os.path.basename(self.img.name)
