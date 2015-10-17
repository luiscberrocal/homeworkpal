from django.contrib import admin

# Register your models here.
from .models import School, SchoolLevel, Teacher, Student, Homework, Subject


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'due_date', 'school', 'subject', 'teacher', 'evaluation')
    list_editable = ('due_date',)

    def school(self, obj):
        return obj.subject.school_level.school


class SchoolLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'name')
    list_editable = ('name',)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'school_level', 'name')

    def school(self, obj):
        return obj.school_level.school


admin.site.register(School)
admin.site.register(SchoolLevel, SchoolLevelAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Subject, SubjectAdmin)

