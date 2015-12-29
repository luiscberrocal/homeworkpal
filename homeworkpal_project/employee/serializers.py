from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Employee, CompanyGroup

__author__ = 'LBerrocal'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'last_name', 'first_name',  'username', 'email', 'groups')


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'middle_name', 'company_id', 'tenure', 'projects')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CompanyGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompanyGroup
        fields =  ('name', 'description', 'parent_group', 'slug',)