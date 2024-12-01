from rest_framework import serializers
from .models import ScrapedData

class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        # fields = ['url', 'title', 'content', 'ScrapedAt']
        fields = '__all__'