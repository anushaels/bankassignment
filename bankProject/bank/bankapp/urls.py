from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('account/', views.manage_account, name='manage_account'),
    path('account/', views.manage_account, name='manage_account'),
    path('transaction/', views.transaction, name='transaction'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
]

