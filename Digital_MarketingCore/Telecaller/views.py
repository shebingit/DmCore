from django.shortcuts import render,redirect
from Registration_Login.models import *
from .models import *
from django.core import serializers
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime,timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from DataManager.models import FollowupStatus,FollowupDetails,FollowupHistory
from django.contrib import messages



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


def TC_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        
        
            emp_dash = LogRegister_Details.objects.get(id=emp_id,active_status=1)
            dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash,emp_active_status=1)
    
            notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
            
            #---------------------------------------------------------------------------------------

            accept_pending_leads = Leads_assignto_tc.objects.filter(TC_Id=dash_details,Status=0,Assign_Date=date.today())

            today_date = date.today()
            

            if request.POST:

                accept_pending_leads = Leads_assignto_tc.objects.filter(TC_Id=dash_details,Status=0)

                d1 = request.POST['sdate']
                d2 = request.POST['edate']

                if d1:
                    accept_pending_leads = accept_pending_leads.filter(Assign_Date__gte=d1)

                if d2:
                    accept_pending_leads = accept_pending_leads.filter(Assign_Date__lte=d2)

            accept_pending_leads_count = accept_pending_leads.count()

           
        
            content = {'emp_dash':emp_dash,
                       'dash_details':dash_details,
                       'notifications':notifications,
                       'accept_pending_leads':accept_pending_leads,
                        'accept_pending_leads_count':accept_pending_leads_count,
                        'today_date':today_date
                        
                       } 

            return render(request,'TC_dashboard.html',content)

    else:
            return redirect('/')

         
def TC_profile(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id,active_status=1)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash,emp_active_status=1)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        
        content = {'emp_dash':emp_dash,'dash_details':dash_details,'notifications':notifications} 

        return render(request,'TC_profile.html',content)

    else:
            return redirect('/')    

    
def TC_profile_detailsUpdate(request):
     
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

        return render(request,'TC_profile.html',content)

    else:
            return redirect('/')
    

# Remove Profile Image ---------------

def TC_profileImage_remove(request):
    emp_id = request.POST.get('emp_id')
    dash_details = EmployeeRegister_Details.objects.get(id=emp_id)
    dash_details.emp_profile = ''
    dash_details.save()
    return JsonResponse({'message': 'Received emp_id: ' + emp_id})
     
# End ------------------------------------------------     
    

def TC_leave(request):
    
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

        return render(request,'TC_leave.html',content)

    else:
            return redirect('/')


def TC_leave_search(request):
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
             
            
        return render(request,'TC_leave.html',content)

    else:
            return redirect('/')    


# Action Taken -------------------

def TC_actionTaken(request):

    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)
        action_taken_data = ActionTaken.objects.filter(act_from_id=dash_details.id).order_by('-id')
        tc_action_taken_data = ActionTaken.objects.filter(act_emp_id=dash_details).order_by('-id')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data,
                   'tc_action_taken_data':tc_action_taken_data}

        return render(request,'TC_actionTaken.html',content)

    else:
            return redirect('/')

# Feedback -------------------------

def TC_feedback(request):

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

        return render(request,'TC_feedback.html',content)

    else:
            return redirect('/')


def TC_feedback_Typechange(request):
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


def TC_complaints(request):
    
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
        complaints_data = Complaints.objects.filter(complaint_emp_id=dash_details).order_by('status')

        
     

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data,
                   'employees':employees,
                  }

        return render(request,'TC_complaints.html',content)

    else:
            return redirect('/')  
    

def TC_complaint_add(request):
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
        if request.POST:
            emp_id= request.POST['to_id']
            emp= EmployeeRegister_Details.objects.get(id=emp_id)
            complaint=request.POST['complaint_content']
            complaint_date = date.today()
             
            data = Complaints(complaint_emp_id=emp,compaint_content=complaint,complaint_date=complaint_date) 
            data.save()

            success=True
            success_text = 'Response add successfully.'
           

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data,
                   'employees':employees,
                   'success':success,
                   'success_text':success_text}
            return render(request,'TC_complaints.html',content)
   

#  Lead Section -----------------------------------

