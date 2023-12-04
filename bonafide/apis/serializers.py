# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import BonafideManagement


# Create a model serializer
class BonafideManagementSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = BonafideManagement
        fields = ("title", "description")
