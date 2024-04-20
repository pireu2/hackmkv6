from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator



class User(AbstractUser):
  USER_TYPE_CHOICES = (
    ('owner','owner'),
    ('admin','admin'),
    ('trucker','trucker')
  )
  id = models.AutoField(primary_key=True)
  user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='trucker')
  company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
  phone_number = models.CharField(max_length=15, null=False, blank=False)

  def __repr__(self) -> str:
    return f'{self.username} - {self.user_type} - {self.phone_number}'
  
  def get_user_type(self):
    return self.user_type
  def get_company(self):
    return self.company
  
class Company(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)

  def get_address(self):
    return self.address

class CompanyInvitation(models.Model):
  id = models.AutoField(primary_key=True)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  code = models.CharField(max_length=50, unique=True)
  is_used = models.BooleanField(default=False)
  
class Invitation(models.Model):
  id = models.AutoField(primary_key=True)
  code = models.CharField(max_length=50, unique=True)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
  user_type = models.CharField(max_length=10,choices=User.USER_TYPE_CHOICES,default='trucker')
  is_used = models.BooleanField(default=False)

class Vehicle(models.Model):
  VEHICLE_TYPE_CHOICES = (
    ('minivan','minivan'),
    ('truck','truck'),
    ('car','car')
  )
  id = models.AutoField(primary_key=True)
  plate_number = models.CharField(max_length=10)
  type = models.CharField(max_length=10,choices=VEHICLE_TYPE_CHOICES,default='car')
  model = models.CharField(max_length=50)
  capacity_mass = models.IntegerField(validators=[MinValueValidator(1)])
  capacity_volume = models.IntegerField(validators=[MinValueValidator(1)])
  company = models.ForeignKey(Company, on_delete=models.CASCADE,blank=False,null=False)
  current_location = models.CharField(max_length=100, default="")
  is_active = models.BooleanField(default=True)

class Cargo(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  mass = models.IntegerField(validators=[MinValueValidator(1)])
  volume = models.IntegerField(validators=[MinValueValidator(1)])
  company = models.ForeignKey(Company, on_delete=models.CASCADE,blank=False,null=False)
  source_address = models.CharField(max_length=100,blank=False,null=False)
  destination_address = models.CharField(max_length=100,blank=False,null=False) 
  is_active = models.BooleanField(default=True)

class Route(models.Model):
  id = models.AutoField(primary_key=True)
  vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,blank=False,null=False)
  cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE,blank=False,null=False)
  departure_time = models.DateTimeField(blank=False,null=False)
  arrival_time = models.DateTimeField(blank=False,null=False)
  is_active = models.BooleanField(default=True)