def TC_leads(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)  
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date') 

        #---------------------------------------------------------------------------------------------------------------

        
        assing_leads = Leads_assignto_tc.objects.filter(TC_Id=dash_details).order_by('-Assign_Date')
        assing_leads_count = assing_leads.count()

       

        d1 = None
        d2 = None
        status_val = None
        pgnum = 30

        if request.POST:
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            pgnum = request.POST['pgnum']
            status_val = request.POST['status_val']

            if status_val:
                  assing_leads =assing_leads.filter(dataBank_ID__lead_status=status_val) 

            if d1:
                assing_leads = assing_leads.filter(Assign_Date__gte=d1) 
               
            if d2:
                assing_leads = assing_leads.filter(Assign_Date__lte=d2) 

        assing_leads_count = assing_leads.count()

        if pgnum:
            pgnum =int(pgnum)
            assing_leads = assing_leads[:pgnum]

            

        data = Leads_assignto_tc.objects.filter(TC_Id=dash_details)
        assign_values = Leads_assignto_tc.objects.filter(TC_Id=dash_details).values('id')
        data_count = None

        lcg_Names = LeadCategory_Register.objects.filter(cTaskId__cTcompId=company)
        TAL = data.count()
        TACP = data.filter(Status=0).count()
        TFL = data.filter(Status=1).count() 
        TJL = data.filter(Update_Action=1).count() 
        WL = Waste_Leads.objects.filter(assignto_tc_id__in=assign_values,Status=0)
        WLP = 0
        if TAL > 0:
            WLP = int((TAL/100)*20)
        
        TAL_WLP = TAL- WLP
        
        if TAL_WLP:
            PERF = round(((TJL/(TAL_WLP))*100),2)
        else:
            PERF = 1
       

        today_date = date.today()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'assing_leads':assing_leads,
                   'assing_leads_count':assing_leads_count,
                   'd1':d1,'d2':d2,'status_val':status_val,'pg_num':pgnum,



                   
                   'data_count':data_count,
                'lcg_Names':lcg_Names,
                   'notifications':notifications,
                   'today_date':today_date,
                   'TAL':TAL,'TACP':TACP,'TFL':TFL,'TJL':TJL,'PERF':PERF
                  }
    return render(request,'TC_all_leads.html',content) 
  

def hr_leadAccept(request):
        
    # Accept Allocated leads
    if request.POST:
        leadSelected = request.POST.getlist('lead_check')

        allocate_count = 0

        for lid in leadSelected:

            data=Leads_assignto_tc.objects.get(id=lid)
            data.Status = 1

            db = DataBank.objects.get(id= data.dataBank_ID.id)
            db.lead_status ='Opend'
            #db.save()
            #data.save()
            allocate_count = allocate_count + 1
        
        success_text = str(allocate_count) + ' leads accepted ' + 'successfully.'
        messages.success(request, success_text)
           
        return redirect('TC_dashboard') 


def hr_leadReport(request,date_str):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)  
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date') 

        
        TodayassingObjs = Leads_assignto_tc.objects.filter(TC_Id=dash_details,Assign_Date=date_str).order_by('-Assign_Date')
        assingObjs = Leads_assignto_tc.objects.filter(TC_Id=dash_details,).order_by('-Assign_Date')
        data_count = TodayassingObjs.count()
       
        data = assingObjs.values('Assign_Date').annotate(count=Count('id'))
        result = {obj['Assign_Date']: obj['count'] for obj in data}
        
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'assingObjs':assingObjs,
                   'data_count':data_count,
                   'result':result,
                   'TodayassingObjs':TodayassingObjs,
                   
                  }
    return render(request,'TC_leadsReport.html',content) 


def TC_waste_leads(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date') 

        waste_objs =  Waste_Leads.objects.filter(TC_Id=dash_details).order_by('Status')
        waste_objs = waste_objs.order_by('-waste_marked_Date')
        pg_num =30

        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            status_val = request.POST['status_val']
            pg_num = request.POST['pgnum']

            if d1:
                waste_objs = waste_objs.filter(waste_marked_Date__gte=d1)

            if d2:
                waste_objs = waste_objs.filter(waste_marked_Date__lte=d2)     
            
            if status_val:
                waste_objs = waste_objs.filter(Status=status_val)

        waste_objs_count = waste_objs.count()
        
        if pg_num:
            
            pg_num = int(pg_num)
            waste_objs = waste_objs[:pg_num]
       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'waste_objs':waste_objs,
                   'waste_objs_count':waste_objs_count,
                   'pg_num':pg_num,
                   
                   
                  }
    return render(request,'TC_waste_leads.html',content)


