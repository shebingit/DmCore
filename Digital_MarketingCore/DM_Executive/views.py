import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render,redirect
from Registration_Login.models import *
from .models import *
from DM_Head.models import *
from django.utils import timezone
from datetime import date
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.db.models import Count
import random
import io, os
from openpyxl.workbook import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


# Create your views here.

# logout

def executive_logout(request):
    request.session.pop('emp_id', None)
    return redirect('login_page')    


def executive_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # Get the current date and time in the timezone defined in your Django settings
        current_datetime = timezone.now()

        # Extract the month from the current date
        current_month = current_datetime.month
        #additional details
        work_count=TaskAssign.objects.filter(ta_workerId= dash_details).count()
        monthwork_count = TaskAssign.objects.filter(ta_workerId=dash_details, ta_start_date__month=current_month).count()
        leave_count=EmployeeLeave.objects.filter(emp_id=dash_details).count()
        monthleave_count =EmployeeLeave.objects.filter(emp_id=dash_details,start_date__month=current_month).count()
        complaint_count=Complaints.objects.filter(complaint_emp_id= dash_details).count()
        monthcomplaint_count = Complaints.objects.filter(complaint_emp_id=dash_details, complaint_date__month=current_month).count()        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'work_count':work_count,
            'monthwork_count': monthwork_count,
            'leave_count':leave_count,
            'monthleave_count': monthleave_count,
            'complaint_count':complaint_count,
            'monthcomplaint_count': monthcomplaint_count,
        }

        return render(request,'Executive_dashboard.html',content)

    else:
            return redirect('/')


# Profile Page -------------------------
def executive_profile(request):  
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        #  notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
        }

        return render(request,'Executive_profile.html',content)

    else:
            return redirect('/')


def Profile_detailsUpdate(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        #  notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')


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
        
        
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'success_text':success_text,
                'success':success
            }

        else:
            error_text = 'Profile Details Updated.'
            error = True
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'error_text':error_text,
                'error':error
            }

        return render(request,'Executive_profile.html',content)

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

def executive_password(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
        }

        return render(request,'Executive_password.html',content)

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

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        if request.POST:
           
           emp_dash.log_username = request.POST['emp_uname']
           emp_dash.log_password = request.POST['emp_password']

           emp_dash.save()  
           success = True
           success_text = 'User name or password change.'
        
           content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'success':success,
                'success_text':success_text
            }
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'error':error,
                'error_text':error_text
            }

        return render(request,'Executive_password.html',content)

    else:
            return redirect('/')


# Action Taken -------------------

def executive_actionTaken(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        actions=ActionTaken.objects.filter(act_emp_id=dash_details).order_by('-action_date')
        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'actions':actions,
        }

        return render(request,'Executive_actionTaken.html',content)

    else:
            return redirect('/')
     


# Notifications section

def executive_allnotification(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):

            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        allnotification=Notification.objects.filter(Q(emp_id=dash_details,notific_status=0) | Q(emp_id=dash_details,notific_status=1)).order_by('-notific_date','-notific_time')

        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'allnotification':allnotification,
        }

        return render(request,'Executive_allnotification.html',content)

    else:
            return redirect('/')


# Mark notification as seen...

def exmark_notification(request,pk):
    
    notification=Notification.objects.get(id=pk)
    notification.notific_status=1
    notification.save()
    return redirect('executive_allnotification')
        

# delete notification
def exdelete_notification(request,pk):

    notification=Notification.objects.get(id=pk)
    notification.notific_status=2
    notification.save()
    return redirect('executive_allnotification')


# delete multiple notifications
def delete_selected_notifications(request):

    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')
        Notification.objects.filter(id__in=selected_ids).update(notific_status=2) 
        
        return JsonResponse({'message': 'Notifications deleted successfully'})

    return JsonResponse({'error': 'Invalid request method'})


# Feedback -------------------------

def executive_feedback(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        #  notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        employee_ids = [1, 2]
        employees=EmployeeRegister_Details.objects.filter(emp_designation_id__in=employee_ids)
        id1=EmployeeRegister_Details.objects.get(logreg_id=emp_id).id
        feedback_view=Feedback.objects.filter(from_id=id1).order_by('-feedback_date')

        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'employees':employees,
            'feedback_view':feedback_view
        }

        return render(request,'Executive_feedback.html',content)

    else:
        return redirect('/')

