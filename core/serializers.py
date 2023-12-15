from rest_framework import serializers
from .models import History,Result

class HistorySerializer(serializers.ModelSerializer):
   class Meta:
     model = History
     fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
   class Meta:
     model = Result
     fields = ['word','label_group']