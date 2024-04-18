from django.db import models

# Create your models here.


class TodoList (models.Model):
    header = models.CharField(max_length=100)
    description = models.CharField(max_length=60)

    def __str__(self):
        return {self.header}