def exadd_feedback(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        #  notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        employee_ids = [1, 2]
        employees=EmployeeRegister_Details.objects.filter(emp_designation_id__in=employee_ids)
        id1=EmployeeRegister_Details.objects.get(logreg_id=emp_id)
        id2=EmployeeRegister_Details.objects.get(logreg_id=emp_id).id
        feedback_view=Feedback.objects.filter(from_id=id2).order_by('-feedback_date')

        if request.POST:
            from_id=id1.id
            from_name=id1.emp_name
            feedback_date=date.today()
            idto=request.POST['feedbackto']
            feedback_emp_id=EmployeeRegister_Details.objects.get(id=idto)
            feedback_content=request.POST['feedback_content']
            feedback=Feedback(from_id=from_id,from_name=from_name,feedback_date=feedback_date,feedback_emp_id=feedback_emp_id,feedback_content=feedback_content)
            feedback.save()
            success_text = 'Feedback Submitted'
            success = True
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'employees':employees,
                'feedback_view':feedback_view,
                'success_text':success_text,
                'success':success,
            }
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'employees':employees,
                'feedback_view':feedback_view,
                'error':error,
                'error_text':error_text,
                
            }      

        

        

        return render(request,'Executive_feedback.html',content)

    else:
        return redirect('/')


# feedbackgiven filter 

def exfeedback_given(request):
    
    if request.session.has_key('emp_id'):
        emp_id = request.session['emp_id']
        
    else:
        return redirect('/')

    id1=EmployeeRegister_Details.objects.get(logreg_id=emp_id).id
    feedback_view =Feedback.objects.filter(from_id=id1).order_by('-feedback_date')
    feedback_list=[]

    for i in feedback_view:
        date=i.feedback_date
        by=i.from_name
        byid=i.from_id
        content=i.feedback_content
        to=i.feedback_emp_id.emp_name
        feedback_list.append({
            'feedback_date':date,
            'from_name':by,
            'from_id':byid,
            'feedback_content':content,
            'feedback_emp':to
        })

    return JsonResponse({'feedback_list': feedback_list})   


# feedbackreceived filter 

def exfeedback_received(request):
    
    if request.session.has_key('emp_id'):
        emp_id = request.session['emp_id']
        
    else:
        return redirect('/')
        
    id1=EmployeeRegister_Details.objects.get(logreg_id=emp_id).id
    feedback_view = Feedback.objects.filter(feedback_emp_id=id1).order_by('-feedback_date')
    feedback_list=[]
    for i in feedback_view:
        date=i.feedback_date
        by=i.from_name
        byid=i.from_id
        content=i.feedback_content
        to=i.feedback_emp_id.emp_name
        feedback_list.append({
            'feedback_date':date,
            'from_name':by,
            'from_id':byid,
            'feedback_content':content,
            'feedback_emp':to
        })

    return JsonResponse({'feedback_list': feedback_list})   


# Complaints ---------------------

def executive_complaints(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        view_complaints=Complaints.objects.filter(complaint_emp_id=dash_details).order_by('-complaint_date')
        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'view_complaints':view_complaints,
        }

        return render(request,'Executive_complaints.html',content)

    else:
            return redirect('/')

def addex_complaint(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
        
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        #  notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        view_complaints=Complaints.objects.filter(complaint_emp_id=dash_details).order_by('-complaint_date')

        if request.POST:
            compaint_head=request.POST['compaint_head']
            compaint_content=request.POST['compaint_content']
            complaint_date=date.today()

            complaint=Complaints(complaint_emp_id=dash_details, compaint_head= compaint_head,compaint_content=compaint_content,complaint_date=complaint_date)
            complaint.save()
            success_text = 'Complaint Registered'
            success = True
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'success_text':success_text,
                'success':success,
                'view_complaints':view_complaints,
                
            }
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'error':error,
                'error_text':error_text,
                'view_complaints':view_complaints
            }      
        

        return render(request,'Executive_complaints.html',content)

    else:
            return redirect('/')


    


# Leave ------------------------------

def executive_leave(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        myleave=EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-start_date')
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        


        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'myleave':myleave,
            
            
        }

        return render(request,'Executive_leave.html',content)

    else:
        return redirect('/')

# function to find number of days

def count_weekdays(start_date, end_date):
    current_date = start_date
    weekdays_count = 0

    # Iterate through each date within the range
    while current_date <= end_date:
        # Check if the current date is a weekday (Monday to Saturday)
        if current_date.weekday() < 6 and current_date.weekday() != 6:
            weekdays_count += 1
        
        # Move to the next day
        current_date += timedelta(days=1)

    return weekdays_count


