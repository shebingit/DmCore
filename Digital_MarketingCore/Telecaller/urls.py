from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   
    path('TC_dashboard',views.TC_dashboard,name='TC_dashboard'),
   
    # Profile setion ----------------------
    path('TC_profile',views.TC_profile,name='TC_profile'),
    path('TC_profile_detailsUpdate',views.TC_profile_detailsUpdate,name='TC_profile_detailsUpdate'),
    path('TC_profileImage_remove',views.TC_profileImage_remove,name='TC_profileImage_remove'),


    # Leave setion ----------------------

    path('TC_leave',views.TC_leave,name='TC_leave'),
    path('TC_leave_search',views.TC_leave_search,name='TC_leave_search'),


    # Action setion ----------------------

    path('TC_actionTaken',views.TC_actionTaken,name='TC_actionTaken'),


    # Feedback setion ----------------------

    path('TC_feedback',views.TC_feedback,name='TC_feedback'),
    path('TC_feedback_Typechange',views.TC_feedback_Typechange,name='TC_feedback_Typechange'),


    #Complaints setion ---------------------

    path('TC_complaints',views.TC_complaints,name='TC_complaints'),
    path('TC_complaint_add',views.TC_complaint_add,name='TC_complaint_add'),

    # Leads setion -------------------------
    path('TC-Leads/',views.TC_leads,name='TC_leads'),
    path('HR-leadAccept',views.hr_leadAccept,name='hr_leadAccept'),
    path('TC_waste_leads',views.TC_waste_leads,name='TC_waste_leads'),
    path('HR-leadReport/<str:date_str>',views.hr_leadReport,name='hr_leadReport'),
    

    # Follow up setion -----------------------

    path('Follow-UpLeads',views.Tc_follow_upLeads,name='Tc_follow_upLeads'),
    path('Lead-Follow-Updates/<int:flID>',views.Lead_FollowUp_Updates,name='Lead_FollowUp_Updates'),
    path('TC_update_Clients_Response/<id>',views.TC_update_Clients_Response,name='TC_update_Clients_Response'),
    path('Tc_followupDetails/<int:lID>',views.Tc_followupDetails,name='Tc_followupDetails'),
    path('TC_waste_leads_action/<int:id>',views.TC_waste_leads_action,name='TC_waste_leads_action'),
    path('HR-leadRecall/<int:assID>',views.hr_recallUpdate,name='hr_recallUpdate'),


    #closed Section ----------------------------
  
    path('Closed-Leads',views.Tc_closedlead,name='Tc_closedlead'),
    path('HR-leadClose/<int:laID>',views.hr_leadClose,name='hr_leadClose'),
    path('HR-leadJoined/<int:ljID>',views.hr_leadJoined,name='hr_leadJoined'),
    
    
    
    #Notification Section ----------------------------
    path('TC_notification',views.TC_notification,name='TC_notification'),
    path('TC_open_notification/<n_id>',views.TC_open_notification,name='TC_open_notification'),
    path('TC_delete_notification/<n_id>',views.TC_delete_notification,name='TC_delete_notification'),



    path('closechange',views.closechange,name='closechange'),
    
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)