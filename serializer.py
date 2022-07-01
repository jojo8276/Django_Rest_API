from rest_framework import serializers
from .models import student

# class Sample(serializers.Serializer):
#     rollnumber = serializers.IntegerField()
#     name = serializers.CharField(max_length=50)
#     age = serializers.IntegerField()
#     mark = serializers.IntegerField()
#     address = serializers.CharField(max_length=100)
#

class Sample(serializers.ModelSerializer):
    class Meta:
        model=student
        fields = '__all__'