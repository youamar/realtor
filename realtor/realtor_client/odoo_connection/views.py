from django.shortcuts import render
from django.contrib import messages
from . import forms
from . models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from xmlrpc.client import ServerProxy


# Create your views here.

def home(request):
    return render(request,'home.html')

def register(request):
    
    if request.method == 'POST':
        odoo_database = request.POST['db']
        odoo_server = request.POST['url']
        odoo_username = request.POST['username']
        odoo_password = request.POST['odoo_password']

        if(odoo_server != 'http://localhost:8069' and odoo_database != 'db' or odoo_database != 'dev01'):
            messages.error(request, 'Uh oh, there seems to have been a problem with the Odoo database name or URL !')
            return render(request, 'accounts/register.html')
        if( not check_unique_username(odoo_username)):
            messages.error(request, 'Whoops, it looks like that username is already taken !')
            return render(request, 'accounts/register.html')
       
        common = ServerProxy('{}/xmlrpc/2/common'.format(odoo_server))
        uid = common.authenticate(odoo_database, odoo_username, odoo_password, {})
        if not uid:
            messages.error(request, 'Looks like there was a problem with your username or password !')
            return render(request, 'accounts/register.html')

        user = User(url_odoo=odoo_server,db_name=odoo_database,username=odoo_username,password = make_password(odoo_password),odoo_password=odoo_password)
        user.save()
        login(request,user)
        return redirect('odoo_connection')
    return render(request, 'accounts/register.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('odoo_connection')
    
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'],password=form.cleaned_data['odoo_password'])
            if user is not None:
                login(request,user)
                return redirect('odoo_connection')
            else:
                messages.error(request, "Whoops, looks like there's a mistake in your credentials !")
                return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/login.html',context)

"""
Give res_users to the odoo_connection and confirm the connection was without issues to odoo api.
"""
@login_required
def odooUsers(request):
    cur_user = request.user
    # Retourner la list des res_users (test)
    common = ServerProxy('{}/xmlrpc/2/common'.format(cur_user.url_odoo))
    uid = common.authenticate(cur_user.db_name, cur_user.username, cur_user.odoo_password, {})
    models = ServerProxy('{}/xmlrpc/2/object'.format(cur_user.url_odoo))
    result = models.execute_kw(cur_user.db_name, uid, cur_user.odoo_password, 'res.partner', 'search', [[]])
    users = models.execute_kw(cur_user.db_name, uid, cur_user.odoo_password, 'res.partner', 'read', [result])
    # Render the template with the list of users
    return render(request, 'accounts/odoo_connection.html', {'users': users})

def check_unique_username(odoo_username):
    for x in User.objects.all():
        if(x.username == odoo_username):
            return False

    return True