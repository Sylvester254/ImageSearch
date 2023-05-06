from django.db import models

class MissingChild(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    image = models.ImageField(upload_to='missing_children/')
    image_encoding = models.BinaryField()
    date_missing = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    last_seen = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=50)
