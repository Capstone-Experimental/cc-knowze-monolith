from django.contrib import admin
from .models import Course, Subtitle, Content, Steps, Feedback


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'is_done', 'created_at', 'avg_rating')
    list_editable = ('is_done',)
    
admin.site.register(Course, CourseAdmin)

class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'course', 'is_done')
    list_editable = ('is_done',)

admin.site.register(Subtitle, SubtitleAdmin)
admin.site.register(Content)
admin.site.register(Steps)
admin.site.register(Feedback)