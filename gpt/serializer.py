from rest_framework import serializers
from .models import News

class TrendingNewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'img_url')