def exapply_leave(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        myleave=EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-start_date')

        # fetch leave details
        if request.POST:
            start_date=request.POST['from']
            end_date=request.POST['to']
            leave_type=request.POST['type_select']
            leave_reason=request.POST['reason']
            leave_request_file = request.FILES['leave_request_file']
            leave_apply_date=date.today()

            leave_details=EmployeeLeave(emp_id=dash_details,start_date=start_date,end_date=end_date,leave_type=leave_type,leave_reason=leave_reason,leave_apply_date=leave_apply_date,leave_request_file=leave_request_file)
            leave_details.save()

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # Calculate the difference in days
            weekdays_count = (count_weekdays(start_date, end_date))
            leave_details.no_of_days = weekdays_count
            leave_details.save()

            success_text = 'Applied Leave'
            success = True
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'success_text':success_text,
                'success':success,
                'myleave':myleave,
            }

            # return redirect('executive_leave')
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {
                'emp_dash':emp_dash,
                'dash_details':dash_details,
                'notifications':notifications,
                'notification':notification,
                'error':error,
                'error_text':error_text,
                'myleave':myleave,
            }    


        

        return render(request,'Executive_leave.html',content)

    else:
        return redirect('/')


# leave filter function

def filter_exleave(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if request.session.has_key('emp_id'):
        emp_id = request.session['emp_id']
    id1=EmployeeRegister_Details.objects.get(logreg_id=emp_id)
    myleave = list(EmployeeLeave.objects.filter(start_date__range=[from_date, to_date],emp_id=id1,).order_by('-start_date').values())

    return JsonResponse({'myleave': myleave})       


#Schedule -------------------------------------------

def executive_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
          
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today).order_by('-schedule_date','-start_time')
        schedule_days = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today).values('schedule_date').distinct()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'notification':notification,
                   'schedules':schedules,
                   'schedule_days':schedule_days}

        return render(request,'Executive_dayTaskschedule.html',content)

    else:
            return redirect('/')


def executive_scheduleRemove(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')


        schedule_remove = EmployeeSchedule.objects.get(id=pk)
        schedule_remove.delete()  

        error = True
        error_text = 'Schedule task removed'
        
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today).order_by('-schedule_date','-start_time')
        schedule_days = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today).values('schedule_date').distinct()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'notification':notification,
                   'schedules':schedules,
                   'schedule_days':schedule_days,'error':error,'error_text':error_text}

        return render(request,'Executive_dayTaskschedule.html',content)

    else:
            return redirect('/')
    

def executive_schedule_save(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        
        
        schedules = None
        schedule_days = None

        if request.POST:

            if request.POST['scheduleId']:

                schedule_obj = EmployeeSchedule.objects.get(id=int(request.POST['scheduleId']))

                schedule_obj.emp_id=dash_details
                schedule_obj.start_time=request.POST['stime']
                schedule_obj.end_time=request.POST['etime']
                schedule_obj.schedule_head=request.POST['task_head']
                schedule_obj.todo_content=request.POST['task_content']
                schedule_obj.log_time = timezone.now()
                schedule_obj.schedule_date =request.POST['date']
                schedule_obj.save()

                today = date.today()
                schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today).order_by('-schedule_date','-start_time')
                schedule_days = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today).values('schedule_date').distinct()
                success_text = 'Schedule edit successful.'
                success = True
                

            else:

    
                schedule_obj = EmployeeSchedule()

                schedule_obj.emp_id=dash_details
                schedule_obj.start_time=request.POST['stime']
                schedule_obj.end_time=request.POST['etime']
                schedule_obj.schedule_head=request.POST['task_head']
                schedule_obj.todo_content=request.POST['task_content']
                schedule_obj.log_time = timezone.now()
                schedule_obj.schedule_date = request.POST['date']

                schedule_obj.save()

                today = date.today()
                schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today).order_by('-schedule_date','-start_time')
                schedule_days = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today).values('schedule_date').distinct()

                success_text = 'Schedule save successful.'
                success = True

        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'notification':notification,
                   'success_text':success_text,
                   'success':success,
                   'schedules':schedules,
                   'schedule_days':schedule_days}

        return render(request,'Executive_dayTaskschedule.html',content)

    else:
            return redirect('/')


def ScheduleEdit(request):

    schedule_id = request.GET.get('scheduleid')
    try:
            schedule = EmployeeSchedule.objects.get(id=schedule_id)
           
            data = {
                'scheduleid':schedule.id,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'task_head': schedule.schedule_head,
                'task_content': schedule.todo_content,
                'schedule_date':schedule.schedule_date
            }
            return JsonResponse(data)
    except EmployeeSchedule.DoesNotExist:
            return JsonResponse({'error': 'Schedule not found'}, status=404)  


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


def executive_scheduleview(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        name=dash_details.emp_name
        
        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        schedules=EmployeeSchedule.objects.filter(emp_id=dash_details).order_by('-schedule_date','-start_time')
        
        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'name':name,
            'schedules':schedules,
        }

        return render(request,'Executive_scheduleFilter.html',content)

    else:
            return redirect('/')
     

