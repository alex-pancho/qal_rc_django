from . models import Course
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__" # [ліст полів, що треба показати]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Назва курсу занадто коротка."
            )
        return value