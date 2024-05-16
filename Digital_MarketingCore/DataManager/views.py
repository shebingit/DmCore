from django.shortcuts import render,redirect
from DM_Head.models import EmployeeRegister_Details,Notification,Leads,ClientTask_Register,LeadCategory_Register,lead_Details,ClientRegister
from Telecaller.models import Leads_assignto_tc,Waste_Leads,Leads_Call_Record
from Registration_Login.models import LogRegister_Details
from django.db.models import Q
from django.db.models import Count
from .models import *
from django.db.models import Sum
from django.utils import timezone
from datetime import date
import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string



def dataManager_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id).count()
        dataBank_followup_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_allocate_status=1).count()
        dataBank_allocate_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status='Allocated').count()
        dataBank_open_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status='Opend').count()
        dataBank_close_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status='Closed').count()
        

        queryset = DataBank.objects.filter(
        lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id
        ).values('Genarated_date').annotate(lead_count=Count('id')).order_by('-Genarated_date')

        labels = [item['Genarated_date'].strftime('%Y-%m-%d') for item in queryset]
        votes_data = [item['lead_count'] for item in queryset]

        PlatForms_queryset = PlatForms.objects.filter(company_Id__id=dash_details.emp_comp_id.id)

        # Assuming YourModel has a field named 'platform_Name'
        PlatForms_labels = [item.platform_Name for item in PlatForms_queryset]

        # Assuming YourModel has a field named 'platform_TotalCount'
        PlatForms_votes_data = [item.platform_TotalCount for item in PlatForms_queryset]



        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_followup_count':dataBank_followup_count,
                   'dataBank_count':dataBank_count,
                   'PlatForms_labels': PlatForms_labels, 'PlatForms_votes_data': PlatForms_votes_data,
                   'dataBank_open_count':dataBank_open_count,
                   'dataBank_close_count':dataBank_close_count,
                   'dataBank_allocate_count':dataBank_allocate_count,
                   'labels': labels,
        'votes_data': votes_data,}
        
        return render(request,'DAM_dashboard.html',content)
    return redirect('/')


#Cards On Dashborad Page 

def DAM_Dashboard_databank(request):

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



        cl_name = None
        ct_name = None
        exe_name = None
        d1 = None
        d2 = None
        pg_num = 20
        
       

        if request.POST:
            cl = request.POST['client_id']
            ct = request.POST['category']
            exe = request.POST['executive'] 
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            status_val =  request.POST['status_val']
            pg_num = request.POST['pgnum']

            dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id)
            
            if d1:
                dataBank_objs = dataBank_objs.filter(Genarated_date__gte=d1)

            if d2:
                dataBank_objs = dataBank_objs.filter(Genarated_date__lte=d2)

            if cl:
                cl_name = ClientRegister.objects.filter(id=cl).values('client_name').first()
                dataBank_objs = dataBank_objs.filter(lead_Id__lead_work_regId__clientId__id=cl)

            if ct:
                ct_name =LeadCategory_Register.objects.filter(id=ct).values('lead_collection_for').first()
                dataBank_objs = dataBank_objs.filter(lead_Id__lead_category_id__id=ct)

            if exe:
                exe_name = EmployeeRegister_Details.objects.filter(id=exe).values('emp_name').first()
                dataBank_objs = dataBank_objs.filter(lead_Id__lead_collect_Emp_id__id=exe)

            if status_val:
                dataBank_objs = dataBank_objs.filter(lead_status=status_val)

            if pg_num:
                pg_num =  int(pg_num)
                dataBank_objs = dataBank_objs[:pg_num]
            

            dataBank_count = dataBank_objs.count()
        
        else:
            dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id).count()
            dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id)[:pg_num]
            

        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_objs':dataBank_objs,
                   'dataBank_count':dataBank_count,
                   'd1':d1,'d2':d2,'cl_name':cl_name,'ct_name':ct_name,'exe_name':exe_name,'pg_num':pg_num,
                   'clients_objs':clients_objs}
        
    return render(request,'DAM_Dashboard_dataBank.html',content)


def DataBank_load(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

       

        try:
            
            DB_data = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__compId__id=dash_details.emp_comp_id.id)
            dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__compId__id=dash_details.emp_comp_id.id).count()
            
            data_list = []
            
            for lead in DB_data:
                    
                    data = {
                   
                    'lead_status':lead.lead_status,
                    'Genarated_date': lead.Genarated_date,
                    'lead_name': lead.lead_Id.lead_name,
                    'lead_email': lead.lead_Id.lead_email,
                    'lead_contact': lead.lead_Id.lead_contact,
                    'id': lead.id,
                    'lead_source':lead.lead_Id.lead_source,
                    'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                    'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                    'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                    'c_status': lead.current_status,
                    }
                    data_list.append(data)

            success = True
            message = "Operation successful"



                # Return a JSON response with lead categories
            return JsonResponse({'success': success, 'message': message,'leads_data': data_list,'dataBank_count':dataBank_count,})
          

        except Exception as e:
            # Handle exceptions and return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': str(e)})


def fetch_leads_source(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        source_id = request.GET.get('selectedSource', None)

        try:
            
            DB_data = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__compId__id=dash_details.emp_comp_id.id,lead_Id__lead_source=source_id)
            dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__compId__id=dash_details.emp_comp_id.id,lead_Id__lead_source=source_id).count()
            
            data_list = []
            
            for lead in DB_data:
                    
                    data = {
                   
                    'lead_status':lead.lead_status,
                    'Genarated_date': lead.Genarated_date,
                    'lead_name': lead.lead_Id.lead_name,
                    'lead_email': lead.lead_Id.lead_email,
                    'lead_contact': lead.lead_Id.lead_contact,
                    'id': lead.id,
                    'lead_source':lead.lead_Id.lead_source,
                    'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                    'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                    'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                    'c_status': lead.current_status,
                    }
                    data_list.append(data)

            success = True
            message = "Operation successful"



                # Return a JSON response with lead categories
            return JsonResponse({'success': success, 'message': message,'leads_data': data_list,'dataBank_count':dataBank_count,})
          

        except Exception as e:
            # Handle exceptions and return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': str(e)})


def DAM_dataBnak_edit(request,dbID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        dataBank_obj = DataBank.objects.get(id=dbID)

        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_obj':dataBank_obj,
                   }
        
    return render(request,'DAM_Dashboard_dataBankEdit.html',content)


def DAM_dataBnak_followup(request,dbID):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        dataBank_obj = DataBank.objects.get(id=dbID)
        followup_details_obj = FollowupDetails.objects.filter(lead_Id__id=dataBank_obj.lead_Id.id)
        followup_history_obj = FollowupHistory.objects.filter(hs_lead_Id__id=dataBank_obj.lead_Id.id)
        lead_details_obj = lead_Details.objects.filter(leadId__id=dataBank_obj.lead_Id.id)
        lead_obj = Leads.objects.get(id=dataBank_obj.lead_Id.id)

        call_records = Leads_Call_Record.objects.filter(leadId__id=dataBank_obj.lead_Id.id).order_by('-record_Date')

        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_obj':dataBank_obj,
                   'followup_details_obj':followup_details_obj,
                   'followup_history_obj':followup_history_obj,
                   'lead_details_obj':lead_details_obj,
                   'lead_obj':lead_obj,
                   'call_records':call_records
                   }
        
    return render(request,'DAM_Dashboard_dataBankFollowup.html',content)


def fetch_lead_executive(request):
    try:
       
        category_id = request.GET.get('category_id', None)
       

        if category_id is not None:
         

            leads_obj = DataBank.objects.filter(lead_Id__lead_category_id__id=category_id)
            
            lead_executive_list = [{'id': leads.lead_Id.lead_collect_Emp_id.id, 'name': leads.lead_Id.lead_collect_Emp_id.emp_name} for leads in leads_obj]

            
            # Convert list of dictionaries to set of tuples
            unique_set = set((lead['id'], lead['name']) for lead in lead_executive_list)

            # Convert set of tuples back to a list of dictionaries
            unique_lead_executive_list = [{'id': lead[0], 'name': lead[1]} for lead in unique_set]
            
            success = True
            message = "Operation successful"
            return JsonResponse({'success': success, 'message': message,'lead_executive_list': unique_lead_executive_list})
        else:

            raise ValueError("Client ID is not provided in the request.")

    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})


#Alloaction and Pending Allocated list

