from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import User, Invitation

# Create your views here.
@login_required
def index(request):
  if request.method == "GET":
    return render(request,"app/index.html")
  

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
    if not username or not password or not phone_number or not invitation_code or not email:
      return render(request,"app/register.html",{"error":"All fields are required"})
    try:
      invitation = Invitation.objects.get(code=invitation_code,is_used = False)
    except Invitation.DoesNotExist:
      return render(request,"app/register.html",{"error":"Invalid invitation code"})
    if password != conf_password:
      return render(request,"app/register.html",{"error":"Passwords do not match"})
    if User.objects.filter(username=username).exists():
      return render(request,"app/register.html",{"error":"Username already exists"})
    if User.objects.filter(phone_number=phone_number).exists():
      return render(request,"app/register.html",{"error":"Phone number already exists"})
    if User.objects.filter(email=email).exists():
      return render(request,"app/register.html",{"error":"Email already exists"})
    try:
      invitation = Invitation.objects.get(code=invitation_code,is_used = False)
    except Invitation.DoesNotExist:
      return render(request,"app/register.html",{"error":"Invalid invitation code"})
    user_type = invitation.user_type
    User.objects.create_user(username=username,password=password,
                             phone_number=phone_number,user_type=user_type)
    invitation.is_used = True
    invitation.save()
    return render(request,"app/login.html")



def login_view(request):
  if request.user.is_authenticated:
    return redirect("index")
  if request.method == "GET":
    return render(request,"app/login.html")
  elif request.method == "POST":
    username = request.POST.get("username").strip()
    password = request.POST.get("password").strip()
    print(username,password)
    user = authenticate(request,username=username,password=password)
    print(user)
    if user is not None:
      login(request,user)
      return render(request,"app/index.html")
    else:
      return render(request,"app/login.html",{"error":"Invalid credentials"})

@login_required
def logout_view(request):
  logout(request)
  return redirect("login")