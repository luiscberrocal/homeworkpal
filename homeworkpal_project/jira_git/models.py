from django.db import models

# Create your models here.

class StashProject(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name

class StashRepository(models.Model):
    name = models.CharField(max_length=60, unique=True)
    project = models.ForeignKey(StashProject)
    software_name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.software_name