def DAM_Dashboard_allocation(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4)
        executives = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=3) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=1))

       
        d1 = None
        d2 = None
        pgnum = 30
        selected_emp = None
        status_val = None

        dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status='Not Attended').exclude(current_status='Marked as Waste')
       

        if request.POST:
            emp = request.POST['executive_id']
            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            pgnum = request.POST['pgnum']

           
            
            if d1:

                dataBank_objs = dataBank_objs.filter(lead_Id__lead_add_date__gte=d1)

            if d2:

                dataBank_objs = dataBank_objs.filter(lead_Id__lead_add_date__lte=d2)
            
            if emp:
                selected_emp = EmployeeRegister_Details.objects.get(id=emp)
                dataBank_objs = dataBank_objs.filter(lead_Id__lead_collect_Emp_id=emp)
         
        dataBank_count = dataBank_objs.count()
            
        if pgnum:
            pgnum = int(pgnum)
            dataBank_objs = dataBank_objs[:pgnum]

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'employees':employees,
                   'executives':executives,
                   'notifications':notifications,
                   'dataBank_count':dataBank_count,'dataBank_objs':dataBank_objs,
                   'selected_emp':selected_emp,'d1':d1,'d2':d2,'pg_num':pgnum}
        
    return render(request,'DAM_dashboard_allocation.html',content)


def DMA_allocate_lead(request):

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

            leads_check = request.POST.getlist('lead_check')
            selected_emp = request.POST['selected_emp']
            emp = EmployeeRegister_Details.objects.get(id=selected_emp)
            count = 0
         
            for l in leads_check:
                db = DataBank.objects.get(id=int(l))
                db.lead_allocate_status = 1
                db.used_count += 1
                db.allocated_date = date.today()
                
                db.lead_status = 'Allocated' 
                db.save()
                count = count + 1

                ld_obj = Leads_assignto_tc()
                ld_obj.dataBank_ID = db
                ld_obj.leadId = db.lead_Id
                ld_obj.TC_Id = EmployeeRegister_Details.objects.get(id=selected_emp)
                ld_obj.client_id = db.lead_Id.lead_work_regId.clientId
                ld_obj.Assign_Date =  date.today()
                ld_obj.Allocate_time = datetime.datetime.now().time()
                ld_obj.save()

                fh_obj = FollowupHistory()
                fh_obj.hs_lead_Id = db.lead_Id
                fh_obj.hr_telecaller_Id =  EmployeeRegister_Details.objects.get(id=selected_emp)
                fh_obj.allocated_date = date.today()
                fh_obj.note ='Lead allocated'
                fh_obj.final_status='Allocated'
                fh_obj.hs_comp_Id = db.lead_Id.lead_work_regId.clientId.compId
                fh_obj.save()

            success_text = str(count) + ' lead allocated to ' + str(emp.emp_name) + ' successfully.'
            messages.success(request, success_text)
        
        return redirect('DAM_Dashboard_allocation')



           


def DAM_allAllocationList(request):   
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4) | Q(emp_designation_id__dashboard_id=5))
        
        if request.POST:
            sdate = request.POST['fdate']
            edate = request.POST['edate']

            sdate = timezone.datetime.strptime(sdate, "%Y-%m-%d").date()
            edate = timezone.datetime.strptime(edate, "%Y-%m-%d").date()

            allocations = Leads_assignto_tc.objects\
                .filter(Assign_Date__range=[sdate, edate],client_id__compId__id=dash_details.emp_comp_id.id).values('Assign_Date')\
                .annotate(count=Count('id'))\
                .order_by('-Assign_Date')
            allocations_result = Leads_assignto_tc.objects.filter(Assign_Date__range=[sdate, edate],client_id__compId__id=dash_details.emp_comp_id.id)
            dataBank_count = Leads_assignto_tc.objects.filter(Assign_Date__range=[sdate, edate],client_id__compId__id=dash_details.emp_comp_id.id).count()

        else:
            allocations = Leads_assignto_tc.objects.values('Assign_Date') \
            .annotate(count=Count('id')) \
            .filter(client_id__compId__id=dash_details.emp_comp_id.id) \
            .order_by('-Assign_Date')

            allocations_result = Leads_assignto_tc.objects.filter(client_id__compId__id=dash_details.emp_comp_id.id)
            dataBank_count = Leads_assignto_tc.objects.filter(client_id__compId__id=dash_details.emp_comp_id.id).count()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'allocations':allocations,
                   'notifications':notifications,
                   'employees':employees,
                   'allocations_result':allocations_result,
                   'dataBank_count':dataBank_count
                   }
        
    return render(request,'DAM_dashboard_allocationList.html',content)


def fetch_lead_allocate_exe(request):
    try:
    
        Emp_id = request.GET.get('emp_id', None)
    

        if Emp_id is not None:
           
            allocations_result = Leads_assignto_tc.objects.filter(TC_Id__id=Emp_id)
            dataBank_count = Leads_assignto_tc.objects.filter(TC_Id__id=Emp_id).count()
            data_list = []
           

            for lead in allocations_result:
                data = {
                'lead_status':lead.Response,
                'Genarated_date':lead.Assign_Date,
                'lead_name':lead.leadId.lead_name,
                'client_name':lead.client_id.client_name,
                'lead_collection_for':lead.leadId.lead_category_id.lead_collection_for,
                'emp_name': lead.TC_Id.emp_name,
               
                }
                data_list.append(data)

            success = True
            message = "Operation successful"

            

          
            return JsonResponse({'success': success, 'message': message,'dataBank_count':dataBank_count,'leads_data': data_list})
        else:
           
            raise ValueError("Client ID is not provided in the request.")

    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})


def DAM_allocated_listBydate(request,date_data):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4) | Q(emp_designation_id__dashboard_id=5))
        
        allocations = Leads_assignto_tc.objects.filter(client_id__compId__id=dash_details.emp_comp_id.id) \
        .values('Assign_Date') \
        .annotate(count=Count('id')) \
        .order_by('-Assign_Date')



        allocations_result = Leads_assignto_tc.objects.filter(Assign_Date=date_data,client_id__compId__id=dash_details.emp_comp_id.id)
        dataBank_count = Leads_assignto_tc.objects.filter(Assign_Date=date_data,client_id__compId__id=dash_details.emp_comp_id.id).count()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'allocations':allocations,
                   'notifications':notifications,
                   'employees':employees,
                   'allocations_result':allocations_result,
                   'dataBank_count':dataBank_count
                   }
        
    return render(request,'DAM_dashboard_allocationList.html',content)



def fetch_leads_status_change(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        status_change = request.GET.get('status_change', None)

      
        dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status=status_change )
        dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status=status_change).count()
        
        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4))
        executives = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=3) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=1) )
        
        countList = []

        for e in executives:
            countNo = DataBank.objects.filter(lead_Id__lead_collect_Emp_id=e,lead_allocate_status=0).count()
            empName = e.emp_name
            countList.append({empName: countNo})
        
        content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'employees':employees,
                        'executives':executives,
                        'notifications':notifications,
                        'dataBank_count':dataBank_count,'dataBank_objs':dataBank_objs,'countList':countList}
        
                
        return render(request,'DAM_dashboard_allocation.html',content)


def fetch_leads_executive_change(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        exe_change = request.GET.get('exe_change', None)
        
        selected_employee = EmployeeRegister_Details.objects.get(id=exe_change)
      
        dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_Id__lead_collect_Emp_id__id=exe_change,lead_allocate_status=0 )
        dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_Id__lead_collect_Emp_id__id=exe_change,lead_allocate_status=0).count()
        
        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4))
        executives = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=3) | Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=1))

        countList = []

        for e in executives:
            countNo = DataBank.objects.filter(lead_Id__lead_collect_Emp_id=e,lead_allocate_status=0).count()
            empName = e.emp_name
            countList.append({empName: countNo})

        content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'selected_employee':selected_employee,
                        'employees':employees,
                        'executives':executives,
                        'notifications':notifications,
                        'dataBank_count':dataBank_count,'dataBank_objs':dataBank_objs,'countList':countList}
        
                
        return render(request,'DAM_dashboard_allocation.html',content)

#===========================================================


def DAM_Dashboard_clients(request):
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
        
        if request.POST:
            
            ctgID = request.POST['categoryid']
            dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_Id__lead_category_id__id=ctgID)
            dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_Id__lead_category_id__id=ctgID).count()
        else:
            dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,)
            dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,).count()
            

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'clients_objs':clients_objs,
                   'notifications':notifications,
                   'dataBank_count':dataBank_count,'dataBank_objs':dataBank_objs}
        
    return render(request,'DAM_dashboard_clients.html',content)



# Data Manager Notification Management Section 

def DAM_notification_section(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        dataBank_newcount =  DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,Genarated_date=date.today()).count()
        dataBank_followup_count = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,followup_date=date.today()).count()
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'dataBank_newcount':dataBank_newcount,
                   'dataBank_followup_count':dataBank_followup_count,
                   'notifications':notifications}
    return render(request,'DAM_notificationSection.html',content)


