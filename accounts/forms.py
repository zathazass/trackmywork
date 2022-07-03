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
		fields = ['username', 'email', 'password', 'confirm_password']

	def clean(self):
		cleaned_data = super().cleaned_data()

		if cleaned_data['confirm_password'] != cleaned_data['password']:
			raise forms.ValidationError('Password and Confirm password does not match')

		for char in cleaned_data['username']:
			if not char.isidentifier():
				raise forms.ValidationError('Username only allow _ as special character or must starts with alphabet')

			if char.isupper():
				raise forms.ValidationError('Username must be in lowercase')

