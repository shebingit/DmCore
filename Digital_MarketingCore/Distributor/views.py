from django.shortcuts import render,redirect
from Registration_Login.models import *



def Distributor_dashboard(request):
    if 'distr_id' in request.session:
        if request.session.has_key('distr_id'):
            distr_id = request.session['distr_id']
           
        else:
            return redirect('/')
        
        dis_dash = LogRegister_Details.objects.get(id=distr_id)
        dash_details = DistributorRegister_Details.objects.get(logdis_id=dis_dash)
        
        content = {'dis_dash':dis_dash,'dash_details':dash_details}

        return render(request,'AD_dashboard.html',content)

    else:
            return redirect('/')
    

def Distributor_logout(request):
    request.session.pop('distr_id', None)
    return redirect('login_page')