def DAM_Dashboard_notification_tody_newLead(request):    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,Genarated_date=date.today())
        dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,Genarated_date=date.today()).count()

        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)

        source_objs = PlatForms.objects.filter(company_Id__id=dash_details.emp_comp_id.id)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_objs':dataBank_objs,
                   'dataBank_count':dataBank_count,
                   'clients_objs':clients_objs,'source_objs':source_objs}
        
    return render(request,'DAM_Dashboard_notification_NewLead.html',content)         


def DAM_Dashboard_todayAllocation(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        dataBank_objs = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,allocated_date=date.today())
        dataBank_count = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,allocated_date=date.today()).count()

        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4) | Q(emp_designation_id__dashboard_id=5))
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_objs':dataBank_objs,
                   'dataBank_count':dataBank_count,
                   'employees':employees,}
        
    return render(request,'DAM_Dashboard_notification_allocation.html',content)  


def Notification_fetch_leads_status_change(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        status_change = request.GET.get('status_change', None)

      
        dataBank_objs = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status=status_change )
        dataBank_count = DataBank.objects.filter(lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,lead_status=status_change).count()
        
        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4) | Q(emp_designation_id__dashboard_id=5))

        content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'employees':employees,
                        'notifications':notifications,
                        'dataBank_count':dataBank_count,'dataBank_objs':dataBank_objs}
        
                
        return render(request,'DAM_Dashboard_notification_allocation.html',content)


def DAM_Dashboard_todayFollowups(request):

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
            selected_emp = request.POST['selected_emp']
            allcate_obj = Leads_assignto_tc.objects.filter(TC_Id__id=selected_emp).values('dataBank_ID__id')
            dataBank_objs = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,followup_date=date.today(),id__in=allcate_obj)
            dataBank_count = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,followup_date=date.today(),id__in=allcate_obj).count()

        else:
            dataBank_objs = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,followup_date=date.today())
            dataBank_count = DataBank.objects.filter(lead_allocate_status=1,lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,followup_date=date.today()).count()

        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=4) | Q(emp_designation_id__dashboard_id=5))
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_objs':dataBank_objs,
                   'dataBank_count':dataBank_count,
                   'employees':employees,}
        
    return render(request,'DAM_Dashboard_notification_followups.html',content)  



# Follow up Section-------------------------

def DAM_Dashboard_followups(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4)

        dataBank_objs = Leads_assignto_tc.objects.filter(dataBank_ID__lead_Id__lead_work_regId__wcompId__id=dash_details.emp_comp_id.id,dataBank_ID__lead_allocate_status=1 )
        dataBank_objs = dataBank_objs.order_by('-Assign_Date')

        d1 = None
        d2 = None
        select_emp = None
        status_val = None
        pgnum = 30

        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            hr_id = request.POST['hr_id']
            status_val =  request.POST['status_val']
            pgnum = request.POST['pgnum']

            if d1:
                dataBank_objs = dataBank_objs.filter(Assign_Date__gte=d1)
            if d2:
                dataBank_objs = dataBank_objs.filter(Assign_Date__lte=d2)

            if hr_id:
                select_emp = EmployeeRegister_Details.objects.get(id=hr_id)
                dataBank_objs = dataBank_objs.filter(TC_Id__id=hr_id)

            if status_val:
                dataBank_objs = dataBank_objs.filter(dataBank_ID__lead_status=status_val)

        dataBank_count = dataBank_objs.count()
            
        if pgnum:
            pgnum = int(pgnum)
            dataBank_objs = dataBank_objs[:pgnum]


        follow_obj = FollowupStatus.objects.filter(company_Id__id=dash_details.emp_comp_id.id)

        content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'employees':employees,
                        'notifications':notifications,
                        'follow_obj':follow_obj,
                        'dataBank_count':dataBank_count,'dataBank_objs':dataBank_objs,
                        'd1':d1,'d2':d2,'select_emp':select_emp,'pg_num':pgnum,'status_val':status_val}
        
                
        return render(request,'DAM_Dashboard_followup.html',content)


def DAM_assign_remove(request,lassignID):

    if request.POST:

        lead_list = request.POST.getlist('allocated_check')

        for l in lead_list:
            try:
                leadAssign_objs = Leads_assignto_tc.objects.get(id=l)
                
                db_obj=DataBank.objects.get(id=leadAssign_objs.dataBank_ID.id)
                db_obj.lead_status='Not Attended'
                db_obj.save()

                leadAssign_objs.delete()
                
            except Leads.DoesNotExist:
                messages.info(request, f'{leadAssign_objs.leadId.lead_name} Lead record Not Found')

        return redirect('DAM_Dashboard_followups')
    
    else:

        try:
            leadAssign_objs = Leads_assignto_tc.objects.get(id=lassignID)
            
            db_obj=DataBank.objects.get(id=leadAssign_objs.dataBank_ID.id)
            db_obj.lead_status='Not Attended'
            db_obj.save()

            leadAssign_objs.delete()

            messages.error(request, f'{leadAssign_objs.leadId.lead_name} Lead Removed.')
        except Leads.DoesNotExist:
            messages.info(request, f'{leadAssign_objs.leadId.lead_name} Lead record Not Found')
        return redirect('DAM_Dashboard_followups')


    
    

#==============================================================

# Dashboard Executives ---------------------

def DAM_Dashboard_Executive(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

       

        employees = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4)
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   
                   'employees':employees,}
        
    return render(request,'DAM_Dashboard_Executive.html',content)  


def DAM_employee_allocated_leads(request,empID):


    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        db_Id_queryset = Leads_assignto_tc.objects.filter(TC_Id__id=empID)
        dataBank_ids = [obj.dataBank_ID.id for obj in db_Id_queryset]

        if request.POST:

            d1 = request.POST.get('fdate', None)
            d2 = request.POST.get('edate', None)
            statusChange = request.POST['Status_change']
            print(statusChange)

            if (d1) and (d2) and (statusChange != 0):
            
                dataBank_objs = DataBank.objects.filter(id__in=dataBank_ids,allocated_date__gte=d1,allocated_date__lte=d2,lead_status=statusChange)  
                dataBank_count = DataBank.objects.filter(id__in=dataBank_ids,allocated_date__gte=d1,allocated_date__lte=d2,lead_status=statusChange).count() 

            elif (d1) and (d2) and (statusChange == 0):
            
                dataBank_objs = DataBank.objects.filter(id__in=dataBank_ids,allocated_date__gte=d1,allocated_date__lte=d2)  
                dataBank_count = DataBank.objects.filter(id__in=dataBank_ids,allocated_date__gte=d1,allocated_date__lte=d2).count()   

            elif statusChange != 0:
            
                dataBank_objs = DataBank.objects.filter(id__in=dataBank_ids,lead_status=statusChange)  
                dataBank_count = DataBank.objects.filter(id__in=dataBank_ids,lead_status=statusChange).count() 
            else:
                dataBank_objs = DataBank.objects.filter(id__in=dataBank_ids)  
                dataBank_count = DataBank.objects.filter(id__in=dataBank_ids).count()     
        else:

            dataBank_objs = DataBank.objects.filter(id__in=dataBank_ids)  
            dataBank_count = DataBank.objects.filter(id__in=dataBank_ids).count()     

    
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'dataBank_objs':dataBank_objs,
                   'dataBank_count':dataBank_count,
                   'empID':empID,}
        
        return render(request,'DAM_Dashboard_Executive_Allocated_leads.html',content) 



#Side Navbar links -------------------------

def DAM_employees_hr_tel(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_designation_id__dashboard_id=4,emp_active_status=1)
       

       
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'employees':employees
                    }
        
    return render(request,'DAM_employees.html',content)


def DAM_employees_exe(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

       
        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=2) | Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,emp_active_status=1)


        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'employees':employees
                    }
        
    return render(request,'DAM_employees.html',content)


def DAM_employess_details(request,empDeatilsID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        emp_obj = EmployeeRegister_Details.objects.get(id=empDeatilsID) 

        cid = 2
        
        if emp_obj.emp_designation_id.dashboard_id == 3: 
            
            cid = 0

        if emp_obj.emp_designation_id.dashboard_id == 4 :

            cid = 1

        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'emp_obj':emp_obj,'cid':cid}

        return render(request,'DAM_emp_details.html',content)

    else:
            return redirect('/')


#Password Section ---------------

def DAM_password(request):
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

        return render(request,'DAM_password.html',content)

    else:
            return redirect('/')

def DAM_passwordUpdate(request):

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

        return render(request,'DAM_password.html',content)

    else:
            return redirect('/')

# Profile Page -------------------------

def DAM_profile(request):  
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

        return render(request,'DAM_profile.html',content)

    else:
            return redirect('/')


def DAM_profile_detailsUpdate(request):
     
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

        return render(request,'DAM_profile.html',content)

    else:
            return redirect('/')
    
# ============================================================================






# Data Manager Executive Dashboard 

def DAM_executive_dashboard(request):
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
    return render(request,'DAM_executiveDashboard.html',content)


