from django.db import models
from  Registration_Login.models import EmployeeRegister_Details,BusinessRegister_Details


class EmployeeSchedule(models.Model):
    emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    start_time = models.TimeField(auto_now=False,default='',null=True,blank=True)
    end_time = models.TimeField(auto_now=False,default='',null=True,blank=True)
    schedule_head = models.CharField(max_length=255,default='',null=True,blank=True)
    todo_content = models.TextField(default='',null=True,blank=True)
    log_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    schedule_status = models.IntegerField(default=0)
    schedule_date = models.DateField(auto_now=False,null=True)


class Feedback(models.Model):
    
    feedback_emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    from_id = models.IntegerField(default=0)
    from_name = models.CharField(max_length=255,default='',null=True,blank=True)
    feedback_content = models.TextField(default='',null=True,blank=True)
    feedback_date = models.DateField(auto_now=False,null=True)


class Complaints(models.Model):
    complaint_emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    compaint_head = models.CharField(max_length=255,default='',null=True,blank=True)
    compaint_content = models.TextField(default='',null=True,blank=True)
    complaint_date = models.DateField(auto_now=True,null=True)
    action = models.TextField(default='',null=True,blank=True)
    action_date = models.DateField(auto_now=False,null=True)
    status = models.IntegerField(default=0)

    
class ActionTaken(models.Model):
    act_emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    act_from_id = models.IntegerField(default=0)
    act_from_name = models.CharField(max_length=255,default='',null=True,blank=True)
    act_reason = models.TextField(default='',null=True,blank=True)
    act_head = models.CharField(max_length=255,default='',null=True,blank=True)
    act_content = models.TextField(default='',null=True,blank=True)
    action_date = models.DateField(auto_now=False,null=True)
    status = models.IntegerField(default=0)


class Notification(models.Model):
    emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    notific_head = models.CharField(max_length=255,default='',null=True,blank=True)
    notific_content = models.TextField(default='',null=True,blank=True)
    notific_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    notific_status = models.IntegerField(default=0)
    notific_date = models.DateField(auto_now=True,null=True)


class EmployeeLeave(models.Model):
    emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    start_date = models.DateField(auto_now=False,default='',null=True,blank=True)
    end_date = models.DateField(auto_now=False,default='',null=True,blank=True)
    leave_type = models.CharField(max_length=255,default='',null=True,blank=True)
    leave_reason = models.TextField(default='',null=True,blank=True)
    no_of_days = models.IntegerField(default=0)
    leave_status = models.IntegerField(default=0)
    leave_apply_date = models.DateField(auto_now=False,null=True)
    leave_statuChange_date = models.DateField(auto_now=False,null=True)
    leave_request_file = models.FileField(upload_to=r'leave\files',default='')


class Allocation_Details(models.Model):
    allocatEmp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    allocat_to = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, related_name="EmployeeRegister", null=True,default='')
    allocate_status = models.IntegerField(default=0)
    alloaction_date = models.DateField(auto_now=False,null=True)


class Previos_Allocation_Details(models.Model):
    allocate_id = models.ForeignKey(Allocation_Details, on_delete=models.CASCADE, null=True,default='')
    newallocation_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    newallocation_date = models.DateField(auto_now=True,null=True)
    previous_from_date = models.DateField(auto_now=False,null=True)
    previous_to_date = models.DateField(auto_now=False,null=True)
    previousemp_id = models.IntegerField(default=0)
    previousemp_name = models.CharField(max_length=255,default='',null=True,blank=True)
    previousemp_allocatedTo = models.IntegerField(default=0)
    previousemp_allocatedName = models.CharField(max_length=255,default='',null=True,blank=True)


    

# Work section -------------------------

class Work_Task(models.Model):
    comp_taskid = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    task_name = models.CharField(max_length=255,default='',null=True,blank=True)
    task_discription = models.TextField(default='',null=True,blank=True)
    task_add_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    task_status = models.IntegerField(default=0)
    task_add_date = models.DateField(auto_now=True,null=True)