def TC_waste_leads_page(request,id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        data = Waste_Leads.objects.filter(TC_Id=dash_details.id,client_id=id,Status=1)
        more = lead_Details.objects.all()
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'data':data,
                   'more':more,
                   'id':id,
                   'notifications':notifications
                   
                  }
    return render(request,'TC_waste_leads_page.html',content)




# Follow up  section-------------------------

def Tc_follow_upLeads(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        #-------------------------------------------------------------------------------------------------------------
        t_date = date.today() 

        dataBank_objs = Leads_assignto_tc.objects.filter(~Q(Response='Mark as waste'),
                                                ~Q(dataBank_ID__lead_status='Closed'),
                                                TC_Id=dash_details,Status=1)
        dataBank_objs = dataBank_objs.order_by('-Assign_Date')

        pgnum =30

        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            d3 = request.POST['follow_date']
            pgnum = request.POST['pgnum']
            status_val = request.POST['status_val']

            if d1:
                dataBank_objs = dataBank_objs.filter(Assign_Date__gte=d1)
            if d2:
                dataBank_objs = dataBank_objs.filter(Assign_Date__lte=d2)
            if d3:
                dataBank_objs = dataBank_objs.filter(Next_update_date=d3)
            if status_val:
                dataBank_objs = dataBank_objs.filter(dataBank_ID__current_status=status_val)

        leads_obj_count = dataBank_objs.count()
            
        if pgnum:
            pgnum = int(pgnum)
            dataBank_objs = dataBank_objs[:pgnum]

        
        
        follow_obj = FollowupStatus.objects.filter(company_Id__id=dash_details.emp_comp_id.id)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'dataBank_objs':dataBank_objs,
                   'notifications':notifications,
                   'leads_obj_count':leads_obj_count,
                   't_date':t_date,
                   'follow_obj':follow_obj,
                   'pg_num':pgnum
                  }
        return render(request,'TC_lead_followup_page.html',content)


def Lead_FollowUp_Updates(request,flID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        try:
            data = Leads_assignto_tc.objects.get(id=flID)
            db_obj = DataBank.objects.get(id=data.dataBank_ID.id)

            if data.leadId :

                FD_obj = FollowupDetails.objects.filter(lead_Id=data.leadId).last()
                FD_objs = FollowupDetails.objects.filter(lead_Id=data.leadId).order_by('-id')
                FBH_objs = FollowupHistory.objects.filter(hs_lead_Id=data.leadId).order_by('-id')


            call_records = Leads_Call_Record.objects.filter(Leads_assignto_tc_id=data)
            lead_details_objs = lead_Details.objects.filter(leadId=data.leadId)

           

        except Leads_assignto_tc.DoesNotExist:

           pass

        
        flstatus = FollowupStatus.objects.filter(company_Id__id=dash_details.emp_comp_id.id)
       
        

        today_date = date.today() 
       
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'data':data,
              
                   'flstatus':flstatus,
                   'notifications':notifications,
                   'today_date':today_date,'lead_details_objs':lead_details_objs,
                   'flID':flID,'call_records':call_records,
                   'FD_obj':FD_obj,'FD_objs':FD_objs,
                   'db_obj':db_obj,'FBH_objs':FBH_objs,
                  }
        return render(request,'TC_lead_followup_UpdatePage.html',content)


