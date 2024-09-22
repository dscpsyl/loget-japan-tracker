from django.urls import path

from . import views

app_name = "tracker"
urlpatterns = [
    path("", views.index, name="index"),
    path("tracker/", views.tracker, name="tracker"),
    
    path("settings/", views.userView, name="user"),
    
    path('login/', views.loginView, name='login'),
    path('signup/', views.signupView, name='signup'),
    path('logout/', views.logoutView, name='logout'),
    
    path('signup/success/', views.signupSuccess, name='signup_success'),
    path('logout/success/', views.logoutSuccess, name='logout_success')
]