from autoslug import AutoSlugField
from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', max_length=50)

    def __str__(self):
        return self.name


class SchoolLevel(models.Model):
    name = models.CharField(max_length=10)
    slug = AutoSlugField(populate_from='name', max_length=5)
    school = models.ForeignKey(School)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', max_length=30)
    school_level = models.ForeignKey(SchoolLevel)

    def __str__(self):
        return '%s (%s)' % (self.name, self.school_level.name)


class Homework(models.Model):
    SUMMATIVE_TYPE = 'SUM'
    FORMATIVE_TYPE = 'FRM'
    HOMEWORK_TYPES = (
        (SUMMATIVE_TYPE, 'Summative'),
        (FORMATIVE_TYPE, 'Formative')
    )
    subject = models.ForeignKey(Subject)
    due_date = models.DateField()
    description = models.TextField()
    evaluation = models.CharField(max_length=3,choices=HOMEWORK_TYPES)

