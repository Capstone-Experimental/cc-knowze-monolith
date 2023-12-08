from django.contrib import admin
from .models import Keyword, News

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('text', 'count', 'created_at')
    list_editable = ('count',)

admin.site.register(Keyword, KeywordAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('no', 'title', 'img_url')
    list_editable = ('title', 'img_url')
    
admin.site.register(News, NewsAdmin)