def DAM_client_newleads(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)

        lead_data = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__in=clients_obj.values('client_Id')
                                            ,lead_allocate_status=0,Genarated_date=date.today()
        ).values('lead_Id__lead_work_regId__clientId').annotate(count=Count('lead_Id'))

    
       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'lead_data':lead_data,'clients_obj':clients_obj}
    return render(request,'DAM_clientNew_lead.html',content)


def DAM_client_lists_newLeads(request,clID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        lead_data = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=clID
                                            ,lead_allocate_status=0,Genarated_date=date.today())
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'lead_data':lead_data}
        
    return render(request,'DAM_clientNew_lead_list.html',content)

#---------------------------------------------------------

def DAM_executive_lead(request):
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
    return render(request,'DAM_executive_lead.html',content)


def DAM_executive_collected_leads(request,eID):
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
    return render(request,'DAM_executive_lead_list.html',content)



#--------------------------------------------------------


def DAM_all_clientleads(request):
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
    return render(request,'DAM_clientAll_lead.html',content)


def DAM_client_lists_allLeads(request,cID):
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
    return render(request,'DAM_clientAll_lead_list.html',content)


# Data Manager Allocation Dashoard 

def DAM_allocation_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        pending_lead = DataBank.objects.filter(lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,lead_allocate_status=0).count()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'pending_lead':pending_lead}
    return render(request,'DAM_allocationDashboard.html',content)


def DAM_allocated_leads(request):

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
            start_date = request.POST['sdate']
            end_date = request.POST['edate']

            allocated_lead = DataBank.objects.filter(
                    lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,
                    lead_allocate_status=1,allocated_date__gte=start_date,allocated_date__lte=end_date,
                ).values('allocated_date').annotate(count=Count('allocated_date')).order_by('-allocated_date')

        
        else:
            allocated_lead = DataBank.objects.filter(
                    lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,
                    lead_allocate_status=1
                ).values('allocated_date').annotate(count=Count('allocated_date')).order_by('-allocated_date')



        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'allocated_lead':allocated_lead,
                   }
    return render(request,'DAM_allocatedLead.html',content)


def DAM_allocatedlead_byDate(request, allocatedDate):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        DATE_leadS = DataBank.objects.filter(lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,allocated_date=allocatedDate)
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'DATE_leadS':DATE_leadS}
        
    return render(request,'DAM_allocatedByDate.html',content)


    
def DAM_pendingleads(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        pending_leads = DataBank.objects.filter(
                    lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,
                    lead_allocate_status=0)
        
       

        clients_obj = ClientTask_Register.objects.filter(task_name='Lead Collection',client_Id__in=pending_leads.values('lead_Id__lead_work_regId__clientId__id'))
       
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   
                   'clients_obj':clients_obj}
    return render(request,'DAM_allocationPending.html',content)


def DAM_client_pendingLeads(request,cID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=3) | Q(emp_designation_id__dashboard_id=5))

        lc_obj = LeadCategory_Register.objects.filter(cTaskId__client_Id=cID)

        leads_obj = DataBank.objects.filter(lead_Id__lead_category_id__in=lc_obj,lead_allocate_status=0)

        data_box = {}

        total = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID).count()
        allocate = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID,lead_allocate_status=1).count()
        pending = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID,lead_allocate_status=0).count()

        data_box['Total Leads'] = [total, allocate, pending]

        for lc in lc_obj:
           
            total = DataBank.objects.filter(lead_Id__lead_category_id__id=lc.id).count()
            allocate = DataBank.objects.filter(lead_Id__lead_category_id__id=lc.id,lead_allocate_status=1).count()
            pending = DataBank.objects.filter(lead_Id__lead_category_id__id=lc.id,lead_allocate_status=0).count()

            data_box[lc.lead_collection_for] = [total, allocate, pending]
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'leads_obj':leads_obj,
                   'notifications':notifications,
                   'lc_obj':lc_obj,
                   'data_box':data_box,
                   'employees':employees}
    return render(request,'DAM_clientPendingLeads.html',content)



def DAM_client_category_pendingLeads(request,lCID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=3) | Q(emp_designation_id__dashboard_id=5))

        lc = LeadCategory_Register.objects.get(id=lCID)

        cID = lc.cTaskId.client_Id.id

        lc_obj = LeadCategory_Register.objects.filter(cTaskId__client_Id=cID)

        leads_obj = DataBank.objects.filter(lead_Id__lead_category_id=lCID,lead_allocate_status=0)

        data_box = {}

        total = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID).count()
        allocate = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID,lead_allocate_status=1).count()
        pending = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID,lead_allocate_status=0).count()

        data_box['Total Leads'] = [total, allocate, pending]

        for lc in lc_obj:
           
            total = DataBank.objects.filter(lead_Id__lead_category_id__id=lc.id).count()
            allocate = DataBank.objects.filter(lead_Id__lead_category_id__id=lc.id,lead_allocate_status=1).count()
            pending = DataBank.objects.filter(lead_Id__lead_category_id__id=lc.id,lead_allocate_status=0).count()

            data_box[lc.lead_collection_for] = [total, allocate, pending]

        viewdiv= True
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'leads_obj':leads_obj,
                   'notifications':notifications,
                   'lc_obj':lc_obj,
                   'viewdiv':viewdiv,
                   'data_box':data_box,
                   'employees':employees}
    return render(request,'DAM_clientPendingLeads.html',content)





def DAM_clientsleads(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        pending_leads = DataBank.objects.filter(
                    lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,
                    lead_allocate_status=0)
        
       

        clients_obj = ClientTask_Register.objects.filter(task_name='Lead Collection',client_Id__in=pending_leads.values('lead_Id__lead_work_regId__clientId__id'))

        data_box= {}

        for cl in clients_obj:

            cID = cl.client_Id.id
           
            total = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID).count()
            allocate = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID,lead_allocate_status=1).count()
            pending = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=cID,lead_allocate_status=0).count()

            data_box[cl] = [pending, allocate, total]

        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'data_box':data_box}
    return render(request,'DAM_clientsLead.html',content)



# Data Manager Telecaller Dashboard ---------------------------

def DAM_telecallers_dashboard(request):
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
    return render(request,'DAM_telecallerDashboard.html',content)


def DAM_followup_leads(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        client_obj = ClientTask_Register.objects.filter(cTcompId__id=dash_details.emp_comp_id.id,task_name='Lead Collection')

        data_bank_obj = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__compId__id=dash_details.emp_comp_id.id,lead_allocate_status=1)

        emp_obj = EmployeeRegister_Details.objects.filter(emp_comp_id__id=dash_details.emp_comp_id.id,emp_designation_id__dashboard_id=4)

        follow_obj = FollowupStatus.objects.filter(company_Id__id=dash_details.emp_comp_id.id)
     
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'client_obj':client_obj,
                   'emp_obj':emp_obj,
                   'follow_obj':follow_obj,
                   'data_bank_obj':data_bank_obj
                   
                   }
        
    return render(request,'DAM_followupleads.html',content)


def followup_view(request):
    lead_id = request.GET.get('leadId', None)
   
    try:
        db_obj = DataBank.objects.get(id=lead_id)

 
        ld_obj = lead_Details.objects.filter(leadId__id=db_obj.lead_Id.id)
        lead_data = [{'fname': lead.lead_field_name, 'data_val': lead.lead_field_data} for lead in ld_obj]

        ld_followup_details = FollowupDetails.objects.filter(lead_Id__id=db_obj.lead_Id.id)
        leadfollowup_details = [{'rdate': lead.response_date, 'rsp': lead.response, 'status':lead.response_status, 'ndate': lead.nextfollowup_date} for lead in ld_followup_details]

        
        ld_followup_history = FollowupHistory.objects.filter(hs_lead_Id__id=db_obj.lead_Id.id)
        lead_followup_history = [{'aldate': lead.allocated_date, 'name': lead.hr_telecaller_Id.emp_name, 'status':lead.final_status, 'note': lead.note} for lead in ld_followup_history]

        success = True
        message = "Operation successful"

        # Return a JSON response
        return JsonResponse({'success': success, 'message': message,'lead_data': lead_data,'leadfollowup_details':leadfollowup_details,'lead_followup_history':lead_followup_history})

    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})



def fetch_lead_categories(request):
    try:
        # Retrieve client ID from query parameters
        client_id = request.GET.get('client_id', None)
       

        if client_id is not None:
        
            lead_categories = LeadCategory_Register.objects.filter(cTaskId__client_Id__id=client_id)
           
            lead_categories_list = [{'id': category.id, 'name': category.lead_collection_for} for category in lead_categories]

            DB_data = DataBank.objects.filter(lead_Id__lead_work_regId__clientId__id=client_id)
            dataBank_count =DB_data.count()
            
            success = True
            message = "Operation successful"

            return JsonResponse({'success': success, 'message': message,'lead_categories': lead_categories_list})
        else:
          
            raise ValueError("Client ID is not provided in the request.")

    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})


