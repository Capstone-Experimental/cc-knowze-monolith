from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from courses.models import Course, Subtitle, Content, Steps
from .serializer import *
from util.pagination import ApiPagination


class Dashboard(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        name = request.user.username
        
        f1_progress = Course.objects.filter(user=request.user, is_done=False)
        f2_progress = CourseProgressSerializer(f1_progress, many=True)
        list_progress = f2_progress.data
        
        f1_course = Course.objects.filter(user=request.user)
        f2_course = CourseDashboard(f1_course, many=True)
        list_course = f2_course.data
        
        course_finished = len(list(filter(lambda x: x['is_done'] == True, list_course)))
        course_progress = len(list(filter(lambda x: x['is_done'] == False, list_course)))
        
        return Response(
            {
                "title": name,
                "img" : request.user.img,
                "progress" : list_progress,
                "courses" : list_course,
                "course_completed" : course_finished,
                "course_progress" : course_progress,
            }
        )
    

class DetailCourse(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, user=request.user)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
class UpdateSubtitle(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, subtitle_id):
        # subtitle = Subtitle.objects.get(id=subtitle_id, course__user=request.user)
        subtitle = get_object_or_404(Subtitle, id=subtitle_id, course__user=request.user)
        subtitle.is_done = True
        subtitle.save()
        
        # if all subtitle is done then course is done
        course = subtitle.course
        
        if course.subtitles.filter(is_done=False).count() == 0:
            course.is_done = True
            course.save()
        
        return Response({"message": "Subtitle Updated"})
    
class CourseFeedback(generics.GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = ApiPagination
    
    def get(self, request):
        course = Course.objects.all()
        paginate_queryset = self.paginate_queryset(course)
        serializer = CourseFeedbackSerializer(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    

class CourseListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = ApiPagination
    serializer_class = CourseDescListSerializer
    queryset = Course.objects.all()
    
class CourseFeedbackDetail(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseFeedbackSerializer(course)
        return Response(serializer.data)
    
class MyCourseListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ApiPagination
    serializer_class = CourseDescListSerializer
    
    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)