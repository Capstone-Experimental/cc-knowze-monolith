from django.urls import path
from .views import *
from .youtube import YoutubeAPIView
# from .sse import OpenAIStream

urlpatterns = [
    # generate course
    path('generate/', Generate.as_view(), name='generate'),
    
    # get prompt recommendation
    path('recommendation', RecommendationsAPIView.as_view(), name='recommendation'),
    
    # get keyword trending
    path('keyword-trending', WeeklyTrendingKeywordView.as_view(), name='keyword-trending'),
    
    # put a feedback course
    path('feedback/<str:course_id>/', SentimentAnalysisView.as_view(), name='feedback-course'),
    
    # get video
    path('video/', YoutubeAPIView.as_view(), name='video'),
    
    # get a intro wikihow
    path('intro', IntrosAPIView.as_view(), name='intro'),
    
    # test
    path('test', TestAPIView.as_view(), name='test'),
]