def executive_scheduleFilterday(request):
    
    if request.session.has_key('emp_id'):
        emp_id = request.session['emp_id']
    emp_dash = LogRegister_Details.objects.get(id=emp_id)
    dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    schedules=list(EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date__range=[from_date, to_date]).order_by('-schedule_date','-start_time').values())
   
    return JsonResponse({'schedules': schedules})



def filter_schedules(request):
    option = request.GET.get('option', 'All')  # Default to 'All' if 'option' is not provided
    schedules = []

    if request.session.get('emp_id'):
        emp_id = request.session['emp_id']
        try:
            emp_dash = LogRegister_Details.objects.get(id=emp_id)
            dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        except (LogRegister_Details.DoesNotExist, EmployeeRegister_Details.DoesNotExist):
            # Handle exceptions when the objects are not found
            return JsonResponse({'schedules': schedules})

        if option == 'All':
            schedules = list(EmployeeSchedule.objects.filter(emp_id=dash_details).order_by('-schedule_date', '-start_time').values())
        elif option == 'Upcoming schedules':
            tomorrow = date.today() + timedelta(days=1)
            schedules = list(EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date__gte=tomorrow).order_by('-schedule_date', '-start_time').values())
        elif option == 'Completed schedules':
            schedules = list(EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_status=1).order_by('-schedule_date', '-start_time').values())

    return JsonResponse({'schedules': schedules})

# work section

def executive_worksection(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
        }

        return render(request,'Executive_work.html',content)

    else:
            return redirect('/')


def executive_newwork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_accept_status=0).order_by('-ta_start_date')
        
        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'tasks':tasks,
        }

        return render(request,'Executive_newwork.html',content)

    else:
            return redirect('/')

def executive_newwork_accept(request,pk):
    task=TaskAssign.objects.get(id=pk)
    task.ta_accept_status=1
    task.ta_accept_date=date.today()
    task.save()
    return redirect('executive_newwork')


def executive_ongoingwork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_accept_status=1,ta_status=1).order_by('-ta_start_date')

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'tasks':tasks,
        }

        return render(request,'Executive_ongoingwork.html',content)

    else:
            return redirect('/')

def executive_ongoingwork_complete(request,pk):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_accept_status=1,ta_status=1).order_by('-ta_start_date')

        #task complete 
        task=TaskAssign.objects.get(id=pk)

        # total count of details of task
        task_det_total_count=TaskDetails.objects.filter(tad_taskAssignId=task).count()
        
        if task_det_total_count > 0:
            #count of task details with status=1
            task_det_with_status1_count=TaskDetails.objects.filter(tad_taskAssignId=task,tad_status=1).count()

            #check condition
            if task_det_total_count == task_det_with_status1_count:

                if task.ta_progress == 100:

                    task.ta_status=2
                    task.save()
                    success_text = 'Task completed successfully.'
                    success = True
                    # return redirect('executive_ongoingwork')
                
                    content = {
                        'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'notification':notification,
                        'tasks':tasks,
                        'success_text':success_text,
                        'success': success,
                    }
                else:
                    error=True
                    error_text = 'Oops! Check your task progress.'
                    content = {
                        'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'notification':notification,
                        'tasks':tasks,
                        'error':error,
                        'error_text':error_text,    
                    }  

            else:

                error=True
                error_text = 'Oops! Check all daily tasks are verified.'
                content = {
                    'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'notification':notification,
                    'tasks':tasks,
                    'error':error,
                    'error_text':error_text,    
                }  

        else:

            # Handle the case where there are no task details to process
            error = True
            error_text = 'No daily task details to process.'

            content = {
                'emp_dash': emp_dash,
                'dash_details': dash_details,
                'notifications': notifications,
                'notification': notification,
                'tasks': tasks,
                'error': error,
                'error_text': error_text,
                            
            }
        return render(request,'Executive_ongoingwork.html',content)

    else:
        return redirect('/')

def executive_ongoingwork_progress(request,pk):

    if request.POST:
        task=TaskAssign.objects.get(id=pk)
        task.ta_progress=request.POST['newProgress']
        task.save()
        return redirect('executive_ongoingwork')

def executive_ongoingwork_dailyworkadd(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)
        tdate=date.today()

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'task':task,
            'daily_works':daily_works,
            'tdate':tdate,
        }

        return render(request,'Executive_ongoingwork_dailyworkadd.html',content)

    else:
            return redirect('/')

