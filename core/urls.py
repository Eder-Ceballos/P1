from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('api/', include('transacciones.urls')),
    
    # Captura cualquier otra ruta (como /login, /dashboard, etc.) y entrega el index.html de React
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
