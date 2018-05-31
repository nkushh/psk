from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('facilities.urls', namespace='facilities')),
    path('distribution/', include('distribution.urls', namespace='distribution')),
    path('visits/', include('visits.urls', namespace='visits')),
    path('reports', include('reporting.urls', namespace='reportong')),
    path('login', auth_views.login, {'template_name': 'authentication/login.html'}, name='login'),
    path('logout', auth_views.logout, name='logout', kwargs={'next_page': '/'}),
    path('account/', include('authentication.urls', namespace='authentication')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
