from django.shortcuts import render,redirect
from Telecaller.models import Waste_Leads,Leads_assignto_tc
from Registration_Login.models import *
from DataManager.models import  DataBank,FollowupDetails,FollowupHistory,FollowupStatus
from .models import *
from DataManager.models import PlatForms,PlatFormsData
from django.core import serializers
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime,timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count
from datetime import date

from django.conf import settings
import os
import pandas as pd
from openpyxl.workbook import Workbook

from django.http import HttpResponse

from django.contrib import messages

#---------new-------

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def head_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

           # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employee_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_active_status=1).count()
        work_count = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).count()
        client_count = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).count()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employee_count':employee_count,
                    'work_count':work_count,
                    'client_count':client_count}

        return render(request,'HD_dashboard.html',content)

    else:
            return redirect('/')


def view_image(request, image_name):
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)

    if os.path.exists(image_path):
        # Determine the content type based on the file extension
        if image_name.lower().endswith('.png'):
            content_type = 'image/png'
        elif image_name.lower().endswith('.jpg') or image_name.lower().endswith('.jpeg'):
            content_type = 'image/jpeg'
        else:
            content_type = 'image/jpeg'  # You can change this to a default content type

        with open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type=content_type)
            return response

    return HttpResponse("Image not found", status=404)

# Profile Page -------------------------
def head_profile(request):  
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'HD_profile.html',content)

    else:
            return redirect('/')
    

    
def profile_detailsUpdate(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        # Details Save -----------------

        if request.POST:
             
             emp_obj = EmployeeRegister_Details.objects.get(id=dash_details.id)

             emp_obj.emp_name = request.POST['empname']
             emp_obj.emp_contact_no = request.POST['contactno']
             emp_obj.emp_email = request.POST['empEmail']
             emp_obj.emp_address1 = request.POST['add1']
             emp_obj.emp_address2 = request.POST['add2']
             emp_obj.emp_address3 = request.POST['add3']
             emp_obj.emp_pin = request.POST['pincode']
             emp_obj.emp_location = request.POST['loc']
             emp_obj.emp_district = request.POST['empdist']
             emp_obj.emp_state = request.POST['empState']

             if request.FILES.get('empProfile'):
                emp_obj.emp_profile = request.FILES.get('empProfile')

             else:
                emp_obj.emp_profile =  emp_obj.emp_profile 

             if request.FILES.get('empResume'):
                emp_obj.emp_file = request.FILES.get('empResume')

             else:
                emp_obj.emp_file =  emp_obj.emp_file 

             emp_obj.save()
             success_text = 'Profile Details Updated.'
             success = True

             dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        
             content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'success_text':success_text,
                    'success':success}

        else:
            error_text = 'Profile Details Updated.'
            error = True
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'error_text':error_text,
                    'error':error}

        return render(request,'HD_profile.html',content)

    else:
            return redirect('/')
    

# Remove Profile Image ---------------

def profileImage_remove(request):
    emp_id = request.POST.get('emp_id')
    dash_details = EmployeeRegister_Details.objects.get(id=emp_id)
    dash_details.emp_profile = ''
    dash_details.save()
    return JsonResponse({'message': 'Received emp_id: ' + emp_id})
     
# End ------------------------------------------------


# Password Section -----------------------------------

def head_password(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'HD_password.html',content)

    else:
            return redirect('/')


def user_passwordUpdate(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
           
           emp_dash.log_username = request.POST['emp_uname']
           emp_dash.log_password = request.POST['emp_password']

           emp_dash.save()  
           success = True
           success_text = 'User name or password change.'
        
           content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success':success,
                   'success_text':success_text}
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'error':error,
                    'error_text':error_text}

        return render(request,'HD_password.html',content)

    else:
            return redirect('/')


# Work section  ----------------------------------

def Head_work_section(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'HD_workSection.html',content)

    else:
            return redirect('/')


def head_createClient(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        data_box ={} 

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)
        
        if request.POST:
             
            client_obj = ClientRegister()

            client_obj.compId = dash_details.emp_comp_id
            client_obj.client_name = request.POST['cName']
            client_obj.client_email_primary = request.POST['cEmail_1']
            client_obj.client_email_alter = request.POST['cEmail_2']
            client_obj.client_phone = request.POST['cPhno_1']
            client_obj.client_phone_alter = request.POST['cPhno_2']
            client_obj.client_address1 = request.POST['cAddress1']
            client_obj.client_address2 = request.POST['cAddress2']
            client_obj.client_address3 = request.POST['cAddress3']
            client_obj.client_place = request.POST['cPlace']
            client_obj.client_district = request.POST['cDistrict']
            client_obj.client_state = request.POST['cState']
            client_obj.client_profile = request.FILES.get('cProfile')

            # Bussiness Details ----------------------

            client_obj.client_bussiness_name = request.POST['cBussinessName']
            client_obj.client_bussiness_email_primary = request.POST['cBussinessEmail_1']
            client_obj.client_bussiness_email_alter = request.POST['cBussinessEmail_2']
            client_obj.client_bussiness_phone = request.POST['cBussinessPhno_1']
            client_obj.client_bussiness_phone_alter = request.POST['cBussinessPhno_2']
            client_obj.client_bussiness_website = request.POST['cBussinessUrl']
            client_obj.client_bussiness_address1 = request.POST['cBussinessAddress_1']
            client_obj.client_bussiness_address2 = request.POST['cBussinessAddress_2']
            client_obj.client_bussiness_address3 = request.POST['cBussinessAddress_3']
            client_obj.client_bussiness_place = request.POST['cBussinessLoc']
            client_obj.client_bussiness_district = request.POST['cBussinessDistrict']
            client_obj.client_bussiness_state = request.POST['cBussinessState']
            client_obj.bussiness_logo = request.FILES.get('cBussinessLogo')
            client_obj.client_bussiness_file = request.FILES.get('cBussinessFile')
            client_obj.more_discription = request.POST['moreAbout']
            client_obj.client_status = 1
        
            client_obj.save()

            success = True
            success_text= 'Client creation successful.' 

            clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
           
                
            data_box = {'success':success,
                        'success_text':success_text,
                        'clients_obj':clients_obj,
                        'Tasks':Tasks}

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}
            
            content = {**data_box, **content}

            return render(request,'HD_createClient.html',content)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,'Tasks':Tasks}

        return render(request,'HD_createClient.html',content)

    else:
            return redirect('/')


def delete_client(request, client_id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        try:
            client_obj = ClientRegister.objects.get(pk=client_id)
            client_obj.delete()
            error = True
            error_text= 'Client data removed successful.' 
          
            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'error':error,'error_text':error_text,
                        'clients_obj':clients_obj,'Tasks':Tasks}

            return render(request,'HD_createClient.html',content)
        
        except ClientRegister.DoesNotExist:

            return redirect('head_createClient')
             

    else:
        return redirect('/')


def head_createWork(request): 

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)
        

        if request.POST:

            try:
                client_obj = ClientRegister.objects.get(id=int(request.POST['clientId']))
                work_obj = WorkRegister.objects.filter(clientId=client_obj)

                if work_obj.exists():
                    print('Client is already registered for a work.')

                    error =True
                    error_text = 'Client is already registered for a work'
                    
                    content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'error':error,
                        'error_text':error_text,
                        'clients_obj':clients_obj,'Tasks':Tasks}
                

                    return render(request,'HD_createClient.html',content)

                else:
                   
                    work_obj = WorkRegister()
                    client_obj = ClientRegister.objects.get(id=int(request.POST['clientId']))
                    work_obj.clientId = client_obj
                    work_obj.work_create_date = request.POST['start_date']
                    work_obj.work_end_date = request.POST['end_date']
                    work_obj.work_discription = request.POST['work_discription']
                    work_obj.work_file = request.FILES.get('work_file')
                    work_obj.wcompId = dash_details.emp_comp_id
                    work_obj.save()
                    client_obj.work_reg_status = 1
                    client_obj.save()

                    tasks_list = request.POST.getlist('task_name')


                    for task in tasks_list:
                        task_obj = ClientTask_Register()
                        task_obj.cTcompId = dash_details.emp_comp_id
                        task_obj.work_Id = work_obj
                        task_obj.client_Id = client_obj
                        task_obj.task_name = task
                        task_obj.task_create_date = date.today()
                        task_obj.save()

                    success = True
                    success_text= 'Work and Tasks creation successful.' 

                    clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
                    Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)
                        
                
                    content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'success':success,
                        'success_text':success_text,
                        'clients_obj':clients_obj,'Tasks':Tasks}
                

                    return render(request,'HD_createClient.html',content)
                
            except ClientRegister.DoesNotExist:
                    print('Client data not Found')
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'Tasks':Tasks}

        return render(request,'HD_createClient.html',content)

    else:
            return redirect('/')


def head_registerWorks(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        lead_category_obj = LeadCategory_Register.objects.all()

        wt_obj = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'lead_category_obj':lead_category_obj,
                   'wt_obj':wt_obj,
                   'works_obj':works_obj,'client_task_obj':client_task_obj}

        return render(request,'HD_workCreated.html',content)

    else:
            return redirect('/')
    

def head_lead_categoryadd(request):

    if request.POST:
        taskID = int(request.POST['task_ID'])

        try:

            cl_obj = ClientTask_Register.objects.get(id=taskID)

            lc_obj = LeadCategory_Register()
            lc_obj.cTaskId = cl_obj
            lc_obj.lead_collection_for = request.POST['head_name']
            lc_obj.lc_discription = request.POST['Cl_discription']
            lc_obj.lc_target = request.POST['target_number']
            lc_obj.lc_file = request.FILES.get('lc_file')
            lc_obj.save()

            return redirect('head_registerWorks')

        except ClientTask_Register.DoesNotExist:

            return redirect('head_registerWorks')
    else:

        return redirect('head_registerWorks')
    

def head_lead_categoryedit(request):

    if request.POST:

        try:

            lc_obj = LeadCategory_Register.objects.get(id=int(request.POST['lc_ID']))

            lc_obj.lead_collection_for = request.POST['head_name']
            lc_obj.lc_discription = request.POST['Cl_discription']
            lc_obj.lc_target = request.POST['target_number']

            if request.FILES.get('lc_file'):

                lc_obj.lc_file = request.FILES.get('lc_file')
            else:
                lc_obj.lc_file =  lc_obj.lc_file 

            lc_obj.save()

            return redirect('head_registerWorks')

        except ClientTask_Register.DoesNotExist:

            return redirect('head_registerWorks')
    else:

        return redirect('head_registerWorks')



def delete_lead_category(request,lc_id):
    try:
        lead_category_obj = LeadCategory_Register.objects.get(id=lc_id)
        lead_category_obj.delete()

        return redirect('head_registerWorks')
    
    except LeadCategory_Register.DoesNotExist:
        return redirect('head_registerWorks')

    

def delete_work(request,work_id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        
        works_delete_obj = WorkRegister.objects.get(id=work_id)
        client = ClientRegister.objects.get(id=works_delete_obj.clientId.id)
        client.work_reg_status = 0
        client.save()
        works_delete_obj.delete()
        error = True
        error_text = 'Opps! Work Removed successfully.'
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'error':error,'error_text':error_text,
                   'works_obj':works_obj,'client_task_obj':client_task_obj}

        return render(request,'HD_workCreated.html',content)

    else:
            return redirect('/')
    

def delete_task(request,task_id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        
       
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')

        task_delete_obj = ClientTask_Register.objects.get(id=task_id)
        task_delete_obj.delete()

        error = True
        error_text = 'Opps! Task Removed successfully.'

        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'error':error,'error_text':error_text,
                   'works_obj':works_obj,'client_task_obj':client_task_obj}

        return render(request,'HD_workCreated.html',content)

    else:
            return redirect('/')

    
def head_clientEdit(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        if request.POST:
             
            client_obj = ClientRegister.objects.get(id=pk)

            client_obj.compId = dash_details.emp_comp_id
            client_obj.client_name = request.POST['cName']
            client_obj.client_email_primary = request.POST['cEmail_1']
            client_obj.client_email_alter = request.POST['cEmail_2']
            client_obj.client_phone = request.POST['cPhno_1']
            client_obj.client_phone_alter = request.POST['cPhno_2']
            client_obj.client_address1 = request.POST['cAddress1']
            client_obj.client_address2 = request.POST['cAddress2']
            client_obj.client_address3 = request.POST['cAddress3']
            client_obj.client_place = request.POST['cPlace']
            client_obj.client_district = request.POST['cDistrict']
            client_obj.client_state = request.POST['cState']

            if request.FILES.get('cProfile'):

                client_obj.client_profile = request.FILES.get('cProfile')
            else:
                client_obj.client_profile = client_obj.client_profile

            # Bussiness Details ----------------------

            client_obj.client_bussiness_name = request.POST['cBussinessName']
            client_obj.client_bussiness_email_primary = request.POST['cBussinessEmail_1']
            client_obj.client_bussiness_email_alter = request.POST['cBussinessEmail_2']
            client_obj.client_bussiness_phone = request.POST['cBussinessPhno_1']
            client_obj.client_bussiness_phone_alter = request.POST['cBussinessPhno_2']
            client_obj.client_bussiness_website = request.POST['cBussinessUrl']
            client_obj.client_bussiness_address1 = request.POST['cBussinessAddress_1']
            client_obj.client_bussiness_address2 = request.POST['cBussinessAddress_2']
            client_obj.client_bussiness_address3 = request.POST['cBussinessAddress_3']
            client_obj.client_bussiness_place = request.POST['cBussinessLoc']
            client_obj.client_bussiness_district = request.POST['cBussinessDistrict']
            client_obj.client_bussiness_state = request.POST['cBussinessState']

            if request.FILES.get('cBussinessLogo'):

                client_obj.bussiness_logo = request.FILES.get('cBussinessLogo')

            else:
                client_obj.bussiness_logo =  client_obj.bussiness_logo

            if request.FILES.get('cBussinessFile'):
                
                client_obj.client_bussiness_file = request.FILES.get('cBussinessFile')
            else:
                client_obj.client_bussiness_file = client_obj.client_bussiness_file 

            client_obj.more_discription = request.POST['moreAbout']
            client_obj.client_status = 1
        
            client_obj.save()

            clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')

            success = True
            success_text= 'Client details edit successful.' 

            

            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'success':success,
                        'success_text':success_text,
                        'clients_obj':clients_obj,
                        'Tasks':Tasks
                        }
        
            return render(request,'HD_createClient.html',content)
        
        else:
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,'Tasks':Tasks}
            

            return render(request,'HD_createClient.html',content)

    else:
        return redirect('/')