class ClientRegister(models.Model):
    compId = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    client_name = models.CharField(max_length=255,default='',null=True,blank=True)
    client_email_primary = models.EmailField(default='client@gmail.com',null=True,blank=True)
    client_email_alter = models.EmailField(default='client@gmail2.com',null=True,blank=True)
    client_phone = models.CharField(max_length=255,default='9000000009',null=True,blank=True)
    client_phone_alter = models.CharField(max_length=255,default='9800000089',null=True,blank=True)
    client_address1 = models.CharField(max_length=255,default='',null=True,blank=True)
    client_address2 = models.CharField(max_length=255,default='',null=True,blank=True)
    client_address3 = models.CharField(max_length=255,default='',null=True,blank=True)
    client_place = models.CharField(max_length=255,default='',null=True,blank=True)
    client_district = models.CharField(max_length=255,default='',null=True,blank=True)
    client_state = models.CharField(max_length=255,default='',null=True,blank=True)
    client_profile = models.ImageField(upload_to='client\profile',default='')
    

    # Bussiness Details ---
    client_bussiness_name = models.CharField(max_length=255,default='9000000009',null=True,blank=True)
    client_bussiness_email_primary = models.EmailField(default='client@gmail.com',null=True,blank=True)
    client_bussiness_email_alter = models.EmailField(default='client@gmail2.com',null=True,blank=True)
    client_bussiness_phone = models.CharField(max_length=255,default='9000000009',null=True,blank=True)
    client_bussiness_website = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_phone_alter = models.CharField(max_length=255,default='9800000089',null=True,blank=True)
    client_bussiness_address1 = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_address2 = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_address3 = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_place = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_district = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_state = models.CharField(max_length=255,default='',null=True,blank=True)
    client_bussiness_file = models.ImageField(upload_to=r'client\files',default='')
    bussiness_logo = models.ImageField(upload_to='client\logo',default='')

    more_discription = models.TextField(default='',null=True,blank=True)
    client_add_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    client_status = models.IntegerField(default=0)
    work_reg_status = models.IntegerField(default=0)
    client_reg_date = models.DateField(auto_now=True,null=True)


class WorkRegister(models.Model):
    wcompId = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    clientId = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='') 
    allocated_emp = models.ManyToManyField(EmployeeRegister_Details, related_name='works_allocated')
    work_discription = models.TextField(default='',null=True,blank=True)
    work_create_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    work_file = models.FileField(upload_to=r'work\files',default='')
    work_progress = models.IntegerField(default=0)
    work_allocate_status = models.IntegerField(default=0)
    work_status = models.IntegerField(default=0)
    work_create_date = models.DateField(auto_now=False,null=True)
    work_end_date = models.DateField(auto_now=False,null=True)


class ClientTask_Register(models.Model):
    cTcompId = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    client_Id = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='') 
    work_Id = models.ForeignKey(WorkRegister, on_delete=models.CASCADE, null=True,default='') 
    task_name = models.CharField(max_length=255,default='',null=True,blank=True)
    task_discription = models.TextField(default='',null=True,blank=True)
    task_file = models.FileField(upload_to=r'work\task\files',default='')
    task_allocate_status = models.IntegerField(default=0)
    task_total_progress = models.IntegerField(default=0)
    task_status = models.IntegerField(default=0)
    task_create_date = models.DateField(auto_now=False,null=True)


class LeadCategory_Register(models.Model):
    cTaskId = models.ForeignKey(ClientTask_Register, on_delete=models.CASCADE, null=True,default='') 
    lc_assign_date = models.DateField(auto_now=True,null=True)
    lead_collection_for = models.CharField(max_length=255,default='',null=True,blank=True)
    lc_discription = models.TextField(default='',null=True,blank=True)
    lc_target = models.IntegerField(default=0)
    lc_target_achived = models.IntegerField(default=0)
    lc_file = models.FileField(upload_to=r'work\files',default='')
    lc_progress = models.IntegerField(default=0)



class LeadField_Register(models.Model):
    field_clientId = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='') 
    field_work_regId = models.ForeignKey(WorkRegister, on_delete=models.CASCADE, null=True,default='') 
    field_lead_category= models.ForeignKey(LeadCategory_Register, on_delete=models.CASCADE, null=True,default='') 
    field_name = models.CharField(max_length=255,default='',null=True,blank=True)
    field_discription = models.TextField(default='',null=True,blank=True)
    field_add_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    field_status = models.IntegerField(default=0)
    field_add_date = models.DateField(auto_now=True,null=True)




# Work Assign Table maintains the data of allocated work details

class WorkAssign(models.Model):
    wa_compId = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    wa_clientId = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='') 
    wa_work_regId = models.ForeignKey(WorkRegister, on_delete=models.CASCADE, null=True,default='') 
    wa_work_allocate = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='', related_name='allocated_tl') 
    wa_tasksId = models.ManyToManyField(ClientTask_Register, related_name='task_allocated')
    allocated_exemp = models.ManyToManyField(EmployeeRegister_Details, related_name='co_works_allocated')
    wa_discription = models.TextField(default='',null=True,blank=True)
    wa_file = models.FileField(upload_to=r'work\files',default='')
    work_assign_progress = models.IntegerField(default=0)
    work_assign_date = models.DateField(auto_now=True,null=True)
    wa_from_date = models.DateField(auto_now=False,null=True)
    wa_due_date = models.DateField(auto_now=False,null=True)
    wa_status = models.IntegerField(default=0)
    wa_type = models.IntegerField(default=0)
    wa_target = models.IntegerField(default=0)
    wa_target_achived = models.IntegerField(default=0)



