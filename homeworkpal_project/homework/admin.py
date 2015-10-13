from django.contrib import admin

# Register your models here.
from .models import School, SchoolLevel, Teacher, Student, Homework, Subject

admin.site.register(School)
admin.site.register(SchoolLevel)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Homework)
admin.site.register(Subject)

