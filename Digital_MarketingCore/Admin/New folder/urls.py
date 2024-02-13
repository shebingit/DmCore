from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   
    #  Admin Module --------------------------------

    path('Admin-Dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('Admin-Login-Requests',views.admin_login_requestpage,name='admin_login_requestpage'),
    path('Admin-Login-Approve\<int:pk>',views.admin_login_approve,name='admin_login_approve'),
    path('Admin-Login-Reject\<int:pk>',views.admin_login_reject,name='admin_login_reject'),
    path('Admin-Logout',views.admin_logout,name='admin_logout'),

    # Profile ------------------------------

    path('Admin-Profile',views.admin_profile,name='admin_profile'),
    path('Admin-profile-Update',views.admin_Profile_detailsUpdate,name='admin_Profile_detailsUpdate'),
    path('Adminprofile-Image\Remove',views.admin_profileImage_remove,name='admin_profileImage_remove'),


    # Password ----------------------------

    path('Admin-password',views.admin_password,name='admin_password'),
    path('Adminpassword-Update',views.admin_passwordUpdate,name='admin_passwordUpdate'),


    # Department ---------------------------------
    
    path('Admin-Department',views.admin_department,name='admin_department'),
    path('Admin-Department-Edit/<int:pk>',views.admin_department_edit,name='admin_department_edit'),
    path('Admin-Department-Delete/<int:pk>',views.admin_department_delete,name='admin_department_delete'),


    # Designation -------------------------------

    path('Admin-Designations',views.admin_designation,name='admin_designation'),
    path('Admin-Designations-Edit/<int:pk>',views.admin_designation_edit,name='admin_designation_edit'),
    path('Admin-Designations-Delete/<int:pk>',views.admin_designation_delete,name='admin_designation_delete'),


       


    # Employees Section -----------------

    path('Admin-Employees-Section',views.admin_employees_section,name='admin_employees_section'),
    path('Admin-Employees-View',views.admin_viewEmployees,name='admin_viewEmployees'),
    path('Admin-Employee-Verification/<int:pk>',views.admin_employee_verification,name='admin_employee_verification'),
    path('Admin-Employee-Inactive/<int:pk>',views.admin_employee_inactive,name='admin_employee_inactive'),  
    path('Admin-Employee-Active/<int:pk>',views.admin_employee_active,name='admin_employee_active'),
    path('Admin-Employees-Resigned',views.admin_resignedEmployees,name='admin_resignedEmployees'),
    path('Admin-Employees-Leaves',views.admin_Employeesleaves,name='admin_Employeesleaves'),
    path('Admin-Employee-leaveDetails',views.admin_get_employee_leavedetails,name='admin_get_employee_leavedetails'),
    path('Admin-Employees-ActionTakens',views.admin_Employees_actiontaken,name='admin_Employees_actiontaken'),
    path('Admin-Employee-ActionDetails',views.admin_get_employee_actiondetails,name='admin_get_employee_actiondetails'),
    path('Admin-Employees-Feedbacks',views.admin_Employees_feedback,name='admin_Employees_feedback'),
    path('Admin-Employee-FeedbackDetails',views.admin_get_employee_feedbackdetails,name='admin_get_employee_feedbackdetails'),
    path('Admin-Employees-Complaints',views.admin_Employees_complaints,name='admin_Employees_complaints'),
    path('Admin-Employee-ComplaintDetails',views.admin_get_employee_complaintdetails,name='admin_get_employee_complaintdetails'),
    path('Admin-Employees-Schedules',views.admin_Employees_schedules,name='admin_Employees_schedules'),
    path('Admin-Employee-ScheduleDetails',views.admin_get_employee_scheduledetails,name='admin_get_employee_scheduledetails'),
    path('Admin-Employees/Allocated-Listpage',views.admin_employeeAllocated_list,name='admin_employeeAllocated_list'),
    path('Admin-Employee-Allocated-EmployeeDetails',views.admin_get_employee_allocatedetails,name='admin_get_employee_allocatedetails'),
    path('Admin-Employee-Works',views.admin_all_works,name='admin_all_works'),
    path('Admin-Executive-Works',views.admin_executivework_page,name='admin_executivework_page'),
    path('Admin-Employee-workDetails',views.admin_get_employee_workdetails,name='admin_get_employee_workdetails'),
    path('Admin-Employee-dailyworkDetails',views.admin_get_employee_dailyworkdetails,name='admin_get_employee_dailyworkdetails'),
    path('Admin-TeamLead-Works',views.admin_tlwork_page,name='admin_tlwork_page'),
    path('Admin-Head-Works',views.admin_headwork_page,name='admin_headwork_page'),
    path('Admin-Clients-Works',views.admin_clientswork_page,name='admin_clientswork_page'),
    path('Admin-newClients-Works',views.admin_new_clientswork,name='admin_new_clientswork'),
    path('Admin-OngoingClients-Works',views.admin_ongoing_clientswork,name='admin_ongoing_clientswork'),
    path('Admin-CompletedClients-Works',views.admin_completed_clientswork,name='admin_completed_clientswork'),
    path('Admin-Client-OngoingworkDetails',views.admin_get_client_ongoingworkdetails,name='admin_get_client_ongoingworkdetails'),
    path('Admin-Client-CompletedworkDetails',views.admin_get_client_completedworkdetails,name='admin_get_client_completedworkdetails'),

    # leads Section -----------------
    path('Admin-Leadsection',views.admin_leads_section,name='admin_leads_section'),
    path('Admin-Leads',views.admin_leads_page,name='admin_leads_page'),
    path('Admin-LeadDetails',views.admin_get_client_leaddetails,name='admin_get_client_leaddetails'),
    path('Admin_lead_categories',views.get_lead_categories, name='get_lead_categories'),
    path('Admin-Lead-DetailsPage/<int:pk>',views.admin_lead_details, name='admin_lead_details'),
    path('Admin_lead_collected_employees',views.get_lead_collected_employees, name='get_lead_collected_employees'),
    path('Admin-Employee-LeadDetails',views.admin_get_client_employee_leaddetails,name='admin_get_client_employee_leaddetails'),
    path('Admin-Waste-Leads',views.admin_wasteleads_page,name='admin_wasteleads_page'),
    path('Admin-Waste-LeadDetails',views.admin_get_client_wasteleaddetails,name='admin_get_client_wasteleaddetails'),
    path('Admin-Employee-Waste-LeadDetails',views.admin_get_client_employee_wasteleaddetails,name='admin_get_client_employee_wasteleaddetails'),
    path('Admin-Followup-Leads',views.admin_followupleads_page,name='admin_followupleads_page'),
    path('Category-Select',views.get_leadcategory,name='get_leadcategory'),
    path('filter_lead', views.filter_lead, name='filter_lead'),
    path('Filter_lead_category', views.filter_lead_category, name='filter_lead_category'),
    path('Filter_lead_caller', views.filter_lead_hr_telecaller, name='filter_lead_hr_telecaller'),
    path('Filter_lead_status', views.filter_lead_status, name='filter_lead_status'),

    # PlatForm Data ======================
    
    path('admin_pltformdata', views.admin_pltformdata, name='admin_pltformdata'),
    path('admin_pltformleads_page/<str:lead_source>', views.admin_pltformleads_page, name='admin_pltformleads_page'),
   

    # Reports ============================

    path('admin_reports', views.admin_reports, name='admin_reports'),
    path('filter_lead_date', views.filter_lead_date, name='filter_lead_date'),
    path('filter_lead_platform', views.filter_lead_platform, name='filter_lead_platform'),


    # Analysis
    path('admin_analysis', views.admin_analysis, name='admin_analysis'),
    path('admin_employee_analysis', views.admin_employee_analysis, name='admin_employee_analysis'),
    path('admin_comparison', views.admin_comparison, name='admin_comparison'),
    
    
     
    


    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)