from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
  USER_TYPE_CHOICES = (
    ('admin','admin'),
    ('trucker','trucker')
  )
  id = models.AutoField(primary_key=True)
  user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='trucker')
  phone_number = models.CharField(max_length=15, null=False, blank=False)

  def __repr__(self) -> str:
    return f'{self.username} - {self.user_type} - {self.phone_number}'
  
  def get_user_type(self):
    return self.user_type
  
class Invitation(models.Model):
  code = models.CharField(max_length=50, unique=True)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
  user_type = models.CharField(max_length=10,choices=User.USER_TYPE_CHOICES,default='trucker')
  is_used = models.BooleanField(default=False)

