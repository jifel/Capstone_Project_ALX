from rest_framework import serializers
from tracker.models import Issue

# Serializer converts Django model instances into JSON (and back).
# This lets the API talk in JSON instead of Python objects.
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'   # include all fields from the Issue model