def executive_ongoingwork_dailyworksave(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # taskassign details
        task=task=TaskAssign.objects.get(id=pk)

        if request.method == 'POST':
            # Retrieve form data from POST request
            tad_title = request.POST.get('tad_title')
            tad_discription = request.POST.get('tad_discription')
            tad_target = request.POST.get('tad_target')
            tad_collect_date = date.today()

            # Handle file inputs
            tad_files = request.FILES.getlist('tad_file')

            task_details = TaskDetails(
                tad_taskAssignId=task,
                tad_collect_date=tad_collect_date,
                tad_title=tad_title,
                tad_discription=tad_discription,
                tad_target=tad_target,           
            )

            task_details.save()

            for file in tad_files:
                # Save the file to a location on your server
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                
                # Store the file path or any relevant file information in the tad_file field
                task_details.tad_file.append({'file_name': file.name, 'file_path': filename})   

            task_details.save()
            return redirect('executive_ongoingwork')

    else:
        return redirect('/')

def executive_ongoingwork_leads_dailywork(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)
        tdate=date.today()

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'task':task,
            'daily_works':daily_works,
            'tdate':tdate,
        }

        return render(request,'Executive_ongoingwork_leads_dailywork.html',content)

    else:
            return redirect('/')

def executive_ongoingwork_leadsdailyworksave(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # taskassign details
        task=task=TaskAssign.objects.get(id=pk)

        if request.method == 'POST':
            # Retrieve form data from POST request
            tad_title = request.POST.get('tad_title')
            tad_discription = request.POST.get('tad_discription')
            tad_target = request.POST.get('tad_target')
            tad_collect_date = date.today()

            # Handle file inputs
            tad_files = request.FILES.getlist('tad_file')

            task_details = TaskDetails(
                tad_taskAssignId=task,
                tad_collect_date=tad_collect_date,
                tad_title=tad_title,
                tad_discription=tad_discription,
                tad_target=tad_target,           
            )

            task_details.save()

            for file in tad_files:
                # Save the file to a location on your server
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                
                # Store the file path or any relevant file information in the tad_file field
                task_details.tad_file.append({'file_name': file.name, 'file_path': filename})   

            task_details.save()
            return redirect('executive_ongoingwork_dailyworkadd_lead',pk)

    else:
        return redirect('/')


def executive_ongoingwork_dailyworkadd_lead(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        

        clientid=task.ta_taskId.client_Id.id
        work_id=(task.ta_workAssignId.wa_work_regId).id
        
        leadinfo = LeadField_Register.objects.filter(field_work_regId=work_id).values('field_name').distinct()

        

        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'task':task,
            'leadinfo':leadinfo,
        }

        return render(request,'Executive_ongoingwork_dailyworkadd_lead.html',content)

    else:
            return redirect('/')



def executive_leadcategory(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        clientid=task.ta_taskId.client_Id.id
        work_id=(task.ta_workAssignId.wa_work_regId).id
        

        # leadcategory assign details
        category=LeadCategory_Register.objects.filter(cTaskId__client_Id=clientid)
        lead_team_allocate = LeadCateogry_TeamAllocate.objects.filter(lc_id__in=category)
        lead_category_assign=LeadCateogry_Assign.objects.filter(executive_id=dash_details,lcta_id__in=lead_team_allocate)

        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'task':task,
            'pk':pk,
            'lead_category_assign':lead_category_assign,
        }
        
        return render(request,'Executive_leadcategory.html',content)

    else:
            return redirect('/')




def executive_lead_add_page(request,pk,id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        task=TaskAssign.objects.get(id=pk)
        work_id=(task.ta_workAssignId.wa_work_regId).id
        today=date.today()

        lead_category_assign=LeadCateogry_Assign.objects.get(executive_id=dash_details,id=id)
        category_id=lead_category_assign.lcta_id.lc_id

        works_obj = WorkRegister.objects.get(id=work_id)
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj,field_lead_category=category_id)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).order_by('-lead_add_date','-lead_add_time')
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
       


        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'works_obj':works_obj,
            'leads_obj':leads_obj,
            'lead_Details_obj':lead_Details_obj,
            'leads_obj_count':leads_obj_count,
            'lf_obj':lf_obj,
            'pk':pk,
            'task':task,
            'lead_category_assign':lead_category_assign,
        }
       
        return render(request,'Executive_ongoingwork_dailyworkadd_leaddata.html',content)

    else:
        return redirect('/')


