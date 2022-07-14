from django import forms

from .models import *


ValidationError = forms.ValidationError


class LoginForm(forms.Form):
	username = forms.CharField(max_length=64, required=True)
	password = forms.CharField(max_length=128, required=True)

class RegisterForm(forms.ModelForm):
	confirm_password = forms.CharField(max_length=128, required=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'confirm_password', 'accept_terms_and_conditions']

	def clean(self):
		cleaned_data = super().clean()
		print(cleaned_data, 'form')

		if cleaned_data['accept_terms_and_conditions'] == False:
			self.add_error('You have to accept our terms and conditions to use this site', field='__all__')
			
		if cleaned_data['confirm_password'] != cleaned_data['password']:
			self.add_error(error='Password and Confirm password does not match', field='confirm_password')

		for char in cleaned_data['username']:
			if not char.isidentifier():
				self.add_error(error='Username only allow _ as special character or must starts with alphabet', field='username')

			if char.isupper():
				self.add_error(error='Username must be in lowercase', field='username')


class AccountConfirmationForm(forms.ModelForm):
	email = forms.EmailField(max_length=255, required=True)

	class Meta:
		model = AccountConfirmation
		fields = ['otp', 'email']