from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .scrap import get_element_by_classname, driversetup
from datetime import datetime
import json
from .models import *
from .serializer import *

class ScrapNewsView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        url = 'https://www.detik.com/tag/gen-z'
        className = "title"
        driver = driversetup() 
        str_trending = get_element_by_classname(url, driver, className)
        
        list_trending = json.loads(str_trending)
        print(list_trending)
        formatted_data = []
        for item in list_trending[:3]:
            title = item['title']
            desc = item['desc']
            image_url = item['image_url']
            created_at = datetime.now()

            trending_news = News.objects.create(title=title, desc=desc, img_url=image_url, created_at=created_at)
            trending_news.save()

            formatted_data.append({
                'title': title,
                'desc': desc,
                'img_url': image_url,
                'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        serializer = TrendingNewsSerializer(data=formatted_data, many=True)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)

class TrendingNewsView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        qs = News.objects.all().order_by('-created_at')[:3]
        serializer = TrendingNewsSerializer(qs, many=True)
        return Response(serializer.data)
        