def fetch_executive_leads(request):
    try:
        categoryid = request.GET.get('selectedlcId', None)
        empid = request.GET.get('selectedempId', None)

       
        if empid is not None:
           

            DB_data = DataBank.objects.filter(lead_Id__lead_collect_Emp_id__id=empid,lead_Id__lead_category_id__id=categoryid)
            dataBank_count = DataBank.objects.filter(lead_Id__lead_collect_Emp_id__id=empid,lead_Id__lead_category_id__id=categoryid).count()
            
            data_list = []
           
            for lead in DB_data:
                
                data = {
              
                'lead_status':lead.lead_status,
                'Genarated_date': lead.Genarated_date,
                'lead_name': lead.lead_Id.lead_name,
                'lead_email': lead.lead_Id.lead_email,
                'lead_contact': lead.lead_Id.lead_contact,
                'id': lead.id,
                'lead_source':lead.lead_Id.lead_source,
                'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                'c_status': lead.current_status,
                }
                data_list.append(data)

            success = True
            message = "Operation successful"



            # Return a JSON response with lead categories
            return JsonResponse({'success': success, 'message': message, 'leads_data': data_list,'dataBank_count':dataBank_count})
        else:
            # Handle the case where client_id is not provided
            raise ValueError("Category ID is not provided in the request.")

    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})


def fetch_employee_allocated_leads(request):

    try:
        # Retrieve client ID from query parameters
        clientid = request.GET.get('client_id', None)
        categoryid = request.GET.get('cateory_id', None)
        empid = request.GET.get('emp_id', None)

       
    
        if empid is not None    :
            lda = Leads_assignto_tc.objects.filter(TC_Id__id=empid)
            leadsId = lda.values_list('leadId__id', flat=True)
            DB_data = DataBank.objects.filter(Q(lead_Id__lead_category_id__id=categoryid,lead_Id__lead_work_regId__clientId__id=clientid)).filter(lead_allocate_status=1,lead_Id__in=leadsId)

    
        else:
            DB_data = DataBank.objects.filter(Q(lead_Id__lead_category_id__id=categoryid) | Q(lead_Id__lead_work_regId__clientId__id=clientid)).filter(lead_allocate_status=1)
                
         
        data_list = []
        print('Data: -',DB_data)
        for lead in DB_data:
                
                data = {
                'lead_status':lead.lead_status,
                'Genarated_date': lead.Genarated_date,
                'lead_name': lead.lead_Id.lead_name,
                'lead_email': lead.lead_Id.lead_email,
                'lead_contact': lead.lead_Id.lead_contact,
                'id': lead.id,
                'lead_source':lead.lead_Id.lead_source,
                'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                'c_status': lead.current_status,
                }
                data_list.append(data)

        success = True
        message = "Operation successful"




            # Return a JSON response with lead categories
        return JsonResponse({'success': success, 'message': message, 'leads_data': data_list})
       
    except Exception as e:
        # Handle exceptions and return a JSON response indicating failure
        return JsonResponse({'success': False, 'message': str(e)})



def DAM_followup_save(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        if request.POST:

            fus = FollowupStatus()
            fus.status_name = request.POST['fw_status']
            fus.company_Id = dash_details.emp_comp_id
            fus.save()
            return redirect('DAM_Dashboard_followups')


def DAM_followup_delete(request,fID):

    fus = FollowupStatus.objects.get(id=fID)    
    fus.delete()
    return redirect('DAM_followup_leads')



# Data Manager Platform Management---------------------------

def DAM_platform_management(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        platform_data = PlatForms.objects.filter(company_Id=dash_details.emp_comp_id)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'platform_data':platform_data}
        
    return render(request,'DAM_platform_management.html',content)


def DAM_platform_add(request):
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

            paltform_obj = PlatForms()
            paltform_obj.platform_Name = request.POST['platform_name']
            paltform_obj.company_Id = dash_details.emp_comp_id
            paltform_obj.save()

            platform_data = PlatForms.objects.filter(company_Id=dash_details.emp_comp_id)

            success = True
            success_text = 'New Platform add successfuly.'
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success':success,
                   'success_text':success_text,
                   'platform_data':platform_data
                   }
        
    return render(request,'DAM_platform_management.html',content)


def DAM_platform_leads(request,pID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        platform_data = PlatForms.objects.get(id=pID)

        if request.POST:

            sdate = request.POST['sDate']
            edate = request.POST['eDate']
            dataBank_objs = DataBank.objects.filter(lead_Id__lead_source=platform_data.platform_Name,lead_Id__lead_add_date__gte=sdate,lead_Id__lead_add_date__lte=edate)
            dataBank_objs_count = DataBank.objects.filter(lead_Id__lead_source=platform_data.platform_Name,lead_Id__lead_add_date__gte=sdate,lead_Id__lead_add_date__lte=edate).count()
            
        else:
            dataBank_objs = DataBank.objects.filter(lead_Id__lead_source=platform_data.platform_Name)
            dataBank_objs_count = DataBank.objects.filter(lead_Id__lead_source=platform_data.platform_Name).count()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'platform_data':platform_data,
                   'dataBank_objs':dataBank_objs,
                   'dataBank_objs_count':dataBank_objs_count,
                   }
        
    return render(request,'DAM_platform_leads.html',content)


def DAM_platform_Report(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        platform_data = PlatForms.objects.filter(company_Id=dash_details.emp_comp_id)
        platform_data_sum = PlatForms.objects.filter(company_Id=dash_details.emp_comp_id).aggregate(Sum('platform_TotalCount'))['platform_TotalCount__sum']

        platform_data_count = PlatForms.objects.filter(company_Id=dash_details.emp_comp_id).count()

        if request.POST:
            sdate= request.POST['fDate']
            edate = request.POST['eDate']
            
            pfd_objs = PlatFormsData.objects.filter(Pfd_company_Id=dash_details.emp_comp_id,data_add_date__gte=sdate,data_add_date__lte=edate).order_by('-data_add_date')
        else:

            pfd_objs = PlatFormsData.objects.filter(Pfd_company_Id=dash_details.emp_comp_id).order_by('-data_add_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'platform_data_count':platform_data_count,
                   'platform_data_sum':platform_data_sum,
                   'pfd_objs':pfd_objs,
                   'platform_data':platform_data}
        
    return render(request,'DAM_platform_report.html',content)



# Data Manager Waste Data Management 

def DAM_wasteData_management(request):
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
    return render(request,'DAM_wastdata.html',content)


def DAM_waste_data_confirm(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        hr_objs = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_designation_id__dashboard_id=4,emp_active_status=1)
        
        lead_waste = Waste_Leads.objects.filter(client_id__compId=dash_details.emp_comp_id,Status=0).order_by('-waste_marked_Date')

        d1 = None
        d2 = None
        hr = None
        selected_hr = None
        status_val = None


        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            hr = request.POST['hr_id']
            status_val = request.POST['status']

            if d1:
                lead_waste = lead_waste.filter(waste_marked_Date__gte=d1)

            if d2:
                lead_waste = lead_waste.filter(waste_marked_Date__lte=d2)

            if hr:
                selected_hr = EmployeeRegister_Details.objects.get(id=hr)
                lead_waste = lead_waste.filter(TC_Id__id=hr)

            if status_val:
                lead_waste = lead_waste.filter(confirmation=status_val)


        lead_waste_count = lead_waste.count()       
       
        # if not lead_waste.exists():
        #     return redirect('DAM_wasteData_management')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'lead_waste':lead_waste,
                   'notifications':notifications,
                   'hr_objs':hr_objs,'d1':d1,'d2':d2,'hr':hr,'status_val':status_val,'selected_hr':selected_hr,
                   'lead_waste_count':lead_waste_count}
        
        return render(request,'DAM_watedata_Confirm.html',content)
    

