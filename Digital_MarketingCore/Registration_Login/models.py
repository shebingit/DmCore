from django.db import models


class LogRegister_Details(models.Model):
    log_username = models.CharField(max_length=255,default='',null=True,blank=True)
    log_password = models.CharField(max_length=255,default='',null=True,blank=True)
    log_date = models.DateField(auto_now_add=True,null=True)
    log_time = models.TimeField(auto_now_add=True,null=True)
    position = models.CharField(max_length=255,default='',null=True,blank=True)
    is_staff = models.IntegerField(default=0)
    active_status = models.IntegerField(default=0)


class DistributorRegister_Details(models.Model):
    logdis_id = models.ForeignKey(LogRegister_Details, on_delete=models.CASCADE, null=True,default='')
    dis_name = models.CharField(max_length=255,default='',null=True,blank=True)
    dis_contact_no = models.CharField(max_length=255,default='',null=True,blank=True)
    dis_email =  models.EmailField(max_length=255,default='email@gmail.com')
    dis_agencies = models.CharField(max_length=255,default='',null=True,blank=True)
    dis_profife = models.FileField(upload_to='profiles',default='')
    dis_file = models.FileField(upload_to='employee_files',default='')
    dis_address1 =  models.CharField(max_length=255,default='',null=True,blank=True)
    dis_address2 =  models.CharField(max_length=255,default='',null=True,blank=True)
    dis_address3 =  models.CharField(max_length=255,default='',null=True,blank=True)
    dis_pin =  models.CharField(max_length=50,default='',null=True,blank=True)
    dis_location =  models.CharField(max_length=150,default='',null=True,blank=True)
    dis_district =  models.CharField(max_length=150,default='',null=True,blank=True)
    dis_state =  models.CharField(max_length=150,default='',null=True,blank=True)
    dis_active_status = models.IntegerField(default=0)
    dis_reg_date = models.DateField(auto_now_add=True,null=True)


class BusinessRegister_Details(models.Model):
    log_id = models.ForeignKey(LogRegister_Details, on_delete=models.CASCADE, null=True,default='')
    distributor_id = models.ForeignKey(DistributorRegister_Details, on_delete=models.CASCADE, null=True,default='')
    owner_fname = models.CharField(max_length=255,default='',null=True,blank=True)
    owner_lname = models.CharField(max_length=255,default='',null=True,blank=True)
    company_name = models.CharField(max_length=255,default='',null=True,blank=True)
    contact_no = models.CharField(max_length=255,default='',null=True,blank=True)
    company_email =  models.EmailField(max_length=255,default='email@gmail.com')
    company_image = models.FileField(upload_to='profiles',default='')
    company_website =  models.CharField(max_length=255,default='',null=True,blank=True)
    company_address1 =  models.CharField(max_length=255,default='',null=True,blank=True)
    company_address2 =  models.CharField(max_length=255,default='',null=True,blank=True)
    company_address3 =  models.CharField(max_length=255,default='',null=True,blank=True)
    company_pin =  models.CharField(max_length=50,default='',null=True,blank=True)
    company_location =  models.CharField(max_length=150,default='',null=True,blank=True)
    company_district =  models.CharField(max_length=150,default='',null=True,blank=True)
    company_state =  models.CharField(max_length=150,default='',null=True,blank=True)
    company_active_status = models.IntegerField(default=0)
    reg_date = models.DateField(auto_now_add=True,null=True)
    company_identify_Id = models.CharField(max_length=150,default='COMID001',blank=False,null=False)


class DepartmentRegister_details(models.Model):
    brd_id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    dept_name = models.CharField(max_length=255,default='',null=True,blank=True)
    dept_active_status = models.IntegerField(default=0)
    dept_content = models.TextField(default='',null=True,blank=True)
    dept_reg_date = models.DateField(auto_now_add=True,null=True)


class DesignationRegister_details(models.Model):
    desig_brd_id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    dept_id = models.ForeignKey(DepartmentRegister_details, on_delete=models.CASCADE, null=True,default='')
    dashboard_id =  models.IntegerField(default=0)
    desig_name = models.CharField(max_length=255,default='',null=True,blank=True)
    desig_content = models.TextField(default='',null=True,blank=True)
    desig_active_status = models.IntegerField(default=0)
    desig_reg_date = models.DateField(auto_now_add=True,null=True)

  
class EmployeeRegister_Details(models.Model):
    logreg_id = models.ForeignKey(LogRegister_Details, on_delete=models.CASCADE, null=True,default='')
    emp_comp_id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    emp_department_id = models.ForeignKey(DepartmentRegister_details, on_delete=models.CASCADE, null=True,default='')
    emp_designation_id = models.ForeignKey(DesignationRegister_details, on_delete=models.CASCADE, null=True,default='')

    emp_name = models.CharField(max_length=255,default='',null=True,blank=True)
    emp_regId = models.CharField(max_length=255,default='',null=True,blank=True)
    emp_contact_no = models.CharField(max_length=255,default='',null=True,blank=True)
    emp_email =  models.EmailField(max_length=255,default='email@gmail.com')
    emp_profile = models.ImageField(upload_to='profiles',default='')
    emp_file = models.FileField(upload_to='employee_files',default='')
    emp_address1 =  models.CharField(max_length=255,default='',null=True,blank=True)
    emp_address2 =  models.CharField(max_length=255,default='',null=True,blank=True)
    emp_address3 =  models.CharField(max_length=255,default='',null=True,blank=True)
    emp_pin =  models.CharField(max_length=50,default='',null=True,blank=True)
    emp_location =  models.CharField(max_length=150,default='',null=True,blank=True)
    emp_district =  models.CharField(max_length=150,default='',null=True,blank=True)
    emp_state =  models.CharField(max_length=150,default='',null=True,blank=True)
    emp_active_status = models.IntegerField(default=0)
    emp_verify_status = models.IntegerField(default=0)
    emp_reg_date = models.DateField(auto_now_add=True,null=True)