def head_workDetailsEdit(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        if request.POST:
            
            works = WorkRegister.objects.get(id=pk)
            works.work_discription =  request.POST['wDiscription']
            works.work_create_date = request.POST['wSdate']
            works.work_end_date = request.POST['wEdate']
            if request.FILES.get('wFile'):
                works.work_file = request.FILES.get('wFile')
            else:
                 works.work_file = works.work_file 

            works.save()  
            
            success = True
            success_text= 'Work details edit successful.' 

            works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')

            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'success':success,
                    'success_text':success_text,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

            return render(request,'HD_workCreated.html',content)
        
        else:
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

            return render(request,'HD_workCreated.html',content)
             

    else:
            return redirect('/')


def head_work_taskadd(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        wt_obj = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id)
        
        if request.POST:

                work_obj = WorkRegister.objects.get(id=int(request.POST['Worktask_ID']))
                    
                clientTask_obj = ClientTask_Register()
                
                
                if 1 == int(request.POST['radio-btn']) :
                   
                    wa = Work_Task.objects.get(id=request.POST['company_task_name'])
                    clientTask_obj.task_name = wa.task_name 
                    
                else:
                    clientTask_obj.task_name = request.POST['task_name']
                   

                clientTask_obj.task_discription = request.POST['task_discription']
                clientTask_obj.task_file = request.FILES.get('task_file') 
                clientTask_obj.task_status = 1
                clientTask_obj.cTcompId = dash_details.emp_comp_id
                clientTask_obj.client_Id = work_obj.clientId
                clientTask_obj.work_Id = work_obj
                clientTask_obj.task_create_date = date.today()
                clientTask_obj.save()

                success = True
                success_text= 'Task add successful.' 
                client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

                content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'success':success,
                    'success_text':success_text,
                    'wt_obj':wt_obj,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

                return render(request,'HD_workCreated.html',content)
        else:
            
            return redirect('head_registerWorks')

    else:
            return redirect('/')
    

def head_work_taskedit(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        
        if request.POST:
                
                clientTaskEdit_obj = ClientTask_Register.objects.get(id=int(request.POST['taskId']))
                company_task = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id)

                found = False
                for comp_task_pro in company_task:
                     
                    if comp_task_pro.task_name == clientTaskEdit_obj.task_name :   
                        found = True
                if not found:
                    clientTaskEdit_obj.task_name = request.POST['edit_task_name']
                else:
                    clientTaskEdit_obj.task_name = clientTaskEdit_obj.task_name 
               
                clientTaskEdit_obj.task_discription = request.POST['edit_task_discription']
                clientTaskEdit_obj.task_file = request.FILES.get('edit_task_file') 
                clientTaskEdit_obj.save()

                success = True
                success_text= 'Task edit successful.' 
                client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)
             

                content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'success':success,
                    'success_text':success_text,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

                return render(request,'HD_workCreated.html',content)
        else:
            
            return redirect('head_registerWorks')

    else:
            return redirect('/')

      
# Lead Section ----------------

def head_lead_fieldForm(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj)
        lead_category_obj = LeadCategory_Register.objects.filter(cTaskId__client_Id__in=clients_obj)
        leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

        if request.POST:

            field_obj = LeadField_Register()
            wrk = WorkRegister.objects.get(id=int(request.POST['w_ID']))
            lc = LeadCategory_Register.objects.get(id=int(request.POST['lc_ID']))
            field_obj.field_work_regId = wrk
            field_obj.field_lead_category = lc
            field_obj.field_clientId = wrk.clientId
            field_obj.field_name = request.POST['fieldName']
            field_obj.field_discription = request.POST['field_Discription']
            field_obj.save()
            leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'lead_category_obj':lead_category_obj,
                    'leadfield_obj':leadfield_obj,
                    }

        return render(request,'HD_LeadFields.html',content)

    else:
            return redirect('/')         


def head_transfer_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        clients_ids = ClientTask_Register.objects.filter(task_name='Lead Collection',
                                                         cTcompId__id=dash_details.emp_comp_id.id).values('client_Id')
    
        client_ids_list = [item['client_Id'] for item in clients_ids]
        leads_obj = Leads.objects.filter(lead_work_regId__clientId__id__in=client_ids_list,
                                         lead_status=1,
                                         waste_data=0,
                                         lead_transfer_status=0,
                                         repeated_status=0)

        Cl_ID = None
        Ct_ID = None
        d1 = None
        d2 = None
        emp = None

        if request.POST:
            Cl_ID = request.POST['client_change']
            Ct_ID = request.POST['category_name']
            emp = request.POST['select_emp']
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            pg_num = request.POST['pgnum']

        else :
            Cl_ID = request.GET.get('Cl_ID')
            Ct_ID = request.GET.get('Ct_ID')
            emp = request.GET.get('employee')
            d1 = request.GET.get('start_date')
            d2 = request.GET.get('end_date')
            pg_num = request.GET.get('pg_num')

        if pg_num is None:
            pg_num = 100


        if Cl_ID and Ct_ID:
            leads_obj = leads_obj.filter(lead_work_regId__clientId__id=Cl_ID,lead_category_id__id=Ct_ID)
            
        if d1:
            leads_obj = leads_obj.filter(lead_add_date__gte=d1)
        if d2:
            leads_obj = leads_obj.filter(lead_add_date__lte=d2)
        if emp:
            leads_obj = leads_obj.filter(lead_collect_Emp_id__id=emp)


            
        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)
        
        paginator = Paginator(leads_obj, pg_num)  
        page_number = request.GET.get('page')
       
        leads = paginator.get_page(page_number)

        leads_obj_count = leads_obj.count()
        
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'executive_data':executive_data,
                    'works_obj':works_obj,
                    'clients_objs':clients_objs,
                    'leads':leads,
                    'leads_obj_count':leads_obj_count,
                    'Cl_ID':Cl_ID,'Ct_ID':Ct_ID,'employee':emp,'start_date':d1,'end_date':d2,'pg_num':pg_num
                    
                    }

        return render(request,'HD_TransferLead.html',content)

    else:
            return redirect('/')     


def head_transferred_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)

        leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,
                                         lead_status=1,
                                         lead_transfer_status=1,
                                         lead_transfer_date=date.today()).order_by('-lead_transfer_date')
        
        leads_obj_count = leads_obj.count()

        date1 = None
        date2 = None
        emp = None
        select_val = None

        if request.POST:
            date1 = request.POST['sdate']
            date2 = request.POST['edate']
            emp = request.POST['select_emp']
            select_val = request.POST['select_val']

            if select_val == 'All':

                leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=1).order_by('-lead_transfer_date')

            if date1:
                leads_obj = leads_obj.filter(lead_transfer_date__gte=date1)
                
            if date2:
                leads_obj = leads_obj.filter(lead_transfer_date__lte=date2)
            
            if emp:
                leads_obj = leads_obj.filter(lead_collect_Emp_id__id=emp)
                emp = EmployeeRegister_Details.objects.get(id=emp)

            leads_obj_count = leads_obj.count()

        
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                    'leads_obj_count':leads_obj_count,
                     'executive_data':executive_data,
                     'date1':date1,'date2':date2,'emp':emp,'select_val':select_val
                    }

        return render(request,'HD_TransferredLead.html',content)

    else:
            return redirect('/')     
     

def head_waste_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')



        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,waste_data=1).order_by('-lead_add_date')

        # Waste leads 
        waste_objs = Waste_Leads.objects.filter(confirmation=1,leadId__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id)
        waste_obj_count = Waste_Leads.objects.filter(confirmation=0,leadId__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id).count()

        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        telecaller_data = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        
        Cl_ID = None
        Ct_ID = None
        d1 = None
        d2 = None
        d3 = None
        d4 = None
        emp = None
        telecaller_emp = None
        client_name = None
        category_name = None
        select_emp = None
        select_telecaller_emp = None

        if request.POST:
            Cl_ID = request.POST['client_change']
            Ct_ID = request.POST['category_name']
            emp = request.POST['select_emp']
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            d3 = request.POST['waste_sdate']
            d4 = request.POST['waste_edate']
            telecaller_emp = request.POST['select_telecaller_emp']
            pg_num = request.POST['pgnum']

        else :
            Cl_ID = request.GET.get('Cl_ID')
            Ct_ID = request.GET.get('Ct_ID')
            emp = request.GET.get('employee')
            d1 = request.GET.get('start_date')
            d2 = request.GET.get('end_date')
            d3 = request.GET.get('wsdate')
            d4 = request.GET.get('wedate')
            telecaller_emp = request.GET.get('telecaller')
            pg_num = request.GET.get('pg_num')

        if pg_num is None:
            pg_num = 10


        if telecaller_emp:
            waste_objs = waste_objs.filter(TC_Id__id=telecaller_emp).values_list('leadId')
            
            leads_obj = leads_obj.filter(id__in=waste_objs)
            select_telecaller_emp = EmployeeRegister_Details.objects.get(id=telecaller_emp)


        if Cl_ID and Ct_ID:
            leads_obj = leads_obj.filter(lead_work_regId__clientId__id=Cl_ID,lead_category_id__id=Ct_ID)
            client_name = ClientRegister.objects.get(id=Cl_ID)
            category_name = LeadCategory_Register.objects.get(id=Ct_ID)
            
        if d1:
            leads_obj = leads_obj.filter(lead_add_date__gte=d1)
        if d2:
            leads_obj = leads_obj.filter(lead_add_date__lte=d2)
        if emp:
            leads_obj = leads_obj.filter(lead_collect_Emp_id__id=emp)
            select_emp = EmployeeRegister_Details.objects.get(id=emp)

        leads_obj_count = leads_obj.count()

        
        
        paginator = Paginator(leads_obj, pg_num) 
        
        page_number = request.GET.get('page')
       
        leads = paginator.get_page(page_number)

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'waste_obj_count':waste_obj_count,
                    'leads_obj_count':leads_obj_count,
                    'clients_objs':clients_objs,
                    'executive_data':executive_data,
                    'telecaller_data':telecaller_data,
                    'leads':leads,
                    'Cl_ID':Cl_ID,'Ct_ID':Ct_ID,'employee':emp,'start_date':d1,'end_date':d2,'pg_num':pg_num,
                    'select_emp':select_emp,'client_name':client_name,'category_name':category_name,
                    'telecaller':telecaller_emp,
                    'd3':d3,'d4':d4,'telecaller_emp':telecaller_emp,'select_telecaller_emp':select_telecaller_emp,
                    }


        return render(request,'HD_WasteLead.html',content)

    else:
            return redirect('/')    


def datamanager_wasteLead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        telecaller_data = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        leads_obj = Waste_Leads.objects.filter(leadId__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,confirmation=0).order_by('-waste_marked_Date')

        Cl_ID = None
        Ct_ID = None
        d1 = None
        d2 = None
        d3 = None
        d4 = None
        emp = None
        telecaller_emp = None
        client_name = None
        category_name = None
        select_emp = None
        select_telecaller_emp = None



        if request.POST:
            Cl_ID = request.POST['client_change']
            Ct_ID = request.POST['category_name']
            emp = request.POST['select_emp']
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            d3 = request.POST['waste_sdate']
            d4 = request.POST['waste_edate']
            telecaller_emp = request.POST['select_telecaller_emp']
            pg_num = request.POST['pgnum']

        else :
            Cl_ID = request.GET.get('Cl_ID')
            Ct_ID = request.GET.get('Ct_ID')
            emp = request.GET.get('employee')
            d1 = request.GET.get('start_date')
            d2 = request.GET.get('end_date')
            d3 = request.GET.get('wsdate')
            d4 = request.GET.get('wedate')
            telecaller_emp = request.GET.get('telecaller')
            pg_num = request.GET.get('pg_num')

        if pg_num is None:
            pg_num = 10
            


        if Cl_ID and Ct_ID:
            leads_obj = leads_obj.filter(leadId__lead_work_regId__clientId__id=Cl_ID,leadId__lead_category_id__id=Ct_ID)
            client_name = ClientRegister.objects.get(id=Cl_ID)
            category_name = LeadCategory_Register.objects.get(id=Ct_ID)

        if d1:
          
            leads_obj = leads_obj.filter(leadId__lead_add_date__gte=d1)
        if d2:
            leads_obj = leads_obj.filter(leadId__lead_add_date__lte=d2)

            
        if d3:
            leads_obj = leads_obj.filter(waste_marked_Date__gte=d3)

        if d4:
            leads_obj = leads_obj.filter(waste_marked_Date__lte=d4)

        if emp:
            leads_obj = leads_obj.filter(leadId__lead_collect_Emp_id__id=emp)
            select_emp = EmployeeRegister_Details.objects.get(id=emp)

        if telecaller_emp:
            leads_obj = leads_obj.filter(TC_Id__id=telecaller_emp)
            select_telecaller_emp = EmployeeRegister_Details.objects.get(id=telecaller_emp)

        leads_obj_count = leads_obj.count()

        paginator = Paginator(leads_obj, pg_num) 
        
        page_number = request.GET.get('page')
       
        leads = paginator.get_page(page_number)
        
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'leads_obj_count':leads_obj_count,
                    'clients_objs':clients_objs,
                    'executive_data':executive_data,
                    'telecaller_data':telecaller_data,
                    'leads':leads,
                    'Cl_ID':Cl_ID,'Ct_ID':Ct_ID,'employee':emp,'start_date':d1,'end_date':d2,'pg_num':pg_num,
                    'telecaller':telecaller_emp,
                    'd3':d3,'d4':d4,'telecaller_emp':telecaller_emp,'select_telecaller_emp':select_telecaller_emp,
                    'select_emp':select_emp,'client_name':client_name,'category_name':category_name
                    
                    }


        return render(request,'HD_DAMWasteLead.html',content)

    else:
            return redirect('/')  


def hd_wastelead_confirm_reject(request,wasteid):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            status_v = request.POST['status_val']
            status_reason = request.POST['head_reason']
            confirm_obj = Waste_Leads.objects.get(id=wasteid)
            confirm_obj.confirmation=status_v
            confirm_obj.head_reason = status_reason
            confirm_obj.save()
           
            if status_v == '2':
                success_text='Data rejected successfully.'
            else:
                success_text='Data confirmed as waste successfully.'
                

                # Waste Data notification----

                emp_obj = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=5)

                for emp in emp_obj:

                    notific_obj = Notification()
                    notific_obj.emp_id = emp
                    notific_obj.notific_head =' Waste Lead Confirmation.'
                    notific_obj.notific_content = (
                        dash_details.emp_name +
                        ' ( ' +
                        dash_details.emp_designation_id.desig_name +
                        ' ) ' +
                        ' has confirmed the lead ' +
                        confirm_obj.leadId.lead_name +
                        ' ( ' +
                        confirm_obj.leadId.lead_category_id.lead_collection_for +
                    ' ) as a waste lead.'
                    )

                    notific_obj.notific_time = timezone

                    notific_obj.save()

            success = True

        leads_obj = Waste_Leads.objects.filter(leadId__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,confirmation=0).order_by('Status')
        leads_obj_count = leads_obj.count()
      
        
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'success_text':success_text,
                    'success':success,
                    'leads_obj':leads_obj,
                    'leads_obj_count':leads_obj_count,
                    
                    }


        return render(request,'HD_DAMWasteLead.html',content)

    else:
            return redirect('/')  


