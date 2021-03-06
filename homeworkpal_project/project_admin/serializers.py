from rest_framework import serializers
from employee.models import CompanyGroup
from .models import ProjectMember, Project

__author__ = 'lberrocal'


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ('role', 'employee', 'project', 'start_date', 'end_date')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('pk', 'short_name', 'description', 'planned_start_date', 'planned_end_date',
                  'actual_start_date', 'actual_end_date', 'slug', 'planned_man_hours',
                  'group', 'priority')
