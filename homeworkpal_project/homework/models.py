from autoslug import AutoSlugField
from django.conf import settings
from django.db import models

# Create your models here.
from .validators import date_not_past


class School(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', max_length=50, unique=True)

    def __str__(self):
        return self.name

class SchoolLevel(models.Model):
    name = models.CharField(max_length=10)
    slug = AutoSlugField(populate_from='name', max_length=10, unique=True)
    school = models.ForeignKey(School)

    class Meta:
        unique_together = ('name', 'school')

    def __str__(self):
        return self.name


class SchoolMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    middle_name = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return '%s, %s' % (self.user.last_name, self.user.first_name)
        else:
            return self.user.username


class Teacher(SchoolMember):
    pass


class Student(SchoolMember):
    school = models.ForeignKey(School)
    school_level = models.ForeignKey(SchoolLevel)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', max_length=30)
    school_level = models.ForeignKey(SchoolLevel)
    teacher = models.ForeignKey(Teacher)

    class Meta:
        unique_together = ('slug', 'school_level')

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
    due_date = models.DateField(validators=[date_not_past])
    description = models.TextField()
    evaluation = models.CharField(max_length=3,choices=HOMEWORK_TYPES)
    teacher = models.ForeignKey(Teacher)

    def __str__(self):
        return '%s - %s' % (self.subject.name, self.description)