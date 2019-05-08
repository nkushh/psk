from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from .forms import UserRegistrationForm, UserUpdateForm

# Create your views here.
@login_required(login_url='login')
def all_accounts(request):
	users = UserProfile.objects.select_related('user')
	context = {
		'users' : users,
	}
	template = 'authentication/accounts.html'
	return render(request, template, context)

@login_required(login_url='login')
def register_user(request):
	if request.method=='POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			first_name = userObj['first_name']
			last_name = userObj['last_name']
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']
			# Profile
			psk_region = request.POST['psk_region']
			usertype = request.POST['usertype']
			phone_no = request.POST['phone_no']

			if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				user = User.objects.create_user(username, email, password)
				user.first_name = first_name
				user.last_name = last_name
				user.save()

				# Create a blank profile for the new user
				UserProfile.objects.create(user=user, psk_region=psk_region, usertype=usertype, phone_no=phone_no)
				messages.success(request, "Success! Account details successfully recorded.")
				return redirect('authentication:accounts')
			else:
				messages.warning(request, "Error! Username with that email already exists")
				return redirect('authentication:register_user')

	else:
		context = {
			'form' : UserRegistrationForm(),
		}
		
		template = 'authentication/register-user.html'
	return render(request, template, context)

def create_account(request):
	if request.method=='POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']

			if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				user = User.objects.create_user(username, email, password)

				# Create a blank profile for the new user
				UserProfile.objects.create(user=user)

				messages.success(request, "Success! {} your account was successfully created. Login!".format(username))
				return redirect('login')
			else:
				messages.warning(request, "Error! Username with that email already exists")
				return redirect('authentication:register')

	else:
		form = UserRegistrationForm()
	return render(request, 'authentication/create-account.html', {'form' : form})


@login_required(login_url='login')
def update_account(request, account_pk):
	account = get_object_or_404(User, pk=account_pk)
	
	if request.method=='POST':
		form = UserUpdateForm(request.POST, instance=account)
		if form.is_valid():
			acc = form.save()
			acc.set_password(request.POST['password'])
			update_session_auth_hash(request, account)
			acc.save()

			messages.success(request, "Success! Account detail successfully updated.")
			return redirect('authentication:accounts')

	else:
		form = UserUpdateForm(instance=account)
	return render(request, 'authentication/edit-account.html', {'form' : form})

@login_required(login_url='login')
def deactivate_account(request, account):
	user = get_object_or_404(User, pk=account)
	user.is_active = False
	farm.save()
	messages.success(request, 'Account successfully deactivated')
	return redirect('authentication:accounts')

@login_required(login_url='login')
def activate_account(request, account):
	user = get_object_or_404(User, pk=account)
	user.is_active = True
	farm.save()
	messages.success(request, 'Account successfully re-activated')
	return redirect('authentication:accounts')


@login_required(login_url='login')
def delete_account(request, account):
	user = get_object_or_404(User, pk=account)
	user.delete()
	messages.success(request, 'Account successfully deleted')
	return redirect('authentication:accounts')

