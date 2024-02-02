from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve


urlpatterns = [
   
    #  Distributor Module --------------------------------

    path('Distributor-Dashboard',views.Distributor_dashboard,name='Distributor_dashboard'),
    path('Distributor-Logout',views.Distributor_logout,name='Distributor_logout'),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)