def Head_lead_data(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj)
        client_tasks = ClientTask_Register.objects.filter(work_Id__in=works_obj,task_name='lead collection')
        leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)
        lc_obj = LeadCategory_Register.objects.filter(cTaskId__in=client_tasks)

        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'client_tasks':client_tasks,
                    'leadfield_obj':leadfield_obj,
                    'lc_obj':lc_obj
                    }

        return render(request,'HD_Leaddata.html',content)

    else:
            return redirect('/')    


def HD_featchLeadFields(request):
    if request.method == 'GET':
        category_Id = request.GET.get('category_Id')

        try:
           
            lc_obj = LeadCategory_Register.objects.get(id=category_Id)
          
            lead_fields = LeadField_Register.objects.filter(field_lead_category=lc_obj)
            lead_fields_list = []  

            for fields in lead_fields:
                lead_fields_list.append(fields.field_name)

            return JsonResponse({'category_fields': lead_fields_list})
        
        except LeadCategory_Register.DoesNotExist:
            return JsonResponse({'error': ' Categoryr not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)     


     
def head_lead_collected_data(request,pk,lcID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.get(id=pk)
        lc_obj=LeadCategory_Register.objects.get(id=lcID)
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,
                                         lead_category_id__id=lcID,
                                         lead_transfer_status=0,
                                         waste_data=0,
                                         lead_status=0,
                                         repeated_status=0).order_by('-lead_add_date')
        
        leads_obj_count = leads_obj.count()



        # Day report ---------------------------


        Total_lead = Leads.objects.filter(lead_work_regId=works_obj,
                                        lead_category_id__id=lcID,lead_add_date=date.today())
        
        Total_lead_count = Total_lead.count()
        
        unverify_lead = Total_lead.filter(lead_status=0).count()
        verify_lead = Total_lead.filter(lead_status=1).count()
        repeated_lead = Total_lead.filter(repeated_status=1).count()
        waste_lead = Total_lead.filter(waste_data=1).count()
        unverify_exlcude = Total_lead.filter(lead_status=0,waste_data=0,repeated_status=0).count()


        transfer_lead = Leads.objects.filter(lead_work_regId=works_obj,
                                             lead_status=1,lead_transfer_status=1,
                                        lead_category_id__id=lcID,lead_transfer_date=date.today()).count()
     
        pending_lead = Total_lead.filter(lead_status=1,lead_transfer_status=0).count()
        

    #-------------------------------------------------------------------

        
        d1= None
        d2= None
        emp_id = None
        status_change = None
        pg_num = 100

        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            emp_id = request.POST['select_emp']
            status_change = request.POST['select_status']
            pg_num = request.POST['pgnum']

        else: 
            d1 = request.GET.get('start_date')
            d2 = request.GET.get('end_date')
            emp_id = request.GET.get('employee')
            status_change = request.GET.get('status')
            pg_num = request.GET.get('pg_num')

            if pg_num is None:
                pg_num = 100

        
        if status_change  :

            leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_category_id__id=lcID,lead_transfer_status=0).order_by('-lead_add_date')
        
        else:
            status_change ='Unverified'
            leads_obj = Leads.objects.filter(lead_work_regId=works_obj,
                                         lead_category_id__id=lcID,
                                         lead_transfer_status=0,
                                         waste_data=0,
                                         lead_status=0,
                                         repeated_status=0).order_by('-lead_add_date')
            
        if d1:

                leads_obj = leads_obj.filter(lead_add_date__gte=d1)
               

        if d2:
                leads_obj = leads_obj.filter(lead_add_date__lte=d2)
                
            
        if emp_id :

                leads_obj = leads_obj.filter(lead_collect_Emp_id__id=emp_id)
                


        
        
        if status_change == 'Verified':
            status_val=1
            leads_obj = leads_obj.filter(lead_status=status_val)

        if status_change == 'Unverified':
            status_val=0
            leads_obj = leads_obj.filter(lead_status=status_val,
                                             lead_transfer_status=0,
                                             waste_data=0,
                                             repeated_status=0)
        if status_change == 'Waste':
            status_val=1
            leads_obj = leads_obj.filter(waste_data=status_val)

        if status_change == 'Repeated':
                status_val=1
                leads_obj = leads_obj.filter(repeated_status=status_val)

        if status_change == 'Incompleted':
                status_val=1
                leads_obj = leads_obj.filter(lead_incomplete_status=status_val)

        if status_change == 'Transfer':
            leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_category_id__id=lcID,lead_transfer_status=1).order_by('-lead_add_date')
            
            if d1:

                leads_obj = leads_obj.filter(lead_transfer_date__gte=d1)
                

            if d2:
                leads_obj = leads_obj.filter(lead_transfer_date__lte=d2)
               

            if emp_id :

                leads_obj = leads_obj.filter(lead_collect_Emp_id__id=emp_id)

                
        leads_obj_count = leads_obj.count()

       

        paginator = Paginator(leads_obj, pg_num)  
        page_number = request.GET.get('page')
       
        leads = paginator.get_page(page_number)


        lf_obj = LeadField_Register.objects.filter(field_lead_category__id=lcID)

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                     'leads_obj_count':leads_obj_count,
                     'lc_obj':lc_obj,
                     'lf_obj':lf_obj,
                     'executive_data':executive_data,
                     'lcID':lcID,
                     'leads_obj':leads_obj,
                     'status_change':status_change,
                     'leads': leads, 'status': status_change, 'employee': emp_id, 'start_date': d1, 'end_date': d2,
                     'pg_num':pg_num,
                     'Total_lead_count':Total_lead_count,
                     'unverify_lead':unverify_lead,
                        'verify_lead':verify_lead,
                        'transfer_lead':transfer_lead,
                        'pending_lead':pending_lead,
                        'repeated_lead':repeated_lead,
                        'waste_lead':waste_lead,
                        'today_date':date.today(),
                        'unverify_exlcude':unverify_exlcude

                    }

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')
    


# april 02 2024 ----------------------

def lead_status_change(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

    selected_value = request.POST.get('selected_value')
    checked_values = request.POST.get('checked_values')

    id_list = checked_values.split(',') 
    works_obj = request.POST.get('wID')
    lcID = request.POST.get('lID')
    reason = request.POST.get('wasteReason')

    if selected_value:
        count_val = 0
        for ids in id_list:
            count_val = count_val + 1

            try:
                    leads_obj = Leads.objects.get(id=ids,
                                                lead_work_regId__id=works_obj,
                                                lead_category_id__id=lcID,
                                                lead_transfer_status=0)
            except Leads.DoesNotExist:
                    continue

            if selected_value == 'Verified':
                status_val=1
                leads_obj.lead_status=status_val
                leads_obj.repeated_status=0
                leads_obj.waste_data=0

            if selected_value == 'Unverified':
                status_val=0
                leads_obj.lead_status=status_val
                
            if selected_value == 'Waste':
                            status_val=1
                            leads_obj.waste_data=status_val
                            leads_obj.waste_data_reason = dash_details.emp_name + ' ( ' +  str(date.today())  +' ) ' + ' :- ' +  reason
            
            if selected_value == 'Unwaste':
                            status_val=0
                            leads_obj.waste_data=status_val

            if selected_value == 'Incompleted':
                            status_val=1
                            leads_obj.lead_incomplete_status=status_val
            leads_obj.save()

            if selected_value == 'Delete':
                status_val=1
                leads_obj.delete()
           
        
    return JsonResponse({'message': f'Data marked as {count_val} successfully for {selected_value}.','work_id':works_obj,'lcid':lcID})


def HD_featchLeadDetails(request):
    if request.method == 'GET':
        lead_id = request.GET.get('lead_id')
        try:
            lead_more=[]

            lead = Leads.objects.get(id=lead_id)
            if lead.lead_status == 1:
                verify='Lead is Verified'
            else:
                 verify='Lead is Unverified'

            if lead.waste_data == 1:
                waste='Lead is marked as waste '
            else:
                 waste='Lead is  not a waste'

            if lead.lead_incomplete_status == 1:
                incomplete='Incompleted Data'
            else:
                incomplete='Not Marked as Incompleted '
            lead_basic = {
                'name': lead.lead_name,
                'email': lead.lead_email,
                'phone': lead.lead_contact,
                'verify':verify,
                'waste':waste,
                'incomplete':incomplete,
                'source':lead.lead_source
            }

            lead_details = lead_Details.objects.filter(leadId=lead)
            lead_details_dict = {}  
            for detail in lead_details:
                lead_details_dict[detail.lead_field_name] = detail.lead_field_data

            return JsonResponse({'lead_basic': lead_basic, 'lead_details': lead_details_dict})
        
        except Leads.DoesNotExist:
            return JsonResponse({'error': 'Lead not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

     
def categoryleadt_details(request,catelcid):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        leads_obj = Leads.objects.get(id=catelcid)
        lc_obj=LeadCategory_Register.objects.get(id=leads_obj.lead_category_id.id)
        
        lf_obj = LeadField_Register.objects.filter(field_lead_category__id=lc_obj.id)
       
        lead_Details_obj = lead_Details.objects.filter(leadId=leads_obj)
        lcID = lc_obj.id

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    
                    'leads_obj':leads_obj,
                     'lead_Details_obj':lead_Details_obj,
                     'lf_obj':lf_obj,
                     'lcID':lcID,
                     'lc_obj':lc_obj
                    }

        return render(request,'HD_category_leadDetails.html',content)

    else:
            return redirect('/')




def Head_lead_add(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.get(id=pk)

        data_list={}

        if request.POST:
             

            ld_obj = Leads()
            ld_obj.lead_work_regId = works_obj
            ld_obj.lead_collect_Emp_id = dash_details
            ld_obj.lead_name = request.POST['leadName']
            ld_obj.lead_email = request.POST['leadEmail']
            ld_obj.lead_contact =request.POST['leadContact']
            ld_obj.lead_source =request.POST['source']
            ld_obj.lead_add_time =  timezone.now()
            ld_obj.lead_category_id =LeadCategory_Register.objects.get(id=request.POST['lcid'])
            ld_obj.save()
            lcID = request.POST['lcid']

            lead_deatils_data  = request.POST.getlist('leadfield')
        
            ldr_obj = LeadField_Register.objects.values_list('field_name').filter(field_lead_category=ld_obj.lead_category_id)

            for ld,ldn in zip(lead_deatils_data,ldr_obj) :

                ldetails_obj = lead_Details()
                ldetails_obj.lead_field_name = ldn[0]
                ldetails_obj.lead_field_data = ld
                ldetails_obj.leadId = ld_obj
                ldetails_obj.save()
            
            success = True
            success_text = 'Lead details add successfull.'
            
            data_list = {'success':success,'success_text':success_text}  
                 
        
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj,field_lead_category__id=lcID)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_category_id__id=lcID)
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_category_id__id=lcID).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                    'lead_Details_obj':lead_Details_obj,
                    'leads_obj_count':leads_obj_count,
                    'lf_obj':lf_obj,
                    'lcID':lcID
                    }
        
        content = {**data_list,**content}

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')
     
# Excel File Create Section ---------------------------------------

    
def download_excel(request,pk,lID):
    wId = WorkRegister.objects.get(id=pk)
 
    data = LeadField_Register.objects.filter(field_work_regId=wId).values('field_name')

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    additional_headers = ["Full Name", "Email Id", "Contact Number", "Source of Lead", "Lead Add Time"]

    headers = list(LeadField_Register.objects.filter(field_work_regId=wId,field_lead_category__id=lID).values_list('field_name', flat=True))
    all_headers = additional_headers + headers
    ws.append(all_headers)

    lc_obj = LeadCategory_Register.objects.get(id=lID)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{wId.clientId.client_name}_{lc_obj.lead_collection_for}.xlsx"'

    # Save the Excel workbook to the response
    wb.save(response)

    return response

# Excel file data add to  Leads modal--------------
def Head_lead_file_upload(request,pk,lcID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.get(id=pk)
        data_list = {}

        if request.POST:


            exfile = request.FILES.get('upload_File')

            # Read the Excel file using pandas
            df = pd.read_excel(exfile)

            # Check if the DataFrame is empty
            if df.empty:
                return redirect('head_lead_collected_data',pk,lcID)
            
            else:

                # Create a list of column headers from the DataFrame
                headers = df.columns.tolist()

                # Process and save the data to the Lead model (adjust as needed)
                lcr = LeadCategory_Register.objects.get(id=lcID)
                for _, row in df.iterrows():
                 
                    lead_data = {header: str(row[header]) for header in headers}


                    lead_exists = Leads.objects.filter(lead_email=lead_data['Email Id'],lead_category_id=lcr).exists() or Leads.objects.filter(lead_contact=lead_data['Contact Number'],lead_category_id=lead_category).exists()
                    
                    lead = Leads()

                    if lead_exists:
                        lead.repeated_status=1
                    else:
                        lead.repeated_status=0

                    lead.lead_work_regId = works_obj
                    lead.lead_collect_Emp_id = dash_details
                    lead.lead_name = lead_data['Full Name']
                    lead.lead_email = lead_data['Email Id']
                    lead.lead_source = lead_data['Source of Lead']
                    lead.lead_add_time = lead_data['Lead Add Time']
                    lead.lead_category_id= LeadCategory_Register.objects.get(id=lcID)
                    phno = str(lead_data.get('Contact Number', ''))
                    lead.waste_data=0
                    lead.lead_contact = phno
                    lead.save()

                    for key, value in lead_data.items():
                        if key not in ('Full Name', 'Email Id', 'Contact Number','Source of Lead'):
                            lead_details = lead_Details(leadId=lead, lead_field_name=key, lead_field_data=value)
                            lead_details.leadId = lead
                            lead_details.save()


                success = True
                success_text = 'File uploaded successfully.'
                data_list = {'success':success,'success_text':success_text}


        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj,field_lead_category__id=lcID)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_category_id__id=lcID)
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_category_id__id=lcID).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)

        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'lf_obj':lf_obj,
                    'leads_obj':leads_obj,
                    'lead_Details_obj':lead_Details_obj,
                    'leads_obj_count':leads_obj_count,
                    'lcID':lcID
                    }
        
        content = {**data_list, **content}

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')
    