def executive_lead_add(request,pk,id):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        task=TaskAssign.objects.get(id=pk)
        work_id=(task.ta_workAssignId.wa_work_regId).id
        works_obj = WorkRegister.objects.get(id=work_id)
        today=date.today()

        lead_category_assign=LeadCateogry_Assign.objects.get(executive_id=dash_details,id=id)
        category_id=lead_category_assign.lcta_id.lc_id

        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj,field_lead_category=category_id)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).order_by('-lead_add_date','-lead_add_time')
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)

        lead_category_assign=LeadCateogry_Assign.objects.get(executive_id=dash_details,id=id)

        if request.POST:
             

            ld_obj = Leads()
            ld_obj.lead_work_regId = works_obj
            ld_obj.lead_collect_Emp_id = dash_details
            ld_obj.lead_name = request.POST['leadName']
            ld_obj.lead_email = request.POST['leadEmail']
            ld_obj.lead_contact =request.POST['leadContact']
            ld_obj.lead_source =request.POST['leadsource']
            ld_obj.lead_taskAssignId=task
            ld_obj.lead_category_id=lead_category_assign.lcta_id.lc_id
            ld_obj.save()


            leadfield_values = request.POST.getlist('leadfield')

            for idx, field in enumerate(lf_obj):
                lead_detail = lead_Details(leadId=ld_obj, lead_field_name=field.field_name, lead_field_data=leadfield_values[idx])
                lead_detail.save()


        # leads_target_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,waste_data=0).count()

        # task.ta_target_achived=leads_target_count
        # task.save() 

        # category_id=lead_category_assign.lcta_id.lc_id
        # leads_categorytarget_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_category_id=category_id,waste_data=0).count()

        # lead_category_assign.lca_target_achived=leads_categorytarget_count
        # lead_category_assign.save() 
        
        
        
        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'works_obj':works_obj,
            'leads_obj':leads_obj,
            'lead_Details_obj':lead_Details_obj,
            'leads_obj_count':leads_obj_count,
            'lf_obj':lf_obj,
            'pk':pk,
            'task':task,
            'lead_category_assign':lead_category_assign,
        }

        return render(request,'Executive_ongoingwork_dailyworkadd_leaddata.html',content)

    else:
            return redirect('/')

# Excel File Create Section ---------------------------------------

    
def download_excelfile(request,pk,id):
    task=TaskAssign.objects.get(id=pk)
    work_id=(task.ta_workAssignId.wa_work_regId).id
    wId = WorkRegister.objects.get(id=work_id)
    lead_category_assign=LeadCateogry_Assign.objects.get(id=id)
    category_id=lead_category_assign.lcta_id.lc_id


 
    data = LeadField_Register.objects.filter(field_work_regId=wId).values('field_name')

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    additional_headers = ["Full Name", "Email Id", "Contact Number", "Lead Source"]

    headers = list(LeadField_Register.objects.filter(field_work_regId=wId,field_lead_category=category_id).values_list('field_name', flat=True))
    all_headers = additional_headers + headers
    ws.append(all_headers)

  
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{wId.clientId.client_name}.xlsx"'

    # Save the Excel workbook to the response
    wb.save(response)

    return response

def is_valid_phone_number(phone_number):
    # Check if phone_number is None or not a string
    if phone_number is None or not isinstance(str(phone_number), str):
        return False

    # Remove non-digit characters from the phone number
    cleaned_phone_number = re.sub(r'\D', '', str(phone_number))

    # Check if the cleaned phone number has exactly 10 digits
    if len(cleaned_phone_number) == 10:
        return True
    else:
        return False

def executive_lead_file_upload(request,pk,id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        task=TaskAssign.objects.get(id=pk)
        work_id=(task.ta_workAssignId.wa_work_regId).id
        works_obj = WorkRegister.objects.get(id=work_id)
        today=date.today()
        lead_category_assign=LeadCateogry_Assign.objects.get(executive_id=dash_details,id=id)

        data_list = {}

        if request.POST:


            exfile = request.FILES.get('upload_File')

            # Read the Excel file using pandas
            df = pd.read_excel(exfile)

            # Check if the DataFrame is empty
            if df.empty:
                return redirect('executive_lead_add_page', pk)
            
            else:

                # Create a list of column headers from the DataFrame
                headers = df.columns.tolist()

                # Process and save the data to the Lead model (adjust as needed)
                for _, row in df.iterrows():
                    lead_data = {header: row[header] for header in headers}

                   

                    lead = Leads()
                    lead.lead_work_regId = works_obj
                    lead.lead_collect_Emp_id = dash_details
                    lead.lead_name = lead_data['Full Name']
                    lead.lead_email = lead_data['Email Id']
                    lead.lead_contact = lead_data['Contact Number']
                    lead.lead_source = lead_data['Lead Source']
                    lead.lead_taskAssignId=task
                    lead.lead_category_id=lead_category_assign.lcta_id.lc_id
                   

                    lead.save()

                    try:
                        validate_email(lead.lead_email)
                    except ValidationError:
                        # Invalid email, mark as waste data
                        lead.waste_data=1

                    # Validate phone number
                    if not is_valid_phone_number(lead.lead_contact):
                        # Invalid phone number, mark as waste data
                        lead.waste_data=1
                        
                    lead.save()    

                    for key, value in lead_data.items():
                        if key not in ('Full Name', 'Email Id', 'Contact Number','Lead Source'):
                            lead_details = lead_Details(leadId=lead, lead_field_name=key, lead_field_data=value)
                            lead_details.leadId = lead
                            lead_details.save()


                success = True
                success_text = 'File uploaded successfully.'
                data_list = {'success':success,'success_text':success_text}


        
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).order_by('-lead_add_date','-lead_add_time')
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        # leads_target_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,waste_data=0).count()

        # task.ta_target_achived=leads_target_count
        # task.save()

        # category_id=lead_category_assign.lcta_id.lc_id
        # leads_categorytarget_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_category_id=category_id,waste_data=0).count()

        # lead_category_assign.lca_target_achived=leads_categorytarget_count
        # lead_category_assign.save()
        


        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'works_obj':works_obj,
            'leads_obj':leads_obj,
            'lead_Details_obj':lead_Details_obj,
            'leads_obj_count':leads_obj_count,
            'lf_obj':lf_obj,
            'pk':pk,
            'task':task,
            'lead_category_assign':lead_category_assign,
        }

        
        content = {**data_list, **content}

        return render(request,'Executive_ongoingwork_dailyworkadd_leaddata.html',content)

    else:
            return redirect('/')      


