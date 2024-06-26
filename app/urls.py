from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.index,name="index"),
  path('login',views.login_view,name="login"),
  path('logout', views.logout_view, name="logout"),
  path('register',views.register_view,name="register"),
  path('invite',views.invite_view,name="invite"),
  path('register_company',views.register_company_view,name="register_company"),
  path('register_vehicle',views.register_vehicle_view,name="register_vehicle"),
  path('vehicles',views.vehicles_view,name="vehicles"),
  path('register_cargo',views.register_cargo_view,name="register_cargo"),
  path('cargo',views.cargo_view,name="cargo"),
  path('map', views.map_view, name="map")
]