def head_all_leadTransfer(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        count_val = 0
        trns_val = 0
        bal_lead = 0

        if request.POST:
            
            if request.POST.getlist('lead_check'):
                leadChecked = request.POST.getlist('lead_check')
                leads_obj = Leads.objects.filter(id__in=leadChecked,lead_status=1,waste_data=0,lead_transfer_status=0)

                for l in leads_obj:
                    #lead_ids_list = []
                   

                    try:
                        #leads_obj_check = Leads.objects.get(id=l.id)
                            count_val = count_val + 1

                        # email_exists = DataBank.objects.filter(lead_Id__lead_category_id=leads_obj_check.lead_category_id,lead_Id__lead_email=leads_obj_check.lead_email).exists()
                        # phone_exists = DataBank.objects.filter(lead_Id__lead_category_id=leads_obj_check.lead_category_id,lead_Id__lead_contact=leads_obj_check.lead_contact).exists()

                        # if email_exists or phone_exists:
                        #     lead_id = l.id
                        #     l.repeated_status = 1
                        #     l.waste_data = 1
                        #     l.waste_data_reason = 'The email id or contact number already exist.'
                        #     l.save()
                        #     lead_ids_list.append(lead_id)

                        # else:
 
                            l.lead_transfer_status = 1
                            l.lead_transfer_date = date.today()
                            l.save()
                            db_obj = DataBank()
                            db_obj.lead_Id = Leads.objects.get(id=l.id)
                            db_obj.lead_status ='Not Attended'
                            db_obj.save()
                            trns_val = trns_val + 1

                            if l.lead_source:
                            
                                try:
                                    pf_obj = PlatForms.objects.get(platform_Name__iexact=l.lead_source,company_Id__id=dash_details.emp_comp_id.id) 
                                    pf_obj.platform_TotalCount = pf_obj.platform_TotalCount +1
                                    pf_obj.save()

                                except PlatForms.DoesNotExist:
                                    pf_obj = PlatForms()
                                    pf_obj.company_Id=dash_details.emp_comp_id
                                    pf_obj.platform_Name = l.lead_source
                                    pf_obj.platform_TotalCount = pf_obj.platform_TotalCount +1
                                    pf_obj.save()
                                    
                                except Exception as e:
                                    print('An error occurred:', e)


                                try:
                                    pfd = PlatFormsData.objects.get(data_add_date=date.today(),platform_name__iexact=l.lead_source,Pfd_company_Id__id=dash_details.emp_comp_id.id)
                                    pfd.platform_dataCount = pfd.platform_dataCount +1
                                    pfd.save()

                                except PlatFormsData.DoesNotExist:
                                    pfd = PlatFormsData()
                                    pfd.Pfd_company_Id=dash_details.emp_comp_id
                                    pfd.platform_name = l.lead_source
                                    pfd.platform_dataCount = pfd.platform_dataCount +1
                                    pfd.save()
                                
                                except Exception as e:
                                    print('An error occurred:', e)
                    except Leads.DoesNotExist:
                        continue

                success = True
                success_text = f'{trns_val} Leads Transfered Successfully.'

                

                works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
                leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=0)
                leads_obj_count = leads_obj.count()
                
                pg_num = 100
                paginator = Paginator(leads_obj, pg_num)  
                page_number = request.GET.get('page')
            
                leads = paginator.get_page(page_number)
                
                clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)
                bal_lead = count_val - trns_val

                content = {'emp_dash':emp_dash,
                            'dash_details':dash_details,
                            'notifications':notifications,
                            'success':success,
                            'success_text':success_text,
                            'works_obj':works_obj,
                            'leads':leads,
                            'clients_objs':clients_objs,
                            'bal_lead':bal_lead,
                            'leads_obj_count':leads_obj_count,
                            'pg_num':pg_num
                            }

                return render(request,'HD_TransferLead.html',content)
            
            else:
             
                return redirect('head_transfer_lead')
        else:
             
            return redirect('head_transfer_lead')

    else:
            return redirect('/')     





# Work Allocate section----------------

def head_allocateWorkView(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).order_by('-id')
        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        
        client_task = ClientTask_Register.objects.all()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works,'tl_list':tl_list,
                  
                   'client_task':client_task}

        return render(request,'HD_workAllocate.html',content)

    else:
            return redirect('/')
    

def head_workAllocate(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

       
       
        message_obj =None
        success = None
        success_text= None

        if request.POST:
             
            works = WorkRegister.objects.get(id=int(request.POST['Work_id']))
            

            seletedTl = EmployeeRegister_Details.objects.get(id=int(request.POST['selected_tl']))
            client_task = ClientTask_Register.objects.get(id=int(request.POST['clientTask']))

            tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
            client_tasks = ClientTask_Register.objects.filter(work_Id=works)
            

            category = request.POST['Taskcategory']
           

            if client_task.task_name == 'Lead Collection' and category == '0' :
                message_obj = 'Lead Collection task selected! Did you forget to select the category?'

            else:

                sdate = request.POST['fDate']
                duedate = request.POST['dueDate']
                discription = request.POST['discription_data']
                any_file = request.FILES.get('wFile')
                w_type = request.POST['work_type']
                wtarget = request.POST['ttarget']
                
                # Adding allocated Team lead id to WorkRegister Table 
                works.allocated_emp.add(seletedTl)
                works.work_allocate_status = 1
                works.save()

                work_assign_obj = WorkAssign()

                work_assign_obj.wa_compId = works.wcompId
                work_assign_obj.wa_clientId = works.clientId
                work_assign_obj.wa_work_regId = works
                work_assign_obj.wa_work_allocate = seletedTl
                work_assign_obj.wa_from_date = sdate
                work_assign_obj.wa_due_date = duedate
                work_assign_obj.wa_discription = discription
                work_assign_obj.wa_file = any_file
                work_assign_obj.wa_status = 1
                work_assign_obj.wa_target = wtarget
                work_assign_obj.wa_type = w_type
                work_assign_obj.save()
                work_assign_obj.wa_tasksId.add(client_task)
                work_assign_obj.save()

                if client_task.task_name == 'Lead Collection' and  category !=0:
            
                    lc_team_obj = LeadCateogry_TeamAllocate()
                    lc_team_obj.Tl_id = seletedTl
                    lc_team_obj.lc_id = LeadCategory_Register.objects.get(id=int(category))
                    lc_team_obj.wa_id = work_assign_obj 
                    lc_team_obj.lcta_discription = discription 
                    lc_team_obj.lcta_from_date = sdate 
                    lc_team_obj.lcta_due_date = duedate 
                    lc_team_obj.lcta_target = wtarget
                    lc_team_obj.lcta_file = any_file
                    lc_team_obj.save()
                
                if w_type == '1' :
                    
                    task_assign_obj = TaskAssign()
                    task_assign_obj.ta_workAssignId = work_assign_obj
                    task_assign_obj.ta_workerId = seletedTl
                    task_assign_obj.ta_taskId = client_task

                    task_assign_obj.ta_discription = discription
                    task_assign_obj.ta_file = any_file
                    task_assign_obj.ta_start_date = sdate
                    task_assign_obj.ta_due_date = duedate
                    task_assign_obj.ta_target = wtarget
                    task_assign_obj.ta_allocate_date = date.today()
                    task_assign_obj.save()
                    work_assign_obj.allocated_exemp.add(seletedTl)
                    work_assign_obj.save()

                    if client_task.task_name == 'Lead Collection' and  category !=0:
                    
                        lca_obj = LeadCateogry_Assign()
                        lca_obj.executive_id = seletedTl
                        lca_obj.lcta_id = lc_team_obj
                        lca_obj.ta_id = task_assign_obj
                        lca_obj.lca_discription = discription
                        lca_obj.lca_from_date = sdate
                        lca_obj.lca_due_date = duedate
                        lca_obj.lca_target = wtarget
                        lca_obj.lca_file = any_file
                        lca_obj.save()


                success = True
                if w_type == '1' :
                    success_text= client_task.task_name +'Task allocated to ' + seletedTl.emp_name +' successful.' 
                else:
                    success_text= client_task.task_name + 'Group task allocated to ' + seletedTl.emp_name +' successful.' 


            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'works':works,'tl_list':tl_list,
                        'client_task':client_tasks,
                        'message_obj':message_obj,'success':success,
                        'success_text':success_text}

            return render(request,'workallocate_page.html',content)
               

        else:
                return redirect('/')
        

def head_teamLead_allocatedTask(request,task_workId,task_empId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.get(id=task_workId)
        works_assign = WorkAssign.objects.filter(wa_work_regId=works,wa_work_allocate_id=task_empId)

        lead_category_allocate = LeadCateogry_TeamAllocate.objects.filter(wa_id__in=works_assign)

        lc_category_obj = LeadCategory_Register.objects.filter(cTaskId__work_Id_id=works.id)
        Tl_obj = EmployeeRegister_Details.objects.get(id=task_empId)
    
        
    
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works_assign':works_assign,
                   'Tl_obj':Tl_obj,
                   'works':works,
                   'lead_category_allocate':lead_category_allocate,
                   'lc_category_obj':lc_category_obj
                   }

        return render(request,'HD_team_Team_Task.html',content)

    else:
            return redirect('/')
    

def head_lead_category_allocateTl(request):

    if request.POST:
        lc_categorys = request.POST.getlist('lc')
         
        for l in lc_categorys:
            lead_team_allocate = LeadCateogry_TeamAllocate()
            lead_team_allocate.lc_id = LeadCategory_Register.objects.get(id=int(l))
            lead_team_allocate.Tl_id = EmployeeRegister_Details.objects.get(id=request.POST['tlId'])
            lead_team_allocate.wa_id = WorkAssign.objects.get(id=request.POST['waId'])
            lead_team_allocate.lcta_discription = request.POST['discription_data']
            lead_team_allocate.lcta_from_date = request.POST['fDate']
            lead_team_allocate.lcta_due_date = request.POST['dueDate']
            lead_team_allocate.lcta_target = request.POST['target']
         
            lead_team_allocate.lcta_status = 1
            lead_team_allocate.save()

        wrID = request.POST['Work_id']
        tlID = request.POST['tlId']

        return redirect('head_teamLead_allocatedTask',wrID,tlID)
        
        
def head_leadCategory_allocate_remove(request,lcID):
    lead_team_allocate = LeadCateogry_TeamAllocate.objects.get(id=lcID)

    wrID = lead_team_allocate.wa_id.wa_work_regId.id
    tlID = lead_team_allocate.Tl_id.id
       
    lead_team_allocate.delete()
    return redirect('head_teamLead_allocatedTask',wrID,tlID)


def head_leadCategory_allocate_edit(request,lcID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        lead_team_allocateedit = LeadCateogry_TeamAllocate.objects.get(id=lcID)
           
        if request.POST:
        
            lead_team_allocate = LeadCateogry_TeamAllocate.objects.get(id=lcID)
           
            lead_team_allocate.lcta_discription = request.POST['discription_data']
            lead_team_allocate.lcta_from_date = request.POST['fDate']
            lead_team_allocate.lcta_due_date = request.POST['dueDate']
            lead_team_allocate.lcta_target = request.POST['target']
         
            lead_team_allocate.lcta_status = 1
            lead_team_allocate.save()

            wrID = lead_team_allocate.wa_id.wa_work_regId.id
            tlID = lead_team_allocate.Tl_id.id

            return redirect('head_teamLead_allocatedTask',wrID,tlID)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   
                   'lead_team_allocateedit':lead_team_allocateedit,
                  
                   }

        return render(request,'HD_leadCategoryEdit.html',content)

    else:
            return redirect('/')


def head_assigned_work_Remove(request,work_assingId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        works_assign = WorkAssign.objects.get(id=work_assingId)
        print('Work Assign Removed')
        works_assign.delete()

        return redirect('head_allocateWorkView')

    else:
            return redirect('/')
    

def head_assigned_task_Remove(request,assingId,assignTaskId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        try:
            works_assign = WorkAssign.objects.get(id=assingId)
            task_obj = ClientTask_Register.objects.get(id=assignTaskId)
        
            works_assign.wa_tasksId.remove(task_obj)
            works_assign.save()

        except works_assign.DoesNotExist:
            print('No data Found')
            return redirect('head_allocateWorkView')
        
       
        except ClientTask_Register.DoesNotExist:
            print('No task Found')
            return redirect('head_allocateWorkView')
        
        
        return redirect('head_allocateWorkView')

    else:
            return redirect('/')
    

def head_removeAllocatedTl(request, workId, empId):

    try:
        work_obj = WorkRegister.objects.get(id=workId)
        employee_obj = EmployeeRegister_Details.objects.get(id=empId)
        
        work_obj.allocated_emp.remove(employee_obj)

        work_obj.save()
        

        work_assign_obj = WorkAssign.objects.filter(wa_work_regId=work_obj,wa_work_allocate=employee_obj)
        work_assign_obj.delete()

        
        wa_obj = WorkAssign.objects.filter(wa_work_regId=work_obj)

        if wa_obj.exists():

            work_obj.work_allocate_status = 1
            print('update 1')
        else:
    
            work_obj.work_allocate_status = 0
            print('update 2')
        
        work_obj.save()
         
        
        

       
    except work_obj.DoesNotExist:
        print('No data Found')
        return redirect('head_allocateWorkView')
        
       
    except EmployeeRegister_Details.DoesNotExist:
        print('No employee Found')
        return redirect('head_allocateWorkView')
    
    return redirect('head_allocateWorkView')
     

def get_client_tasks(request):
    client_id = request.GET.get('client_id')
    
    # Fetch data from the ClientTaskRegister model based on the selected client_id
    client_tasks = ClientTask_Register.objects.filter(client_Id=client_id).values('id', 'task_name')
    
    return JsonResponse(list(client_tasks), safe=False)


def head_TlsingleTask(request,work_assigngId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

       
        works_assign = WorkAssign.objects.get(id=work_assigngId)
        lc_category_obj = LeadCateogry_TeamAllocate.objects.filter(wa_id=works_assign)

        success = False
        success_text = None


        if request.POST:

            task_obj = TaskAssign()
            task_obj.ta_workAssignId = works_assign
            task_obj.ta_workerId = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_ID']))
            task_obj.ta_taskId = ClientTask_Register.objects.get(id=int(request.POST['task_name']))
            task_obj.ta_discription = request.POST['discription_data']
            task_obj.ta_start_date = request.POST['fDate']
            task_obj.ta_due_date = request.POST['dueDate']
            task_obj.ta_allocate_date =  date.today()
            task_obj.ta_target =  request.POST['task_target']
            task_obj.ta_file =  request.FILES.get('wFile')
            task_obj.save()
            emp_obj=EmployeeRegister_Details.objects.get(id=int(request.POST['emp_ID']))
            works_assign.allocated_exemp.add(emp_obj)
            if request.POST.getlist('lc'):

                list_category = request.POST.getlist('lc')

                for l in list_category:
                    lca = LeadCateogry_Assign()
                    lca.executive_id = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_ID']))
                    lca.ta_id = task_obj
                    lca.lcta_id =  LeadCateogry_TeamAllocate.objects.get(id=l)
                    lca.lca_discription = request.POST['discription_data']
                    lca.lca_due_date =   request.POST['dueDate']
                    lca.lca_from_date =  request.POST['fDate']
                    lca.lca_target = request.POST['task_target']
                    lca.lca_file = request.FILES.get('wFile')
                    lca.lca_status = 1
                    lca.save()
               

            success = True
            success_text = 'Task allocated success.'
        
    
        content = {'emp_dash':emp_dash,'success_text':success_text,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'lc_category_obj':lc_category_obj,
                   'works_assign':works_assign,'success':success
                   }

        return render(request,'HD_Team_Taskallocate.html',content)

    else:
            return redirect('/')


     

def head_pendingworkView(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        assigned_works = WorkAssign.objects.filter(wa_compId=dash_details.emp_comp_id).order_by('-wa_clientId','-work_assign_date')

        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        client_task = ClientTask_Register.objects.all()


        # pagination--------------------- 
        page = request.GET.get('page', 1)
        paginator = Paginator(assigned_works,5)  # Show 5 items per page
        try:
            items = paginator.page(page)
        
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)




        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'assigned_works':items,'tl_list':tl_list,
                   'client_task':client_task}

        return render(request,'HD_workpending.html',content)

    else:
            return redirect('/')
    
     
    
def head_WorkProgress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).order_by('-id')
       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works}


        return render(request,'HD_workProgress.html',content)

    else:
            return redirect('/')    