def remove_duplicate_leads(request,pk,id):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        work_id=(task.ta_workAssignId.wa_work_regId).id
        works_obj = WorkRegister.objects.get(id=work_id)
        today=date.today()

        lead_category_assign=LeadCateogry_Assign.objects.get(executive_id=dash_details,id=id)
        category_id=lead_category_assign.lcta_id.lc_id

        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj,field_lead_category=category_id)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).order_by('-lead_add_date','-lead_add_time')
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=today).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)

       
        # Get a list of duplicates based on name, email, and contact
        duplicate_leads = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details).values('lead_name', 'lead_email', 'lead_contact').annotate(count=Count('id')).filter(count__gt=1)

        for duplicate_lead in duplicate_leads:
            name = duplicate_lead['lead_name']
            email = duplicate_lead['lead_email']
            contact = duplicate_lead['lead_contact']

            # Get the duplicate leads with the same name, email, and contact
            duplicates = Leads.objects.filter(Q(lead_name=name) & Q(lead_email=email) & Q(lead_contact=contact))

            # Keep one lead and delete the rest
            lead_to_keep = duplicates.first()
            duplicate_lead_ids = duplicates.exclude(pk=lead_to_keep.pk).values_list('id', flat=True)

            # Delete related records in lead_Details
            lead_Details.objects.filter(leadId__in=duplicate_lead_ids).delete()

            # Delete duplicate leads
            duplicates.exclude(pk=lead_to_keep.pk).delete()


        # leads_target_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,waste_data=0).count()

        # task.ta_target_achived=leads_target_count
        # task.save()    

        # leads_categorytarget_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_category_id=category_id,waste_data=0).count()

        # lead_category_assign.lca_target_achived=leads_categorytarget_count
        # lead_category_assign.save()


        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'works_obj':works_obj,
            'leads_obj':leads_obj,
            'lead_Details_obj':lead_Details_obj,
            'leads_obj_count':leads_obj_count,
            'lf_obj':lf_obj,
            'pk':pk,
            'task':task,
            'lead_category_assign':lead_category_assign,
        }


        return render(request,'Executive_ongoingwork_dailyworkadd_leaddata.html',content)

    else:
            return redirect('/')


def executive_ongoingwork_dailywork_leads(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        work_id=(task.ta_workAssignId.wa_work_regId).id
        works_obj = WorkRegister.objects.get(id=work_id)
        today=date.today()

        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details).order_by('-lead_add_date','-lead_add_time')
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'works_obj':works_obj,
            'leads_obj':leads_obj,
            'lead_Details_obj':lead_Details_obj,
            'leads_obj_count':leads_obj_count,
            'lf_obj':lf_obj,
            'pk':pk,
        }

        return render(request,'Executive_ongoingwork_dailywork_leads.html',content)

    else:
            return redirect('/')



def executive_ongoingwork_dailyworks(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task).order_by('-tad_collect_date')

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'task':task,
            'daily_works':daily_works,
        }

        return render(request,'Executive_ongoingwork_dailyworks.html',content)

    else:
            return redirect('/')


