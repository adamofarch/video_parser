from django.db import models

# Create your models here.

class Vid(models.Model):
    vid_name = models.CharField(max_length=50)
    vid_file = models.FileField(upload_to='')

    def __str__(self):
        return self.vid_name