class TaskAssign(models.Model):
    ta_workAssignId = models.ForeignKey(WorkAssign, on_delete=models.CASCADE, null=True,default='') 
    ta_workerId = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    ta_taskId = models.ForeignKey(ClientTask_Register, on_delete=models.CASCADE, null=True,default='') 
    ta_discription = models.TextField(default='',null=True,blank=True)
    ta_file = models.FileField(upload_to=r'work\files',default='')
    ta_progress = models.IntegerField(default=0)
    ta_allocate_date = models.DateField(auto_now=False,null=True)
    ta_start_date = models.DateField(auto_now=False,null=True)
    ta_due_date = models.DateField(auto_now=False,null=True)
    ta_target = models.IntegerField(default=0)
    ta_target_achived = models.IntegerField(default=0)
    ta_status = models.IntegerField(default=0)
    ta_accept_status = models.IntegerField(default=0)
    ta_accept_date = models.DateField(auto_now=False,null=True)
    ta_type = models.IntegerField(default=0)


class TaskDetails(models.Model):
    tad_taskAssignId = models.ForeignKey(TaskAssign, on_delete=models.CASCADE, null=True,default='') 
    tad_collect_date = models.DateField(auto_now=True,null=True)
    tad_title = models.CharField(max_length=255,default='',null=True,blank=True)
    tad_discription = models.TextField(default='',null=True,blank=True)
    tad_file = models.JSONField(default=list)
    tad_target = models.IntegerField(default=0)
    tad_status = models.IntegerField(default=0)
    tad_verified_target = models.IntegerField(default=0)


class LeadCateogry_TeamAllocate(models.Model):
    Tl_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    lc_id = models.ForeignKey(LeadCategory_Register, on_delete=models.CASCADE, null=True,default='')
    wa_id = models.ForeignKey(WorkAssign, on_delete=models.CASCADE, null=True,default='')
    lcta_discription = models.TextField(default='',null=True,blank=True)
    lcta_from_date = models.DateField(auto_now=False,null=True)
    lcta_due_date = models.DateField(auto_now=False,null=True)
    lcta_target = models.IntegerField(default=0)
    lcta_target_achived = models.IntegerField(default=0)
    lcta_file = models.FileField(upload_to=r'work\files',default='')
    lcta_progress = models.IntegerField(default=0)
    lcta_status = models.IntegerField(default=0)


class LeadCateogry_Assign(models.Model):
    executive_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    lcta_id = models.ForeignKey(LeadCateogry_TeamAllocate, on_delete=models.CASCADE, null=True,default='')
    ta_id = models.ForeignKey(TaskAssign, on_delete=models.CASCADE, null=True,default='')
    lca_discription = models.TextField(default='',null=True,blank=True)
    lca_from_date = models.DateField(auto_now=False,null=True)
    lca_due_date = models.DateField(auto_now=False,null=True)
    lca_target = models.IntegerField(default=0)
    lca_target_achived = models.IntegerField(default=0)
    lca_file = models.FileField(upload_to=r'work\files',default='')
    lca_progress = models.IntegerField(default=0) 
    lca_status = models.IntegerField(default=0)

    
class Leads(models.Model):
    lead_work_regId = models.ForeignKey(WorkRegister, on_delete=models.CASCADE, null=True,default='') 
    lead_collect_Emp_id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    lead_taskAssignId = models.ForeignKey(TaskAssign, on_delete=models.CASCADE, null=True,default='') 
    lead_category_id =  models.ForeignKey(LeadCategory_Register, on_delete=models.CASCADE, null=True,default='') 

    lead_name = models.CharField(max_length=255,default='',null=True,blank=True)
    lead_email = models.EmailField(default='',null=True,blank=True)
    lead_contact = models.CharField(max_length=255,default='',null=True,blank=True)
    lead_source = models.CharField(max_length=255,default='',null=True,blank=True)
    
    lead_add_date = models.DateField(auto_now=True,null=True)
    lead_add_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    waste_data = models.IntegerField(default=0)
    waste_data_reason = models.TextField(default='',null=True,blank=True)
    lead_status = models.IntegerField(default=0)
    lead_transfer_date = models.DateField(auto_now=False,null=True)
    lead_transfer_status = models.IntegerField(default=0)
    lead_incomplete_status = models.IntegerField(default=0)
    target_update_status = models.IntegerField(default=0)
    repeated_status = models.IntegerField(default=0)


class lead_Details(models.Model):
    leadId = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='') 
    lead_field_name = models.CharField(max_length=255,default='',null=True,blank=True)
    lead_field_data = models.CharField(max_length=855,default='',null=True,blank=True)


class WorkProgress(models.Model):
    wp_workerId = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='') 
    wp_add_date = models.DateField(auto_now=True,null=True)
    wp_from_date = models.DateField(auto_now=False,null=True)
    wp_to_date = models.DateField(auto_now=False,null=True)
    work_discription = models.TextField(default='',null=True,blank=True)
    wp_type = models.CharField(max_length=255,default='',null=True,blank=True)
    wp_progress = models.IntegerField(default=0)
    wp_status = models.IntegerField(default=0)
    wp_file = models.JSONField(default=list)

