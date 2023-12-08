from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import status
from courses.serializer import FeedbackSerializer, CourseSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from .intro import get_intros
from .brain import get_completion2
from .ner import detect_entities
from .models import Keyword
from .recommendation import append_data_to_csv_in_gcs, retrain_model_and_upload, get_recommendations
# from .sentiment import SentimentAnalyzer
from util.ratelimiter import MyDailyThrottle, MyMinuteThrottle
import json
from json.decoder import JSONDecodeError

from courses.models import Course, Subtitle, Content, Steps, Feedback
from firebase_admin import auth

class Generate(APIView):
    throttle_classes = [MyMinuteThrottle, MyDailyThrottle]

    def post(self, request, format=None):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()  # Mendapatkan token dari header
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            prompt = request.data.get('prompt')
            
            if Course.objects.filter(prompt=prompt, user=uid).exists():
                return Response(
                    {
                        "error": "topic sudah ada"
                    },400
                )
                
            if Course.objects.filter(user=uid).count() >= 2:
                return Response(
                    {
                        "error": "course sudah mencapai batas"
                    },404
                )
            json_str = get_completion2(prompt=prompt)
            
            # print(json_str)
                
            json_obj = json.loads(json_str)
            
            # ner
            trend_keyword = detect_entities(prompt)
            
            
            if trend_keyword:
                if Keyword.objects.filter(text=trend_keyword).exists():
                    keyword = get_object_or_404(Keyword, text=trend_keyword)
                    keyword.count += 1
                    keyword.save()
                else:
                    Keyword.objects.create(
                        text=trend_keyword,
                        count=1
                    )
            
            # print(json_obj)
            title = json_obj['title']
            desc = json_obj['desc']
            duration = json_obj['duration']
            
            
            type_activity = json_obj['type_activity']
            theme_activity = json_obj['theme_activity'] 
            
            with transaction.atomic():
                course_create = Course.objects.create(
                    user=uid,
                    type_activity=type_activity,
                    theme_activity=theme_activity,
                    prompt=prompt,
                    title=title,
                    desc=desc,
                    duration=duration,
                    is_done=False,
                    created_at=timezone.now()
                )
                
                for subtitle in json_obj['subtitles']:
                    subtitle_instance = Subtitle.objects.create(
                    # Subtitle.objects.create(
                        topic=subtitle['topic'],
                        shortdesc=subtitle['shortdesc'],
                        course=course_create,
                        is_done=False
                    )
                    content = subtitle['content']
                    content_instance = Content.objects.create(
                        opening=content['opening'],
                        closing=content['closing'],
                        subtitle=subtitle_instance
                    )

                    for step in content['step']:
                        Steps.objects.create(
                            text=step,
                            content=content_instance
                        )
                append_data_to_csv_in_gcs('go-mono', 'csv/data_recom.csv', prompt, type_activity, theme_activity, desc)      
                retrain_model_and_upload('go-mono', 'csv/data_recom.csv', 'model/recom-v1.pkl')
                # with open('csv/data_recom.csv', 'a') as f:
                #     f.write(f'{prompt},{type_activity},{theme_activity},{desc}\n')
            # print(json_obj)
            return Response({
                "message": "course berhasil dibuat",
                "course_id": course_create.id,
            },200)
        except auth.InvalidIdTokenError as e:
            return Response({"error": "Invalid token"}, 401)
        
        except JSONDecodeError:
            return Response({"error": "Terjadi kesalahan dalam format JSON"}, 400)

        except ValidationError as ve:
            return Response({"error": f"Validasi gagal: {ve}"}, 400)

        except Exception as e:
            return Response({"error": f"Terjadi kesalahan server: {e}"}, 500)
        

# NER Keyword
class WeeklyTrendingKeywordView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        keywords = Keyword.objects.all().order_by('-count')[:5]
        data = []
        for keyword in keywords:
            data.append(keyword.text)
        dict = {
            "keywords": data
        }
        return Response(dict, 200)
    
# Senfiment Analysis in Feedback
class SentimentAnalysisView(generics.GenericAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = FeedbackSerializer 
    # sentiment_analyzer = SentimentAnalyzer('model/sentimen.keras') 

    def post(self, request, course_id, *args, **kwargs):
        try:
            course = get_object_or_404(Course, id=course_id)
            text = request.data.get('text', '')
            rating = request.data.get('rating')
            if not text:
                raise ValueError("Field 'text' is required.")
            if rating and (rating < 1 or rating > 5):
                raise ValueError("Field 'rating' must be between 1 and 5.")
            if not rating:
                raise ValueError("Field 'rating' is required.")

            sentiment_result = 'positif'
            # sentiment_result = self.sentiment_analyzer.analyze_sentiment(text)
            print(text)
            try :
                Feedback.objects.create(
                    course=course,
                    text=text,
                    rating=rating,
                    sentiment=sentiment_result
                    )
                course.avg_rating = course.feedbacks.all().aggregate(models.Avg('rating'))['rating__avg']
                course.save()
            except Exception as e:
                print(e)
                return Response({'error': 'error'}, 400)

            return Response({
                'message': 'Feedback berhasil disimpan.'
            })

        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, 400)

# Recommendation
class RecommendationsAPIView(generics.GenericAPIView):
    
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()
        try:
        # last = Course.objects.filter(user=request.user).order_by('created_at').first().prompt
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            last = Course.objects.filter(user=uid).order_by('-created_at').first()
            # print(len(Course.objects.filter(user=request.user)))
            if not last:
                return Response({'recommendations': []})
            last = last.prompt
            print(last)
            
            recommendations = get_recommendations(last)
            return Response({'recommendations': recommendations})
        except auth.InvalidIdTokenError as e:
            return Response({"error": "Invalid token"}, 401)
        except IndexError:
            return Response({'recommendations': []})
        # serializer = CourseSerializer(last, many=False)
        # return Response(serializer.data, 200)
        
# Intros
class IntrosAPIView(generics.GenericAPIView):
    
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            prompt = request.data.get('prompt')
            intros = get_intros(prompt, 2)
            return Response({'intros': intros})
        except IndexError:
            return Response({'intros': []})
        # serializer = CourseSerializer(last, many=False)
        # return Response(serializer.data, 200)
        

class TestAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [MyDailyThrottle, MyMinuteThrottle]
    
    def get(self, request):
        return Response({'message': 'Hello World!'})