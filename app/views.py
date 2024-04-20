from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import User, Invitation, CompanyInvitation, Company, Vehicle
import uuid

# Create your views here.
def index(request):
  if request.user.is_authenticated:
    if request.method == "GET":
      return render(request,"app/index.html")
  else:
    return redirect("login")
  

def register_company_view(request):
  if request.user.is_authenticated:
    return redirect("index")
  if request.method == "GET":
    return render(request,"app/register_company.html")
  elif request.method == "POST":
    company_name = request.POST.get("company_name").strip()
    company_address = request.POST.get("company_address").strip()
    if not company_name or not company_address:
      return render(request,"app/register_company.html",{"error":"All fields are required"})
    code = uuid.uuid4()
    company = Company.objects.create(name=company_name,address=company_address)
    invitation = CompanyInvitation.objects.create(code=code,company=company)
   
    return render(request,"app/register_company.html",{"invitation_message":code})

def register_view(request):
  if request.user.is_authenticated:
    return redirect("index")
  if request.method == "GET":
    return render(request,"app/register.html")
  elif request.method == "POST":
    username = request.POST.get("username").strip()
    password = request.POST.get("password").strip()
    conf_password = request.POST.get("conf-password").strip()
    email = request.POST.get("email").strip()
    phone_number = request.POST.get("phone").strip()
    invitation_code = request.POST.get("invitation").strip()

    invitation_type = None
    if not username or not password or not phone_number or not invitation_code or not email:
      return render(request,"app/register.html",{"error":"All fields are required"})
    try:
      invitation = Invitation.objects.get(code=invitation_code,is_used = False)
      invitation_type = 'user'
    except Invitation.DoesNotExist:
      try:
        company_invitation = CompanyInvitation.objects.get(code=invitation_code,is_used = False)
        invitation_type = 'company'
      except CompanyInvitation.DoesNotExist:
        return render(request,"app/register.html",{"error":"Invalid invitation code"})
      
    if invitation_type == 'user':
      user_type = invitation.user_type
      company = Company.objects.get(id=invitation.created_by.get_company().id)
      invitation.is_used = True
      invitation.save()
    else:
      user_type = 'owner'
      company = company_invitation.company
      company_invitation.is_used = True
      company_invitation.save()

    if password != conf_password:
      return render(request,"app/register.html",{"error":"Passwords do not match"})
    if User.objects.filter(username=username).exists():
      return render(request,"app/register.html",{"error":"Username already exists"})
    if User.objects.filter(phone_number=phone_number).exists():
      return render(request,"app/register.html",{"error":"Phone number already exists"})
    if User.objects.filter(email=email).exists():
      return render(request,"app/register.html",{"error":"Email already exists"})
    User.objects.create_user(username=username,password=password,
                             phone_number=phone_number,user_type=user_type,company = company)
    return redirect("login")



def login_view(request):
  if request.user.is_authenticated:
    return redirect("index")
  if request.method == "GET":
    return render(request,"app/login.html")
  elif request.method == "POST":
    username = request.POST.get("username").strip()
    password = request.POST.get("password").strip()
    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect("index")
    else:
      return render(request,"app/login.html",{"error":"Invalid credentials"})

@login_required
def logout_view(request):
  logout(request)
  return redirect("login")


@login_required
def register_vehicle_view(request):
  if request.method == 'GET':
    return render(request, "app/register_vehicle.html")
  elif request.method == 'POST':
    vehicle_number = request.POST.get("plate_number")
    vehicle_type = request.POST.get("vehicle_type")
    vehicle_model = request.POST.get("model")
    vehicle_capacity_mass = request.POST.get("capacity_mass")
    vehicle_capacity_volume = request.POST.get("capacity_volume")
    vehicle_company = request.user.company
    if not vehicle_number or not vehicle_type or not vehicle_model or not vehicle_capacity_mass or not vehicle_capacity_volume:
      return render(request, "app/register_vehicle.html", {"error": "All fields are required"})
    if len(vehicle_number) != 10:
      return render(request, "app/register_vehicle.html", {"error": "Plate number must be 10 characters"})
    if Vehicle.objects.filter(plate_number=vehicle_number).exists():
      return render(request, "app/register_vehicle.html", {"error": "Vehicle already exists"})
    Vehicle.objects.create(plate_number=vehicle_number,type=vehicle_type,model=vehicle_model,capacity_mass=vehicle_capacity_mass,capacity_volume=vehicle_capacity_volume,company=vehicle_company)

    
    return redirect("index")
  
@login_required
def vehicles_view(request):
  if request.method == 'GET':
    vehicles = Vehicle.objects.filter(company=request.user.company)
    return render(request, "app/vehicles.html", {"vehicles":vehicles})

@login_required
def invite_view(request):
  if request.method == 'GET':
    if request.user.get_user_type() != 'admin' and request.user.get_user_type() != 'owner':
      return redirect("index")
    return render(request, "app/invite.html")
  elif request.method == 'POST':
    user_type = request.POST.get("user_type")
    user_type = user_type.lower()
    while True:
      invitation_code = uuid.uuid4()
      if not Invitation.objects.filter(code=invitation_code).exists():
        break
    Invitation.objects.create(code=invitation_code,created_by=request.user,user_type=user_type)
    return render(request,"app/invite.html",{"invitation_message":invitation_code})