def head_clientWorkDetails(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        client = ClientRegister.objects.get(id=pk)

        works = WorkRegister.objects.get(clientId=client)

        client_task_obj = ClientTask_Register.objects.filter(work_Id=works)

        # Over all task progress calculation

        for cl_task in client_task_obj:
            task_assign_obj = TaskAssign.objects.filter(ta_workAssignId__wa_work_regId_id=works.id,ta_taskId=cl_task)
            # To calculate average progress of task
            task_assign_count = TaskAssign.objects.filter(ta_workAssignId__wa_work_regId_id=works.id,ta_taskId=cl_task).count()

            if task_assign_count:
                task_progress_calc = 0

                for task_progress in task_assign_obj:
                
                    task_progress_calc = int(task_progress_calc + task_progress.ta_progress)

                cl_task.task_total_progress = int(task_progress_calc / task_assign_count)
                cl_task.save()


        # Over all work progress calculation

        progress_calc = 0 
    
        client_task_count = ClientTask_Register.objects.filter(work_Id=works).count()
      
        for progress in client_task_obj:
            
            progress_calc = progress_calc + progress.task_total_progress
             
        works.work_progress = int(progress_calc / client_task_count)
        works.save()

        tasks = ClientTask_Register.objects.filter(client_Id=client)
       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'client':client,'works':works,'tasks':tasks}


        return render(request,'HD_client_WorkMonitor.html',content)

    else:
            return redirect('/')    


def head_clientTaskDetails(request,client_workId,client_TaskId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        client_task_obj = ClientTask_Register.objects.get(id=client_TaskId,work_Id_id=client_workId)
        work_aasign_obj = WorkAssign.objects.filter(wa_work_regId=client_workId,wa_tasksId=client_task_obj)
        task_assign_obj = TaskAssign.objects.filter(ta_workAssignId__in=work_aasign_obj,ta_taskId=client_TaskId)

        task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj).order_by('tad_collect_date')

        if request.POST:
             
            if request.POST['task_emp'] == '0' and request.POST['task_sdate'] and request.POST['task_todate']:

                d1 = request.POST['task_sdate']
                d2 = request.POST['task_todate']
                 
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj,
                    tad_collect_date__gte=d1,tad_collect_date__lte=d2).order_by('tad_collect_date')
                
            elif request.POST['task_emp'] != '0' and request.POST['task_sdate'] and request.POST['task_todate']:
                 
                d1 = request.POST['task_sdate']
                d2 = request.POST['task_todate']
                emp = EmployeeRegister_Details.objects.get(id=int(request.POST['task_emp']))
                 
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj,
                    tad_collect_date__gte=d1,tad_collect_date__lte=d2,tad_taskAssignId__ta_workerId=emp).order_by('tad_collect_date')
                
            elif request.POST['task_emp'] != '0':
                 
                emp = EmployeeRegister_Details.objects.get(id=int(request.POST['task_emp']))
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj,tad_taskAssignId__ta_workerId=emp).order_by('tad_collect_date')
            
            else:
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj).order_by('tad_collect_date')
                 
    
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'client_task_obj':client_task_obj,
                   'task_assign_obj':task_assign_obj,
                   'task_details_obj':task_details_obj
                   }


        return render(request,'HD_client_WorktaskDetails.html',content)

    else:
            return redirect('/')    


def head_tasksForWork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        try:
            task_add_obj = Work_Task.objects.get(task_name='Lead Collection',comp_taskid=dash_details.emp_comp_id)
            pass

        except Work_Task.DoesNotExist:
            task_obj = Work_Task()
            task_obj.task_name = 'Lead Collection'
            task_obj.task_discription = 'Efficient lead collection is the cornerstone of successful business growth.'
            task_obj.comp_taskid = dash_details.emp_comp_id
            task_obj.save()
             

        data_box = {}
        if request.POST:
             
            taskName = request.POST['task_name']
            taskDiscription = request.POST['task_discription']

            task_obj = Work_Task()
            task_obj.task_name = taskName
            task_obj.task_discription = taskDiscription
            task_obj.comp_taskid = dash_details.emp_comp_id
            task_obj.save()
            success = True
            success_text= 'Task add successful.' 
                
            data_box = {'success':success,'success_text':success_text}
            
            
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Tasks':Tasks}
        
        content = {**data_box, **content}

        return render(request,'HD_workTasks.html',content)

    else:
            return redirect('/')
    
     
def company_taskEdit(request,task_edit):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        task_edit_obj = Work_Task.objects.get(id=task_edit)

        data_box = {}
        
        if request.POST:
           task_title = request.POST['task_name'] 
           task_dis = request.POST['task_discription']

           task_edit_obj.task_name = task_title
           task_edit_obj.task_discription = task_dis

           task_edit_obj.save()
           success = True
           success_text= 'Task Edit successful.' 
                
           data_box = {'success':success,'success_text':success_text}
            


        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Tasks':task_edit_obj}
        
        content = {**data_box, **content}

        return render(request,'HD_workTasksEdit.html',content)
    else:
            return redirect('/')


def company_taskDelete(request,task_delete):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        data_box = {}
        

        task_obj = Work_Task.objects.get(id=task_delete)
        task_obj.delete()
        error = True
        error_text= 'Task Delete successful.' 
        data_box = {'error':error,'error_text':error_text}
            
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Tasks':Tasks}
        
        content = {**data_box, **content}

        return render(request,'HD_workTasks.html',content)
    else:
            return redirect('/')



def head_WeeklyProgress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)



        try:
           work_progress_obj = WorkProgress.objects.filter(wp_type='weekly',wp_workerId__in=employees).order_by('-id')
           
        except WorkProgress.DoesNotExist:
             work_progress_obj = None

        
        if request.POST:
            
            date1 = request.POST['d1']
            date2 = request.POST['d2']
            empId = int(request.POST['selected_emp'])

             
            if date1 and date2 and empId == 0:
                try:
                    work_progress_obj = WorkProgress.objects.filter(wp_type='weekly',wp_workerId__in=employees,wp_from_date__gte=date1,wp_to_date__lte=date2).order_by('-id')
                    
                except WorkProgress.DoesNotExist:
                   return redirect('head_WeeklyProgress')
            
            elif date1 and date2 and empId != 0:
                try:
                    emp = EmployeeRegister_Details.objects.get(id=empId)
                    work_progress_obj = WorkProgress.objects.filter(wp_type='weekly',wp_from_date__gte=date1,wp_to_date__lte=date2,wp_workerId=emp)
                    
                except WorkProgress.DoesNotExist:
                   return redirect('head_WeeklyProgress') 
                
            elif  empId != 0:
                try:
                    emp = EmployeeRegister_Details.objects.get(id=empId)
                    work_progress_obj = WorkProgress.objects.filter(wp_type='weekly',wp_workerId=emp)
                    
                except WorkProgress.DoesNotExist:
                   return redirect('head_WeeklyProgress') 
            else:
                try:
                    work_progress_obj = WorkProgress.objects.filter(wp_type='weekly',wp_workerId__in=employees).order_by('-id')
                    
                except WorkProgress.DoesNotExist:
                        work_progress_obj = None
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'work_progress_obj':work_progress_obj,
                   'works':works}


        return render(request,'HD_weeklyProgress.html',content)

    else:
            return redirect('/')    


def head_progreess_verify_unverify(request,pk):

    work_progress_obj = WorkProgress.objects.get(id=pk)
    
    if work_progress_obj.wp_status == 0:
        work_progress_obj.wp_status = 1
        work_progress_obj.save()

    elif work_progress_obj.wp_status == 1: 
        work_progress_obj.wp_status = 0  
        work_progress_obj.save()

    if work_progress_obj.wp_type == 'weekly' :
        return redirect('head_WeeklyProgress')
    elif work_progress_obj.wp_type == 'monthly':
        return redirect('head_MonthlyProgress')
     

def head_progress_change(request):
    
    if request.POST:
        wp_Id = request.POST['wpId']
        work_progress_obj = WorkProgress.objects.get(id=wp_Id)
        work_progress_obj.wp_progress = request.POST['wprogress']
        work_progress_obj.save()

        if work_progress_obj.wp_type == 'weekly' :
            return redirect('head_WeeklyProgress')
        elif work_progress_obj.wp_type == 'monthly':
            return redirect('head_MonthlyProgress')
     

def head_MonthlyProgress(request): 
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)

        try:
            work_progress_obj = WorkProgress.objects.filter(wp_type='monthly',wp_workerId__in=employees).order_by('-id')
            
        except WorkProgress.DoesNotExist:
            work_progress_obj = None

        
        if request.POST:
            
            date1 = request.POST['d1']
            date2 = request.POST['d2']
            empId = int(request.POST['selected_emp'])

             
            if date1 and date2 and empId == 0:
                try:
                    work_progress_obj = WorkProgress.objects.filter(wp_type='monthly',wp_workerId__in=employees,wp_from_date__gte=date1,wp_to_date__lte=date2).order_by('-id')
                    
                except WorkProgress.DoesNotExist:
                   return redirect('head_MonthlyProgress')
            
            elif date1 and date2 and empId != 0:
                try:
                    emp = EmployeeRegister_Details.objects.get(id=empId)
                    work_progress_obj = WorkProgress.objects.filter(wp_type='monthly',wp_from_date__gte=date1,wp_to_date__lte=date2,wp_workerId=emp)
                    
                except WorkProgress.DoesNotExist:
                   return redirect('head_MonthlyProgress') 
                
            elif  empId != 0:
                try:
                    emp = EmployeeRegister_Details.objects.get(id=empId)
                    work_progress_obj = WorkProgress.objects.filter(wp_type='monthly',wp_workerId=emp)
                    
                except WorkProgress.DoesNotExist:
                   return redirect('head_MonthlyProgress') 
            else:
                try:
                    work_progress_obj = WorkProgress.objects.filter(wp_type='monthly',wp_workerId__in=employees).order_by('-id')
                    
                except WorkProgress.DoesNotExist:
                        work_progress_obj = None
       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'work_progress_obj':work_progress_obj,
                   'works':works}


        return render(request,'HD_monthlyProgress.html',content)

    else:
            return redirect('/')     



#Completed Work View---

def head_workCompleted(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=1).order_by('-id')
        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        client_task = ClientTask_Register.objects.all()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works,'tl_list':tl_list,
                   'client_task':client_task}

        return render(request,'HD_workCompleted.html',content)
     

# Employee Section ---------------------------------


def Head_employees_section(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'HD_employeeSection.html',content)

    else:
            return redirect('/')    


def head_viewEmployees(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        log_obj = LogRegister_Details.objects.filter(active_status=1)
        employees = EmployeeRegister_Details.objects.filter(logreg_id__in=log_obj,emp_comp_id=dash_details.emp_comp_id)

        designation_objs = DesignationRegister_details.objects.all()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'employees':employees,'designation_objs':designation_objs}

        return render(request,'HD_employeeView.html',content)

    else:
            return redirect('/')    


def head_employeeAllocate(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

          # Team Leads featch----
        Team_leads_desig_obj = DesignationRegister_details.objects.get(dashboard_id=2,desig_brd_id=dash_details.emp_comp_id) 
        Team_leads = EmployeeRegister_Details.objects.filter(emp_designation_id=Team_leads_desig_obj,logreg_id__active_status=1)
        TeamLead_emp_ids = [leads.id for leads in Team_leads]

        data_box ={}

        if request.POST:
            allocateTo =  request.POST['alocated_to']
            employee_list = request.POST.getlist('selected_emp')
            dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

            count_allocate = 0

            for emp_id in employee_list:
                allocate_obj = Allocation_Details()
                allocate_obj.allocatEmp_id = EmployeeRegister_Details.objects.get(id=int(emp_id))
                allocate_obj.allocat_to = EmployeeRegister_Details.objects.get(id=int(allocateTo))
                allocate_obj.allocate_status = 1
                allocate_obj.alloaction_date = date.today()
                allocate_obj.save()
                count_allocate =count_allocate +  1
                success = True
                success_text= str(count_allocate) + " " +'Allocation successful.' 
                
                data_box = {'success':success,'success_text':success_text}


             
        # Allocated Employees -------------------
        allocated_emp = Allocation_Details.objects.filter(allocate_status=1)
        allocated_emp_ids = [allocation.allocatEmp_id.id for allocation in allocated_emp]

        # Pending to allocate ------------
        allocate_employees = EmployeeRegister_Details.objects.filter(
            emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1,emp_designation_id__dashboard_id=3).exclude(
            id__in=allocated_emp_ids).exclude(
            id=dash_details.id).exclude(
            id__in=TeamLead_emp_ids)
        
        allocation_counts = Allocation_Details.objects.values('allocat_to__id', 'allocat_to__emp_name').annotate(count=Count('allocatEmp_id'))
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Team_leads':Team_leads,
                   'employees':allocate_employees,
                   'allocation_counts':allocation_counts}
        
        content = {**data_box, **content}

        return render(request,'HD_employeeAllocate.html',content)

    else:
            return redirect('/')    


def head_employeeAllocated_list(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)

        Team_leads_desig_obj = DesignationRegister_details.objects.get(dashboard_id=2) 
        Team_leads = EmployeeRegister_Details.objects.filter(emp_designation_id=Team_leads_desig_obj)
        TeamLead_emp_ids = [leads.id for leads in Team_leads]
        
        allocated_employees = Allocation_Details.objects.filter(allocat_to__in=TeamLead_emp_ids,
                                                                allocatEmp_id__emp_designation_id__dashboard_id=3).order_by('allocat_to')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'allocated_employees':allocated_employees,
                   'Team_leads':Team_leads,
                   'employees':employees}

        return render(request,'HD_employeeAllocatedList.html',content)

    else:
            return redirect('/')    


def head_reallocate_teamLead(request):

    if request.POST:
       
        selected_ids = request.POST.getlist('emp_check')
        tl_id = request.POST['alocated_to']
        emp = EmployeeRegister_Details.objects.get(id=tl_id)
        

        for empid in selected_ids:
            try:
                Ad_obj = Allocation_Details.objects.get(allocatEmp_id__id=int(empid))
                Ad_obj.allocat_to = EmployeeRegister_Details.objects.get(id=tl_id)
                Ad_obj.save()
            except Allocation_Details.DoesNotExist:
                print(f"No Allocation_Details found for empid {empid}")
            except EmployeeRegister_Details.DoesNotExist:
                print(f"No EmployeeRegister_Details found for tl_id {tl_id}")

    return redirect('head_employeeAllocated_list')

