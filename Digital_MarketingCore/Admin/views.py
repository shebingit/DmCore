from datetime import date
from Telecaller.models import Leads_assignto_tc,Waste_Leads
from Registration_Login.models import *
from DataManager.models import DataBank
from django.db.models import Q
from DM_Head.models import *
from DataManager.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from itertools import chain 
from django.db.models import Count
from django.shortcuts import render,redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def admin_checker_section(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        if request.POST:
            try:
                log_dashboard =  LogRegister_Details.objects.get(log_username=request.POST['emailid'],log_password=request.POST['passwordid'] )
                
                content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                }
        
                return render(request,'Checker/AD_checkerDashBoard.html',content)
            
            except LogRegister_Details.DoesNotExist:

                return redirect('admin_checker_section')

        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
        }
     
        return render(request,'Checker/AD_checkerLogin.html',content)
    else:
            return redirect('/')
    return redirect('login_page')

# Dashboard section---------------------------------

def admin_dashboard(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)

        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
        # counts section

        employee_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=1).count()
        department_count = DepartmentRegister_details.objects.filter(brd_id=dash_details).count()
        client_count = ClientRegister.objects.filter(compId=dash_details).count()
        databank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details).count()

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'employees':employees,
            'employee_count':employee_count,
            'department_count':department_count,
            'client_count':client_count,
            'databank_count':databank_count
           
        }

        return render(request,'AD_dashboard.html',content)

    else:
            return redirect('/')
    return redirect('login_page')

# Logout Section ---------------------------------

def admin_logout(request):
    request.session.pop('admin_id', None)
    return redirect('login_page')
        
    
#Appove Login 

def admin_login_requestpage(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)


        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }

        return render(request,'AD_login_requests.html',content)

    else:
            return redirect('/')


def admin_login_approve(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        employees_obj = EmployeeRegister_Details.objects.get(id=pk)
        employees_obj.emp_active_status = 1
        employees_obj.save()

        log_obj = LogRegister_Details.objects.get(id=employees_obj.logreg_id.id)
        log_obj.active_status=1
        log_obj.save()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }

        return render(request,'AD_login_requests.html',content)

    else:
            return redirect('/')


def admin_login_reject(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        employees_obj = EmployeeRegister_Details.objects.get(id=pk)
        employees_obj.emp_active_status = 2
        employees_obj.save()

        log_obj = LogRegister_Details.objects.get(id=employees_obj.logreg_id.id)
        log_obj.active_status=2
        log_obj.save()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }

        return render(request,'AD_login_requests.html',content)

    else:
            return redirect('/')


# Profile Page -------------------------

def admin_profile(request):  
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        
        # notification-----------
        
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            
        }

        return render(request,'AD_profile.html',content)

    else:
            return redirect('/')

def admin_Profile_detailsUpdate(request):
     
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        
        # notification-----------
        


        # Details Save -----------------

        if request.POST:
             
            emp_obj = BusinessRegister_Details.objects.get(id=dash_details.id)

            emp_obj.company_name = request.POST['cname']
            emp_obj.owner_fname = request.POST['fname']
            emp_obj.owner_lname = request.POST['lname']
            emp_obj.contact_no = request.POST['contactno']
            emp_obj.company_email = request.POST['empEmail']
            emp_obj.company_address1 = request.POST['add1']
            emp_obj.company_address2 = request.POST['add2']
            emp_obj.company_address3 = request.POST['add3']
            emp_obj.company_pin = request.POST['pincode']
            emp_obj.company_location = request.POST['loc']
            emp_obj.company_district = request.POST['empdist']
            emp_obj.company_state = request.POST['empState']
            emp_obj.company_website = request.POST['cwebsite']

            if request.FILES.get('empProfile'):
                emp_obj.company_image = request.FILES.get('empProfile')

            else:
                emp_obj.company_image =  emp_obj.company_image 

             

            emp_obj.save()
            success_text = 'Profile Details Updated.'
            success = True

        
        
            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'success_text':success_text,
                'success':success
            }
            return redirect('admin_profile')

        else:
            error_text = 'Profile Details Updated.'
            error = True
            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'error_text':error_text,
                'error':error
            }

        return render(request,'AD_profile.html',content)

    else:
            return redirect('/')
    

# Remove Profile Image ---------------

def admin_profileImage_remove(request):
    emp_id = request.POST.get('emp_id')
    dash_details = BusinessRegister_Details.objects.get(id=emp_id)
    dash_details.company_image = ''
    dash_details.save()
    return JsonResponse({'message': 'Received emp_id: ' + emp_id})

# Password Section -----------------------------------

def admin_password(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # notification-----------
        
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
           
        }

        return render(request,'AD_password.html',content)

    else:
            return redirect('/')

def admin_passwordUpdate(request):

    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        

        # notification-----------
       

        if request.POST:
           
           Admin_dash.log_username = request.POST['emp_uname']
           Admin_dash.log_password = request.POST['emp_password']

           Admin_dash.save()  
           success = True
           success_text = 'User name or password change.'
        
           content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'success':success,
                'success_text':success_text
            }
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'error':error,
                'error_text':error_text
            }

        return render(request,'AD_password.html',content)

    else:
            return redirect('/')


# Department ---------------------

def admin_department(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        departments = DepartmentRegister_details.objects.filter(brd_id=dash_details)

        if request.POST:
             
            depart_obj = DepartmentRegister_details()
            depart_obj.dept_name = request.POST['department_name']
            depart_obj.dept_content = request.POST['department_discription']
            depart_obj.dept_active_status = 1
            depart_obj.brd_id = dash_details
            depart_obj.save()

            success = True
            success_text = 'New department created successfully '

            departments = DepartmentRegister_details.objects.filter(brd_id=dash_details)

        
            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'success':success,
                'success_text':success_text,
                'departments':departments
            }

        else:
             
            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'departments':departments
            }

        return render(request,'AD_department.html',content)

    else:
            return redirect('/')

def admin_department_edit(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        departments = DepartmentRegister_details.objects.filter(brd_id=dash_details)


        # edit-----------
        if request.POST:
     
            depart_obj = DepartmentRegister_details.objects.get(id=pk)
            depart_obj.dept_name = request.POST['department_name']
            depart_obj.dept_content = request.POST['department_discription']
            depart_obj.save()

            success = True
            success_text = 'Department details edited successfully '

            return redirect('admin_department')
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'success':success,
            'success_text':success_text,
            'departments':departments
           
        }

        return render(request,'AD_department.html',content)

    else:
            return redirect('/')


def admin_department_delete(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        departments = DepartmentRegister_details.objects.filter(brd_id=dash_details)


        # delete-----------
        if request.POST:
     
            depart_obj = DepartmentRegister_details.objects.get(id=pk)
            depart_obj.delete()

            success = True
            success_text = 'Department deleted successfully '

            return redirect('admin_department')
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'success':success,
            'success_text':success_text,
            'departments':departments
           
        }

        return render(request,'AD_department.html',content)

    else:
            return redirect('/')




# Designation ----------------------------

def admin_designation(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        departments = DepartmentRegister_details.objects.filter(brd_id=dash_details,dept_active_status=1)
        designations = DesignationRegister_details.objects.filter(dept_id__in=departments)

        if request.POST:
            
            desidnation_obj = DesignationRegister_details()

            desidnation_obj.desig_name = request.POST['designation_name']
            desidnation_obj.desig_content = request.POST['designation_discription']
            desidnation_obj.desig_brd_id = dash_details
            desidnation_obj.dept_id =  DepartmentRegister_details.objects.get(id=int(request.POST['deparmentId'])) 
            desidnation_obj.desig_active_status = 1
            desidnation_obj.dashboard_id = request.POST['dashboardId'] 
            desidnation_obj.save()

            success = True
            success_text = 'New designation add successfully '
            designations = DesignationRegister_details.objects.filter(dept_id__in=departments)
           

            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'departments':departments,
                'designations':designations,
                'success':success,
                'success_text':success_text
            }

        else:
            
            content = {
                'Admin_dash':Admin_dash,
                'dash_details':dash_details,
                'departments':departments,
                'designations':designations
            }

        return render(request,'AD_designation.html',content)

    else:
            return redirect('/')
     
def admin_designation_edit(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        departments = DepartmentRegister_details.objects.filter(brd_id=dash_details,dept_active_status=1)
        designations = DesignationRegister_details.objects.filter(dept_id__in=departments)

        # edit-----------

        if request.POST:
            
            designation_obj = DesignationRegister_details.objects.get(id=pk)

            designation_obj.desig_name = request.POST['designation_name']
            designation_obj.desig_content = request.POST['designation_discription']
            designation_obj.dept_id =  DepartmentRegister_details.objects.get(id=int(request.POST['deparmentId'])) 
            designation_obj.dashboard_id = request.POST['dashboardId'] 
            designation_obj.save()

            success = True
            success_text = 'Designation details edited successfully '

            return redirect('admin_designation')
           
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'departments':departments,
            'designations':designations,
            'success':success,
            'success_text':success_text
        }

        

        return render(request,'AD_designation.html',content)

    else:
        return redirect('/')

