from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from courses.models import Course, Subtitle, Content, Steps
from .serializer import *
from util.pagination import ApiPagination
from firebase_admin import auth

class Dashboard(APIView):
    
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()  # Mendapatkan token dari header

        try:
            decoded_token = auth.verify_id_token(id_token)
            user_name = decoded_token.get('name')
            uid = decoded_token.get('uid')
            picture = decoded_token.get('picture')
            # id = decoded_token.get('user_id')

            # f1_progress = Course.objects.filter(user=request.user, is_done=False)
            
            # fix
            f1_progress = Course.objects.filter(is_done=False, user=uid)
            # f1_progress = Course.objects.filter(is_done=False)[:3]
            f2_progress = CourseProgressSerializer(f1_progress, many=True)
            list_progress = f2_progress.data
            
            # f1_course = Course.objects.filter(user=request.user)
            #fix
            f1_course = Course.objects.filter(user=uid)
            # f1_course = Course.objects.all()[:3]
            f2_course = CourseDashboard(f1_course, many=True)
            list_course = f2_course.data
            
            course_finished = len(list(filter(lambda x: x['is_done'] == True, list_course)))
            course_progress = len(list(filter(lambda x: x['is_done'] == False, list_course)))
            
            return Response(
                {
                    "name": user_name,
                    "img" : picture,
                    "progress" : list_progress,
                    "courses" : list_course,
                    "course_completed" : course_finished,
                    "course_progress" : course_progress,
                }
            )
        
        except auth.InvalidIdTokenError as e:
            # Handle error jika token tidak valid
            return Response({"error": "Invalid token"}, 401)
        
        
class DetailCourse(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()  # Mendapatkan token dari header

        try:
            decoded_token = auth.verify_id_token(id_token)
            # user_name = decoded_token.get('name')
            uid = decoded_token.get('uid')
            # picture = decoded_token.get('picture')
            course = get_object_or_404(Course, id=course_id, user=uid)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except auth.InvalidIdTokenError as e:
            # Handle error jika token tidak valid
            return Response({"error": "Invalid token"}, 401)
    
class UpdateSubtitle(APIView):
    
    # permission_classes = [IsAuthenticated]
    
    def put(self, request, subtitle_id):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()  # Mendapatkan token dari header
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            # user_name = decoded_token.get('name')
            uid = decoded_token.get('uid')
            # picture = decoded_token.get('picture')
        # subtitle = Subtitle.objects.get(id=subtitle_id, course__user=request.user)
            subtitle = get_object_or_404(Subtitle, id=subtitle_id, course__user=uid)
            subtitle.is_done = True
            subtitle.save()
            
            # if all subtitle is done then course is done
            course = subtitle.course
            
            if course.subtitles.filter(is_done=False).count() == 0:
                course.is_done = True
                course.save()
            
            return Response({"message": "Subtitle Updated"})
        except auth.InvalidIdTokenError as e:
            # Handle error jika token tidak valid
            return Response({"error": "Invalid token"}, 401)
    
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
    
class MyCourseListView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    pagination_class = ApiPagination
    serializer_class = CourseDescListSerializer
    
    def get(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()  # Mendapatkan token dari header
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            # user_name = decoded_token.get('name')
            uid = decoded_token.get('uid')
            # picture = decoded_token.get('picture')
            obj = Course.objects.filter(user=uid)
            serializer = CourseDescListSerializer(obj, many=True)
            paginate_queryset = self.paginate_queryset(obj)
            return self.get_paginated_response(serializer.data)
        except auth.InvalidIdTokenError as e:
            # Handle error jika token tidak valid
            return Response({"error": "Invalid token"}, 401)