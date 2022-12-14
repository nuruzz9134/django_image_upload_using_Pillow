from django.db import models

class Image(models.Model):
    img = models.ImageField(upload_to="ImageStoreFiles")

# Remember it that after uploding image all filtered images are stored into "ImageStoreFiles"