from django.contrib import admin
from .models import User, Invitation, Company, Vehicle, Cargo, Route
# Register your models here.
admin.site.register(User)
admin.site.register(Invitation)
admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(Cargo)
admin.site.register(Route)
