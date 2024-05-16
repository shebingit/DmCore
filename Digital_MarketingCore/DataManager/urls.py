from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   
    # Data Manager Module --------------------------------

    path('Data-Manager-Dashboard',views.dataManager_dashboard,name='dataManager_dashboard'),

    path('Data-Manager-DataBank',views.DAM_Dashboard_databank,name='DAM_Dashboard_databank'),
    path('DataBank_load',views.DataBank_load,name='DataBank_load'),
    path('Data-Manager-FeatchExecutive',views.fetch_lead_executive,name='fetch_lead_executive'),
    path('fetch_leads_source',views.fetch_leads_source,name='fetch_leads_source'),
    path('Data-ManagerEdit\<int:dbID>',views.DAM_dataBnak_edit,name='DAM_dataBnak_edit'),
    path('Data-ManagerFollowUp\<int:dbID>',views.DAM_dataBnak_followup,name='DAM_dataBnak_followup'),
    
    
    path('Data-Manager-Allocation',views.DAM_Dashboard_allocation,name='DAM_Dashboard_allocation'),
    path('Data-Manager-Allocation-list',views.DAM_allAllocationList,name='DAM_allAllocationList'),
    path('Data-allocated_listBydate\<str:date_data>',views.DAM_allocated_listBydate,name='DAM_allocated_listBydate'),
    path('fetch_lead_allocate_exe/', views.fetch_lead_allocate_exe, name='fetch_lead_allocate_exe'),
    path('Allocation-Transfer/',views.DMA_allocate_lead,name='DMA_allocate_lead'),
    path('Change-Status/', views.fetch_leads_status_change, name='fetch_leads_status_change'),


    # Data Manager Follow Up 

     path('FollowUp-Management',views.DAM_Dashboard_followups,name='DAM_Dashboard_followups'),
     path('DAM_assign_remove/<int:lassignID>',views.DAM_assign_remove,name='DAM_assign_remove'),
    
    # Data Manager Notification Section ----------------

    path('Notification-Management',views.DAM_notification_section,name='DAM_notification_section'),
    path('Data-Manager-Notification-NewLead',views.DAM_Dashboard_notification_tody_newLead,name='DAM_Dashboard_notification_tody_newLead'),
    path('Toady-Allocation',views.DAM_Dashboard_todayAllocation,name='DAM_Dashboard_todayAllocation'),
    path('Toady-Followups',views.DAM_Dashboard_todayFollowups,name='DAM_Dashboard_todayFollowups'),
    path('AllocationChange-Status/', views.Notification_fetch_leads_status_change, name='Notification_fetch_leads_status_change'),

    
    # Clients section ---------------------------------

    path('Dashboard_Client-Management',views.DAM_Dashboard_clients,name='DAM_Dashboard_clients'),
    

    # Data Manager Account section --------------------------------

    path('Data-Manager/Password-Section',views.DAM_password,name='DAM_password'),
    path('Data-Manager/Password-change',views.DAM_passwordUpdate,name='DAM_passwordUpdate'),

    path('Data-Manager/Profile',views.DAM_profile,name='DAM_profile'),
    path('Data-Manager/Update-Profile',views.DAM_profile_detailsUpdate,name='DAM_profile_detailsUpdate'),


    #Side Navbar --------------------------
    path('Data-Manager-HR-Telecaller/',views.DAM_employees_hr_tel,name='DAM_employees_hr_tel'),
    path('Data-Manager-Executive/',views.DAM_employees_exe,name='DAM_employees_exe'),
    path('Data-Manager-Details-Employees/<int:empDeatilsID>',views.DAM_employess_details,name='DAM_employess_details'),
    

   


    # Data Manager Executive Dashboard Section ---------
    
    path('Executive-Dashboard/',views.DAM_Dashboard_Executive,name='DAM_Dashboard_Executive'),
    path('Telecaller-Allocated/<int:empID>',views.DAM_employee_allocated_leads,name='DAM_employee_allocated_leads'),



    path('Executive-Dashboard-Management/',views.DAM_executive_dashboard,name='DAM_executive_dashboard'),
    path('Clients-New-Leads/',views.DAM_client_newleads,name='DAM_client_newleads'),
    path('Clients/New-Leads-List/<int:clID>',views.DAM_client_lists_newLeads,name='DAM_client_lists_newLeads'),
    path('Executives/',views.DAM_executive_lead,name='DAM_executive_lead'),
    path('Executive-All/Leads-List/<int:eID>',views.DAM_executive_collected_leads,name='DAM_executive_collected_leads'),
    path('Clients-All-Leads/',views.DAM_all_clientleads,name='DAM_all_clientleads'),
    path('Clients-All/Leads-List/<int:cID>',views.DAM_client_lists_allLeads,name='DAM_client_lists_allLeads'),

    # Data Manager Allocation dashboard Section -----------------------

    
    path('Allocation-Dashboard-Management/',views.DAM_allocation_dashboard,name='DAM_allocation_dashboard'),
    path('Allocation-Pending/',views.DAM_pendingleads,name='DAM_pendingleads'),
    path('Allocated-Lead/',views.DAM_allocated_leads,name='DAM_allocated_leads'),
    path('Allocated-LeadBy-Date/<str:allocatedDate>/', views.DAM_allocatedlead_byDate, name='DAM_allocatedlead_byDate'),
    path('Client-Allocation-Pending/<int:cID>',views.DAM_client_pendingLeads,name='DAM_client_pendingLeads'),
    path('Client-Category-Pending/<int:lCID>',views.DAM_client_category_pendingLeads,name='DAM_client_category_pendingLeads'),
    
    path('Clients-Leads/',views.DAM_clientsleads,name='DAM_clientsleads'),
    
    
    


    # Data Manager Telecaller Dashboard Section -------

    path('Telecaller-Dashboard-Management/',views.DAM_telecallers_dashboard,name='DAM_telecallers_dashboard'),
    path('Follow-Up/',views.DAM_followup_leads,name='DAM_followup_leads'), 
    path('FollowUp-View', views.followup_view, name='followup_view'),
    path('Fetch-lead-categories', views.fetch_lead_categories, name='fetch_lead_categories'),
    path('Fetch-categorie-leads', views.fetch_executive_leads, name='fetch_executive_leads'),
    path('Fetch-Employee-Allocated-leads', views.fetch_employee_allocated_leads, name='fetch_employee_allocated_leads'),
   
    
    path('Follow-Up-Status-Save/',views.DAM_followup_save,name='DAM_followup_save'),
    path('Follow-Up-Status-Delete/<int:fID>',views.DAM_followup_delete,name='DAM_followup_delete'),



    # Data Manager platform  Section -------

    path('Platform-Management/',views.DAM_platform_management,name='DAM_platform_management'),
    path('Add-Platform',views.DAM_platform_add,name='DAM_platform_add'),
    path('Platform-Leads/<int:pID>',views.DAM_platform_leads,name='DAM_platform_leads'),
    path('Platform-Report',views.DAM_platform_Report,name='DAM_platform_Report'),

 
    # Data Manager Waste Data Section -------

    path('WasteData-Management/',views.DAM_wasteData_management,name='DAM_wasteData_management'),
    path('WasteData-Confirm-section/',views.DAM_waste_data_confirm,name='DAM_waste_data_confirm'),
    path('Waste-Data-Appove/',views.DAM_waste_dateApprove,name='DAM_waste_dateApprove'),
    path('Waste-Data-Remove/',views.DAM_waste_dateCancel,name='DAM_waste_dateCancel'),
    path('WasteData-List/',views.DAM_Approved_waste_data,name='DAM_Approved_waste_data'),
    
    path('Client-WasteData/',views.DAM_client_waste_data,name='DAM_client_waste_data'),
    path('Executive-WasteData/',views.DAM_exicutive_waste_data,name='DAM_exicutive_waste_data'),
    path('Hr-Telecaller-WasteData/',views.DAM_hr_telecaller_waste_data,name='DAM_hr_telecaller_waste_data'),
    

    #Repeat Data -----------------
    path('Repeats-Data/',views.DAM_repeat_data,name='DAM_repeat_data'),
    path('DataBankRepeat-Data/',views.DataBankRepeat_load,name='DataBankRepeat_load'),
    
    path('fetch_leadrepaet_categories-Data/',views.fetch_leadrepaet_categories,name='fetch_leadrepaet_categories'),
    path('fetch_lead_repatecategory-Data/',views.fetch_lead_repatecategory,name='fetch_lead_repatecategory'),

    path('DAM_waste_repeat_dateApprove/<int:rwaID>',views.DAM_waste_repeat_dateApprove,name='DAM_waste_repeat_dateApprove'),
    
    
    
    # Data Bank Section -------------------
 
    path('Data-Bank/',views.DAM_dataBank,name='DAM_dataBank'),
    path('Data-Remove/<int:dBID>',views.DAM_dataBnak_remove,name='DAM_dataBnak_remove'),
    
    path('Change-Executive/', views.fetch_leads_executive_change, name='fetch_leads_executive_change'),



    # 19/02/24 Report section -----
    path('Dm_dataReports/',views.Dm_dataReports,name='Dm_dataReports'),
    path('Dm_HReport_DateFetch/<int:pk>',views.Dm_hrReport_dateFetch,name='Dm_hrReport_dateFetch'),
    path('Dm_SingleDateFetch/<str:strDate>/<int:pk>',views.Dm_SingleDateFetch,name='Dm_SingleDateFetch'),
    
    path('DAM_Hr_JoinedLead/<int:pk>',views.DAM_Hr_JoinedLead,name='DAM_Hr_JoinedLead'),
    path('DAM_Hr_LeadStatusChange/<int:pk>',views.DAM_Hr_LeadStatusChange,name='DAM_Hr_LeadStatusChange'),



    path('DataManager-LeadTrack/<int:dbid>',views.lead_track,name='lead_track'),
    


    #---------------------------------------------------------------------------
    path('DataManager-Logout/',views.DAM_logout,name='DAM_logout'),

    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



