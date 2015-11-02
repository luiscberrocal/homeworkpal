from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Employee

__author__ = 'LBerrocal'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', 'middle_name', 'company_id', 'tenure', 'projects')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
