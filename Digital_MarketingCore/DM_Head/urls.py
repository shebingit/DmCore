from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   
    # Head Module --------------------------------

    path('Head-Dashboard',views.head_dashboard,name='head_dashboard'),
    path('Head-Logout',views.head_logout,name='head_logout'),

    # Profile ------------------------------

    path('Profile',views.head_profile,name='head_profile'),
    path('Profile-Update',views.profile_detailsUpdate,name='profile_detailsUpdate'),
    path('Profile-Image\Remove',views.profileImage_remove,name='profileImage_remove'),

    # Password ----------------------------

    path('Password',views.head_password,name='head_password'),
    path('Password-Update',views.user_passwordUpdate,name='user_passwordUpdate'),


    # Work Section --------------------- 

    path('Work/Work-Section/',views.Head_work_section,name='Head_work_section'),
    path('Work/Create-Client/',views.head_createClient,name='head_createClient'),
    path('delete-client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('Work/Create/',views.head_createWork,name='head_createWork'),
    path('delete-work/<int:work_id>/', views.delete_work, name='delete_work'),
    path('Work/Register-works-list/',views.head_registerWorks,name='head_registerWorks'),
    path('Work/Lead-Category/',views.head_lead_categoryadd,name='head_lead_categoryadd'),
    path('Work/Lead-Edit-Category/',views.head_lead_categoryedit,name='head_lead_categoryedit'),
    path('delete-lead-category/<int:lc_id>/', views.delete_lead_category, name='delete_lead_category'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),

    
    path('Work/Client-Edit/<int:pk>',views.head_clientEdit,name='head_clientEdit'),
    path('Work/Task-add/',views.head_work_taskadd,name='head_work_taskadd'),
    path('Work/Task-edit/',views.head_work_taskedit,name='head_work_taskedit'),

    #Lead Section ---------------
    path('Work/Lead-Data/',views.Head_lead_data,name='Head_lead_data'),
    path('HD_featchLeadFields/',views.HD_featchLeadFields,name='HD_featchLeadFields'),
    
    path('Work/Lead-Collection/Field-AddForm/',views.head_lead_fieldForm,name='head_lead_fieldForm'),

    path('Client/Lead-Data-List/<int:pk>/<int:lcID>',views.head_lead_collected_data,name='head_lead_collected_data'),
   
 
    

    path('Lead-add/<int:pk>',views.Head_lead_add,name='Head_lead_add'),
    #Excel Create and download 
    path('download_excel/<int:pk>/<int:lID>',views.download_excel,name='download_excel'),
    path('Upload-Data/<int:pk>/<int:lcID>',views.Head_lead_file_upload,name='Head_lead_file_upload'),
    

    path('Lead/Transfer-Data',views.head_transfer_lead,name='head_transfer_lead'),
    path('Client/Lead-Transfer-DataManager/',views.head_all_leadTransfer,name='head_all_leadTransfer'),

    path('Lead/Transferred-Data',views.head_transferred_lead,name='head_transferred_lead'),
    path('Lead/Waste-Data',views.head_waste_lead,name='head_waste_lead'),
    path('DataManager_WasteLead/',views.datamanager_wasteLead,name='datamanager_wasteLead'),
    path('Confirm-Reject-Lead/<int:wasteid>/',views.hd_wastelead_confirm_reject,name='hd_wastelead_confirm_reject'),
    

    path('Work/Allocate-View-works/',views.head_allocateWorkView,name='head_allocateWorkView'),
    path('Work/Work-Allocate/',views.head_workAllocate,name='head_workAllocate'),
    path('Work/Team-Lead-Tasks/<int:task_workId>/<int:task_empId>',views.head_teamLead_allocatedTask,name='head_teamLead_allocatedTask'),
    path('head_lead_category_allocateTl',views.head_lead_category_allocateTl,name='head_lead_category_allocateTl'),
    path('head_leadCategory_allocate_edit/<int:lcID>',views.head_leadCategory_allocate_edit,name='head_leadCategory_allocate_edit'),
    path('head_leadCategory_allocate_remove/<int:lcID>',views.head_leadCategory_allocate_remove,name='head_leadCategory_allocate_remove'),
    
    path('Work/Remove/Work-Assign/<int:work_assingId>',views.head_assigned_work_Remove,name='head_assigned_work_Remove'),
    path('Work/Remove/Work-Task/<int:assingId>/<int:assignTaskId>',views.head_assigned_task_Remove,name='head_assigned_task_Remove'),  
    # Team lead Sigle Task Allocate----
    path('Work/Team-Lead/Task-Allocate/<int:work_assigngId>',views.head_TlsingleTask,name='head_TlsingleTask'),

    path('Work/Remove/Allocate-Delete/<int:workId>/<int:empId>', views.head_removeAllocatedTl, name='head_removeAllocatedTl'),
    path('get_client_tasks',views.get_client_tasks,name='get_client_tasks'),
    path('Work/Pending-Works/',views.head_pendingworkView,name='head_pendingworkView'),
    
    path('Work/Progress',views.head_WorkProgress,name='head_WorkProgress'),
    path('Work/Client-Work-Details/<int:pk>',views.head_clientWorkDetails,name='head_clientWorkDetails'),
    path('Work/Client-Task-Details/<int:client_workId>/<int:client_TaskId>', views.head_clientTaskDetails, name='head_clientTaskDetails'),
    
    path('Work/Weekly-Progress',views.head_WeeklyProgress,name='head_WeeklyProgress'),
    path('Weekly-Verify-Unverify/<int:pk>',views.head_progreess_verify_unverify,name='head_progreess_verify_unverify'),
    path('Work/Monthly-Progress',views.head_MonthlyProgress,name='head_MonthlyProgress'),

    path('Work/Weekly-Monthly-Progress-Change',views.head_progress_change,name='head_progress_change'),
    


    path('Work/Tasks',views.head_tasksForWork,name='head_tasksForWork'),
    path('Comapany-TaskEdit/<int:task_edit>',views.company_taskEdit,name='company_taskEdit'),
    path('Comapany-TaskDelete/<int:task_delete>',views.company_taskDelete,name='company_taskDelete'),
    path('Work/work-Edit/<int:pk>',views.head_workDetailsEdit,name='head_workDetailsEdit'),

    # Completed Work View ---

    path('Work/Completed',views.head_workCompleted,name='head_workCompleted'),
    
    
    # Employees Section -----------------

    path('Employees/Employees-Section',views.Head_employees_section,name='Head_employees_section'),
    path('Employees/View',views.head_viewEmployees,name='head_viewEmployees'),
    path('Employees/Allocate',views.head_employeeAllocate,name='head_employeeAllocate'),
    path('Employees/Allocated-List',views.head_employeeAllocated_list,name='head_employeeAllocated_list'),
    path('Employees/Re-Allocate',views.head_reallocate_teamLead,name='head_reallocate_teamLead'),

    path('hd_employeeDesignationEdit/',views.hd_employeeDesignationEdit,name='hd_employeeDesignationEdit'),

    #leave ----------
    path('Employees/Employees-Leave',views.head_employee_leaves,name='head_employee_leaves'),

    #Schedules -----
    path('Employees/Employees-Schedules',views.head_employee_schedules,name='head_employee_schedules'),

    #Action Taken Views ----
    path('Employees/Employees-ActionTaken',views.head_employee_actionTaken,name='head_employee_actionTaken'),


    # Feedback -------
    path('Employees/Employees-Feedback',views.head_employee_feedback,name='head_employee_feedback'),

    # Works ----------
    
    path('Employees/Employees-Work',views.head_employeesWork,name='head_employeesWork'),
    path('Employees/Employees-Work/<int:wid>/<int:pk>',views.head_employe_workView,name='head_employe_workView'),
    

    #Resigned -------
    
    path('Employees/Resigned-List',views.head_resignedEmployees,name='head_resignedEmployees'),
    
    
    
    

    #Schedule ----------------------------

    path('Schedule',views.head_schedule,name='head_schedule'),
     
    path('Head-schedule-save',views.head_schedule_save,name='head_schedule_save'),
    path('Head/schedule/By-Date/Search',views.head_schedulesearchBy_date,name='head_schedulesearchBy_date'),

    path('Head-schedule-Edit',views.ScheduleEdit,name='ScheduleEdit'),
    path('Head-update_schedule_status',views.update_schedule_status,name='update_schedule_status'),
    path('Head-schedule-remove/<int:pk>',views.head_scheduleRemove,name='head_scheduleRemove'),
    path('Head-Employees-schedule',views.head_employees_schedule,name='head_employees_schedule'),
    path('Head-ScheduleAdd-Employees/',views.head_employee_scheduleAdd,name='head_employee_scheduleAdd'),
    path('Head-Employees-scheduleEdit/<int:pk>',views.head_employeeScheduleEdit,name='head_employeeScheduleEdit'),
    path('Head-Remove-Employees-Schedule/<int:pk>',views.head_employee_scheduleRemove,name='head_employee_scheduleRemove'),
    path('Head-schedule-view',views.head_scheduleFilter,name='head_scheduleFilter'),
    

    # Feedback  --------------------------

    path('Head-Feedback',views.head_feedback,name='head_feedback'),
    path('Head-Feedback-Type-Change',views.feedback_Typechange,name='feedback_Typechange'),
    

    # Complaints --------------------------

    path('Head-Complaints',views.head_complaints,name='head_complaints'),

    # Action Taken  --------------------------

    path('Head-Action-Taken',views.head_actionTaken,name='head_actionTaken'),
    path('Head-EditAction-Taken/<int:pk>',views.head_action_takenEdit,name='head_action_takenEdit'),
    

    # Notification ----------------------

    path('Head-Notification',views.head_allnotification,name='head_allnotification'),
    path('Head-Notification-Update',views.head_notificationUpdate,name='head_notificationUpdate'),
    path('Head-Notification-Remove',views.head_delete_notifications,name='head_delete_notifications'),

    # Leave ---------------------------
    
    path('Head-Leave',views.head_leave,name='head_leave'),
    path('Head-Request-leave',views.head_leave_request,name='head_leave_request'),
    path('Head-Search-leave',views.head_leave_search,name='head_leave_search'),
    
    path('Head-Approve-Reject/<int:request_id>/<int:request_status>',views.head_leaveApprove_Reject,name='head_leaveApprove_Reject'),
    path('Head-Leave-Seach',views.head_leaveSearch,name='head_leaveSearch'),
    
    path('view-image/<str:image_name>/', views.view_image, name='view_image'),

    path('Client/head_lead_verify_unverify_all/<int:all_wkid>/<int:all_lcid>',views.head_lead_verify_unverify_all,name='head_lead_verify_unverify_all'),
    path('Client/categoryleadt_details/<int:catelcid>',views.categoryleadt_details,name='categoryleadt_details'),
    
# ========================================================================================================================

# tesing url section 


    path('Work_allocate/<int:pk>',views.allocate_page,name='allocate_page'),
    path('Fetch_Task_Categories',views.fetch_task_categories,name='fetch_task_categories'),
    path('Featch-Lead-Details',views.HD_featchLeadDetails,name='HD_featchLeadDetails'),


    path('leadActivity_data/<int:lead_id>/', views.leadActivity_data, name='leadActivity_data'),
    path('Status-Chabge',views.lead_status_change,name='lead_status_change'),


    path('Reports/',views.head_Reports,name='head_Reports'),
    path('Lead-Categories/',views.leadCategories,name='leadCategories'),
    path('Waste-Reason/',views.HD_featchLeadwasteReason,name='HD_featchLeadwasteReason'),
    
    path('leadFollwup_data/<int:lead_id>/', views.leadFollwup_data, name='leadFollwup_data'),

    path('Repeated-Lead/',views.head_repeated_lead,name='head_repeated_lead'),
    path('Repeated-DeleteLead/',views.lead_repeat_delete,name='lead_repeat_delete'),

    path('Lead/Tracker-Data',views.head_lead_tracker,name='head_lead_tracker'),
    path('leadActivity_Tracker/<int:lead_id>/', views.leadActivity_Tracker, name='leadActivity_Tracker'),
    
    
    path('leadrepeated_data/<int:rlead_id>/', views.leadrepeated_data, name='leadrepeated_data'),
    path('waste_leadPDF_preview/<int:pdf_id>/', views.waste_leadPDF_preview, name='waste_leadPDF_preview'), 
    


    #Executive Task allocate ----------------

    path('Head/Task-Allocate/',views.head_allocate_task_to_executive,name='head_allocate_task_to_executive'),
    path('Head/Task-Assign/',views.head_TaskkAssign_Executive,name='head_TaskkAssign_Executive'),
    
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)