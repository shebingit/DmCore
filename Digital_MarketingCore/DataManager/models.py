from django.db import models
from DM_Head.models import Leads,lead_Details
from Registration_Login.models import BusinessRegister_Details,EmployeeRegister_Details


class DataBank(models.Model):
    lead_Id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    Genarated_date = models.DateField(auto_now_add=True,null=True)
    used_count = models.IntegerField(default=0)
    lead_allocate_status = models.IntegerField(default=0)
    current_status = models.CharField(max_length=150,default='No updation')
    allocated_date = models.DateField(auto_now_add=False,null=True)
    followup_date = models.DateField(auto_now_add=False,null=True)
    lead_status = models.CharField(max_length=150,default='Not Attended')

class PlatForms(models.Model):
    company_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    created_date = models.DateField(auto_now_add=True,null=True)
    platform_Name = models.CharField(max_length=150,default='')
    platform_TotalCount = models.IntegerField(default=0)


class PlatFormsData(models.Model):
    Pfd_company_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    data_add_date = models.DateField(auto_now_add=True,null=True)
    platform_name = models.CharField(max_length=150,default='')
    platform_dataCount = models.IntegerField(default=0)


class FollowupStatus(models.Model):
    status_name = models.CharField(max_length=150,default='')
    company_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')


class FollowupDetails(models.Model):
    lead_Id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    comp_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    hr_telecaller_Id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    response_date = models.DateField(auto_now_add=True,null=True)
    response = models.TextField(default='',null=True,blank=True)
    nextfollowup_date = models.DateField(auto_now_add=False,null=True)
    response_status = models.CharField(max_length=150,default='')

class FollowupHistory(models.Model):
    hs_lead_Id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    hs_comp_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
    hr_telecaller_Id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    allocated_date = models.DateField(auto_now_add=False,null=True)
    note = models.TextField(default='',null=True,blank=True)
    final_status = models.CharField(max_length=150,default='')
