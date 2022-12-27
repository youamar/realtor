from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    odoo_password = forms.CharField(max_length=63,label='Password',widget=forms.PasswordInput)