def TC_update_Clients_Response(request,id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id,active_status=1)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash,emp_active_status=1)
     
    if request.method == 'POST':
          response=request.POST['Response']
          reason=request.POST['Reason']
          record=request.FILES.get('record')
          next_date=request.POST['nud']
          ud=date.today()
          tc = Leads_assignto_tc.objects.get(id=id)
          if next_date != '':
              tc.Next_update_date=next_date
          else:
            next_date =  date.today() + timedelta(days=1)
            tc.Next_update_date=next_date 


          tc.Response = response
          tc.Reason = reason
          tc.Update_Date=ud
          
          
          tc.save()
          if (record): 
            tcr=Leads_Call_Record(Leads_assignto_tc_id=tc,Record=record,leadId=tc.leadId)
            print('Record found')
            tcr.save()
          
           

            #Adding Followuo respinse and details to FollowupDetails
          FD_obj = FollowupDetails()

          FD_obj.lead_Id = tc.leadId
          FD_obj.comp_Id = tc.TC_Id.emp_comp_id
          FD_obj.hr_telecaller_Id = tc.TC_Id
          FD_obj.response_date = date.today()
          FD_obj.response = str(reason)
          if next_date != '':
            FD_obj.nextfollowup_date = next_date
          else:
            next_date =  date.today() + timedelta(days=1)
            FD_obj.nextfollowup_date = next_date
         
          FD_obj.response_status = response
          FD_obj.save()

          db = DataBank.objects.get(id=tc.dataBank_ID.id)
          db.current_status = response
          if next_date != '':
            db.followup_date = next_date
            
            db.save()
          else:
              next_date =  date.today() + timedelta(days=1)
              db.followup_date = next_date
              db.save()
              
          

          FDHistory = FollowupHistory.objects.filter(hs_lead_Id__id=tc.leadId.id,hr_telecaller_Id__id=tc.TC_Id.id).last()
          FDHistory.final_status = response
          FDHistory.note = 'Lead status changed.'
          FDHistory.allocated_date = date.today() 
          FDHistory.save()

          messages.success(request, "Response updated successfully.")

          try:
                assingObjs = Leads_assignto_tc.objects.filter(Q(Assign_Date=date.today()) | Q(dataBank_ID__current_status='No updation'),TC_Id=dash_details,Status=1).last()
        
                return redirect('Lead_FollowUp_Updates',assingObjs.id)
          
          except Leads_assignto_tc.DoesNotExist:
                return redirect('Tc_follow_upLeads')
   

def TC_waste_leads_action(request,id):

        if request.POST:
            data=Leads_assignto_tc.objects.get(id=id)
            data.Response='Mark as waste'
            data.save()
        
            reason_data = request.POST['reason_for']
           
            waste=Waste_Leads(client_id = data.client_id,TC_Id = data.TC_Id,leadId = data.leadId,dbId=data.dataBank_ID,reason=reason_data,assignto_tc_id=data)
            waste.save()
            messages.success(request, f'{data.leadId.lead_name} marked as waste lead.')
            return redirect('Tc_follow_upLeads')


def hr_leadClose(request,laID):

    la = Leads_assignto_tc.objects.get(id=laID)
    la.Status = 2
    la.Next_update_date = None
    la.Update_Date = date.today()
    la.save()

    FH_obj = FollowupHistory()
    FH_obj.hs_lead_Id = la.leadId
    FH_obj.hs_comp_Id = la.TC_Id.emp_comp_id
    FH_obj.hr_telecaller_Id = la.TC_Id
    FH_obj.allocated_date = date.today()
    FH_obj.note = 'Lead is closed. '
    FH_obj.final_status = 'Closed'
    FH_obj.save()

    db_obj = DataBank.objects.get(id=la.dataBank_ID.id)
    db_obj.followup_date = None
    db_obj.lead_status = 'Closed'
    db_obj.save()
    
    messages.success(request, f'{la.leadId.lead_name}  closed successfully.')
    return redirect('Tc_follow_upLeads')


def hr_recallUpdate(request,assID):
    la = Leads_assignto_tc.objects.get(id=assID)
    la.Status = 1
    la.Update_Action=0
    la.Response = 'Recalled'
    la.Next_update_date = date.today()
    la.Update_Date=None
    la.save()

    FH_obj = FollowupHistory.objects.filter(hs_lead_Id=la.leadId,hr_telecaller_Id=la.TC_Id).last()
    FH_obj.hs_lead_Id = la.leadId
    FH_obj.hs_comp_Id = la.TC_Id.emp_comp_id
    FH_obj.hr_telecaller_Id = la.TC_Id
    FH_obj.allocated_date = date.today()
    FH_obj.note = 'Lead is recalled. '
    FH_obj.final_status = 'Recalled'
    FH_obj.save()

    db_obj = DataBank.objects.get(id=la.dataBank_ID.id)
   
    db_obj.followup_date =  date.today()
    db_obj.lead_status = 'Recalled'
    db_obj.save()
    messages.success(request, f'{la.leadId.lead_name}  recalled successfully.')
    return redirect('Tc_follow_upLeads')



