from django.shortcuts import render
from xmlrpc.client import ServerProxy
from django.contrib import messages
import ast

#General configuration
odoo_database = None
odoo_server = None
odoo_username = None
odoo_password = None
models = None
uid = None

# Create your views here.

def login(request):
    #bloqué l'accès sans une connection à odoo
    if not request.user.is_authenticated:
        return render(request,'warning.html')
    
    setConnexion(request.user)
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        return get_res_patner(request,name,email,password)
    # Partner is not present in the database
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        return create_res_partner(request,name,email,password)
    return render(request,'register.html')

def apartments(request, res_partner):
    # Fetch apartment records
    result = models.execute_kw(odoo_database, uid, odoo_password, 'realtor.apartment', 'search', [[]])
    apartments = models.execute_kw(odoo_database, uid, odoo_password, 'realtor.apartment', 'read', [result])
    # Fetch product records
    result = models.execute_kw(odoo_database, uid, odoo_password, 'product.product', 'search', [[]])
    products = models.execute_kw(odoo_database, uid, odoo_password, 'product.product', 'read', [result])
    # Render template with apartment and product data
    return render(request, 'apartments.html', {'apartments': apartments, 'partner': res_partner, 'products': products})

def get_res_patner(request,name,email,password):

    partner = models.execute_kw(odoo_database, uid, odoo_password, 'res.partner', 'search', [[['name', '=', name],[
        'email','=',email],['password','=',password]]])
    if len(partner) > 0:
        records = models.execute_kw(odoo_database, uid, odoo_password, 'res.partner', 'read', [partner], {'fields': ['name', 'email']})
        return apartments(request,records)
    else:
        messages.error(request, 'There seems to be an issue with your credentials !')
        return render(request,'login.html')

def create_res_partner(request,name,email,password):
    
    # Create a new res_partner object in Odoo
    partner_id = models.execute_kw(odoo_database, uid, odoo_password, 'res.partner', 'create', [{
    'name': name,
    'email': email,
    'password': password,}])
    return get_res_patner(request,name,email,password)

def offer(request):
    if request.method == 'POST':
        apartment_detail = request.POST['apartement_detail']
        partner = request.POST['partners']
        offer = request.POST['offer']
        partner = ast.literal_eval(partner)
        updateAfterOffer(apartment_detail,offer,partner) 
   
    return apartments(request,partner)

def updateAfterOffer(apartment_detail,offer,partner):

    apartment_detail = ast.literal_eval(apartment_detail)
    models.execute_kw(odoo_database, uid, odoo_password, 'realtor.apartment', 'write',
                    [[apartment_detail['id']], {'best_offer_price': offer}])
    new_partner = models.execute_kw(odoo_database, uid, odoo_password, 'res.partner', 'read', [partner[0]['id']], {'fields': ['name', 'email','password']})
     
    #mise à jour suite à l'offre du meilleur acheteur
    models.execute_kw(odoo_database, uid, odoo_password, 'realtor.apartment', 'write', [[apartment_detail['id']],{'best_offer_buyer': new_partner[0]['id']}])

def setConnexion(user):
    global odoo_server
    odoo_server = user.url_odoo
    global odoo_database
    odoo_database = user.db_name
    global odoo_password
    odoo_password = user.odoo_password
    global odoo_username
    odoo_username = user.username
    global uid
    common = ServerProxy('{}/xmlrpc/2/common'.format(odoo_server))
    uid = common.authenticate(odoo_database, odoo_username, odoo_password, {})
    global models
    models = ServerProxy('{}/xmlrpc/2/object'.format(odoo_server))