def admin_designation_delete(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        departments = DepartmentRegister_details.objects.filter(brd_id=dash_details,dept_active_status=1)
        designations = DesignationRegister_details.objects.filter(dept_id__in=departments)

        # delete-----------

        if request.POST:
            
            designation_obj = DesignationRegister_details.objects.get(id=pk)
            designation_obj.delete()

            success = True
            success_text = 'Designation details deleted successfully '

            return redirect('admin_designation')

           
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'departments':departments,
            'designations':designations,
            'success':success,
            'success_text':success_text
        }

        

        return render(request,'AD_designation.html',content)

    else:
        return redirect('/')


# Employees Section ---------------------------------


def admin_employees_section(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------
        
        content = {

            'admin_dash':admin_dash,
            'dash_details':dash_details,
        }

        return render(request,'AD_employeeSection.html',content)

    else:
        return redirect('/')


# View Employees---------------------------------

def admin_viewEmployees(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        
        
        # else:
        #     return render(request,'error-404.html')  

        return render(request,'AD_employeeView.html',content)

    else:
        return redirect('/')    

def admin_employee_verification(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))

        if request.POST:

            employee = EmployeeRegister_Details.objects.get(id=pk)
            employee.emp_verify_status=1
            employee.save()

            success = True
            success_text = 'Employee details verified'
           

        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees,
            'success':success,
            'success_text':success_text,
        }
        
        
        # else:
        #     return render(request,'error-404.html')  

        return render(request,'AD_employeeView.html',content)

    else:
        return redirect('/')    


def admin_employee_inactive(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))

        if request.POST:

            employee = EmployeeRegister_Details.objects.get(id=pk)
            employee.emp_active_status=2
            employee.save()

            success = True
            success_text = 'Success'
           

        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees,
            'success':success,
            'success_text':success_text,
        }
        
        
       

        return render(request,'AD_employeeView.html',content)

    else:
        return redirect('/')    

def admin_employee_active(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=2)

        if request.POST:

            employee = EmployeeRegister_Details.objects.get(id=pk)
            employee.emp_active_status=1
            employee.save()

            success = True
            success_text = 'Success'
           

        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees,
            'success':success,
            'success_text':success_text,
        }
        
        
       


        return render(request,'AD_employeeresignView.html',content)

    else:
        return redirect('/')    



# View Resigned Employees ---------------------------------

def admin_resignedEmployees(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=2)
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        

        return render(request,'AD_employeeresignView.html',content)

    else:
            return redirect('/')    


# Employee wise leave page---------------------------------

def admin_Employeesleaves(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        

        return render(request,'AD_employeeLeaves.html',content)

    else:
            return redirect('/')    


# Employee wise leave details---------------------------------

def admin_get_employee_leavedetails(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        

        # Query your database to fetch employee details based on the employee_id.
        # Replace 'EmployeeLeave' with the actual model that stores employee details.

        employee_details = list(EmployeeLeave.objects.filter(emp_id=employee_id).order_by('-start_date').values())
        

        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': employee_details})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


# Employee wise action page---------------------------------

def admin_Employees_actiontaken(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        

        return render(request,'AD_employeeactions.html',content)

    else:
            return redirect('/')    

# Employee wise action details---------------------------------

def admin_get_employee_actiondetails(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        

        # Query your database to fetch employee details based on the employee_id.
        # Replace 'EmployeeLeave' with the actual model that stores employee details.

        employee_details = list(ActionTaken.objects.filter(act_emp_id=employee_id).order_by('-action_date').values())
        

        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': employee_details})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


# Employee wise feedback page---------------------------------

def admin_Employees_feedback(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        

        return render(request,'AD_employeefeedback.html',content)

# Employee wise feedback details---------------------------------

def admin_get_employee_feedbackdetails(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        

        # Query your database to fetch employee details based on the employee_id.
        # Replace 'EmployeeLeave' with the actual model that stores employee details.

        employee_details = Feedback.objects.filter(from_id=employee_id).order_by('-feedback_date')
        details_list=[]

        for i in employee_details:
            feedback_date= i.feedback_date
            feedback_to=i.feedback_emp_id.emp_name
            feedback_content=i.feedback_content

            details_list.append({
                'feedback_date':feedback_date,
                'feedback_to':feedback_to,
                'feedback_content':feedback_content,
            })

        

        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': details_list})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



# Employee wise complaint page---------------------------------

def admin_Employees_complaints(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        

        return render(request,'AD_employeecomplaint.html',content)


# Employee wise complaint details---------------------------------

def admin_get_employee_complaintdetails(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        

        # Query your database to fetch employee details based on the employee_id.
        # Replace 'EmployeeLeave' with the actual model that stores employee details.

        employee_details = list(Complaints.objects.filter(complaint_emp_id=employee_id).order_by('-complaint_date').values())
        

        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': employee_details})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

# Employee wise Schedules page---------------------------------

def admin_Employees_schedules(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)

        # Notification-----------

        employees = EmployeeRegister_Details.objects.filter(Q(emp_comp_id=dash_details, emp_active_status=0) | Q(emp_comp_id=dash_details, emp_active_status=1))
        
        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'employees':employees
        }
        

        return render(request,'AD_employeeschedules.html',content)

# Employee wise schedule details---------------------------------

def admin_get_employee_scheduledetails(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        

        # Query your database to fetch employee details based on the employee_id.
        # Replace 'EmployeeLeave' with the actual model that stores employee details.

        employee_details = EmployeeSchedule.objects.filter(emp_id=employee_id).order_by('-schedule_date','-start_time')
        details_list=[]

        for i in employee_details:
            schedule_date= i.schedule_date
            start_time=i.start_time
            end_time=i.end_time
            schedule_head=i.schedule_head
            content=i.todo_content
            schedule_status=i.schedule_status
            

            details_list.append({
                'schedule_date':schedule_date,
                'starttime': start_time,
                'endtime': end_time,
                'schedule_head':schedule_head,
                'content':content,
                'schedule_status':schedule_status,
            })

        

        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': details_list})



# Employee Allocated list---------------------------------

def admin_employeeAllocated_list(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=admin_dash)


        # Notification-----------

        team_lead = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=2)
        

        content = {
            'admin_dash':admin_dash,
            'dash_details':dash_details,
            'team_lead':team_lead,
        }

        return render(request,'AD_employeeAllocatedList.html',content)

    else:
            return redirect('/')    

# teamlead wise employees allocated details---------------------------------

def admin_get_employee_allocatedetails(request):
    if request.method == 'POST':
        teamlead_id = request.POST.get('employee_id')
        

        # Query your database to fetch employee details based on the employee_id.

        employee_details = Allocation_Details.objects.filter(allocat_to=teamlead_id).order_by('-alloaction_date')
        details_list=[]

        for i in employee_details:
            date= i.alloaction_date
            emp_name=i.allocatEmp_id.emp_name
            teamlead=i.allocat_to.emp_name
            status=i.allocate_status
            
            
            details_list.append({
                'date':date,
                'emp_name': emp_name,
                'teamlead': teamlead,
                'status':status,
            })


        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': details_list})

def admin_all_works(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # counts section

        head_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=1,emp_active_status=1).count()
        tl_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=2,emp_active_status=1).count()
        executive_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=3,emp_active_status=1).count()
        client_count = ClientRegister.objects.filter(compId=dash_details,client_status=1).count()

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'head_count':head_count,
            'tl_count':tl_count,
            'executive_count':executive_count,
            'client_count':client_count,
        }

        return render(request,'AD_workpage.html',content)

    else:
            return redirect('/')

def admin_executivework_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # executive section
        executives = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=3,emp_active_status=1)

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'executives':executives,
        }

        return render(request,'AD_executivework_page.html',content)

    else:
            return redirect('/')


# executive,tl,head wise work, dailywork details---------------------------------

def admin_get_employee_workdetails(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        head_company=EmployeeRegister_Details.objects.get(id=employee_id).emp_comp_id 
        

        # Query your database to fetch employee details based on the employee_id.

        ongoing_details = TaskAssign.objects.filter(ta_workerId=employee_id,ta_status=1,ta_accept_status=1).order_by('-ta_start_date')
        completed_details = TaskAssign.objects.filter(ta_workerId=employee_id,ta_status=2).order_by('-ta_start_date')
        allocation_details = WorkAssign.objects.filter(wa_work_allocate=employee_id).order_by('-work_assign_date')
        workassign_details = WorkRegister.objects.filter(wcompId=head_company).order_by('-work_create_time')
        client_details = ClientRegister.objects.filter(compId=head_company).order_by('-client_add_time')
        clientwork_details=ClientTask_Register.objects.filter(cTcompId=head_company).order_by('-task_create_date')



        ongoing_list=[]
        completed_list=[]
        allocation_list=[]
        workassign_list=[]
        client_list=[]
        clientworks_list=[]

        # ongoing work details of employees.

        for i in ongoing_details:
            t_id=i.id
            sdate= i.ta_start_date
            edate= i.ta_due_date
            task_name=i.ta_taskId.task_name
            progress=i.ta_progress
            status=i.ta_status
            
            
            ongoing_list.append({
                'id':t_id,
                'sdate':sdate,
                'edate':edate,
                'name': task_name,
                'progress': progress,
                'status':status,
            })


        # completed work details of employees.

        for i in completed_details:
            t_id=i.id
            sdate= i.ta_start_date
            edate= i.ta_due_date
            task_name=i.ta_taskId.task_name
            progress=i.ta_progress
            status=i.ta_status
            
            
            completed_list.append({
                'id':t_id,
                'sdate':sdate,
                'edate':edate,
                'name': task_name,
                'progress': progress,
                'status':status,
            })


        # allocation details of team lead employees.

        for i in allocation_details:
            t_id=i.id
            adate= i.work_assign_date
            sdate= i.wa_from_date
            edate= i. wa_due_date
            executive_names = [emp.emp_name for emp in i.allocated_exemp.all()]
            task=[emp.task_name for emp in i.wa_tasksId.all()]
            target=i.wa_target
            atarget=i.wa_target_achived
            progress=i.work_assign_progress
            
            
            
            allocation_list.append({
                'id':t_id,
                'adate':adate,
                'sdate':sdate,
                'edate':edate,
                'name':executive_names,
                'task':task,
                'target':target,
                'atarget':atarget,
                'progress':progress,
                
            })


        # allocation details of head employees.

        for i in workassign_details:
            t_id=i.id
            cdate= i.work_create_date
            edate= i.work_end_date
            client=i.clientId.client_name
            tl_names = [emp.emp_name for emp in i.allocated_emp.all()]
            progress=i.work_progress
            astatus=i.work_allocate_status
            wstatus=i.work_status
            
            
            workassign_list.append({
                'id':t_id,
                'cdate':cdate,
                'edate':edate,
                'client':client,
                'tl_names':tl_names,
                'progress':progress,
                'astatus':astatus,
                'wstatus':wstatus,
                
            })    


        # client details under the company.

        for i in client_details:
            t_id=i.id
            date= i.client_reg_date
            name=i.client_name
            email=i.client_email_primary
            phone=i.client_phone
            place=i.client_place
            district=i.client_district
            state=i.client_state
            status=i.client_status
            
            
            client_list.append({
                'id':t_id,
                'date':date,
                'name':name,
                'email':email,
                'phone':phone,
                'place':place,
                'district':district,
                'state':state,
                'status':status,
                
            }) 


        # client work details under the company.

        for i in clientwork_details:
            t_id=i.id
            date= i.task_create_date
            client=i.client_Id.client_name
            task=i.task_name
            description=i.task_discription
            progress=i.task_total_progress
            astatus=i.task_allocate_status
            tstatus=i.task_status
            
            
            clientworks_list.append({
                'id':t_id,
                'date':date,
                'client':client,
                'task':task,
                'description':description,
                'progress':progress,
                'astatus':astatus,
                'tstatus':tstatus,
                
            }) 
       
        context={
            'details1':ongoing_list,
            'details2':completed_list,
            'details3':allocation_list,
            'details4':workassign_list,
            'details5':client_list,
            'details6':clientworks_list,
        }    
        
        
        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse(context)


def admin_get_employee_dailyworkdetails(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        

        # Query your database to fetch daily work details based on the task_id.
        task= TaskAssign.objects.get(id=task_id)
        dailywork_details = TaskDetails.objects.filter(tad_taskAssignId=task).order_by('-tad_collect_date')

        daily_list=[]
        

        for i in dailywork_details:
            t_id=i.id
            date= i.tad_collect_date
            title=i.tad_title
            description=i.tad_discription
            target=i.tad_target
            vtarget=i.tad_verified_target
            status=i.tad_status
           
            
            
            daily_list.append({
                'id':t_id,
                'date':date,
                'title':title,
                'description': description,
                'target': target,
                'vtarget':vtarget,
                'status':status,
                
            })

        
        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse({'details': daily_list,})


def admin_tlwork_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # tl section
        tl = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=2,emp_active_status=1)

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'tl':tl,
        }

        return render(request,'AD_tlwork_page.html',content)

    else:
        return redirect('/')


def admin_headwork_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        #head section
        head = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_designation_id=1,emp_active_status=1)

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'head':head,
        }

        return render(request,'AD_headwork_page.html',content)

    else:
        return redirect('/')