def DAM_waste_dateApprove(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

    if request.POST:

        lead_id = request.POST.get('lead_id')
        hr = request.POST.get('hr')
        d1 = request.POST.get('sdate')
        d2 = request.POST.get('edate')
        status_val = request.POST.get('status_val')
        
        
        waste = Waste_Leads.objects.get(id=lead_id)

        if waste.confirmation == 1:
            waste.Status = 1
            waste.save()

            lead_obj = Leads.objects.get(id=waste.leadId.id)
            lead_obj.waste_data = 1
            
            if waste.assignto_tc_id:
                lead_obj.waste_data_reason = waste.assignto_tc_id.TC_Id.emp_name + '( ' +  str(waste.waste_marked_Date)  +' )' + ' :- ' +  waste.reason 
            else:
                lead_obj.waste_data_reason =  str(waste.waste_marked_Date) + ' :- ' + waste.reason

            lead_obj.save()

            assign_obj = Leads_assignto_tc.objects.get(id=waste.assignto_tc_id.id)
            assign_obj.Status = 2
            assign_obj.save()

            db = DataBank.objects.get(lead_Id__id=waste.leadId.id)
            db.current_status = 'Marked as Waste'
            db.lead_status = 'Closed'
            db.save 

            fh = FollowupHistory()
            fh.hs_lead_Id=waste.leadId
            fh.note = 'Lead marked as waste'
            fh.allocated_date = date.today()
            fh.hr_telecaller_Id = waste.TC_Id
            fh.hs_comp_Id=dash_details.emp_comp_id
            fh.final_status = 'Marked as Waste'
            fh.save()


            # Waste Data notification----

            emp_obj = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=1)

            for emp in emp_obj:

                notific_obj = Notification()
                notific_obj.emp_id = emp
                notific_obj.notific_head ='New waste Lead added.'
                notific_obj.notific_content = (
                    dash_details.emp_name +
                    ' ( ' +
                    dash_details.emp_designation_id.desig_name +
                    ' ) ' +
                    ' has marked the lead ' +
                    waste.leadId.lead_name +
                    ' ( ' +
                    waste.leadId.lead_category_id.lead_collection_for +
                ' ) as a waste lead.'
                )

                notific_obj.notific_time = timezone

                notific_obj.save()

            lead_waste = Waste_Leads.objects.filter(client_id__compId__id=dash_details.emp_comp_id.id,Status=0).order_by('-waste_marked_Date')

            if d1:
                lead_waste = lead_waste.filter(waste_marked_Date__gte=d1)

            if d2:
                lead_waste = lead_waste.filter(waste_marked_Date__lte=d2)

            if hr:
                lead_waste = lead_waste.filter(TC_Id__id=hr)

            if status_val:
                lead_waste = lead_waste.filter(confirmation=status_val)
            
            lead_waste_count = lead_waste.count()     

            content = {'lead_waste':lead_waste}

            table_content = render_to_string('table_waste_content.html', content, request=request)

            return JsonResponse({
                'lead_waste_count': lead_waste_count,
                'table_content': table_content
            })
        
        

        else:
           return JsonResponse({'status': 'Confirmation Missing'})   
    else:
        return JsonResponse({'status': 'error'}, status=400)   
                 


def DAM_waste_dateCancel(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        if request.POST:

            lead_id = request.POST.get('lead_id')
            hr = request.POST.get('hr')
            d1 = request.POST.get('sdate')
            d2 = request.POST.get('edate')
            status_val = request.POST.get('status_val')
            
            waste = Waste_Leads.objects.get(id=lead_id)
            data=Leads_assignto_tc.objects.get(id=waste.assignto_tc_id.id)
            data.Response='Not Waste'
            data.save()

            FBH = FollowupHistory()
            FBH.hs_lead_Id= waste.leadId
            FBH.hs_comp_Id= dash_details.emp_comp_id
            FBH.hr_telecaller_Id= waste.TC_Id

            FBH.allocated_date = date.today()
            FBH.note = 'Changed the status Marked as waste to Not a waste '
            FBH.final_status = 'Not Waste'
            FBH.save()

            waste.delete()

            lead_waste = Waste_Leads.objects.filter(client_id__compId__id=dash_details.emp_comp_id.id,Status=0).order_by('-waste_marked_Date')
            
            if d1:
                lead_waste = lead_waste.filter(waste_marked_Date__gte=d1)

            if d2:
                lead_waste = lead_waste.filter(waste_marked_Date__lte=d2)

            if hr:
                lead_waste = lead_waste.filter(TC_Id__id=hr)

            if status_val:
                lead_waste = lead_waste.filter(confirmation=status_val)
            
            lead_waste_count = lead_waste.count()     

            content = {'lead_waste':lead_waste}

            table_content = render_to_string('table_waste_content.html', content, request=request)

            return JsonResponse({
                'lead_waste_count': lead_waste_count,
                'table_content': table_content
            })
    
        else:
            return JsonResponse({'status': 'error'}, status=400)   



def DAM_Approved_waste_data(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        hr_objs = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_designation_id__dashboard_id=4,emp_active_status=1)
        
        lead_waste = Waste_Leads.objects.filter(client_id__compId__id=dash_details.emp_comp_id.id,Status=1)
        
        d1 = None
        d2 = None
        hr = None
        selected_hr = None
       


        if request.POST:

            d1 = request.POST['sdate']
            d2 = request.POST['edate']
            hr = request.POST['hr_id']
           

            if d1:
                lead_waste = lead_waste.filter(waste_marked_Date__gte=d1)

            if d2:
                lead_waste = lead_waste.filter(waste_marked_Date__lte=d2)

            if hr:
                selected_hr = EmployeeRegister_Details.objects.get(id=hr)
                lead_waste = lead_waste.filter(TC_Id__id=hr)

        lead_waste_count = lead_waste.count()   

            
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'lead_waste':lead_waste,
                    'lead_waste_count':lead_waste_count,
                    'hr_objs':hr_objs,'d1':d1,'d2':d2,'hr':hr,'selected_hr':selected_hr,
                    'notifications':notifications}
            
        return render(request,'DAM_watedata_list.html',content)



def DAM_client_waste_data(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        lead_task_clients = ClientTask_Register.objects.filter(task_name='Lead Collection')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'lead_task_clients':lead_task_clients,
                   'notifications':notifications}
        
    return render(request,'DAM_clientwatedata.html',content)


def DAM_exicutive_waste_data(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        exe_obj = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=3)|Q(emp_designation_id__dashboard_id=2),emp_comp_id=dash_details.emp_comp_id,)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'exe_obj':exe_obj,
                   'notifications':notifications}
        
    return render(request,'DAM_executivewatedata.html',content)


def DAM_hr_telecaller_waste_data(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        exe_obj = EmployeeRegister_Details.objects.filter(Q(emp_designation_id__dashboard_id=5)|Q(emp_designation_id__dashboard_id=3),emp_comp_id=dash_details.emp_comp_id,)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'exe_obj':exe_obj}
        
    return render(request,'DAM_hr_teecaller_watedata.html',content)


# Data Bank Section ------------------

def DAM_dataBank(request):
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
                   'notifications':notifications,
                   }
        
    return render(request,'DAM_dataBank.html',content)


def DAM_dataBnak_remove(request,dBID):
    data_leads = DataBank.objects.get(id=dBID)
    data_leads.delete()
    messages.error(request, "Lead Removed from DataBank.")
    return redirect('DAM_Dashboard_databank')



def DAM_repeat_data(request):
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

        source_objs = PlatForms.objects.filter(company_Id__id=dash_details.emp_comp_id.id)

        duplicate_emails = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

           
        duplicate_phones = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

            # Combine duplicate email IDs and phone numbers
        duplicate_values = set([item['lead_email'] for item in duplicate_emails] + [item['lead_contact'] for item in duplicate_phones])

            # Filter DataBank objects based on duplicate values
        DB_data = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id).order_by('Genarated_date')
            
           
        dataBank_count = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id).order_by('Genarated_date').count()
        
        if request.POST:
            
            d1 = request.POST['fdate']
            d2 = request.POST['edate']

            print('-------------------')
            print(d1,d2)

            duplicate_emails = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

            # Find duplicate phone numbers in Lead model
            duplicate_phones = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

            # Combine duplicate email IDs and phone numbers
            duplicate_values = set([item['lead_email'] for item in duplicate_emails] + [item['lead_contact'] for item in duplicate_phones])

            # Filter DataBank objects based on duplicate values
            DB_data = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | 
                                              Q(lead_Id__lead_contact__in=duplicate_values),
                                              lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,
                                              Genarated_date__gte=d1,Genarated_date__lte=d2).order_by('Genarated_date')
            
           
            dataBank_count = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | 
                                                     Q(lead_Id__lead_contact__in=duplicate_values),
                                                     lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,
                                                     Genarated_date__gte=d1,Genarated_date__lte=d2).order_by('Genarated_date').count()
          
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                    'DB_data':DB_data, 'dataBank_count':dataBank_count,
                   'clients_objs':clients_objs,'source_objs':source_objs}
        
        
        return render(request,'DAM_repeatData.html',content)
    

   

