from django.shortcuts import render,redirect
from Registration_Login.models import *



def supper_admin_dashboard(request):
    if 'super_admin_id' in request.session:
        if request.session.has_key('super_admin_id'):
            su_admin_id = request.session['super_admin_id']
           
        else:
            return redirect('/')
        
        Super_Admin = LogRegister_Details.objects.get(id=su_admin_id)
        
        content = {'Super_Admin':Super_Admin}

        return render(request,'SA_dashboard.html',content)

    else:
            return redirect('/')
    

def super_admin_logout(request):
    request.session.pop('super_admin_id', None)
    return redirect('login_page')
     

   