def admin_clientswork_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        #clients count
        new_count = ClientRegister.objects.filter(
            compId=dash_details
        ).exclude(
            id__in=WorkRegister.objects.filter(wcompId=dash_details).values('clientId').distinct()
        ).count()

        ongoing_count = ClientRegister.objects.filter(
            id__in=WorkRegister.objects.filter(
                wcompId=dash_details,work_status=0,
            ).values('clientId').distinct()
        ).count()


        completed_count = ClientRegister.objects.filter(
            id__in=WorkRegister.objects.filter(
                wcompId=dash_details,
                work_status=1,
                work_progress=100
            ).values('clientId').distinct()
        ).count()
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'new_count':new_count,
            'ongoing_count':ongoing_count,
            'completed_count':completed_count,
        }

        return render(request,'AD_clientswork_page.html',content)

    else:
        return redirect('/')

def admin_new_clientswork(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        #new clients section
        newclients = ClientRegister.objects.filter(
            compId=dash_details
        ).exclude(
            id__in=WorkRegister.objects.filter(wcompId=dash_details).values('clientId').distinct()
        ).order_by('-client_reg_date')

        
        
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'newclients':newclients,
        }

        return render(request,'AD_new_clientswork.html',content)

    else:
        return redirect('/')

def admin_ongoing_clientswork(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

       # Get a queryset of clients with completed work under this admin
        ongoing_clients = ClientRegister.objects.filter(
            id__in=WorkRegister.objects.filter(
                wcompId=dash_details,
                work_status=0,
            ).values('clientId').distinct()
        )

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'ongoing_clients':ongoing_clients,
        }

        return render(request,'AD_ongoing_clientswork.html',content)

    else:
        return redirect('/')

# Client wise ongoing work, dailywork details---------------------------------

