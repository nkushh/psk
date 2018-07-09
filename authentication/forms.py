from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):
	USERTYPES = (('', '--Select usertype--',), ('Admin', 'Admin',), ('Coordinator', 'Coordinator',), ('Data clerk', 'Data clerk',), ('Field Assistant', 'Field Assistant',))
	REGIONS = (('', '--Select region--',), ('Central', 'Central'), ('Central Nyanza', 'Central Nyanza'), ('Coast', 'Coast',), ('HQ', 'HQ',), ('Mountain', 'Mountain',), ('Nairobi 2', 'Nairobi 2',), ('North Rift', 'North Rift',), ('South Nyanza', 'South Nyanza',), ('South Rift', 'South Rift',), ('Western', 'Western'))

	username = forms.CharField(required=True, label='Username', max_length=32)
	email = forms.EmailField(required=True, label='Email', max_length=200)
	usertype = forms.ChoiceField(widget=forms.Select(attrs={'id': 'usertype-input'}), choices=USERTYPES)
	psk_region = forms.ChoiceField(widget=forms.Select(attrs={'id' : 'div-id-psk-region', 'style': 'display:block'}), choices=REGIONS, required=False)
	phone_no = forms.CharField(required=True, label='Phone No', max_length=10)
	password = forms.CharField(required=True, label='Password', max_length=32, widget=forms.PasswordInput())

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User

		fields = ['first_name', 'last_name', 'username', 'email', 'password']
		# widgets= {
		# 	'password':TextInput(attrs={'type':'password'})
		# }

class CustomAuthenticationForm(AuthenticationForm):
	def confirm_login_allowed(self, user):
		if not user.is_active or not user.is_validated:
			messages.warning(request, 'Account credentials not valid.')
