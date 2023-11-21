from django.contrib import admin
from django.urls import path, include
# from django.views.static import serve
# from django.conf import settings

urlpatterns = [
    path('adm/', admin.site.urls),

    path('api/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('gpt.urls')),
    
    # path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