#Leave View-------
def head_employee_leaves(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        employees_leaves = EmployeeLeave.objects.filter(start_date__lte=today,end_date__gte=today,emp_id__in=employee_ids)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate'] :

                employees_leaves = EmployeeLeave.objects.filter(start_date__gte=request.POST['fDate'],end_date__lte=request.POST['toDate'],emp_id__in=employee_ids)
            
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                employees_leaves = EmployeeLeave.objects.filter(start_date__gte=request.POST['fDate'],end_date__lte=request.POST['toDate'],emp_id=emp_obj)
                 
            
            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                employees_leaves = EmployeeLeave.objects.filter(emp_id=emp_obj)

            else:

                employees_leaves = EmployeeLeave.objects.filter(start_date__lte=today,end_date__gte=today,emp_id__in=employee_ids)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_leaves':employees_leaves}

        return render(request,'HD_employeeLeave.html',content)

    else:
            return redirect('/')     


# Schedules View -------------

def head_employee_schedules(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        schedules = EmployeeSchedule.objects.filter(emp_id__in=employee_ids,schedule_date=today)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate']:
                 
                schedules = EmployeeSchedule.objects.filter(schedule_date__gte=request.POST['fDate'],schedule_date__lte=request.POST['toDate'],emp_id__in=employee_ids)
                 
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                schedules = EmployeeSchedule.objects.filter(schedule_date__gte=request.POST['fDate'],schedule_date__lte=request.POST['toDate'],emp_id=emp_obj)

            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj)

            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employee_ids,schedule_date=today)
        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'schedules':schedules}

        return render(request,'HD_employeeSchedules.html',content)

    else:
            return redirect('/')     
     
# All Employees Actin Taken ----------------

def head_employee_actionTaken(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        actions_taken = ActionTaken.objects.filter(act_emp_id__in=employee_ids)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate']:
                 
                actions_taken = ActionTaken.objects.filter(action_date__gte=request.POST['fDate'],action_date__lte=request.POST['toDate'],act_emp_id__in=employee_ids)
                 
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                actions_taken = ActionTaken.objects.filter(action_date__gte=request.POST['fDate'],action_date__lte=request.POST['toDate'],act_emp_id=emp_obj)

            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                actions_taken = ActionTaken.objects.filter(act_emp_id=emp_obj)

            else:
                actions_taken = ActionTaken.objects.filter(act_emp_id__in=employee_ids)
             

        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'actions_taken':actions_taken}

        return render(request,'HD_employeeActionTaken.html',content)

    else:
            return redirect('/')     
     

# All Employees Feedback -------------------

def head_employee_feedback(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

      

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        feedback_obj = Feedback.objects.filter(Q(feedback_emp_id__in=employee_ids) | Q(from_id__in=employee_ids))

        if request.POST:

            if request.POST['feed_type'] == '0' : # All Feedback
                 
                if request.POST['emp_name'] != '0':

                    emp = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                    feedback_obj = Feedback.objects.filter(Q(feedback_emp_id=emp) | Q(from_id=emp.id))
                    
                else:
                    feedback_obj = Feedback.objects.filter(Q(feedback_emp_id__in=employee_ids) | Q(from_id__in=employee_ids))
                     
                 
            elif request.POST['feed_type'] == '1' : # Feedback Given

                if request.POST['emp_name']:

                    emp = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                    feedback_obj = Feedback.objects.filter(from_id=emp.id)
                    
                else: 
                    feedback_obj = Feedback.objects.filter(from_id__in=employee_ids)
                 
            else :  # Feedback Recived
                if request.POST['emp_name']:

                    emp = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                    feedback_obj = Feedback.objects.filter(feedback_emp_id=emp)
                    
                else:
                    feedback_obj = Feedback.objects.filter(feedback_emp_id__in=employee_ids) 
                 


        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'feedback_obj':feedback_obj}

        return render(request,'HD_employeeFeedback.html',content)

    else:
            return redirect('/')     
     
# All Employees Work ---------------------

def head_employeesWork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        work_pending_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=0)
        work_complete_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=1)
        emp = 0

        if request.POST:
             
            if request.POST['selected_emp'] != '0' :
                emp_id = int(request.POST['selected_emp'])
                
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                work_pending_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=0,allocated_emp=emp_obj)
                work_complete_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=1,allocated_emp=emp_obj)
                emp = emp_obj.id

            else:
                work_pending_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=0)
                work_complete_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=1)
        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'emp':emp,
                   'work_pending_obj':work_pending_obj,
                   'work_complete_obj':work_complete_obj}

        return render(request,'HD_employeeWork.html',content)

    else:
        return redirect('/')   
    

def head_employe_workView(request,wid,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if pk == 0:
            task_assi = TaskAssign.objects.filter(ta_workAssignId__wa_work_regId=wid)
        else:
            task_assi = TaskAssign.objects.filter(ta_workAssignId__wa_work_regId=wid,ta_workerId=pk)
        
        task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assi)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'task_assi':task_assi,
                   'task_details_obj':task_details_obj
                   }

        return render(request,'HD_employeeWorkcheck.html',content)

    else:
        return redirect('/')  

     

# All Resigned Employees -----------------

def head_resignedEmployees(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_active_status=2)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'employees':employees}

        return render(request,'HD_resignedEmployeeView.html',content)

    else:
            return redirect('/')    
     


     
# =================================End Employeee Section ===============================

#Schedule -------------------------------------------

def head_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
          
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)

        if request.POST:
            date1 = request.POST['d1']
            date2 = request.POST['d2']
            schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date__gte=date1,schedule_date__lte=date2)
       
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'schedules':schedules,
                   }

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')
    
    
def head_scheduleRemove(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        schedule_remove = EmployeeSchedule.objects.get(id=pk)
        schedule_remove.delete()  

        error = True
        error_text = 'Schedule task removed'
        
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today)
       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'schedules':schedules,
                   'error':error,'error_text':error_text}

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')
    

def head_schedule_save(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        schedules = None


        if request.POST:

           
            schedule_obj = EmployeeSchedule()

            schedule_obj.emp_id=dash_details
            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = request.POST['schedule_date']

            schedule_obj.save()

            today = date.today()
            schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)
              

            success_text = 'Schedule save successful.'
            success = True

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success_text':success_text,
                   'success':success,
                   'schedules':schedules,
                  }

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')


def ScheduleEdit(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        schedules = None
       

        if request.POST:


            schedule_obj = EmployeeSchedule.objects.get(id=int(request.POST['scheduleId']))

            schedule_obj.emp_id=dash_details
            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = date.today()
            schedule_obj.save()

            today = date.today()
            schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)
               
            success_text = 'Schedule edit successful.'
            success = True
    

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success_text':success_text,
                   'success':success,
                   'schedules':schedules,
                 }

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')
     


def update_schedule_status(request):
        schedule_id = request.POST.get('schedule_id')
        checked = request.POST.get('checked')

        # Retrieve the schedule by ID
        schedule = EmployeeSchedule.objects.get(id=schedule_id)
        if schedule.schedule_status == 0:
            schedule.schedule_status =  1
        else: 
            schedule.schedule_status =  0
        schedule.save()
        return JsonResponse({'success': True})


def head_schedulesearchBy_date(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        if request.POST:
            
            if request.POST['f_date'] and request.POST['t_date']:

                fdate = request.POST['f_date']
                tdate = request.POST['t_date']
            
                schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date__gte=fdate,schedule_date__lte=tdate)
            
            else:
                schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)

            schedule_days = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today).values('schedule_date').distinct()

            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'schedules':schedules,
                    'schedule_days':schedule_days}

            return render(request,'HD_dayTaskschedule.html',content)
        else:
             
             return redirect('head_schedule')

    else:
            return redirect('/')
     


def head_employees_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
      
        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=2),emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))

        
        today = date.today()

        schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,schedule_date__lte=today).order_by('start_time')
        

        if request.POST: 

            if request.POST['employeeId']!='0':  

                employee_id= int(request.POST['employeeId'])

                try:
                    schedules = EmployeeSchedule.objects.filter(emp_id__id=employee_id,schedule_date__gte=today,
                    schedule_date__lte=today).order_by('start_time')
                except EmployeeSchedule.DoesNotExist:
                    schedules = None

                try:
                    employee_name = EmployeeRegister_Details.objects.get(id=employee_id)
                except EmployeeRegister_Details.DoesNotExist:
                    print('No Data Found')
            
            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,schedule_date__lte=today).order_by('start_time')

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'employees':employees,'schedules':schedules}

        return render(request,'HD_employees_dayTaskschedule.html',content)
        

    else:
            return redirect('/')
    
     
def head_employee_scheduleAdd(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        
        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=2),emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))


        today = date.today()

        if request.POST:   

            employee_id= int(request.POST['add_employeeId'])
                 
            schedule_obj = EmployeeSchedule()

            schedule_obj.emp_id=EmployeeRegister_Details.objects.get(id=employee_id)
            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = request.POST['schedule_date']

            schedule_obj.save()

            emp_obj=EmployeeRegister_Details.objects.get(id=int(request.POST['add_employeeId']))

            schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
            schedule_date__lte=today).order_by('start_time')
            
            success_text = 'Schedule saved for ' + emp_obj.emp_name + ' successfully.'
            success = True 

            # Notification add 

            Notification_obj = Notification()
            Notification_obj.emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['add_employeeId']))
            Notification_obj.notific_head = 'Schedule Update'
            Notification_obj.notific_content = 'There is change in your schedule , Please check the schedule section '
            Notification_obj.save()

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'success':success,
                   'today':today,'success_text':success_text,
                   'employees':employees,'schedules':schedules,
                   'employee_name':emp_obj}

            return render(request,'HD_employees_dayTaskschedule.html',content)
      
        else:
            return redirect('head_employees_schedule')

    else:
        return redirect('/')

    
def head_employeeScheduleEdit(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))
       
        
        today = date.today()

        if request.POST:   

           
                 
            schedule_obj = EmployeeSchedule.objects.get(id=pk)

            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = request.POST['schedule_date']

            schedule_obj.save()


            schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,schedule_date__lte=today).order_by('start_time')
            
            success_text = 'Schedule saved for ' + schedule_obj.emp_id.emp_name + ' successfully.'
            success = True      

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'success':success,
                   'today':today,'success_text':success_text,
                   'employees':employees,'schedules':schedules,
                   }

            return render(request,'HD_employees_dayTaskschedule.html',content)
      
        
        else:
            return redirect('head_employees_schedule')


    else:
            return redirect('/')


def head_employee_scheduleRemove(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))
        schedule_remove = EmployeeSchedule.objects.get(id=pk)
        empName = schedule_remove.emp_id.emp_name
        schedule_remove.delete()  

        error = True
        error_text = empName + " " +' Schedule task removed'
        
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
            schedule_date__lte=today).order_by('start_time')
       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'schedules':schedules,
                   'error':error,'error_text':error_text}

        return render(request,'HD_employees_dayTaskschedule.html',content)

    else:
            return redirect('/')
    
    
def head_scheduleFilter(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

          # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))
      

        schedules = None 
        emp_obj=None
        today = date.today()

        if request.POST:
             
            empId = request.POST['emp_name']
            from_date = request.POST['fDate']
            to_date = request.POST['toDate']
       

            if empId != '0' and from_date and to_date :

                emp_obj = EmployeeRegister_Details.objects.get(id=empId)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj,schedule_date__gte=from_date,
                schedule_date__lte=to_date).order_by('emp_id')
            
            elif empId == '0' and from_date and to_date :

                schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=from_date,
                schedule_date__lte=to_date).order_by('emp_id')

            elif empId != '0' :

                emp_obj = EmployeeRegister_Details.objects.get(id=empId)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj,schedule_date__gte=today,
                schedule_date__lte=today).order_by('emp_id')

            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
                schedule_date__lte=today).order_by('emp_id')
        
        else:
            
            schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
            schedule_date__lte=today).order_by('emp_id')
                 

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'schedules':schedules,'emp_obj':emp_obj}

        return render(request,'HD_scheduleFilter.html',content)

    else:
            return redirect('/')
     

# Feedback -------------------------

def head_feedback(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)

        feedback_data = Feedback.objects.filter(feedback_emp_id__in=employees).exclude(
            Q(feedback_emp_id=dash_details) | Q(feedback_emp_id=None)).order_by('-id')


        # Saveing Feedback 
        if request.POST:

            feedback_obj = Feedback()
            feedback_obj.feedback_emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['to_id']))
            feedback_obj.from_id = dash_details.id
            feedback_obj.from_name = dash_details.emp_name
            feedback_obj.feedback_content = request.POST['feedback_content']
            feedback_obj.feedback_date = date.today()
            feedback_obj.save()

            success=True
            success_text = 'Feedback add successfully.'

            feedback_data =Feedback.objects.filter(feedback_emp_id__in=employees).exclude(
            Q(feedback_emp_id=dash_details) | Q(feedback_emp_id=None)).order_by('-id')

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,

                   'employees':employees,
                   'feedback_data':feedback_data,
                   'success':success,
                   'success_text':success_text}
        
        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,

                   'employees':employees,
                   'feedback_data':feedback_data}

        return render(request,'HD_feedback.html',content)

    else:
            return redirect('/')


def feedback_Typechange(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)

        selected_value = request.GET.get('value')
    
        if selected_value == '1':
            feedback_data =Feedback.objects.filter(from_id=dash_details.id)
        else:
            feedback_data =Feedback.objects.filter(feedback_emp_id=dash_details).order_by('-id')
        
        data_list = []
        for feedback in feedback_data:
            data = {
                'feedback_date': feedback.feedback_date,
               
                'from_name': feedback.from_name,
                
                'to_name': feedback.feedback_emp_id.emp_name,
                'feedback_content': feedback.feedback_content
            }
            data_list.append(data)
        
        return JsonResponse(data_list, safe=False)
     

# Complaints ---------------------

def head_complaints(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)
        complaints_data = Complaints.objects.filter(complaint_emp_id__in=employees).order_by('status')

        # Save action taken to the selected complaint
        if request.POST:
            complaints_obj = Complaints.objects.get(id=int(request.POST['complaintId']))
            complaints_obj.action = request.POST['action_content']
            complaints_obj.action_date = date.today()
            complaints_obj.status = 1
            complaints_obj.save()

            success=True
            success_text = 'Response add successfully.'
            complaints_data = Complaints.objects.filter(complaint_emp_id__in=employees).order_by('status')

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data,
                   'success':success,
                   'success_text':success_text}

        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data}

        return render(request,'HD_complaints.html',content)

    else:
            return redirect('/')
     

# Action Taken -------------------

