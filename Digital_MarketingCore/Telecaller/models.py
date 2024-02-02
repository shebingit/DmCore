from django.db import models
from  Registration_Login.models import EmployeeRegister_Details,BusinessRegister_Details
from DataManager.models import DataBank
from DM_Head.models import *


class Leads_assignto_tc(models.Model):
    leadId = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    dataBank_ID = models.ForeignKey(DataBank, on_delete=models.CASCADE, null=True,default='')
    TC_Id =  models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    Response = models.CharField(max_length=255,default='',null=True,blank=True)
    Reason = models.CharField(max_length=255,default='',null=True,blank=True)
    Assign_Date = models.DateField(auto_now_add=True,null=True)
    Update_Date = models.DateField(auto_now_add=False,null=True,)
    Next_update_date = models.DateField(auto_now_add=False,null=True)
    Update_Action = models.IntegerField(default=0)
    Status = models.IntegerField(default=0)
    client_id = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='')  

class Leads_Call_Record(models.Model):
    Leads_assignto_tc_id = models.ForeignKey(Leads_assignto_tc, on_delete=models.CASCADE, null=True,default='')
    leadId = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    record_Date = models.DateField(auto_now_add=True,null=True)
    record_time = models.TimeField(auto_now_add=True,null=True)
    Record = models.FileField(upload_to=r'record',default='',null=True,blank=True)

class Waste_Leads(models.Model):
    leadId = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    dbId = models.ForeignKey(DataBank, on_delete=models.CASCADE, null=True,default='')
    client_id = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='') 
    TC_Id =  models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    waste_marked_Date = models.DateField(auto_now_add=True,null=True)
    reason = models.TextField(default='')
    Status = models.IntegerField(default=0)
    confirmation = models.IntegerField(default=0)
    

