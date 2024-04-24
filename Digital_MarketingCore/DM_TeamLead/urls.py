from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   
    # TL Module -------Sumayya-------------------------

    path('TL-Dashboard',views.tl_dashboard,name='tl_dashboard'),
    path('TL-Logout',views.tl_logout,name='tl_logout'),

    # Profile ------------------------------

    path('TL-Profile',views.tl_profile,name='tl_profile'),
    path('TL-Profile-Update',views.tl_profile_detailsUpdate,name='tl_profile_detailsUpdate'),
    path('TL-Profile-Image\Remove',views.tl_profileImage_remove,name='tl_profileImage_remove'),

    # Password ----------------------------

    path('TL-Password',views.tl_password,name='tl_password'),
    path('TL-Password-Update',views.tl_user_passwordUpdate,name='tl_user_passwordUpdate'),

    # Feedback  --------------------------

    path('TL-Feedback',views.tl_feedback,name='tl_feedback'),
    path('TL-Add-Feedback',views.tl_add_feedback,name='tl_add_feedback'),
    path('TL-Filter-Feedback',views.tl_filter_feedback,name='tl_filter_feedback'),

    # Complaints --------------------------

    path('TL-Complaints',views.tl_complaints,name='tl_complaints'),
    path('TL-Complaints-Action',views.tl_complaints_action_taken,name='tl_complaints_action_taken'),

    # Action Taken  --------------------------

    path('TL-Action-Taken',views.tl_actionTaken,name='tl_actionTaken'),
    path('TL-ActionTakenSave',views.tl_action_taken_save,name='tl_action_taken_save'),
    path('TL-ActionTakenEditPage\<int:act_id>',views.tl_action_taken_editPage,name='tl_action_taken_editPage'),
    path('TL-ActionTakenEdit\<int:aid>',views.tl_action_takenEdit,name='tl_action_takenEdit'),

    # Leave ---------------------------
    
    path('TL-Leave',views.tl_leave,name='tl_leave'),
    path('TL-Leave-Apply',views.tl_leave_apply,name='tl_leave_apply'),
    path('TL-Filter-Leave',views.tl_filter_leaves,name='tl_filter_leaves'),
    path('TL-Filter-Leave-Emp',views.tl_filter_leaves_emp,name='tl_filter_leaves_emp'),

    # Notification ----------------------

    path('TL-Notification',views.tl_allnotification,name='tl_allnotification'),
    path('TL-Open-Notification\<int:n_id>',views.tl_open_notification,name='tl_open_notification'),
    path('TL-Delete-Notification\<int:n_id>',views.tl_delete_notification,name='tl_delete_notification'),

    # Schedule ----------------------------

    path('TL-Schedule',views.tl_schedule,name='tl_schedule'),
    path('TL-schedule-Tasks',views.tl_schedule_tasks,name='tl_schedule_tasks'),
    path('TL-schedule-Edit-Page\<int:sch_id>',views.tl_edit_schedulePage,name='tl_edit_schedulePage'),
    path('TL-schedule-Edit\<int:taskid>',views.tl_edit_schedule,name='tl_edit_schedule'),
    path('TL-schedule-Delete\<int:taskid>',views.tl_delete_schedule,name='tl_delete_schedule'),
    path('TL-schedule-Status',views.tl_update_schedule_status,name='tl_update_schedule_status'),
    path('TL-Filter-schedule',views.tl_filter_schedule,name='tl_filter_schedule'),

    path('TL-Employees-schedule',views.tl_employees_schedule,name='tl_employees_schedule'),
    path('TL-Employees-schedule-add',views.tl_schedule_emp_tasks,name='tl_schedule_emp_tasks'),
    path('TL-Employees-schedule-Edit-Page\<int:sch_id>',views.tl_edit_emp_schedulePage,name='tl_edit_emp_schedulePage'),
    path('TL-Employees-schedule-Edit\<int:taskid>',views.tl_edit_emp_schedule,name='tl_edit_emp_schedule'),
    path('TL-Employees-schedule-delete\<int:taskid>',views.tl_delete_emp_schedule,name='tl_delete_emp_schedule'),
    path('TL-Employees-schedule-filter',views.tl_emp_filter_schedule,name='tl_emp_filter_schedule'),

    # Employees Section----------------------------

    path('TL-Employees-Section',views.tl_employee_section,name='tl_employee_section'),
    path('TL-Employees-View',views.tl_view_employees,name='tl_view_employees'),
    path('TL-Employees-Progress',views.tl_WorkProgress,name='tl_WorkProgress'),
    path('TL-Employees-Leaves',views.tl_employee_leaves,name='tl_employee_leaves'),
    path('TL-Employees-Filter-Leave',views.tl_emp_filter_leaves,name='tl_emp_filter_leaves'),
    path('TL-Employees-Schedules',views.tl_employee_schedules,name='tl_employee_schedules'),
    path('TL-Employees-Filter-Schedules',views.tl_emp_filter_schedules,name='tl_emp_filter_schedules'),
    path('TL-Employees-ActionTaken',views.tl_employee_actionTaken,name='tl_employee_actionTaken'),
    path('TL-Employees-Filter-ActionTaken',views.tl_emp_filter_actionTaken,name='tl_emp_filter_actionTaken'),
    path('TL-Employees-Feedback',views.tl_employee_feedback,name='tl_employee_feedback'),
    path('TL-Employees-Filter-Feedback',views.tl_emp_filter_feedback,name='tl_emp_filter_feedback'),
    path('TL-Employees-Complaints',views.tl_employee_complaints,name='tl_employee_complaints'),
    path('TL-Employees-Filter-Complaints',views.tl_emp_filter_complaints,name='tl_emp_filter_complaints'),
    path('TL-Employees-Works',views.tl_employeesWork,name='tl_employeesWork'),
    path('TL-Filter-Employees-Works',views.tl_employee_works_filter,name='tl_employee_works_filter'),

    # Work Section----------------------------

    path('TL-Work-Section',views.tl_work_section,name='tl_work_section'),
    path('TL-Assign-Work-View',views.tl_allocateWorkView,name='tl_allocateWorkView'),
    path('TL-Get_lead_category',views.get_lead_category,name='get_lead_category'),
    path('TL-Assign-Work',views.tl_workAssign,name='tl_workAssign'),
    path('TL-Delete-Task-Assign\<int:taskAsId>',views.tl_delete_taskAssign,name='tl_delete_taskAssign'),
    path('TL-Edit-Task-Assign\<int:taskAsId>',views.tl_edit_taskAssign,name='tl_edit_taskAssign'),

    path('TL-Pending-Works',views.tl_pending_works,name='tl_pending_works'),
    path('TL-Assign-Work-Remove-Works\<int:pk>',views.tl_assignTask_delete,name='tl_assignTask_delete'),
    path('TL-Verify-Works\<int:tdId>',views.tl_verify_workDone,name='tl_verify_workDone'),
    path('TL-Verify-Works-No-Target\<int:tdId>',views.tl_verify_workDone_notarget,name='tl_verify_workDone_notarget'),

    path('TL-Work-Progress',views.tl_work_progress,name='tl_work_progress'),
    path('TL-Completed-Works',views.tl_completed_works,name='tl_completed_works'),

    path('TL-Individual-Works-Section',views.tl_individualWorks_section,name='tl_individualWorks_section'),
    path('TL-Individual-Works-Accept',views.tl_individual_works_accept,name='tl_individual_works_accept'),
    path('TL-New-Works-Accept\<int:pk>',views.tl_newwork_accept,name='tl_newwork_accept'),

    path('TL-Ongoing-Works',views.tl_ongoing_works,name='tl_ongoing_works'),
    path('TL-OngoingWork-Progress\<int:pk>',views.tl_ongoingwork_progress,name='tl_ongoingwork_progress'),
    path('TL-DailyWork-Add\<int:pk>',views.tl_ongoingwork_dailyworkadd,name='tl_ongoingwork_dailyworkadd'),
    path('TL-DailyWork-Save\<int:pk>',views.tl_ongoingwork_dailyworksave,name='tl_ongoingwork_dailyworksave'),
    path('TL-DailyWork-View\<int:pk>',views.tl_ongoingwork_dailyworks,name='tl_ongoingwork_dailyworks'),
    path('TL-DailyWork-Complete\<int:pk>',views.tl_ongoingwork_complete,name='tl_ongoingwork_complete'),

    path('TL-Individual-Completed-Works',views.tl_individual_completed_works,name='tl_individual_completed_works'),
    path('TL-Individual-Completed-DailyWorks\<int:pk>',views.tl_completedwork_dailyworks,name='tl_completedwork_dailyworks'),

    path('TL-Lead-Data\<int:pk>',views.tl_lead_data,name='tl_lead_data'),
    path('TL-Lead-Collected-Data\<int:pk>',views.tl_lead_collected_data,name='tl_lead_collected_data'),
    path('TL-Lead-Add\<int:pk>',views.tl_lead_add,name='tl_lead_add'),
    path('TL-Lead-File-Download\<int:pk>',views.tl_download_excel,name='tl_download_excel'),
    path('TL-Lead-File-Upload\<int:pk>',views.tl_lead_file_upload,name='tl_lead_file_upload'),
    path('TL-Duplicate-Data\<int:pk>',views.tl_duplicate_data,name='tl_duplicate_data'),

    path('TL-DailyWork-Add-Lead\<int:pk>',views.tl_ongoingwork_dailyworkadd_lead,name='tl_ongoingwork_dailyworkadd_lead'),
    path('TL-DailyWork-Save-Lead\<int:pk>',views.tl_ongoingwork_dailyworksave_lead,name='tl_ongoingwork_dailyworksave_lead'),

    # Progress Section----------------------------

    path('TL-Progress-Section',views.tl_progress_section,name='tl_progress_section'),
    path('TL-Weekly-Progress',views.tl_weekly_progress,name='tl_weekly_progress'),
    path('Download-file-progress/<int:pid>/<int:file_index>/', views.download_file_progress, name='download_file_progress'),
    path('TL-Verify-Progress\<int:pId>',views.tl_verify_progress,name='tl_verify_progress'),
    path('TL-Filter-Weekly-Progress',views.tl_filter_weekly_progress,name='tl_filter_weekly_progress'),
    path('TL-Add-Weekly-Progress',views.tl_add_weekly_progress,name='tl_add_weekly_progress'),

    path('TL-Monthly-Progress',views.tl_monthly_progress,name='tl_monthly_progress'),
    path('TL-Filter-Monthly-Progress',views.tl_filter_monthly_progress,name='tl_filter_monthly_progress'),
    path('TL-Add-Monthly-Progress',views.tl_add_monthly_progress,name='tl_add_monthly_progress'),

    # Waste Data Section----------------------------

    path('TL-WasteData-Section',views.tl_waste_data,name='tl_waste_data'),
    path('TL-Update-Target-on-WasteData\<int:waste_id>',views.tl_update_target_on_wastedata,name='tl_update_target_on_wastedata'),
    path('TL-Update-Target-DailyTask\<int:tid>\<int:wid>',views.tl_update_target_dailyTask,name='tl_update_target_dailyTask'),



    # 17/04/24
    
    path('TL-Leads',views.tl_lead_list,name='tl_lead_list'),







    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)