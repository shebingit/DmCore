from datetime import date
from django.shortcuts import render,redirect
from .models import *
from Supper_admin.views import supper_admin_dashboard
from django.http import JsonResponse
from Telecaller.models import*

#Login Section ------------
def login_page(request):
    title = 'Digital Markenting Core-Login'
    content = {'title':title}
    return render(request,'login.html',content)

def login_submitt(request):

    if request.POST:

        try:
            log_dashboard =  LogRegister_Details.objects.get(log_username=request.POST['email_id'],log_password=request.POST['password_id'] )
            

            if log_dashboard.position == 'Super Admin':

                request.session["super_admin_id"]=log_dashboard.id
                if 'super_admin_id' in request.session:
                    if request.session.has_key('super_admin_id'):
                        su_admin_id = request.session['super_admin_id']
                    else:
                        return redirect('/')
                    
                    Super_Admin = LogRegister_Details.objects.get(id=su_admin_id)

                    success=True
                    success_text = 'Your authenticated successfully.'
            
                    content = {'Super_Admin':Super_Admin,'success':success}
            
                return render(request,'SA_dashboard.html',content)
            

            
            
            elif log_dashboard.position == 'Admin':

                request.session["admin_id"]=log_dashboard.id
                if 'admin_id' in request.session:
                    if request.session.has_key('admin_id'):
                        admin_id = request.session['admin_id']
                    else:
                        return redirect('/')
                    
                    try:
                    
                        Admin_dash = LogRegister_Details.objects.get(id=admin_id,active_status=1)



                    except LogRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'Your account is inactive'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
                    

                    try:

                        Admin_dash = LogRegister_Details.objects.get(id=admin_id,active_status=1)
                        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash,company_active_status=1)


                        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
                        # counts section

                        employee_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=1).count()
                        department_count = DepartmentRegister_details.objects.filter(brd_id=dash_details).count()
                        client_count = ClientRegister.objects.filter(compId=dash_details).count()
                        databank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details).count()

                        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
                
                        success=True
                        success_text = 'Your authenticated successfully.'

                       
                           
                        content = { 'Admin_dash':Admin_dash,
                                    'dash_details':dash_details,
                                    'employees':employees,
                                    'employee_count':employee_count,
                                    'department_count':department_count,
                                    'client_count':client_count,
                                    'databank_count':databank_count,
                                   'success':success,
                                   'success_text':success_text}
                        
                        return render(request,'AD_dashboard.html',content)
                    
                    except BusinessRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'You account is not verified.'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
            
            
            elif log_dashboard.position == 'Distributor':

                request.session["distr_id"]=log_dashboard.id
                if 'distr_id' in request.session:
                    if request.session.has_key('distr_id'):
                        distr_id = request.session['distr_id']
                    else:
                        return redirect('/')
                    try:
                    
                        dis_dash = LogRegister_Details.objects.get(id=distr_id,active_status=1)

                    except LogRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'Your account is inactive'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
            

                    try:
                        dash_details = DistributorRegister_Details.objects.get(logdis_id=dis_dash,dis_active_status=1)

                        success=True
                        success_text = 'Your authenticated successfully.'

                        content = {'dis_dash':dis_dash,'dash_details':dash_details,'success':success}

                        return render(request,'Distributor_dashboard.html',content)
                    
                    except DistributorRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'You account is not verified.'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
            

            elif log_dashboard.position == 'Employee':

                request.session["emp_id"]=log_dashboard.id
                if 'emp_id' in request.session:
                    if request.session.has_key('emp_id'):
                        emp_id = request.session['emp_id']
                    else:
                        return redirect('/')
                    
                    try:
                    
                        emp_dash = LogRegister_Details.objects.get(id=emp_id,active_status=1)

                    except LogRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'Your account is inactive'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
                    
                    try:
                        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash,emp_active_status=1)
                       
                        success=True
                        success_text = 'Your authenticated successfully.'
                        
                        content = {'emp_dash':emp_dash,
                                   'dash_details':dash_details,
                                   'success':success,
                                   'success_text':success_text}
                        
                        # Dashbord List-----
                        
                        # ----Dashbord Name ---  --Dashboard ID--
                        # Digital Marketing Head -     1
                        # Team Lead              -     2
                        # Exicutive              -     3
                        # Hr / Telecaller        -     4
                        # Data Manager           -     5

                        hr_content = {'emp_dash':emp_dash,
                                   'dash_details':dash_details,
                                   'success':success,
                                   'success_text':success_text,
                                   
                                     }
                        
                        if dash_details.emp_designation_id.dashboard_id == 1:
                        
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
                        
                        elif dash_details.emp_designation_id.dashboard_id == 2:
                             
                            return render(request,'TL_dashboard.html',content)
                           
                        elif dash_details.emp_designation_id.dashboard_id == 3:
                            return render(request,'Executive_dashboard.html',content)
                            
                        elif dash_details.emp_designation_id.dashboard_id == 4:
                            
                            notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
                            today_date = date.today()
                           
                            content = {'emp_dash':emp_dash,
                                   'dash_details':dash_details,
                                   'success':success,
                                   'success_text':success_text,
                                   'today_date':today_date,
                                   'notifications':notifications
                                   
                                     }
                            return render(request,'TC_dashboard.html',content)
                            
                        elif dash_details.emp_designation_id.dashboard_id == 5:
                             
                            return render(request,'DAM_dashboard.html',content)    
                        
                        else:
                            return render(request,'error-404.html')
                            

                    except EmployeeRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'You account is not verified.'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
        
        except LogRegister_Details.DoesNotExist:
            
            error_message = 'Incorrect email id or password  '
            content ={'error_message':error_message}
            return render(request,'login.html',content)

    else:
        error_message = 'Oops! something went wrong please try again '
        content ={'error_message':error_message}
        return render(request,'login.html',content)