def head_actionTaken(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        action_taken_data = ActionTaken.objects.filter(act_emp_id__in=employees,act_from_id=dash_details.id)

        # Save data
        if request.POST:
             
             action_taken_obj = ActionTaken()
             action_taken_obj.act_emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['action_employeeId']))
             action_taken_obj.act_from_id = dash_details.id
             action_taken_obj.act_from_name = dash_details.emp_name
             action_taken_obj.act_head = request.POST['reason_content_head']
             action_taken_obj.act_reason = request.POST['reason_content']
             action_taken_obj.act_content = request.POST['what_action_content']
             action_taken_obj.action_date = request.POST['action_taken_date']
             action_taken_obj.status = 1
             action_taken_obj.save()

             success=True
             success_text = 'Action taken add successfully.'
             
             # Notification Add 
             Notification_obj = Notification()
             Notification_obj.emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['action_employeeId']))
             Notification_obj.notific_head = 'Action Taken'
             Notification_obj.notific_content = 'An action is taken for you , Please check the action taken section '
             Notification_obj.save()

             action_taken_data = ActionTaken.objects.filter(act_emp_id__in=employees)

             content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data,
                   'success':success,
                   'success_text':success_text}

        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data}

        return render(request,'HD_actionTaken.html',content)

    else:
            return redirect('/')


def head_action_takenEdit(request,pk):  
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        action_taken_data =  ActionTaken.objects.get(id=pk)

        # Edit and Save data
        if request.POST:
             
             action_taken_obj = ActionTaken.objects.get(id=pk)
             action_taken_obj.act_emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['action_employeeId']))
             action_taken_obj.act_from_id = dash_details.id
             action_taken_obj.act_from_name = dash_details.emp_name
             action_taken_obj.act_head = request.POST['reason_content_head']
             action_taken_obj.act_reason = request.POST['reason_content']
             action_taken_obj.act_content = request.POST['what_action_content']
             action_taken_obj.action_date = request.POST['action_taken_date']
             action_taken_obj.status = 1
             action_taken_obj.save()

             success=True
             success_text = 'Action taken edit successfully.'
             action_taken_data = ActionTaken.objects.filter(act_emp_id__in=employees)

             content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data,
                   'success':success,
                   'success_text':success_text}
             
             return render(request,'HD_actionTaken.html',content)
        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data}
             

        return render(request,'HD_actionTakenedit.html',content)

    else:
            return redirect('/')  


# Leave ------------------------------

def count_weekdays(start_date, end_date):
    current_date = start_date
    weekdays_count = 0

    # Iterate through each date within the range
    while current_date <= end_date:
        # Check if the current date is a weekday (Monday to Saturday)
        if current_date.weekday() < 6:
            weekdays_count += 1
        
        # Move to the next day
        current_date += timedelta(days=1)

    return weekdays_count


def head_leave(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

       
        
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        #Head Leave --------
        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')

    
       
        if request.POST:
             
            leave_obj = EmployeeLeave()
            leave_obj.start_date = request.POST['fromDate']
            leave_obj.end_date = request.POST['toDate']
            leave_obj.leave_type = request.POST['type_select']
            leave_obj.leave_reason = request.POST['reason_content']
            leave_obj.leave_request_file = request.FILES.get('leave_requestFile')
            leave_obj.emp_id = dash_details
            leave_obj.leave_apply_date = date.today()

            # day calculation
                
            start_date_str = request.POST['fromDate']
            end_date_str = request.POST['toDate'] 

            # Convert the date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Calculate the difference in days
            weekdays_count = (count_weekdays(start_date, end_date))
                
            leave_obj.no_of_days = weekdays_count
            leave_obj.save()
                
            success=True
            success_text = 'Leave applied successfully, waiting for approvel.'

            leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
            

            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'success':success,
                    'success_text':success_text,'leave_data':leave_data}

        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'leave_data':leave_data}

        return render(request,'HD_leave.html',content)

    else:
            return redirect('/')


def head_leave_search(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

       
        
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        #Head Leave --------
        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')

       
        if request.POST:
             
            if request.POST['d1'] and request.POST['d2']:

                date1 = request.POST['d1'] 
                date2 = request.POST['d2']
                
                leave_data = EmployeeLeave.objects.filter(emp_id=dash_details,start_date__gte=date1,end_date__lte=date2)

                content = {'emp_dash':emp_dash,
                            'dash_details':dash_details,
                            'notifications':notifications,
                            'leave_data':leave_data
                            }    
             
            
        return render(request,'HD_leave.html',content)

    else:
            return redirect('/')
     

def head_leave_request(request):
     
      
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

       
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        #Leave request --------
        leave_request = EmployeeLeave.objects.filter(leave_status=0)

       
        #
        if request.POST:
            leave_stataus_obj = request.POST['leve_status_change'] 
             
            if leave_stataus_obj == '3':
                leave_request = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
            else:
                leave_request = EmployeeLeave.objects.filter(emp_id=dash_details,leave_status=leave_stataus_obj)
              
      
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'leave_request':leave_request}

        
        return render(request,'HD_leave_request.html',content)

    else:
            return redirect('/')
   


def head_leaveApprove_Reject(request,request_id,request_status):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        

        leave_obj = EmployeeLeave.objects.get(id=int(request_id)) 

        if request_status == 1 :
           
            leave_obj.leave_status = 1 
            leave_obj.leave_statuChange_date = date.today()
            leave_obj.save()

            # Adding Notification --------

            notification_obj = Notification()

            notification_obj.emp_id = dash_details
            notification_obj.notific_head = 'Leave Approved'
            notification_obj.notific_content = "I'm pleased to inform you that your request for " + str(leave_obj.leave_type) + "leave from " + str(leave_obj.start_date) + " to " + str(leave_obj.end_date) + " has been approved."
            notification_obj.save()
                
        elif request_status == 2:
           
            leave_obj.leave_status = 2
            leave_obj.leave_statuChange_date = date.today()
            leave_obj.save()

            # Adding Notification --------

            notification_obj = Notification()

            notification_obj.emp_id = dash_details
            notification_obj.notific_head = 'Leave Rejectd'
            notification_obj.notific_content = "I regret to inform you that your request for " + leave_obj.leave_type + " from " + str(leave_obj.start_date) + " to " + str(leave_obj.end_date) + " has been reviewed and unfortunately, we are unable to approve it at this time."

            notification_obj.save()


        leave_request = EmployeeLeave.objects.filter(leave_status=0)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

            
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'leave_request':leave_request}

        return render(request,'HD_leave_request.html',content)
       

    else:
            return redirect('/')



def head_leaveSearch(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company).exclude(
            Q(id=dash_details.id) | Q(id=None)).order_by('-id')
        

        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
        empleave_data = EmployeeLeave.objects.filter(emp_id__in=employees).order_by('-id')
        leave_request = EmployeeLeave.objects.filter(leave_status=0)
        leave_request_json = serializers.serialize('json', leave_request)
        

        if request.method == 'POST':
            employeeid = request.POST.get('searchValue')
            fdate = request.POST.get('f_Date')
            edate = request.POST.get('e_Date')

            if fdate and edate :

                if  dash_details.id == int(employeeid):
                    try:
                        leave_data = EmployeeLeave.objects.filter(emp_id__id=int(employeeid),start_date__gte=fdate,end_date__lte=edate).order_by('-id')
                    except EmployeeLeave.DoesNotExist:
                        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
                    
                else:
                    try:
                        empleave_data = EmployeeLeave.objects.filter(emp_id__id=int(employeeid),start_date__gte=fdate,end_date__lte=edate).order_by('-id')
                    except EmployeeLeave.DoesNotExist:
                        empleave_data = EmployeeLeave.objects.filter(emp_id__in=employees).order_by('-id')
            else: 
                 
                 return redirect('head_leave')

            my_leave = render(request, 'HD_leaveAjaxresponse.html', {'leave_data': leave_data,'dash_details':dash_details}).content.decode('utf-8')
            employe_leave = render(request, 'HD_employeeLeave_ajaxresponse.html', {'emp_data': empleave_data,'employees':employees}).content.decode('utf-8')

            response_data = {'html_content': employe_leave,'my_leave':my_leave,'leave_request':leave_request_json}
            return JsonResponse(response_data)

        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)
       

    else:
            return redirect('/')
    

# Notification -----------------------


def head_allnotification(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        notifications_data = Notification.objects.filter(Q(notific_status=0) | Q(notific_status=1),emp_id=dash_details,).order_by('-notific_date')
        
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'notifications_data':notifications_data}

        return render(request,'HD_allnotification.html',content)

    else:
            return redirect('/')


def head_notificationUpdate(request):
    
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.notific_status = 1
            notification.save()
            return JsonResponse({'status': 'success', 'message': 'Notification status updated'})
            

        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@method_decorator(csrf_exempt, name='dispatch')
def head_delete_notifications(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')

        try:
            # Delete notifications with the selected IDs
            Notification.objects.filter(id__in=selected_ids).update(notific_status=2)
            return JsonResponse({'status': 'success', 'message': 'Notifications deleted successfully'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




def head_lead_verify_unverify_all(request,all_wkid,all_lcid):
        
        leads_ids = request.POST.getlist('lead_check')

        
        for lid in leads_ids:
            
            try:
                lead_obj = Leads.objects.get(id=lid,waste_data=0)

                if lead_obj.lead_status == 0:
                    lead_obj.lead_status = 1
                else:
                    lead_obj.lead_status = 0  
                
                lead_obj.save()

            except Leads.DoesNotExist:
                print('Markerd as waste lead')

        return redirect('head_lead_collected_data',all_wkid,all_lcid)


#====================================================================================================================================


#   testing section ------------------------------


def allocate_page(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.get(id=pk)
        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        client_task = ClientTask_Register.objects.filter(work_Id=works)
        lead_category_obj = LeadCategory_Register.objects.filter(cTaskId__in=client_task)
    
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works,'tl_list':tl_list,
                   'client_task':client_task,'lead_category_obj':lead_category_obj}

        return render(request,'workallocate_page.html',content)

    else:
            return redirect('/')
    


def fetch_task_categories(request):
    try:
        # Retrieve client ID from query parameters
        selected_id = request.GET.get('selectedId', None)
    

        if selected_id is not None:
            # Fetch lead categories based on the selected client ID
            lead_categories = LeadCategory_Register.objects.filter(cTaskId__id=selected_id)
           
            # Convert lead categories to a list of dictionaries
            lead_categories_list = [{'id': category.id, 'name': category.lead_collection_for} for category in lead_categories]

    
            success = True
            message = "Operation successful"



            # Return a JSON response with lead categories
            return JsonResponse({'success': success, 'message': message,'lead_categories': lead_categories_list})
        else:
            # Handle the case where client_id is not provided
            raise ValueError("Client ID is not provided in the request.")

    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})


def leadActivity_data(request,lead_id):

    try:
        wl_lead = Waste_Leads.objects.get(id=lead_id) 
        fd_objs = FollowupDetails.objects.filter(lead_Id=wl_lead.leadId).order_by('-id')
        fl_history = FollowupHistory.objects.filter(hs_lead_Id=wl_lead.leadId).order_by('-id')
        fields_obj = lead_Details.objects.filter(leadId=wl_lead.leadId)
    
    except Waste_Leads.DoesNotExist:

        return redirect('datamanager_wasteLead')

    context = {
        'wl_lead': wl_lead,
        'fd_objs':fd_objs,  
        'fl_history':fl_history,
        'fields_obj':fields_obj,
    }
    return render(request, 'modal_content.html', context)




# Reprort Section --------------------------------12/04/24

def head_Reports(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        leads_objs = Leads.objects.filter(lead_work_regId__wcompId=dash_details.emp_comp_id).order_by('-lead_add_date')

        status_val = None
        lead_count = None
        today_val= None
        emp = None
        d1 = None
        d2 = None
        client = None
        category = None

        
        # Total Leads 
        tol_count = leads_objs.count()
        trsf_count = leads_objs.filter(lead_transfer_status=1).count()
        trsf_pending_count = leads_objs.filter(lead_transfer_status=0,waste_data=0,repeated_status=0).count()
        wsate_count = leads_objs.filter(waste_data=1).count()
        pg_num = 100

        if request.POST:
            emp_id = request.POST['emplyoee']
            d1 = request.POST['sdate']
            d2 =  request.POST['edate']
            client_val = request.POST['client_val']
            category_val = request.POST['category_val']
            pg_num = request.POST['pgnum']

            if client_val:
                client = ClientRegister.objects.get(id=client_val)
                leads_objs = leads_objs.filter(lead_category_id__cTaskId__client_Id=client)
            if category_val:
                category = LeadCategory_Register.objects.get(id=category_val)
                leads_objs = leads_objs.filter(lead_category_id=category)

            if emp_id:
                emp = EmployeeRegister_Details.objects.get(id=emp_id)
                leads_objs = leads_objs.filter(lead_collect_Emp_id__id=emp_id)

            if d1:
                leads_objs = leads_objs.filter(lead_add_date__gte=d1)

            if d2:
                leads_objs = leads_objs.filter(lead_add_date__lte=d2)
              
            status_val = request.POST['status_val']
              
            if status_val == 'Verified' :
                leads_objs = leads_objs.filter(lead_status=1)
                lead_count = leads_objs.count()
            if status_val == 'Unverified' :
                leads_objs = leads_objs.filter(lead_status=0)
                lead_count = leads_objs.count()
            if status_val == 'Transfered' :
                leads_objs = leads_objs.filter(lead_transfer_status=1)
                lead_count = leads_objs.count()
            if status_val == 'Pending' :
                leads_objs = leads_objs.filter(lead_transfer_status=0)
                lead_count = leads_objs.count()
            if status_val == 'Incompleted' :
                leads_objs = Leads.objects.filter(lead_incomplete_status=1)
                lead_count = leads_objs.count()
            if status_val == 'Repeated' :
                leads_objs = leads_objs.filter(repeated_status=1)
                lead_count = leads_objs.count()
            if status_val == 'Waste' :
                leads_objs = leads_objs.filter(waste_data=1)
                lead_count = leads_objs.count()
            

        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | 
                                                                 Q(emp_designation_id__dashboard_id=2) | 
                                                                 Q(emp_designation_id__dashboard_id=3),
                                                                 emp_comp_id=dash_details.emp_comp_id,
                                                                emp_active_status=1)
        if d1:
            pass
        else:
            d1=date.today()
            today_val = 1

        if d2:
            pass
        else:
            today_val = 1
            d2=date.today()
            

       
        
        toady_trsf_count = leads_objs.filter(lead_transfer_status=1,lead_transfer_date__gte=d1,lead_transfer_date__lte=d2).count()

        toady_tol_count = leads_objs.filter(lead_add_date__gte=d1,
                                                    lead_add_date__lte=d2).count()
            
        toady_trsf_pending_count = leads_objs.filter(lead_add_date__gte=d1,
                                                        lead_add_date__lte=d2,
                                                        lead_transfer_status=0,waste_data=0,repeated_status=0).count()
            
        toady_wsate_count = leads_objs.filter(waste_data=1,
                                                lead_add_date__gte=d1,
                                                lead_add_date__lte=d2).count()    
        
        paginator = Paginator(leads_objs, pg_num) 
        page_number = request.GET.get('page')
       
        leads = paginator.get_page(page_number)
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'tol_count':tol_count,
                   'trsf_count':trsf_count,
                   'trsf_pending_count':trsf_pending_count,
                   'wsate_count':wsate_count,
                   'clients_objs':clients_objs,
                   'executive_data':executive_data,
                   'leads':leads,'status_val':status_val,'lead_count':lead_count,'emp':emp,
                   'd1':d1,'d2':d2,'client':client,'category':category,
                   'toady_tol_count':toady_tol_count,
                   'toady_trsf_count':toady_trsf_count,
                   'toady_trsf_pending_count':toady_trsf_pending_count,
                   'toady_wsate_count':toady_wsate_count,
                   'today_val':today_val,'pg_num':pg_num
                   }

        return render(request,'reports.html',content)

    else:
            return redirect('/')



