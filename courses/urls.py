from django.urls import path
from .views import *
urlpatterns = [
    # dashboard
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    
    # mark as done subtitle
    path('subtitle/<str:subtitle_id>/', UpdateSubtitle.as_view(), name='update-subtitle'),
    
    # all course 
    path('course/', CourseListView.as_view(), name='all-course'),
    
    # my course
    path('my-course/', MyCourseListView.as_view(), name='my-course'),
    
    # detail course
    path('course/<str:course_id>', DetailCourse.as_view(), name='update-course'),
       
    # get all course feedback
    path('feedback', CourseFeedback.as_view(), name='feedback-course'),
    
    # get detail course feedback
    path('feedback/<str:course_id>', CourseFeedbackDetail.as_view(), name='feedback-course-detail'),
]
