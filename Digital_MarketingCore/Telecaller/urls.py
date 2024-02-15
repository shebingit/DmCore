from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   
    path('TC_dashboard',views.TC_dashboard,name='TC_dashboard'),
    path('TC_current_clients',views.TC_current_clients,name='TC_current_clients'),
    path('TC_current_clients_details/<id>',views.TC_current_clients_details,name='TC_current_clients_details'),
    path('TC_update_Clients_Response/<id>',views.TC_update_Clients_Response,name='TC_update_Clients_Response'),
    path('TC_previous_clients',views.TC_previous_clients,name='TC_previous_clients'),
    path('TC_previous_clients_details/<id>',views.TC_previous_clients_details,name='TC_previous_clients_details'),
    path('TC_profile',views.TC_profile,name='TC_profile'),
    path('TC_profile_detailsUpdate',views.TC_profile_detailsUpdate,name='TC_profile_detailsUpdate'),
    path('TC_profileImage_remove',views.TC_profileImage_remove,name='TC_profileImage_remove'),
    path('TC_leave',views.TC_leave,name='TC_leave'),
    path('TC_leave_search',views.TC_leave_search,name='TC_leave_search'),
    path('TC_actionTaken',views.TC_actionTaken,name='TC_actionTaken'),
    path('TC_feedback',views.TC_feedback,name='TC_feedback'),
    path('TC_feedback_Typechange',views.TC_feedback_Typechange,name='TC_feedback_Typechange'),
    path('TC_complaints',views.TC_complaints,name='TC_complaints'),
    path('TC_complaint_add',views.TC_complaint_add,name='TC_complaint_add'),
    path('TC_leads/<id>',views.TC_leads,name='TC_leads'),
    path('TC_newleads/<id>',views.TC_newleads,name='TC_newleads'),
    path('TC_ongoing_leads/<id>',views.TC_ongoing_leads,name='TC_ongoing_leads'),
    path('TC_waiting_leads/<id>',views.TC_waiting_leads,name='TC_waiting_leads'),
    path('TC_rejected_leads/<id>',views.TC_rejected_leads,name='TC_rejected_leads'),
    path('TC_completed_leads/<id>',views.TC_completed_leads,name='TC_completed_leads'),
    path('TC_newleads_accept/<id>',views.TC_newleads_accept,name='TC_newleads_accept'),

    path('TC_waste_leads',views.TC_waste_leads,name='TC_waste_leads'),
    path('TC_waste_leads_action/<id>',views.TC_waste_leads_action,name='TC_waste_leads_action'),
    path('TC_waste_leads_details/<id>',views.TC_waste_leads_details,name='TC_waste_leads_details'),
    path('TC_waste_leads_page/<id>',views.TC_waste_leads_page,name='TC_waste_leads_page'),
    path('TC_pending_waste_leads/<id>',views.TC_pending_waste_leads,name='TC_pending_waste_leads'),
    path('TC_notification',views.TC_notification,name='TC_notification'),
    path('TC_open_notification/<n_id>',views.TC_open_notification,name='TC_open_notification'),
    path('TC_delete_notification/<n_id>',views.TC_delete_notification,name='TC_delete_notification'),

    # follow up setion -----------------------

    path('Follow-UpLeads',views.Tc_follow_upLeads,name='Tc_follow_upLeads'),
    path('Lead-Follow-Updates/<int:flID>',views.Lead_FollowUp_Updates,name='Lead_FollowUp_Updates'),
    path('Tc_followupDetails/<int:lID>',views.Tc_followupDetails,name='Tc_followupDetails'),


    #closed Section ----------------------------
    path('Complete-Leads/<int:laID>',views.TC_complete_lead,name='TC_complete_lead'),
    path('Closed-Leads',views.Tc_closedlead,name='Tc_closedlead'),
    
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)