def DataBankRepeat_load(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

       

        try:

            duplicate_emails = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

            # Find duplicate phone numbers in Lead model
            duplicate_phones = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

            # Combine duplicate email IDs and phone numbers
            duplicate_values = set([item['lead_email'] for item in duplicate_emails] + [item['lead_contact'] for item in duplicate_phones])

            # Filter DataBank objects based on duplicate values
            DB_data = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id).order_by('Genarated_date')
            
           
            dataBank_count = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id).order_by('Genarated_date').count()
            
            data_list = []
            
            for lead in DB_data:
                    
                    data = {
                   
                    'lead_status':lead.lead_status,
                    'Genarated_date': lead.Genarated_date,
                    'lead_name': lead.lead_Id.lead_name,
                    'lead_email': lead.lead_Id.lead_email,
                    'lead_contact': lead.lead_Id.lead_contact,
                    'id': lead.id,
                    'lead_source':lead.lead_Id.lead_source,
                    'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                    'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                    'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                    'c_status': lead.current_status,
                    }
                    data_list.append(data)

            success = True
            message = "Operation successful"



                # Return a JSON response with lead categories
            return JsonResponse({'success': success, 'message': message,'leads_data': data_list,'dataBank_count':dataBank_count,})
          

        except Exception as e:
            # Handle exceptions and return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': str(e)})
        


def fetch_leadrepaet_categories(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        try:
            # Retrieve client ID from query parameters
            client_id = request.GET.get('client_id', None)
        

            if client_id is not None:
                # Fetch lead categories based on the selected client ID
                lead_categories = LeadCategory_Register.objects.filter(cTaskId__client_Id__id=client_id)
            
                # Convert lead categories to a list of dictionaries
                lead_categories_list = [{'id': category.id, 'name': category.lead_collection_for} for category in lead_categories]

                duplicate_emails = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

                # Find duplicate phone numbers in Lead model
                duplicate_phones = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

                # Combine duplicate email IDs and phone numbers
                duplicate_values = set([item['lead_email'] for item in duplicate_emails] + [item['lead_contact'] for item in duplicate_phones])

                # Filter DataBank objects based on duplicate values
                DB_data = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,lead_Id__lead_work_regId__clientId__id=client_id).order_by('Genarated_date')
                
            
                dataBank_count = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,lead_Id__lead_work_regId__clientId__id=client_id).order_by('Genarated_date').count()

            
                data_list = []
            
                for lead in DB_data:
                    
                    data = {
                    
                    'lead_status':lead.lead_status,
                    'Genarated_date': lead.Genarated_date,
                    'lead_name': lead.lead_Id.lead_name,
                    'lead_email': lead.lead_Id.lead_email,
                    'lead_contact': lead.lead_Id.lead_contact,
                    'id': lead.id,
                    'lead_source':lead.lead_Id.lead_source,
                    'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                    'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                    'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                    'c_status': lead.current_status,
                    }
                    data_list.append(data)

                success = True
                message = "Operation successful"



                # Return a JSON response with lead categories
                return JsonResponse({'success': success, 'message': message,'dataBank_count':dataBank_count,'lead_categories': lead_categories_list,'leads_data': data_list})
            else:
                # Handle the case where client_id is not provided
                raise ValueError("Client ID is not provided in the request.")

        except Exception as e:
            # Handle exceptions and return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': str(e)})
        

def fetch_lead_repatecategory(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        try:
        
            category_id = request.GET.get('category_id', None)
        

            if category_id is not None:
            

                leads_obj = DataBank.objects.filter(lead_Id__lead_category_id__id=category_id)
                
                lead_executive_list = [{'id': leads.lead_Id.lead_collect_Emp_id.id, 'name': leads.lead_Id.lead_collect_Emp_id.emp_name} for leads in leads_obj]

                duplicate_emails = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

                    # Find duplicate phone numbers in Lead model
                duplicate_phones = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

                    # Combine duplicate email IDs and phone numbers
                duplicate_values = set([item['lead_email'] for item in duplicate_emails] + [item['lead_contact'] for item in duplicate_phones])

                    # Filter DataBank objects based on duplicate values
                DB_data = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,lead_Id__lead_category_id__id=category_id).order_by('Genarated_date')
                    
                
                dataBank_count = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id,lead_Id__lead_category_id__id=category_id).order_by('Genarated_date').count()

               
                data_list = []
            
                for lead in DB_data:
                    
                    data = {
                    'lead_status':lead.lead_status,
                    'Genarated_date': lead.Genarated_date,
                    'lead_name': lead.lead_Id.lead_name,
                    'lead_email': lead.lead_Id.lead_email,
                    'lead_contact': lead.lead_Id.lead_contact,
                    'id': lead.id,
                    'lead_source':lead.lead_Id.lead_source,
                    'client_name':lead.lead_Id.lead_work_regId.clientId.client_name,
                    'lead_collection_for':lead.lead_Id.lead_category_id.lead_collection_for,
                    'emp_name': lead.lead_Id.lead_collect_Emp_id.emp_name,
                    'c_status': lead.current_status,
                    }
                    data_list.append(data)

                success = True
                message = "Operation successful"



                # Return a JSON response with lead categories
                return JsonResponse({'success': success, 'message': message,'dataBank_count':dataBank_count,'lead_executive_list': lead_executive_list,'leads_data': data_list})
            else:
                # Handle the case where client_id is not provided
                raise ValueError("Client ID is not provided in the request.")

        except Exception as e:
            # Handle exceptions and return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': str(e)})



def DAM_waste_repeat_dateApprove(request,rwaID):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        db = DataBank.objects.get(id=rwaID)
        db.current_status ='Marked as Waste'
        db.save()


        waste = Waste_Leads()
        waste.leadId = db.lead_Id
        waste.dbId = db
        waste.client_id = db.lead_Id.lead_work_regId.clientId
        waste.TC_Id = dash_details
        waste.Status = 1
        waste.reason = 'This lead is already available in our Data Bank.( Email id or Phone number exist. )'
        waste.save()

        

        success_text='Data Marked as waste successfully.'
        success = True

        # Waste Data notification----

        emp_obj = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=1)

        for emp in emp_obj:

            notific_obj = Notification()
            notific_obj.emp_id = emp
            notific_obj.notific_head ='New waste Lead added.'
            notific_obj.notific_content = (
                dash_details.emp_name +
                ' ( ' +
                dash_details.emp_designation_id.desig_name +
                ' ) ' +
                ' has marked the lead ' +
                db.lead_Id.lead_name +
                ' ( ' +
                db.lead_Id.lead_category_id.lead_collection_for +
            ' ) as a waste lead. This lead is already available in our Data Bank.( Email id or Phone number exist. )'
            )

            notific_obj.notific_time = timezone

            notific_obj.save()

        clients_objs = ClientTask_Register.objects.filter(task_name='Lead Collection',cTcompId__id=dash_details.emp_comp_id.id)

        source_objs = PlatForms.objects.filter(company_Id__id=dash_details.emp_comp_id.id)

        duplicate_emails = Leads.objects.values('lead_email').annotate(email_count=Count('lead_email')).filter(email_count__gt=1)

           
        duplicate_phones = Leads.objects.values('lead_contact').annotate(phone_count=Count('lead_contact')).filter(phone_count__gt=1)

            # Combine duplicate email IDs and phone numbers
        duplicate_values = set([item['lead_email'] for item in duplicate_emails] + [item['lead_contact'] for item in duplicate_phones])

            # Filter DataBank objects based on duplicate values
        DB_data = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id).order_by('Genarated_date')
            
           
        dataBank_count = DataBank.objects.filter(Q(lead_Id__lead_email__in=duplicate_values) | Q(lead_Id__lead_contact__in=duplicate_values),lead_Id__lead_collect_Emp_id__emp_comp_id__id=dash_details.emp_comp_id.id).order_by('Genarated_date').count()


    content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                    'DB_data':DB_data, 'dataBank_count':dataBank_count,
                     'success_text':success_text,
                   'success':success,
                   'clients_objs':clients_objs,'source_objs':source_objs}
        
        
    return render(request,'DAM_repeatData.html',content)


def DAM_logout(request):
    request.session['emp_id'] = ''
    return render(request,'login.html')



