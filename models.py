from django.db import models

class student(models.Model):
    rollnumber=models.IntegerField()
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    mark=models.IntegerField()
    address=models.CharField(max_length=100)
    def __str__(self):
        return self.name


# Create your models here.