def hr_leadJoined(request,ljID):
    la = Leads_assignto_tc.objects.get(id=ljID)
    la.Update_Action = 1
    la.Status = 2
    la.Next_update_date = None
    la.Update_Date = date.today()
    la.save()

    FH_obj = FollowupHistory()
    FH_obj.hs_lead_Id = la.leadId
    FH_obj.hs_comp_Id = la.TC_Id.emp_comp_id
    FH_obj.hr_telecaller_Id = la.TC_Id
    FH_obj.allocated_date = date.today()
    FH_obj.note = 'Lead is joined. '
    FH_obj.final_status = 'Joined'
    FH_obj.save()

    db_obj = DataBank.objects.get(id=la.dataBank_ID.id)
    db_obj.followup_date = None
    db_obj.lead_status = 'Joined'
    db_obj.save()
    messages.success(request, f'{la.leadId.lead_name}  joined successfully.')
    return redirect('Tc_follow_upLeads')



def Tc_closedlead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        dataBank_objs = Leads_assignto_tc.objects.filter(TC_Id=dash_details,Status=2).order_by('-id')
        dataBank_objs_m = dataBank_objs
        follow_objs = FollowupStatus.objects.filter(company_Id__id=dash_details.emp_comp_id.id)

        pg_num =30 

        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['sdate']
            status_val = request.POST['status_val']
            pg_num = request.POST['pgnum']

            if d1: 
                dataBank_objs = dataBank_objs.filter(Assign_Date__gte=d1)
            if d2: 
                dataBank_objs = dataBank_objs.filter(Assign_Date__lte=d2)
            if status_val: 
                dataBank_objs = dataBank_objs.filter(dataBank_ID__current_status=status_val)

        dataBank_objs_count = dataBank_objs.count()

        if pg_num:
            pg_num = int(pg_num)
            dataBank_objs = dataBank_objs[:pg_num]

        
       
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                    'dataBank_objs':dataBank_objs,
                   'dataBank_objs_count':dataBank_objs_count,
                   'pg_num':pg_num,'follow_objs':follow_objs,
                   'dataBank_objs_m':dataBank_objs_m
                   
                  }
        return render(request,'TC_closedlead_page.html',content)


def Tc_followupDetails(request,lID):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        data = Leads_assignto_tc.objects.get(id=lID)
        lead_obj = Leads.objects.get(id=data.leadId.id)
        followup_details_obj = FollowupDetails.objects.filter(lead_Id=lead_obj).order_by('-id')
        followup_history_obj = FollowupHistory.objects.filter(hs_lead_Id=lead_obj).order_by('-id')
        lead_details_objs = lead_Details.objects.filter(leadId=lead_obj)
        call_records = Leads_Call_Record.objects.filter(leadId=lead_obj).order_by('-record_Date')
        wsal_obj= Waste_Leads.objects.filter(leadId=data.leadId)

        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'data':data,'wsal_obj':wsal_obj,
                   'followup_details_obj':followup_details_obj,
                   'followup_history_obj':followup_history_obj,
                   'lead_details_objs':lead_details_objs,
                   'lead_obj':lead_obj,
                   'call_records':call_records
                   }
        
    return render(request,'TC_follow_details.html',content)



# Notification ------------------------------------------------

def TC_notification(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   
                   
                   
                  }
    return render(request,'TC_notification.html',content)

def TC_open_notification(request,n_id):
     notification = Notification.objects.get(id=n_id)
     notification.notific_status = 1
     notification.save()
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def TC_delete_notification(request,n_id):
     notification = Notification.objects.get(id=n_id)
     notification.delete()
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def closechange(request):

    if request.POST:
        leads_check = request.POST.getlist('lead_check') 
         
        for l in leads_check:
            la = Leads_assignto_tc.objects.get(id=int(l))
            la.Status = 1
            la.save()

            db = DataBank.objects.get(id=la.dataBank_ID.id)
            db.lead_status = 'Opend'
            db.save()

            wl = Waste_Leads()
            wl.leadId = la.leadId
            wl.assignto_tc_id = la
            wl.dbId = db
            wl.client_id = la.leadId.lead_work_regId.wa_clientId
            wl.TC_Id = la.TC_Id
            wl.waste_marked_Date = date.today()
            wl.reason = db.current_status
            wl.save()
        return redirect('TC_waste_leads')
           