def leadCategories(request):

    try:
        client_id = request.GET.get('client_id', None)
       
        if client_id is not None:
            lead_categories = LeadCategory_Register.objects.filter(cTaskId__client_Id__id=client_id)
            lead_categories_list = [{'id': category.id, 'name': category.lead_collection_for} for category in lead_categories]
            success = True
            return JsonResponse({'success': success,'lead_categories': lead_categories_list})
        else:
           
            raise ValueError("Client ID is not provided in the request.")

    except Exception as e:
      
        return JsonResponse({'success': False, 'message': str(e)})



def HD_featchLeadwasteReason(request):

    try:
        lead_id = request.GET.get('lead_id', None)
        if lead_id is not None:
            lead = Leads.objects.get(id=lead_id)
            lead_waste_reason = lead.waste_data_reason
            success = True
            return JsonResponse({'success': success, 'lead_wsate_reason': lead_waste_reason})  # Corrected key name
        else:
            raise ValueError("Lead ID is not provided in the request.")
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



def leadFollwup_data(request,lead_id):

    try:
        lead = Leads.objects.get(id=lead_id) 
        wl_lead = Waste_Leads.objects.filter(leadId=lead).last()
        fd_objs = FollowupDetails.objects.filter(lead_Id=lead).order_by('-id')
        fl_history = FollowupHistory.objects.filter(hs_lead_Id=lead).order_by('-id')
        fields_obj = lead_Details.objects.filter(leadId=lead)
    
    except Waste_Leads.DoesNotExist:

        return redirect('datamanager_wasteLead')

    context = {
        'lead': lead,
        'wl_lead':wl_lead,
        'fd_objs':fd_objs,  
        'fl_history':fl_history,
        'fields_obj':fields_obj,
    }
    return render(request, 'leadFollowup_content.html', context)



#29/04/24 -- Repeated Lead


def head_repeated_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')



        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)


        # Get leads with duplicate email addresses
        duplicate_email_leads = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

        # Get leads with duplicate phone numbers
        duplicate_phone_leads = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

        for item in duplicate_phone_leads:
            leads_with_phone = Leads.objects.filter(lead_contact__exact=item['lead_contact'])
            if len(leads_with_phone) > 1:
                for lead in leads_with_phone:
                    l = Leads.objects.get(id=lead.id)
                    l.repeated_status=1
                    #l.save()
                

        LCR = LeadCategory_Register.objects.filter(cTaskId__cTcompId=dash_details.emp_comp_id)
        executive_data  = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)


        repeated_leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,repeated_status=1).order_by('-lead_contact')

        if request.POST:
            category = request.POST['select_category']
            emp = request.POST['select_emp']

            if category:
                repeated_leads_obj = repeated_leads_obj.filter(lead_category_id__id=category)

            if emp:
                repeated_leads_obj = repeated_leads_obj.filter(lead_collect_Emp_id=emp)
       
        repeated_leads_obj_count = repeated_leads_obj.count()

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'repeated_leads_obj':repeated_leads_obj,
                    'repeated_leads_obj_count':repeated_leads_obj_count,
                    'executive_data':executive_data,
                    'LCR':LCR
                    
        }

        return render(request,'HD_Repeated.html',content)

    else:
            return redirect('/')    


def lead_repeat_delete(request):
    checked_values = request.POST.get('checked_values')

    id_list = checked_values.split(',') 
    count_val = 0

    for ids in id_list:

        try:
            leads_obj = Leads.objects.get(id=ids)
            leads_obj.delete() 
            count_val = count_val + 1
        except Leads.DoesNotExist:
            continue
    return JsonResponse({'message': f'Data deleted {count_val} successfully .'})




def head_lead_tracker(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)
        executive_data = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        telecaller_data = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)
        leads_obj = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_Id__lead_transfer_status=1).order_by('-Genarated_date')
        fs_obj=FollowupStatus.objects.filter(company_Id__id=dash_details.emp_comp_id.id)

        Cl_ID = None
        Ct_ID = None
        d1 = None
        d2 = None
        d3 = None
        d4 = None
        emp = None
        telecaller_emp = None
        client_name = None
        category_name = None
        select_emp = None
        select_telecaller_emp = None



        if request.POST:
            Cl_ID = request.POST['client_change']
            Ct_ID = request.POST['category_name']
            emp = request.POST['select_emp']
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            d3 = request.POST['waste_sdate']
            d4 = request.POST['waste_edate']
            telecaller_emp = request.POST['select_telecaller_emp']
            select_lead_ststus = request.POST['select_lead_ststus']
            fs_status = request.POST['fs_status']
            pg_num = request.POST['pgnum']

        else :
            Cl_ID = request.GET.get('Cl_ID')
            Ct_ID = request.GET.get('Ct_ID')
            emp = request.GET.get('employee')
            d1 = request.GET.get('start_date')
            d2 = request.GET.get('end_date')
            d3 = request.GET.get('wsdate')
            d4 = request.GET.get('wedate')
            select_lead_ststus = request.GET.get('slstatus')
            fs_status = request.GET.get('fs_lsta')
            telecaller_emp = request.GET.get('telecaller')
            pg_num = request.GET.get('pg_num')

        if pg_num is None:
            pg_num = 100
            


        if Cl_ID and Ct_ID:
            leads_obj = leads_obj.filter(lead_Id__lead_work_regId__clientId__id=Cl_ID,lead_Id__lead_category_id__id=Ct_ID)
            client_name = ClientRegister.objects.get(id=Cl_ID)
            category_name = LeadCategory_Register.objects.get(id=Ct_ID)

        if d1:
          
            leads_obj = leads_obj.filter(Genarated_date__gte=d1)
        if d2:
            leads_obj = leads_obj.filter(Genarated_date__lte=d2)

        
        if select_lead_ststus:
            leads_obj = leads_obj.filter(lead_status=select_lead_ststus)

         
        if fs_status:
            leads_obj = leads_obj.filter(current_status=fs_status)

            
        if emp:
            leads_obj = leads_obj.filter(lead_Id__lead_collect_Emp_id__id=emp)
            select_emp = EmployeeRegister_Details.objects.get(id=emp)

        if telecaller_emp:
            Leads_assignto_obj = Leads_assignto_tc.objects.filter(TC_Id__id=telecaller_emp).values('dataBank_ID')
            leads_obj = leads_obj.filter(id__in=Leads_assignto_obj)
            select_telecaller_emp = EmployeeRegister_Details.objects.get(id=telecaller_emp)

        if d3:
            Leads_assignto_obj = Leads_assignto_tc.objects.filter(Assign_Date__gte=d3).values('dataBank_ID')
            leads_obj = leads_obj.filter(id__in=Leads_assignto_obj)

        if d4:
            Leads_assignto_obj = Leads_assignto_tc.objects.filter(Assign_Date__lte=d4).values('dataBank_ID')
            leads_obj = leads_obj.filter(id__in=Leads_assignto_obj)


        leads_obj_count = leads_obj.count()

        paginator = Paginator(leads_obj, pg_num) 
        
        page_number = request.GET.get('page')
       
        leads = paginator.get_page(page_number)
        
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'leads_obj_count':leads_obj_count,
                    'clients_objs':clients_objs,
                    'executive_data':executive_data,
                    'telecaller_data':telecaller_data,
                    'leads':leads,
                    'Cl_ID':Cl_ID,'Ct_ID':Ct_ID,'employee':emp,'start_date':d1,'end_date':d2,'pg_num':pg_num,
                    'telecaller':telecaller_emp,'fs_obj':fs_obj,'fs_status':fs_status,
                    'd3':d3,'d4':d4,'telecaller_emp':telecaller_emp,'select_telecaller_emp':select_telecaller_emp,
                    'select_emp':select_emp,'client_name':client_name,'category_name':category_name,'select_lead_ststus':select_lead_ststus
                    
                    }


        return render(request,'HD_TrackerLead.html',content)

    else:
            return redirect('/')  
    




def leadActivity_Tracker(request,lead_id):

    try:
        db = DataBank.objects.get(id=lead_id) 
        wl_lead = Waste_Leads.objects.filter(leadId=db.lead_Id).last()
        fd_objs = FollowupDetails.objects.filter(lead_Id=db.lead_Id).order_by('-id')
        fl_history = FollowupHistory.objects.filter(hs_lead_Id=db.lead_Id).order_by('-id')
        fields_obj = lead_Details.objects.filter(leadId=db.lead_Id)

    
    except Waste_Leads.DoesNotExist:

        return redirect('head_lead_tracker')

    context = {
        'db': db,
        'fd_objs':fd_objs,  
        'fl_history':fl_history,
        'fields_obj':fields_obj,
        'wl_lead':wl_lead
    }
    return render(request, 'leadTrack_content.html', context)




def leadrepeated_data(request,rlead_id):

    try:
        lead_obj = Leads.objects.get(id=rlead_id) 
        repeated_leads = Leads.objects.filter(Q(lead_email=lead_obj.lead_email) | Q(lead_contact=lead_obj.lead_contact)) 
    
    except lead_obj.DoesNotExist:

        return redirect('head_lead_collected_data')

    context = {
        'repeated_leads':repeated_leads
    }
    return render(request, 'repeated_leads.html', context)
            



def waste_leadPDF_preview(request,pdf_id):

    try:
        wl_lead = Waste_Leads.objects.get(id=pdf_id) 
        fd_objs = FollowupDetails.objects.filter(lead_Id=wl_lead.leadId).order_by('-id')
        fl_history = FollowupHistory.objects.filter(hs_lead_Id=wl_lead.leadId).order_by('-id')
        fields_obj = lead_Details.objects.filter(leadId=wl_lead.leadId)
    
    except Waste_Leads.DoesNotExist:

        return redirect('datamanager_wasteLead')

    context = {
        'wl_lead': wl_lead,
        'fd_objs':fd_objs,  
        'fl_history':fl_history,
        'fields_obj':fields_obj,
    }
    return render(request, 'waste_leadPDF.html', context)




def hd_employeeDesignationEdit(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
    

        emp_id = request.POST['empid']
        desig_id =DesignationRegister_details.objects.get(id=request.POST['desigantion_name'])

        employees = EmployeeRegister_Details.objects.get(id=emp_id)
        employees.emp_department_id = desig_id.dept_id
        employees.emp_designation_id = desig_id
        employees.save()
        messages.success(request, f'{employees.emp_name} Designation Changed to {desig_id.desig_name}')
     

        return redirect('head_viewEmployees')
        
       

    else:
            return redirect('/') 





#Executive Task Allocate-----


def head_allocate_task_to_executive(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        tls = tl_list.values('id')

        work_assign = WorkAssign.objects.filter(wa_work_allocate__in=tls,wa_type=0).order_by('-id')
        lc_team = LeadCateogry_TeamAllocate.objects.filter(wa_id__in=work_assign)
        team = Allocation_Details.objects.filter(allocat_to__in=tls,).exclude(allocatEmp_id__emp_active_status=2)
        team = team.exclude(allocatEmp_id__emp_designation_id__dashboard_id=2)
        team_ids = [t.allocatEmp_id_id for t in team]

        task_assign = TaskAssign.objects.filter(ta_workerId_id__in=team_ids).order_by('-id') 
        lc_assign = LeadCateogry_Assign.objects.filter(executive_id_id__in=team_ids).order_by('-id') 
        

        success = True
        success_text= 'Task add successful.'            
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'work_assign':work_assign,
                   'task_assign':task_assign,
                   'team':team,
                   'lc_team':lc_team,
                   'lc_assign':lc_assign,
                #    'success':success,
                #    'success_text':success_text,
        }
        return render(request,'HD_ExecutiveTaskAllocate.html',content)

    else:
            return redirect('/')



def head_TaskkAssign_Executive(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        
        if request.POST:
             
            workAs = WorkAssign.objects.get(id=int(request.POST['Workassign_id']))
            seletedTask = ClientTask_Register.objects.get(id=int(request.POST['selected_task']))
            selected_emp_list = request.POST.getlist('emp')


            sdate = request.POST['fDate']
            duedate = request.POST['dueDate']
            target = request.POST.get('target', None)
            discription = request.POST['discription_data']
            any_file = request.FILES.get('wFile')
            if target is None or target == '':
                target = 0

            for emp_id in selected_emp_list:
                employee = EmployeeRegister_Details.objects.get(id=int(emp_id))
                workAs.allocated_exemp.add(employee)
            workAs.save()

            for emp_id in selected_emp_list:
                taskAs = TaskAssign()
                taskAs.ta_workAssignId = workAs
                taskAs.ta_workerId = EmployeeRegister_Details.objects.get(id=int(emp_id))
                taskAs.ta_taskId = seletedTask
                taskAs.ta_discription = discription
                taskAs.ta_file = any_file
                taskAs.ta_allocate_date = date.today()
                taskAs.ta_start_date = sdate
                taskAs.ta_due_date = duedate
                taskAs.ta_target = target
                taskAs.ta_status = 1
                taskAs.save()

                if seletedTask.task_name == 'Lead Collection':
                     categoryId = request.POST['selected_category']
                    
                     LeadCategoryTA = LeadCateogry_TeamAllocate.objects.get(lc_id_id=categoryId,wa_id=workAs,Tl_id=workAs.wa_work_allocate)
                     lcAssign = LeadCateogry_Assign()
                     lcAssign.executive_id=EmployeeRegister_Details.objects.get(id=int(emp_id))
                     lcAssign.lcta_id=LeadCategoryTA
                     lcAssign.ta_id=taskAs
                     lcAssign.lca_discription=discription
                     lcAssign.lca_from_date=sdate
                     lcAssign.lca_due_date=duedate
                     lcAssign.lca_target=target
                     lcAssign.lca_file=any_file
                     lcAssign.lca_status=1
                     lcAssign.save()

                notification_obj = Notification()
                notification_obj.emp_id = employee  
                notification_obj.notific_head = "Work Assigned" 
                notification_obj.notific_content = "A new task has been assigned to you. " 
                notification_obj.save()

            # messages.success(request, 'Work assigned successfully...')
           
        return redirect('head_allocate_task_to_executive')

    else:
        return redirect('/')



def head_logout(request):
    request.session.pop('emp_id', None)
    return redirect('login_page')