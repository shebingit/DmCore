from django.urls import path,re_path  
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve


urlpatterns = [
   
    # Login section-------------------
    path('',views.login_page,name='login_page'),
    path('Login-Authenticate',views.login_submitt,name='login_submitt'),

    #Registration section-------------
    path('Company-Registration-Form',views.company_registration_form,name='company_registration_form'),
    path('Employee-Registration-Form',views.employee_registration_form,name='employee_registration_form'),
    path('Departments-Select',views.get_departments,name='get_departments'),
    path('Designation-Select',views.get_designation,name='get_designation'),
    
    path('Business-Distributor-Registration-Form',views.business_distributor_registration_form,name='business_distributor_registration_form'),

    # check -----------------
    path('Email-Validation',views.check_email,name='check_email'),
    path('check_company_id',views.check_company_id,name='check_company_id'),

    # Save --------------------
    path('Company-Registration-Save',views.company_registration_form_save,name='company_registration_form_save'),
    path('Employee-Registration-Save',views.employee_registration_form_save,name='employee_registration_form_save'),
    path('Business-Distributor-Registration-Form-Save',views.business_distributor_registration_form_save,name='business_distributor_registration_form_save'),
    

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)