def executive_ongoingwork_leadcomplete(request,pk):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_accept_status=1,ta_status=1).order_by('-ta_start_date')

        #task complete 
        task=TaskAssign.objects.get(id=pk)

        # total count of details of task
        task_det_total_count=TaskDetails.objects.filter(tad_taskAssignId=task).count()
        
        if task_det_total_count > 0:
            #count of task details with status=1
            task_det_with_status1_count=TaskDetails.objects.filter(tad_taskAssignId=task,tad_status=1).count()

            #check condition
            if task_det_total_count == task_det_with_status1_count:

                if task.ta_progress == 100 and (task.ta_target == task.ta_target_achived) :

                    task.ta_status=2
                    task.save()
                    success_text = 'Task completed successfully.'
                    success = True
                    # return redirect('executive_ongoingwork')
                
                    content = {
                        'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'notification':notification,
                        'tasks':tasks,
                        'success_text':success_text,
                        'success': success,
                    }
                else:
                    error=True
                    error_text = 'Oops! Check your task progress or target acheived.'
                    content = {
                        'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'notification':notification,
                        'tasks':tasks,
                        'error':error,
                        'error_text':error_text,    
                    }  

            else:

                error=True
                error_text = 'Oops! Check all daily tasks are verified.'
                content = {
                    'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'notification':notification,
                    'tasks':tasks,
                    'error':error,
                    'error_text':error_text,    
                }  

        else:

            # Handle the case where there are no task details to process
            error = True
            error_text = 'No daily task details to process.'

            content = {
                'emp_dash': emp_dash,
                'dash_details': dash_details,
                'notifications': notifications,
                'notification': notification,
                'tasks': tasks,
                'error': error,
                'error_text': error_text,
                            
            }
        return render(request,'Executive_ongoingwork.html',content)

    else:
        return redirect('/')



def download_file(request, task_id, file_index):
    task = get_object_or_404(TaskDetails, pk=task_id)

    # Get the file information from the tad_file field
    try:
        file_info = task.tad_file[file_index]
        file_path = file_info.get('file_path', '')
        file_name = file_info.get('file_name', '')
    except (IndexError, KeyError):
        return HttpResponse("File not found", status=404)

    # Construct the file path
    file_path = os.path.join('media', file_path)  # Replace 'your_file_directory' with the actual directory path where files are stored

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)   


def executive_completedwork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_status=2).order_by('-ta_start_date')

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'tasks':tasks,
        }

        return render(request,'Executive_completedwork.html',content)

    else:
            return redirect('/')


def executive_completedwork_dailyworks(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'task':task,
            'daily_works':daily_works,
        }

        return render(request,'Executive_completedwork_dailyworks.html',content)

    else:
            return redirect('/')






def executive_weekly_progress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # weekly progress

        progress= WorkProgress.objects.filter(wp_workerId=dash_details,wp_type='Weekly').order_by('-wp_from_date',)
        
        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'progress':progress,
            
        }

        return render(request,'Executive_weeklyprogress.html',content)

    else:
            return redirect('/')



def executive_monthly_progress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # monthly progress

        progress= WorkProgress.objects.filter(wp_workerId=dash_details,wp_type='Monthly').order_by('-wp_from_date')
        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'notification':notification,
            'progress':progress,
            
        }

        return render(request,'Executive_monthlyprogress.html',content)

    else:
            return redirect('/')


def executive_progress_save(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # work progress details
        if request.POST:
            wp_workerId=dash_details
            wp_type1=request.POST['type']
            wp_type2=request.POST['type']
            work_discription=request.POST['description']
            wp_progress=request.POST['progress']
            wp_from_date=request.POST['fdate']
            wp_to_date=request.POST['tdate']

            # Handle file inputs
            files = request.FILES.getlist('files')

            if  wp_type1 == 'Weekly':

                progress=WorkProgress(wp_workerId=wp_workerId,wp_type=wp_type1,work_discription=work_discription,wp_progress=wp_progress,wp_from_date=wp_from_date,wp_to_date=wp_to_date)
                progress.save()



                for file in files:
                    # Save the file to a location on your server
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
        
                    # Store the file path or any relevant file information in the tad_file field
                    progress.wp_file.append({'file_name': file.name, 'file_path': filename})   

                progress.save()
                return redirect('executive_weekly_progress')

            else:
                
                progress=WorkProgress(wp_workerId=wp_workerId,wp_type=wp_type2,work_discription=work_discription,wp_progress=wp_progress,wp_from_date=wp_from_date,wp_to_date=wp_to_date)
                progress.save()



                for file in files:
                    # Save the file to a location on your server
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
        
                    # Store the file path or any relevant file information in the tad_file field
                    progress.wp_file.append({'file_name': file.name, 'file_path': filename})   

                progress.save()
                return redirect('executive_monthly_progress')

    else:
        return redirect('/')

def download_progressfile(request, progress_id, file_index):
    progress = get_object_or_404(WorkProgress, pk=progress_id)

    # Get the file information from the wp_file field
    try:
        file_info = progress.wp_file[file_index]
        file_path = file_info.get('file_path', '')
        file_name = file_info.get('file_name', '')
    except (IndexError, KeyError):
        return HttpResponse("File not found", status=404)

    # Construct the file path
    file_path = os.path.join('media', file_path)  # Replace 'your_file_directory' with the actual directory path where files are stored

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)   