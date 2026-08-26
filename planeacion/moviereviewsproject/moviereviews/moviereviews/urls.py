from django.contrib import admin
from django.urls import path, include
from movie import views as movieviews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movieviews.home, name='home'),
    path('about/', movieviews.about, name='about'),
    path('news/', include('news.urls')),
    path('statistics/', movieviews.statistics_view, name='statistics'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)