from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from youtube_api import YouTubeDataAPI
from firebase_admin import auth

class YoutubeAPIView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()  # Mendapatkan token dari header
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            prompt = request.data.get('prompt', '')
            if not prompt:
                raise ValueError("Field 'prompt' is required.")
            print(prompt)

            api_key = settings.YT_API_KEY
            yt = YouTubeDataAPI(api_key)
            obj = yt.search(
                q=prompt,
                max_results=3,
            )
            data = []
            
            for i in range(len(obj)):
                                
                data.append({
                    'id': obj[i]['video_id'],
                    'title': obj[i]['video_title'].replace('&quot;', "'"),
                    'channel': obj[i]['channel_title'],
                    'link' : f'https://www.youtube.com/watch?v={obj[i]["video_id"]}'
                })
            
            return Response({
                'videos': data,
            })
        except auth.InvalidIdTokenError as e:
            return Response({"error": "Invalid token"}, 401)