def Dm_dataReports(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        Hr_objs = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details.emp_comp_id)
        Hr_objs_count = Hr_objs.count()

        all_report_objs = []

        if request.POST:
             
             d1 = request.POST['fdate']
             d2 = request.POST['edate']

           

             for hr in Hr_objs:

                assign_objs = Leads_assignto_tc.objects.filter(TC_Id=hr,Assign_Date__gte=d1,Assign_Date__lte=d2)

                HR_NAME = hr.emp_name
                AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
                ALP = assign_objs.filter(Status=0).count()
                FLP = assign_objs.filter(Status=1).count()
                CL = assign_objs.filter(Status=2).count()
                JL = Leads_assignto_tc.objects.filter(TC_Id=hr,Status=2,Update_Action=1,Update_Date__gte=d1,Update_Date__lte=d2).count()
                WL = Waste_Leads.objects.filter(TC_Id=hr,waste_marked_Date__gte=d1,waste_marked_Date__lte=d2).count()

                # Append the data to all_report_objs as a dictionary
                all_report_objs.append({
                    'HR_NAME': HR_NAME,
                    'AL': AL,
                    'ALP': ALP,
                    'FLP': FLP,
                    'CL': CL,
                    'JL': JL,
                    'WL': WL
                })

        
        else:

            for hr in Hr_objs:
                assign_objs = Leads_assignto_tc.objects.filter(TC_Id=hr)
                HR_NAME = hr.emp_name
                AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
                ALP = assign_objs.filter(Status=0).count()
                FLP = assign_objs.filter(Status=1).count()
                CL = assign_objs.filter(Status=2).count()
                JL = Leads_assignto_tc.objects.filter(TC_Id=hr,Status=2,Update_Action=1).count()
                WL = Waste_Leads.objects.filter(TC_Id=hr).count()

                # Append the data to all_report_objs as a dictionary
                all_report_objs.append({
                    'HR_NAME': HR_NAME,
                    'AL': AL,
                    'ALP': ALP,
                    'FLP': FLP,
                    'CL': CL,
                    'JL': JL,
                    'WL': WL
                })

        assign_objs = Leads_assignto_tc.objects.filter(client_id__compId=dash_details.emp_comp_id,Assign_Date=date.today())
        AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
        ALP = assign_objs.filter(Status=0).count()
        FLP = assign_objs.filter(Status=1).count()
        CL = assign_objs.filter(Status=2).count()
        JL = Leads_assignto_tc.objects.filter(client_id__compId=dash_details.emp_comp_id,Status=2,Update_Action=1,Update_Date=date.today()).count()
        WL = Waste_Leads.objects.filter(client_id__compId=dash_details.emp_comp_id,waste_marked_Date=date.today()).count()
       
     
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Hr_objs':Hr_objs,'Hr_objs_count':Hr_objs_count,
                   'AL':AL,'ALP':ALP,'FLP':FLP,'CL':CL,'JL':JL,'WL':WL,
                   'assign_objs':assign_objs,
                   'all_report_objs':all_report_objs,'pk':0
                    }
        
    return render(request,'DAM_ALReport.html',content)


def Dm_hrReport_dateFetch(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        Hr_objs = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details.emp_comp_id)
        Hr_objs_count = Hr_objs.count()

        all_report_objs = []

        for hr in Hr_objs:
            assign_objs = Leads_assignto_tc.objects.filter(TC_Id=hr)
            HR_NAME = hr.emp_name
            AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
            ALP = assign_objs.filter(Status=0).count()
            FLP = assign_objs.filter(Status=1).count()
            CL = assign_objs.filter(Status=2).count()
            JL = Leads_assignto_tc.objects.filter(TC_Id=hr,Status=2,Update_Action=1).count()
            WL = Waste_Leads.objects.filter(TC_Id=hr).count()

            # Append the data to all_report_objs as a dictionary
            all_report_objs.append({
                'HR_NAME': HR_NAME,
                'AL': AL,
                'ALP': ALP,
                'FLP': FLP,
                'CL': CL,
                'JL': JL,
                'WL': WL
            })


        hr_assign_dates = Leads_assignto_tc.objects.filter(TC_Id__id=pk).values('Assign_Date').annotate(count=Count('id')).order_by('-Assign_Date')
        hr_assign_dates_count = hr_assign_dates.count()

        assign_objs = Leads_assignto_tc.objects.filter(TC_Id__id=pk)
        AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
        ALP = assign_objs.filter(Status=0).count()
        FLP = assign_objs.filter(Status=1).count()
        CL = assign_objs.filter(Status=2).count()
        JL = assign_objs.filter(TC_Id__id=pk,Status=2,Update_Action=1).count()
        WL = Waste_Leads.objects.filter(TC_Id__id=pk).count()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Hr_objs':Hr_objs,'Hr_objs_count':Hr_objs_count,
                   'hr_assign_dates_count':hr_assign_dates_count,
                   'hr_assign_dates':hr_assign_dates,
                   'AL':AL,'ALP':ALP,'FLP':FLP,'CL':CL,'JL':JL,'WL':WL,'pk':pk,
                   'assign_objs':assign_objs,'all_report_objs':all_report_objs
                   }
        
    return render(request,'DAM_ALReport.html',content)


def Dm_SingleDateFetch(request,strDate,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        Hr_objs = EmployeeRegister_Details.objects.filter(emp_designation_id__dashboard_id=4,emp_comp_id=dash_details.emp_comp_id)
        Hr_objs_count = Hr_objs.count()

        all_report_objs = []

        for hr in Hr_objs:
            assign_objs = Leads_assignto_tc.objects.filter(TC_Id=hr)
            HR_NAME = hr.emp_name
            AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
            ALP = assign_objs.filter(Status=0).count()
            FLP = assign_objs.filter(Status=1).count()
            CL = assign_objs.filter(Status=2).count()
            JL = Leads_assignto_tc.objects.filter(TC_Id=hr,Status=2,Update_Action=1).count()
            WL = Waste_Leads.objects.filter(TC_Id=hr).count()

            # Append the data to all_report_objs as a dictionary
            all_report_objs.append({
                'HR_NAME': HR_NAME,
                'AL': AL,
                'ALP': ALP,
                'FLP': FLP,
                'CL': CL,
                'JL': JL,
                'WL': WL
            })


        hr_assign_dates = Leads_assignto_tc.objects.filter(TC_Id__id=pk).values('Assign_Date').annotate(count=Count('id')).order_by('-Assign_Date')
        hr_assign_dates_count = hr_assign_dates.count()

        assign_objs = Leads_assignto_tc.objects.filter(TC_Id__id=pk,Assign_Date=strDate)
        AL = assign_objs.filter(dataBank_ID__lead_allocate_status=1).count()
        ALP = assign_objs.filter(Status=0).count()
        FLP = assign_objs.filter(Status=1).exclude(Response='Mark as waste').count()
       
        CL = assign_objs.filter(Status=2).count()
        JL =  Leads_assignto_tc.objects.filter(TC_Id__id=pk,Status=2,Update_Action=1,Update_Date=strDate).count()
        WL = Waste_Leads.objects.filter(TC_Id__id=pk,waste_marked_Date=strDate).count()

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Hr_objs':Hr_objs,'Hr_objs_count':Hr_objs_count,
                   'hr_assign_dates_count':hr_assign_dates_count,
                   'hr_assign_dates':hr_assign_dates,
                   'AL':AL,'ALP':ALP,'FLP':FLP,'CL':CL,'JL':JL,'WL':WL,'pk':pk,
                   'assign_objs':assign_objs,'all_report_objs':all_report_objs
                   }
        
    return render(request,'DAM_ALReport.html',content)


def DAM_Hr_JoinedLead(request,pk):
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
            Hr_obj = EmployeeRegister_Details.objects.get(id=pk)
        except EmployeeRegister_Details.DoesNotExist:
            return redirect('Dm_dataReports')

        assign_objs =  Leads_assignto_tc.objects.filter(TC_Id__id=pk,Status=2,Update_Action=1)
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Hr_obj':Hr_obj,
                   'assign_objs':assign_objs
                   }
        
        return render(request,'DAM_Hr_JoinedList.html',content)


def DAM_Hr_LeadStatusChange(request,pk):
    assign_obj =  Leads_assignto_tc.objects.get(id=pk)

    la = Leads_assignto_tc.objects.get(id=pk)
    la.Update_Action = 0
    la.Status = 1
    la.Next_update_date = date.today()
    la.Update_Date = date.today()
    la.save()

    FH_obj = FollowupHistory.objects.filter(hs_lead_Id=la.leadId,hr_telecaller_Id=la.TC_Id).last()
    FH_obj.delete()

    db_obj = DataBank.objects.get(id=la.dataBank_ID.id)
    db_obj.followup_date = None
    db_obj.lead_status = 'Opend'
    db_obj.save()
    messages.success(request,f"{assign_obj.leadId.lead_name } joind status changed.")
    return redirect('DAM_Hr_JoinedLead',assign_obj.TC_Id.id)



def lead_track(request,dbid):
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
            db = DataBank.objects.get(id=dbid) 
            wl_lead = Waste_Leads.objects.filter(leadId=db.lead_Id).last()
            fd_objs = FollowupDetails.objects.filter(lead_Id=db.lead_Id).order_by('-id')
            fl_history = FollowupHistory.objects.filter(hs_lead_Id=db.lead_Id).order_by('-id')
            fields_obj = lead_Details.objects.filter(leadId=db.lead_Id)
       
    
        except Waste_Leads.DoesNotExist:
            return redirect('DAM_Dashboard_databank')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'db': db,
                    'fd_objs':fd_objs,  
                    'fl_history':fl_history,
                    'fields_obj':fields_obj,
                    'wl_lead':wl_lead
                   
                   }
        
        return render(request,'DAM_leadTrack.html',content)