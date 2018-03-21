from django.urls import path
from . import views


app_name = 'authentication'
urlpatterns = [
	path('', views.all_accounts, name='accounts'),
	path('register-user', views.register_user, name='register_user'),
	path('update', views.update_account, name='update_account'),
	path('deactivate-account/<int:account>/', views.deactivate_account, name='deactivate-account'),
	path('activate-account/<int:account>/', views.activate_account, name='activate-account'),
	path('delete-account/<int:account>/', views.delete_account, name='delete-account'),
]