#Registration Section---------
def company_registration_form(request):
    title = 'Digital Markenting Core\Company Registration'
    content = {'title':title}
    return render(request,'business_register.html',content)


def company_registration_form_save(request):

    if request.POST:

        log_details = LogRegister_Details()

        log_details.log_username = request.POST['business_uname']
        log_details.log_password = request.POST['business_password']
        log_details.position = 'Admin'
        log_details.active_status = 1
        log_details.save()

        bussiness_reg = BusinessRegister_Details()

        bussiness_reg.log_id = log_details
        bussiness_reg.owner_fname = request.POST['fname']
        bussiness_reg.owner_lname = request.POST['lname']
        bussiness_reg.company_name = request.POST['companyName']
        bussiness_reg.company_identify_Id = request.POST['companyID']
        bussiness_reg.contact_no = request.POST['contactNo']
        bussiness_reg.company_email = request.POST['companyEmail']
        bussiness_reg.company_location = request.POST['companyLocation']
        bussiness_reg.company_website = request.POST['companyWebsite']
        bussiness_reg.company_active_status = 1
        bussiness_reg.save()

        success = True
        success_text = 'Business'


        content = {'success':success,
                    'success_text':success_text}

        return render(request,'login.html',content)
    
    else:
        return render(request,'business_register.html')


def employee_registration_form(request):
    companyees = BusinessRegister_Details.objects.filter(company_active_status=1)
    title = 'Digital Markenting Core\Employee Registration'
    
    content = {'title':title,'companyees':companyees}
    return render(request,'employee_register.html',content)


def get_departments(request):
   
   identifier_id = request.GET.get('company_id')

   try:
    company = BusinessRegister_Details.objects.get(company_identify_Id=identifier_id)
   except BusinessRegister_Details.DoesNotExist:
    return JsonResponse({'departments': []})

   departments = DepartmentRegister_details.objects.filter(brd_id=company, dept_active_status=1).values('id', 'dept_name')

   department_list = [{'id': department['id'], 'name': department['dept_name']} for department in departments]

   return JsonResponse({'departments': department_list})



def get_designation(request):
    deptart_id = request.GET.get('deptartment_id')
    companyees = DepartmentRegister_details.objects.get(id=deptart_id)
    designations = DesignationRegister_details.objects.filter(dept_id=companyees,desig_active_status=1).values('id', 'desig_name')
    
    designation_list = [{'id': designation['id'], 'name': designation['desig_name']} for designation in designations]
    return JsonResponse({'designation_data': designation_list})


def employee_registration_form_save(request):

    if request.POST:

        log_details = LogRegister_Details()

        log_details.log_username = request.POST['emp_username']
        log_details.log_password = request.POST['emp_password']
        log_details.position = 'Employee'
        log_details.save()

        emp = EmployeeRegister_Details()

        emp.logreg_id = log_details
        identifier_id=request.POST['companyID']
        company_details=BusinessRegister_Details.objects.get(company_identify_Id=identifier_id)
        emp.emp_comp_id = company_details
        emp.emp_department_id = DepartmentRegister_details.objects.get(id=int(request.POST['emp_dept_name']))
        emp.emp_designation_id = DesignationRegister_details.objects.get(id=int(request.POST['emp_desig_name']))

        emp.emp_name = request.POST['emp_name']
        emp.emp_email = request.POST['emp_email']
        emp.emp_contact_no = request.POST['emp_contact']
        emp.save()

        success = True
        success_text = 'Employee'

        content = {'success':success,
                    'success_text':success_text}

        return render(request,'login.html',content)
    
    else:

        return render(request,'employee_register.html')


def business_distributor_registration_form(request):

    title = 'Digital Markenting Core\Distributor Registration'
    
    content = {'title':title}
    return render(request,'business_distributor_register.html',content)


def business_distributor_registration_form_save(request):

    if request.POST:

        log_details = LogRegister_Details()

        log_details.log_username = request.POST['dis_username']
        log_details.log_password = request.POST['dis_password']
        log_details.position = 'Distributor'
        log_details.save()

        distributor = DistributorRegister_Details()

        distributor.logdis_id = log_details
        distributor.dis_name =  request.POST['dis_fname'] + ' ' +  request.POST['dis_lname']
        distributor.dis_email =  request.POST['dis_email']
        distributor.dis_contact_no =  request.POST['dis_contact']
        distributor.dis_location =  request.POST['dis_location']
        distributor.dis_agencies =  request.POST['dis_agenci']
        
        distributor.save()

        success = True
        success_text = 'Distributor'


        content = {'success':success,
                    'success_text':success_text}

        return render(request,'login.html',content)
    
    else:

        return render(request,'business_distributor_register.html')


# Validation check - Email 

def check_email(request):
    email = request.GET.get('e-data', None)
    print('hai:',email)
    if email:

        email_exists = LogRegister_Details.objects.filter(log_username=email).exists()
        return JsonResponse({'exists': email_exists})

    return JsonResponse({'exists': False})
    
# Validation check - Company Identifier ID 

def check_company_id(request):
    company_id = request.GET.get('companyID', None)
    data = {'exists': BusinessRegister_Details.objects.filter(company_identify_Id=company_id).exists()}
    return JsonResponse(data)



