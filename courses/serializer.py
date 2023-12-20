from rest_framework import serializers
from .models import Course, Subtitle, Content, Feedback

class ContentSerializer(serializers.ModelSerializer):
        
    steps = serializers.SerializerMethodField()
    
    def get_steps(self, obj):
        list = [] 
        for step in obj.steps.all():
            list.append(step.text)
        return list
    class Meta:
        model = Content
        fields = ['id', 'opening', 'closing', 'steps']

class SubtitleSerializer(serializers.ModelSerializer):
    
    content = serializers.SerializerMethodField()
    
    def get_content(self, obj):
        content_obj = Content.objects.get(subtitle=obj)
        serializer = ContentSerializer(content_obj)
        return serializer.data
    class Meta:
        model = Subtitle
        fields = ['id', 'topic', 'shortdesc', 'is_done', 'content']

class CourseSerializer(serializers.ModelSerializer):
    
    lessons = serializers.SerializerMethodField()
    subtitles = serializers.SerializerMethodField()
    
    def get_lessons(self, obj):       
        return obj.subtitles.count()
    
    def get_subtitles(self, obj):
        subtitle = obj.subtitles.all()
        serializer = SubtitleSerializer(subtitle, many=True)
        return serializer.data
    
    class Meta:
        model = Course
        fields = ['title', 'desc', 'type_activity', 'theme_activity', 'duration', 'lessons', 'subtitles']

class CourseDashboard(serializers.ModelSerializer):
    
    total_lessons = serializers.SerializerMethodField()
    
    def get_total_lessons(self, obj):
        return obj.subtitles.count()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'duration', 'total_lessons', 'is_done']

class CourseProgressSerializer(serializers.ModelSerializer):
    
    progress = serializers.SerializerMethodField()
    
    def get_progress(self, obj):
        subtitle = obj.subtitles.all()
        total = subtitle.count()
        done = subtitle.filter(is_done=True).count()
        if total == 0:
            return "0 %"
        else:
            percentage = int((done/total)*100)
            return f"{percentage} %"
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'duration', 'is_done', 'progress']
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'text', 'sentiment', 'rating']


class CourseFeedbackSerializer(serializers.ModelSerializer):
        
    feedback = serializers.SerializerMethodField()
    
    def get_feedback(self, obj):
        feedback_obj = Feedback.objects.filter(course=obj)
        serializer = FeedbackSerializer(feedback_obj, many=True)
        return serializer.data
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'feedback']
        
class CourseDescListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'desc']