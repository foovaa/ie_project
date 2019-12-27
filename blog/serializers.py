from rest_framework import serializers
from .models import Employees

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['name', 'last_name', 'age', 'salary', 'tele', 'address', 'national_id', 'personal_id', 'is_married', 'gender']

