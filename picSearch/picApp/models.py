from django.db import models

class MissingChild(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    image = models.ImageField(upload_to='')
    image_encoding = models.BinaryField()
    date_missing = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    last_seen = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=50)

    class Meta:
        unique_together = ('name', 'age', 'gender', 'date_missing')