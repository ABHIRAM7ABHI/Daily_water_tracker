from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('calculate-difference/', views.calculate_difference, name='calculate_difference'),
    path('update-intake/', views.update_water_intake, name='update_water_intake'),
    path('delete-intake/', views.delete_water_intake, name='delete_water_intake'),

]
