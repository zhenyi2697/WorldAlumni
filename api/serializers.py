from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers
from social_auth.models import UserSocialAuth

from backend.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserSocialAuthSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserSocialAuth
        fields = ('id', 'provider', 'uid', 'user')

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'sid')

class BindingSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    schools = SchoolSerializer(many=True)

    class Meta:
        model = Binding
        fields = ('id', 'bind_from', 'create_time', 'modify_time', 'user', 'schools')

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('id', 'binding', 'school', 'type', 'attend_year', 'finish_year')