def admin_get_client_ongoingworkdetails(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        

        # Query your database to fetch employee details based on the employee_id.
        registeredwork_details = WorkRegister.objects.filter(clientId=client_id,work_status=0).order_by('-work_create_date','-work_create_time')
        clientwork_details=ClientTask_Register.objects.filter(client_Id=client_id,work_Id__in=registeredwork_details).order_by('-task_create_date')
        allocation_details = WorkAssign.objects.filter(wa_clientId=client_id,wa_work_regId__in=registeredwork_details).order_by('-work_assign_date')
        ongoing_details = TaskAssign.objects.filter(ta_taskId__client_Id=client_id,ta_workAssignId__in=allocation_details,ta_status=1,ta_accept_status=1).order_by('-ta_start_date')
        completed_details = TaskAssign.objects.filter(ta_taskId__client_Id=client_id,ta_workAssignId__in=allocation_details,ta_status=2).order_by('-ta_start_date')
        


        registeredwork_list=[]
        clientworks_list=[]
        allocation_list=[]
        ongoing_list=[]
        completed_list=[]
        # client_list=[]
        

        # allocation details of head employees.

        for i in registeredwork_details:
            t_id=i.id
            cdate= i.work_create_date
            edate= i.work_end_date
            client=i.clientId.client_name
            tl_names = [emp.emp_name for emp in i.allocated_emp.all()]
            progress=i.work_progress
            astatus=i.work_allocate_status
            wstatus=i.work_status
            
            
            registeredwork_list.append({
                'id':t_id,
                'cdate':cdate,
                'edate':edate,
                'client':client,
                'tl_names':tl_names,
                'progress':progress,
                'astatus':astatus,
                'wstatus':wstatus,
                
            })   

        # client work details under the company.

        for i in clientwork_details:
            t_id=i.id
            date= i.task_create_date
            client=i.client_Id.client_name
            task=i.task_name
            description=i.task_discription
            progress=i.task_total_progress
            astatus=i.task_allocate_status
            tstatus=i.task_status
            
            
            clientworks_list.append({
                'id':t_id,
                'date':date,
                'client':client,
                'task':task,
                'description':description,
                'progress':progress,
                'astatus':astatus,
                'tstatus':tstatus,
                
            }) 


        # allocation details of team lead employees.

        for i in allocation_details:
            t_id=i.id
            adate= i.work_assign_date
            sdate= i.wa_from_date
            edate= i. wa_due_date
            executive_names = [emp.emp_name for emp in i.allocated_exemp.all()]
            task=[emp.task_name for emp in i.wa_tasksId.all()]
            target=i.wa_target
            atarget=i.wa_target_achived
            progress=i.work_assign_progress
            
            
            
            allocation_list.append({
                'id':t_id,
                'adate':adate,
                'sdate':sdate,
                'edate':edate,
                'name':executive_names,
                'task':task,
                'target':target,
                'atarget':atarget,
                'progress':progress,
                
            })




        # ongoing work details of employees.

        for i in ongoing_details:
            t_id=i.id
            sdate= i.ta_start_date
            edate= i.ta_due_date
            task_name=i.ta_taskId.task_name
            employee=i.ta_workerId.emp_name
            progress=i.ta_progress
            status=i.ta_status
            
            
            ongoing_list.append({
                'id':t_id,
                'sdate':sdate,
                'edate':edate,
                'name': task_name,
                'employee':employee,
                'progress': progress,
                'status':status,
            })



        # completed work details of employees.

        for i in completed_details:
            t_id=i.id
            sdate= i.ta_start_date
            edate= i.ta_due_date
            task_name=i.ta_taskId.task_name
            employee=i.ta_workerId.emp_name
            progress=i.ta_progress
            status=i.ta_status
            
            
            completed_list.append({
                'id':t_id,
                'sdate':sdate,
                'edate':edate,
                'name': task_name,
                'employee':employee,
                'progress': progress,
                'status':status,
            })


       

       
        context={
            'details1':registeredwork_list,
            'details2':clientworks_list,
            'details3':allocation_list,
            'details4':ongoing_list,
            'details5':completed_list,   
        }    
        
        
        
        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse(context)



def admin_completed_clientswork(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

       # Get a queryset of clients with completed work under this admin
        completed_clients = ClientRegister.objects.filter(
            id__in=WorkRegister.objects.filter(
                wcompId=dash_details,
                work_status=1,
                work_progress=100
            ).values('clientId').distinct()
        )

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'completed_clients':completed_clients,
        }

        return render(request,'AD_completed_clientswork.html',content)

    else:
        return redirect('/')


# Client wise completed work, dailywork details---------------------------------

def admin_get_client_completedworkdetails(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        

        # Query your database to fetch employee details based on the employee_id.
        registeredwork_details = WorkRegister.objects.filter(clientId=client_id,work_status=1,work_progress=100).order_by('-work_create_date','-work_create_time')
        clientwork_details=ClientTask_Register.objects.filter(client_Id=client_id,work_Id__in=registeredwork_details).order_by('-task_create_date')
        allocation_details = WorkAssign.objects.filter(wa_clientId=client_id,wa_work_regId__in=registeredwork_details).order_by('-work_assign_date')
        ongoing_details = TaskAssign.objects.filter(ta_taskId__client_Id=client_id,ta_workAssignId__in=allocation_details,ta_status=1,ta_accept_status=1).order_by('-ta_start_date')
        completed_details = TaskAssign.objects.filter(ta_taskId__client_Id=client_id,ta_workAssignId__in=allocation_details,ta_status=2).order_by('-ta_start_date')
        


        registeredwork_list=[]
        clientworks_list=[]
        allocation_list=[]
        ongoing_list=[]
        completed_list=[]
        # client_list=[]
        

        # allocation details of head employees.

        for i in registeredwork_details:
            t_id=i.id
            cdate= i.work_create_date
            edate= i.work_end_date
            client=i.clientId.client_name
            tl_names = [emp.emp_name for emp in i.allocated_emp.all()]
            progress=i.work_progress
            astatus=i.work_allocate_status
            wstatus=i.work_status
            
            
            registeredwork_list.append({
                'id':t_id,
                'cdate':cdate,
                'edate':edate,
                'client':client,
                'tl_names':tl_names,
                'progress':progress,
                'astatus':astatus,
                'wstatus':wstatus,
                
            })   

        # client work details under the company.

        for i in clientwork_details:
            t_id=i.id
            date= i.task_create_date
            client=i.client_Id.client_name
            task=i.task_name
            description=i.task_discription
            progress=i.task_total_progress
            astatus=i.task_allocate_status
            tstatus=i.task_status
            
            
            clientworks_list.append({
                'id':t_id,
                'date':date,
                'client':client,
                'task':task,
                'description':description,
                'progress':progress,
                'astatus':astatus,
                'tstatus':tstatus,
                
            }) 


        # allocation details of team lead employees.

        for i in allocation_details:
            t_id=i.id
            adate= i.work_assign_date
            sdate= i.wa_from_date
            edate= i. wa_due_date
            executive_names = [emp.emp_name for emp in i.allocated_exemp.all()]
            task=[emp.task_name for emp in i.wa_tasksId.all()]
            target=i.wa_target
            atarget=i.wa_target_achived
            progress=i.work_assign_progress
            
            
            
            allocation_list.append({
                'id':t_id,
                'adate':adate,
                'sdate':sdate,
                'edate':edate,
                'name':executive_names,
                'task':task,
                'target':target,
                'atarget':atarget,
                'progress':progress,
                
            })




        # ongoing work details of employees.

        for i in ongoing_details:
            t_id=i.id
            sdate= i.ta_start_date
            edate= i.ta_due_date
            task_name=i.ta_taskId.task_name
            employee=i.ta_workerId.emp_name
            progress=i.ta_progress
            status=i.ta_status
            
            
            ongoing_list.append({
                'id':t_id,
                'sdate':sdate,
                'edate':edate,
                'name': task_name,
                'employee':employee,
                'progress': progress,
                'status':status,
            })



        # completed work details of employees.

        for i in completed_details:
            t_id=i.id
            sdate= i.ta_start_date
            edate= i.ta_due_date
            task_name=i.ta_taskId.task_name
            employee=i.ta_workerId.emp_name
            progress=i.ta_progress
            status=i.ta_status
            
            
            completed_list.append({
                'id':t_id,
                'sdate':sdate,
                'edate':edate,
                'name': task_name,
                'employee':employee,
                'progress': progress,
                'status':status,
            })


       

       
        context={
            'details1':registeredwork_list,
            'details2':clientworks_list,
            'details3':allocation_list,
            'details4':ongoing_list,
            'details5':completed_list,
           
            
        }    
        
        
        
        # You might want to serialize the 'employee_details' to a JSON format.
        return JsonResponse(context)

# lead section
def admin_leads_section(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

       
        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            
        }

        return render(request,'AD_leads_section.html',content)

    else:
        return redirect('/')



def admin_leads_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # Get a queryset of clients with lead work under this admin
        # Assuming you have instances of ClientTask_Register model with task_name='lead collection'
        tasks_with_lead_collection = ClientTask_Register.objects.filter(task_name='lead collection',cTcompId=dash_details)

        # Get the corresponding clients using the reverse relation
        clients = ClientRegister.objects.filter(clienttask_register__in=tasks_with_lead_collection)

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'clients':clients,
            
        }

        return render(request,'AD_leads_page.html',content)

    else:
        return redirect('/')


# Client wise lead details---------------------------------

def admin_get_client_leaddetails(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')

        # Query your database to fetch lead details based on the client_id.
        client = get_object_or_404(ClientRegister, id=client_id)
        client_tasks = ClientTask_Register.objects.filter(client_Id=client, task_name='lead collection')
        
        # Assuming ta_taskId is a ForeignKey in TaskAssign pointing to TaskAssign model
        task_assigns = TaskAssign.objects.filter(ta_taskId__in=client_tasks)
        
        leads = Leads.objects.filter(lead_taskAssignId__in=task_assigns, waste_data=0).order_by('-lead_add_date', '-lead_add_time')
        
        leaddata_list = []

        # Lead details of clients.
        for lead in leads:
            lead_id = lead.id
            date = lead.lead_add_date
            employee = lead.lead_collect_Emp_id.emp_name
            lead_category=lead.lead_category_id.lead_collection_for
            lead_name = lead.lead_name
            lead_email = lead.lead_email
            lead_contact = lead.lead_contact
            lead_source = lead.lead_source

            # Get all lead details related to this lead
            lead_details = lead_Details.objects.filter(leadId=lead)

            lead_details_list = []
            for detail in lead_details:
                lead_details_list.append({
                    'field_name': detail.lead_field_name,
                    'field_data': detail.lead_field_data,
                })

            leaddata_list.append({
                'id': lead_id,
                'date': date,
                'employee': employee,
                'category':lead_category,
                'name': lead_name,
                'email': lead_email,
                'contact': lead_contact,
                'source': lead_source,
                'lead_details': lead_details_list,
            })

        context = {
            'details1': leaddata_list,
        }

        # Return the serialized data as JSON.
        return JsonResponse(context)


# Client wise lead category details---------------------------------

def get_lead_categories(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        lead_categories = LeadCategory_Register.objects.filter(cTaskId__client_Id=client_id).values('lead_collection_for').distinct()

        return JsonResponse(list(lead_categories), safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# lead collected employee details---------------------------------

def get_lead_collected_employees(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        
        # Query your database to fetch lead details based on the client_id.
        client = get_object_or_404(ClientRegister, id=client_id)
        client_tasks = ClientTask_Register.objects.filter(client_Id=client, task_name='lead collection')
        
        # Assuming ta_taskId is a ForeignKey in TaskAssign pointing to TaskAssign model
        task_assigns = TaskAssign.objects.filter(ta_taskId__in=client_tasks)

        # Extract employee instances from TaskAssign instances
        employees = task_assigns.values('ta_workerId__id', 'ta_workerId__emp_name').distinct()
        
        
        return JsonResponse(list(employees), safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Client, employee  wise lead details---------------------------------

def admin_get_client_employee_leaddetails(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        employee_id =request.POST.get('employee_id')

        employee_details = EmployeeRegister_Details.objects.get(id=employee_id)

        # Query your database to fetch lead details based on the client_id.
        client = get_object_or_404(ClientRegister, id=client_id)
        client_tasks = ClientTask_Register.objects.filter(client_Id=client, task_name='lead collection')
        
        # Assuming ta_taskId is a ForeignKey in TaskAssign pointing to TaskAssign model
        task_assigns = TaskAssign.objects.filter(ta_taskId__in=client_tasks)
        
        leads = Leads.objects.filter(lead_taskAssignId__in=task_assigns, waste_data=0,lead_collect_Emp_id=employee_details).order_by('-lead_add_date', '-lead_add_time')
        
        leaddata_list1 = []

        # Lead details of clients.
        for lead in leads:
            lead_id = lead.id
            date = lead.lead_add_date
            employee = lead.lead_collect_Emp_id.emp_name
            lead_category=lead.lead_category_id.lead_collection_for
            lead_name = lead.lead_name
            lead_email = lead.lead_email
            lead_contact = lead.lead_contact
            lead_source = lead.lead_source

            # Get all lead details related to this lead
            lead_details = lead_Details.objects.filter(leadId=lead)

            lead_details_list = []
            for detail in lead_details:
                lead_details_list.append({
                    'field_name': detail.lead_field_name,
                    'field_data': detail.lead_field_data,
                })

            leaddata_list1.append({
                'id': lead_id,
                'date': date,
                'employee': employee,
                'category':lead_category,
                'name': lead_name,
                'email': lead_email,
                'contact': lead_contact,
                'source': lead_source,
                'lead_details': lead_details_list,
            })

       
        context = {
            'details2': leaddata_list1,
        }

        # Return the serialized data as JSON.
        return JsonResponse(context)

def admin_wasteleads_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # Get a queryset of clients with lead work under this admin
        # Assuming you have instances of ClientTask_Register model with task_name='lead collection'
        tasks_with_lead_collection = ClientTask_Register.objects.filter(task_name='lead collection',cTcompId=dash_details)

        # Get the corresponding clients using the reverse relation
        clients = ClientRegister.objects.filter(clienttask_register__in=tasks_with_lead_collection)

        
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'clients':clients,
            
        }

        return render(request,'AD_wasteleads_page.html',content)

    else:
        return redirect('/')

def admin_get_client_wasteleaddetails(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')

        # Query your database to fetch lead details based on the client_id.
        client = get_object_or_404(ClientRegister, id=client_id)
        client_tasks = ClientTask_Register.objects.filter(client_Id=client, task_name='lead collection')
        
        # Assuming ta_taskId is a ForeignKey in TaskAssign pointing to TaskAssign model
        task_assigns = TaskAssign.objects.filter(ta_taskId__in=client_tasks)
        
        leads = Leads.objects.filter(lead_taskAssignId__in=task_assigns, waste_data=1).order_by('-lead_add_date', '-lead_add_time')
        
        leaddata_list = []

        # Lead details of clients.
        for lead in leads:
            lead_id = lead.id
            date = lead.lead_add_date
            employee = lead.lead_collect_Emp_id.emp_name
            lead_category=lead.lead_category_id.lead_collection_for
            lead_name = lead.lead_name
            lead_email = lead.lead_email
            lead_contact = lead.lead_contact
            lead_source = lead.lead_source

            # Get all lead details related to this lead
            lead_details = lead_Details.objects.filter(leadId=lead)

            lead_details_list = []
            for detail in lead_details:
                lead_details_list.append({
                    'field_name': detail.lead_field_name,
                    'field_data': detail.lead_field_data,
                })

            leaddata_list.append({
                'id': lead_id,
                'date': date,
                'employee': employee,
                'category':lead_category,
                'name': lead_name,
                'email': lead_email,
                'contact': lead_contact,
                'source': lead_source,
                'lead_details': lead_details_list,
            })

        context = {
            'details1': leaddata_list,
        }

        # Return the serialized data as JSON.
        return JsonResponse(context)


# Client, employee  wise lead details---------------------------------

def admin_get_client_employee_wasteleaddetails(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        employee_id =request.POST.get('employee_id')

        employee_details = EmployeeRegister_Details.objects.get(id=employee_id)

        # Query your database to fetch lead details based on the client_id.
        client = get_object_or_404(ClientRegister, id=client_id)
        client_tasks = ClientTask_Register.objects.filter(client_Id=client, task_name='lead collection')
        
        # Assuming ta_taskId is a ForeignKey in TaskAssign pointing to TaskAssign model
        task_assigns = TaskAssign.objects.filter(ta_taskId__in=client_tasks)
        
        leads = Leads.objects.filter(lead_taskAssignId__in=task_assigns, waste_data=1,lead_collect_Emp_id=employee_details).order_by('-lead_add_date', '-lead_add_time')
        
        leaddata_list1 = []

        # Lead details of clients.
        for lead in leads:
            lead_id = lead.id
            date = lead.lead_add_date
            employee = lead.lead_collect_Emp_id.emp_name
            lead_category=lead.lead_category_id.lead_collection_for
            lead_name = lead.lead_name
            lead_email = lead.lead_email
            lead_contact = lead.lead_contact
            lead_source = lead.lead_source

            # Get all lead details related to this lead
            lead_details = lead_Details.objects.filter(leadId=lead)

            lead_details_list = []
            for detail in lead_details:
                lead_details_list.append({
                    'field_name': detail.lead_field_name,
                    'field_data': detail.lead_field_data,
                })

            leaddata_list1.append({
                'id': lead_id,
                'date': date,
                'employee': employee,
                'category':lead_category,
                'name': lead_name,
                'email': lead_email,
                'contact': lead_contact,
                'source': lead_source,
                'lead_details': lead_details_list,
            })

       
        context = {
            'details2': leaddata_list1,
        }

        # Return the serialized data as JSON.
        return JsonResponse(context)


def admin_followupleads_page(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        # Get a queryset of clients with lead work under this admin
        # Assuming you have instances of ClientTask_Register model with task_name='lead collection'
        tasks_with_lead_collection = ClientTask_Register.objects.filter(task_name='lead collection',cTcompId=dash_details)

        # Get the corresponding clients using the reverse relation
        clients = ClientRegister.objects.filter(clienttask_register__in=tasks_with_lead_collection)
        task_assigns = TaskAssign.objects.filter(ta_taskId__in=tasks_with_lead_collection)

        works=WorkRegister.objects.filter(wcompId=dash_details)

        followup_leads=Leads.objects.filter(lead_work_regId__in=works,waste_data=0,lead_transfer_status=1).order_by('-lead_add_date', '-lead_add_time')
        #followup_lead_details=lead_Details.objects.filter(leadId__in=followup_leads)
        #followup_followup_details = FollowupDetails.objects.filter(lead_Id__in=followup_leads).order_by('response_date')
        #followup_history_details = FollowupHistory.objects.filter(hs_lead_Id__in=followup_leads)
        hr_telecaller=EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details)
        followup_status=FollowupStatus.objects.filter(company_Id=dash_details)
       
       
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'clients':clients,
            #'followup_leads':followup_leads,
            #'followup_lead_details':followup_lead_details,
            #'followup_followup_details': followup_followup_details,
            #'followup_history_details': followup_history_details,
            'hr_telecaller':hr_telecaller,
            'followup_status':followup_status,
            
            
        }

        return render(request,'AD_followupleads_page.html',content)

    else:
        return redirect('/')
    


def admin_lead_details(request,pk):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

  

        followup_leads=Leads.objects.get(id=pk,waste_data=0,lead_transfer_status=1)
        followup_lead_details=lead_Details.objects.filter(leadId=followup_leads)
        followup_followup_details = FollowupDetails.objects.filter(lead_Id=followup_leads).order_by('response_date')
        followup_history_details = FollowupHistory.objects.filter(hs_lead_Id=followup_leads)
       
       
       
        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'followup_leads':followup_leads,
            'followup_lead_details':followup_lead_details,
            'followup_followup_details': followup_followup_details,
            'followup_history_details': followup_history_details,
           
            
            
        }

        return render(request,'AD_followupleads_Detailspage.html',content)

    else:
        return redirect('/')


def get_leadcategory(request):
    client_id = request.GET.get('client_id')

    try:
        client = ClientRegister.objects.get(id=client_id)
    except ClientRegister.DoesNotExist:
        return JsonResponse({'categories': []})

    categories = LeadCategory_Register.objects.filter(cTaskId__client_Id=client).values('id', 'lead_collection_for')

    category_list = [{'id': category['id'], 'name': category['lead_collection_for']} for category in categories]

    return JsonResponse({'categories': category_list})




def filter_lead(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')

        # Fetch follow-up leads based on the client_id
        followup_leads = Leads.objects.filter(
            lead_taskAssignId__ta_taskId__client_Id_id=client_id, 
            lead_transfer_status=1, 
            waste_data=0
        ).order_by('-lead_add_date', '-lead_add_time')

        lcount = Leads.objects.filter(
            lead_taskAssignId__ta_taskId__client_Id_id=client_id, 
            lead_transfer_status=1, 
            waste_data=0
        ).count()
        # Build a list of dictionaries for follow-up leads
        lead_list = []
        db_obj=None

        for lead in followup_leads:
           

            lead_list.append({
                'date': lead.lead_transfer_date,
                'client_name': lead.lead_taskAssignId.ta_taskId.client_Id.client_name,
                'category': lead.lead_category_id.lead_collection_for,
                'name': lead.lead_name,
                'email': lead.lead_email,
                'contact': lead.lead_contact,
                'source': lead.lead_source,
                'modalid': lead.id,
               
                'collected_by': lead.lead_collect_Emp_id.emp_name,
            })
        
        context={
            'details1': lead_list,'lcount':lcount,
        }

        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def filter_lead_category(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        category_id = request.POST.get('category_id')

       
        # Fetch follow-up leads based on the client_id, categor_id
        followup_leads_category = Leads.objects.filter(
            lead_taskAssignId__ta_taskId__client_Id_id=client_id, 
            lead_transfer_status=1,
            waste_data=0,
            lead_category_id=category_id
        ).order_by('-lead_add_date', '-lead_add_time')

        lcount  = Leads.objects.filter(
            lead_taskAssignId__ta_taskId__client_Id_id=client_id, 
            lead_transfer_status=1,
            waste_data=0,
            lead_category_id=category_id
        ).count()
        # Build a list of dictionaries for follow-up leads
        leadcategory_list = []
        for lead in followup_leads_category:
            

            leadcategory_list.append({
                'date': lead.lead_transfer_date,
                'client_name': lead.lead_taskAssignId.ta_taskId.client_Id.client_name,
                'category': lead.lead_category_id.lead_collection_for,
                'name': lead.lead_name,
                'email': lead.lead_email,
                'contact': lead.lead_contact,
                'source': lead.lead_source,
                
                'modalid': lead.id,
                'collected_by': lead.lead_collect_Emp_id.emp_name,
            })
        
        context={
            'details2': leadcategory_list,'lcount':lcount,
        }

        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def filter_lead_hr_telecaller(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
        else:
            return redirect('/')

        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        if request.method == 'POST':
            client_id = request.POST.get('client_id')
            category_id = request.POST.get('category_id')
            caller_id = request.POST.get('caller_id')

            # Get FollowupHistory followup  instances related to the specific hr_telecaller_id in reverse order
            followup_history_details = FollowupHistory.objects.filter(hs_comp_Id=dash_details, hr_telecaller_Id=caller_id)
            followup_details= FollowupDetails.objects.filter(comp_Id=dash_details,  hr_telecaller_Id=caller_id)

            if client_id and category_id:
                
                related_leads_details1 = Leads.objects.filter(
                    lead_taskAssignId__ta_taskId__client_Id_id=client_id,
                    lead_category_id=category_id,
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_history_details.values_list('hs_lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')
                related_leads_details2 = Leads.objects.filter(
                    lead_taskAssignId__ta_taskId__client_Id_id=client_id,
                    lead_category_id=category_id,
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_details.values_list('lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')
            else:
              

                related_leads_details1 = Leads.objects.filter(
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_history_details.values_list('hs_lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')

                related_leads_details2 = Leads.objects.filter(
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_details.values_list('lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')


            # Build a list of dictionaries for follow-up leads
            leadhr_list = []
            lcount=0
            for lead in chain(related_leads_details1, related_leads_details2):
                lcount = lcount+1
                leadhr_list.append({
                    'date': lead.lead_transfer_date,
                    'client_name': lead.lead_taskAssignId.ta_taskId.client_Id.client_name,
                    'category': lead.lead_category_id.lead_collection_for,
                    'name': lead.lead_name,
                    'email': lead.lead_email,
                    'contact': lead.lead_contact,
                    'source': lead.lead_source,
                    'modalid': lead.id,
                    
                    'collected_by': lead.lead_collect_Emp_id.emp_name,
                })

            context = {
                'details3': sorted(leadhr_list, key=lambda x: (x['date'], x['modalid']), reverse=True),'lcount':lcount
            }

            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)

    else:
        return redirect('/')


def filter_lead_status(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
        else:
            return redirect('/')

        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        if request.method == 'POST':
            client_id = request.POST.get('client_id')
            category_id = request.POST.get('category_id')
            caller_id = request.POST.get('caller_id')
            status = request.POST.get('status_id')

            if caller_id:
                # Get FollowupHistory instances related to the specific hr_telecaller_id in reverse order
                followup_history_statusdetails = FollowupHistory.objects.filter(hs_comp_Id=dash_details, hr_telecaller_Id=caller_id, final_status=status)
                followup_statusdetails =FollowupDetails.objects.filter(comp_Id=dash_details, hr_telecaller_Id=caller_id,response_status=status)
            else:
                # Get FollowupHistory instances related to the specific hr_telecaller_id in reverse order
                followup_history_statusdetails = FollowupHistory.objects.filter(hs_comp_Id=dash_details,final_status=status)
                followup_statusdetails =FollowupDetails.objects.filter(comp_Id=dash_details,response_status=status)

            
            if client_id and category_id:
                # Get corresponding Leads details for the filtered FollowupHistory instances
                related_leads_details1 = Leads.objects.filter(
                    lead_taskAssignId__ta_taskId__client_Id_id=client_id,
                    lead_category_id=category_id,
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_statusdetails.values_list('lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')
                
                related_leads_details2 = Leads.objects.filter(
                    lead_taskAssignId__ta_taskId__client_Id_id=client_id,
                    lead_category_id=category_id,
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_history_statusdetails.values_list('hs_lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')
            else:
                # Get corresponding Leads details for the filtered FollowupHistory instances
                related_leads_details1 = Leads.objects.filter(
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_statusdetails.values_list('lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')

                related_leads_details2 = Leads.objects.filter(
                    lead_transfer_status=1,
                    waste_data=0,
                    id__in=followup_history_statusdetails.values_list('hs_lead_Id', flat=True)
                ).order_by('-lead_add_date', '-lead_add_time')

            

            # Build a list of dictionaries for follow-up leads
            leadstatus_list = []
            lcount = 0
            # Combine the results from both queries
            for lead in chain(related_leads_details1, related_leads_details2):
                lcount=lcount+1
                leadstatus_list.append({
                    'date': lead.lead_transfer_date,
                    'client_name': lead.lead_taskAssignId.ta_taskId.client_Id.client_name,
                    'category': lead.lead_category_id.lead_collection_for,
                    'name': lead.lead_name,
                    'email': lead.lead_email,
                    'contact': lead.lead_contact,
                    'source': lead.lead_source,
                    'modalid': lead.id,
                    'collected_by': lead.lead_collect_Emp_id.emp_name,
                })

           
            context = {
                'details4': sorted(leadstatus_list, key=lambda x: (x['date'], x['modalid']), reverse=True),'lcount':lcount
            }

            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)

    else:
        return redirect('/')        
    



def filter_lead_date(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
        else:
            return redirect('/')

        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        if request.method == 'POST':
            client_id = request.POST.get('client_id')
            category_id = request.POST.get('category_id')
            caller_id = request.POST.get('caller_id')
            status = request.POST.get('status_id')
            d1 = request.POST.get('fdate')
            d2 = request.POST.get('todate')
            
          

            # Define the base queryset
            databank_obj = DataBank.objects.all()

           
            if client_id:
                databank_obj = databank_obj.filter(lead_Id__lead_work_regId__clientId__id=client_id)

            if category_id:
                databank_obj = databank_obj.filter(lead_Id__lead_category_id__id=category_id)

            if caller_id:
              
                followup_statusdetails =FollowupDetails.objects.filter(comp_Id=dash_details, hr_telecaller_Id=caller_id)
                databank_obj.filter(lead_Id__in=followup_statusdetails.values_list('lead_Id', flat=True))

            if status:
                followup_statusdetails =FollowupDetails.objects.filter(comp_Id=dash_details,response_status=status)
                databank_obj.filter(lead_Id__in=followup_statusdetails.values_list('lead_Id', flat=True))

            if d1 and d2:
                
                databank_obj = databank_obj.filter(allocated_date__gte=d1, allocated_date__lte=d2)

            # Execute the final query
            result_obj = databank_obj.filter(lead_Id__lead_work_regId__wcompId=dash_details)
            lcount = databank_obj.filter(lead_Id__lead_work_regId__wcompId=dash_details).count()
           


            
            leadstatus_list = []
            
           
            for lead in result_obj:
               
                leadstatus_list.append({
                    'date': lead.allocated_date, #lead_Id.lead_transfer_date,
                    'client_name': lead.lead_Id.lead_taskAssignId.ta_taskId.client_Id.client_name,
                    'category': lead.lead_Id.lead_category_id.lead_collection_for,
                    'name': lead.lead_Id.lead_name,
                    'email': lead.lead_Id.lead_email,
                    'contact': lead.lead_Id.lead_contact,
                    'source': lead.lead_Id.lead_source,
                    'modalid': lead.lead_Id.id,
                    'collected_by': lead.lead_Id.lead_collect_Emp_id.emp_name,
                })

           
            context = {
                'lcount':lcount,
                'details5': leadstatus_list,
            }

            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)

    else:
        return redirect('/')        
    

def filter_lead_platform(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        category_id = request.POST.get('category_id')
        platform_id = request.POST.get('platformName')
        plf= PlatForms.objects.get(id=platform_id)

       
        # Fetch follow-up leads based on the client_id, categor_id
        followup_leads_platforms = Leads.objects.filter(
            lead_taskAssignId__ta_taskId__client_Id_id=client_id, 
            lead_transfer_status=1,
            waste_data=0,
            lead_category_id=category_id,
            lead_source=plf.platform_Name
        ).order_by('-lead_add_date', '-lead_add_time')

        lcount  = Leads.objects.filter(
            lead_taskAssignId__ta_taskId__client_Id_id=client_id, 
            lead_transfer_status=1,
            waste_data=0,
            lead_category_id=category_id,
            lead_source=plf.platform_Name
        ).count()
        # Build a list of dictionaries for follow-up leads
        leadplatform_list = []

        for lead in followup_leads_platforms:
            

            leadplatform_list.append({
                'date': lead.lead_transfer_date,
                'client_name': lead.lead_taskAssignId.ta_taskId.client_Id.client_name,
                'category': lead.lead_category_id.lead_collection_for,
                'name': lead.lead_name,
                'email': lead.lead_email,
                'contact': lead.lead_contact,
                'source': lead.lead_source,
                
                'modalid': lead.id,
                'collected_by': lead.lead_collect_Emp_id.emp_name,
            })
        
        context={
            'details6': leadplatform_list,'lcount':lcount,
        }

        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    





    
def admin_pltformdata(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

    
        platform_obj = PlatForms.objects.filter(company_Id__id=dash_details.id)

        if request.POST:
            d1 = request.POST['sdate']
            d2 = request.POST['edate']

            lead_source_count = DataBank.objects.filter(
            lead_Id__lead_work_regId__clientId__compId__id=dash_details.id,
            lead_Id__lead_add_date__gte=d1,
            lead_Id__lead_add_date__lte=d2)\
                .values('lead_Id__lead_source')\
                .annotate(count=Count('lead_Id__lead_source'))
        
        else:

            lead_source_count = DataBank.objects.filter(
            lead_Id__lead_work_regId__clientId__compId__id=dash_details.id)\
                .values('lead_Id__lead_source')\
                .annotate(count=Count('lead_Id__lead_source'))

        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'platform_obj':platform_obj,
            'lead_source_count':lead_source_count,
            
        }

        return render(request,'AD_platformdata.html',content)

    else:
            return redirect('/')


def admin_pltformleads_page(request,lead_source):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

    
        platform_obj = PlatForms.objects.filter(company_Id__id=dash_details.id)

        lead_source_count = DataBank.objects.filter(
        lead_Id__lead_work_regId__clientId__compId__id=dash_details.id,lead_Id__lead_source=lead_source).count()
           

        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'platform_obj':platform_obj,
            'lead_source_count':lead_source_count,
            
        }

        return render(request,'AD_platform_leaddata.html',content)

    else:
            return redirect('/')
    



def admin_reports(request):
    if 'admin_id' in request.session:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
           
        else:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

    
        databank_obj = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details)


        tasks_with_lead_collection = ClientTask_Register.objects.filter(task_name='lead collection',cTcompId=dash_details)

        clients = ClientRegister.objects.filter(clienttask_register__in=tasks_with_lead_collection)
        hr_telecaller=EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details)
        followup_status=FollowupStatus.objects.filter(company_Id=dash_details)

        platform_obj = PlatForms.objects.filter(company_Id=dash_details)
        

        # Count section -----

        databank_obj_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details).count()
        TNC = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details,Genarated_date=date.today()).count()
        APC = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details,lead_allocate_status=0).count()
        TFC = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details,lead_allocate_status=1).count()
        TDFC = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details,followup_date=date.today()).count()

           

        content = {
            'Admin_dash':Admin_dash,
            'dash_details':dash_details,
            'databank_obj':databank_obj,
            'databank_obj_count':databank_obj_count,
            'TNC':TNC,'APC':APC,'TFC':TFC,'TDFC':TDFC,
            'clients':clients,'hr_telecaller':hr_telecaller,
            'followup_status':followup_status,
            'platform_obj':platform_obj            
            
        }

        return render(request,'AD_hr_lead_Report.html',content)

    else:
            return redirect('/')
    


def admin_analysis(request):
    if 'admin_id' in request.session:
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)
        hr_telecaller = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4, emp_comp_id=dash_details)
        tasks_with_lead_collection = ClientTask_Register.objects.filter(task_name='lead collection', cTcompId=dash_details)
        clients = ClientRegister.objects.filter(clienttask_register__in=tasks_with_lead_collection)
        followup_status=FollowupStatus.objects.filter(company_Id=dash_details)

        db_obj = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details)
        

        # Lead marked as waste 
        waste_obj = Waste_Leads.objects.filter(confirmation=1,TC_Id__emp_comp_id__id=dash_details.id).values('dbId')

        # Apply filtering if form is submitted
        if request.method == 'POST':
            hr_id = request.POST.get('hr_select')
            cl_id = request.POST.get('client-select')
            ct_id = request.POST.get('leadcatagory')
            flup_name = request.POST.get('status_select')

            d1 = request.POST.get('sdate')
            d2 = request.POST.get('edate')


           

            result_obj = Leads_assignto_tc.objects.filter(leadId__lead_work_regId__wcompId=dash_details)

           

            if hr_id:
                result_obj = result_obj.filter(TC_Id__id=hr_id).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(TC_Id=hr_id).values('dbId')
                db_obj = db_obj.filter(id__in=result_obj)
                

            if cl_id:
                result_obj = result_obj.filter(leadId__lead_work_regId__clientId__id=cl_id).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(client_id__id=cl_id).values('dbId')
                db_obj = db_obj.filter(id__in=result_obj)

            if ct_id:
                result_obj = result_obj.filter(leadId__lead_category_id__id=cl_id).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(leadId__lead_category_id__id=cl_id).values('dbId')
                db_obj = db_obj.filter(id__in=result_obj)

            if flup_name:
                result_obj = result_obj.filter(Response=flup_name).values_list('dataBank_ID__id')
                db_obj = db_obj.filter(id__in=result_obj)

            if d1 and d2:
                result_obj = result_obj.filter(Assign_Date__gte=d1,Assign_Date__lte=d2,).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(waste_marked_Date__gte=d1,waste_marked_Date__lte=d2).values('dbId')
                db_obj = db_obj.filter(id__in=result_obj)


        db_obj_count = db_obj.count()

        

        
        
        # Performance Calculation
        AL = db_obj.filter(lead_allocate_status=1).count()
        JL = 0
        WL = db_obj.filter(id__in=waste_obj).count()
        FL = db_obj.filter(lead_status='Opend').exclude(current_status='No updation').count()
        APT = db_obj.filter(lead_status='Opend', current_status='No updation').count()

        AL_Pending = db_obj_count - AL
        APT_Pending = AL - APT
        FL_Pending = APT - FL

        hr_Performance = int((JL / AL) * 100) if AL != 0 else 0
        hr_Performance_roundof = round(((JL / AL) * 100), 2) if AL != 0 else 0


       
        content = {
            'Admin_dash': Admin_dash,
            'dash_details': dash_details,
            'hr_telecaller': hr_telecaller,
            'hr_Performance': hr_Performance,
            'hr_Performance_roundof': hr_Performance_roundof,
            'clients': clients,
            'db_obj': db_obj,
            'followup_status':followup_status,
            'db_obj_count': db_obj_count,
            'AL': AL, 'JL': JL, 'FL': FL, 'APT': APT,'WL':WL,
            'AL_Pending': AL_Pending,
            'APT_Pending': APT_Pending,
            'FL_Pending': FL_Pending,
            
        }

        return render(request, 'AD_analysis.html', content)
    else:
        return redirect('/')



def admin_employee_analysis(request):
    if 'admin_id' in request.session:
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        emps_obj = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) |
                                                         Q(emp_designation_id__dashboard_id=2) | 
                                                         Q(emp_designation_id__dashboard_id=3) , 
                                                         emp_comp_id=dash_details)
        
        clients = ClientRegister.objects.filter(compId=dash_details.id)
       
        ld_obj = Leads.objects.filter(lead_work_regId__wcompId=dash_details)
        

       

        # Apply filtering if form is submitted
        if request.method == 'POST':
            emp_id = request.POST.get('emp_select')
            cl_id = request.POST.get('client-select')
            ct_id = request.POST.get('leadcatagory')
            
            d1 = request.POST.get('sdate')
            d2 = request.POST.get('edate')

            ld_obj = Leads.objects.filter(lead_work_regId__wcompId=dash_details)

            if emp_id:

                ld_obj = ld_obj.filter(lead_collect_Emp_id__id=emp_id)
                

            if cl_id: 
               ld_obj = ld_obj.filter(lead_work_regId__clientId__id=cl_id)

            if ct_id:
                ld_obj = ld_obj.filter(lead_category_id__id=cl_id)

            if d1 and d2:
                ld_obj = ld_obj.filter(lead_add_date__gte=d1,lead_add_date__lte=d2)


        ld_obj_count = ld_obj.count()

        
        # Performance Calculation
        CL = ld_obj.filter(Q(lead_status=0) | Q(lead_status=1) ).count()
    
        WL = ld_obj.filter(waste_data=1).count()
        
    
        emp_Performance = int((CL / (CL + WL)) * 100) if CL != 0 else 0
        emp_Performance_roundof = round(((CL / (CL + WL)) * 100), 2) if CL != 0 else 0


       
        content = {
            'Admin_dash': Admin_dash,
            'dash_details': dash_details,
            'emps_obj': emps_obj,
            'emp_Performance': emp_Performance,
            'emp_Performance_roundof': emp_Performance_roundof,
            'clients': clients,
            'ld_obj': ld_obj,
           
            'ld_obj_count': ld_obj_count,
            'CL': CL,  'WL':WL,
            
        }

        return render(request, 'AD_employees_analysis.html', content)
    else:
        return redirect('/')



def admin_comparison(request):
    if 'admin_id' in request.session:
        admin_id = request.session.get('admin_id')
        if not admin_id:
            return redirect('/')
        
        Admin_dash = LogRegister_Details.objects.get(id=admin_id)
        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash)

        clients = ClientRegister.objects.filter(compId=dash_details.id)
        

        AL = 0
        FL = 0
        JL = 0
        WL = 0
        CL = 0
        EWL = 0
        count_value=0

        db_obj = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId=dash_details)
        ld_obj = Leads.objects.filter(lead_work_regId__wcompId=dash_details)

         # Lead marked as waste 
        waste_obj = Waste_Leads.objects.filter(confirmation=1,TC_Id__emp_comp_id__id=dash_details.id).values('dbId')

        if request.method == 'POST':
           
            cl_id = request.POST.get('client-select')
            ct_id = request.POST.get('leadcatagory')
          
            d1 = request.POST.get('sdate')
            d2 = request.POST.get('edate')

            result_obj = Leads_assignto_tc.objects.filter(leadId__lead_work_regId__wcompId=dash_details)

            if cl_id:
                result_obj = result_obj.filter(leadId__lead_work_regId__clientId__id=cl_id).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(client_id__id=cl_id).values('dbId')
                ld_obj = ld_obj.filter(lead_work_regId__clientId__id=cl_id)
                db_obj = db_obj.filter(id__in=result_obj)

            if ct_id:
                result_obj = result_obj.filter(leadId__lead_category_id__id=cl_id).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(leadId__lead_category_id__id=cl_id).values('dbId')
                ld_obj = ld_obj.filter(lead_category_id__id=cl_id)
                db_obj = db_obj.filter(id__in=result_obj)

           
            if d1 and d2:
                result_obj = result_obj.filter(Assign_Date__gte=d1,Assign_Date__lte=d2,).values_list('dataBank_ID__id')
                waste_obj = waste_obj.filter(waste_marked_Date__gte=d1,waste_marked_Date__lte=d2).values('dbId')
                ld_obj = ld_obj.filter(lead_add_date__gte=d1,lead_add_date__lte=d2)
                db_obj = db_obj.filter(id__in=result_obj)

               



        hr_obj = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details)

        hr_performance_list = []

        
        for hr in hr_obj:

            result_obj = Leads_assignto_tc.objects.filter(leadId__lead_work_regId__wcompId=dash_details,TC_Id=hr)
            waste_obj = waste_obj.filter(TC_Id=hr).values('dbId')
            db_obj = db_obj.filter(id__in=result_obj)

            AL = db_obj.filter(lead_allocate_status=1).count()
            JL = 0
            WL = db_obj.filter(id__in=waste_obj).count()
            FL = db_obj.filter(lead_status='Opend').exclude(current_status='No updation').count()

        
            hr_Performance = int((JL / AL) * 100) if AL != 0 else 0
            hr_Performance_roundof = round(((JL / AL) * 100), 2) if AL != 0 else 0
            count_value = count_value +1

            hr_performance_list.append({
                'id':count_value,
            'employee_id': hr.id,
            'employee_name': hr.emp_name,  # Assuming emp object has an attribute 'name'
            'AL':AL,
            'JL':JL,
            'WL':WL,
            'FL':FL,
            'performance': hr_Performance,
            'performance_roundoff': hr_Performance_roundof
            })
                    
        hr_obj_count = len(hr_performance_list)


        #===========================================================================

        emps_obj = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=1) |
                                                         Q(emp_designation_id__dashboard_id=2) | 
                                                         Q(emp_designation_id__dashboard_id=3) , 
                                                         emp_comp_id=dash_details)
        employee_performance_list = []


        for emp in emps_obj:

            CL = ld_obj.filter(lead_collect_Emp_id=emp ).count()
            EWL = ld_obj.filter(waste_data=1,lead_collect_Emp_id=emp ).count() 

            emp_Performance = int((CL / (CL + EWL)) * 100) if CL != 0 else 0
            emp_Performance_roundof = round(((CL / (CL + EWL)) * 100), 2) if CL != 0 else 0
            count_value = count_value +1
            
            employee_performance_list.append({
                    'id':count_value,
            'employee_id': emp.id,
            'employee_name': emp.emp_name,  # Assuming emp object has an attribute 'name'
            'COL':CL,
            'EWLD':EWL,
            'performance': emp_Performance,
            'performance_roundoff': emp_Performance_roundof
            })

        pl_obj_count = len(employee_performance_list)



        content = {
            'Admin_dash': Admin_dash,
            'dash_details': dash_details,
            'clients':clients,
            'pl_obj_count':pl_obj_count,
            'employee_performance_list':employee_performance_list,
            'hr_obj_count':hr_obj_count,
            'hr_performance_list':hr_performance_list
            
        }

        return render(request, 'AD_comparison.html', content)
    else:
        return redirect('/')
